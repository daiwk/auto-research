"""Evaluator-only multi-correct choice allocation audit (arXiv:2610.29217).

No model, paid API or benchmark is loaded. Categorical choice shares are not
independent probabilities of correctness. Validation threshold fitting is kept
separate from test evaluation; an in-sample threshold curve is only an oracle
diagnostic, not evidence of calibrated deployment behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable


@dataclass(frozen=True, slots=True)
class PublicChoiceList:
    request_id: str
    question: str
    choices: tuple[str, ...]

    def __post_init__(self):
        if (type(self.request_id) is not str or not self.request_id or type(self.question) is not str
                or type(self.choices) is not tuple or not self.choices):
            raise ValueError("identity and nonempty immutable choices required")
        if not all(isinstance(choice, str) for choice in self.choices):
            raise ValueError("choice descriptions must be public strings")


@dataclass(frozen=True, slots=True)
class EvaluatorRow:
    request_id: str
    probabilities: tuple[float, ...] | None
    correct: frozenset[int]
    choice_count: int
    rounding_decimals: int | None = None

    def __post_init__(self):
        if not self.request_id or type(self.choice_count) is not int or self.choice_count < 1:
            raise ValueError("identity and positive choice count required")
        if type(self.correct) is not frozenset or any(type(i) is not int or not 0 <= i < self.choice_count for i in self.correct):
            raise ValueError("evaluator labels must be a set of valid choice indices")
        if self.rounding_decimals is not None and (type(self.rounding_decimals) is not int or not 0 <= self.rounding_decimals <= 12):
            raise ValueError("explicit probability precision required")
        if self.probabilities is not None:
            p = self.probabilities
            tolerance = 1e-8 if self.rounding_decimals is None else self.choice_count * .5 * 10**-self.rounding_decimals + 1e-8
            if (type(p) is not tuple or len(p) != self.choice_count
                    or any(type(v) not in (float, int) or not math.isfinite(v) or not 0 <= v <= 1 for v in p)
                    or sum(p) <= 0 or abs(sum(p)-1) > tolerance):
                raise ValueError("aligned finite categorical shares required; no silent renormalization")


def collect_public_predictions(requests: tuple[PublicChoiceList, ...], predictor: Callable) -> dict:
    """Predictor receives only the public request, never evaluator labels."""
    if not requests or any(type(row) is not PublicChoiceList for row in requests):
        raise ValueError("only rebuilt public requests may reach the predictor")
    if len({row.request_id for row in requests}) != len(requests):
        raise ValueError("duplicate public request identity")
    return {row.request_id: predictor(row) for row in requests}


def _rows(rows):
    if not rows or any(not isinstance(row, EvaluatorRow) for row in rows):
        raise ValueError("nonempty evaluator rows required")
    if len({row.request_id for row in rows}) != len(rows):
        raise ValueError("duplicate evaluation identity")
    return tuple(rows)


def evaluate(rows: tuple[EvaluatorRow, ...], threshold: float) -> dict:
    rows = _rows(rows)
    if not isinstance(threshold, (int, float)) or not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("finite threshold in [0,1] required")
    exact = tp = fp = fn = refused = ranked = below_ranked = 0
    gaps, empty_confidences = [], []
    for row in rows:
        p, gold = row.probabilities, row.correct
        if p is None:
            refused += 1
            fn += len(gold)
            continue  # A refusal is NOT a successful empty-set prediction.
        selected = {i for i, value in enumerate(p) if value >= threshold}
        exact += selected == gold
        tp += len(selected & gold)
        fp += len(selected - gold)
        fn += len(gold - selected)
        if not gold:
            empty_confidences.append(max(p))
        if len(gold) > 1:
            gaps.append(max(p[i] for i in gold)-min(p[i] for i in gold))
            distractors = set(range(row.choice_count))-gold
            if distractors and min(p[i] for i in gold) > max(p[i] for i in distractors):
                ranked += 1
                below_ranked += any(p[i] < 1/row.choice_count for i in gold)
    precision = tp/(tp+fp) if tp+fp else 0.0
    recall = tp/(tp+fn) if tp+fn else 0.0
    return {"examples": len(rows), "refusals": refused, "exact_set_accuracy": exact/len(rows),
        "micro_precision": precision, "micro_recall": recall,
        "micro_f1": 2*precision*recall/(precision+recall) if precision+recall else 0.0,
        "multi_correct_scored": len(gaps), "correct_probability_gap_pp": 100*sum(gaps)/len(gaps) if gaps else None,
        "strictly_ranked_with_distractor": ranked,
        "below_uniform_given_strict_ranking": below_ranked/ranked if ranked else None,
        "no_correct_mean_max_probability": sum(empty_confidences)/len(empty_confidences) if empty_confidences else None}


@dataclass(frozen=True, slots=True)
class ThresholdRule:
    threshold: float
    validation_ids: frozenset[str]

    def __post_init__(self):
        if (type(self.threshold) not in (float, int) or not math.isfinite(self.threshold)
                or not 0 <= self.threshold <= 1 or type(self.validation_ids) is not frozenset
                or not self.validation_ids or any(type(i) is not str or not i for i in self.validation_ids)):
            raise ValueError("finite threshold and recorded nonempty validation identities required")


def fit_validation_threshold(rows: tuple[EvaluatorRow, ...]) -> ThresholdRule:
    rows = _rows(rows)
    # Paper's hundredth grid; lowest threshold wins ties deterministically.
    best = max(range(101), key=lambda i: evaluate(rows, i/100)["exact_set_accuracy"])
    return ThresholdRule(best/100, frozenset(row.request_id for row in rows))


def evaluate_test(rule: ThresholdRule, rows: tuple[EvaluatorRow, ...]) -> dict:
    rows = _rows(rows)
    if rule.validation_ids & {row.request_id for row in rows}:
        raise ValueError("validation/test identities overlap")
    return evaluate(rows, rule.threshold)


def identical_copy_gap(probabilities: tuple[tuple[float, ...], ...], *, rounding_decimals: int | None = None) -> float:
    """Mean highest-minus-lowest copy share, in percentage points."""
    if not probabilities:
        raise ValueError("five-copy response lists required")
    for i, p in enumerate(probabilities):
        if type(p) is not tuple:
            raise ValueError("five-copy probability tuples required")
        EvaluatorRow(str(i), p, frozenset(range(5)), 5, rounding_decimals)
    return 100*sum(max(p)-min(p) for p in probabilities)/len(probabilities)


def binary_ece(probabilities: tuple[float, ...], labels: tuple[bool, ...], *, exclude_first_bin=False) -> float:
    """Author convention: (a,b], first bin also includes zero; no rounding.

    Callers must explicitly reproduce an API's decimal rounding before passing
    probabilities. Excluding the first bin renormalizes over retained examples.
    """
    if (not probabilities or len(probabilities) != len(labels) or any(type(y) is not bool for y in labels)
            or any(not math.isfinite(p) or not 0 <= p <= 1 for p in probabilities)):
        raise ValueError("aligned binary labels and probabilities required")
    bins = [[] for _ in range(10)]
    for p, y in zip(probabilities, labels):
        index = next(i for i in range(10) if p <= (i+1)/10)
        bins[index].append((p, int(y)))
    kept = bins[1:] if exclude_first_bin else bins
    count = sum(len(items) for items in kept)
    return sum(abs(sum(p-y for p, y in items)) for items in kept)/count if count else 0.0


def diagnostic(seed: int = 42) -> dict:
    rows = (EvaluatorRow("validation", (.90, .05, .03, .02), frozenset({0, 1}), 4),)
    rule = fit_validation_threshold(rows)
    heldout = (EvaluatorRow("test", (.80, .10, .06, .04), frozenset({0, 1}), 4),)
    m = evaluate_test(rule, heldout)
    stats = evaluate(rows, .25)
    rejected = False
    try:
        evaluate_test(rule, rows)
    except ValueError:
        rejected = True
    seen = []
    collect_public_predictions((PublicChoiceList("public", "synthetic", ("a", "b")),),
                               lambda row: seen.append(set(row.__dataclass_fields__)) or (.5, .5))
    refusal = evaluate((EvaluatorRow("none", None, frozenset(), 2),), .25)
    checks = {"ranking_not_set_recovery": stats["strictly_ranked_with_distractor"] == 1 and stats["exact_set_accuracy"] == 0,
        "low_mass_correct_choice_counted": stats["below_uniform_given_strict_ranking"] == 1,
        "test_does_not_refit_threshold": rule.threshold == .04 and m["exact_set_accuracy"] == 0,
        "validation_test_overlap_rejected": rejected,
        "refusal_not_empty_set_success": refusal["refusals"] == 1 and refusal["exact_set_accuracy"] == 0,
        "public_predictor_has_no_gold": seen == [{"request_id", "question", "choices"}],
        "identical_copy_reference": abs(identical_copy_gap(((.6,.1,.1,.1,.1),))-50) < 1e-12,
        "ece_excluding_low_bin_renormalizes": abs(binary_ece((.05,.2,.8),(False,True,True),exclude_first_bin=True)-.5) < 1e-12}
    return {"seed": seed, "checks": checks, "metrics": {"scorer_contract_cases": len(checks),
        "validation_overlap_rejections": int(rejected), "model_calls": 0}}
