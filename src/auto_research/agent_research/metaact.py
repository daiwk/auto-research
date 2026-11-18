"""MetaAct offline replay gate and two exact deterministic primitive slices.

No LLM specification synthesis, goal extractor menu, embodied environment, or
online win-rate retirement is supplied. Guard inputs contain only pre-action
observations/history; success/score labels are evaluator-only replay metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable, Sequence
import math

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class View:
    history: tuple[tuple[str, str], ...] = ()
    done_options: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Spec:
    primitive: str
    message: str
    action_class: str = "click"
    navigation_options: frozenset[str] = frozenset()

    def __post_init__(self):
        if self.primitive not in {"no_op_repeat", "idempotence_block"}:
            raise ValueError("only the two independently verified primitive slices are supported")
        if not self.message or not isinstance(self.action_class, str):
            raise ValueError("typed action class and nonempty trigger message required")
        if not isinstance(self.navigation_options, frozenset):
            raise TypeError("navigation options must be immutable")


def compile_guards(specs: Sequence[Spec]) -> Callable[[View, str], bool]:
    """Return admissibility (True=allow); conjunction implements constraint union."""
    rules = tuple(specs)
    if any(not isinstance(s, Spec) for s in rules):
        raise TypeError("typed specifications required")

    def allow(view: View, action: str) -> bool:
        for spec in rules:
            if spec.primitive == "no_op_repeat":
                h = view.history
                if len(h) >= 2 and action and action == h[-1][0] and h[-1][1] == h[-2][1]:
                    return False
            else:
                a, cls = action.strip().lower(), spec.action_class.lower()
                if cls and not a.startswith(cls):
                    continue
                prefix = cls + "["
                option = (
                    a[len(prefix) : -1].strip() if a.startswith(prefix) and a.endswith("]") else a
                )
                if option not in spec.navigation_options and option in view.done_options:
                    return False
        return True

    return allow


@dataclass(frozen=True)
class Event:
    action: str
    view: View
    effective: bool
    wasted: bool = False

    def __post_init__(self):
        if type(self.effective) is not bool or type(self.wasted) is not bool:
            raise TypeError("replay annotations are strict bools")


@dataclass(frozen=True)
class Episode:
    events: tuple[Event, ...]
    success: bool
    score: float

    def __post_init__(self):
        if (
            type(self.success) is not bool
            or isinstance(self.score, bool)
            or not math.isfinite(self.score)
            or not self.events
        ):
            raise ValueError("nonempty annotated episode required")


def replay_report(
    specs: Sequence[Spec], episodes: Sequence[Episode], *, minimum_reference_score: float
) -> dict:
    """Eq2–5, with undefined evidence rejected rather than silently zero-filled.

    ok is the fraction of successful trajectories containing any block. Replay
    is counterfactual blocking only, not a claim of improved downstream reward.
    """
    if isinstance(minimum_reference_score, bool) or not math.isfinite(minimum_reference_score):
        raise ValueError("explicit finite safety-reference score threshold required")
    failures = [e for e in episodes if not e.success]
    successes = [e for e in episodes if e.success]
    if not failures or not successes:
        raise ValueError("both failed and successful replay evidence required")
    guard = compile_guards(specs)
    blocked = []
    for episode in episodes:
        verdicts = tuple(guard(event.view, event.action) for event in episode.events)
        if any(type(v) is not bool for v in verdicts):
            raise TypeError("deterministic guard must return strict bool")
        blocked.append(tuple(not x for x in verdicts))
    failure_hits = success_hits = effective = effective_blocks = wasted = wasted_blocks = 0
    for ep, masks in zip(episodes, blocked):
        if not ep.success:
            failure_hits += any(masks)
        else:
            success_hits += any(masks)
        for event, block in zip(ep.events, masks):
            if (ep.success or ep.score >= minimum_reference_score) and event.effective:
                effective += 1
                effective_blocks += block
            if not ep.success and event.wasted:
                wasted += 1
                wasted_blocks += block
    if effective == 0 or wasted == 0:
        raise ValueError("effective safety actions and annotated wasted failure steps required")
    coverage = failure_hits / len(failures)
    eff, ok, rho = (
        effective_blocks / effective,
        success_hits / len(successes),
        wasted_blocks / wasted,
    )
    return {
        "coverage": coverage,
        "effective_block_rate": eff,
        "success_block_rate": ok,
        "wasted_recall": rho,
        "objective": 0.5 * rho + 0.5 * coverage - 2 * eff - 2 * ok,
        "accepted": coverage >= 0.3 and eff <= 0.15 and ok <= 0.10,
        "search_stop": coverage >= 0.3 and eff <= 0.15 and ok <= 0.10 and rho >= 0.8,
    }


def select_union(
    incumbent: Sequence[Spec],
    proposal: Sequence[Spec],
    episodes: Sequence[Episode],
    *,
    minimum_reference_score: float,
) -> dict:
    candidates = (tuple(incumbent), tuple(proposal), tuple(dict.fromkeys((*incumbent, *proposal))))
    reports = [
        replay_report(s, episodes, minimum_reference_score=minimum_reference_score)
        for s in candidates
    ]
    # Fixed input-order ties preserve the incumbent; no test trajectory is read.
    index = max(range(3), key=lambda i: reports[i]["objective"])
    return {"specs": candidates[index], "report": reports[index], "candidate_index": index}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    spec = Spec("no_op_repeat", "Choose a different action")
    stagnant = View((("look", "same"), ("look", "same")))
    episodes = (
        Episode((Event("look", stagnant, False, True),), False, 0),
        Episode((Event("finish", View(), True),), True, 1),
    )
    report = replay_report((spec,), episodes, minimum_reference_score=0.5)
    selection = select_union((), (spec,), episodes, minimum_reference_score=0.5)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "no_op_blocked": not compile_guards((spec,))(stagnant, "look"),
            "changed_observation_allows": compile_guards((spec,))(
                View((("look", "old"), ("look", "new"))), "look"
            ),
            "safe_action_not_blocked": compile_guards((spec,))(View(), "finish"),
            "offline_gate_accepts": report["accepted"],
            "union_measured_not_assumed": selection["specs"] == (spec,),
            "guard_has_no_reward_input": set(View.__dataclass_fields__)
            == {"history", "done_options"},
        },
        "metrics": {
            "coverage": report["coverage"],
            "effective_block_rate": report["effective_block_rate"],
            "wasted_recall": report["wasted_recall"],
        },
    }
