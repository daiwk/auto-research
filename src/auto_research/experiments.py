from __future__ import annotations

import json
import math
import os
import random
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

from .datasets import movielens_100k, tiny_shakespeare

MetricFn = Callable[[dict[str, Any]], float]


def builtin_experiment(
    track: str, dataset_dir: Path, seed: int, allow_network: bool
) -> tuple[str, str, MetricFn]:
    if track == "llm":
        text = tiny_shakespeare(dataset_dir, allow_network)
        return "validation_perplexity", "minimize", lambda p: ngram_perplexity(text, p)
    ratings = movielens_100k(dataset_dir, allow_network)
    return "validation_rmse", "minimize", lambda p: matrix_factorization_rmse(ratings, p, seed)


def ngram_perplexity(text: str, params: dict[str, Any]) -> float:
    """Fast local proxy for language-model architecture/search experiments."""
    limit = min(int(params.get("train_chars", 50000)), len(text) - 1000)
    train = text[:limit]
    valid = text[limit : min(limit + 10000, len(text))]
    order = int(params.get("order", 3))
    alpha = float(params.get("alpha", 0.1))
    vocab = max(len(set(train)), 1)
    contexts: dict[str, Counter[str]] = defaultdict(Counter)
    totals: Counter[str] = Counter()
    for index in range(order - 1, len(train)):
        context = train[index - order + 1 : index]
        contexts[context][train[index]] += 1
        totals[context] += 1
    loss = 0.0
    count = 0
    for index in range(order - 1, len(valid)):
        context = valid[index - order + 1 : index]
        probability = (contexts[context][valid[index]] + alpha) / (
            totals[context] + alpha * vocab
        )
        loss -= math.log(probability)
        count += 1
    return math.exp(loss / max(count, 1))


def matrix_factorization_rmse(
    ratings: list[tuple[int, int, float, int]], params: dict[str, Any], seed: int
) -> float:
    """Biased matrix factorization on MovieLens 100K, using a chronological split."""
    ordered = sorted(ratings, key=lambda row: row[3])
    cutoff = int(len(ordered) * 0.8)
    train, valid = ordered[:cutoff], ordered[cutoff:]
    factors = int(params.get("factors", 16))
    lr = float(params.get("learning_rate", 0.01))
    reg = float(params.get("regularization", 0.05))
    epochs = int(params.get("epochs", 8))
    rng = random.Random(seed)
    global_mean = sum(row[2] for row in train) / len(train)
    users: dict[int, list[float]] = {}
    items: dict[int, list[float]] = {}
    user_bias: defaultdict[int, float] = defaultdict(float)
    item_bias: defaultdict[int, float] = defaultdict(float)

    def vector(table: dict[int, list[float]], key: int) -> list[float]:
        if key not in table:
            table[key] = [(rng.random() - 0.5) * 0.1 for _ in range(factors)]
        return table[key]

    samples = list(train)
    for _ in range(epochs):
        rng.shuffle(samples)
        for user, item, rating, _timestamp in samples:
            pu, qi = vector(users, user), vector(items, item)
            prediction = global_mean + user_bias[user] + item_bias[item]
            prediction += sum(left * right for left, right in zip(pu, qi))
            error = rating - prediction
            user_bias[user] += lr * (error - reg * user_bias[user])
            item_bias[item] += lr * (error - reg * item_bias[item])
            for index in range(factors):
                old_user = pu[index]
                pu[index] += lr * (error * qi[index] - reg * pu[index])
                qi[index] += lr * (error * old_user - reg * qi[index])
    squared_error = 0.0
    for user, item, rating, _timestamp in valid:
        prediction = global_mean + user_bias[user] + item_bias[item]
        if user in users and item in items:
            prediction += sum(a * b for a, b in zip(users[user], items[item]))
        prediction = min(5.0, max(1.0, prediction))
        squared_error += (rating - prediction) ** 2
    return math.sqrt(squared_error / len(valid))


def command_experiment(
    command: list[str], metric_name: str, timeout: int, workdir: Path
) -> MetricFn:
    """Run a user-approved command. It must print a JSON object on its last line."""
    if not command:
        raise ValueError("experiment_command must not be empty")

    def run(params: dict[str, Any]) -> float:
        env = os.environ.copy()
        env["AUTO_RESEARCH_PARAMS"] = json.dumps(params)
        completed = subprocess.run(
            command,
            cwd=workdir,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr[-2000:] or f"exit code {completed.returncode}")
        last_line = next((line for line in reversed(completed.stdout.splitlines()) if line), "")
        payload = json.loads(last_line)
        return float(payload[metric_name])

    return run


def prepare_implementation(
    command: list[str], manifest: dict[str, Any], timeout: int, workdir: Path
) -> None:
    """Run an explicitly configured paper-to-code step before experiments.

    The command receives a read-only research manifest through the environment. It is
    intentionally opt-in because generated code must be reviewed and sandboxed by the user.
    """
    env = os.environ.copy()
    env["AUTO_RESEARCH_MANIFEST"] = json.dumps(manifest, ensure_ascii=False)
    completed = subprocess.run(
        command,
        cwd=workdir,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            "implementation command failed: "
            + (completed.stderr[-3000:] or f"exit code {completed.returncode}")
        )
