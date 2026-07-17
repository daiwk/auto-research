from __future__ import annotations

from auto_research.runtime import device_for

import copy
import random
import re
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..llm_rec_data import load_text_ctr_data


@dataclass(frozen=True)
class RewriteExample:
    query: str
    target: str
    item: int


@dataclass(frozen=True)
class BEQUEData:
    train: tuple[RewriteExample, ...]
    test: tuple[RewriteExample, ...]
    catalog: tuple[str, ...]


@dataclass(frozen=True)
class BEQUEConfig:
    model_name: str = "google-t5/t5-small"
    batch_size: int = 8
    sft_steps: int = 60
    pro_steps: int = 20
    learning_rate: float = 3e-4
    maximum_train: int = 600
    maximum_test: int = 100
    beams: int = 4


def require_backend():
    try:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("BEQUE requires `pip install -e '.[plum]'`.") from exc
    return torch, AutoModelForSeq2SeqLM, AutoTokenizer


def build_rewrite_data(root: Path, seed: int = 17) -> BEQUEData:
    source = load_text_ctr_data(root)
    rows = []
    catalog = []
    for item, (title, genres) in enumerate(zip(source.titles, source.genres)):
        clean = re.sub(r"\([^)]*\)$", "", title).strip()
        words = re.findall(r"[a-z0-9]+", clean.lower())
        if not words:
            words = re.findall(r"[a-z0-9]+", " ".join(genres).lower()) or ["movie"]
        # A short, semantically incomplete e-commerce-like query; the rewrite
        # recovers full product/movie facets used by the retrieval simulator.
        query = " ".join(words[: min(2, len(words))])
        target = clean + " " + " ".join(genres)
        catalog.append(target)
        rows.append(RewriteExample(query, target, item))
    rng = random.Random(seed)
    rng.shuffle(rows)
    split = int(0.8 * len(rows))
    return BEQUEData(tuple(rows[:split]), tuple(rows[split:]), tuple(catalog))


def build_model(config: BEQUEConfig):
    _, AutoModelForSeq2SeqLM, AutoTokenizer = require_backend()
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(config.model_name)
    return model, tokenizer


def train_sft(model, tokenizer, rows, config: BEQUEConfig, seed: int):
    torch, _, _ = require_backend()
    device = device_for(torch)
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    started = time.perf_counter()
    for _ in range(config.sft_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        encoded = tokenizer(
            ["rewrite product query: " + row.query for row in batch],
            text_target=[row.target for row in batch], padding=True, truncation=True,
            max_length=48, return_tensors="pt",
        ).to(device)
        loss = model(**encoded).loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])),
        "seconds": time.perf_counter() - started, "device": device.type,
        "parameters": sum(value.numel() for value in model.parameters()),
    }


def sample_preference_lists(model, tokenizer, rows, data: BEQUEData, config: BEQUEConfig):
    torch, _, _ = require_backend()
    device = next(model.parameters()).device
    model.eval()
    lists = []
    subset = rows[: min(len(rows), 160)]
    with torch.inference_mode():
        for start in range(0, len(subset), config.batch_size):
            batch = subset[start:start + config.batch_size]
            encoded = tokenizer(
                ["rewrite product query: " + row.query for row in batch],
                padding=True, truncation=True, max_length=32, return_tensors="pt",
            ).to(device)
            generated = model.generate(
                **encoded, max_new_tokens=24, num_beams=config.beams,
                num_return_sequences=config.beams, early_stopping=True,
            )
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            for offset, row in enumerate(batch):
                candidates = list(dict.fromkeys(decoded[offset * config.beams:(offset + 1) * config.beams]))
                # PRO ranks only model/self-sampled outputs and label-free
                # fallbacks; injecting the supervised target would leak it.
                if row.query not in candidates:
                    candidates.append(row.query)
                fallback_index = 0
                while len(candidates) < config.beams:
                    fallback = f"{row.query} alternative {fallback_index}"
                    if fallback not in candidates:
                        candidates.append(fallback)
                    fallback_index += 1
                candidates.sort(key=lambda value: offline_feedback(row, value, data.catalog), reverse=True)
                lists.append((row.query, tuple(candidates[:config.beams])))
    return tuple(lists)


def train_pro(model, tokenizer, preference_lists, config: BEQUEConfig, seed: int):
    torch, _, _ = require_backend()
    device = next(model.parameters()).device
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate * 0.3)
    rng = random.Random(seed)
    losses = []
    for _ in range(config.pro_steps):
        batch = [preference_lists[rng.randrange(len(preference_lists))] for _ in range(config.batch_size)]
        candidates = [candidate for _, values in batch for candidate in values]
        queries = ["rewrite product query: " + query for query, values in batch for _ in values]
        log_probabilities = sequence_log_probabilities(model, tokenizer, queries, candidates, device, torch)
        width = len(batch[0][1])
        log_probabilities = log_probabilities.reshape(len(batch), width)
        # PRO: the offline-search partial order is converted to a rank-aware
        # listwise distribution; the best candidate also receives SFT weight.
        ranks = torch.arange(width, device=device, dtype=torch.float32)
        target = torch.softmax(-ranks / 0.5, dim=0)
        listwise = -(target * torch.log_softmax(log_probabilities, dim=1)).sum(1).mean()
        sft = -log_probabilities[:, 0].mean()
        loss = listwise + 0.2 * sft
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {"initial_loss": float(np.mean(losses[:5])), "final_loss": float(np.mean(losses[-5:])), "preference_lists": len(preference_lists)}


def sequence_log_probabilities(model, tokenizer, queries, targets, device, torch):
    encoded = tokenizer(
        queries, text_target=targets, padding=True, truncation=True,
        max_length=48, return_tensors="pt",
    ).to(device)
    labels = encoded.pop("labels")
    output = model(**encoded, labels=labels, return_dict=True)
    logits = output.logits
    token_log = torch.log_softmax(logits, dim=-1).gather(2, labels.clamp_min(0).unsqueeze(-1)).squeeze(-1)
    mask = labels != -100
    return (token_log * mask).sum(1) / mask.sum(1).clamp_min(1)


def evaluate(model, tokenizer, rows, data: BEQUEData, config: BEQUEConfig):
    torch, _, _ = require_backend()
    device = next(model.parameters()).device
    model.eval()
    metrics = []
    with torch.inference_mode():
        for start in range(0, len(rows), config.batch_size):
            batch = rows[start:start + config.batch_size]
            encoded = tokenizer(
                ["rewrite product query: " + row.query for row in batch],
                padding=True, truncation=True, max_length=32, return_tensors="pt",
            ).to(device)
            generated = model.generate(**encoded, max_new_tokens=24)
            rewrites = tokenizer.batch_decode(generated, skip_special_tokens=True)
            metrics.extend(offline_feedback(row, rewrite, data.catalog, detailed=True) for row, rewrite in zip(batch, rewrites))
    return {
        key: float(np.mean([value[key] for value in metrics]))
        for key in metrics[0]
    } | {"examples": len(rows)}


def offline_feedback(row: RewriteExample, rewrite: str, catalog, detailed: bool = False):
    query_tokens = set(re.findall(r"[a-z0-9]+", row.query.lower()))
    rewrite_tokens = set(re.findall(r"[a-z0-9]+", rewrite.lower()))
    target_tokens = set(re.findall(r"[a-z0-9]+", row.target.lower()))
    relevance = len(rewrite_tokens & target_tokens) / max(len(rewrite_tokens | target_tokens), 1)
    increment = len(rewrite_tokens - query_tokens) / max(len(target_tokens), 1)
    scores = []
    for item, text in enumerate(catalog):
        tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
        scores.append(len(rewrite_tokens & tokens) / max(len(rewrite_tokens | tokens), 1))
    hit = float(int(np.argmax(scores)) == row.item)
    score = relevance + 0.2 * increment + hit
    return {"relevance": relevance, "increment": increment, "hit_at_1": hit, "feedback": score} if detailed else score
