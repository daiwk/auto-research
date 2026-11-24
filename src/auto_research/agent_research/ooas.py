"""OOAS Algorithm1/2 CPU bandit kernel, arXiv:2611.30405v1.

Hints and terminal aggregate rewards are explicit inputs. No coding agent,
activation probe, turn-level reward vector, gold answer or plan is available.
The theorem assumes oblivious rewards/hints/task partition; stateful LLM-agent
rollouts do not automatically satisfy that assumption.
"""
from __future__ import annotations

import math
import random

REQUIRES_GPU_VALIDATION = False


def _real(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("finite real scalar required")
    return float(value)


def _vector(values, *, size=None):
    if not isinstance(values, (tuple, list)) or not values:
        raise ValueError("explicit nonempty vector required")
    result = tuple(_real(value) for value in values)
    if size is not None and len(result) != size:
        raise ValueError("vector width mismatch")
    return result


def _probabilities(values, *, size=None):
    p = _vector(values, size=size)
    if len(p) < 2 or min(p) <= 0 or not math.isclose(math.fsum(p), 1., abs_tol=1e-12):
        raise ValueError("strictly positive simplex vector required")
    return p


def regularizer(probabilities, alpha, beta):
    p, a, b = _probabilities(probabilities), _real(alpha), _real(beta)
    if a <= 0 or b <= 0:
        raise ValueError("positive regularization coefficients required")
    value = (2*a*(math.sqrt(len(p))-math.fsum(math.sqrt(x) for x in p))
             + b*math.fsum(-math.log(len(p)*x) for x in p))
    return _real(value)


def ftrl_distribution(scores, alpha, beta):
    """Solve the strictly concave Tsallis-plus-barrier map by KKT bisection.

    At the optimum G_k + alpha/sqrt(p_k) + beta/p_k = multiplier.
    Translation of all scores leaves the result unchanged. This solves that
    map rather than substituting softmax/EXP3 for the defining regularizer.
    """
    g, a, b = _vector(scores), _real(alpha), _real(beta)
    if len(g) < 2 or len(g) > 128 or a <= 0 or b <= 0:
        raise ValueError("2..128 arms and positive coefficients required")
    shift = max(g)
    relative = tuple(_real(value-shift) for value in g)
    high = _real(a*math.sqrt(len(g)) + b*len(g))
    low = 0.

    def probabilities(multiplier):
        result = []
        for value in relative:
            delta = multiplier-value
            if delta <= 0:
                raise ValueError("invalid KKT root bracket")
            root = math.hypot(a, 2*math.sqrt(b)*math.sqrt(delta))
            direction = (a+root)/(2*delta)
            result.append(_real(direction*direction))
        return tuple(result)

    for _ in range(100):
        middle = low+(high-low)/2
        if math.fsum(probabilities(middle)) > 1:
            low = middle
        else:
            high = middle
    p = probabilities(high)
    total = math.fsum(p)
    if not math.isclose(total, 1., rel_tol=1e-10, abs_tol=1e-12):
        raise ValueError("FTRL simplex solver did not converge")
    # Remove only roundoff in the numerical root, not a heuristic projection.
    return _probabilities(tuple(value/total for value in p))


def potential(scores, alpha, beta):
    g = _vector(scores)
    p = ftrl_distribution(g, alpha, beta)
    return _real(math.fsum(x*y for x, y in zip(g, p, strict=True))-regularizer(p, alpha, beta))


def constant_arm_probabilities(probability_path):
    """Exact probabilities of an arm winning EVERY turn under shared Exp noise."""
    if not isinstance(probability_path, (list, tuple)) or not probability_path:
        raise ValueError("nonempty probability path required")
    path = tuple(_probabilities(row) for row in probability_path)
    arms = len(path[0])
    if any(len(row) != arms for row in path):
        raise ValueError("path width mismatch")
    result = []
    for k in range(arms):
        denominator = _real(math.fsum(max(row[j]/row[k] for row in path) for j in range(arms)))
        rho = _real(1/denominator)
        if rho <= 0:
            raise ValueError("constant-arm importance probability underflow")
        result.append(rho)
    return tuple(result)


def aggregate_residual(hints, probability_path, actions, aggregate_reward):
    """Algorithm1 lines10--14; never accepts unobserved per-turn rewards."""
    if not isinstance(hints, (list, tuple)) or not hints:
        raise ValueError("nonempty explicit hints required")
    rows = tuple(_vector(row) for row in hints)
    arms = len(rows[0])
    if any(len(row) != arms or min(row) < 0 or max(row) > 1 for row in rows):
        raise ValueError("aligned hints in [0,1] required")
    if len(probability_path) != len(rows) or len(actions) != len(rows):
        raise ValueError("aligned path and action count required")
    rho = constant_arm_probabilities(probability_path)
    if len(rho) != arms or any(type(k) is not int or not 0 <= k < arms for k in actions):
        raise ValueError("valid arm choices required")
    reward = _real(aggregate_reward)
    if not 0 <= reward <= len(rows):
        raise ValueError("terminal aggregate must lie in [0, task length]")
    mass = tuple(math.fsum(row[k] for row in rows) for k in range(arms))
    residual = _real(reward-math.fsum(row[k] for row, k in zip(rows, actions, strict=True)))
    correction = [0.]*arms
    if len(set(actions)) == 1:
        arm = actions[0]
        correction[arm] = _real(residual/rho[arm])
    return mass, tuple(correction), residual, rho


class OptimisticSteering:
    """Sequential task API with task-shared noise and optional Algorithm2 restarts.

    `choose` sees only this turn's hints and past completed-task feedback.
    `finish` receives one terminal aggregate. Pending state cannot cross tasks.
    Injected noise exists for controlled mathematical tests, not model outputs.
    """

    def __init__(self, arms, max_task_length, *, seed=42, alpha=None):
        if (type(arms) is not int or not 2 <= arms <= 128 or type(max_task_length) is not int
                or not 1 <= max_task_length <= 10000 or type(seed) is not int or seed < 0):
            raise ValueError("bounded arm/task sizes and nonnegative seed required")
        self.arms, self.max_task_length = arms, max_task_length
        self.beta = float(6*max_task_length)
        self.adaptive = alpha is None
        self.threshold = float(4*self.beta*arms)
        self.alpha = self.threshold/(4*math.sqrt(arms)) if self.adaptive else _real(alpha)
        if self.alpha <= 0:
            raise ValueError("positive fixed alpha required")
        self.score = (0.,)*arms
        self.signed_gap = 0.
        self.rng = random.Random(seed)
        self._active = False

    def begin(self, *, noise=None):
        if self._active:
            raise ValueError("finish pending task before starting another")
        generated = tuple(self.rng.expovariate(1.) for _ in range(self.arms)) if noise is None else noise
        self._noise = _vector(generated, size=self.arms)
        if min(self._noise) <= 0:
            raise ValueError("positive shared exponential samples required")
        self._hints, self._path, self._actions = [], [], []
        self._active = True

    def choose(self, hint):
        if not self._active or len(self._hints) >= self.max_task_length:
            raise ValueError("active task within its declared length bound required")
        m = _vector(hint, size=self.arms)
        if min(m) < 0 or max(m) > 1:
            raise ValueError("hints must lie in [0,1]")
        turn = len(self._hints)+1
        provisional = tuple(_real(self.score[k]+math.fsum(row[k] for row in self._hints)+turn*m[k])
                            for k in range(self.arms))
        p = ftrl_distribution(provisional, self.alpha, self.beta)
        arm = min(range(self.arms), key=lambda k: (self._noise[k]/p[k], k))
        self._hints.append(m)
        self._path.append(p)
        self._actions.append(arm)
        return arm, p

    def finish(self, aggregate_reward):
        if not self._active or not self._hints:
            raise ValueError("nonempty active task required")
        m, d, z, rho = aggregate_residual(self._hints, self._path, self._actions, aggregate_reward)
        updated = tuple(_real(g+x+y) for g, x, y in zip(self.score, m, d, strict=True))
        hint_value = math.fsum(math.fsum(p*x for p, x in zip(prob, hint, strict=True))
                               for prob, hint in zip(self._path, self._hints, strict=True))
        gap = _real(potential(updated, self.alpha, self.beta)-potential(self.score, self.alpha, self.beta)-hint_value-z)
        restart = self.adaptive and self.signed_gap+gap > self.threshold
        if restart:
            self.threshold = _real(2*self.threshold)
            self.score, self.signed_gap = (0.,)*self.arms, 0.
            self.alpha = self.threshold/(4*math.sqrt(self.arms))
        else:
            self.score = updated
            self.signed_gap = _real(self.signed_gap+gap)
        self._active = False
        return {"hint_mass": m, "correction": d, "residual": z, "rho": rho,
                "gap": gap, "restart": bool(restart), "actions": tuple(self._actions),
                "probabilities": tuple(self._path)}


def diagnostic(seed=42, device="cpu"):
    if device != "cpu":
        raise ValueError("CPU-only numerical component")
    learner = OptimisticSteering(3, 4, seed=seed)
    learner.begin()
    rewards = []
    # The evaluator sums an explicit synthetic reward after choices. It never
    # provides the learner's API with a turn reward or a full reward vector.
    for hint in ((.8, .2, .4), (.7, .3, .5), (.9, .1, .4)):
        arm, _ = learner.choose(hint)
        rewards.append((.9, .1, .5)[arm])
    trace = learner.finish(math.fsum(rewards))
    p = ftrl_distribution((1., 2., -1.), 3., 6.)
    kkt = tuple(g+3/math.sqrt(x)+6/x for g, x in zip((1., 2., -1.), p, strict=True))
    same = constant_arm_probabilities((p, p))
    _, correction, _, _ = aggregate_residual(((.2, .8), (.8, .2)), ((.4, .6), (.6, .4)), (0, 1), 1.)
    checks = {
        "ftrl_kkt_residual_small": max(kkt)-min(kkt) < 1e-10,
        "ftrl_not_softmax_substitute": not math.isclose(p[0]/p[1], math.exp(-1)),
        "constant_distribution_all_task_probability": max(abs(a-b) for a, b in zip(p, same, strict=True)) < 1e-12,
        "switching_task_has_no_residual_correction": correction == (0., 0.),
        "strictly_positive_turn_probabilities": all(min(row) > 0 for row in trace["probabilities"]),
        "completed_task_is_not_pending": not learner._active,
        "translation_invariant_ftrl": max(abs(a-b) for a, b in zip(p, ftrl_distribution((101., 102., 99.), 3., 6.), strict=True)) < 1e-12,
    }
    return {"seed": seed, "device": "cpu", "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"arms": 3, "turns": 3, "kkt_residual": max(kkt)-min(kkt),
                                           "potential_gap": trace["gap"], "task_residual": trace["residual"]},
            "agent_evaluation_executed": False, "activation_steering_executed": False}
