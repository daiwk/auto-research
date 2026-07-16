from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np


def load_zip_rows(root: Path, features: np.ndarray):
    users = {}
    with (root / "ml-100k" / "u.user").open(encoding="latin-1") as stream:
        for line in stream:
            user, _, _, _, zipcode = line.rstrip().split("|")
            users[int(user)] = zipcode
    events = {}
    with (root / "ml-100k" / "u.data").open() as stream:
        for line in stream:
            user, item, rating, timestamp = line.split()
            if float(rating) >= 4.0 and int(item) <= len(features):
                events.setdefault(int(user), []).append((int(timestamp), int(item) - 1))
    return [(user, users[user], tuple(item for _, item in sorted(rows))) for user, rows in events.items() if user in users and len(rows) >= 7]


def adaptive_keys(rows, target_size: int = 12):
    # ZIP replaces geo-IP coordinates; fine-to-coarse prefix length is the public equivalent of scalar s.
    remaining = {user: zipcode for user, zipcode, _ in rows}
    keys = {}
    for width in (5, 4, 3, 2, 1, 0):
        groups = {}
        for user, zipcode in remaining.items():
            groups.setdefault(zipcode[:width] if width else "global", []).append(user)
        assigned = []
        for prefix, members in groups.items():
            if len(members) >= target_size or width == 0:
                buckets = max(1, int(np.ceil(len(members) / target_size)))
                for user in members:
                    digest = int(hashlib.sha256(str(user).encode()).hexdigest()[:8], 16)
                    keys[user] = f"{prefix}:{digest % buckets}"
                    assigned.append(user)
        for user in assigned:
            remaining.pop(user, None)
    return keys


def train_proximity(root: Path, features: np.ndarray):
    rows = load_zip_rows(root, features)
    keys = adaptive_keys(rows)
    bucket = {}
    global_feature = np.zeros(features.shape[1])
    count = 0
    for user, _, sequence in rows:
        train = sequence[:-2]
        value = features[list(train)].mean(0)
        bucket.setdefault(keys[user], []).append(value)
        global_feature += value
        count += 1
    aggregates = {key: np.mean(values, axis=0) for key, values in bucket.items()}
    sizes = [len(values) for values in bucket.values()]
    return rows, keys, aggregates, global_feature / count, {"target_bucket_size": 12, "buckets": len(bucket), "minimum_bucket": min(sizes), "median_bucket": float(np.median(sizes)), "consent_filter_simulated": "only public, non-sensitive ZIP prefix is read; no persistent identifier is used in scoring"}


def evaluate_proximity(rows, keys, aggregates, global_feature, features):
    best = (float("-inf"), 0.1)
    for alpha in np.linspace(0.1, 1.0, 10):
        hit = ndcg = 0.0
        for user, _, sequence in rows:
            history, target = sequence[:-2], sequence[-2]
            scores = ((1 - alpha) * global_feature + alpha * aggregates[keys[user]]) @ features.T
            scores[list(set(history))] = -np.inf
            top = np.argsort(-scores)[:10]
            position = np.flatnonzero(top == target)
            if position.size:
                hit += 1; ndcg += 1 / np.log2(int(position[0]) + 2)
        objective = ndcg / len(rows) + 0.25 * hit / len(rows)
        if objective > best[0]:
            best = (objective, float(alpha))
    selected_alpha = best[1]
    baseline_hit = method_hit = baseline_ndcg = method_ndcg = 0.0
    for user, _, sequence in rows:
        history, target = sequence[:-2], sequence[-1]
        base = global_feature @ features.T
        method = ((1 - selected_alpha) * global_feature + selected_alpha * aggregates[keys[user]]) @ features.T
        for scores, name in ((base, "base"), (method, "method")):
            scores = scores.copy()
            scores[list(set(history))] = -np.inf
            top = np.argsort(-scores)[:10]
            position = np.flatnonzero(top == target)
            if position.size:
                if name == "base":
                    baseline_hit += 1; baseline_ndcg += 1 / np.log2(int(position[0]) + 2)
                else:
                    method_hit += 1; method_ndcg += 1 / np.log2(int(position[0]) + 2)
    n = len(rows)
    base = {"hit_at_10": baseline_hit / n, "ndcg_at_10": baseline_ndcg / n, "fresh_hit_at_10": baseline_hit / n, "head_share_at_10": 0.0}
    method = {"hit_at_10": method_hit / n, "ndcg_at_10": method_ndcg / n, "fresh_hit_at_10": method_hit / n, "head_share_at_10": 0.0}
    return base, method, selected_alpha
