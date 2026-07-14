from __future__ import annotations

import random
import time
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..llm_lora import device_for, inject_lora, require_llm_backend
from ..llm_rec_data import TextCTRData, binary_auc


@dataclass(frozen=True)
class MSDConfig:
    teacher_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct"
    student_name: str = "google-t5/t5-small"
    maximum_users: int = 30
    teacher_items: int = 160
    distill_steps: int = 32
    ranker_steps: int = 100
    batch_size: int = 16
    dimensions: int = 40
    learning_rate: float = 7e-4
    maximum_train: int = 5000
    maximum_test: int = 1000
    relevant_items: int = 3


def user_prompt(data: TextCTRData, user: int, histories: dict[int, tuple[int, ...]]):
    history = "; ".join(data.titles[item] for item in histories.get(user, ())[-8:])
    return f"Summarize durable user preference as key phrases and a rationale. History: {history}"


def item_prompt(data: TextCTRData, item: int):
    return f"Summarize this item as recommendation key phrases and a rationale. Item: {data.titles[item]}. Genres: {', '.join(data.genres[item])}"


def build_prompts(data: TextCTRData):
    histories = {}
    for row in data.train:
        histories[row.user] = row.history
    users = [user_prompt(data, user, histories) for user in range(data.users)]
    items = [item_prompt(data, item) for item in range(len(data.titles))]
    return users, items


def _teacher_generate(prompts, config: MSDConfig):
    torch, _, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    tokenizer = AutoTokenizer.from_pretrained(config.teacher_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(config.teacher_name).to(device_for(torch)).eval()
    texts = []
    with torch.inference_mode():
        for start in range(0, len(prompts), 8):
            batch = prompts[start : start + 8]
            encoded = tokenizer(batch, padding=True, truncation=True, max_length=96, return_tensors="pt").to(next(model.parameters()).device)
            output = model.generate(**encoded, max_new_tokens=24, do_sample=False, pad_token_id=tokenizer.pad_token_id)
            generated = output[:, encoded["input_ids"].shape[1] :]
            texts.extend(tokenizer.batch_decode(generated, skip_special_tokens=True))
    return [text.strip() or prompt for text, prompt in zip(texts, prompts)]


def distill_student(data: TextCTRData, root: Path, config: MSDConfig, seed: int):
    torch, _, _, _ = require_llm_backend()
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    output_dir = root / "msd" / f"t5-small-u{config.maximum_users}-s{seed}"
    metrics_path = output_dir / "distillation-metrics.json"
    torch.manual_seed(seed)
    users, items = build_prompts(data)
    frequency = np.bincount([row.candidate for row in data.train], minlength=len(data.titles))
    selected_items = np.argsort(-frequency)[: config.teacher_items].tolist()
    prompts = users + [items[index] for index in selected_items]
    if (output_dir / "config.json").exists():
        tokenizer = AutoTokenizer.from_pretrained(output_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(output_dir)
        metrics = {"cache_hit": True, "teacher_examples": len(prompts)}
        if metrics_path.exists():
            metrics.update(json.loads(metrics_path.read_text()))
    else:
        targets = _teacher_generate(prompts, config)
        tokenizer = AutoTokenizer.from_pretrained(config.student_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(config.student_name).to(device_for(torch))
        optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
        rng = random.Random(seed)
        losses = []
        model.train()
        for _ in range(config.distill_steps):
            indices = [rng.randrange(len(prompts)) for _ in range(4)]
            source = tokenizer([prompts[i] for i in indices], padding=True, truncation=True, max_length=96, return_tensors="pt").to(next(model.parameters()).device)
            labels = tokenizer(text_target=[targets[i] for i in indices], padding=True, truncation=True, max_length=48, return_tensors="pt")["input_ids"].to(next(model.parameters()).device)
            labels[labels == tokenizer.pad_token_id] = -100
            loss = model(**source, labels=labels).loss
            optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
            losses.append(float(loss.detach().cpu()))
        output_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(output_dir, safe_serialization=True)
        tokenizer.save_pretrained(output_dir)
        metrics = {"cache_hit": False, "teacher_examples": len(prompts), "distill_loss_initial": float(np.mean(losses[:8])), "distill_loss_final": float(np.mean(losses[-8:]))}
        metrics_path.write_text(json.dumps({"distill_loss_initial": metrics["distill_loss_initial"], "distill_loss_final": metrics["distill_loss_final"]}))
    model.to(device_for(torch))
    for parameter in model.parameters():
        parameter.requires_grad = False
    trainable = inject_lora(model, rank=4, alpha=8.0)
    metrics["lora_trainable"] = trainable
    return model, tokenizer, users, items, frequency, metrics


def _encode(model, tokenizer, texts, gradients: bool):
    torch, _, _, _ = require_llm_backend()
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=96, return_tensors="pt").to(next(model.parameters()).device)
    context = torch.enable_grad() if gradients else torch.inference_mode()
    with context:
        hidden = model.encoder(**encoded).last_hidden_state
        weights = encoded["attention_mask"].unsqueeze(-1)
        return (hidden * weights).sum(1) / weights.sum(1).clamp_min(1)


def build_rankers(data, student, tokenizer, user_prompts, item_prompts, frequency, config: MSDConfig, seed: int):
    torch, nn, _, _ = require_llm_backend()
    torch.manual_seed(seed)
    device = next(student.parameters()).device
    with torch.inference_mode():
        cached_items = []
        for start in range(0, len(item_prompts), 32):
            cached_items.append(_encode(student, tokenizer, item_prompts[start : start + 32], False).cpu())
        cached_items = torch.cat(cached_items)

    class IDRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.user = nn.Embedding(data.users, config.dimensions)
            self.item = nn.Embedding(len(data.titles), config.dimensions)
            self.head = nn.Sequential(nn.Linear(3 * config.dimensions, 2 * config.dimensions), nn.GELU(), nn.Linear(2 * config.dimensions, 1))

        def forward(self, users, items, histories=None):
            u, i = self.user(users), self.item(items)
            return self.head(torch.cat((u, i, u * i), -1)).squeeze(-1)

    class MSDRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.student = student
            self.tokenizer = tokenizer
            self.user_id = nn.Embedding(data.users, config.dimensions)
            self.item_id = nn.Embedding(len(data.titles), config.dimensions)
            hidden = student.config.d_model
            self.user_adapter = nn.Sequential(nn.Linear(hidden, 2 * config.dimensions), nn.GELU(), nn.Linear(2 * config.dimensions, config.dimensions))
            self.item_adapter = nn.Sequential(nn.Linear(hidden, 2 * config.dimensions), nn.GELU(), nn.Linear(2 * config.dimensions, config.dimensions))
            self.history_adapter = nn.Sequential(nn.Linear(hidden, config.dimensions), nn.GELU())
            self.register_buffer("cached_items", cached_items)
            self.register_buffer("frequency", torch.tensor(frequency, dtype=torch.float32))
            self.head = nn.Sequential(nn.Linear(4 * config.dimensions, 2 * config.dimensions), nn.GELU(), nn.Linear(2 * config.dimensions, 1))

        def forward(self, users, items, histories):
            user_indices = users.detach().cpu().tolist()
            item_indices = items.detach().cpu().tolist()
            user_knowledge = _encode(self.student, self.tokenizer, [user_prompts[x] for x in user_indices], self.training)
            online_item = _encode(self.student, self.tokenizer, [item_prompts[x] for x in item_indices], self.training)
            freq = self.frequency[items]
            cache_probability = freq / (freq + 5.0)
            if self.training:
                use_cache = torch.rand_like(cache_probability) < cache_probability
            else:
                use_cache = cache_probability >= 0.5
            item_knowledge = torch.where(use_cache.unsqueeze(-1), self.cached_items[items].detach(), online_item)
            candidate_cache = torch.nn.functional.normalize(self.cached_items[items], dim=-1)
            history_cache = self.cached_items[histories]
            similarities = (torch.nn.functional.normalize(history_cache, dim=-1) * candidate_cache.unsqueeze(1)).sum(-1)
            top = similarities.topk(min(config.relevant_items, histories.shape[1]), dim=1).indices
            relevant = history_cache.gather(1, top.unsqueeze(-1).expand(-1, -1, history_cache.shape[-1])).mean(1)
            u = self.user_id(users) + self.user_adapter(user_knowledge)
            i = self.item_id(items) + self.item_adapter(item_knowledge) + self.history_adapter(relevant)
            return self.head(torch.cat((u, i, u * i, (u - i).abs()), -1)).squeeze(-1)

    return IDRanker().to(device), MSDRanker().to(device)


def train_and_evaluate(model, train, test, config: MSDConfig, seed: int):
    torch, _, _, _ = require_llm_backend()
    rng = random.Random(seed)
    device = next(model.parameters()).device
    parameters = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=config.learning_rate)
    rows = train[: config.maximum_train]
    losses = []
    started = time.perf_counter()
    model.train()
    for _ in range(config.ranker_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        users = torch.tensor([row.user for row in batch], device=device)
        items = torch.tensor([row.candidate for row in batch], device=device)
        width = max(len(row.history[-8:]) for row in batch)
        histories = torch.tensor([((row.history[-8:][0],) * (width - len(row.history[-8:])) + row.history[-8:]) for row in batch], device=device)
        labels = torch.tensor([row.label for row in batch], dtype=torch.float32, device=device)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(model(users, items, histories), labels)
        optimizer.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(parameters, 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    labels, scores = [], []
    model.eval()
    with torch.inference_mode():
        for row in test[: config.maximum_test]:
            users = torch.tensor([row.user], device=device); items = torch.tensor([row.candidate], device=device); histories = torch.tensor([row.history[-8:]], device=device)
            scores.append(float(torch.sigmoid(model(users, items, histories)).cpu())); labels.append(row.label)
    return {"auc": binary_auc(labels, scores), "initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])), "seconds": time.perf_counter() - started, "trainable_parameters": sum(p.numel() for p in parameters)}
