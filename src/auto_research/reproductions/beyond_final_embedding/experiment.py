"""Actual frozen content-token extraction and source-query adapter training."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np

from ..near.data import retrieval_metrics
from ..near.experiment import _mean, comparison_contract, pooled_baseline, prepare, render
from .algorithm import SparseTokenIndex, multipositive_maxsim_loss, query_adapter


def _evaluate(rows, labels, features, adapter, device, alpha):
    import torch
    scored, rankings = [], {}
    for query in rows:
        if not labels[query.id]:
            continue
        feature = features[query.id]
        tokens = feature["tokens_q"]
        if adapter is not None:
            with torch.no_grad():
                tokens = adapter(torch.as_tensor(tokens, device=device)).cpu().numpy()
        index = SparseTokenIndex(feature["tokens_m"], feature["pool_m"], device)
        scores = index.scores(tokens, feature["pool_q"], alpha=alpha)
        order = np.argsort(-scores, kind="stable")[:10]
        ranking = [query.memory_ids[i] for i in order]
        scored.append(retrieval_metrics(ranking, labels[query.id]))
        rankings[query.id] = ranking
    return _mean(scored), rankings


def run_beyond(config: dict, seed: int) -> dict:
    import torch
    torch.manual_seed(seed)
    split, labels, features, protocol = prepare(config)
    device = config.get("device", "cpu")
    dimension = next(iter(features.values()))["pool_q"].shape[0]
    adapter = query_adapter(dimension, config.get("rank", 32)).to(device)
    optimizer = torch.optim.AdamW(adapter.parameters(), lr=1e-4, weight_decay=1e-4)
    max_epochs = config.get("adapter_epochs", 2)
    trials, best, best_state = [], None, None
    training_losses = []
    for epoch in range(max_epochs + 1):
        if epoch:
            order = torch.randperm(len(split["train"])).tolist()
            adapter.train()
            losses = []
            for position in order:
                query = split["train"][position]
                if not labels[query.id]:
                    continue
                feature = features[query.id]
                q = torch.as_tensor(feature["tokens_q"], device=device)
                memories = [torch.as_tensor(x, device=device) for x in feature["tokens_m"]]
                positives = {i for i, memory in enumerate(query.memory_ids) if memory in labels[query.id]}
                loss = multipositive_maxsim_loss(adapter(q), memories, positives)
                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(adapter.parameters(), 1)
                optimizer.step()
                losses.append(float(loss.detach()))
            training_losses.append({"epoch": epoch, "maxsim_loss": float(np.mean(losses))})
        adapter.eval()
        for alpha in (0.25, 0.5, 0.75):
            metric, _ = _evaluate(split["validation"], labels, features, adapter, device, alpha)
            trial = {"epoch": epoch, "alpha": alpha, "validation": metric}
            trials.append(trial)
            if best is None or metric["ndcg_at_10"] > best["validation"]["ndcg_at_10"]:
                best, best_state = trial, copy.deepcopy(adapter.state_dict())
    adapter.load_state_dict(best_state)
    test, rankings = _evaluate(split["test"], labels, features, adapter, device, best["alpha"])
    training_free, _ = _evaluate(split["test"], labels, features, None, device, 0.5)
    baseline = pooled_baseline(split["test"], labels, features)
    return {"paper": "beyond-final-embedding", "seed": seed, "device": device,
            "evaluation_tier": "l2_public_dataset", "fidelity": "core_mechanism",
            "diagnostic_only": protocol["shared_unlabelled_memory"],
            "promotion_eligible": not protocol["shared_unlabelled_memory"],
            "protocol": {**protocol, "token_budget": 64, "adapter_rank": config.get("rank", 32),
                         "adapter_epochs": max_epochs, "encoder_and_memory_frozen": True},
            "comparison_contract": comparison_contract(protocol, "frozen MiniLM native pooled cosine",
                                                       "beyond-final-embedding"),
            "selection": best, "validation_trials": trials, "training_losses": training_losses,
            "test": test, "training_free_test": training_free, "baseline": baseline,
            "test_rankings": rankings,
            "parameter_update_l2": float(torch.linalg.vector_norm(adapter.b.weight).detach()),
            "limitations": ["MiniLM replaces original backbones", "exact sparse search replaces HNSW",
                            "LongMemEval source split replaces EvoTrain; no original downstream QA",
                            "training uses memory relevance labels, never reference answer text"]}


def reproduce_beyond(dataset_dir: Path, seed: int) -> dict:
    return run_beyond(json.loads((dataset_dir / "beyond-final-embedding.json").read_text()), seed)


__all__ = ["reproduce_beyond", "render", "run_beyond"]
