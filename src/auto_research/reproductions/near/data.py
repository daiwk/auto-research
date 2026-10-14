"""Public LongMemEval loader and frozen MiniLM content-token extraction.

Reference answers are never retained. Relevance lives in a separate evaluator
map; encoder inputs consist solely of question and haystack session text.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class MemoryQuery:
    id: str
    question: str
    memories: tuple[str, ...]
    memory_ids: tuple[str, ...]
    group: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_longmemeval(path: Path, limit: int | None = None
                    ) -> tuple[list[MemoryQuery], dict[str, set[str]]]:
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    queries, relevance = [], {}
    # Limit is fixed in source order before inspecting relevance labels.
    for row in raw[:limit]:
        identifier = str(row["question_id"])
        ids = tuple(str(x) for x in row["haystack_session_ids"])
        sessions = row["haystack_sessions"]
        if len(ids) != len(sessions):
            raise ValueError("session IDs must align with the memory records")
        texts = tuple("\n".join(f"{turn['role']}: {turn['content']}" for turn in session)
                      for session in sessions)
        # The official file repeats a small number of session IDs. Merge only
        # those identities, without looking at query/relevance/answer fields.
        unique: dict[str, str] = {}
        for memory_id, text in zip(ids, texts, strict=True):
            if memory_id not in unique:
                unique[memory_id] = text
            elif unique[memory_id] != text:
                unique[memory_id] += "\n" + text
        ids, texts = tuple(unique), tuple(unique.values())
        group = hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()
        queries.append(MemoryQuery(identifier, row["question"], texts, ids, group))
        relevance[identifier] = {str(x) for x in row.get("answer_session_ids", [])}
    return queries, relevance


def grouped_split(queries: list[MemoryQuery]) -> dict[str, list[MemoryQuery]]:
    """Connected memory-bank groups, preventing overlap across all three splits."""
    parent = list(range(len(queries)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen = {}
    for i, q in enumerate(queries):
        for memory in q.memory_ids:
            if memory in seen:
                parent[find(i)] = find(seen[memory])
            else:
                seen[memory] = i
    groups: dict[int, list[MemoryQuery]] = {}
    for i, q in enumerate(queries):
        groups.setdefault(find(i), []).append(q)
    ordered = sorted(groups.values(), key=lambda group: hashlib.sha256(
        ("oct13-memory-split-v1:" + ":".join(sorted(q.id for q in group))).encode()).hexdigest())
    if len(ordered) < 3:
        raise ValueError("at least three disjoint memory-bank groups required")
    train_n = min(len(ordered) - 2, max(1, int(0.6 * len(ordered))))
    val_n = max(1, int(0.2 * len(ordered)))
    parts = (ordered[:train_n], ordered[train_n:train_n + val_n], ordered[train_n + val_n:])
    return {name: [q for group in part for q in group]
            for name, part in zip(("train", "validation", "test"), parts, strict=True)}


def query_disjoint_shared_bank_split(queries: list[MemoryQuery]) -> dict[str, list[MemoryQuery]]:
    """Explicit diagnostic alternative; not an unseen-bank generalization test."""
    if len(queries) < 5 or len({q.id for q in queries}) != len(queries):
        raise ValueError("at least five unique query IDs required for shared-bank protocol")
    ordered = sorted(queries, key=lambda q: hashlib.sha256(
        ("oct13-shared-bank-v1:" + q.id).encode()).hexdigest())
    train_n, val_n = int(0.6 * len(ordered)), max(1, int(0.2 * len(ordered)))
    return {"train": ordered[:train_n], "validation": ordered[train_n:train_n + val_n],
            "test": ordered[train_n + val_n:]}


class FrozenMiniLM:
    """Native masked-mean pool; local token mask excludes special/padding tokens."""

    def __init__(self, model_dir: Path, device: str = "cpu", max_length: int = 128):
        import torch
        from transformers import AutoModel, AutoTokenizer
        self.torch = torch
        self.device, self.max_length = device, max_length
        self.tokenizer = AutoTokenizer.from_pretrained(str(model_dir), local_files_only=True)
        self.model = AutoModel.from_pretrained(str(model_dir), local_files_only=True).to(device)
        self.model.eval().requires_grad_(False)

    def encode(self, texts: list[str], batch_size: int = 16) -> tuple[np.ndarray, list[np.ndarray]]:
        pools, tokens = [], []
        for start in range(0, len(texts), batch_size):
            inputs = self.tokenizer(texts[start:start + batch_size], return_tensors="pt", padding=True,
                                    truncation=True, max_length=self.max_length,
                                    return_special_tokens_mask=True)
            special = inputs.pop("special_tokens_mask").bool()
            mask = inputs["attention_mask"].bool()
            with self.torch.no_grad():
                hidden = self.model(**{k: v.to(self.device) for k, v in inputs.items()}).last_hidden_state
                mean = (hidden * mask.to(self.device).unsqueeze(-1)).sum(1)
                mean /= mask.sum(1).to(self.device).clamp_min(1).unsqueeze(-1)
                pools.extend(self.torch.nn.functional.normalize(mean.float(), dim=-1).cpu().numpy())
                normalized = self.torch.nn.functional.normalize(hidden.float(), dim=-1).cpu().numpy()
            for row, content in zip(normalized, (mask & ~special).numpy(), strict=True):
                if not content.any():
                    raise ValueError("empty content token sequence")
                tokens.append(row[content])
        return np.asarray(pools), tokens


def retrieval_metrics(ranking: list[str], relevant: set[str], k: int = 10) -> dict[str, float]:
    if not relevant:
        raise ValueError("unanswerable queries must be counted separately, not scored as retrieval successes")
    hits = [float(m in relevant) for m in ranking[:k]]
    discounts = 1 / np.log2(np.arange(2, len(hits) + 2))
    ideal = np.sum(1 / np.log2(np.arange(2, min(k, len(relevant)) + 2)))
    return {"recall_at_10": sum(hits) / min(k, len(relevant)),
            "ndcg_at_10": float(np.dot(hits, discounts) / ideal)}
