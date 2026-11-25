"""Small finite-family CAPE compiler, arXiv:2611.31938v1, equations 1--7.

Calibration may query named reproducible configurations. The returned policy
contains actions and observation branches only: deployment never receives the
active configuration, a full effect table, a reference answer or a gold plan.
This implements a bounded compiler component, not the paper's native CSV/JSON
tools, LLM proposal stage, or performance campaign.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Callable


Value = tuple[int, int]  # completed configurations, NEGATED total call mass


@dataclass(frozen=True)
class Effect:
    observation: str
    commit: bool


@dataclass(frozen=True)
class Action:
    name: str
    program: bool


@dataclass(frozen=True)
class Policy:
    action: str | None = None
    branches: tuple[tuple[str, "Policy"], ...] = ()
    default: "Policy | None" = None

    def after(self, observation: str) -> "Policy":
        return dict(self.branches).get(observation, self.default or Policy())


@dataclass(frozen=True)
class Witness:
    policy: Policy
    successes: frozenset[str]
    call_mass: int

    @property
    def value(self) -> Value:
        return len(self.successes), -self.call_mass


def catalog_retry(programs: tuple[str, ...]) -> Policy:
    policy = Policy()
    for name in reversed(programs):
        policy = Policy(name, default=policy)
    return policy


def execute(policy: Policy, tool: Callable[[str], Effect], *, call_limit: int) -> tuple[bool, int]:
    """An observation-only deployment interface; the tool owns commit checks."""
    if call_limit < 0:
        raise ValueError("negative execution allowance")
    for i in range(call_limit):
        if policy.action is None:
            return False, i
        effect = tool(policy.action)
        if not isinstance(effect, Effect):
            raise TypeError("tool must return an Effect")
        if effect.commit:
            return True, i + 1
        policy = policy.after(effect.observation)
    return False, call_limit


class CapeCompiler:
    """CAPE on at most eight configurations and a short finite call horizon.

    A query-count allowance makes interruption deterministic. Unlike a native
    wall-clock compilation budget it does not measure acquisition/search costs.
    Persistent witnesses, the executable/optimistic frontier, local closure and
    selected-action two-call tightening follow the fixed-v1 algorithm.
    """

    def __init__(self, configurations: tuple[str, ...], actions: tuple[Action, ...],
                 calibrate: Callable[[str, str], Effect], initial: Policy,
                 *, call_limit: int = 3):
        if not 1 <= len(configurations) <= 8 or len(set(configurations)) != len(configurations):
            raise ValueError("component supports one to eight distinct configurations")
        if not 1 <= call_limit <= 4:
            raise ValueError("component supports one to four deployment calls")
        if not actions or len({a.name for a in actions}) != len(actions):
            raise ValueError("actions must be nonempty and uniquely named")
        if any(not isinstance(a.program, bool) or not isinstance(a.name, str) or
               not a.name for a in actions):
            raise ValueError("action kind/name must be explicit")
        if not any(a.program for a in actions):
            raise ValueError("at least one program is required")
        self.h = configurations
        self.actions = actions
        self.by_name = {a.name: a for a in actions}
        self.calibrate = calibrate
        self.initial = initial
        self.calls = call_limit
        self.effects: dict[tuple[str, str], Effect] = {}
        self.required: frozenset[str] = frozenset()
        self.witnesses: dict[tuple[frozenset[str], int], Witness] = {}
        self.upper_history: dict[tuple[frozenset[str], int], Value] = {}
        self.action_bounds: dict[tuple[frozenset[str], int, str], Value] = {}
        self.snapshots: list[dict] = []
        self.query_log: list[tuple[str, str]] = []
        self.selected_tightenings = 0
        self.certified = False
        self._limit = 0

    def _acquire(self, action: str, h: str) -> Effect:
        if (action, h) not in self.effects:
            if len(self.query_log) >= self._limit:
                raise InterruptedError("calibration allowance exhausted")
            if action not in self.by_name or h not in self.h:
                raise ValueError("query outside declared calibration family")
            effect = self.calibrate(action, h)
            if (not isinstance(effect, Effect) or not isinstance(effect.observation, str)
                    or not isinstance(effect.commit, bool)):
                raise TypeError("calibration must return a string-observation, boolean-commit Effect")
            if effect.commit and not self.by_name[action].program:
                raise ValueError("a diagnostic probe cannot commit")
            self.effects[action, h] = effect
            self.query_log.append((action, h))
        return self.effects[action, h]

    def _parts(self, action: Action, scope: frozenset[str], *, optimistic: bool):
        successes: set[str] = set()
        cells: dict[tuple[str, str], set[str]] = {}
        for h in sorted(scope):
            effect = self.effects.get((action.name, h))
            if effect is None:
                if not optimistic:
                    raise ValueError("action is not locally closed")
                if action.program:
                    successes.add(h)
                else:
                    # Unknown probes get singleton hypothetical responses. Tags
                    # cannot collide with observed strings, even adversarial ones.
                    cells[("unknown", h)] = {h}
            elif effect.commit:
                successes.add(h)
            else:
                cells.setdefault(("known", effect.observation), set()).add(h)
        return frozenset(successes), {key: frozenset(v) for key, v in cells.items()}

    def _closed(self, action: Action, scope: frozenset[str]) -> bool:
        return all((action.name, h) in self.effects for h in scope)

    def _lower(self, scope: frozenset[str], b: int) -> Witness | None:
        state = scope, b
        obligation = scope & self.required
        best = self.witnesses.get(state)
        if not obligation and best is None:
            best = Witness(Policy(), frozenset(), 0)
        if b:
            for action in self.actions:
                if not self._closed(action, scope):
                    continue
                success, cells = self._parts(action, scope, optimistic=False)
                children = [(key, self._lower(cell, b - 1)) for key, cell in cells.items()]
                if any(child is None for _, child in children):
                    continue
                successes = success | frozenset().union(*(child.successes for _, child in children))
                if not obligation <= successes:
                    continue
                candidate = Witness(Policy(action.name, tuple(
                    (key[1], child.policy) for key, child in children)), successes,
                    len(scope) + sum(child.call_mass for _, child in children))
                if best is None or candidate.value > best.value:
                    best = candidate
        if best is not None:
            self.witnesses[state] = best
        return best

    def _cheap(self, scope: frozenset[str], b: int) -> Value | None:
        obligation = scope & self.required
        if b == 0:
            return None if obligation else (0, 0)
        possible = [frozenset(h for h in scope if (a.name, h) not in self.effects or
                    self.effects[a.name, h].commit) for a in self.actions if a.program]
        if b == 1:
            values = [(len(s), -len(scope)) for s in possible if obligation <= s]
            if not obligation:
                values.append((0, 0))
            return max(values) if values else None
        support = frozenset().union(*possible)
        if not obligation <= support:
            return None
        if not support:
            return (0, 0)
        # Eq. 5: support count, then a lower bound on call mass.
        return len(support), -(len(scope) + len(support) - max(map(len, possible)))

    def _action_upper(self, action: Action, scope: frozenset[str], b: int,
                      *, selected: bool = False) -> Value | None:
        success, cells = self._parts(action, scope, optimistic=True)
        values = []
        closed = self._closed(action, scope)
        for cell in cells.values():
            if closed:
                value = self._upper(cell, b - 1)
            elif selected and b - 1 == 2:
                value = self._two_call(cell)
            else:
                value = self._cheap(cell, b - 1)
            if value is None:
                return None
            values.append(value)
        value = len(success) + sum(v[0] for v in values), -len(scope) + sum(v[1] for v in values)
        key = scope, b, action.name
        if key in self.action_bounds:
            value = min(value, self.action_bounds[key])
        self.action_bounds[key] = value
        return value

    def _two_call(self, scope: frozenset[str]) -> Value | None:
        self.selected_tightenings += 1
        # Eq. 7: exact optimistic two-call problem; no recursive horizon reduction
        # of the actual deployment problem is performed.
        values = []
        for a in self.actions:
            success, cells = self._parts(a, scope, optimistic=True)
            children = [self._cheap(cell, 1) for cell in cells.values()]
            if all(v is not None for v in children):
                values.append((len(success) + sum(v[0] for v in children),
                               -len(scope) + sum(v[1] for v in children)))
        if not scope & self.required:
            values.append((0, 0))
        cheap = self._cheap(scope, 2)
        return min(max(values), cheap) if values and cheap is not None else None

    def _upper(self, scope: frozenset[str], b: int) -> Value | None:
        cheap = self._cheap(scope, b)
        if cheap is None or b == 0:
            return cheap
        values = [value for a in self.actions if (value := self._action_upper(a, scope, b)) is not None]
        if not scope & self.required:
            values.append((0, 0))
        if not values:
            return None
        upper = min(cheap, max(values))
        state = scope, b
        if state in self.upper_history:
            upper = min(upper, self.upper_history[state])
        self.upper_history[state] = upper
        return upper

    def _frontier(self) -> set[tuple[frozenset[str], int]]:
        frontier = set()
        def witness_path(scope, b, policy):
            if not b or not scope or policy.action is None:
                return
            frontier.add((scope, b))
            a = self.by_name[policy.action]
            _, cells = self._parts(a, scope, optimistic=False)
            for key, cell in cells.items():
                witness_path(cell, b - 1, policy.after(key[1]))
        root = frozenset(self.h)
        witness = self._lower(root, self.calls)
        if witness:
            witness_path(root, self.calls, witness.policy)
        visited = set()
        def optimistic_path(scope, b):
            if not b or not scope or (scope, b) in visited:
                return
            visited.add((scope, b))
            frontier.add((scope, b))
            candidates = [(v, -i, a) for i, a in enumerate(self.actions)
                          if (v := self._action_upper(a, scope, b)) is not None]
            if not candidates:
                return
            _, _, action = max(candidates, key=lambda x: (x[0], x[1]))
            if self._closed(action, scope):
                _, cells = self._parts(action, scope, optimistic=False)
                for cell in cells.values():
                    optimistic_path(cell, b - 1)
        optimistic_path(root, self.calls)
        return frontier

    def _select(self):
        candidates = []
        for scope, b in sorted(self._frontier(), key=lambda s: (s[1], sorted(s[0]))):
            lower = self._lower(scope, b)
            for index, action in enumerate(self.actions):
                missing = len([h for h in scope if (action.name, h) not in self.effects])
                if not missing:
                    continue
                upper = self._action_upper(action, scope, b)
                if upper is None or (lower and upper <= lower.value):
                    continue
                if lower is None:
                    tier, gain = 3, len(scope & self.required)
                elif upper[0] > lower.value[0]:
                    tier, gain = 2, upper[0] - lower.value[0]
                else:
                    tier, gain = 1, upper[1] - lower.value[1]
                candidates.append(((tier, gain / missing, -missing, action.program, -index),
                                   scope, b, action))
        return max(candidates, key=lambda x: x[0])[1:] if candidates else None

    def _snapshot(self) -> None:
        root = frozenset(self.h)
        lower = self._lower(root, self.calls)
        upper = self._upper(root, self.calls)
        if lower is None or upper is None or lower.value > upper:
            raise ArithmeticError("invalid executable/optimistic bounds")
        self.snapshots.append({"queries": len(self.query_log), "lower": lower.value,
                               "upper": upper, "required": sorted(self.required)})

    def compile(self, *, max_queries: int) -> Policy:
        if max_queries < 0:
            raise ValueError("negative calibration allowance")
        if self.query_log:
            raise ValueError("use a fresh compiler for each campaign")
        self._limit = max_queries
        successes = set()
        try:
            # Validate the initial policy, acquiring only its actual paths.
            for h in self.h:
                ok, _ = execute(self.initial, lambda a, h=h: self._acquire(a, h), call_limit=self.calls)
                if ok:
                    successes.add(h)
        except InterruptedError:
            # The original initial policy is returned, with no certificate or
            # claim that its not-yet-validated coverage is known.
            return self.initial
        self.required = frozenset(successes)
        self._snapshot()
        while self.snapshots[-1]["lower"] != self.snapshots[-1]["upper"]:
            selected = self._select()
            if selected is None:
                raise ArithmeticError("unresolved root has no acquisition frontier")
            scope, b, action = selected
            while not self._closed(action, scope):
                lower = self._lower(scope, b)
                upper = self._action_upper(action, scope, b, selected=True)
                if upper is None or (lower and upper <= lower.value):
                    break
                missing = [h for h in self.h if h in scope and (action.name, h) not in self.effects]
                missing.sort(key=lambda h: h not in self.required)
                try:
                    self._acquire(action.name, missing[0])
                except InterruptedError:
                    self._snapshot()
                    return self.witnesses[frozenset(self.h), self.calls].policy
                self._snapshot()
            self._snapshot()
        self.certified = True
        return self.witnesses[frozenset(self.h), self.calls].policy


def exhaustive_oracle(configurations: tuple[str, ...], actions: tuple[Action, ...],
                      full_effects: dict[tuple[str, str], Effect], required: frozenset[str],
                      calls: int) -> Value:
    """Independent complete-information finite search, evaluation side only."""
    @lru_cache(None)
    def enumerate_actions(scope: frozenset[str], budget: int):
        best = (0, 0) if not scope & required else None
        if budget == 0:
            return best
        for action in actions:
            commits = set()
            branches = {}
            for h in scope:
                effect = full_effects[action.name, h]
                if effect.commit:
                    commits.add(h)
                else:
                    branches.setdefault(effect.observation, set()).add(h)
            parts = [enumerate_actions(frozenset(v), budget - 1) for v in branches.values()]
            if any(value is None for value in parts):
                continue
            value = len(commits) + sum(p[0] for p in parts), -len(scope) + sum(p[1] for p in parts)
            if best is None or value > best:
                best = value
        return best
    result = enumerate_actions(frozenset(configurations), calls)
    if result is None:
        raise ValueError("protected coverage infeasible")
    return result


REQUIRES_GPU_VALIDATION = False


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """The paper's four-configuration teaching structure, not its native data."""
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    import random
    configurations = ("semicolon-day", "comma-day", "semicolon-month", "comma-month")
    actions = tuple(Action(f"p{i}", True) for i in range(4)) + (Action("probe", False),)
    effects = {(a.name, h): Effect(h if not a.program else "parse-error",
               a.program and a.name == f"p{i}")
               for a in actions for i, h in enumerate(configurations)}
    order = list(configurations)
    random.Random(seed).shuffle(order)
    compiler = CapeCompiler(tuple(order), actions, lambda a, h: effects[a, h],
                            catalog_retry(("p3", "p0", "p1")))
    policy = compiler.compile(max_queries=len(effects))
    outcomes = [execute(policy, lambda a, h=h: effects[a, h], call_limit=3) for h in configurations]
    value = sum(ok for ok, _ in outcomes), -sum(n for _, n in outcomes)
    oracle = exhaustive_oracle(configurations, actions, effects, compiler.required, 3)
    result = {"diagnostic_only": True, "seed": seed, "configurations": 4,
            "calibration_queries": len(compiler.query_log), "eager_table_queries": len(effects),
            "completed_configurations": value[0], "total_deployment_calls": -value[1],
            "oracle_agreement": value == oracle, "runtime_certificate": compiler.certified,
            "protected_configurations": len(compiler.required),
            "bound_snapshots": len(compiler.snapshots),
            "selected_two_call_tightenings": compiler.selected_tightenings}
    result["evaluation_tier"] = "l1_mechanism"
    result["checks"] = {
        "independent_exhaustive_oracle_agrees": result["oracle_agreement"],
        "closed_lower_bound_has_certificate": result["runtime_certificate"],
        "all_four_configurations_complete": result["completed_configurations"] == 4,
        "bounded_deployment_calls": max(calls for _, calls in outcomes) <= 3,
        "calibration_does_not_exceed_full_table": result["calibration_queries"] <= result["eager_table_queries"],
        "full_table_negative_result_is_preserved": result["calibration_queries"] == result["eager_table_queries"],
    }
    result["metrics"] = {key: result[key] for key in (
        "configurations", "calibration_queries", "eager_table_queries", "completed_configurations",
        "total_deployment_calls", "protected_configurations", "bound_snapshots", "selected_two_call_tightenings")}
    return result
