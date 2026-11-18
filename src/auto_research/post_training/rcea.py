"""Finite-policy entropy accounting and local covariance from RCEA v1."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import exp, fsum, isclose, isfinite, log
from random import Random
from typing import Sequence

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Trajectory:
    """One distinct completion for one fixed prompt, with deterministic labels."""

    probability: float
    success: bool
    valid: bool | None = None
    mode: str | None = None


@dataclass(frozen=True)
class EntropyAllocation:
    """Eq. (7) terms in nats, already weighted by the relevant masses."""

    total: float
    outcome: float
    failed: float
    validity: float
    modes: float
    within_mode: float
    invalid_success: float
    effective_modes: float | None

    @property
    def reconstructed(self) -> float:
        return fsum((self.outcome, self.failed, self.validity, self.modes,
                     self.within_mode, self.invalid_success))


def _weighted_entropy(masses: Sequence[float]) -> float:
    total = fsum(masses)
    return -fsum(mass * (log(mass) - log(total)) for mass in masses if mass > 0)


def entropy_allocation(rows: Sequence[Trajectory]) -> EntropyAllocation:
    """Exact Eq. (3), (6)–(8) on enumerated support; not a rollout estimator."""
    if not rows or any(not isfinite(x.probability) or not 0 <= x.probability <= 1 for x in rows):
        raise ValueError("expected nonempty finite probabilities in [0, 1]")
    if not isclose(fsum(x.probability for x in rows), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("trajectory probabilities must sum to one")
    failure, invalid = [], []
    modes: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if type(row.success) is not bool:
            raise ValueError("success must be a Boolean verifier result")
        if not row.success:
            if row.valid is not None or row.mode is not None:
                raise ValueError("validity and mode are defined within verifier successes")
            failure.append(row.probability)
        elif row.valid is False and row.mode is None:
            invalid.append(row.probability)
        elif row.valid is True and isinstance(row.mode, str) and row.mode.strip():
            modes[row.mode].append(row.probability)
        else:
            raise ValueError("successful trajectories need validity and valid ones a mode")
    mode_masses = [fsum(masses) for masses in modes.values()]
    valid_mass, invalid_mass = fsum(mode_masses), fsum(invalid)
    mode_entropy = _weighted_entropy(mode_masses)
    return EntropyAllocation(
        total=_weighted_entropy([row.probability for row in rows]),
        outcome=_weighted_entropy([fsum(failure), fsum((valid_mass, invalid_mass))]),
        failed=_weighted_entropy(failure),
        validity=_weighted_entropy([valid_mass, invalid_mass]),
        modes=mode_entropy,
        within_mode=fsum(_weighted_entropy(masses) for masses in modes.values()),
        invalid_success=_weighted_entropy(invalid),
        effective_modes=exp(mode_entropy / valid_mass) if valid_mass else None,
    )


def _log_policy(logits: Sequence[float]) -> list[float]:
    if not logits or not all(map(isfinite, logits)):
        raise ValueError("expected nonempty finite logits")
    peak = max(logits)
    shifted = [x - peak for x in logits]
    if not all(map(isfinite, shifted)):
        raise ValueError("logit range overflows")
    normalizer = log(fsum(map(exp, shifted)))
    return [x - normalizer for x in shifted]


def local_entropy_change(
    logits: Sequence[float], logit_delta: Sequence[float],
) -> tuple[float, float]:
    """Eq. (10) first-order prediction and actual finite change, same prefix."""
    if len(logits) != len(logit_delta) or not all(map(isfinite, logit_delta)):
        raise ValueError("delta must be finite and match vocabulary")
    logp = _log_policy(logits)
    weights = list(map(exp, logp))
    mean_logp = fsum(p * value for p, value in zip(weights, logp, strict=True))
    center = logit_delta[0]
    predicted = -fsum(
        p * (value - mean_logp) * (delta - center)
        for p, value, delta in zip(weights, logp, logit_delta, strict=True)
    )
    updated_logp = _log_policy([a + b for a, b in zip(logits, logit_delta, strict=True)])
    actual = -fsum(exp(x) * x for x in updated_logp) + mean_logp
    return predicted, actual


def diagnostic(seed: int, *, device: str = "cpu") -> dict:
    """L1 arithmetic fixtures, never an RLVR training or model benchmark."""
    if device != "cpu":
        raise ValueError("RCEA diagnostic only supports CPU")
    rng = Random(seed)
    weights = [rng.uniform(1, 4) for _ in range(8)]
    p = [x / fsum(weights) for x in weights]
    labels = [(False, None, None)] * 2 + [(True, False, None)] * 2 + [
        (True, True, "a"), (True, True, "a"), (True, True, "b"), (True, True, "c"),
    ]
    result = entropy_allocation([Trajectory(w, *label) for w, label in zip(p, labels, strict=True)])
    logits = [rng.uniform(-3, 3) for _ in range(7)]
    predicted, actual = local_entropy_change(logits, [0.001 * x for x in logits])
    residual = abs(result.total - result.reconstructed)
    checks = {
        "chain_rule": residual < 1e-12,
        "covariance_predicts_sharpening": predicted < 0 and actual < 0,
        "mode_count_within_support": result.effective_modes is not None and 1 < result.effective_modes <= 3,
    }
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "checks": checks,
        "metrics": {
            "entropy_reconstruction_abs_error": residual,
            "effective_valid_modes": result.effective_modes,
            "predicted_entropy_delta_nats": predicted, "observed_entropy_delta_nats": actual,
            "first_order_abs_error": abs(predicted - actual),
        },
    }
