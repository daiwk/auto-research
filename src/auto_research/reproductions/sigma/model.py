from __future__ import annotations

import random
import time
from dataclasses import dataclass

import numpy as np

from ..llm_lora import device_for, inject_lora, require_llm_backend
from .data import SigmaData, SigmaExample


@dataclass
class Grounder:
    lm: object
    tokenizer: object
    projection: object
    device: object


def train_grounder(data: SigmaData, model_name: str, steps: int, seed: int):
    torch, nn, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    lm = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
    trainable = inject_lora(lm, rank=4, alpha=8.0)
    device = device_for(torch)
    lm.to(device)
    hidden = lm.get_input_embeddings().weight.shape[1]
    projection = nn.Linear(hidden, 64).to(device)
    optimizer = torch.optim.AdamW(
        [p for p in lm.parameters() if p.requires_grad] + list(projection.parameters()),
        lr=1e-4,
    )
    collaborative = torch.tensor(data.collaborative_vectors, device=device)
    rng = random.Random(seed)
    losses, cl_losses, kd_losses = [], [], []
    started = time.perf_counter()
    lm.train()
    for _ in range(steps):
        selected = [data.grounding_pairs[rng.randrange(len(data.grounding_pairs))] for _ in range(8)]
        left = [row[1] for row in selected]
        right = [row[2] for row in selected]
        semantic = encode_items(
            Grounder(lm, tokenizer, projection, device), data.titles,
            left + right, torch, inference=False,
        )
        semantic = torch.nn.functional.normalize(semantic, dim=-1)
        similarity = semantic @ semantic.T / 0.05
        similarity.fill_diagonal_(-1e4)
        targets = torch.cat((torch.arange(8, 16), torch.arange(0, 8))).to(device)
        cl_loss = torch.nn.functional.cross_entropy(similarity, targets)
        teacher = torch.cat((collaborative[left], collaborative[right]), 0)
        teacher_similarity = teacher @ teacher.T / 0.05
        teacher_similarity.fill_diagonal_(-1e4)
        kd_loss = torch.nn.functional.kl_div(
            torch.log_softmax(similarity, -1),
            torch.softmax(teacher_similarity, -1),
            reduction="batchmean",
        )
        loss = cl_loss + kd_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [p for group in optimizer.param_groups for p in group["params"]], 1.0
        )
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        cl_losses.append(float(cl_loss.detach().cpu()))
        kd_losses.append(float(kd_loss.detach().cpu()))
    window = min(5, len(losses))
    return Grounder(lm, tokenizer, projection, device), {
        "steps": steps,
        "trainable_lora_parameters": trainable,
        "initial_loss": float(np.mean(losses[:window])),
        "final_loss": float(np.mean(losses[-window:])),
        "mean_contrastive_loss": float(np.mean(cl_losses)),
        "mean_kd_loss": float(np.mean(kd_losses)),
        "seconds": time.perf_counter() - started,
    }


def materialize_semantics(grounder, data, batch_size=32):
    torch, _, _, _ = require_llm_backend()
    output = []
    grounder.lm.eval()
    with torch.inference_mode():
        for start in range(0, len(data.titles), batch_size):
            items = list(range(start, min(start + batch_size, len(data.titles))))
            output.append(encode_items(grounder, data.titles, items, torch, True).cpu())
    return torch.cat(output).to(grounder.device)


def build_sigma(grounder, data: SigmaData, semantic_vectors):
    torch, nn, _, _ = require_llm_backend()
    hidden = grounder.lm.get_input_embeddings().weight.shape[1]
    prefix_count = int(data.codes[:, 0].max()) + 1

    class SIGMA(nn.Module):
        def __init__(self):
            super().__init__()
            self.lm = grounder.lm
            self.tokenizer = grounder.tokenizer
            self.device_value = grounder.device
            self.item_id = nn.Embedding(len(data.codes), 32)
            self.visual_projection = nn.Linear(data.visual_vectors.shape[1], 32)
            self.fusion = nn.Sequential(
                nn.Linear(32 + 64 + 32, 96), nn.SiLU(), nn.Linear(96, 64)
            )
            self.prefix_head = nn.Linear(hidden, prefix_count)
            self.prefix_embedding = nn.Embedding(prefix_count, 32)
            self.query = nn.Sequential(
                nn.Linear(hidden + 32, 96), nn.SiLU(), nn.Linear(96, 64)
            )
            self.id_query = nn.Sequential(
                nn.Linear(hidden, 96), nn.SiLU(), nn.Linear(96, 64)
            )
            self.register_buffer("semantic_vectors", semantic_vectors)
            self.register_buffer(
                "visual_vectors", torch.tensor(data.visual_vectors, device=grounder.device)
            )

        def item_vectors(self, items=None):
            if items is None:
                items = torch.arange(len(data.codes), device=self.device_value)
            values = torch.cat(
                (
                    self.item_id(items),
                    self.semantic_vectors[items],
                    self.visual_projection(self.visual_vectors[items]),
                ),
                -1,
            )
            return torch.nn.functional.normalize(self.fusion(values), dim=-1)

        def encode_prompts(self, examples):
            prompts = [prompt_text(example, data) for example in examples]
            encoded = self.tokenizer(
                prompts, padding=True, truncation=True, max_length=128, return_tensors="pt"
            ).to(self.device_value)
            output = self.lm(
                **encoded, output_hidden_states=True, use_cache=False, return_dict=True
            )
            weights = encoded["attention_mask"].unsqueeze(-1)
            return (output.hidden_states[-1] * weights).sum(1) / weights.sum(1).clamp_min(1)

        def query_vector(self, hidden_state, prefixes):
            return torch.nn.functional.normalize(
                self.query(torch.cat((hidden_state, self.prefix_embedding(prefixes)), -1)),
                dim=-1,
            )

    return SIGMA().to(grounder.device)


def train_sigma(model, data: SigmaData, steps: int, seed: int):
    torch, _, _, _ = require_llm_backend()
    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad], lr=2e-4
    )
    codes = torch.tensor(data.codes, dtype=torch.long, device=model.device_value)
    rng = random.Random(seed)
    losses, prefix_losses, item_losses = [], [], []
    started = time.perf_counter()
    model.train()
    for _ in range(steps):
        rows = [data.train[rng.randrange(len(data.train))] for _ in range(8)]
        hidden = model.encode_prompts(rows)
        targets = torch.tensor([row.target for row in rows], device=model.device_value)
        prefixes = codes[targets, 0]
        prefix_loss = torch.nn.functional.cross_entropy(model.prefix_head(hidden), prefixes)
        candidate_rows = []
        for target, prefix in zip(targets.tolist(), prefixes.tolist()):
            same = np.flatnonzero(data.codes[:, 0] == prefix).tolist()
            if target in same:
                same.remove(target)
            negatives = rng.sample(same, min(31, len(same)))
            while len(negatives) < 31:
                negatives.append(rng.randrange(len(data.codes)))
            candidate_rows.append([target, *negatives])
        candidates = torch.tensor(candidate_rows, device=model.device_value)
        query = model.query_vector(hidden, prefixes)
        item_vectors = model.item_vectors(candidates)
        logits = torch.einsum("bd,bnd->bn", query, item_vectors) / 0.05
        prefix_item_loss = torch.nn.functional.cross_entropy(
            logits, torch.zeros(len(rows), dtype=torch.long, device=model.device_value)
        )
        id_query = torch.nn.functional.normalize(model.id_query(hidden), dim=-1)
        id_logits = torch.einsum("bd,bnd->bn", id_query, item_vectors) / 0.05
        id_item_loss = torch.nn.functional.cross_entropy(
            id_logits, torch.zeros(len(rows), dtype=torch.long, device=model.device_value)
        )
        item_loss = 0.5 * (prefix_item_loss + id_item_loss)
        loss = prefix_loss + item_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [p for p in model.parameters() if p.requires_grad], 1.0
        )
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        prefix_losses.append(float(prefix_loss.detach().cpu()))
        item_losses.append(float(item_loss.detach().cpu()))
    window = min(5, len(losses))
    return {
        "steps": steps,
        "initial_loss": float(np.mean(losses[:window])),
        "final_loss": float(np.mean(losses[-window:])),
        "mean_prefix_ntp_loss": float(np.mean(prefix_losses)),
        "mean_prefix_hard_negative_infonce": float(np.mean(item_losses)),
        "seconds": time.perf_counter() - started,
        "tasks": list(sorted(set(row.task for row in data.train))),
    }


def score_catalog(model, data, row: SigmaExample, mode: str, top_prefixes=5):
    torch, _, _, _ = require_llm_backend()
    model.eval()
    with torch.inference_mode():
        hidden = model.encode_prompts([row])
        item_vectors = model.item_vectors()
        if mode == "id_only":
            query = torch.nn.functional.normalize(model.id_query(hidden), dim=-1)
            return (query @ item_vectors.T).squeeze(0).cpu().numpy()
        prefix_logp = torch.log_softmax(model.prefix_head(hidden), -1).squeeze(0)
        selected = torch.topk(prefix_logp, min(top_prefixes, len(prefix_logp))).indices
        if mode == "top1_prefix":
            selected = selected[:1]
        sigma = prefix_logp[selected].std(unbiased=False).clamp_min(0.05)
        scores = torch.full((len(data.codes),), -torch.inf, device=model.device_value)
        for prefix in selected:
            items = torch.tensor(
                np.flatnonzero(data.codes[:, 0] == int(prefix)).tolist(),
                device=model.device_value,
            )
            if not len(items):
                continue
            query = model.query_vector(hidden, prefix.view(1))
            similarity = (query @ item_vectors[items].T).squeeze(0)
            scale = sigma if mode == "apf" else torch.tensor(1.0, device=model.device_value)
            conditional = torch.log_softmax(similarity * scale / 0.05, -1)
            scores[items] = prefix_logp[prefix] + conditional
        return scores.cpu().numpy()


def encode_items(grounder, titles, items, torch, inference):
    encoded = grounder.tokenizer(
        [titles[item] for item in items],
        padding=True,
        truncation=True,
        max_length=32,
        return_tensors="pt",
    ).to(grounder.device)
    output = grounder.lm(
        **encoded, output_hidden_states=True, use_cache=False, return_dict=True
    )
    weights = encoded["attention_mask"].unsqueeze(-1)
    pooled = (output.hidden_states[-1] * weights).sum(1) / weights.sum(1).clamp_min(1)
    return grounder.projection(pooled)


def prompt_text(example: SigmaExample, data: SigmaData) -> str:
    history = " | ".join(data.titles[item][:48] for item in example.history[-5:])
    return (
        "You are a multi-task product recommender.\n"
        f"Task: {example.task}. Instruction: {example.instruction}\n"
        f"User history: {history}\nGenerate the hybrid semantic-prefix and item recommendation:"
    )
