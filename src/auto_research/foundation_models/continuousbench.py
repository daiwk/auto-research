"""Fixed author-code Geminon evaluation protocol for ContinuousBench (2606.01849).

Reference: ContinuousBenchEval tree 0f8a521cfef8c3f500ece717b626ad7c9124dee4.
The released parser differs from the prose appendix: we bind this code protocol
explicitly and do NOT silently remove arbitrary measurement units. News LLM
judging, synthesis, DP training/accounting and inference are not implemented.
"""
from __future__ import annotations

import math
import re

UPSTREAM_REVISION = "0f8a521cfef8c3f500ece717b626ad7c9124dee4"
REQUIRES_GPU_VALIDATION = False


def score_geminon(question: str, raw_prediction: str, ground_truth: str) -> dict[str, bool | str]:
    if any(not isinstance(x, str) for x in [question, raw_prediction, ground_truth]) or not ground_truth.strip():
        raise ValueError("question, raw prediction and nonempty gold string required")
    boundary = re.search(r"[\s.][Qq]:", raw_prediction)
    content = raw_prediction[:boundary.start()] if boundary else raw_prediction
    lines = [s.strip() for s in content.splitlines() if s.strip()]
    clean = lines[0] if lines else ""
    if clean.endswith(".") and not clean.endswith(".."):
        clean = clean[:-1].rstrip()
    p, g = clean.lower().strip().strip("."), ground_truth.lower().strip().strip(".")
    components = [t.strip() for t in g.split("and") if t.strip()] if "types of" in question.lower() else [g]
    return {"exact_match": p == g, "contains_match": bool(components) and all(t in p for t in components), "normalized_prediction": p}


def select_validation_checkpoint(records: list[dict]) -> str:
    """Only validation contains accuracy selects a checkpoint; no test lookup."""
    if not records or len({r.get("checkpoint") for r in records}) != len(records):
        raise ValueError("unique nonempty validation checkpoint records required")
    for record in records:
        value = record.get("contains_accuracy")
        if record.get("split") != "validation" or not isinstance(record.get("checkpoint"), str) or not record["checkpoint"] or not isinstance(value, (float, int)) or isinstance(value, bool) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("selection requires validation-only finite accuracy")
    # Stable input order breaks equal-score ties, documented local convention.
    return max(records, key=lambda r: r["contains_accuracy"])["checkpoint"]


def capability_gain(base: list[dict], adapted: list[dict], *, release_revision: str) -> dict[str, float | str]:
    """Paired held-out exact match on the same fixed public release, absolute gain.

    An unchanged-base/no-corpus arm must be supplied, not assumed zero. Inputs
    are completed predictions; this evaluator never provides gold to generation.
    """
    if not release_revision or not base or len(base) != len(adapted):
        raise ValueError("paired nonempty fixed-release evaluations required")
    scores = []
    id_sets = []
    for records in [base, adapted]:
        ids = [r.get("id") for r in records]
        if len(set(ids)) != len(ids) or any(not isinstance(i, str) or not i for i in ids):
            raise ValueError("unique question IDs required")
        id_sets.append(set(ids))
        mapping = {}
        for r in records:
            if r.get("split") != "test" or r.get("release_revision") != release_revision:
                raise ValueError("test-only records must match the bound release")
            mapping[r["id"]] = (r["question"], r["ground_truth"], bool(score_geminon(r["question"], r["raw_prediction"], r["ground_truth"])["exact_match"]))
        scores.append(mapping)
    if id_sets[0] != id_sets[1] or any(scores[0][i][:2] != scores[1][i][:2] for i in id_sets[0]):
        raise ValueError("base/adapted must evaluate the identical questions and references")
    base_em = sum(x[2] for x in scores[0].values()) / len(base)
    adapted_em = sum(x[2] for x in scores[1].values()) / len(adapted)
    return {"base_exact_match": base_em, "adapted_exact_match": adapted_em,
            "absolute_capability_gain": adapted_em - base_em, "examples": len(base),
            "release_revision": release_revision, "evaluation_protocol_revision": UPSTREAM_REVISION}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU evaluator only")
    revision = "explicit-diagnostic-fixture-not-public-benchmark"
    def row(pred):
        return {"id": "q1", "question": "What are the types of X?", "ground_truth": "Normal and Flying", "raw_prediction": pred, "split": "test", "release_revision": revision}
    result = capability_gain([row("Normal")], [row("Normal and Flying. Q: next")], release_revision=revision)
    selected = select_validation_checkpoint([{"checkpoint": "a", "split": "validation", "contains_accuracy": .5}, {"checkpoint": "b", "split": "validation", "contains_accuracy": .75}])
    return {"seed": seed, "device": device, "metrics": {k: v for k, v in result.items() if isinstance(v, (int, float))},
            "checks": {"reference_baseline_is_not_assumed_zero": result["absolute_capability_gain"] == 1,
                       "validation_selects_checkpoint": selected == "b",
                       "types_contains_is_not_exact_match": not score_geminon("types of X", "Flying and Normal", "Normal and Flying")["exact_match"] and bool(score_geminon("types of X", "Flying and Normal", "Normal and Flying")["contains_match"]),
                       "fixture_not_benchmark_capability": True}, "diagnostic_only": True, "evaluation_tier": "l1_mechanism"}
