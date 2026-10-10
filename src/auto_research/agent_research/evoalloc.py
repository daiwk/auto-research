"""EvoAlloc's allocation/evidence controller, with external LLM callbacks.

No candidate program is executed by this module. Evaluator callbacks must use a
sandbox. Full search-suite scores are optimization evidence, not held-out tests.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Callable


@dataclass(frozen=True)
class Candidate:
    identifier: str
    program: str
    parent_score: float


@dataclass(frozen=True)
class Allocation:
    actions: tuple[str, ...]
    partial_result: dict | None

    @property
    def full(self):
        return self.actions[-1] in {"FULL_EVAL", "CONTINUE_TO_FULL"}


@dataclass(frozen=True)
class Experience:
    identifier: str
    content: str
    status: str = "tentative"
    support_cases: tuple[int, ...] = ()
    counter_cases: tuple[int, ...] = ()


def apply_experience_operations(previous, operations, observed_cases):
    """Fixed statements; ADD/UPDATE/DELETE, case-grounded evidence, bounded memory."""
    from dataclasses import replace
    entries = {e.identifier: e for e in previous}
    observed_cases = set(observed_cases)
    for op in operations:
        action, key = op["operation"], op["identifier"]
        if action == "DELETE":
            if key not in entries:
                raise ValueError("cannot delete unknown experience")
            del entries[key]
            continue
        support, counter = tuple(op.get("support_cases", ())), tuple(op.get("counter_cases", ()))
        if not set(support + counter) <= observed_cases or set(support) & set(counter):
            raise ValueError("experience evidence must reference observed, noncontradictory case indices")
        if action == "ADD":
            if key in entries or not op.get("content", "").strip():
                raise ValueError("ADD requires new identifier and fixed statement")
            entries[key] = Experience(key, op["content"], "tentative", support, counter)
        elif action == "UPDATE":
            if key not in entries or "content" in op:
                raise ValueError("UPDATE cannot rewrite experience content")
            status = op.get("status", entries[key].status)
            if status not in {"active", "tentative", "stale"}:
                raise ValueError("invalid experience status")
            old = entries[key]
            merged_support = tuple(dict.fromkeys(old.support_cases + support))
            merged_counter = tuple(dict.fromkeys(old.counter_cases + counter))
            if set(merged_support) & set(merged_counter):
                raise ValueError("merged experience evidence must remain noncontradictory")
            entries[key] = replace(old, status=status,
                support_cases=merged_support, counter_cases=merged_counter)
        else:
            raise ValueError("unknown experience operation")
    values = tuple(entries.values())
    if sum(e.status != "stale" for e in values) > 4 or sum(e.status == "stale" for e in values) > 4:
        raise ValueError("experience capacities: four active/tentative and four stale")
    return values


def allocate(candidate, context, strategy, experiences, decide, partial_evaluate,
             partial_cache):
    action = decide(candidate, context, strategy, experiences, None)
    if action in {"FULL_EVAL", "DISCARD"}:
        return Allocation((action,), None)
    if action != "PARTIAL_EVAL" or partial_evaluate is None:
        raise ValueError("unsupported initial allocation action")
    if candidate.identifier not in partial_cache:
        partial_cache[candidate.identifier] = partial_evaluate(candidate)
    evidence = partial_cache[candidate.identifier]
    action2 = decide(candidate, context, strategy, experiences, evidence)
    if action2 not in {"CONTINUE_TO_FULL", "STOP"}:
        raise ValueError("post-partial decision must continue or stop")
    return Allocation((action, action2), evidence)


def _strategy_cost(history, shadow=False):
    missed, full, partial = 0, 0, 0
    for entry in history:
        decision = entry["shadow"] if shadow else entry["allocation"]
        if decision is None:
            continue
        missed += bool(entry["new_best"] and not decision.full)
        full += decision.full
        partial += "PARTIAL_EVAL" in decision.actions
    return missed, full, partial


def evolve_allocation(*, initial_archive: dict, initial_strategy: str,
                      propose: Callable, decide: Callable, full_evaluate: Callable,
                      update_experiences: Callable, reflect_strategy: Callable,
                      partial_evaluate=None, budget=20, exploration=.3,
                      experience_interval=5, strategy_interval=10,
                      validation_disagreements=2, seed=42, proposal_limit=10000):
    """Algorithm 1 with union evidence and lexicographic shadow validation."""
    if not initial_archive or budget <= 0 or not 0 <= exploration <= 1:
        raise ValueError("initial scored archive and valid budget/exploration required")
    if min(experience_interval, strategy_interval, validation_disagreements, proposal_limit) < 1:
        raise ValueError("positive update intervals required")
    rng, archive, history = random.Random(seed), dict(initial_archive), []
    strategy, experiences, shadow = initial_strategy, (), None
    full_count = last_experience = last_reflection = 0
    validation_start = 0
    found_new_best = found_non_best = False
    while full_count < budget:
        if len(history) >= proposal_limit:
            raise RuntimeError("proposal guard reached before consuming the full budget")
        candidate = propose(dict(archive), tuple(history))
        if candidate.identifier in archive or any(h["candidate"].identifier == candidate.identifier for h in history):
            raise ValueError("candidate identifiers must be unique")
        best_before = max(archive.values())
        context = {"parent_score": candidate.parent_score, "best_score": best_before,
                   "full_evaluations": full_count, "remaining_budget": budget - full_count}
        cache = {}
        incumbent = allocate(candidate, context, strategy, experiences, decide, partial_evaluate, cache)
        challenger = (allocate(candidate, context, shadow, experiences, decide, partial_evaluate, cache)
                      if shadow is not None else None)
        warmup_complete = found_new_best and found_non_best
        reason = "strategy" if incumbent.full else (
            "warmup" if not warmup_complete else (
                "shadow-union" if challenger is not None and challenger.full else (
                    "counterfactual" if rng.random() < exploration else None)))
        observed = float(full_evaluate(candidate)) if reason is not None else None
        if observed is not None and not math.isfinite(observed):
            raise ValueError("full evaluator returned a nonfinite score")
        new_best = observed is not None and observed > best_before
        entry = {"candidate": candidate, "context": context, "allocation": incumbent,
                 "shadow": challenger, "observed_score": observed,
                 "evaluation_reason": reason, "new_best": new_best,
                 "strategy": strategy, "shadow_strategy": shadow}
        history.append(entry)
        if observed is not None:
            full_count += 1
            archive[candidate.identifier] = observed
            found_new_best |= new_best
            found_non_best |= not new_best
        if full_count - last_experience >= experience_interval:
            experiences = update_experiences(experiences, tuple(history))
            last_experience = full_count
        if shadow is not None:
            disagreements = [h for h in history[validation_start:]
                             if h["allocation"].actions != h["shadow"].actions
                             and h["observed_score"] is not None]
            if len(disagreements) >= validation_disagreements:
                if _strategy_cost(disagreements, True) < _strategy_cost(disagreements):
                    strategy = shadow
                shadow = None
        elif found_new_best and found_non_best and full_count - last_reflection >= strategy_interval:
            shadow = reflect_strategy(strategy, experiences, tuple(history))
            if not isinstance(shadow, str) or not shadow.strip():
                raise ValueError("reflection must produce a nonempty explicit strategy")
            last_reflection, validation_start = full_count, len(history)
    return {"best_identifier": max(archive, key=archive.get), "best_score": max(archive.values()),
            "full_evaluations": full_count, "strategy": strategy,
            "experiences": experiences, "history": history}
