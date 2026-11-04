"""Continual AutoResearch post-run metrics, not an autonomous research agent.

https://arxiv.org/html/2611.05108v1 §3.3, equations 1–3. Hidden-test scores
are accepted only in closed-run evaluator records, never returned to an actor.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False


def _finite(value, minimum=None, maximum=None):
    if (type(value) not in (int, float) or not math.isfinite(value)
            or (minimum is not None and value < minimum) or (maximum is not None and value > maximum)):
        raise ValueError("finite value in range required")
    return float(value)


def normalized_reward(value, metric: str, *, training_sd=1.0):
    value = _finite(value)
    if metric in {"accuracy", "f1"}:
        return _finite(value, 0, 1)
    if metric == "rmse":
        sd = _finite(training_sd)
        if sd <= 0 or value < 0:
            raise ValueError("nonnegative RMSE and positive training-only SD required")
        return 1.0 / (1.0 + value / sd)
    if metric == "r2":
        return 1.0 / (2.0 - min(value, 1.0))
    raise ValueError("unsupported paper metric")


@dataclass(frozen=True)
class Attempt:
    candidate_id: str
    completed_at: float
    hidden_metric: float | None
    valid: bool = True


@dataclass(frozen=True)
class ClosedRun:
    task_id: str
    budget: float
    metric: str
    attempts: tuple[Attempt, ...]
    selected_id: str | None
    closed: bool
    training_sd: float = 1.0

    def __post_init__(self):
        if self.closed is not True or not isinstance(self.task_id, str) or not self.task_id:
            raise ValueError("only closed evaluator runs with named tasks are accepted")
        if _finite(self.budget) <= 0:
            raise ValueError("positive task budget required")
        normalized_reward(0, self.metric, training_sd=self.training_sd)
        rows = tuple(self.attempts)
        previous, ids, valid_ids = 0.0, set(), set()
        for row in rows:
            if (not isinstance(row, Attempt) or not isinstance(row.candidate_id, str) or not row.candidate_id
                    or row.candidate_id in ids or type(row.valid) is not bool):
                raise ValueError("distinct typed candidate records required")
            time = _finite(row.completed_at, 0, self.budget)
            if time < previous:
                raise ValueError("candidate times must remain chronological")
            if row.valid:
                normalized_reward(row.hidden_metric, self.metric, training_sd=self.training_sd)
                valid_ids.add(row.candidate_id)
            elif row.hidden_metric is not None:
                raise ValueError("invalid submissions cannot supply a hidden reward")
            previous = time
            ids.add(row.candidate_id)
        if (valid_ids and self.selected_id not in valid_ids) or (not valid_ids and self.selected_id is not None):
            raise ValueError("final selection must name an actually valid submission")
        object.__setattr__(self, "attempts", rows)


def score_run(run: ClosedRun):
    if not isinstance(run, ClosedRun) or run.closed is not True:
        raise ValueError("closed evaluator record required")
    best, previous, first, selected = 0.0, 0.0, None, 0.0
    areas = []
    for row in run.attempts:
        areas.append((row.completed_at - previous) * best)
        previous = row.completed_at
        if not row.valid:
            continue
        reward = normalized_reward(row.hidden_metric, run.metric, training_sd=run.training_sd)
        if first is None:
            first = reward
        best = max(best, reward)
        if row.candidate_id == run.selected_id:
            selected = reward
    areas.append((run.budget - previous) * best)
    return {"initialization": first if first is not None else 0.0, "outcome": selected,
            "search_utility": math.fsum(areas) / run.budget, "selection_regret": best - selected}


def paired_stream(stateful: tuple[ClosedRun, ...], reset: tuple[ClosedRun, ...]):
    """Task 1 has no previous experience: exclude it from transfer statistics."""
    if len(stateful) != len(reset) or len(stateful) < 2:
        raise ValueError("matched stream with at least two tasks required")
    ids = [run.task_id for run in stateful]
    if len(set(ids)) != len(ids):
        raise ValueError("distinct ordered tasks required")
    differences = []
    for left, right in zip(stateful, reset):
        if (left.task_id, left.budget, left.metric, left.training_sd) != (right.task_id, right.budget, right.metric, right.training_sd):
            raise ValueError("match task, budget, metric and training normalization")
        a, b = score_run(left), score_run(right)
        differences.append({key: 100 * (a[key] - b[key]) for key in a})
    keys = differences[0].keys()
    return {key: math.fsum(row[key] for row in differences[1:]) / (len(differences) - 1) for key in keys}


def family_balanced(stream_gains):
    """Mean within each stream first, then equal-weight the streams."""
    rows = tuple(stream_gains)
    if not rows or any(set(row) != set(rows[0]) for row in rows):
        raise ValueError("consistent stream summaries required")
    return {key: math.fsum(_finite(row[key]) for row in rows) / len(rows) for key in rows[0]}


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU only")
    run = ClosedRun(f"task-{seed}", 10, "accuracy", (Attempt("early", 2, .8), Attempt("late", 6, .5)), "late", True)
    result = score_run(run)
    bad = False
    try:
        ClosedRun("live", 10, "accuracy", (), None, False)
    except ValueError:
        bad = True
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism", "metrics": result,
            "checks": {"best_curve_not_last_candidate": math.isclose(result["search_utility"], .64),
                       "selected_not_oracle_best": result["outcome"] == .5,
                       "selection_regret_preserved": math.isclose(result["selection_regret"], .3),
                       "live_feedback_rejected": bad, "negative_r2_supported": normalized_reward(-2, "r2") == .25}}
