"""Executable Blocksworld verifier and restricted optimum (2604.02910 §4.1).

No model/actor receives a gold plan. Independent BFS is limited to small tests;
the analytic formula is rejected outside its stated curriculum assumptions.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class State:
    towers: tuple[tuple[str, ...], ...]
    held: str | None = None

    def __post_init__(self):
        blocks = [b for t in self.towers for b in t] + ([] if self.held is None else [self.held])
        if any(not t for t in self.towers) or any(not isinstance(b, str) or not b for b in blocks) or len(set(blocks)) != len(blocks):
            raise ValueError("nonempty disjoint bottom-to-top towers required")
        object.__setattr__(self, "towers", tuple(sorted(self.towers)))


def transition(state: State, action: tuple[str, ...]) -> State:
    if not action or action[0] not in {"pickup", "putdown", "unstack", "stack"}:
        raise ValueError("unknown four-action operator")
    op = action[0]
    if len(action) != (3 if op in {"stack", "unstack"} else 2):
        raise ValueError("wrong operator arity")
    b = action[1]; towers = list(state.towers)
    if op in {"pickup", "unstack"}:
        if state.held is not None:
            raise ValueError("hand must be empty")
        for i, tower in enumerate(towers):
            if tower[-1] == b and ((op == "pickup" and len(tower) == 1) or (op == "unstack" and len(tower) >= 2 and tower[-2] == action[2])):
                remaining = tower[:-1]
                towers.pop(i)
                if remaining:
                    towers.append(remaining)
                return State(tuple(towers), b)
        raise ValueError("block is not clear/on requested support")
    if state.held != b:
        raise ValueError("requested block is not held")
    if op == "putdown":
        return State(tuple([*towers, (b,)]))
    for i, tower in enumerate(towers):
        if tower[-1] == action[2]:
            towers[i] = (*tower, b)
            return State(tuple(towers))
    raise ValueError("stack destination is not clear")


def satisfies(state: State, goal: tuple[str, ...]) -> bool:
    return any(len(t) >= len(goal) and t[:len(goal)] == goal for t in state.towers)


def restricted_optimal_cost(state: State, goal: tuple[str, ...]) -> int:
    if state.held is not None or not goal or len(set(goal)) != len(goal):
        raise ValueError("empty hand and unique nonempty goal required")
    positions = {b: (i, j, len(t)-j-1) for i, t in enumerate(state.towers) for j, b in enumerate(t)}
    if any(b not in positions for b in goal):
        raise ValueError("goal contains unknown block")
    if positions[goal[0]][1] != 0 or len({positions[b][0] for b in goal}) != len(goal):
        raise ValueError("formula requires table-supported base and at most one target per source tower")
    return sum(2 * positions[b][2] for b in goal) + 2 * (len(goal) - 1)


def score_plan(state: State, goal: tuple[str, ...], actions: list[tuple[str, ...]]) -> dict:
    optimum = restricted_optimal_cost(state, goal)
    current = state
    try:
        for action in actions:
            current = transition(current, action)
    except ValueError:
        return {"valid": False, "optimal_cost": optimum, "relative_gap": None}
    valid = satisfies(current, goal)
    return {"valid": valid, "optimal_cost": optimum,
            "relative_gap": ((len(actions)-optimum)/optimum if optimum else (0. if not actions else None)) if valid else None}


def bfs_optimal_cost(state: State, goal: tuple[str, ...], *, max_blocks: int = 6) -> int:
    """Independent four-operator shortest-path search, never calls the formula."""
    if sum(map(len, state.towers)) + int(state.held is not None) > max_blocks:
        raise ValueError("BFS is a bounded small-instance validation, not a production planner")
    queue = deque([(state, 0)]); seen = {state}
    while queue:
        current, distance = queue.popleft()
        if satisfies(current, goal):
            return distance
        actions = []
        if current.held is None:
            for t in current.towers:
                actions.append(("pickup", t[-1]) if len(t) == 1 else ("unstack", t[-1], t[-2]))
        else:
            actions.append(("putdown", current.held))
            actions.extend(("stack", current.held, t[-1]) for t in current.towers)
        for action in actions:
            nxt = transition(current, action)
            if nxt not in seen:
                seen.add(nxt); queue.append((nxt, distance+1))
    raise ValueError("goal unreachable")


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU verifier only")
    initial = State((("A",), ("x", "B")))
    goal = ("A", "B")
    shortest = bfs_optimal_cost(initial, goal)
    detour = score_plan(initial, goal, [("unstack", "B", "x"), ("putdown", "B"), ("pickup", "B"), ("stack", "B", "A")])
    invalid = score_plan(initial, goal, [("pickup", "B")])
    return {"seed": seed, "device": device, "metrics": {"bfs_optimal_cost": shortest, "formula_optimal_cost": restricted_optimal_cost(initial, goal), "valid_detour_relative_gap": detour["relative_gap"]},
            "checks": {"formula_matches_independent_search": shortest == restricted_optimal_cost(initial, goal),
                       "valid_is_not_optimal": detour["valid"] and detour["relative_gap"] == 1,
                       "invalid_plans_not_given_gap": not invalid["valid"] and invalid["relative_gap"] is None},
            "diagnostic_only": True, "evaluation_tier": "l1_mechanism"}
