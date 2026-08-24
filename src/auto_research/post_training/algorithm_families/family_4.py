from __future__ import annotations

import numpy as np

from ..algorithm_core import (PolicyState, _one_hot, _reinforce_gradient, _scalar_rewards, _softmax, _weighted_policy_gradient)
from ..data import CandidateGroup
from ..rollout_correction import (icepop_weights, rollout_engine_probabilities, truncated_importance_weights)

def apply(algorithm, state, group, learning_rate, rng, group_size, cache_index, probabilities, reference, rollout_training_probabilities, sampling_probabilities, sampled, diagnostics):
    if algorithm in {
        'rrc', 'rail', 'specroll', 'pto', 'c2-dpo', 'gcpo',
        'r2-opd', 'sr-opsd', 'opd2', 'causal-opd', 'smopd', 'rstg',
        'sa-mrpo', 'rubric-dropout', 'erils', 'crpo', 'serpo', 'iso-rlvr',
    }:
        if algorithm in {
            'r2-opd', 'sr-opsd', 'opd2', 'causal-opd', 'smopd', 'rstg',
            'sa-mrpo', 'rubric-dropout', 'erils', 'crpo', 'serpo', 'iso-rlvr',
        }:
            from ..historical_b08_b09 import update_historical

            gradient, loss, latest = update_historical(
                algorithm, state, group, probabilities, reference,
                rollout_training_probabilities, sampled, rng,
            )
            diagnostics.update(latest)
            return gradient, loss, diagnostics
        if algorithm == 'gcpo':
            from ..latest_20260824 import update_gcpo

            gradient, loss, latest = update_gcpo(
                state, group, probabilities, reference, sampled
            )
            diagnostics.update(latest)
            return gradient, loss, diagnostics
        if algorithm in {'pto', 'c2-dpo'}:
            from ..latest_20260813 import update_latest
        else:
            from ..latest_20260809 import update_latest

        gradient, loss, latest = update_latest(
            algorithm, state, group, probabilities, reference,
            rollout_training_probabilities, sampled, rng,
        )
        diagnostics.update(latest)
    elif algorithm in {'minirl', 'missing-old-logits', 'stare'}:
        from ..p1_20260808 import update_p1

        gradient, loss, diagnostics = update_p1(
            algorithm, state, group, probabilities, reference, sampled, rng,
        )
    else:
        rewards = group.rewards[sampled]
        if algorithm == "gprl":
            normalized = (rewards - rewards.mean(0)) / (rewards.std(0) + 1e-6)
            advantages = normalized @ state.reward_axis_weights
            # A normalized axis always has zero mean, so drift must be measured
            # before normalization. Compare each axis' operating point with the
            # group-wide reward level to detect an exploitable dominant axis.
            axis_drift = np.abs(rewards.mean(0) - rewards.mean())
            if float(axis_drift.max()) > 0.25:
                state.reward_axis_weights = 1.0 / (axis_drift + 0.25)
                state.reward_axis_weights /= state.reward_axis_weights.sum()
                state.drift_events += 1
            diagnostics["preference_axes"] = 4.0
            diagnostics["drift_events"] = float(state.drift_events)
        elif algorithm == "tcr":
            outcome = rewards[:, 0]
            process = rewards[:, 2]
            state.outcome_ema = 0.9 * state.outcome_ema + 0.1 * float(outcome.mean())
            thinking_surplus = process - state.outcome_ema
            advantages = outcome + 0.5 * thinking_surplus
            advantages -= advantages.mean()
            diagnostics["outcome_ema"] = state.outcome_ema
            diagnostics["thinking_surplus"] = float(thinking_surplus.mean())
        else:  # Defensive fallback; config rejects unknown algorithms.
            scalar = rewards @ np.asarray((0.7, 0.05, 0.2, 0.05))
            advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        gradient = np.zeros_like(state.weights)
        expected_features = probabilities @ group.features
        for index, advantage in zip(sampled, advantages):
            gradient += float(advantage) * (group.features[index] - expected_features)
        gradient /= len(sampled)
        kl_gradient = group.features.T @ (probabilities - reference)
        gradient -= 0.02 * kl_gradient
        loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
    return gradient, loss, diagnostics
