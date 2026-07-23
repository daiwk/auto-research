from __future__ import annotations

import json
import re

import numpy as np


def _answer(text: str):
    match = re.search(r"####\s*(-?[\d,]+(?:\.\d+)?)", text)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def _pair_features(question: str, candidate: float):
    numbers = [
        float(value.replace(",", ""))
        for value in re.findall(r"-?\d[\d,]*(?:\.\d+)?", question)
    ]
    numbers = numbers[:8] or [0.0]
    total = sum(numbers)
    product = float(np.prod(numbers[:3])) if len(numbers) <= 3 else numbers[0] * numbers[1]
    differences = [abs(candidate - total), abs(candidate - product)]
    if len(numbers) >= 2:
        differences.extend([abs(candidate - (numbers[0] - numbers[1])), abs(candidate - (numbers[0] / max(numbers[1], 1e-6)))])
    else:
        differences.extend([abs(candidate - numbers[0]), abs(candidate - numbers[0])])
    scale = max(abs(candidate), abs(total), abs(product), 1.0)
    keywords = question.lower()
    return np.asarray([
        1.0,
        np.tanh(candidate / 100.0),
        np.exp(-differences[0] / scale),
        np.exp(-differences[1] / scale),
        np.exp(-differences[2] / scale),
        np.exp(-differences[3] / scale),
        float(any(word in keywords for word in ("total", "altogether", "sum", "combined"))),
        float(any(word in keywords for word in ("each", "times", "per", "every"))),
        float(any(word in keywords for word in ("left", "remain", "difference", "fewer"))),
        float(any(word in keywords for word in ("average", "ratio", "percent"))),
    ], dtype=np.float64)


def _example(row, rng):
    gold = _answer(row["answer"])
    if gold is None or not np.isfinite(gold):
        return None
    scale = max(1.0, abs(gold) * 0.08)
    distractors = [gold + offset * scale for offset in (-3, -2, -1, 1, 2, 3, 5)]
    candidates = np.asarray([gold, *distractors], dtype=np.float64)
    order = rng.permutation(len(candidates))
    candidates = candidates[order]
    gold_index = int(np.flatnonzero(order == 0)[0])
    return {
        "features": np.stack([_pair_features(row["question"], value) for value in candidates]),
        "gold": gold_index,
        "guide": row["answer"].split("####")[0].strip(),
        "candidate_values": candidates,
    }


def load_gsm8k(dataset_dir, maximum_train: int = 1200, maximum_test: int = 300, seed: int = 42):
    root = dataset_dir / "gsm8k"
    train_path, test_path = root / "train.jsonl", root / "test.jsonl"
    if not train_path.exists() or not test_path.exists():
        raise FileNotFoundError(
            "GSM8K is missing. Run `scripts/download_public_data.sh gsm8k` or place "
            "the official train.jsonl/test.jsonl under data/gsm8k/."
        )
    rng = np.random.default_rng(seed)
    def read(path, limit):
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        chosen = rng.choice(len(rows), min(limit, len(rows)), replace=False)
        return [example for index in chosen if (example := _example(rows[int(index)], rng)) is not None]
    return read(train_path, maximum_train), read(test_path, maximum_test)
