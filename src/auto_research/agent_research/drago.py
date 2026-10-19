"""DRAGO's grounded STRIPS diagnosis/repair acceptance subset, reference-free.

Not a PDDL text parser, LLM formalizer, SMT-LIB or MiniZinc implementation.
The actual kernels are delete-relaxation reachability and bounded complete search.
"""
from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from typing import Callable

Atom = tuple[str, ...]


@dataclass(frozen=True)
class Action:
    name: str
    preconditions: frozenset[Atom]
    add: frozenset[Atom]
    delete: frozenset[Atom]


@dataclass(frozen=True)
class Domain:
    name: str
    predicates: tuple[tuple[str, int], ...]
    actions: tuple[Action, ...]


@dataclass(frozen=True)
class Problem:
    domain: str
    objects: tuple[tuple[str, str], ...]
    initial: frozenset[Atom]
    goals: frozenset[Atom]


@dataclass(frozen=True)
class Finding:
    axis: str
    detail: str
    weight: int = 1


@dataclass(frozen=True)
class Diagnosis:
    findings: tuple[Finding, ...]
    search_status: str

    @property
    def weight(self):
        return sum(f.weight for f in self.findings)


def contract(domain: Domain, problem: Problem) -> tuple[Finding, ...]:
    if (not domain.name or len(dict(domain.predicates)) != len(domain.predicates)
            or any(not name or type(arity) is not int or arity < 0 for name, arity in domain.predicates)
            or len({a.name for a in domain.actions}) != len(domain.actions)):
        raise ValueError("invalid trusted domain")
    issues = []
    objects = dict(problem.objects)
    if problem.domain != domain.name:
        issues.append(Finding("contract", "wrong domain"))
    if len(objects) != len(problem.objects) or any(not name or not kind for name, kind in problem.objects):
        issues.append(Finding("contract", "duplicate/empty object declarations"))
    signature = dict(domain.predicates)
    atoms = set(problem.initial) | set(problem.goals)
    for action in domain.actions:
        if not action.name or action.add & action.delete:
            raise ValueError("invalid trusted grounded action")
        atoms.update(action.preconditions | action.add | action.delete)
    for atom in sorted(atoms):
        if (not atom or atom[0] not in signature or len(atom)-1 != signature.get(atom[0])
                or any(arg not in objects for arg in atom[1:])):
            issues.append(Finding("contract", f"ill-typed/undeclared grounded atom: {atom}"))
    return tuple(issues)


def diagnose(domain: Domain, problem: Problem, *, expected_counts: tuple[tuple[str, int], ...] = (),
             search_budget: int = 10_000) -> Diagnosis:
    """Counts come from public statement, never reference formalization/answer.

    Search budget exhaustion is unknown, not unsolvability evidence.
    """
    if type(search_budget) is not int or search_budget < 1:
        raise ValueError("positive search budget required")
    if (len(dict(expected_counts)) != len(expected_counts) or
            any(not kind or type(count) is not int or count < 0 for kind, count in expected_counts)):
        raise ValueError("valid public statement counts required")
    findings = list(contract(domain, problem))
    if findings:
        return Diagnosis(tuple(findings), "invalid")
    counts = Counter(kind for _, kind in problem.objects)
    findings.extend(Finding("count", f"{kind}: declared {counts[kind]}, stated {count}",
                            abs(counts[kind]-count)) for kind, count in expected_counts if counts[kind] != count)
    reachable = set(problem.initial)
    while True:
        added = set().union(*(a.add for a in domain.actions if a.preconditions <= reachable))
        updated = reachable | added
        if updated == reachable:
            break
        reachable = updated
    findings.extend(Finding("reachability", f"goal unreachable even without deletes: {atom}")
                    for atom in sorted(problem.goals-reachable))
    queue, visited = deque([problem.initial]), {problem.initial}
    status, expanded = "exhausted", 0
    while queue:
        if expanded >= search_budget:
            status = "budget_exhausted"
            break
        state = queue.popleft()
        expanded += 1
        if problem.goals <= state:
            status = "solvable"
            break
        for action in domain.actions:
            if action.preconditions <= state:
                next_state = (state-action.delete) | action.add
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append(next_state)
    if status == "exhausted":
        findings.append(Finding("joint_unsolvable", "complete reachable state space exhausted"))
    return Diagnosis(tuple(findings), status)


def accept_repair(domain: Domain, before: Problem, candidate: Problem, *,
                  expected_counts: tuple[tuple[str, int], ...] = (), search_budget: int = 10_000) -> tuple[bool, str]:
    previous = diagnose(domain, before, expected_counts=expected_counts, search_budget=search_budget)
    after = diagnose(domain, candidate, expected_counts=expected_counts, search_budget=search_budget)
    if candidate == before or contract(domain, candidate):
        return False, "unchanged_or_contract_failure"
    if not previous.weight or after.weight >= previous.weight:
        return False, "no_strict_diagnostic_descent"
    if {f.axis for f in after.findings}-{f.axis for f in previous.findings}:
        return False, "new_blocking_axis"
    if len(candidate.goals) < len(before.goals):
        return False, "goal_weakening"
    old_counts, new_counts = Counter(t for _, t in before.objects), Counter(t for _, t in candidate.objects)
    expected = dict(expected_counts)
    for kind in set(old_counts) | set(new_counts):
        if old_counts[kind] != new_counts[kind]:
            if kind not in expected or abs(new_counts[kind]-expected[kind]) >= abs(old_counts[kind]-expected[kind]):
                return False, "object_count_weakening"
    if previous.search_status == "solvable" and after.search_status != "solvable":
        return False, "solver_regression_or_unknown"
    return True, "strict_reference_free_progress"


def repair_loop(domain: Domain, initial: Problem, *, proposer: Callable[[Problem, Diagnosis], Problem],
                expected_counts: tuple[tuple[str, int], ...] = (), rounds: int = 1,
                search_budget: int = 10_000) -> tuple[Problem, tuple[dict, ...]]:
    if type(rounds) is not int or not 0 <= rounds <= 20:
        raise ValueError("bounded repair rounds required")
    current, trace = initial, []
    for _ in range(rounds):
        diagnosis = diagnose(domain, current, expected_counts=expected_counts, search_budget=search_budget)
        if diagnosis.weight == 0:
            break
        candidate = proposer(current, diagnosis)
        accepted, reason = accept_repair(domain, current, candidate, expected_counts=expected_counts,
                                          search_budget=search_budget)
        trace.append({"before_weight": diagnosis.weight, "accepted": accepted, "reason": reason,
                      "after_weight": diagnose(domain, candidate, expected_counts=expected_counts,
                                               search_budget=search_budget).weight})
        if not accepted:
            break
        current = candidate
    return current, tuple(trace)
