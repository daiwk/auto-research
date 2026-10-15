"""Bounded CASI mechanism audit; no language-model or auction simulation claim."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .algorithm import (Candidate, CachedCoalitionEvaluator, RetrievalSnapshot,
                        credit_rules, permutation_credit, shape_advantages,
                        token_advantages)


def run(dataset_dir: Path, seed: int) -> dict:
    path = dataset_dir / "casi-snapshot.json"
    source = "controlled frozen retrieval example; no private production data"
    if path.exists():
        if path.stat().st_size > 2_000_000:
            raise ValueError("snapshot exceeds the 2 MB component input budget")
        payload = json.loads(path.read_text())
        if set(payload) != {"actions"} or not 1 <= len(payload["actions"]) <= 8:
            raise ValueError("snapshot requires actions only and at most eight actions")
        if any(not isinstance(row.get("candidates"), list) or len(row["candidates"]) > 1024
               for row in payload["actions"]):
            raise ValueError("each action requires at most 1024 cached candidates")
        actions = tuple(row["key"] for row in payload["actions"])
        rows = {row["key"]: tuple(Candidate(**c) for c in row["candidates"])
                for row in payload["actions"]}
        source = "user-supplied frozen snapshot; caller owns value semantics"
    else:
        actions = tuple(f"rewrite-{i}" for i in range(5))
        candidates = (Candidate("a", 4, 1), Candidate("b", 3, 5),
                      Candidate("c", 2, -2), Candidate("d", 1, 3))
        indices = ((0, 1), (1, 2), (2, 3), (0, 3), (1,))
        rows = {action: tuple(candidates[i] for i in index)
                for action, index in zip(actions, indices, strict=True)}
    calls: list[str] = []

    def retrieve(action):
        calls.append(action)
        return rows[action]

    snapshot = RetrievalSnapshot.capture(actions, retrieve)

    def evaluator(candidates):
        # Explicit diagnostic sensitivity backend: frozen scores, top-2 selection
        # rerun per coalition.  This is not the paper's private pr_filter backend.
        selected = sorted(candidates, key=lambda c: (-c.rank_score, c.key))[:2]
        return sum(c.value for c in selected)

    exact = CachedCoalitionEvaluator(snapshot, evaluator)
    values = exact.exact_values()
    credits = credit_rules(values)
    sampled = CachedCoalitionEvaluator(snapshot, evaluator)
    estimate = permutation_credit(sampled, permutations=128, seed=seed)
    group = np.stack([credits["shapley"], credits["singleton"], credits["loo"]])
    base = np.array([-0.5, 0.0, 0.5])
    shaped = shape_advantages(group, base)
    spans = np.tile(np.r_[-1, np.arange(len(actions)), -1], (3, 1))
    tokens = token_advantages(shaped["advantages"], base, spans)
    metrics = {"shapley_efficiency_error": float(abs(credits["shapley"].sum() - values[-1])),
               "zero_sum_error": float(abs(shaped["offsets"].sum(axis=1)).max()),
               "action_mean_error": float(abs(shaped["advantages"].mean(axis=1) - base).max()),
               "shared_token_error": float(abs(tokens[:, 0] - base).max()),
               "permutation_credit_l2_error": float(np.linalg.norm(estimate - credits["shapley"])),
               "retrieval_calls": len(calls), "exact_evaluator_calls": exact.calls,
               "permutation_evaluator_calls": sampled.calls}
    return {"seed": seed, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "promotion_eligible": False, "full_paper_reproduction": False,
            "full_experiment_status": "not_reproduced_high_cost",
            "dataset": {"id": source, "revision": snapshot.sha256},
            "backend": "frozen-top2-rerun component diagnostic; not private pr_filter",
            "snapshot_sha256": snapshot.sha256, "coalition_values": values.tolist(),
            "credits": {key: value.tolist() for key, value in credits.items()},
            "action_advantages": shaped["advantages"].tolist(),
            "group_std": shaped["group_std"], "metrics": metrics,
            "limitations": ["No learned retrieval policy, auction replay, production labels or online A/B.",
                            "Only the snapshot/credit/advantage component is executed.",
                            "Negative marginals and negative results are retained."]}


def render(result: dict) -> str:
    lines = ["# CASI 快照信用组件", "", "L1 机制诊断；不是私有拍卖或生产效果复现。", "",
             "完整高成本实验：不复现（审查 DONE）。", "", "| 指标 | 实测值 |", "| --- | ---: |"]
    lines.extend(f"| {key} | {value} |" for key, value in result["metrics"].items())
    return "\n".join(lines) + "\n"
