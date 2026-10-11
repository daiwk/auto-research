"""Memento 3: reflective rulebook/code pairs gated by complete exact replay.

The generator sees only the action interface and public interaction history.
No environment source, latent state, gold plan or evaluator is stored here.
Failed proposals and code/semantic disagreements remain in the audit trail.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import copy
import json
import random

from .memento3_python import ProgramError, RestrictedProgram, bounded_value


def observation(value: dict) -> dict:
    if (type(value) is not dict or set(value) != {"grid", "completed", "terminated"}
            or type(value["completed"]) is not bool or type(value["terminated"]) is not bool):
        raise ProgramError("public observation schema")
    grid = value["grid"]
    if (type(grid) is not list or not 1 <= len(grid) <= 64
            or any(type(row) is not list or len(row) != len(grid[0]) for row in grid)
            or not 1 <= len(grid[0]) <= 64
            or any(type(cell) is not int or not 0 <= cell <= 255 for row in grid for cell in row)):
        raise ProgramError("rectangular integer grid required")
    bounded_value(value)
    return copy.deepcopy(value)


def _json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    value = json.loads(text)
    if type(value) is not dict:
        raise ProgramError("generator must emit a JSON object")
    return value


@dataclass
class Trajectory:
    initial: dict
    transitions: list[tuple[int, dict]]

    def public(self):
        return {"initial": observation(self.initial), "transitions": [
            {"action": action, "observation": observation(obs)} for action, obs in self.transitions]}


@dataclass
class Hypothesis:
    rulebook: str
    program: RestrictedProgram
    generation: int


def replay(program: RestrictedProgram, histories: list[Trajectory]):
    """Initialise once per trajectory; never reset to every observed next frame."""
    state = None
    for trajectory_index, history in enumerate(histories):
        state = program.call("initialise", observation(history.initial))
        for transition_index, (action, expected) in enumerate([(None, history.initial), *history.transitions]):
            if action is not None:
                state = program.call("step", state, action)
            actual = observation(program.call("observe", state))
            completed = program.call("goal", state)
            if type(completed) is not bool or actual != observation(expected) or completed != expected["completed"]:
                raise ProgramError(f"replay mismatch at trajectory {trajectory_index}, transition {transition_index}")
    if state is None:
        raise ProgramError("at least one observed initial frame required")
    return state


def shortest_plan(program: RestrictedProgram, state, actions: tuple[int, ...], *, horizon=8, nodes=512):
    """Breadth-first unit-cost planning on generated dynamics, no real env calls."""
    if min(horizon, nodes) < 1:
        raise ValueError("positive planner budgets")
    queue = deque([(state, ())])
    seen = {json.dumps(state, sort_keys=True)}
    expanded = 0
    while queue and expanded < nodes:
        current, plan = queue.popleft()
        expanded += 1
        is_goal = program.call("goal", current)
        if type(is_goal) is not bool:
            raise ProgramError("goal must be boolean")
        if is_goal:
            return plan
        if len(plan) >= horizon:
            continue
        for action in actions:
            next_state = program.call("step", current, action)
            observation(program.call("observe", next_state))
            key = json.dumps(next_state, sort_keys=True)
            if key not in seen:
                seen.add(key)
                queue.append((next_state, (*plan, action)))
    return None


SYNTAX = (
    "Pure restricted Python only. Define initialise(observation), step(state,action), "
    "observe(state), goal(state); optional named helper functions. JSON-valued state only. "
    "Allowed: assignment including indexed assignment, lists/dicts/tuples, indexing/slices, "
    "if/for/while/break/continue, return, + - * // %, comparisons, booleans. "
    "Calls only to your named functions or len/range/min/max/abs/sum/int/bool/list. "
    "NO imports, attributes/methods (including copy/append/get), comprehensions, classes, "
    "recursion, external access, globals, floats, exponentiation. Copy lists using loops "
    "and list concatenation or slicing. Each function call has 20000 execution fuel. "
    "observe returns exactly {grid: rectangular integer cells, completed: bool, terminated: bool}. "
    "goal returns the inferred completion boolean. Initialise once from the initial frame; "
    "step simulates actions; observe renders the complete predicted frame. "
    "Do not memorise recorded next frames as a transition lookup table."
)


class Memento3:
    def __init__(self, generate, actions: tuple[int, ...], *, population=2, seed=42,
                 repair_attempts=2, horizon=8, planner_nodes=512, revision_budget=4):
        if (not actions or any(type(x) is not int for x in actions) or len(set(actions)) != len(actions)
                or min(population, repair_attempts, horizon, planner_nodes, revision_budget) < 1):
            raise ValueError("bounded action/population/controller budgets required")
        self.generate, self.actions = generate, tuple(actions)
        self.population, self.repair_attempts = population, repair_attempts
        self.horizon, self.planner_nodes, self.revision_budget = horizon, planner_nodes, revision_budget
        self.rng = random.Random(seed)
        self.histories: list[Trajectory] = []
        self.members: list[Hypothesis | None] = [None] * population
        self.versions: list[dict] = []
        self.events: list[dict] = []
        self.active: tuple[int, tuple[int, ...]] | None = None
        self.revision_rounds = 0

    def start(self, initial):
        self.histories.append(Trajectory(observation(initial), []))
        self.active = None

    def _context(self, old):
        return json.dumps({"action_interface": list(self.actions),
                           "history": [t.public() for t in self.histories],
                           "previous": None if old is None else {
                               "rulebook": old.rulebook, "source": old.program.source},
                           "versions": self.versions[-4:]}, ensure_ascii=False)

    def _propose(self, old):
        context = self._context(old)
        choice = "revise_rulebook"
        if old:
            reflection = _json(self.generate("reflection", "From this public interaction evidence choose "
                                "retain, revise_rulebook or repair_code. Return JSON {choice, reason}.\n" + context))
            choice = reflection.get("choice")
            if choice not in {"retain", "revise_rulebook", "repair_code"}:
                raise ProgramError("invalid reflection choice")
            self.events.append({"stage": "reflection", **reflection})
        rulebook = old.rulebook if old else ""
        if choice == "revise_rulebook":
            rules = _json(self.generate("rulebook", "Infer/refine a concise natural-language rulebook "
                          "from ONLY the action interface and observed frames. Record unknown mechanics "
                          "as hypotheses, not facts. Return JSON {rulebook: string}.\n" + context))
            rulebook = rules.get("rulebook")
            if type(rulebook) is not str or not rulebook.strip() or len(rulebook) > 8192:
                raise ProgramError("invalid rulebook")
        if choice == "retain":
            source = old.program.source
        else:
            code = _json(self.generate("compile", "Compile the rulebook into executable transition "
                         "and inferred goal dynamics. Return ONLY JSON {source: Python string}.\n"
                         + SYNTAX + "\nRULEBOOK: " + rulebook + "\n" + context))
            source = code.get("source")
        program = RestrictedProgram(source)
        judge = _json(self.generate("faithfulness", "Judge whether source faithfully implements "
                      "ALL stated rulebook hypotheses, without silently substituting recorded-frame "
                      "lookup. Unknown mechanics may be explicitly hypothesised. Return ONLY JSON "
                      "{faithful: boolean, reason: string}. Fail on omitted/contradictory rules.\n"
                      + json.dumps({"rulebook": rulebook, "source": source})))
        if type(judge.get("faithful")) is not bool or not isinstance(judge.get("reason"), str):
            raise ProgramError("invalid faithfulness judgement")
        self.events.append({"stage": "faithfulness", **judge})
        if not judge["faithful"]:
            raise ProgramError("LLM semantic faithfulness rejected")
        replay(program, self.histories)
        return Hypothesis(rulebook, program, len(self.versions))

    def update(self):
        can_revise = self.revision_rounds < self.revision_budget
        if not can_revise:
            self.events.append({"stage": "revision_budget_exhausted"})
        else:
            self.revision_rounds += 1
        for index, old in enumerate(self.members):
            if old:
                try:
                    replay(old.program, self.histories)
                    continue
                except ProgramError as exc:
                    self.events.append({"stage": "falsified", "member": index, "reason": str(exc)})
                    self.members[index] = None
            if not can_revise:
                continue
            for attempt in range(self.repair_attempts):
                try:
                    proposal = self._propose(old)
                    self.members[index] = proposal
                    version = {"member": index, "generation": proposal.generation,
                               "rulebook": proposal.rulebook, "source": proposal.program.source,
                               "real_transitions": sum(len(t.transitions) for t in self.histories)}
                    self.versions.append(version)
                    self.events.append({"stage": "accepted", **version})
                    break
                except (ProgramError, ValueError, TypeError) as exc:
                    self.events.append({"stage": "rejected", "member": index,
                                        "attempt": attempt, "reason": str(exc)})

    def plans(self, remaining_budget):
        classes: dict[tuple[int, ...], list[int]] = {}
        for index, member in enumerate(self.members):
            if member is None:
                continue
            try:
                state = replay(member.program, self.histories)
                plan = shortest_plan(member.program, state, self.actions,
                                     horizon=min(self.horizon, remaining_budget), nodes=self.planner_nodes)
                if plan:
                    classes.setdefault(plan, []).append(index)
            except ProgramError as exc:
                self.events.append({"stage": "planning_rejected", "member": index, "reason": str(exc)})
        return classes

    def choose(self, remaining_budget):
        if not self.histories or remaining_budget < 1:
            raise ValueError("active trajectory/action budget required")
        if self.active:
            index, plan = self.active
            if self.members[index] is not None and plan:
                self.active = (index, plan[1:])
                return plan[0]
        classes = self.plans(remaining_budget)
        if classes:
            plan = self.rng.choice(list(classes))  # Uniform over plans, NOT models.
            index = classes[plan][0]
            self.active = (index, plan[1:])
            self.events.append({"stage": "plan", "class_count": len(classes),
                                "equivalent_members": classes[plan], "plan": list(plan)})
            return plan[0]
        # Frozen LLM chooses exploration; no oracle or hard-coded navigation fallback.
        try:
            proposed = _json(self.generate("explore", "No verified model yields a goal plan. "
                             "Choose ONE exploratory action from the public interface to resolve "
                             "uncertain rules. Return JSON {action: integer, reason: string}.\n"
                             + self._context(None)))
            action = proposed.get("action")
            if type(action) is not int or action not in self.actions:
                raise ProgramError("invalid exploratory action")
            self.events.append({"stage": "explore", **proposed})
            return action
        except (ProgramError, ValueError, TypeError) as exc:
            self.events.append({"stage": "exploration_failed", "reason": str(exc)})
            return None

    def observe(self, action, next_observation):
        if not self.histories or type(action) is not int or action not in self.actions:
            raise ValueError("known action and active trajectory required")
        self.histories[-1].transitions.append((action, observation(next_observation)))
        mismatch = False
        for index, member in enumerate(self.members):
            if member:
                try:
                    replay(member.program, self.histories)
                except ProgramError as exc:
                    mismatch = True
                    self.events.append({"stage": "prediction_mismatch", "member": index, "reason": str(exc)})
        if mismatch:
            self.active = None  # Never execute the rest of a falsified plan.
        return mismatch
