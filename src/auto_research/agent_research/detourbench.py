"""DetourBench exact finite-state reference and trajectory metrics (§3).

Evaluator infrastructure, not an LLM agent. Hidden graphs/oracles must remain
outside the actor process; this module never claims a synthetic policy score.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import ceil, isfinite

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class State:
    visited: frozenset[str]
    credentials: frozenset[str] = frozenset()
    outcome: str = "active"

    def __post_init__(self):
        if (
            not isinstance(self.visited, frozenset)
            or not isinstance(self.credentials, frozenset)
            or self.outcome not in {"active", "success", "wrong"}
        ):
            raise ValueError("immutable state sets and declared outcome required")


@dataclass(frozen=True)
class Action:
    key: str
    source: str
    requires: frozenset[str] = frozenset()
    credentials: frozenset[str] = frozenset()
    reveals: frozenset[str] = frozenset()
    grants: frozenset[str] = frozenset()
    terminal: str | None = None

    def __post_init__(self):
        if not self.key or not self.source or self.terminal not in {None, "success", "wrong"}:
            raise ValueError("named action/source and valid terminal required")
        if any(
            not isinstance(v, frozenset)
            for v in (self.requires, self.credentials, self.reveals, self.grants)
        ):
            raise TypeError("immutable prerequisite/effect sets required")


class FiniteTask:
    """Evaluator-only monotone task; all dispatched accesses cost exactly one."""

    def __init__(self, actions: tuple[Action, ...], initial: State):
        self.actions = {a.key: a for a in actions}
        if len(self.actions) != len(actions) or initial.outcome != "active":
            raise ValueError("unique actions and active initial state required")
        self.initial = initial

    def step(self, state: State, key: str) -> tuple[State, str]:
        if state.outcome != "active":
            raise ValueError("terminal states dispatch no further access")
        a = self.actions.get(key)
        if (
            a is None
            or a.source not in state.visited
            or not a.requires <= state.visited
            or not a.credentials <= state.credentials
        ):
            return state, "invalid"
        new = State(state.visited | a.reveals, state.credentials | a.grants, a.terminal or "active")
        return new, "duplicate" if new == state else "advancing"

    def shortest(self, start: State | None = None, *, max_states: int = 100_000):
        """Exact BFS, returning distance and replayable witness, or None.

        A wrong terminal has no finite residual. An active unrecoverable graph
        is rejected by metrics rather than assigned a made-up residual.
        """
        if type(max_states) is not int or max_states < 1:
            raise ValueError("positive integer state cap required")
        start = self.initial if start is None else start
        if start.outcome == "wrong":
            return None
        queue = deque([(start, ())])
        seen = {start}
        while queue:
            state, path = queue.popleft()
            if state.outcome == "success":
                return len(path), path
            for key in sorted(self.actions):
                new, _ = self.step(state, key)
                if new.outcome == "wrong" or new in seen:
                    continue
                seen.add(new)
                if len(seen) > max_states:
                    raise RuntimeError(
                        "exact oracle state cap exceeded; no approximate bound returned"
                    )
                queue.append((new, path + (key,)))
        return None

    def replay(self, batches: tuple[tuple[str, ...], ...], *, budget: int):
        if type(budget) is not int or budget < 1:
            raise ValueError("positive fixed budget required")
        state, cost, invalid, duplicate = self.initial, 0, 0, 0
        dispatched = []
        for batch in batches:
            for key in batch:
                if state.outcome != "active" or cost >= budget:
                    break
                state, kind = self.step(state, key)
                cost += 1
                invalid += kind == "invalid"
                duplicate += kind == "duplicate"
                dispatched.append(key)
        return {
            "state": state,
            "cost": cost,
            "invalid": invalid,
            "duplicate": duplicate,
            "dispatched": tuple(dispatched),
        }

    def metrics(self, run: dict) -> dict:
        oracle = self.shortest()
        if oracle is None or oracle[0] < 1:
            raise ValueError("admitted task needs reachable success with positive oracle cost")
        lo, _ = oracle
        state, cost = run["state"], run["cost"]
        success = state.outcome == "success"
        residual = self.shortest(state)
        if state.outcome != "wrong" and residual is None:
            raise ValueError("active state is not graph-recoverable under the benchmark contract")
        r = None if residual is None else residual[0]
        if r is not None and not (0 <= r <= lo and cost + r >= lo):
            raise ValueError("trajectory/oracle contract mismatch")
        return {
            "success": success,
            "oracle_cost": lo,
            "residual": r,
            "attainment": lo / cost if success else None,
            "progress": None if r is None else 1 - r / lo,
            "normalized_detour": None if r is None else (cost + r - lo) / lo,
            "redundant_ratio": (run["invalid"] + run["duplicate"]) / cost if success else None,
            "irreversible_failure": state.outcome == "wrong",
        }


def access_budget(oracle: int, informed_witness: int, multiplier: float = 1.5) -> int:
    if (
        type(oracle) is not int
        or type(informed_witness) is not int
        or min(oracle, informed_witness) < 1
        or isinstance(multiplier, bool)
        or not isfinite(multiplier)
        or multiplier < 1
    ):
        raise ValueError("positive frozen witnesses and multiplier >=1 required")
    return ceil(multiplier * max(oracle, informed_witness))


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    task = FiniteTask(
        (
            Action("read", "start", reveals=frozenset({"evidence"})),
            Action("finish", "start", requires=frozenset({"evidence"}), terminal="success"),
            Action("wrong", "start", terminal="wrong"),
        ),
        State(frozenset({"start"})),
    )
    run = task.replay((("missing", "read", "read", "finish", "wrong"),), budget=5)
    good = task.metrics(run)
    bad = task.metrics(task.replay((("wrong", "finish"),), budget=5))
    partial = task.metrics(task.replay((("read",),), budget=1))
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "bfs_replay": task.shortest() == (2, ("read", "finish")),
            "invalid_duplicate_charged": run["cost"] == 4
            and run["invalid"] == 1
            and run["duplicate"] == 1,
            "batch_stops_terminal": len(run["dispatched"]) == 4,
            "wrong_not_zero_residual": bad["residual"] is None,
            "partial_residual": partial["residual"] == 1,
            "budget_not_efficiency_numerator": access_budget(2, 4) == 6,
        },
        "metrics": {
            "oracle_cost": good["oracle_cost"],
            "charged_accesses": run["cost"],
            "attainment": good["attainment"],
            "normalized_detour": good["normalized_detour"],
        },
    }
