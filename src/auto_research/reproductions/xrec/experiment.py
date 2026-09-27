"""Public MovieLens evaluation for the X-Rec core algorithm.

No TikTok data, production embeddings or online experiment is available here.
All item representation learning and model selection use training/validation
only; the held-out test target is read once after training.
"""

from __future__ import annotations

import random
import time
from pathlib import Path

import numpy as np
import torch
from torch import Tensor, nn
from torch.nn import functional as F

from ..rec_utils import batched_ranking_metrics, load_movielens_1m_sequences
from .model import XRec, sphere_normalize


def learn_item_vectors(train: tuple[tuple[int, ...], ...], item_count: int, *, seed: int, dim: int = 32, steps: int = 160) -> Tensor:
    """Full-catalog contrastive next-item representation training."""
    torch.manual_seed(seed)
    pairs = torch.tensor([(a, b) for seq in train for a, b in zip(seq, seq[1:])], dtype=torch.long)
    if len(pairs) < 2:
        raise ValueError("at least two training transitions are required")
    embeddings = nn.Embedding(item_count, dim)
    optimizer = torch.optim.AdamW(embeddings.parameters(), lr=0.003)
    sampler = torch.Generator().manual_seed(seed + 11)
    for _ in range(steps):
        batch = pairs[torch.randint(len(pairs), (128,), generator=sampler)]
        vectors = sphere_normalize(embeddings.weight)
        logits = sphere_normalize(embeddings(batch[:, 0])) @ vectors.T * 12
        loss = F.cross_entropy(logits, batch[:, 1])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return sphere_normalize(embeddings.weight.detach())


def cluster_anchors(vectors: Tensor, count: int, *, seed: int, iterations: int = 12) -> Tensor:
    """Spherical k-means on train-only item representations."""
    if count > len(vectors):
        raise ValueError("more anchors than items")
    generator = torch.Generator().manual_seed(seed)
    centers = vectors[torch.randperm(len(vectors), generator=generator)[:count]].clone()
    for _ in range(iterations):
        labels = (vectors @ centers.T).argmax(dim=-1)
        updated = torch.zeros_like(centers).index_add_(0, labels, vectors)
        sizes = torch.bincount(labels, minlength=count)
        centers = sphere_normalize(torch.where(sizes[:, None] > 0, updated, centers))
    return (vectors @ centers.T).argmax(dim=-1)


def training_examples(train: tuple[tuple[int, ...], ...], *, max_history: int, last_only: bool = False) -> tuple[tuple[tuple[int, ...], int], ...]:
    examples = []
    for sequence in train:
        ends = (len(sequence) - 1,) if last_only else range(1, len(sequence))
        for end in ends:
            examples.append((sequence[max(0, end - max_history):end], sequence[end]))
    if not examples:
        raise ValueError("no sequence training examples")
    return tuple(examples)


def batch_examples(examples: tuple[tuple[tuple[int, ...], int], ...], indices: Tensor) -> tuple[Tensor, Tensor, Tensor]:
    selected = [examples[int(index)] for index in indices]
    length = max(len(history) for history, _ in selected)
    histories = torch.zeros(len(selected), length, dtype=torch.long)
    valid = torch.zeros(len(selected), length, dtype=torch.bool)
    for row, (history, _) in enumerate(selected):
        histories[row, :len(history)] = torch.tensor(history)
        valid[row, :len(history)] = True
    return histories, valid, torch.tensor([target for _, target in selected], dtype=torch.long)


class U2IBaseline(nn.Module):
    """Same item table and history transformer, deterministic one-vector retrieval."""

    def __init__(self, vectors: Tensor, width: int, max_history: int) -> None:
        super().__init__()
        self.register_buffer("items", vectors)
        self.item_project = nn.Linear(vectors.shape[1], width)
        self.position = nn.Embedding(max_history, width)
        self.encoder = nn.ModuleList([
            nn.TransformerEncoderLayer(width, 4, 4 * width, dropout=0.0, batch_first=True, norm_first=True)
            for _ in range(2)
        ])
        self.output = nn.Linear(width, vectors.shape[1])

    def forward(self, history: Tensor, valid: Tensor) -> Tensor:
        length = history.shape[1]
        tokens = self.item_project(self.items[history]) + self.position(torch.arange(length))[None]
        causal = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
        hidden = tokens
        for layer in self.encoder:
            hidden = layer(hidden, src_mask=causal, src_key_padding_mask=~valid)
        summary = hidden[torch.arange(len(history)), valid.long().sum(dim=1) - 1]
        return sphere_normalize(self.output(summary))


def _fit(model: nn.Module, examples: tuple[tuple[tuple[int, ...], int], ...], *, seed: int, steps: int, anchors: Tensor | None = None) -> dict[str, float]:
    model.train()
    sampler = torch.Generator().manual_seed(seed + 23)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    last = {}
    for _ in range(steps):
        ids = torch.randint(len(examples), (64,), generator=sampler)
        history, valid, target = batch_examples(examples, ids)
        if isinstance(model, XRec):
            assert anchors is not None
            loss, components = model.loss(history, valid, target, anchors[target])
            last = {name: float(value) for name, value in components.items()}
        elif hasattr(model, "codes"):
            loss = model.loss(history, valid, target)
            last = {"sid_ar_ce": float(loss.detach())}
        else:
            logits = model(history, valid) @ model.items.T * 12
            loss = F.cross_entropy(logits, target)
            last = {"retrieval_ce": float(loss.detach())}
        optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 2.0)
        optimizer.step()
    model.eval()
    return last


def _recall_20x1(data, generate, *, target: str, batch_size: int = 16) -> float:
    """Paper-like K triggers, one exact nearest item each, union after seen filtering."""
    targets = data.validation if target == "validation" else data.test
    hits = 0
    for start in range(0, len(data.train), batch_size):
        contexts = [
            history + ((data.validation[index],) if target == "test" else ())
            for index, history in enumerate(data.train[start : start + batch_size], start)
        ]
        triggers, vectors = generate(contexts)
        retrieved = (triggers @ vectors.T).argmax(dim=-1).cpu().numpy()
        for row, context in enumerate(contexts):
            candidate_set = set(int(item) for item in retrieved[row]) - set(context)
            hits += int(targets[start + row] in candidate_set)
    return hits / len(targets)


@torch.no_grad()
def _generation_qps(generate, batch_size: int, *, warmup: int = 2, repeats: int = 5) -> float:
    """Generation only; excludes history packing, ANN and training."""
    for _ in range(warmup):
        generate()
    times = []
    for _ in range(repeats):
        started = time.perf_counter()
        generate()
        times.append(time.perf_counter() - started)
    return batch_size / float(np.median(times))


def reproduce_xrec_fair(dataset_dir: Path, seed: int = 42) -> dict:
    """Matched public-data SID-AR / X-Rec / U2I training and trigger budget.

    This benchmark is CPU-only and does not stand in for the paper's production
    GPU streaming benchmark. All models receive 200 sequence-update steps.
    """
    from .sid_ar import SIDAutoregressive, fit_item_codes

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(min(torch.get_num_threads(), 4))
    data = load_movielens_1m_sequences(dataset_dir)
    if len(data.train) < 1000:
        raise ValueError("full MovieLens-1M is required")
    vectors = learn_item_vectors(data.train, data.item_count, seed=seed)
    anchors = cluster_anchors(vectors, 16, seed=seed)
    codes, codebooks = fit_item_codes(vectors, seed=seed)
    examples = training_examples(data.train, max_history=40)
    last = training_examples(data.train, max_history=40, last_only=True)
    xrec = XRec(vectors, anchors=16, max_history=40)
    sid_ar = SIDAutoregressive(vectors, codes, codebooks)
    u2i = U2IBaseline(vectors, width=48, max_history=40)
    training = {
        "xrec_pretrain": _fit(xrec, examples, seed=seed, steps=160, anchors=anchors),
        "xrec_sft": _fit(xrec, last, seed=seed + 1, steps=40, anchors=anchors),
        "sid_ar": _fit(sid_ar, examples, seed=seed, steps=200),
        "u2i": _fit(u2i, examples, seed=seed, steps=200),
    }

    def batch(histories):
        return batch_examples(tuple((history[-40:], 0) for history in histories), torch.arange(len(histories)))[:2]

    def xrec_generate(histories):
        history, valid = batch(histories)
        with torch.no_grad():
            return xrec.triggers(history, valid, samples=20, steps=3, seed=seed), vectors

    def sid_generate(histories):
        history, valid = batch(histories)
        with torch.no_grad():
            return sid_ar.trigger_vectors(history, valid, width=20), vectors

    def u2i_generate(histories):
        history, valid = batch(histories)
        with torch.no_grad():
            return u2i(history, valid)[:, None, :], vectors

    # U2I gets a single trigger and top 20; the other two get 20 × top 1.
    def u2i_recall(target):
        targets = data.validation if target == "validation" else data.test
        hits = 0
        for start in range(0, len(data.train), 32):
            contexts = [h + ((data.validation[i],) if target == "test" else ()) for i, h in enumerate(data.train[start:start + 32], start)]
            query, _ = u2i_generate(contexts)
            scores = (query[:, 0] @ vectors.T).cpu().numpy()
            for row, context in enumerate(contexts):
                scores[row, list(set(context))] = -np.inf
                top = np.argpartition(scores[row], -20)[-20:]
                hits += int(targets[start + row] in top)
        return hits / len(targets)

    validation = {
        "xrec": _recall_20x1(data, xrec_generate, target="validation"),
        "sid_ar": _recall_20x1(data, sid_generate, target="validation"),
        "u2i": u2i_recall("validation"),
    }
    test = {
        "xrec": _recall_20x1(data, xrec_generate, target="test"),
        "sid_ar": _recall_20x1(data, sid_generate, target="test"),
        "u2i": u2i_recall("test"),
    }
    sample_history, sample_valid = batch(list(data.train[:16]))
    throughput = {name: _generation_qps(fn, len(sample_history)) for name, fn in (
        ("xrec", lambda: xrec.triggers(sample_history, sample_valid, samples=20, steps=3, seed=seed)),
        ("sid_ar", lambda: sid_ar.trigger_vectors(sample_history, sample_valid, width=20)),
        ("u2i", lambda: u2i(sample_history, sample_valid)),
    )}
    return {
        "seed": seed,
        "dataset": {"name": "MovieLens 1M", "users": len(data.train), "items": data.item_count},
        "training": training,
        "validation_recall_at_20": validation,
        "test_recall_at_20": test,
        "generation_requests_per_second_cpu": throughput,
        "protocol": "train-only item vectors/SIDs; 200 model updates each; X-Rec and SID-AR 20 triggers × top1 exact NN; U2I 1 trigger × top20; seen-item filtered; CPU generation-only timing excludes packing and NN, batch 16, warmup 2, five repeats",
        "diagnostic_only": True,
    }


def _scorer(model: XRec | U2IBaseline, vectors: Tensor, *, seed: int):
    def score(histories: list[tuple[int, ...]]) -> np.ndarray:
        examples = tuple((history[-40:], 0) for history in histories)
        ids = torch.arange(len(examples))
        history, valid, _ = batch_examples(examples, ids)
        with torch.no_grad():
            if isinstance(model, XRec):
                triggers = model.triggers(history, valid, seed=seed)
                values = (triggers @ vectors.T).amax(dim=1)
            else:
                values = model(history, valid) @ vectors.T
        return values.numpy()

    return score


def reproduce_xrec(dataset_dir: Path, seed: int = 42) -> dict:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(min(torch.get_num_threads(), 4))
    data = load_movielens_1m_sequences(dataset_dir)
    if len(data.train) < 1000:
        raise ValueError("X-Rec requires the full MovieLens-1M public dataset")
    vectors = learn_item_vectors(data.train, data.item_count, seed=seed)
    labels = cluster_anchors(vectors, 16, seed=seed)
    all_prefixes = training_examples(data.train, max_history=40)
    last_prefixes = training_examples(data.train, max_history=40, last_only=True)
    method = XRec(vectors, anchors=16, max_history=40)
    baseline = U2IBaseline(vectors, width=48, max_history=40)
    method_pretrain = _fit(method, all_prefixes, seed=seed, steps=160, anchors=labels)
    method_sft = _fit(method, last_prefixes, seed=seed + 1, steps=40, anchors=labels)
    baseline_train = _fit(baseline, all_prefixes, seed=seed, steps=200)
    # Evaluate validation first. Never use test labels to choose model or budget.
    method_validation = batched_ranking_metrics(data, _scorer(method, vectors, seed=seed), 32, target="validation")
    baseline_validation = batched_ranking_metrics(data, _scorer(baseline, vectors, seed=seed), 32, target="validation")
    method_test = batched_ranking_metrics(data, _scorer(method, vectors, seed=seed), 32, target="test")
    baseline_test = batched_ranking_metrics(data, _scorer(baseline, vectors, seed=seed), 32, target="test")
    return {
        "paper": {"arxiv_id": "2609.29180", "title": "X-Rec Technical Report", "url": "https://arxiv.org/abs/2609.29180"},
        "dataset": {"name": "MovieLens 1M", "users": len(data.train), "items": data.item_count},
        "seed": seed,
        "training": {"item_contrastive_steps": 160, "pretraining_steps": 160, "sft_steps": 40, "baseline_steps": 200, "prefix_examples": len(all_prefixes), "sft_examples": len(last_prefixes), "method_pretrain_loss": method_pretrain, "method_sft_loss": method_sft, "baseline_loss": baseline_train},
        "validation": {"xrec": method_validation, "u2i": baseline_validation},
        "test": {"xrec": method_test, "u2i": baseline_test},
        "scope": "公开数据缩比核心机制：执行对比式 item 表征、球面锚点聚类、锚点 CE、RFM 目标、仅末层重复的去噪交互、球面 Euler 积分与多触发器全目录检索；无 TikTok 私有日志、目标属性、工业规模 embedding、线上 A/B 或生产 KV 服务栈。",
    }
