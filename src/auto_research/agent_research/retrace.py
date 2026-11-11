"""ReTrace typed decision-list IR. No LLM compiler, actor, tool or network calls."""
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

REQUIRES_GPU_VALIDATION = False


class MissingEvidence(ValueError):
    """An IR condition or argument depends on an observation not yet available."""


@dataclass(frozen=True)
class Binding:
    source: str
    key: str = ""
    value: Any = None

    def __post_init__(self):
        if self.source not in {"input", "observation", "constant"}:
            raise ValueError("arguments may originate only in inputs, past observations or constants")
        if self.source != "constant" and (not isinstance(self.key, str) or not self.key):
            raise ValueError("a concrete input/observation key is required")

    def resolve(self, inputs, observations):
        if self.source == "constant":
            return self.value
        state = inputs if self.source == "input" else observations
        if self.key not in state:
            raise MissingEvidence(f"unavailable {self.source}: {self.key}")
        return state[self.key]


@dataclass(frozen=True)
class Guard:
    binding: Binding
    operator: str
    value: Any = None

    def __post_init__(self):
        if self.operator not in {"eq", "ne", "exists"}:
            raise ValueError("this explicit IR subset supports eq, ne and exists guards")

    def holds(self, inputs, observations):
        try:
            actual = self.binding.resolve(inputs, observations)
        except MissingEvidence:
            if self.operator == "exists":
                return False
            raise
        if self.operator == "exists":
            return True
        # Boolean true and integer one are distinct typed states.
        equal = type(actual) is type(self.value) and actual == self.value
        return equal if self.operator == "eq" else not equal


@dataclass(frozen=True)
class Rule:
    identity: str
    guard: Guard
    tool: str
    arguments: tuple[tuple[str, Binding], ...]
    citations: tuple[str, ...]
    witnessed: bool = True

    def __post_init__(self):
        if (not isinstance(self.identity, str) or not self.identity or not self.tool
                or not self.citations or not all(isinstance(x, str) and x for x in self.citations)
                or type(self.witnessed) is not bool):
            raise ValueError("identified rules need explicit supporting SOP/trace citations")
        if len({name for name, _ in self.arguments}) != len(self.arguments):
            raise ValueError("duplicate argument names")


@dataclass(frozen=True)
class ToolCall:
    rule_id: str
    tool: str
    arguments: object
    witnessed: bool


class DecisionList:
    def __init__(self, completion: Guard, rules, tool_schemas):
        self.completion, self.rules = completion, tuple(rules)
        if not self.rules or len({row.identity for row in self.rules}) != len(self.rules):
            raise ValueError("a nonempty decision list with unique rule IDs is required")
        self.tool_schemas = {key: dict(value) for key, value in tool_schemas.items()}
        supported = {"string", "integer", "number", "boolean"}
        for rule in self.rules:
            schema = self.tool_schemas.get(rule.tool)
            if schema is None or any(value not in supported for value in schema.values()):
                raise ValueError("declared typed tool schema required")
            if {key for key, _ in rule.arguments} != set(schema):
                raise ValueError("rule arguments must match the declared tool signature")

    def next_call(self, *, inputs, observations):
        """Choose the first satisfied rule using only observations already supplied.

        This method emits a call; it does not execute tools. In particular it does
        not infer missing observations, call a model, or evaluate arbitrary Python.
        """
        if self.completion.holds(inputs, observations):
            return None
        for rule in self.rules:
            if not rule.guard.holds(inputs, observations):
                continue
            args = {key: binding.resolve(inputs, observations) for key, binding in rule.arguments}
            for key, kind in self.tool_schemas[rule.tool].items():
                allowed = {"string": {str}, "integer": {int}, "boolean": {bool}, "number": {int, float}}[kind]
                if type(args[key]) not in allowed:
                    raise ValueError(f"argument {key} violates type {kind}")
            return ToolCall(rule.identity, rule.tool, MappingProxyType(args), rule.witnessed)
        raise MissingEvidence("no supported rule applies; do not invent a branch")


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("ReTrace IR dispatch is CPU-only")
    rule = Rule("disable", Guard(Binding("observation", "airplane"), "eq", True),
                "toggle", (("enabled", Binding("constant", value=False)),), ("trace-1:step-2",))
    ir = DecisionList(Guard(Binding("observation", "done"), "eq", True), (rule,),
                      {"toggle": {"enabled": "boolean"}})
    selected = ir.next_call(inputs={}, observations={"done": False, "airplane": True})
    unknown_rejected = False
    try:
        ir.next_call(inputs={}, observations={"done": False})
    except MissingEvidence:
        unknown_rejected = True
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"decision_rules": len(ir.rules), "runtime_planner_calls": 0},
            "checks": {"guard_selects_typed_tool": selected.tool == "toggle" and selected.arguments["enabled"] is False,
                       "completion_stops_dispatch": ir.next_call(inputs={}, observations={"done": True}) is None,
                       "unseen_observation_not_invented": unknown_rejected,
                       "source_support_retained": rule.citations == ("trace-1:step-2",)}}
