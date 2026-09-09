"""Timestamp-split Amazon Beauty interactions and public product content.

Review sequences are a next-product task, NOT semantic complementarity labels.
Metadata relation edges are never included in content features.
"""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import re

import numpy as np

from ..datasets import amazon_beauty_5core
from .industrial_batch import CompactSequences
from .industrial_2026 import IndustrialData


def load_product_data(root: Path, maximum_items=2000, maximum_users=1000):
    interactions = amazon_beauty_5core(root, allow_network=False)
    metadata_path = root / "amazon-beauty-5core/meta_Beauty.json.gz"
    histories = defaultdict(list)
    for user, item, _, timestamp in interactions:
        histories[user].append((timestamp, item))
    split = []
    for user in sorted(histories):
        ordered = sorted(histories[user])
        items = list(dict.fromkeys(item for _, item in ordered))
        if len(items) >= 5:
            split.append((items[:-2], items[-2], items[-1]))
    frequency = Counter(item for history, _, _ in split for item in history)
    selected = {item for item, _ in sorted(frequency.items(), key=lambda row: (-row[1], row[0]))[:maximum_items]}
    metadata = {}
    with gzip.open(metadata_path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = ast.literal_eval(line)  # upstream is Python literals; never eval
            if row.get("asin") in selected:
                metadata[row["asin"]] = row
    selected &= metadata.keys()
    item_ids = sorted(selected)
    mapping = {item: index for index, item in enumerate(item_ids)}
    rows = []
    for history, validation, test in split:
        train = [mapping[item] for item in history if item in selected]
        if len(train) >= 3 and validation in selected and test in selected:
            rows.append((train, mapping[validation], mapping[test]))
        if len(rows) >= maximum_users:
            break
    if not rows:
        raise ValueError("No timestamp-heldout users within training-only catalog")
    categories = []
    features = np.zeros((len(item_ids), 256), dtype=np.float32)
    for index, item in enumerate(item_ids):
        row = metadata[item]
        category_paths = row.get("categories") or [["unknown"]]
        path = category_paths[0] or ["unknown"]
        categories.append(" / ".join(path))
        text = " ".join(str(row.get(field, "")) for field in ("title", "description", "brand"))
        for token in re.findall(r"\w+", text.lower()):
            bucket = int.from_bytes(hashlib.sha256(token.encode()).digest()[:4], "big") % 256
            features[index, bucket] += 1
    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1)
    category_ids = {name: index for index, name in enumerate(sorted(set(categories)))}
    domains = np.asarray([category_ids[name] for name in categories])
    popularity = np.zeros(len(item_ids), dtype=np.float32)
    transition = np.full((len(item_ids), len(item_ids)), 1e-3)
    for history, _, _ in rows:
        for item in history:
            popularity[item] += 1
        for source, target in zip(history, history[1:]):
            transition[source, target] += 1
    transition /= transition.sum(axis=1, keepdims=True)
    sequences = CompactSequences(tuple(tuple(row[0]) for row in rows),
                                 tuple(row[1] for row in rows), tuple(row[2] for row in rows),
                                 features, popularity)
    normalized = np.log1p(popularity)
    normalized /= max(float(normalized.max()), 1)
    data = IndustrialData(sequences, transition, features @ features.T, normalized, domains)
    fingerprints = {}
    for path in (metadata_path, root / "amazon-beauty-5core/reviews_Beauty_5.json.gz"):
        with path.open("rb") as stream:
            fingerprints[path.name] = hashlib.file_digest(stream, "sha256").hexdigest()
    evidence = {
        "dataset": "Amazon Beauty 2014 5-core",
        "source": "https://cseweb.ucsd.edu/~jmcauley/datasets/amazon/links.html",
        "sha256": fingerprints, "users": len(rows), "items": len(item_ids),
        "categories": len(category_ids), "train_interactions": int(popularity.sum()),
        "split": "per-user chronological last-two; catalog selected using training counts only",
        "split_sha256": hashlib.sha256(json.dumps(rows).encode()).hexdigest(),
        "content": "hashed title/description/brand; no review text or related-product edges",
        "task": "next-product retrieval, not labelled semantic complementarity",
    }
    return data, evidence
