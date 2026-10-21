"""ConvApparel §4 validation statistics and a deliberately non-LLM CPU baseline.

PLSA means population-level statistical alignment, not latent semantic analysis.
The small logistic discriminator below is a diagnostic baseline, not the paper's
fine-tuned Gemini HLS model. Real HLS can be supplied through the same scorer API.
"""

from __future__ import annotations

import itertools
import math
import random
import re
from bisect import bisect_left, bisect_right
from collections import Counter
from dataclasses import dataclass
from statistics import mean
from typing import Callable, Sequence


@dataclass(frozen=True)
class Conversation:
    session_id: str
    participant_id: str
    policy: str
    user_turns: tuple[str, ...]
    is_human: bool
    # Annotation values come from human raters or an independently validated judge.
    # They are not inferred from keywords by the validation component.
    annotations: tuple[tuple[str, float], ...] = ()
    simulator_training_sessions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.session_id or not self.participant_id or not self.policy:
            raise ValueError("session, participant and policy IDs are required")
        if type(self.is_human) is not bool:
            raise ValueError("is_human must be an explicit boolean")
        if not self.user_turns or any(not text.strip() for text in self.user_turns):
            raise ValueError("at least one nonempty user turn is required")
        if len(dict(self.annotations)) != len(self.annotations):
            raise ValueError("duplicate annotation name")
        if any(not math.isfinite(value) for _, value in self.annotations):
            raise ValueError("annotations must be finite")


@dataclass(frozen=True)
class DiscriminatorView:
    """No source class, policy, participant identity or rating reaches D(c)."""

    user_turns: tuple[str, ...]


def behavior_metrics(conversation: Conversation) -> dict[str, float]:
    """Basic §4.1 statistics plus externally provided dialog-act/experience rates."""
    result = {
        "turns_per_session": float(len(conversation.user_turns)),
        "words_per_user_turn": mean(len(turn.split()) for turn in conversation.user_turns),
    }
    if set(result).intersection(dict(conversation.annotations)):
        raise ValueError("annotations cannot overwrite computed basic statistics")
    result.update(conversation.annotations)
    return result


def _finite(values: Sequence[float]) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if not result or any(not math.isfinite(value) for value in result):
        raise ValueError("samples must be nonempty and finite")
    return result


def ks_statistic(first: Sequence[float], second: Sequence[float]) -> float:
    """Two-sided empirical KS distance, with ties evaluated at each jump."""
    a, b = _finite(first), _finite(second)
    a, b = sorted(a), sorted(b)
    return max(abs(bisect_right(a, point) / len(a) - bisect_right(b, point) / len(b)) for point in sorted(set(a + b)))


def mann_whitney_u(first: Sequence[float], second: Sequence[float]) -> float:
    """U for the first sample; average ranks are equivalent to half credit on ties."""
    a, b = _finite(first), _finite(second)
    ordered = sorted(b)
    return sum(bisect_left(ordered, x) + 0.5 * (bisect_right(ordered, x) - bisect_left(ordered, x)) for x in a)


def alignment_test(
    human: Sequence[float],
    simulated: Sequence[float],
    *,
    permutations: int = 999,
    exact_limit: int = 20_000,
    seed: int = 42,
) -> dict[str, float | int | str]:
    """KS and MWU with exact small-sample or seeded permutation p-values.

    This avoids asymptotic tie assumptions. Monte Carlo p-values use the +1
    correction. Neither a high p-value nor a small distance proves equivalence.
    """
    a, b = _finite(human), _finite(simulated)
    if permutations < 1 or exact_limit < 1:
        raise ValueError("positive permutation budgets required")
    pooled, n = a + b, len(a)
    ks = ks_statistic(a, b)
    u = mann_whitney_u(a, b)
    centered_u = abs(u - len(a) * len(b) / 2)
    combinations = math.comb(len(pooled), n)
    exact = combinations <= exact_limit
    rng = random.Random(seed)
    groups = (
        itertools.combinations(range(len(pooled)), n)
        if exact
        else (rng.sample(range(len(pooled)), n) for _ in range(permutations))
    )
    ks_extreme = u_extreme = total = 0
    for indices in groups:
        chosen = set(indices)
        left = [pooled[i] for i in range(len(pooled)) if i in chosen]
        right = [pooled[i] for i in range(len(pooled)) if i not in chosen]
        ks_extreme += ks_statistic(left, right) >= ks - 1e-12
        u_extreme += abs(mann_whitney_u(left, right) - len(a) * len(b) / 2) >= centered_u - 1e-12
        total += 1
    correction = 0 if exact else 1
    return {
        "human_mean": mean(a),
        "simulated_mean": mean(b),
        "ks": ks,
        "ks_pvalue": (ks_extreme + correction) / (total + correction),
        "mann_whitney_u": u,
        "mwu_pvalue": (u_extreme + correction) / (total + correction),
        "pvalue_method": "exact_permutation" if exact else "monte_carlo_permutation",
        "permutations": total,
    }


def plsa(
    human: Sequence[Conversation], simulated: Sequence[Conversation], *, seed: int = 42
) -> dict[str, dict[str, float | int | str]]:
    """Compare the same explicitly annotated metric in each population."""
    if not human or not simulated or any(not c.is_human for c in human) or any(c.is_human for c in simulated):
        raise ValueError("separate nonempty human and simulated populations required")
    metrics = [behavior_metrics(c) for c in (*human, *simulated)]
    keys = set(metrics[0])
    if any(set(row) != keys for row in metrics):
        raise ValueError("all conversations must use the same annotation schema")
    return {
        key: alignment_test(
            [row[key] for row in metrics[: len(human)]],
            [row[key] for row in metrics[len(human) :]],
            seed=seed,
        )
        for key in sorted(keys)
    }


def assert_split_disjoint(train: Sequence[Conversation], heldout: Sequence[Conversation]) -> None:
    """Participant/session-level separation, not a random split of user turns."""
    for name in ("session_id", "participant_id"):
        if {getattr(c, name) for c in train}.intersection(getattr(c, name) for c in heldout):
            raise ValueError(f"train/heldout {name} leakage")
    ids = [c.session_id for c in (*train, *heldout)]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate conversation session")


@dataclass(frozen=True)
class LogisticHumanDiscriminator:
    """Actually trained bag-of-words diagnostic; never advertised as Gemini HLS."""

    vocabulary: tuple[str, ...]
    weights: tuple[float, ...]
    bias: float
    training_sessions: frozenset[str]
    training_participants: frozenset[str]
    training_policies: frozenset[str]

    @staticmethod
    def tokens(conversation: Conversation | DiscriminatorView) -> Counter[str]:
        tokens = re.findall(r"\w+", " ".join(conversation.user_turns).lower())
        return Counter(tokens + [f"{left} {right}" for left, right in zip(tokens, tokens[1:])])

    def __call__(self, conversation: DiscriminatorView) -> float:
        counts = self.tokens(conversation)
        norm = max(1, sum(counts.values()))
        logit = self.bias + sum(weight * counts[token] / norm for token, weight in zip(self.vocabulary, self.weights, strict=True))
        return 1.0 / (1.0 + math.exp(-max(-40.0, min(40.0, logit))))


def train_logistic_discriminator(
    train: Sequence[Conversation], *, epochs: int = 200, learning_rate: float = 0.5, l2: float = 0.001
) -> LogisticHumanDiscriminator:
    """CPU diagnostic BCE optimization. Only training labels enter this routine."""
    if not train or {c.is_human for c in train} != {True, False}:
        raise ValueError("both human and simulated training classes required")
    if not 1 <= epochs <= 400 or not math.isfinite(learning_rate) or learning_rate <= 0 or not math.isfinite(l2) or l2 < 0:
        raise ValueError("invalid optimization budget")
    if len(train) > 256 or any(sum(len(turn.split()) for turn in c.user_turns) > 4096 for c in train):
        raise ValueError("CPU diagnostic training budget exceeds 256 conversations or 4096 words per conversation")
    if len({c.session_id for c in train}) != len(train):
        raise ValueError("duplicate training sessions")
    vocabulary = tuple(sorted({word for c in train for word in LogisticHumanDiscriminator.tokens(c)}))
    if len(vocabulary) > 4096:
        raise ValueError("CPU diagnostic vocabulary exceeds 4096 features; no automatic truncation")
    features = []
    for conversation in train:
        counts = LogisticHumanDiscriminator.tokens(conversation)
        norm = max(1, sum(counts.values()))
        features.append(tuple(counts[token] / norm for token in vocabulary))
    weights, bias = [0.0] * len(vocabulary), 0.0
    # Class balancing prevents the paper's different human/simulator counts from
    # becoming an unspoken source prior in this diagnostic baseline.
    counts_by_class = Counter(c.is_human for c in train)
    for _ in range(epochs):
        gradient, bias_gradient = [0.0] * len(vocabulary), 0.0
        for conversation, row in zip(train, features, strict=True):
            logit = bias + sum(w * x for w, x in zip(weights, row, strict=True))
            prediction = 1 / (1 + math.exp(-max(-40.0, min(40.0, logit))))
            error = (prediction - float(conversation.is_human)) / (2 * counts_by_class[conversation.is_human])
            bias_gradient += error
            for index, value in enumerate(row):
                gradient[index] += error * value
        weights = [w - learning_rate * (g + l2 * w) for w, g in zip(weights, gradient, strict=True)]
        bias -= learning_rate * bias_gradient
    return LogisticHumanDiscriminator(
        vocabulary, tuple(weights), bias,
        frozenset(c.session_id for c in train),
        frozenset(c.participant_id for c in train),
        frozenset(c.policy for c in train),
    )


def evaluate_hls(
    heldout: Sequence[Conversation], scorer: Callable[[DiscriminatorView], float]
) -> dict[str, float | int]:
    """Mean D(c), heldout classifier accuracy and Brier score are separate facts."""
    if not heldout or {c.is_human for c in heldout} != {True, False}:
        raise ValueError("both heldout classes required to validate a discriminator")
    if isinstance(scorer, LogisticHumanDiscriminator):
        if scorer.training_sessions.intersection(c.session_id for c in heldout) or scorer.training_participants.intersection(c.participant_id for c in heldout):
            raise ValueError("discriminator evaluated on training identity")
    predictions = [float(scorer(DiscriminatorView(c.user_turns))) for c in heldout]
    if any(not math.isfinite(p) or not 0 <= p <= 1 for p in predictions):
        raise ValueError("D(c) must be a finite human probability")
    return {
        "conversations": len(heldout),
        "simulated_hls": mean(p for c, p in zip(heldout, predictions, strict=True) if not c.is_human),
        "human_hls": mean(p for c, p in zip(heldout, predictions, strict=True) if c.is_human),
        "discriminator_accuracy": mean((p >= 0.5) == c.is_human for c, p in zip(heldout, predictions, strict=True)),
        "brier_score": mean((p - c.is_human) ** 2 for c, p in zip(heldout, predictions, strict=True)),
    }


def counterfactual_validation(
    simulator_training: Sequence[Conversation], heldout: Sequence[Conversation],
    scorer: Callable[[DiscriminatorView], float], *, training_policy: str, target_policy: str,
    seed: int = 42,
) -> dict:
    """Validate supplied OOD simulator traces, not train or generate a simulator.

    The simulator's human training manifest is distinct from the discriminator
    training corpus. Generated traces must declare the source training sessions;
    this is a provenance contract, not proof of a remote simulator's behavior.
    """
    if training_policy == target_policy or not simulator_training or {c.policy for c in simulator_training} != {training_policy} or any(not c.is_human for c in simulator_training):
        raise ValueError("simulator training must contain only human source-policy data")
    assert_split_disjoint(simulator_training, heldout)
    if not heldout or {c.policy for c in heldout} != {target_policy}:
        raise ValueError("heldout data must contain only the unseen target policy")
    expected_sessions = frozenset(c.session_id for c in simulator_training)
    if any(frozenset(c.simulator_training_sessions) != expected_sessions for c in heldout if not c.is_human):
        raise ValueError("simulated trace has missing/mismatched simulator training provenance")
    return {
        "training_policy": training_policy, "target_policy": target_policy,
        "simulator_training_provenance": "declared_manifest_not_independently_certified",
        "plsa": plsa([c for c in heldout if c.is_human], [c for c in heldout if not c.is_human], seed=seed),
        "hls": evaluate_hls(heldout, scorer),
        "diagnostic_only": True,
        "discriminator_backend": "cpu_bag_of_words_logistic_not_paper_gemini" if isinstance(scorer, LogisticHumanDiscriminator) else "external_scorer_requires_independent_validation",
    }
