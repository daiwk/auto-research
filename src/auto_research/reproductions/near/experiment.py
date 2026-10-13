"""Bounded real frozen-encoder retrieval; selection reads validation only."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

from .algorithm import NEARIndex
from .data import (FrozenMiniLM, grouped_split, load_longmemeval,
                   query_disjoint_shared_bank_split, retrieval_metrics, sha256_file)


def _mean(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("at least one answerable query required in each evaluation split")
    return {key: float(np.mean([row[key] for row in rows])) for key in rows[0]}


def verify_provenance(root: Path, public_id: str, revision: str,
                      required: tuple[str, ...]) -> dict:
    provenance = json.loads((root / "provenance.json").read_text())
    if provenance.get("public_id") != public_id or provenance.get("revision") != revision:
        raise ValueError(f"pinned public resource mismatch: {public_id}")
    for name in required:
        expected = provenance.get("files", {}).get(name)
        if not isinstance(expected, str) or sha256_file(root / name) != expected:
            raise ValueError(f"resource checksum mismatch: {name}")
    return {"public_id": public_id, "revision": revision,
            "files": {name: provenance["files"][name] for name in required}}


def prepare(config: dict) -> tuple:
    raw = Path(config["raw_data"])
    expected = "d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442"
    if sha256_file(raw) != expected:
        raise ValueError("LongMemEval official pinned raw SHA256 mismatch")
    model = Path(config["model_dir"])
    model_provenance = verify_provenance(
        model, "sentence-transformers/all-MiniLM-L6-v2",
        "1110a243fdf4706b3f48f1d95db1a4f5529b4d41",
        ("config.json", "model.safetensors", "tokenizer.json", "vocab.txt"))
    queries, labels = load_longmemeval(raw, config.get("max_queries", 30))
    split_policy = config.get("split_policy", "bank-disjoint")
    if split_policy == "bank-disjoint":
        split = grouped_split(queries)
    elif split_policy == "query-disjoint-shared-bank":
        split = query_disjoint_shared_bank_split(queries)
    else:
        raise ValueError("unknown split policy; no implicit shared-bank fallback")
    encoder = FrozenMiniLM(model, config.get("device", "cpu"), config.get("max_length", 128))
    features, memory_cache = {}, {}
    for query in queries:
        missing = list(dict.fromkeys(text for text in query.memories if text not in memory_cache))
        if missing:
            pools, tokens = encoder.encode(missing, config.get("batch_size", 16))
            memory_cache.update({text: (pool, token) for text, pool, token in zip(missing, pools, tokens, strict=True)})
        pools_q, tokens_q = encoder.encode([query.question])
        features[query.id] = {"pool_q": pools_q[0],
            "pool_m": np.asarray([memory_cache[text][0] for text in query.memories]),
            "tokens_q": tokens_q[0], "tokens_m": [memory_cache[text][1] for text in query.memories]}
    split_ids = {name: [q.id for q in rows] for name, rows in split.items()}
    fingerprint = hashlib.sha256(json.dumps(split_ids, sort_keys=True).encode()).hexdigest()
    protocol = {"dataset": "xiaowu0162/longmemeval-cleaned",
                "dataset_revision": "98d7416c24c778c2fee6e6f3006e7a073259d48f",
                "raw_sha256": expected, "split_ids": split_ids, "split_revision": fingerprint,
                "split_policy": split_policy,
                "split_rule": ("connected candidate-session ID components; fixed hash order; 60/20/20"
                    if split_policy == "bank-disjoint" else "query-ID-only fixed hash order; 60/20/20"),
                "shared_unlabelled_memory": split_policy == "query-disjoint-shared-bank",
                "unseen_bank_generalization": False,
                "memory_encoding_cache": "immutable frozen encodings keyed by source text; no query or relevance",
                "max_queries": config.get("max_queries", 30),
                "max_length": config.get("max_length", 128),
                "encoder": model_provenance, "index": "exact-inner-product (not original HNSW)",
                "answer_fields_exposed": False,
                "label_boundary": "train labels for optional adapter loss; validation selection; test scorer only",
                "unanswerable_queries": sum(not labels[q.id] for q in queries),
                "nonofficial_benchmark": True}
    return split, labels, features, protocol


def _evaluate_near(rows, labels, features, params, seed):
    scored, rankings = [], {}
    for query in rows:
        if not labels[query.id]:
            continue
        feature = features[query.id]
        index = NEARIndex(seed=seed, **params).fit(feature["pool_m"])
        order = index.search(feature["pool_q"]).tolist()
        ranking = [query.memory_ids[i] for i in order]
        rankings[query.id] = ranking
        scored.append(retrieval_metrics(ranking, labels[query.id]))
    return _mean(scored), rankings


def pooled_baseline(rows, labels, features):
    scored = []
    for query in rows:
        if labels[query.id]:
            feature = features[query.id]
            order = np.argsort(-(feature["pool_m"] @ feature["pool_q"]), kind="stable")
            scored.append(retrieval_metrics([query.memory_ids[i] for i in order[:10]], labels[query.id]))
    return _mean(scored)


def comparison_contract(protocol: dict, baseline: str, key: str) -> dict:
    source = Path(__file__).parent
    files = [*source.glob("*.py")]
    if key == "beyond-final-embedding":
        files.extend((source.parent / "beyond_final_embedding").glob("*.py"))
    digest = hashlib.sha256()
    for path in sorted(files):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return {"protocol_id": f"oct13-{key}-longmemeval-minilm-{protocol.get('split_policy', 'bank-disjoint')}-v1",
            "dataset_revision": protocol["dataset_revision"] + ":" + protocol["raw_sha256"],
            "split_revision": protocol["split_revision"], "baseline": baseline,
            "code_revision": digest.hexdigest(), "test_isolated": True}


def run_near(config: dict, seed: int) -> dict:
    split, labels, features, protocol = prepare(config)
    trials = []
    for depth, normalize, alpha in itertools.product((1, 2, 3), (False, True), (0.25, 0.5, 1, 2, 4)):
        params = {"depth": depth, "normalize_residual": normalize, "alpha": alpha}
        validation, _ = _evaluate_near(split["validation"], labels, features, params, seed)
        trials.append({"parameters": params, "validation": validation})
    selected = max(trials, key=lambda x: x["validation"]["ndcg_at_10"])
    test, rankings = _evaluate_near(split["test"], labels, features, selected["parameters"], seed)
    baseline = pooled_baseline(split["test"], labels, features)
    return {"paper": "near", "seed": seed, "device": config.get("device", "cpu"),
            "evaluation_tier": "l2_public_dataset", "fidelity": "core_mechanism",
            "diagnostic_only": protocol["shared_unlabelled_memory"],
            "promotion_eligible": not protocol["shared_unlabelled_memory"], "protocol": protocol,
            "comparison_contract": comparison_contract(protocol, "frozen MiniLM native pooled cosine", "near"),
            "selection": selected, "validation_trials": trials,
            "test": test, "baseline": baseline, "test_rankings": rankings,
            "limitations": ["MiniLM replaces paper backbones", "exact search replaces HNSW",
                            "bounded source-order query set; not full LMEB or downstream QA",
                            "three seeds are required before any stable comparison claim"]}


def reproduce_near(dataset_dir: Path, seed: int) -> dict:
    return run_near(json.loads((dataset_dir / "near.json").read_text()), seed)


def render(result: dict) -> str:
    return (f"# {result['paper']} 实际公开数据评测\n\n"
            f"seed={result['seed']}；缩放、非官方 benchmark；未运行论文下游 QA。\n\n"
            f"验证选择：`{result.get('selection')}`\n\n"
            f"Test：`{result['test']}`；同协议基线：`{result['baseline']}`。\n")
