"""C2-Routing Eq.2--7 risk/utility kernel, NOT a trained visual router."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

import numpy as np

REQUIRES_GPU_VALIDATION = False
REDUCED_ACTIONS = frozenset({"R", "C256", "C512"})


def reduction_risk(probabilities: np.ndarray) -> float:
    """Joint-state order is (11,H,B,00); risk is P(H)-P(B), not error rate."""
    p = np.asarray(probabilities, dtype=float)
    if (p.shape != (4,) or not np.isfinite(p).all() or (p < 0).any()
            or not np.isclose(p.sum(), 1)):
        raise ValueError("four calibrated joint-correctness probabilities required")
    return float(p[1] - p[2])


def validation_cost_ratio(reduced: np.ndarray, original: np.ndarray,
                          dataset_ids: list[str], *, split: str) -> float:
    """Eq.5: equal-dataset average of FLOP-sum ratios, never per-example mean."""
    reduced, original = np.asarray(reduced, dtype=float), np.asarray(original, dtype=float)
    if (split != "validation" or reduced.ndim != 1 or not len(reduced)
            or reduced.shape != original.shape or len(dataset_ids) != len(reduced)
            or any(not isinstance(x, str) or not x for x in dataset_ids)
            or not np.isfinite(reduced).all() or not np.isfinite(original).all()
            or (reduced <= 0).any() or (original <= 0).any()):
        raise ValueError("aligned positive validation FLOPs and dataset identities required")
    ids = np.asarray(dataset_ids)
    return float(np.mean([reduced[ids == group].sum() / original[ids == group].sum()
                          for group in sorted(set(dataset_ids))]))


@dataclass(frozen=True)
class SafetyPolicy:
    """Validation-frozen ratios; an external calibrated risk head supplies p."""
    tradeoff: float
    cost_ratios: Mapping[str, float]
    fitted_split: str = "validation"

    def __post_init__(self):
        if (self.fitted_split != "validation" or not np.isfinite(self.tradeoff)
                or self.tradeoff < 0 or set(self.cost_ratios) != REDUCED_ACTIONS
                or any(not np.isfinite(v) or v <= 0 for v in self.cost_ratios.values())):
            raise ValueError("validation-frozen finite nonnegative utility policy required")
        object.__setattr__(self, "cost_ratios", MappingProxyType(dict(self.cost_ratios)))

    def decide(self, proposed_action: str, joint_probabilities: np.ndarray) -> str:
        if proposed_action not in REDUCED_ACTIONS:
            raise ValueError("external proposal must be R, C256, or C512")
        risk = reduction_risk(joint_probabilities)
        return (proposed_action if risk <= self.tradeoff * (1 - self.cost_ratios[proposed_action])
                else "F")


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("this CPU policy kernel does not implement a CUDA VLM/router")
    rng = np.random.default_rng(seed)
    original = rng.uniform(1, 2, 6)
    reduced = original * np.array([.2, .2, .2, .2, .2, .8])
    ratio = validation_cost_ratio(reduced, original, ["large"] * 5 + ["small"], split="validation")
    policy = SafetyPolicy(.1, {"R": ratio, "C256": .25, "C512": .5})
    p = np.array([.2, .15, .1, .55])
    risk = reduction_risk(p)
    original_accuracy, reduced_accuracy = p[0] + p[1], p[0] + p[2]
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"joint_expected_accuracy_loss": risk,
                        "dataset_macro_cost_ratio": ratio,
                        "shared_failure_probability": float(p[3])},
            "checks": {"risk_equals_expected_correctness_difference": np.isclose(
                risk, original_accuracy - reduced_accuracy).item(),
                "benefit_is_credited": policy.decide("C512", np.array([.1, .1, .7, .1])) == "C512",
                "shared_failure_is_not_correctable_harm": policy.decide(
                    "C512", np.array([.1, 0, 0, .9])) == "C512",
                "harm_triggers_original_fallback": policy.decide(
                    "C512", np.array([.1, .7, .1, .1])) == "F",
                "dataset_macro_not_sample_micro": abs(ratio - .5) < 1e-12,
                "cost_and_risk_utility_identity": bool(abs((reduced_accuracy - .1 * .5)
                    - (original_accuracy - .1) - (-risk + .1 * (1 - .5))) < 1e-12)}}
