from __future__ import annotations

import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..industrial_ranking import require_backend
from ..llm_lora import encode_texts, load_lora_lm, lora_sft
from .data import JointData, instruction


@dataclass(frozen=True)
class LSVCRConfig:
    model_name: str = "HuggingFaceTB/SmolLM2-135M"
    dimensions: int = 48
    maximum_users: int = 80
    lora_steps: int = 24
    alignment_steps: int = 80
    finetune_steps: int = 120
    batch_size: int = 24
    maximum_length: int = 12
    learning_rate: float = 6e-4
    temperature: float = 0.07
    vcc_weight: float = 0.5


def prepare_llm_views(data: JointData, root: Path, config: LSVCRConfig, seed: int):
    slug = config.model_name.rsplit("/", 1)[-1].lower()
    cache = root / "lsvcr" / f"{slug}-u{config.maximum_users}-s{seed}.npz"
    if cache.exists():
        payload = np.load(cache)
        return {key: payload[key] for key in ("items", "comments", "teacher_items", "teacher_comments")}, {"lora_trainable": int(payload["lora_trainable"]), "lora_loss_initial": float(payload["lora_loss_initial"]), "lora_loss_final": float(payload["lora_loss_final"]), "cache_hit": True}
    model, tokenizer, trainable = load_lora_lm(config.model_name, seed)
    sft = []
    for row in data.train:
        sft.append((instruction(data, row, "item"), data.item_texts[row.target_item]))
        sft.append((instruction(data, row, "comment"), data.comment_texts[row.target_comment][:100]))
    metrics = lora_sft(model, tokenizer, sft, config.lora_steps, 2, 2e-4, seed)
    item_prompts = [instruction(data, row, "item") for row in (*data.train, *data.test)]
    comment_prompts = [instruction(data, row, "comment") for row in (*data.train, *data.test)]
    views = {
        "items": encode_texts(model, tokenizer, list(data.item_texts), maximum_length=64),
        "comments": encode_texts(model, tokenizer, list(data.comment_texts), maximum_length=96),
        "teacher_items": encode_texts(model, tokenizer, item_prompts),
        "teacher_comments": encode_texts(model, tokenizer, comment_prompts),
    }
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache, **views, lora_trainable=trainable, lora_loss_initial=metrics["initial"], lora_loss_final=metrics["final"])
    return views, {"lora_trainable": trainable, "lora_loss_initial": metrics["initial"], "lora_loss_final": metrics["final"], "cache_hit": False}


def build_model(data: JointData, views, config: LSVCRConfig):
    torch, nn = require_backend()
    item_pad, comment_pad = len(data.item_texts), len(data.comment_texts)

    class LSVCR(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_pad + 1, config.dimensions, padding_idx=item_pad)
            self.comment = nn.Embedding(comment_pad + 1, config.dimensions, padding_idx=comment_pad)
            self.register_buffer("item_text", torch.tensor(np.vstack((views["items"], np.zeros((1, views["items"].shape[1])))), dtype=torch.float32))
            self.register_buffer("comment_text", torch.tensor(np.vstack((views["comments"], np.zeros((1, views["comments"].shape[1])))), dtype=torch.float32))
            self.item_text_project = nn.Linear(views["items"].shape[1], config.dimensions)
            self.comment_text_project = nn.Linear(views["comments"].shape[1], config.dimensions)
            self.position_item = nn.Embedding(config.maximum_length, config.dimensions)
            self.position_comment = nn.Embedding(config.maximum_length, config.dimensions)
            layer = lambda: nn.TransformerEncoderLayer(config.dimensions, 4, 4 * config.dimensions, batch_first=True, norm_first=True, dropout=0.0)
            self.item_encoder = nn.TransformerEncoder(layer(), 2)
            self.comment_encoder = nn.TransformerEncoder(layer(), 2)
            self.item_cross = nn.MultiheadAttention(config.dimensions, 4, batch_first=True)
            self.comment_cross = nn.MultiheadAttention(config.dimensions, 4, batch_first=True)
            self.item_merge = nn.Linear(2 * config.dimensions, config.dimensions)
            self.comment_merge = nn.Linear(2 * config.dimensions, config.dimensions)
            self.item_attention = nn.Linear(config.dimensions, 1)
            self.teacher_item = nn.Linear(views["teacher_items"].shape[1], config.dimensions)
            self.teacher_comment = nn.Linear(views["teacher_comments"].shape[1], config.dimensions)

        def encode(self, items, comments, random_positions=False):
            item_mask, comment_mask = items != item_pad, comments != comment_pad
            width_i, width_c = items.shape[1], comments.shape[1]
            if random_positions and width_i < config.maximum_length:
                pos_i = torch.sort(torch.randperm(config.maximum_length, device=items.device)[:width_i]).values
                pos_c = torch.sort(torch.randperm(config.maximum_length, device=items.device)[:width_c]).values
            else:
                pos_i, pos_c = torch.arange(width_i, device=items.device), torch.arange(width_c, device=items.device)
            item = self.item(items) + self.item_text_project(self.item_text[items]) + self.position_item(pos_i)
            comment = self.comment(comments) + self.comment_text_project(self.comment_text[comments]) + self.position_comment(pos_c)
            item = self.item_encoder(item, src_key_padding_mask=~item_mask)
            comment = self.comment_encoder(comment, src_key_padding_mask=~comment_mask)
            item_cross, _ = self.item_cross(item, comment, comment, key_padding_mask=~comment_mask)
            comment_cross, _ = self.comment_cross(comment, item, item, key_padding_mask=~item_mask)
            item = self.item_merge(torch.cat((item, item_cross), -1))
            comment = self.comment_merge(torch.cat((comment, comment_cross), -1))
            item_weights = self.item_attention(item).squeeze(-1).masked_fill(~item_mask, -1e4).softmax(-1)
            item_pref = (item * item_weights.unsqueeze(-1)).sum(1)
            query = item_pref.unsqueeze(1)
            comment_weights = (comment * query).sum(-1).masked_fill(~comment_mask, -1e4).softmax(-1)
            comment_pref = (comment * comment_weights.unsqueeze(-1)).sum(1)
            return item_pref, comment_pref

        def item_candidates(self):
            indices = torch.arange(item_pad, device=self.item.weight.device)
            return self.item(indices) + self.item_text_project(self.item_text[indices])

        def comment_candidates(self):
            indices = torch.arange(comment_pad, device=self.comment.weight.device)
            return self.comment(indices) + self.comment_text_project(self.comment_text[indices])

    return LSVCR()


def _collate(rows, data, config, device, torch):
    width_i = min(config.maximum_length, max(len(row.item_history) for row in rows))
    width_c = min(config.maximum_length, max(len(row.comment_history) for row in rows))
    items = torch.full((len(rows), width_i), len(data.item_texts), device=device, dtype=torch.long)
    comments = torch.full((len(rows), width_c), len(data.comment_texts), device=device, dtype=torch.long)
    for index, row in enumerate(rows):
        i, c = row.item_history[-width_i:], row.comment_history[-width_c:]
        items[index, -len(i):] = torch.tensor(i, device=device)
        comments[index, -len(c):] = torch.tensor(c, device=device)
    return items, comments


def train_variant(data, views, config: LSVCRConfig, seed: int, aligned: bool):
    torch, _ = require_backend()
    torch.manual_seed(seed)
    rng = random.Random(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = build_model(data, views, config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = {"alignment": [], "finetune": []}
    started = time.perf_counter()
    if aligned:
        model.train()
        for _ in range(config.alignment_steps):
            indices = [rng.randrange(len(data.train)) for _ in range(config.batch_size)]
            rows = [data.train[index] for index in indices]
            items, comments = _collate(rows, data, config, device, torch)
            pv, pc = model.encode(items, comments, random_positions=True)
            ti = model.teacher_item(torch.tensor(views["teacher_items"][indices], device=device))
            tc = model.teacher_comment(torch.tensor(views["teacher_comments"][indices], device=device))
            labels = torch.arange(len(rows), device=device)
            contrast = lambda a, b: torch.nn.functional.cross_entropy(torch.nn.functional.normalize(a, dim=-1) @ torch.nn.functional.normalize(b, dim=-1).T / config.temperature, labels)
            loss = contrast(pv, ti) + contrast(pc, tc) + config.vcc_weight * contrast(pv, pc)
            optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
            losses["alignment"].append(float(loss.detach().cpu()))
    for _ in range(config.finetune_steps):
        rows = [data.train[rng.randrange(len(data.train))] for _ in range(config.batch_size)]
        items, comments = _collate(rows, data, config, device, torch)
        pv, pc = model.encode(items, comments)
        item_logits = pv @ model.item_candidates().T
        comment_logits = pc @ model.comment_candidates().T
        loss = torch.nn.functional.cross_entropy(item_logits, torch.tensor([r.target_item for r in rows], device=device)) + torch.nn.functional.cross_entropy(comment_logits, torch.tensor([r.target_comment for r in rows], device=device))
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
        losses["finetune"].append(float(loss.detach().cpu()))
    result = evaluate(model, data, config, device, torch)
    result.update({"alignment_loss_initial": None if not losses["alignment"] else float(np.mean(losses["alignment"][:10])), "alignment_loss_final": None if not losses["alignment"] else float(np.mean(losses["alignment"][-10:])), "finetune_loss_initial": float(np.mean(losses["finetune"][:10])), "finetune_loss_final": float(np.mean(losses["finetune"][-10:])), "seconds": time.perf_counter() - started})
    return result


def evaluate(model, data, config, device, torch):
    metrics = {"item": [], "comment": []}
    model.eval()
    with torch.inference_mode():
        for row in data.test:
            items, comments = _collate([row], data, config, device, torch)
            pv, pc = model.encode(items, comments)
            for name, scores, target in (("item", pv @ model.item_candidates().T, row.target_item), ("comment", pc @ model.comment_candidates().T, row.target_comment)):
                top = scores[0].topk(min(10, scores.shape[1])).indices.tolist()
                rank = top.index(target) if target in top else None
                metrics[name].append((float(rank is not None), 0.0 if rank is None else 1 / np.log2(rank + 2)))
    return {f"{name}_recall_at_10": float(np.mean([x[0] for x in rows])) for name, rows in metrics.items()} | {f"{name}_ndcg_at_10": float(np.mean([x[1] for x in rows])) for name, rows in metrics.items()}
