from __future__ import annotations

from auto_research.runtime import device_for

import hashlib
import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..industrial_ranking import require_backend
from .data import PreciseData


@dataclass(frozen=True)
class PreciseConfig:
    model_name: str = "HuggingFaceTB/SmolLM2-135M"
    dimensions: int = 32
    experts: int = 4
    active_experts: int = 2
    heads: int = 4
    layers: int = 2
    history_length: int = 12
    text_tokens: int = 8
    maximum_users: int = 300
    universal_steps: int = 120
    targeted_steps: int = 80
    batch_size: int = 48
    learning_rate: float = 6e-4


def initialize_llm_tokens(data: PreciseData, root: Path, config: PreciseConfig) -> tuple[np.ndarray, np.ndarray, dict]:
    """Cache contextual token states; the recommendation model then trains these states."""
    digest = hashlib.sha1("\n".join(data.item_texts).encode()).hexdigest()[:12]
    cache = root / "precise" / f"smollm2-tokens-{digest}-t{config.text_tokens}.npz"
    if cache.exists():
        payload = np.load(cache)
        return payload["tokens"], payload["mask"], {"cache": "hit", "path": str(cache)}
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("PRECISE needs `pip install -e '.[plum]'` for LLM token initialization.") from exc
    cache.parent.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(config.model_name)
    device = device_for(torch)
    model.to(device).eval()
    vectors, masks = [], []
    started = time.perf_counter()
    with torch.inference_mode():
        for start in range(0, len(data.item_texts), 32):
            encoded = tokenizer(
                data.item_texts[start:start + 32], padding="max_length", truncation=True,
                max_length=config.text_tokens, return_tensors="pt",
            ).to(device)
            output = model(**encoded, output_hidden_states=True, return_dict=True)
            vectors.append(output.hidden_states[-1].cpu().float().numpy())
            masks.append(encoded["attention_mask"].cpu().numpy().astype(np.bool_))
    tokens, mask = np.concatenate(vectors).astype(np.float16), np.concatenate(masks)
    np.savez_compressed(cache, tokens=tokens, mask=mask)
    return tokens, mask, {"cache": "miss", "path": str(cache), "seconds": time.perf_counter() - started}


def build_precise(item_count: int, initial_tokens: np.ndarray, token_mask: np.ndarray, config: PreciseConfig, fusion: str = "moe"):
    torch, nn = require_backend()

    class EmbeddingFusion(nn.Module):
        def __init__(self):
            super().__init__()
            token_dim = initial_tokens.shape[-1]
            self.id_embedding = nn.Embedding(item_count, config.dimensions)
            self.token_embedding = nn.Parameter(torch.tensor(initial_tokens, dtype=torch.float32))
            self.register_buffer("token_mask", torch.tensor(token_mask, dtype=torch.bool))
            self.project = nn.Linear(token_dim, config.dimensions)
            self.expert_queries = nn.Parameter(torch.randn(config.experts, config.dimensions) * 0.02)
            self.gate = nn.Linear(config.dimensions, config.experts)

        def forward(self, items):
            ids = self.id_embedding(items)
            tokens = self.project(self.token_embedding[items])
            mask = self.token_mask[items]
            if fusion == "id":
                semantic = torch.zeros_like(ids)
            elif fusion == "pool":
                semantic = (tokens * mask.unsqueeze(-1)).sum(-2) / mask.sum(-1, keepdim=True).clamp_min(1)
            else:
                attention = torch.einsum("...td,kd->...kt", tokens, self.expert_queries) / np.sqrt(config.dimensions)
                attention = attention.masked_fill(~mask.unsqueeze(-2), -1e4).softmax(-1)
                expert_values = torch.einsum("...kt,...td->...kd", attention, tokens)
                pooled = (tokens * mask.unsqueeze(-1)).sum(-2) / mask.sum(-1, keepdim=True).clamp_min(1)
                gate_logits = self.gate(pooled)
                top_values, top_indices = gate_logits.topk(config.active_experts, dim=-1)
                weights = top_values.softmax(-1)
                chosen = expert_values.gather(-2, top_indices.unsqueeze(-1).expand(*top_indices.shape, config.dimensions))
                semantic = (chosen * weights.unsqueeze(-1)).sum(-2)
            return torch.cat((ids, semantic), dim=-1)

    class PRECISE(nn.Module):
        def __init__(self):
            super().__init__()
            self.fusion = EmbeddingFusion()
            width = 2 * config.dimensions
            self.position = nn.Embedding(config.history_length, width)
            layer = nn.TransformerEncoderLayer(width, config.heads, 4 * width, dropout=0.0, batch_first=True, norm_first=True)
            self.transformer = nn.TransformerEncoder(layer, config.layers)
            self.user_mlp = nn.Sequential(nn.Linear(config.history_length * width, 2 * width), nn.GELU(), nn.Linear(2 * width, width))

        def encode(self, items, padding, targeted: bool):
            values = self.fusion(items) + self.position(torch.arange(items.shape[1], device=items.device))
            causal = None
            if not targeted:
                causal = torch.triu(torch.ones(items.shape[1], items.shape[1], dtype=torch.bool, device=items.device), diagonal=1)
            hidden = self.transformer(values, mask=causal, src_key_padding_mask=padding)
            if targeted:
                return self.user_mlp(hidden.masked_fill(padding.unsqueeze(-1), 0).flatten(1))
            return hidden

    return PRECISE()


def _batch_sequences(sequences, config, rng, device, torch, include_target: bool):
    width = config.history_length + int(include_target)
    items = torch.zeros((config.batch_size, width), dtype=torch.long, device=device)
    padding = torch.ones((config.batch_size, width), dtype=torch.bool, device=device)
    for row in range(config.batch_size):
        sequence = sequences[rng.randrange(len(sequences))]
        end = rng.randrange(3, len(sequence) + 1)
        values = sequence[max(0, end - width):end]
        items[row, -len(values):] = torch.tensor(values, device=device)
        padding[row, -len(values):] = False
    return items, padding


def universal_train(model, sequences, config: PreciseConfig, seed: int):
    torch, _ = require_backend()
    rng = random.Random(seed); torch.manual_seed(seed)
    device = device_for(torch)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []; frozen_steps = config.universal_steps // 2
    for step in range(config.universal_steps):
        model.fusion.token_embedding.requires_grad_(step >= frozen_steps)
        items, padding = _batch_sequences(sequences, config, rng, device, torch, True)
        hidden = model.encode(items[:, :-1], padding[:, :-1], targeted=False)
        valid = ~padding[:, 1:]
        queries = hidden[valid]
        targets = items[:, 1:][valid]
        # In-batch negatives must be item classes, not occurrences. Without
        # deduplication repeated positives become contradictory CE columns.
        unique_targets, class_indices = torch.unique(targets, sorted=True, return_inverse=True)
        candidates = model.fusion(unique_targets)
        logits = queries @ candidates.T / np.sqrt(2 * config.dimensions)
        loss = torch.nn.functional.cross_entropy(logits, class_indices)
        optimizer.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])), "token_frozen_steps": frozen_steps}


def targeted_train(model, sequences, config: PreciseConfig, seed: int):
    torch, _ = require_backend()
    rng = random.Random(seed + 991); torch.manual_seed(seed + 991)
    device = next(model.parameters()).device
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    model.fusion.token_embedding.requires_grad_(True)
    for _ in range(config.targeted_steps):
        items, padding = _batch_sequences(sequences, config, rng, device, torch, True)
        users = model.encode(items[:, :-1], padding[:, :-1], targeted=True)
        targets = model.fusion(items[:, -1])
        positive = (users * targets).sum(-1)
        negative = (users.roll(1, 0) * targets).sum(-1)
        loss = -torch.nn.functional.logsigmoid(positive - negative).mean()
        optimizer.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:]))}


def evaluate(model, data: PreciseData, config: PreciseConfig):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    all_items = model.fusion(torch.arange(len(data.item_texts), device=device))
    order = np.argsort(np.asarray(data.train_frequency))
    cold = set(order[: max(1, int(0.8 * len(order)))].tolist())
    recalls = []; ndcgs = []; cold_recalls = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(data.targeted), config.batch_size):
            sequences = data.targeted[start:start + config.batch_size]
            targets = data.test_targets[start:start + config.batch_size]
            items = torch.zeros((len(sequences), config.history_length), dtype=torch.long, device=device)
            padding = torch.ones_like(items, dtype=torch.bool)
            for row, sequence in enumerate(sequences):
                values = sequence[-config.history_length:]
                items[row, -len(values):] = torch.tensor(values, device=device)
                padding[row, -len(values):] = False
            users = model.encode(items, padding, targeted=True)
            ranked = (users @ all_items.T).topk(10, dim=-1).indices.cpu().tolist()
            for target, values in zip(targets, ranked):
                if target in values:
                    rank = values.index(target)
                    recalls.append(1.0); ndcgs.append(1.0 / np.log2(rank + 2))
                else:
                    recalls.append(0.0); ndcgs.append(0.0)
                if target in cold:
                    cold_recalls.append(float(target in values))
    return {"recall_at_10": float(np.mean(recalls)), "ndcg_at_10": float(np.mean(ndcgs)), "cold_recall_at_10": float(np.mean(cold_recalls)) if cold_recalls else 0.0, "test_users": len(recalls), "cold_test_users": len(cold_recalls)}
