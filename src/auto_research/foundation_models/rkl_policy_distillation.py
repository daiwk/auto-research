"""Algorithm 1 of arXiv:2610.30844v1, exact finite-policy CPU implementation.

This implements online full-feedback bounded prefix comparisons, NOT an LLM
optimizer. The learner sees teacher distributions only at visited states. Exact
population risks and moment audits are separate evaluation-only functions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

LEARNING_RATE = 1 / 256
REQUIRES_GPU_VALIDATION = False


def _probabilities(value: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(value, dtype=np.float64)
    if not np.isfinite(array).all() or np.any(array < 0) or not np.allclose(array.sum(-1), 1, atol=1e-12, rtol=1e-12):
        raise ValueError(f"{name} must be finite nonnegative probability rows")
    return array


@dataclass(frozen=True)
class FiniteMDP:
    initial: np.ndarray
    transitions: np.ndarray  # [H-1,S,A,S], no reward or teacher information

    def __post_init__(self) -> None:
        initial = _probabilities(self.initial, "initial distribution")
        transition = _probabilities(self.transitions, "transitions")
        if initial.ndim != 1 or transition.ndim != 4 or transition.shape[1] != len(initial) or transition.shape[3] != len(initial):
            raise ValueError("expected initial[S] and transitions[H-1,S,A,S]")
        if not 1 <= len(initial) <= 16 or not 1 <= transition.shape[2] <= 16 or not 0 <= len(transition) < 16:
            raise ValueError("cost gate: S,A,H <= 16")
        for name, array in (("initial", initial), ("transitions", transition)):
            immutable = array.copy()
            immutable.setflags(write=False)
            object.__setattr__(self, name, immutable)

    @property
    def horizon(self) -> int:
        return len(self.transitions) + 1

    @property
    def states(self) -> int:
        return len(self.initial)

    @property
    def actions(self) -> int:
        return self.transitions.shape[2]


def _policies(policies: np.ndarray, mdp: FiniteMDP | None = None) -> np.ndarray:
    value = _probabilities(policies, "candidate policies")
    if value.ndim != 4 or min(value.shape) < 1 or value.shape[0] > 64 or value.size > 262144:
        raise ValueError("expected bounded policy class [N,H,S,A], N <= 64")
    if mdp is not None and value.shape[1:] != (mdp.horizon, mdp.states, mdp.actions):
        raise ValueError("policy and MDP dimensions do not align")
    return value


def local_reverse_kl(candidate: np.ndarray, teacher: np.ndarray) -> np.ndarray:
    """Exact KL(candidate||teacher), including zero-support handling."""
    p = _probabilities(candidate, "candidate distributions")
    q = _probabilities(teacher, "teacher distributions")
    if p.shape[-1] != q.shape[-1]:
        raise ValueError("action dimensions differ")
    if np.any((p > 0) & (q == 0)):
        raise ValueError("teacher does not cover candidate support: finite-risk assumption fails")
    logp = np.log(np.where(p > 0, p, 1))
    logq = np.log(np.where(q > 0, q, 1))
    return np.maximum((p * (logp - logq)).sum(-1), 0)


@dataclass(frozen=True)
class PrefixComparison:
    losses: np.ndarray
    increments: np.ndarray
    prefix_weights: np.ndarray


def bounded_prefix_comparisons(policies: np.ndarray, rollout_index: int,
                               states: np.ndarray, actions: np.ndarray,
                               teacher_feedback: np.ndarray) -> PrefixComparison:
    """Eq. 2 and Eq. 6 on ONE observed episode, no unvisited-state teacher data.

    Prefix h excludes action h. One clipped prefix ratio multiplies BOTH the
    candidate increment and the rollout increment; do not clip their difference.
    """
    policies = _policies(policies)
    n, horizon, state_count, action_count = policies.shape
    states, actions = np.asarray(states), np.asarray(actions)
    if (states.shape != (horizon,) or actions.shape != (horizon,)
            or not np.issubdtype(states.dtype, np.integer) or not np.issubdtype(actions.dtype, np.integer)
            or np.any((states < 0) | (states >= state_count))
            or np.any((actions < 0) | (actions >= action_count))):
        raise ValueError("valid integer states/actions for a complete episode required")
    if not isinstance(rollout_index, (int, np.integer)) or not 0 <= rollout_index < n:
        raise ValueError("rollout policy outside class")
    feedback = _probabilities(teacher_feedback, "visited-state full feedback")
    if feedback.shape != (horizon, action_count):
        raise ValueError("full distribution at every visited state required")
    visited = policies[:, np.arange(horizon), states]
    k = local_reverse_kl(visited, feedback[None])
    clipped = np.minimum(k.cumsum(axis=1), 1)
    increments = np.diff(np.concatenate((np.zeros((n, 1)), clipped), axis=1), axis=1)
    weights = np.empty((n, horizon), dtype=np.float64)
    log_ratio = np.zeros(n, dtype=np.float64)
    for h in range(horizon):
        weights[:, h] = np.exp(np.minimum(log_ratio, 0))
        probability = visited[:, h, actions[h]]
        denominator = probability[rollout_index]
        if denominator <= 0:
            raise ValueError("observed action has zero rollout probability")
        log_probability = np.full(n, -np.inf)
        np.log(probability, out=log_probability, where=probability > 0)
        log_ratio += log_probability - np.log(denominator)
    losses = (weights * (increments - increments[rollout_index])).sum(1)
    if np.any(np.abs(losses) > 1 + 1e-12):
        raise ArithmeticError("bounded comparison violated [-1,1]")
    return PrefixComparison(losses, increments, weights)


def exponential_weights(weights: np.ndarray, losses: np.ndarray) -> np.ndarray:
    """Algorithm 1 update with its FIXED eta=1/256, stable log normalization."""
    weights = _probabilities(weights, "policy weights")
    losses = np.asarray(losses, dtype=np.float64)
    if weights.ndim != 1 or losses.shape != weights.shape or np.any(weights <= 0):
        raise ValueError("positive policy weights and matching losses required")
    if not np.isfinite(losses).all() or np.any(np.abs(losses) > 1 + 1e-12):
        raise ValueError("comparison losses must be in [-1,1]")
    logits = np.log(weights) - LEARNING_RATE * losses
    unnormalized = np.exp(logits - logits.max())
    return unnormalized / unnormalized.sum()


@dataclass(frozen=True)
class OnlineResult:
    selected_index: int
    weights: np.ndarray
    weight_history: np.ndarray
    rollout_indices: np.ndarray
    losses: np.ndarray
    states: np.ndarray
    actions: np.ndarray
    teacher_query_count: int


def learn_online(mdp: FiniteMDP, policies: np.ndarray,
                 teacher_feedback: Callable[[int, int], np.ndarray], *,
                 episodes: int = 256, seed: int = 42) -> OnlineResult:
    """Algorithm 1: sample policy, execute full episode, update all candidates.

    No risk evaluator, best-policy index, gold trajectory, or teacher tensor is
    accepted by this interface. Feedback is queried exactly H times per episode.
    """
    policies = _policies(policies, mdp).copy()
    if not isinstance(episodes, int) or not 1 <= episodes <= 4096:
        raise ValueError("cost gate: 1 <= episode budget <= 4096")
    rng = np.random.default_rng(seed)
    n, horizon, _, _ = policies.shape
    weights = np.full(n, 1 / n)
    history = [weights.copy()]
    rollout_indices, observed_states, observed_actions, losses = [], [], [], []
    for _ in range(episodes):
        rollout = int(rng.choice(n, p=weights))
        state = int(rng.choice(mdp.states, p=mdp.initial))
        states, actions, feedback = [], [], []
        for h in range(horizon):
            states.append(state)
            observed = _probabilities(teacher_feedback(h, state), "teacher full feedback")
            if observed.shape != (mdp.actions,):
                raise ValueError("teacher must return the full action distribution")
            feedback.append(observed.copy())
            action = int(rng.choice(mdp.actions, p=policies[rollout, h, state]))
            actions.append(action)
            if h + 1 < horizon:
                state = int(rng.choice(mdp.states, p=mdp.transitions[h, state, action]))
        comparison = bounded_prefix_comparisons(policies, rollout, np.array(states),
                                                np.array(actions), np.array(feedback))
        weights = exponential_weights(weights, comparison.losses)
        rollout_indices.append(rollout)
        observed_states.append(states)
        observed_actions.append(actions)
        losses.append(comparison.losses)
        history.append(weights.copy())
    # np.argmax returns the first (smallest) candidate index on a tie.
    return OnlineResult(int(weights.argmax()), weights, np.array(history),
                        np.array(rollout_indices), np.array(losses),
                        np.array(observed_states), np.array(observed_actions), episodes * horizon)


def evaluate_exact_moments(mdp: FiniteMDP, policies: np.ndarray,
                           teacher: np.ndarray) -> dict[str, np.ndarray | float]:
    """EVALUATION ONLY: exact E[K], E[K^2] by finite-state forward recursion.

    These population values never enter learn_online. Teacher support is checked
    globally here (a conservative requirement at unreachable states is explicit).
    B=max(1,max E[K^2]/E[K]) verifies Assumption 2.1 for this finite fixture only.
    """
    policies = _policies(policies, mdp)
    teacher = _probabilities(teacher, "teacher policy")
    if teacher.shape != policies.shape[1:]:
        raise ValueError("teacher must have shape [H,S,A]")
    local_kl = local_reverse_kl(policies, teacher[None])
    risks, seconds = [], []
    for policy, local in zip(policies, local_kl, strict=True):
        mass = mdp.initial.copy()
        first = np.zeros(mdp.states)
        second = np.zeros(mdp.states)
        for h in range(mdp.horizon):
            updated_first = first + mass * local[h]
            updated_second = second + 2 * first * local[h] + mass * local[h] ** 2
            if h + 1 < mdp.horizon:
                kernel = (policy[h, :, :, None] * mdp.transitions[h]).sum(1)
                mass, first, second = mass @ kernel, updated_first @ kernel, updated_second @ kernel
            else:
                risks.append(updated_first.sum())
                seconds.append(updated_second.sum())
    risks, seconds = np.array(risks), np.array(seconds)
    ratios = np.divide(seconds, risks, out=np.zeros_like(risks), where=risks > 0)
    return {"risks": risks, "second_moments": seconds, "relative_second_moment_B": max(1., float(ratios.max()))}


def diagnostic(seed: int = 42) -> dict:
    """CPU-only Algorithm 1 fixture and post-training exact-population audit."""
    transition = np.zeros((2, 2, 2, 2))
    transition[:, :, 0, 0] = 1
    transition[:, :, 1, 1] = 1
    mdp = FiniteMDP(np.array([1., 0.]), transition)
    teacher = np.broadcast_to(np.array([[.85, .15], [.2, .8]]), (3, 2, 2)).copy()
    one_step_policies = np.array([[[.7, .3], [.3, .7]],
                                  [[.3, .7], [.7, .3]],
                                  [[.95, .05], [.1, .9]]])
    policies = np.repeat(one_step_policies[:, None], 3, axis=1)
    queries: list[tuple[int, int]] = []

    def feedback(h: int, state: int) -> np.ndarray:
        queries.append((h, state))
        return teacher[h, state]

    result = learn_online(mdp, policies, feedback, episodes=256, seed=seed)
    # Population risk audit begins only AFTER the learner returned its candidate.
    moments = evaluate_exact_moments(mdp, policies, teacher)
    replay = np.full(len(policies), 1 / len(policies))
    replay_error = 0.
    for t, loss in enumerate(result.losses):
        direct = replay * np.exp(-loss / 256)
        replay = direct / direct.sum()
        replay_error = max(replay_error, float(np.max(np.abs(replay - result.weight_history[t + 1]))))
    observed = [(h, int(state)) for episode in result.states for h, state in enumerate(episode)]
    checks = {"teacher_queries_only_visited_states": queries == observed,
              "full_episode_budget": len(result.rollout_indices) == 256 and len(queries) == 768,
              "bounded_comparisons": bool(np.max(np.abs(result.losses)) <= 1 + 1e-12),
              "rollout_self_comparison_zero": bool(np.max(np.abs(result.losses[np.arange(256), result.rollout_indices])) < 1e-14),
              "fixed_eta_exponential_weight_reference": replay_error < 1e-12,
              "final_argmax_not_risk_oracle": result.selected_index == int(result.weights.argmax()),
              "relative_second_moment_assumption": bool(np.all(moments["second_moments"] <= moments["relative_second_moment_B"] * moments["risks"] + 1e-12))}
    if not all(checks.values()):
        raise RuntimeError(f"RKL Algorithm 1 diagnostic failed: {checks}")
    return {"seed": seed, "checks": checks, "metrics": {
        "episodes": 256, "horizon": 3, "policy_count": 3, "teacher_queries": len(queries),
        "selected_index": result.selected_index,
        "selected_trajectory_reverse_kl": float(moments["risks"][result.selected_index]),
        "best_in_class_risk_evaluation_only": float(moments["risks"].min()),
        "relative_second_moment_B": float(moments["relative_second_moment_B"]),
        "exponential_weight_replay_max_abs_error": replay_error,
        "max_abs_comparison_loss": float(np.max(np.abs(result.losses)))}}
