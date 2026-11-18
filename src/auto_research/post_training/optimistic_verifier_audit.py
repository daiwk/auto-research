"""Exact finite-domain minimal sufficient reasons and model-free proxy audit.

Gold policy oracle is an external evaluator, never an evaluated Agent input.
"""

from __future__ import annotations
from itertools import combinations, product
import math
from ._nov18_contracts import receipt, scalar

REQUIRES_GPU_VALIDATION = False


def minimal_sufficient_reasons(domains, context, gate, *, maximum_states=4096):
    values = tuple(tuple(d) for d in domains)
    c = tuple(context)
    if (
        not values
        or len(c) != len(values)
        or any(not d or c[i] not in d for i, d in enumerate(values))
    ):
        raise ValueError("nonempty finite domains and a valid context required")
    if (
        type(maximum_states) is not int
        or maximum_states < 1
        or math.prod(map(len, values)) > maximum_states
    ):
        raise ValueError("explicit small-enumeration budget exceeded")
    states = tuple(product(*values))
    decisions = {s: gate(s) for s in states}
    if any(type(x) is not bool for x in decisions.values()):
        raise ValueError("gate must return a Boolean decision")
    reasons = []
    for size in range(len(c) + 1):
        for items in combinations(range(len(c)), size):
            subset = frozenset(items)
            if any(r <= subset for r in reasons):
                continue
            if all(
                decisions[s] == decisions[c] for s in states if all(s[i] == c[i] for i in subset)
            ):
                reasons.append(subset)
    return tuple(reasons)


def exact_reward(
    citations,
    reasons,
    *,
    length_violation=False,
    wrong_decision=False,
    length_penalty=0,
    decision_penalty=0,
):
    e = frozenset(citations)
    rs = tuple(frozenset(r) for r in reasons)
    if not rs or any(type(i) is not int or i < 0 for i in e | frozenset().union(*rs)):
        raise ValueError("nonempty MSR antichain and nonnegative feature IDs required")
    if any(a != b and a <= b for a in rs for b in rs):
        raise ValueError("reasons must be subset-minimal antichain")
    if type(length_violation) is not bool or type(wrong_decision) is not bool:
        raise ValueError("Boolean penalties required")
    lp = scalar(length_penalty, "length_penalty", lower=0)
    dp = scalar(decision_penalty, "decision_penalty", lower=0)
    union = frozenset().union(*rs)
    precision = len(e & union) / len(e) if e else 0.0
    recall = max(len(e & r) / len(r) if r else 1.0 for r in rs)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "reward": f1 - lp * length_violation - dp * wrong_decision,
    }


def proxy_audit(true_rewards, proxy_rewards):
    truth = tuple(true_rewards)
    proxy = tuple(proxy_rewards)
    if (
        len(truth) != len(proxy)
        or not truth
        or any(
            isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
            for v in truth + proxy
        )
    ):
        raise ValueError("matching finite reward vectors required")
    errors = []
    for i in range(len(truth)):
        for j in range(i):
            if truth[i] == truth[j]:
                continue
            sign = (truth[i] - truth[j]) * (proxy[i] - proxy[j])
            errors.append(1.0 if sign < 0 else 0.5 if sign == 0 else 0.0)
    if not errors:
        raise ValueError("selection error undefined without unequal true rewards")
    return {
        "selection_error": sum(errors) / len(errors),
        "signed_gap": sum(p - t for p, t in zip(proxy, truth)) / len(truth),
        "absolute_gap": sum(abs(p - t) for p, t in zip(proxy, truth)) / len(truth),
    }


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("CPU exact oracle requires integer seed")
    rs = minimal_sufficient_reasons([(0, 1)] * 3, (1, 1, 0), lambda x: bool(x[0] or x[1]))
    faithful = exact_reward([0], rs)
    padded = exact_reward([0, 1, 2], rs)
    audit = proxy_audit([faithful["reward"], padded["reward"]], [1.0, 1.0])
    return receipt(
        seed,
        "l1_mechanism",
        {
            "alternative_minimal_reasons": set(rs) == {frozenset([0]), frozenset([1])},
            "irrelevant_padding_reduces_precision": padded["precision"] < faithful["precision"],
            "sufficiency_tie_hides_true_preference": audit["selection_error"] == 0.5,
            "irrelevant_feature_is_not_a_reason": all(2 not in r for r in rs),
        },
        {"faithful_reward": faithful["reward"], "padded_reward": padded["reward"], **audit},
    )
