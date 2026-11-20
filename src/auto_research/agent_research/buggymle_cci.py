"""Fixed-calibration CCI projection, arXiv:2611.25088v1 §3.1, Eq.1--5.

L0 arithmetic interface, not a repository analyzer or trained difficulty model.
Callers must supply an independently fitted reference calibration; the paper does
not publish all feature/group scales. Synthetic diagnostic calibration is never
advertised as the eight-benchmark fit. No oracle patch or test label is read.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import math
from statistics import median

REQUIRES_GPU_VALIDATION = False
GROUPS = {
    "repo": ("lines_of_code", "file_count", "max_dir_depth"),
    "dep": ("dependency_count", "max_dep_chain"),
    "patch": ("files_changed", "hunks", "lines_added", "lines_removed", "total_lines_delta"),
}
FEATURES = tuple(name for group in GROUPS.values() for name in group)


def _finite(value: float) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)


def validate_features(features: Mapping[str, float]) -> dict[str, float]:
    if set(features) != set(FEATURES):
        raise ValueError("exactly the ten published structural features are required")
    for name, value in features.items():
        if not _finite(value) or value <= -1 or (name != "total_lines_delta" and value < 0):
            raise ValueError("count features must be nonnegative; net delta must permit log1p")
    return dict(features)


def benchmark_medians(tasks: Sequence[Mapping[str, float]]) -> dict[str, float]:
    if not tasks:
        raise ValueError("nonempty task-level structural measurements required")
    rows = [validate_features(row) for row in tasks]
    return {name: median(row[name] for row in rows) for name in FEATURES}


@dataclass(frozen=True)
class Calibration:
    reference_id: str
    feature_means: tuple[float, ...]
    feature_stds: tuple[float, ...]
    group_stds: tuple[float, ...]
    coefficients: tuple[float, ...]
    raw_min: float
    raw_max: float
    intercept: float | None = None

    def __post_init__(self):
        if not isinstance(self.reference_id, str) or not self.reference_id.strip():
            raise ValueError("named immutable reference calibration required")
        for values, size in [(self.feature_means, 10), (self.feature_stds, 10),
                             (self.group_stds, 3), (self.coefficients, 3)]:
            if len(values) != size or not all(_finite(v) for v in values):
                raise ValueError("finite, complete calibration vectors required")
        if any(v <= 0 for v in self.feature_stds + self.group_stds):
            raise ValueError("strictly positive feature and group scales required")
        if not _finite(self.raw_min) or not _finite(self.raw_max) or self.raw_min >= self.raw_max:
            raise ValueError("nondegenerate fixed reference min/max required")
        if self.intercept is not None and not _finite(self.intercept):
            raise ValueError("finite optional solve-rate intercept required")


def project(features: Mapping[str, float], calibration: Calibration) -> dict:
    """Project without fitting, clipping or centering the group means again."""
    values = validate_features(features)
    if not isinstance(calibration, Calibration):
        raise TypeError("explicit reference Calibration required")
    z = {name: (math.log1p(values[name]) - mu) / sigma
         for name, mu, sigma in zip(FEATURES, calibration.feature_means,
                                    calibration.feature_stds, strict=True)}
    scores = {group: sum(z[name] for name in names) / len(names) / scale
              for (group, names), scale in zip(GROUPS.items(), calibration.group_stds, strict=True)}
    linear = sum(beta * score for beta, score in
                 zip(calibration.coefficients, scores.values(), strict=True))
    raw = -linear
    scaled = (raw - calibration.raw_min) / (calibration.raw_max - calibration.raw_min)
    if not all(math.isfinite(v) for v in (*z.values(), *scores.values(), raw, scaled)):
        raise ValueError("calibration produces nonfinite projection")
    predicted = None
    if calibration.intercept is not None:
        eta = calibration.intercept + linear
        if not math.isfinite(eta):
            raise ValueError("nonfinite solve-rate logit")
        predicted = 1 / (1 + math.exp(-eta)) if eta >= 0 else math.exp(eta) / (1 + math.exp(eta))
    return {"reference_id": calibration.reference_id, "group_scores": scores,
            "raw_cci": raw, "scaled_cci": scaled, "predicted_solve_rate": predicted}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    c = Calibration("synthetic-arithmetic-control-not-paper-fit", (0.,)*10, (1.,)*10,
                    (1.,)*3, (.64, -.34, -.99), -2., 2.)
    base = {name: 0. for name in FEATURES}
    large_patch = base | {name: 100. for name in GROUPS["patch"]}
    large_repo = base | {name: 100. for name in GROUPS["repo"]}
    a, b, r = project(base, c), project(large_patch, c), project(large_repo, c)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
            "checks": {"patch_sign_preserved": b["raw_cci"] > a["raw_cci"],
                       "positive_repo_conditional_coefficient_preserved": r["raw_cci"] < a["raw_cci"],
                       "out_of_reference_range_not_clipped": b["scaled_cci"] > 1,
                       "unfitted_intercept_not_invented": a["predicted_solve_rate"] is None,
                       "task_medians_not_means": benchmark_medians([base, base, large_patch]) == base},
            "metrics": {"controlled_patch_raw_cci": b["raw_cci"],
                        "controlled_patch_scaled_cci": b["scaled_cci"]}}
