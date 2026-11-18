"""Marginal and temporal diagnostics for completed LLM samples (2604.06543).

Requires the optional research-components SciPy dependency. A large p-value is
non-rejection, never proof of randomness/independence. No model sampler is faked.
"""
from __future__ import annotations

import numpy as np

REQUIRES_GPU_VALIDATION = False


def evaluate_discrete_uniform(samples: list[int], labels: list[int], *, expected_count: int = 1024) -> dict[str, float]:
    from scipy.stats import chisquare
    if expected_count < 2 or len(samples) != expected_count or len(labels) < 2 or len(set(labels)) != len(labels) or any(isinstance(x, bool) or not isinstance(x, int) for x in samples + labels):
        raise ValueError("exact integer sample count and distinct integer labels required")
    lookup = {x: i for i, x in enumerate(labels)}
    if any(x not in lookup for x in samples):
        raise ValueError("out-of-support sample; do not silently drop it")
    codes = np.array([lookup[x] for x in samples]); counts = np.bincount(codes, minlength=len(labels))
    result = chisquare(counts)
    # Matching-symbol lag1 excess does not depend on arbitrary numeric labels.
    repeat = float(np.mean(codes[:-1] == codes[1:]))
    transitions = np.zeros((len(labels), len(labels)), dtype=int)
    np.add.at(transitions, (codes[:-1], codes[1:]), 1)
    concentration = float(transitions.max() / (len(codes) - 1))
    return {"chi_square": float(result.statistic), "marginal_p_value": float(result.pvalue), "lag1_repeat_rate": repeat,
            "uniform_independent_repeat_reference": 1 / len(labels), "max_transition_fraction": concentration, "samples": len(samples)}


def evaluate_continuous(samples: list[float], *, distribution: str, expected_count: int = 1024) -> dict[str, float]:
    from scipy.stats import kstest
    x = np.asarray(samples, dtype=float)
    if x.ndim != 1 or len(x) != expected_count or len(x) < 3 or not np.isfinite(x).all() or distribution not in {"uniform", "normal"}:
        raise ValueError("fixed-count finite samples and standard uniform/normal required")
    if distribution == "uniform" and np.any((x < 0) | (x > 1)):
        raise ValueError("uniform support is [0,1]")
    result = kstest(x, "uniform" if distribution == "uniform" else "norm")
    centered = x - x.mean(); denominator = float(centered @ centered)
    if denominator == 0:
        raise ValueError("autocorrelation undefined for a constant sequence")
    return {"ks_statistic": float(result.statistic), "marginal_p_value": float(result.pvalue),
            "lag1_autocorrelation": float(centered[:-1] @ centered[1:] / denominator), "samples": len(x)}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU statistical evaluator only")
    rng = np.random.default_rng(seed)
    periodic = [i % 4 for i in range(1024)]
    marginal = evaluate_discrete_uniform(periodic, [0, 1, 2, 3])
    continuous = evaluate_continuous(rng.random(1024).tolist(), distribution="uniform")
    return {"seed": seed, "device": device, "metrics": {**marginal, "independent_fixture_ks": continuous["ks_statistic"]},
            "checks": {"uniform_histogram_can_be_deterministic": marginal["chi_square"] == 0 and marginal["max_transition_fraction"] > .24,
                       "temporal_repeat_exposes_cycle": marginal["lag1_repeat_rate"] == 0,
                       "reference_fixture_not_llm_output": True}, "diagnostic_only": True, "evaluation_tier": "l1_mechanism"}
