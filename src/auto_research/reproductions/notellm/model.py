from __future__ import annotations

from auto_research.runtime import device_for

import random
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class NoteLLMConfig:
    model_name: str = "google-t5/t5-small"
    batch_size: int = 8
    steps: int = 40
    learning_rate: float = 1e-4
    temperature: float = 0.07


def require_backend():
    try:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("NoteLLM requires `pip install -e '.[plum]'`.") from exc
    return torch, AutoModelForSeq2SeqLM, AutoTokenizer


def build_model(config):
    _, AutoModelForSeq2SeqLM, AutoTokenizer = require_backend()
    return AutoModelForSeq2SeqLM.from_pretrained(config.model_name), AutoTokenizer.from_pretrained(config.model_name)


def prompts(titles, genres):
    return tuple(
        f"compress this note: {title}; categories: {', '.join(kind)} <extra_id_0>"
        for title, kind in zip(titles, genres)
    )


def embed_all(model, tokenizer, texts, batch_size=64):
    torch, _, _ = require_backend(); device = next(model.parameters()).device
    rows = []; model.eval()
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            encoded = tokenizer(list(texts[start:start + batch_size]), padding=True, truncation=True, max_length=48, return_tensors="pt").to(device)
            hidden = model.encoder(input_ids=encoded["input_ids"], attention_mask=encoded["attention_mask"], return_dict=True).last_hidden_state
            index = encoded["attention_mask"].sum(1) - 1
            compressed = hidden[torch.arange(len(index), device=device), index]
            rows.append(torch.nn.functional.normalize(compressed, dim=-1).cpu().numpy())
    return np.concatenate(rows)


def train(model, tokenizer, texts, genres, pairs, config, seed):
    torch, _, _ = require_backend(); device = device_for(torch)
    model.to(device).train(); torch.manual_seed(seed); rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate); losses=[]
    for _ in range(config.steps):
        batch = [pairs[rng.randrange(len(pairs))] for _ in range(config.batch_size)]
        left = _encode(model, tokenizer, [texts[a] for a, _ in batch], device, torch)
        right = _encode(model, tokenizer, [texts[b] for _, b in batch], device, torch)
        labels = torch.arange(len(batch), device=device)
        logits = left @ right.T / config.temperature
        gcl = (torch.nn.functional.cross_entropy(logits, labels) + torch.nn.functional.cross_entropy(logits.T, labels)) / 2
        source_ids = [a for a, _ in batch]
        encoded = tokenizer(
            [texts[a] for a in source_ids], text_target=["categories: " + ", ".join(genres[a]) for a in source_ids],
            padding=True, truncation=True, max_length=48, return_tensors="pt",
        ).to(device)
        csft = model(**encoded).loss
        loss = gcl + 0.2 * csft
        optimizer.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); losses.append(float(loss.detach().cpu()))
    return {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])), "parameters": sum(p.numel() for p in model.parameters()), "device": device.type}


def _encode(model, tokenizer, texts, device, torch):
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=48, return_tensors="pt").to(device)
    hidden = model.encoder(input_ids=encoded["input_ids"], attention_mask=encoded["attention_mask"], return_dict=True).last_hidden_state
    index = encoded["attention_mask"].sum(1) - 1
    return torch.nn.functional.normalize(hidden[torch.arange(len(index), device=device), index], dim=-1)


def i2i_metrics(vectors, data):
    hits = ndcg = 0.0
    for query, target in zip(data.validation, data.test):
        scores = vectors @ vectors[query]; scores[query] = -np.inf
        top = np.argpartition(scores, -10)[-10:]; top = top[np.argsort(scores[top])[::-1]]
        positions = np.flatnonzero(top == target)
        if positions.size: hits += 1; ndcg += 1 / np.log2(int(positions[0]) + 2)
    count = len(data.test)
    return {"hit_at_10": hits / count, "ndcg_at_10": ndcg / count, "queries": count}
