from __future__ import annotations

import json
import hashlib
import re

import numpy as np


def _words(text):
    return re.findall(r"[A-Za-z0-9']+", text.lower())


def _corruptions(answer: str):
    words = _words(answer)
    if not words:
        words = ["unknown"]
    truncated = " ".join(words[: max(1, len(words) // 4)])
    shuffled = " ".join(words[::2] + words[1::2])
    return answer, truncated, shuffled


def _hash_vector(text: str, dimensions: int = 192):
    values = np.zeros(dimensions, dtype=np.float64)
    for token in _words(text):
        bucket = int.from_bytes(hashlib.blake2b(token.encode(), digest_size=4).digest(), "big")
        values[bucket % dimensions] += 1.0
    return values / max(np.linalg.norm(values), 1.0)


def _rubrics(prompt: str, response: str):
    prompt_words = set(_words(prompt))
    response_words = _words(response)
    unique = set(response_words)
    coverage = len(prompt_words & unique) / max(len(prompt_words), 1)
    adequate = min(len(response_words) / 24.0, 1.0)
    diversity = len(unique) / max(len(response_words), 1)
    structure = float(any(mark in response for mark in (".", ":", "\n", "1.", "- ")))
    return np.asarray([coverage, adequate, diversity, structure], dtype=np.float64)


def load_alpaca_preferences(dataset_dir, maximum_examples: int = 900, seed: int = 42):
    path = dataset_dir / "alpaca" / "alpaca_data.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    rng = np.random.default_rng(seed)
    chosen = rng.choice(len(rows), min(maximum_examples, len(rows)), replace=False)
    examples = []
    for index in chosen:
        row = rows[int(index)]
        prompt = (row["instruction"] + " " + row.get("input", "")).strip()
        candidates = _corruptions(row["output"])
        examples.append({
            "prompt": prompt,
            "prompt_vector": _hash_vector(prompt),
            "candidate_vectors": np.stack([_hash_vector(prompt + " " + candidate) for candidate in candidates]),
            "rubrics": np.stack([_rubrics(prompt, candidate) for candidate in candidates]),
            "gold": 0,
        })
    split = int(len(examples) * 0.8)
    return examples[:split], examples[split:]
