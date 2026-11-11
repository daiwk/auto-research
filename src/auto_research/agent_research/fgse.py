"""FGSE equations 7-9 on external verifier records; no actor or probe generator."""
from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Probe:
    before: float
    after: float
    expected_effect: bool = True

    def __post_init__(self):
        if (any(type(x) not in {int, float} or not math.isfinite(x) or not 0 <= x <= 1
                for x in (self.before, self.after)) or type(self.expected_effect) is not bool):
            raise ValueError("paired finite verifier scores in [0,1] and a binary effect required")

    @property
    def delta(self):
        return self.after - self.before


@dataclass(frozen=True)
class GateConfig:
    minimum_gain: float = .05
    maximum_failure: float = .1
    maximum_regression: float = .02
    tolerated_drop: float = 0.

    def __post_init__(self):
        values = (self.minimum_gain, self.maximum_failure, self.maximum_regression, self.tolerated_drop)
        if (any(type(x) not in {int, float} or not math.isfinite(x) for x in values)
                or not 0 < self.minimum_gain <= 1 or not 0 <= self.maximum_failure <= 1
                or not 0 <= self.maximum_regression <= 1 or not 0 <= self.tolerated_drop <= 1):
            raise ValueError("valid finite commitment thresholds required")


@dataclass(frozen=True)
class GateDecision:
    commit: bool
    gain: float
    failure_rate: float
    regression_damage: float


def commitment_gate(transfer, falsification, regression, config: GateConfig | None = None):
    """Empirical gate only, not the paper's confidence-bound generalization theorem.

    Records must come from paired before/temporary-state runs, never predictions
    of what a candidate might do. This function does not generate those runs.
    """
    groups = tuple(tuple(group) for group in (transfer, falsification, regression))
    if any(not group or not all(isinstance(row, Probe) for row in group) for group in groups):
        raise ValueError("three nonempty verifier-probe groups required")
    config = config or GateConfig()
    gain = math.fsum(row.delta for row in groups[0]) / len(groups[0])
    failure = sum(row.delta < -config.tolerated_drop or not row.expected_effect
                  for row in groups[1]) / len(groups[1])
    damage = math.fsum(max(0., -row.delta) for row in groups[2]) / len(groups[2])
    commit = (gain >= config.minimum_gain and failure <= config.maximum_failure
              and damage <= config.maximum_regression)
    return GateDecision(commit, gain, failure, damage)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("FGSE empirical gate is CPU-only")
    transfer, safe = (Probe(.2, .4), Probe(.4, .5)), (Probe(.7, .7),)
    accepted = commitment_gate(transfer, safe, safe)
    bad_effect = commitment_gate(transfer, (Probe(.7, .8, False),), safe)
    bad_regression = commitment_gate(transfer, safe, (Probe(.9, .7),))
    no_gain = commitment_gate(safe, safe, safe)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"transfer_gain": accepted.gain, "falsification_failure": bad_effect.failure_rate,
                        "regression_damage": bad_regression.regression_damage},
            "checks": {"passes_three_gates": accepted.commit,
                       "effect_failure_blocks_even_without_drop": not bad_effect.commit,
                       "regression_blocks_positive_transfer": not bad_regression.commit,
                       "no_gain_rejected": not no_gain.commit}}
