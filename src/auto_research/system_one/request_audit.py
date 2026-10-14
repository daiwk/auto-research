"""Paired retrieval request-independence protocol, not a new decision model."""
from __future__ import annotations

from dataclasses import dataclass, replace
import json
import math

import numpy as np


@dataclass(frozen=True)
class RetrievalRequest:
    query: str
    passages: tuple[tuple[str, str], ...]
    questions: tuple[tuple[str, str], ...]
    eligible: tuple[str, ...]


def intervention(request, kind, *, question=None, passage=None, candidate=None):
    """Independent interventions keep the two non-target channels byte-identical."""
    if kind == "request_expansion":
        if not question or question[0] in dict(request.questions):
            raise ValueError("a distinct additional question required")
        return replace(request, questions=request.questions + (question,))
    if kind == "evidence_addition":
        if not passage or passage[0] in dict(request.passages):
            raise ValueError("a distinct evidence passage required")
        return replace(request, passages=request.passages + (passage,))
    if kind == "candidate_expansion":
        if candidate not in dict(request.passages) or candidate in request.eligible:
            raise ValueError("candidate must already be displayed, but not eligible")
        return replace(request, eligible=request.eligible + (candidate,))
    raise ValueError("unknown intervention")


def compile_independent(request, target_key):
    """Gold-free compiler: other questions, routing keys and eligibility omitted."""
    question = dict(request.questions)[target_key]
    return json.dumps({"query": request.query, "passages": request.passages, "question": question},
                      ensure_ascii=False, separators=(",", ":"))


def allowed_label_distribution(vocabulary_logits, allowed_indices):
    logits = np.asarray(vocabulary_logits, dtype=float)
    raw_indices = np.asarray(allowed_indices)
    if not np.issubdtype(raw_indices.dtype, np.integer):
        raise ValueError("integer label indices required")
    indices = raw_indices.astype(int)
    if logits.ndim != 1 or not len(logits) or not np.isfinite(logits).all():
        raise ValueError("finite vocabulary logits required")
    if indices.ndim != 1 or not len(indices) or len(set(indices)) != len(indices) or (indices < 0).any() or (indices >= len(logits)).any():
        raise ValueError("distinct in-range allowed labels required")
    probabilities = np.exp(logits - logits.max())
    probabilities /= probabilities.sum()
    mass = float(probabilities[indices].sum())
    local = logits[indices]
    normalized = np.exp(local - local.max())
    normalized /= normalized.sum()
    return {"normalized_probability": normalized.tolist(), "allowed_label_mass": mass}


def retained_ab_preference(probabilities, first="A", second="B"):
    if first == second or first not in probabilities or second not in probabilities:
        raise ValueError("two retained distinct options required")
    a, b = _probabilities([probabilities[first], probabilities[second]])
    if a + b == 0:
        raise ValueError("retained labels have no probability support")
    return float(a / (a + b))


def _probabilities(values):
    p = np.asarray(values, dtype=float)
    if p.ndim != 1 or not len(p) or not np.isfinite(p).all() or (p < 0).any() or (p > 1).any():
        raise ValueError("nonempty finite probabilities in [0,1] required")
    return p


def select_action(scores, *, threshold=0.5, eligible=None):
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("fixed threshold in [0,1] required")
    labels = sorted(scores if eligible is None else eligible)
    if not labels or len(set(labels)) != len(labels) or any(k not in scores for k in labels):
        raise ValueError("nonempty unique eligible labels with scores required")
    values = _probabilities([scores[k] for k in labels])
    accepted = [(k, float(p)) for k, p in zip(labels, values) if p > threshold]
    return min(accepted, key=lambda x: (-x[1], x[0]))[0] if accepted else None


def binary_pair_metrics(before, after):
    before, after = _probabilities(before), _probabilities(after)
    if before.shape != after.shape:
        raise ValueError("paired arrays must align")
    ties = (before == 0.5) | (after == 0.5)
    return {"judgments": len(before), "strict_flip_rate": float(((before - .5) * (after - .5) < 0).mean()),
            "threshold_tie_rate": float(ties.mean()), "mean_absolute_movement": float(abs(after - before).mean())}


def audit_paired_predictions(rows, *, threshold=0.5, resamples=5000, seed=20260928):
    """Query-cluster bootstrap, equally weighted scenarios, separate years.

    Each row is one paired state with keys year/query_id/scenario, before/after
    probability dictionaries, and scorer-only positive passage labels. Targets
    stay identical; added evidence is not automatically eligible for selection.
    """
    rows = tuple(rows)
    if not rows or resamples < 1:
        raise ValueError("nonempty paired rows and positive bootstrap budget required")
    seen = set()
    grouped = {}
    for row in rows:
        key = (str(row["year"]), str(row["query_id"]), str(row["scenario"]))
        if key in seen:
            raise ValueError("duplicate paired state")
        seen.add(key)
        before, after = row["before"], row["after"]
        if set(before) != set(after) or not set(row["positive_labels"]) <= set(before):
            raise ValueError("fixed target labels and scorer-only gold labels required")
        metric = binary_pair_metrics([before[k] for k in sorted(before)], [after[k] for k in sorted(before)])
        a, b = select_action(before, threshold=threshold), select_action(after, threshold=threshold)
        positives = set(row["positive_labels"])
        correct_a = a in positives if positives else a is None
        correct_b = b in positives if positives else b is None
        metric.update(action_change=float(a != b), correct_action_delta=float(correct_b) - float(correct_a))
        labels = sorted(before)
        gold = np.asarray([label in positives for label in labels])
        before_correct = (_probabilities([before[k] for k in labels]) > threshold) == gold
        after_correct = (_probabilities([after[k] for k in labels]) > threshold) == gold
        metric["binary_accuracy_delta"] = float(after_correct.mean() - before_correct.mean())
        grouped.setdefault(key[0], {}).setdefault(key[1], []).append((key[2], metric))
    rng = np.random.default_rng(seed)
    output = {}
    for year, queries in sorted(grouped.items()):
        scenario_sets = {tuple(sorted(s for s, _ in records)) for records in queries.values()}
        if len(scenario_sets) != 1:
            raise ValueError("every query must cover the same fixed scenarios; do not silently reweight")
        names = list(next(iter(queries.values()))[0][1])
        matrix = np.asarray([[np.mean([m[name] for _, m in records]) for name in names]
                             for _, records in sorted(queries.items())])
        samples = matrix[rng.integers(0, len(matrix), size=(resamples, len(matrix)))].mean(1)
        summary = {}
        for i, name in enumerate(names):
            value = float(matrix[:, i].mean())
            no_events = bool(name in {"strict_flip_rate", "action_change"} and np.all(matrix[:, i] == 0))
            summary[name] = {"mean": value, "ci95": None if no_events else np.quantile(samples[:, i], [.025, .975]).tolist(),
                             "zero_observed_events": no_events}
            if no_events:
                summary[name]["query_event_upper_bound_95"] = 1 - 0.05 ** (1 / len(matrix))
        output[year] = {"queries": len(queries), "states": sum(map(len, queries.values())), "metrics": summary}
    return {"schema_version": 2, "paper": "2610.14631", "evaluation_tier": "paired_prediction_protocol",
            "model_inference_performed": False, "threshold": threshold, "bootstrap_seed": seed,
            "bootstrap_resamples": resamples, "years": output}
