from __future__ import annotations

import numpy as np

from .algorithm_core import PolicyState, _softmax, initialize, metrics
from .data import CandidateGroup
from .rollout_correction import rollout_engine_probabilities
from .algorithm_families.family_1 import apply as family_1
from .algorithm_families.family_2 import apply as family_2
from .algorithm_families.family_3 import apply as family_3
from .algorithm_families.family_4 import apply as family_4


def update(
    algorithm: str,
    state: PolicyState,
    group: CandidateGroup,
    learning_rate: float,
    rng: np.random.Generator,
    group_size: int,
    cache_index: int,
) -> tuple[float, dict[str, float]]:
    probabilities = _softmax(group.features @ state.weights)
    reference = _softmax(group.features @ state.reference)
    rollout_training_probabilities = _softmax(
        group.features @ state.rollout_weights
    )
    sampling_probabilities = (
        rollout_training_probabilities
        if algorithm in {
            "ppo-rlhf", "grpo", "reco-grpo", "dapo", "gspo", "spin",
            "seed", "cast", "cort", "ripo", "tis", "icepop", "kpop",
            "gppo", "dr-grpo", "armor", "reinforce-plus", "taco",
            "chord", "vapo",
        } else probabilities
    )
    if algorithm in {"tis", "icepop", "online-icepop"}:
        sampling_probabilities = rollout_engine_probabilities(
            group.features, state.rollout_weights
        )
    sampled = rng.choice(
        len(probabilities), size=min(group_size, len(probabilities)),
        replace=False, p=sampling_probabilities,
    )
    diagnostics: dict[str, float] = {}

    for handler in (family_1, family_2, family_3, family_4):
        result = handler(algorithm, state, group, learning_rate, rng, group_size, cache_index, probabilities, reference, rollout_training_probabilities, sampling_probabilities, sampled, diagnostics)
        if result is not None:
            gradient, loss, diagnostics = result
            break

    state.weights += learning_rate * np.clip(gradient, -5.0, 5.0)
    if algorithm == "ppo-rlhf" and state.ppo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "grpo" and state.grpo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "reco-grpo" and state.reco_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "dapo" and state.dapo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "gspo" and state.gspo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "spin" and state.spin_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm in {
        "ripo", "tis", "icepop", "kpop", "gppo", "dr-grpo", "armor",
        "reinforce-plus", "taco", "chord", "vapo",
        "vad", "rlaif", "process-supervision", "math-shepherd",
        "self-rewarding", "luffy", "ttrl", "absolute-zero", "intuitor",
        "cispo", "spiral", "conspo",
        "minirl", "missing-old-logits", "stare",
        "rrc", "rail", "specroll",
    }:
        state.variant_updates += 1
        if state.variant_updates % 16 == 0:
            state.rollout_weights = state.weights.copy()
    if algorithm == "online-icepop":
        state.rollout_weights = state.weights.copy()
        state.online_rollout_refreshes += 1
    diagnostics["loss"] = loss
    diagnostics["policy_entropy"] = float(-np.sum(probabilities * np.log(probabilities + 1e-12)))
    return loss, diagnostics
