"""Finite-MDP exact references for the complete online Algorithm 1."""
import itertools
import json
import math
from pathlib import Path

import numpy as np
import pytest

from auto_research.foundation_models.rkl_policy_distillation import (
    FiniteMDP, LEARNING_RATE, bounded_prefix_comparisons, diagnostic,
    evaluate_exact_moments, exponential_weights, learn_online, local_reverse_kl,
)


def fixture():
    transitions = np.array([[[[.8, .2], [.1, .9]], [[.4, .6], [.3, .7]]],
                            [[[.7, .3], [.2, .8]], [[.5, .5], [.15, .85]]]])
    mdp = FiniteMDP(np.array([.7, .3]), transitions)
    teacher = np.repeat(np.array([[[.8, .2], [.3, .7]]]), 3, axis=0)
    policies = np.repeat(np.array([[[[.6, .4], [.4, .6]]],
                                   [[[.2, .8], [.7, .3]]],
                                   [[[.95, .05], [.1, .9]]]]), 3, axis=1)
    return mdp, policies, teacher


def trajectories(mdp, policy):
    """Independent enumeration, deliberately separate from forward recursion."""
    for states in itertools.product(range(mdp.states), repeat=mdp.horizon):
        for actions in itertools.product(range(mdp.actions), repeat=mdp.horizon):
            probability = mdp.initial[states[0]]
            for h in range(mdp.horizon):
                probability *= policy[h, states[h], actions[h]]
                if h + 1 < mdp.horizon:
                    probability *= mdp.transitions[h, states[h], actions[h], states[h + 1]]
            if probability > 0:
                yield np.array(states), np.array(actions), probability


def scalar_kl(p, q):
    return sum(float(x) * math.log(float(x / y)) for x, y in zip(p, q, strict=True) if x > 0)


def test_local_kl_support_and_zero_terms():
    np.testing.assert_allclose(local_reverse_kl(np.array([.5, .5]), np.array([.8, .2])), scalar_kl([.5, .5], [.8, .2]))
    assert local_reverse_kl(np.array([1., 0.]), np.array([1., 0.])) == 0
    with pytest.raises(ValueError, match="support"):
        local_reverse_kl(np.array([.5, .5]), np.array([1., 0.]))


def test_eq2_eq6_scalar_reference_and_common_weight_negative_control():
    _, policies, teacher = fixture()
    states = np.array([0, 1, 0])
    actions = np.array([0, 1, 0])
    result = bounded_prefix_comparisons(policies, 0, states, actions, teacher[np.arange(3), states])
    expected = []
    for index, policy in enumerate(policies):
        prior_candidate = prior_rollout = 0.
        candidate_prefix = rollout_prefix = 1.
        loss = 0.
        for h, state in enumerate(states):
            next_candidate = min(1., prior_candidate + scalar_kl(policy[h, state], teacher[h, state]))
            next_rollout = min(1., prior_rollout + scalar_kl(policies[0, h, state], teacher[h, state]))
            increment_candidate = next_candidate - min(1., prior_candidate)
            increment_rollout = next_rollout - min(1., prior_rollout)
            weight = min(1., candidate_prefix / rollout_prefix)
            assert result.prefix_weights[index, h] == pytest.approx(weight)
            loss += weight * (increment_candidate - increment_rollout)
            prior_candidate += scalar_kl(policy[h, state], teacher[h, state])
            prior_rollout += scalar_kl(policies[0, h, state], teacher[h, state])
            candidate_prefix *= policy[h, state, actions[h]]
            rollout_prefix *= policies[0, h, state, actions[h]]
        expected.append(loss)
    np.testing.assert_allclose(result.losses, expected, atol=1e-14)
    np.testing.assert_allclose(result.increments.sum(1), np.minimum(
        local_reverse_kl(policies[:, np.arange(3), states], teacher[np.arange(3), states][None]).sum(1), 1))
    assert np.all(result.prefix_weights[:, 0] == 1)  # before first action
    wrong_baseline = (result.prefix_weights * result.increments - result.increments[0]).sum(1)
    assert not np.allclose(result.losses, wrong_baseline)
    wrong_clipping = np.minimum(local_reverse_kl(policies[:, np.arange(3), states], teacher[np.arange(3), states][None]), 1)
    assert not np.allclose(result.increments, wrong_clipping)


def test_zero_candidate_prefix_no_division_nan():
    policies = np.array([[[[.5, .5]], [[.5, .5]]], [[[0., 1.]], [[.9, .1]]]])
    teacher = np.array([[.8, .2], [.8, .2]])
    result = bounded_prefix_comparisons(policies, 0, np.array([0, 0]), np.array([0, 1]), teacher)
    assert result.prefix_weights[1].tolist() == [1., 0.]
    assert np.isfinite(result.losses).all()


def test_exact_population_moments_and_trajectory_chain_rule():
    mdp, policies, teacher = fixture()
    actual = evaluate_exact_moments(mdp, policies, teacher)
    means, seconds, direct_divergences = [], [], []
    for policy in policies:
        mean = second = divergence = total_probability = 0.
        for states, actions, probability in trajectories(mdp, policy):
            total_probability += probability
            cumulative = sum(scalar_kl(policy[h, state], teacher[h, state]) for h, state in enumerate(states))
            mean += probability * cumulative
            second += probability * cumulative ** 2
            trajectory_ratio = math.prod(policy[h, state, actions[h]] / teacher[h, state, actions[h]] for h, state in enumerate(states))
            divergence += probability * math.log(trajectory_ratio)
        assert total_probability == pytest.approx(1)
        means.append(mean)
        seconds.append(second)
        direct_divergences.append(divergence)
    np.testing.assert_allclose(actual["risks"], means, atol=1e-14)
    np.testing.assert_allclose(actual["second_moments"], seconds, atol=1e-14)
    np.testing.assert_allclose(actual["risks"], direct_divergences, atol=1e-14)
    assert actual["relative_second_moment_B"] >= 1


def test_symmetric_prefix_mass_identity_under_exact_rollout_expectation():
    mdp, policies, teacher = fixture()
    expected_losses = np.zeros((len(policies), len(policies)))
    for rollout in range(len(policies)):
        for states, actions, probability in trajectories(mdp, policies[rollout]):
            comparison = bounded_prefix_comparisons(policies, rollout, states, actions, teacher[np.arange(3), states])
            expected_losses[rollout] += probability * comparison.losses
    # Eq. 7 exchanges candidate/rollout under the shared min(prefix masses).
    np.testing.assert_allclose(expected_losses, -expected_losses.T, atol=1e-14)
    w = np.array([.2, .3, .5])
    assert w @ expected_losses @ w == pytest.approx(0, abs=1e-14)


def test_algorithm1_visited_only_feedback_and_weight_replay():
    mdp, policies, teacher = fixture()
    visited = []

    def feedback(h, state):
        visited.append((h, state))
        return teacher[h, state]

    result = learn_online(mdp, policies, feedback, episodes=32, seed=9)
    assert visited == [(h, state) for episode in result.states for h, state in enumerate(episode)]
    assert result.teacher_query_count == 32 * 3
    weights = np.full(3, 1 / 3)
    np.testing.assert_array_equal(result.weight_history[0], weights)
    for t, loss in enumerate(result.losses):
        assert loss[result.rollout_indices[t]] == 0
        weights *= np.exp(-LEARNING_RATE * loss)
        weights /= weights.sum()
        np.testing.assert_allclose(result.weight_history[t + 1], weights, atol=1e-14)
    assert result.selected_index == int(weights.argmax())
    duplicate = np.repeat(policies[:1], 2, axis=0)
    tied = learn_online(mdp, duplicate, lambda h, state: teacher[h, state], episodes=4)
    assert tied.selected_index == 0


def test_unvisited_states_are_not_queried_and_budget_is_enforced():
    transitions = np.zeros((1, 2, 2, 2))
    transitions[..., 0] = 1
    mdp = FiniteMDP(np.array([1., 0.]), transitions)
    policies = np.full((2, 2, 2, 2), .5)

    def feedback(h, state):
        assert state == 0
        return np.array([.6, .4])

    result = learn_online(mdp, policies, feedback, episodes=3)
    assert result.teacher_query_count == 6
    with pytest.raises(ValueError, match="cost gate"):
        learn_online(mdp, policies, feedback, episodes=4097)
    with pytest.raises(ValueError, match="full action distribution"):
        learn_online(mdp, policies, lambda h, state: np.array([[.6, .4]]), episodes=1)
    with pytest.raises(ValueError):
        exponential_weights(np.array([.5, .5]), np.array([1.1, 0.]))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic_contract(seed):
    row = diagnostic(seed)
    assert row["seed"] == seed and all(row["checks"].values())
    assert row["metrics"]["episodes"] == 256
    assert all(type(value) in (float, int, bool) and math.isfinite(value) for value in row["metrics"].values())


def test_documentation_keeps_theoretical_cpu_scope():
    root = Path(__file__).resolve().parents[1]
    spec = json.loads((root / "src/auto_research/paper_specs/catalog/foundation-models/rkl-policy-distillation.json").read_text())
    assert spec["first_author_affiliation"] == "University of Virginia"
    assert spec["published_at"] == "2026-10-22T07:19:49Z"
    assert spec["full_experiment_status"] == "not_run_scope_limited_protocol"
    assert spec["requires_gpu_validation"] is False and spec["adapter"] is None
    text = (root / "docs" / spec["detail_path"]).read_text()
    for marker in ("论文信息", "原作者代码", "未发现", "Algorithm 1", "1/256", "Google Research", "relative second", "future work", "未报告生产线上 A/B"):
        assert marker in text
