"""EmoReward's bounded CPU allocation kernel (arXiv:2611.06518v1, Eqs. 8–10)."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
import math
import random
from types import MappingProxyType

REQUIRES_GPU_VALIDATION = False


def _finite(value: float, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


def _unit_vector(values: Sequence[float], label: str) -> tuple[float, ...]:
    result = tuple(_finite(value, label) for value in values)
    if not result or any(not 0 <= value <= 1 for value in result):
        raise ValueError(f"{label} must be a nonempty vector in [0, 1]")
    return result


def _base(values: Sequence[float]) -> tuple[float, ...]:
    base = _unit_vector(values, "base weights")
    if not math.isclose(math.fsum(base), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("base weights must sum to 1")
    return base


def _context(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("context must be a nonempty regime key")
    return value


@dataclass(frozen=True, slots=True)
class ReferenceTrace:
    """Raw provider scores and an outcome from a completed reference run."""

    context: str
    scores: tuple[float, ...]
    outcome: float


@dataclass(frozen=True, slots=True)
class RewardMemory:
    """Frozen regime entries plus a global fallback; retains no reference rows."""

    provider_count: int
    global_multipliers: tuple[float, ...] | None = None
    contexts: Mapping[str, tuple[float, ...]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if type(self.provider_count) is not int or self.provider_count < 1:
            raise ValueError("provider_count must be a positive integer")

        def checked(values: Sequence[float]) -> tuple[float, ...]:
            result = tuple(_finite(value, "multiplier") for value in values)
            if len(result) != self.provider_count or any(value <= 0 for value in result):
                raise ValueError("multipliers must be positive and match provider_count")
            return result

        if self.global_multipliers is not None:
            object.__setattr__(self, "global_multipliers", checked(self.global_multipliers))
        object.__setattr__(self, "contexts", MappingProxyType({
            _context(key): checked(values) for key, values in self.contexts.items()
        }))

    def multipliers(self, context: str) -> tuple[float, ...]:
        """Algorithm 1 lookup: supported regime, global table, then unit weights."""
        return self.contexts.get(
            _context(context), self.global_multipliers or (1.0,) * self.provider_count
        )

    def weights(self, base_weights: Sequence[float], context: str) -> tuple[float, ...]:
        """Equation 10 normalized allocation before per-instance gates."""
        base = _base(base_weights)
        weights = _tilt(base, self.multipliers(context))
        total = math.fsum(weights)
        return tuple(weight / total for weight in weights)


def _tilt(base: tuple[float, ...], multipliers: tuple[float, ...]) -> tuple[float, ...]:
    if len(base) != len(multipliers):
        raise ValueError("memory and base weights use different provider counts")
    return tuple(weight * multiplier for weight, multiplier in zip(base, multipliers, strict=True))


def _center(values: Sequence[float]) -> tuple[float, ...]:
    mean = math.fsum(values) / len(values)
    return tuple(value - mean for value in values)


def _calibrate(
    rows: Sequence[ReferenceTrace], provider_count: int, temperature: float, cap: float, epsilon: float
) -> tuple[float, ...]:
    # Correlate raw scores, not gated scores or applied weights. Scaling y
    # and epsilon together preserves Eq. 9 while avoiding outcome overflow.
    scale = max(1.0, max(abs(row.outcome) for row in rows))
    y = _center([row.outcome / scale for row in rows])
    count = len(y)
    sigma_y = math.sqrt(math.fsum(value * value for value in y) / count)
    reliabilities = []
    for index in range(provider_count):
        scores = tuple(row.scores[index] for row in rows)
        if sigma_y == 0 or min(scores) == max(scores):
            reliabilities.append(0.0)
            continue
        x = _center(scores)
        sigma_x = math.sqrt(math.fsum(value * value for value in x) / count)
        covariance = math.fsum(a * b for a, b in zip(x, y, strict=True)) / count
        denominator = sigma_x * sigma_y + epsilon / scale
        reliabilities.append(covariance / denominator if denominator else 0.0)
    return tuple(math.exp(max(-cap, min(cap, relative / temperature))) for relative in _center(reliabilities))


def build_reward_memory(
    traces: Iterable[ReferenceTrace],
    *,
    provider_count: int,
    temperature: float = 0.5,
    cap: float = 1.0,
    minimum_support: int = 20,
    epsilon: float = 1e-8,
) -> RewardMemory:
    """Fit Algorithm 2 once; sparse regimes use the global reference bank."""
    if type(provider_count) is not int or provider_count < 1:
        raise ValueError("provider_count must be a positive integer")
    if type(minimum_support) is not int or minimum_support < 1:
        raise ValueError("minimum_support must be a positive integer")
    temperature = _finite(temperature, "temperature")
    cap = _finite(cap, "log-multiplier cap")
    epsilon = _finite(epsilon, "epsilon")
    if temperature <= 0 or not 0 <= cap <= 700 or epsilon <= 0:
        raise ValueError("positive temperature/epsilon and a safe nonnegative log cap required")
    rows = []
    by_context = defaultdict(list)
    for trace in traces:
        context = _context(trace.context)
        scores = _unit_vector(trace.scores, "reference scores")
        if len(scores) != provider_count:
            raise ValueError("trace width differs from provider_count")
        row = ReferenceTrace(context, scores, _finite(trace.outcome, "reference outcome"))
        rows.append(row)
        by_context[context].append(row)
    if not rows:
        return RewardMemory(provider_count)
    args = provider_count, temperature, cap, epsilon
    return RewardMemory(
        provider_count,
        _calibrate(rows, *args),
        {key: _calibrate(subset, *args) for key, subset in by_context.items() if len(subset) >= minimum_support},
    )


@dataclass(frozen=True, slots=True)
class FusedReward:
    emotion_reward: float
    total_reward: float
    active_weights: tuple[float, ...]


def fuse_reward(
    *,
    scores: Sequence[float],
    gates: Sequence[float],
    base_weights: Sequence[float],
    context: str,
    video_reward: float,
    memory: RewardMemory | None = None,
    alpha: float = 0.5,
    beta: float = 0.5,
    gate_threshold: float = 1e-8,
    epsilon: float = 1e-8,
) -> FusedReward:
    """Fuse precomputed scores and Eq. 7 gates; the current outcome is not an input."""
    score = _unit_vector(scores, "scores")
    gate = _unit_vector(gates, "gates")
    base = _base(base_weights)
    context = _context(context)
    if not len(score) == len(gate) == len(base):
        raise ValueError("scores, gates and base weights must use the same provider order")
    threshold = _finite(gate_threshold, "gate threshold")
    epsilon = _finite(epsilon, "epsilon")
    alpha = _finite(alpha, "alpha")
    beta = _finite(beta, "beta")
    video = _finite(video_reward, "video reward")
    if threshold < 0 or epsilon <= 0 or alpha < 0 or beta < 0:
        raise ValueError("nonnegative threshold and mixture coefficients, positive epsilon required")
    tilted = base if memory is None else _tilt(base, memory.multipliers(context))
    weighted_gates = tuple(weight * current for weight, current in zip(tilted, gate, strict=True))
    active = tuple(weight if weight > threshold else 0.0 for weight in weighted_gates)
    emotion = math.fsum(weight * value for weight, value in zip(active, score, strict=True)) / (
        math.fsum(active) + epsilon
    )
    return FusedReward(emotion, alpha * video + beta * emotion, active)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Synthetic signed-reliability and frozen-lookup mechanism checks only."""
    if device != "cpu":
        raise ValueError("EmoReward allocation diagnostic is CPU-only")
    rng = random.Random(seed)
    outcomes = [rng.uniform(0.0, 1.0) for _ in range(25)]
    traces = [ReferenceTrace("active", (y, 1 - y, 0.5), y) for y in outcomes]
    traces.append(ReferenceTrace("rare", (0.9, 0.3, 0.5), 0.7))
    memory = build_reward_memory(traces, provider_count=3)
    before = memory.multipliers("active")
    options = dict(scores=(0.2, 0.8, 0.6), gates=(0.0, 0.5, 1.0), base_weights=(0.4, 0.4, 0.2),
                   context="active", video_reward=0.7)
    reflect = fuse_reward(**options)
    evolved = fuse_reward(**options, memory=memory)
    cold = fuse_reward(**options, memory=build_reward_memory([], provider_count=3))
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "metrics": {
            "reflect_emotion_reward": reflect.emotion_reward,
            "memory_emotion_reward": evolved.emotion_reward,
            "largest_multiplier": max(before),
            "smallest_multiplier": min(before),
            "masked_provider_weight": evolved.active_weights[0],
            "reference_mean_outcome": math.fsum(outcomes) / len(outcomes),
        },
        "checks": {
            "signed_reliability_is_bounded": before[0] > before[2] > before[1]
            and all(math.exp(-1) <= value <= math.e for value in before),
            "invalid_evidence_gets_no_mass": evolved.active_weights[0] == 0.0,
            "memory_changes_relative_allocation": not math.isclose(reflect.emotion_reward, evolved.emotion_reward),
            "sparse_and_unseen_regimes_use_global": memory.multipliers("rare") == memory.multipliers("unseen")
            == memory.global_multipliers,
            "empty_bank_recovers_reflect": cold == reflect,
            "runtime_lookup_does_not_update_memory": memory.multipliers("active") == before,
        },
    }
