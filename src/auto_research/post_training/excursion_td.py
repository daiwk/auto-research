"""Excursion TD / truncated Ex-Retrace (2611.13275), CPU tabular reference.

Eqs. 11 and 28--31, with the paper's 5-state/3-action random-MDP protocol.
No continuous-control actor, replay trainer or neural-network result is implied.
"""
from __future__ import annotations

import math
import numpy as np

REQUIRES_GPU_VALIDATION = False


def _unit(value: float, name: str) -> None:
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} must be in [0,1]")


def excursion_weights(ratios: np.ndarray, beta: float, *, clip: float | None = None) -> np.ndarray:
    """C[t,k] = (1-beta) + beta*rho[t]*C[t+1,k], C[k+1,k]=1.

    Rows/columns use a single trajectory's zero-based transition indices. This
    is a MIXTURE over excursion durations, not a product of mixed policies.
    """
    ratios = np.asarray(ratios, dtype=np.float64)
    _unit(beta, "beta")
    if ratios.ndim != 1 or ratios.size == 0 or not np.isfinite(ratios).all() or np.any(ratios < 0):
        raise ValueError("nonempty finite nonnegative ratio vector required")
    if clip is not None:
        if not math.isfinite(clip) or clip <= 0:
            raise ValueError("positive finite clip required")
        ratios = np.minimum(ratios, clip)
    result = np.zeros((ratios.size, ratios.size), dtype=np.float64)
    for k in range(ratios.size):
        tail = 1.
        for t in range(k, -1, -1):
            tail = (1 - beta) + beta * ratios[t] * tail
            result[t, k] = tail
    return result


def ex_retrace_targets(q: np.ndarray, states: np.ndarray, actions: np.ndarray, rewards: np.ndarray,
                      target: np.ndarray, behavior: np.ndarray, *, gamma: float = .9,
                      trace_lambda: float = 1., beta: float = .5, rho_bar: float = 1.) -> np.ndarray:
    """Truncated sample target, Eqs. 29--31; q and both policies are frozen.

    ``states`` includes the final next state. Rewards are deterministic/sample
    realized transitions, not gold action labels. Return one target per start.
    """
    q, target, behavior = (np.asarray(x, dtype=np.float64) for x in (q, target, behavior))
    states, actions, rewards = np.asarray(states), np.asarray(actions), np.asarray(rewards, dtype=np.float64)
    _validate_policies(target, behavior)
    for v, name in ((gamma, "gamma"), (trace_lambda, "lambda"), (beta, "beta")):
        _unit(v, name)
    if not math.isfinite(rho_bar) or rho_bar <= 0 or q.shape != target.shape or not np.isfinite(q).all():
        raise ValueError("finite aligned Q and positive clip required")
    n = actions.size
    if actions.ndim != 1 or n < 1 or states.shape != (n + 1,) or rewards.shape != (n,) or not np.isfinite(rewards).all():
        raise ValueError("states[N+1], actions[N], rewards[N] required")
    if states.dtype.kind not in "iu" or actions.dtype.kind not in "iu" or np.any(states < 0) or np.any(states >= q.shape[0]) or np.any(actions < 0) or np.any(actions >= q.shape[1]):
        raise ValueError("valid integer states and actions required")
    ratios = np.minimum(target[states[:-1], actions] / behavior[states[:-1], actions], rho_bar)
    bootstrap_mu, bootstrap_pi = (q * behavior).sum(-1), (q * target).sum(-1)
    delta_mu = rewards + gamma * bootstrap_mu[states[1:]] - q[states[:-1], actions]
    delta_pi = rewards + gamma * bootstrap_pi[states[1:]] - q[states[:-1], actions]
    result = q[states[:-1], actions].copy()
    for t in range(n):
        prefix, prefix_sum = 1., 1.
        for k in range(t, n):
            if k > t:
                prefix *= beta * ratios[k]
                prefix_sum += prefix
            mixed_delta = (1 - beta) * prefix_sum * delta_mu[k] + beta * prefix * delta_pi[k]
            result[t] += (gamma * trace_lambda) ** (k - t) * mixed_delta
    return result


def _validate_policies(target: np.ndarray, behavior: np.ndarray) -> None:
    if target.ndim != 2 or min(target.shape) < 1 or target.shape != behavior.shape or not np.isfinite(target).all() or not np.isfinite(behavior).all():
        raise ValueError("finite aligned [state,action] policies required")
    if np.any(target < 0) or np.any(behavior <= 0) or not np.allclose(target.sum(-1), 1.) or not np.allclose(behavior.sum(-1), 1.):
        raise ValueError("normalized policies and full-support behavior required")


def expected_operator(transitions: np.ndarray, rewards: np.ndarray, target: np.ndarray, behavior: np.ndarray,
                      *, horizon: int, gamma: float = .9, trace_lambda: float = 1.,
                      beta: float = .5, rho_bar: float = 1.) -> tuple[np.ndarray, np.ndarray]:
    """Exact finite-MDP affine operator RQ = offset + matrix @ Q.flatten().

    A clipped prefix follows P_c; after the excursion ends, the remaining
    suffix follows P_mu. This preserves duration mixing rather than replacing
    the whole history by a per-action mixture policy.
    """
    transitions, rewards, target, behavior = (np.asarray(x, dtype=np.float64) for x in (transitions, rewards, target, behavior))
    _validate_policies(target, behavior)
    s, a = target.shape
    if transitions.shape != (s, a, s) or rewards.shape != (s, a) or not np.isfinite(transitions).all() or not np.isfinite(rewards).all() or np.any(transitions < 0) or not np.allclose(transitions.sum(-1), 1.):
        raise ValueError("stochastic P[state,action,next] and finite mean rewards required")
    if type(horizon) is not int or horizon < 1 or not math.isfinite(rho_bar) or rho_bar <= 0:
        raise ValueError("positive integer horizon and clip required")
    for v, name in ((gamma, "gamma"), (trace_lambda, "lambda"), (beta, "beta")):
        _unit(v, name)
    n = s * a
    p_mu = (transitions[..., None] * behavior[None, None, :, :]).reshape(n, n)
    p_pi = (transitions[..., None] * target[None, None, :, :]).reshape(n, n)
    p_c = (transitions[..., None] * np.minimum(target, rho_bar * behavior)[None, None, :, :]).reshape(n, n)
    eye = np.eye(n)
    offset, matrix = np.zeros(n), eye.copy()
    powers_mu = [np.linalg.matrix_power(p_mu, i) for i in range(horizon)]
    powers_c = [np.linalg.matrix_power(p_c, i) for i in range(horizon)]
    for d in range(horizon):
        mu_weight = (1 - beta) * sum(beta ** j * powers_c[j] @ powers_mu[d - j] for j in range(d + 1))
        pi_weight = beta ** (d + 1) * powers_c[d]
        discount = (gamma * trace_lambda) ** d
        offset += discount * (mu_weight + pi_weight) @ rewards.reshape(n)
        matrix += discount * (mu_weight @ (gamma * p_mu - eye) + pi_weight @ (gamma * p_pi - eye))
    return offset, matrix


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """A real small random MDP, not a hardcoded score or neural RL benchmark."""
    if device != "cpu":
        raise ValueError("tabular excursion reference is CPU-only")
    rng = np.random.default_rng(seed)
    states, actions, horizon, gamma = 5, 3, 6, .9
    transitions = rng.dirichlet(np.ones(states), size=(states, actions))
    behavior = rng.dirichlet(np.ones(actions), size=states)
    target = rng.dirichlet(np.ones(actions), size=states)
    rewards = rng.uniform(0., 1., size=(states, actions))
    offset, matrix = expected_operator(transitions, rewards, target, behavior, horizon=horizon, gamma=gamma, beta=.5)
    fixed = np.linalg.solve(np.eye(states * actions) - matrix, offset)
    p_pi = (transitions[..., None] * target[None, None, :, :]).reshape(states * actions, -1)
    q_pi = np.linalg.solve(np.eye(states * actions) - gamma * p_pi, rewards.ravel())
    # beta=0 is an N-step behavior return in expectation, with contraction gamma^N.
    offset_zero, matrix_zero = expected_operator(transitions, rewards, target, behavior, horizon=horizon, gamma=gamma, beta=0.)
    p_mu = (transitions[..., None] * behavior[None, None, :, :]).reshape(states * actions, -1)
    q_mu = np.linalg.solve(np.eye(states * actions) - gamma * p_mu, rewards.ravel())
    # At beta=1 the target-policy value is the fixed point (clipped Retrace).
    offset_one, matrix_one = expected_operator(transitions, rewards, target, behavior, horizon=horizon, gamma=gamma, beta=1.)
    # Actual sampled transition, checked against an independent scalar expansion.
    path_states = [int(rng.integers(states))]; path_actions, path_rewards = [], []
    for _ in range(horizon):
        s = path_states[-1]; a = int(rng.choice(actions, p=behavior[s]))
        path_actions.append(a); path_rewards.append(rewards[s, a])
        path_states.append(int(rng.choice(states, p=transitions[s, a])))
    q = fixed.reshape(states, actions)
    values = ex_retrace_targets(q, np.array(path_states), np.array(path_actions), np.array(path_rewards), target, behavior, gamma=gamma)
    # The affine fixed-point operator is independently iterated from zero.
    iterate = np.zeros_like(fixed)
    for _ in range(100):
        iterate = offset + matrix @ iterate
    ratios = np.array([2., .25, 1.5])
    mixed = excursion_weights(ratios, .5)[0, 2]
    duration_reference = .5 + .25 * ratios[0] + .125 * ratios[0] * ratios[1] + .125 * np.prod(ratios)
    checks = {
        "duration_mixture_not_action_mixture": bool(np.isclose(mixed, duration_reference)),
        "beta_zero_n_step_contraction": bool(np.isclose(np.max(np.abs(matrix_zero).sum(-1)), gamma ** horizon)),
        "beta_zero_behavior_fixed_point": bool(np.allclose(offset_zero + matrix_zero @ q_mu, q_mu)),
        "beta_one_target_fixed_point": bool(np.allclose(offset_one + matrix_one @ q_pi, q_pi)),
        "actual_random_mdp_operator_converges": bool(np.max(np.abs(iterate - fixed)) < 1e-7),
        "sampled_targets_finite": bool(np.isfinite(values).all()),
    }
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"states": states, "actions": actions, "horizon": horizon, "contraction_sup_norm": float(np.max(np.abs(matrix).sum(-1))), "fixed_point_target_bias_mse": float(np.mean((fixed - q_pi) ** 2)), "operator_iteration_error": float(np.max(np.abs(iterate - fixed))), "sampled_initial_target": float(values[0])}, "checks": checks}
