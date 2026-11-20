"""Meta fleet feature paper: explicit FI blending, trimming and admission.

No LLM proposer, FI estimator, model training or production launch is executed.
Set-dependent pipeline costs remain caller-supplied, not additive proxies.
"""

from __future__ import annotations

import math
import random

REQUIRES_GPU_VALIDATION = False


def _number(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError("finite numerical value required")
    return float(x)


def pareto_fronts(importance):
    """All nondominated layers; ties remain together, without invented tie cuts."""
    if not importance:
        raise ValueError("nonempty feature importance required")
    values = {k: tuple(_number(v) for v in row) for k, row in importance.items()}
    width = len(next(iter(values.values())))
    if not width or any(len(v) != width for v in values.values()):
        raise ValueError("same nonempty task dimensions required")
    pending = list(values)
    fronts = []
    while pending:
        front = [
            i for i in pending
            if not any(
                all(a >= b for a, b in zip(values[j], values[i], strict=True))
                and any(a > b for a, b in zip(values[j], values[i], strict=True))
                for j in pending if j != i
            )
        ]
        fronts.append(front)
        pending = [i for i in pending if i not in front]
    return fronts


def blend_sources(rankings, quotas, *, banned=()):
    """Fixed source order, skipping selected/banned IDs.

    Integer round(pi*N) quotas and within-front tie order are explicit inputs:
    the paper does not specify their rounding/tie conventions. Exhaustion is
    reported; no silent padding or quota renormalization is invented.
    """
    if len(rankings) != len(quotas) or not rankings:
        raise ValueError("one quota per ordered source required")
    if any(type(q) is not int or q < 0 for q in quotas):
        raise ValueError("nonnegative integer quotas required")
    selected, contributions = [], []
    blocked = set(banned)
    for ranking, quota in zip(rankings, quotas, strict=True):
        if len(set(ranking)) != len(ranking):
            raise ValueError("a ranking must not duplicate feature IDs")
        count = 0
        for feature in ranking:
            if count == quota:
                break
            if feature not in selected and feature not in blocked:
                selected.append(feature)
                count += 1
        contributions.append(count)
    return {"selected": selected, "contributions": contributions,
            "quota_exhausted": contributions != list(quotas)}


def pipeline_delta(incumbent, proposed, other_models, cost):
    """Change in a shared budget using its actual set-cost oracle."""
    others = set().union(*(set(x) for x in other_models))
    old = _number(cost(others | set(incumbent)))
    new = _number(cost(others | set(proposed)))
    if old < 0 or new < 0:
        raise ValueError("nonnegative pipeline cost required")
    return new - old


def trim_additions(selected, incumbent, already_used, category, rankings,
                   removal_order, within_budget, *, banned=()):
    """Paper's remove/refill primitive, not a feature/LLM optimizer.

    Costliest-addition order is supplied by the real budget service because
    cross-budget ordering is not specified in the paper. Failure is explicit.
    """
    result = list(selected)
    if len(set(result)) != len(result) or any(x not in category for x in result):
        raise ValueError("unique categorized selection required")
    if set(result) & set(banned):
        raise ValueError("selection contains banned features")
    if len(set(removal_order)) != len(removal_order):
        raise ValueError("duplicate removal priority")
    additions = set(result) - set(incumbent)
    if set(removal_order) != additions:
        raise ValueError("exact cost-ordered additions required")
    available = set(already_used) | set(incumbent)
    changes = []
    for feature in removal_order:
        allowed = within_budget(frozenset(result))
        if type(allowed) is not bool:
            raise ValueError("budget oracle must return bool")
        if allowed:
            break
        group = category[feature]
        replacement = next((x for x in rankings[group]
                            if x in available and x not in result and x not in banned
                            and category.get(x) == group), None)
        if replacement is None:
            return {"selection": result, "feasible": False,
                    "reason": "no_already_used_same_category_refill", "changes": changes}
        result[result.index(feature)] = replacement
        changes.append((feature, replacement))
    feasible = within_budget(frozenset(result))
    if type(feasible) is not bool:
        raise ValueError("budget oracle must return bool")
    return {"selection": result, "feasible": feasible,
            "reason": "within_budget" if feasible else "budget_still_violated", "changes": changes}


def choose_winner(trials, baseline_ne, caps):
    """Lowest completed feasible validation NE with strict improvement.

    This is an admission primitive. The caller must enforce Algorithm1's
    all-K-trials-terminal barrier before using it for a final search decision.
    """
    baseline_ne = _number(baseline_ne)
    caps = {k: _number(v) for k, v in caps.items()}
    if not caps or baseline_ne < 0 or any(v <= 0 for v in caps.values()):
        raise ValueError("positive upper-bound resource caps required")
    winners = []
    for trial in trials:
        if trial.get("status") != "completed":
            continue
        ne = _number(trial["validation_ne"])
        resources = trial["resources"]
        if set(resources) != set(caps):
            raise ValueError("exact resource contract required; QPS must be inverted upstream")
        resources = {k: _number(v) for k, v in resources.items()}
        if any(v < 0 for v in resources.values()) or ne < 0:
            raise ValueError("nonnegative measured values required")
        if ne < baseline_ne and all(resources[k] <= caps[k] for k in caps):
            winners.append(trial)
    return min(winners, key=lambda x: x["validation_ne"]) if winners else None


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU protocol required")
    scale = random.Random(seed).uniform(1, 3)
    fronts = pareto_fronts({"a": [4*scale, 1], "b": [1*scale, 4], "c": [0, 0]})
    blended = blend_sources([["a", "b"], ["a", "c"]], [1, 1])
    trim = trim_additions(["expensive"], ["old"], [],
                          {"old": "sparse", "expensive": "sparse"},
                          {"sparse": ["expensive", "old"]}, ["expensive"],
                          lambda s: "expensive" not in s)
    winner = choose_winner([
        {"id": "unsafe", "status": "completed", "validation_ne": .1, "resources": {"inverse_qps": 2}},
        {"id": "safe", "status": "completed", "validation_ne": .6, "resources": {"inverse_qps": 1}},
    ], .7, {"inverse_qps": 1.2})
    checks = {"single_task_extremes_kept": set(fronts[0]) == {"a", "b"},
              "dominated_later": fronts[1] == ["c"],
              "sources_skip_duplicates": blended["selected"] == ["a", "c"],
              "counts_preserved_by_trim": trim["selection"] == ["old"] and trim["feasible"],
              "unsafe_lower_ne_rejected": winner["id"] == "safe",
              "already_used_adds_zero_cost": pipeline_delta([], ["a"], [["a"]], len) == 0}
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": checks, "metrics": {"pareto_front_count": len(fronts),
                                           "blend_unique_count": len(blended["selected"]),
                                           "trim_replacements": len(trim["changes"])}}
