"""Counterbalanced behavioral protocol from arXiv:2609.30716v1.

Only the AD-series four-cell contrasts and evaluator-side statistics are
implemented. This module never loads a language model, executes author code,
or implements the separate J-Lens / activation-patching toolkit.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
import warnings

import numpy as np


UPSTREAM_REVISION = "fc468f2374540870042b20db1ec7e836ed205db7"
CONDITIONS = ("T1", "T1c", "T2", "T2c", "T3", "T3c", "T4", "T4c", "T5", "T5b")
EFFECTS = ("token", "role", "order_null", "serial")
_HADAMARD = np.array([[1, 1, 1, 1], [1, 1, -1, -1],
                      [1, -1, 1, -1], [1, -1, -1, 1]], dtype=float)


def four_cell_effects(cells: Sequence[Sequence[float]]) -> np.ndarray:
    """Rows are e1..e4 = log P(B)-log P(A); output is HALF-effects.

    e1/e2 use stale=A,recent=B with stale/recent printed first, respectively;
    e3/e4 reverse the word roles with the same two block orders. Negative
    serial means primacy. The third column is a null control, not position.
    """
    raw = np.asarray(cells)
    if raw.dtype.kind not in "iuf" or raw.ndim != 2 or raw.shape[1] != 4:
        raise ValueError("cells must be a nonempty numeric (items, 4) matrix")
    raw = raw.astype(float)
    if len(raw) == 0 or not np.isfinite(raw).all():
        raise ValueError("cells must be nonempty and finite")
    return raw @ _HADAMARD.T / 4


def _vector(values: Sequence[float]) -> np.ndarray:
    x = np.asarray(values)
    if x.dtype.kind not in "iuf" or x.ndim != 1 or len(x) < 3:
        raise ValueError("statistics require at least three numeric items")
    x = x.astype(float)
    if not np.isfinite(x).all():
        raise ValueError("statistics require finite items")
    return x


def bca_interval(values: Sequence[float], *, seed: int = 42,
                 resamples: int = 9999, confidence: float = 0.95) -> dict:
    """BCa only: failures are visible, never silently changed to percentile CIs."""
    x = _vector(values)
    if (isinstance(resamples, bool) or not isinstance(resamples, int) or resamples < 2
            or not 0 < confidence < 1):
        raise ValueError("resamples >= 2 and confidence in (0, 1) required")
    if np.ptp(x) == 0:
        return {"status": "degenerate", "low": None, "high": None,
                "reason": "zero item variance; BCa inference not identifiable"}
    from scipy import stats

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            warnings.simplefilter("error", stats.DegenerateDataWarning)
            result = stats.bootstrap((x,), np.mean, method="BCa", random_state=seed,
                                     n_resamples=resamples, confidence_level=confidence)
        low, high = float(result.confidence_interval.low), float(result.confidence_interval.high)
        if not np.isfinite([low, high]).all() or low > high:
            raise ValueError("nonfinite or reversed BCa interval")
    except (ValueError, RuntimeError, RuntimeWarning, FloatingPointError) as error:
        return {"status": "failed", "low": None, "high": None,
                "reason": type(error).__name__}
    return {"status": "ok", "low": low, "high": high}


def tost(values: Sequence[float], *, bound: float = 0.15, seed: int = 42,
         resamples: int = 9999) -> dict:
    """Author's paired-item TOST plus BCa90 criterion; no pass on failed inference."""
    x = _vector(values)
    if not np.isfinite(bound) or bound <= 0:
        raise ValueError("positive finite equivalence bound required")
    interval = bca_interval(x, seed=seed, resamples=resamples, confidence=0.90)
    if interval["status"] != "ok":
        return {"status": interval["status"], "p_value": None, "equivalent": None,
                "ci90": interval, "bound": float(bound)}
    from scipy import stats

    mean = float(x.mean())
    se = float(x.std(ddof=1) / np.sqrt(len(x)))
    p_value = float(max(stats.t.sf((mean + bound) / se, df=len(x)-1),
                        stats.t.cdf((mean - bound) / se, df=len(x)-1)))
    equivalent = (p_value < 0.05 and -bound <= interval["low"]
                  and interval["high"] <= bound)
    return {"status": "ok", "p_value": p_value, "equivalent": bool(equivalent),
            "ci90": interval, "bound": float(bound)}


def _summary(values: np.ndarray, *, seed: int, resamples: int) -> dict:
    return {"mean": float(values.mean()), "n": len(values),
            "sd": float(values.std(ddof=1)),
            "ci95": bca_interval(values, seed=seed, resamples=resamples)}


def _contrast_vectors(e: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    serial = {key: value[:, 3] for key, value in e.items()}
    role = {key: value[:, 1] for key, value in e.items()}
    a1, a2 = serial["T1c"]-serial["T1"], serial["T3c"]-serial["T3"]
    c1, c2 = serial["T4c"]-serial["T2c"], serial["T3c"]-serial["T1c"]
    c4 = serial["T3"]-serial["T1"]
    return {"A1": a1, "A2": a2, "A3": (a1+a2)/2, "A4": a1-a2,
            "B1": serial["T2"]-serial["T1"], "B2": serial["T2c"]-serial["T2"],
            "B3": serial["T2c"]-serial["T1"], "B4": serial["T2c"]-serial["T1c"],
            "C1": c1, "C2": c2, "C3": c1-c2, "C4": c4, "C5": c1-c4,
            "C6": serial["T4"]-serial["T2"],
            "D1": abs(role["T5b"])-abs(serial["T5b"]),
            "D2": abs(role["T5"])-abs(serial["T5"]), "D3": role["T5b"]-role["T5"],
            "E1": serial["T5b"]-serial["T4c"], "E2": serial["T5"]-serial["T4"]}


def analyze_cells(conditions: Mapping[str, Sequence[Sequence[float]]],
                  item_ids: Sequence[str], *, seed: int = 42, resamples: int = 9999) -> dict:
    """Analyze external fixed predictions; item order must match in ALL conditions.

    Filters are the paper's analysis rule, not validation tuning or evidence of
    model improvement. Sensitivity includes every item regardless of filtering.
    """
    if not isinstance(conditions, Mapping) or set(conditions) != set(CONDITIONS):
        raise ValueError("all ten AD conditions are required exactly once")
    if (len(item_ids) < 4 or not all(isinstance(x, str) and x for x in item_ids)
            or len(set(item_ids)) != len(item_ids)):
        raise ValueError("at least four unique nonempty item IDs required")
    effects = {key: four_cell_effects(conditions[key]) for key in CONDITIONS}
    if any(len(x) != len(item_ids) for x in effects.values()):
        raise ValueError("condition item counts must match the same fixed item order")
    flags = {key: np.flatnonzero((abs(x[:, 0]) > 2) | (abs(x[:, 2]) > 0.5)).tolist()
             for key, x in effects.items()}
    dropped = set(i for indices in flags.values() for i in indices)
    keep = [i for i in range(len(item_ids)) if i not in dropped]
    if len(keep) < 3:
        raise ValueError("global keep set has fewer than three items")

    def subset(indices: list[int]) -> dict:
        selected = {key: value[indices] for key, value in effects.items()}
        results = {}
        for key, values in selected.items():
            summaries = {name: _summary(values[:, i], seed=seed, resamples=resamples)
                         for i, name in enumerate(EFFECTS)}
            summaries["serial_tost"] = tost(values[:, 3], seed=seed, resamples=resamples)
            results[key] = summaries
        contrasts = {name: _summary(x, seed=seed, resamples=resamples)
                     for name, x in _contrast_vectors(selected).items()}
        return {"n": len(indices), "conditions": results, "contrasts": contrasts}

    return {"primary": subset(keep), "sensitivity": subset(list(range(len(item_ids)))),
            "items_kept": [item_ids[i] for i in keep],
            "items_dropped": [item_ids[i] for i in range(len(item_ids)) if i in dropped],
            "per_condition_flags": {key: [item_ids[i] for i in indices]
                                    for key, indices in flags.items()},
            "seed": seed, "resamples": resamples, "model_calls": 0,
            "effect_scale": "half_effect_nats", "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "upstream_revision": UPSTREAM_REVISION}


def diagnostic(seed: int = 42) -> dict:
    """Seeded algebra/filter contracts only, not Gemma inference or capability."""
    rng = np.random.default_rng(seed)
    known = rng.normal(size=(8, 4))/8
    raw = known @ _HADAMARD
    error = float(np.max(abs(four_cell_effects(raw)-known)))
    bad = known.copy()
    bad[0, 2] = 0.6
    matrices = {key: raw.copy() for key in CONDITIONS}
    matrices["T5b"] = bad @ _HADAMARD
    # A short report exercises failure-visible statistics and the shared mask.
    report = analyze_cells(matrices, [f"item-{i}" for i in range(8)],
                           seed=seed, resamples=199)
    degenerate = tost([0.0]*4, seed=seed, resamples=199)
    checks = {"orthogonal_contrast_recovery": error < 1e-12,
              "global_keep_set_shared": all(x["n"] == 7
                                           for condition in report["primary"]["conditions"].values()
                                           for x in condition.values() if "n" in x),
              "sensitivity_preserves_all_items": report["sensitivity"]["n"] == 8,
              "single_bad_condition_drops_globally": report["items_dropped"] == ["item-0"],
              "degenerate_tost_is_not_a_pass": degenerate["equivalent"] is None,
              "half_effect_orientation": np.allclose(four_cell_effects([[-1, 1, 1, -1]])[0],
                                                       [0, 0, 0, -1])}
    return {"seed": seed, "checks": {key: bool(value) for key, value in checks.items()},
            "metrics": {"contract_cases": float(len(checks)), "algebra_max_error": error,
                        "global_items_kept": float(report["primary"]["n"]), "model_calls": 0.0},
            "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "requires_gpu_validation": False,
            "full_experiment_status": "not_run_scope_limited_protocol",
            "upstream_revision": UPSTREAM_REVISION}
