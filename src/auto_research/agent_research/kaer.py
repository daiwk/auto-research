"""Kaer finite failure channel and seven deterministic repair operators.

Local L1 slice: no LLM planner, endpoint gateway, Cintra or output validator.
Capabilities outside the fixed task policy are rejected; the paper's separate
user-authorization extension is deliberately not implemented. Indices are zero
based (paper k corresponds to local k-1). Only final plans are policy checked.
"""

from __future__ import annotations
from dataclasses import dataclass, replace
from collections.abc import Mapping, Sequence

REQUIRES_GPU_VALIDATION = False
CONDITIONS = frozenset(
    {
        "endpoint_transient_fault",
        "endpoint_access_denied",
        "no_close_out",
        "directive_underspecified",
        "directive_incorrect",
        "capability_not_granted",
        "input_artifact_absent",
        "input_lacks_required_datum",
        "upstream_input_contradicted",
        "information_not_found",
        "constraints_unsatisfiable",
        "result_uncorroborated",
        "budget_exhausted",
    }
)
OPERATORS = frozenset(
    {"re_execute", "revise_directive", "rescope", "reassign", "insert", "prune", "rewire"}
)


def failure_channel(conditions: Sequence[str], *, from_gateway: bool = False) -> tuple[str, ...]:
    """Only finite trusted template IDs cross. No raw report/output argument exists."""
    if type(from_gateway) is not bool or isinstance(conditions, str):
        raise ValueError("typed condition list and source required")
    rows = tuple(conditions)
    if not rows or any(x not in CONDITIONS for x in rows):
        raise ValueError("unknown or empty failure template list")
    if not from_gateway and "no_close_out" in rows:
        raise ValueError("no-close-out is gateway generated, not agent asserted")
    return tuple(dict.fromkeys(rows))


@dataclass(frozen=True)
class Agent:
    capabilities: frozenset[str]
    output_recipients: frozenset[str]

    def __post_init__(self):
        if any(
            not isinstance(x, frozenset) or any(not isinstance(y, str) or not y for y in x)
            for x in (self.capabilities, self.output_recipients)
        ):
            raise ValueError("immutable named capability/recipient sets required")


@dataclass(frozen=True)
class Step:
    agent: str
    capabilities: frozenset[str]
    directive: str
    dependencies: frozenset[int] = frozenset()

    def __post_init__(self):
        if (
            not isinstance(self.agent, str)
            or not self.agent
            or not isinstance(self.directive, str)
            or not self.directive
        ):
            raise ValueError("named agent and nonempty directive required")
        if not isinstance(self.capabilities, frozenset) or any(
            not isinstance(c, str) or not c for c in self.capabilities
        ):
            raise ValueError("immutable capability set required")
        if not isinstance(self.dependencies, frozenset) or any(
            type(i) is not int or i < 0 for i in self.dependencies
        ):
            raise ValueError("immutable nonnegative dependency indices required")


def validate(
    plan: Sequence[Step], registry: Mapping[str, Agent], task_policy: frozenset[str]
) -> None:
    """Paper Eq2 conditions a--d; a valid plan is not proof of correct outputs."""
    if not plan or any(not isinstance(s, Step) for s in plan):
        raise ValueError("nonempty typed plan required")
    if not isinstance(task_policy, frozenset) or any(
        not isinstance(a, Agent) for a in registry.values()
    ):
        raise ValueError("trusted typed registry and immutable task policy required")
    for k, step in enumerate(plan):
        if step.agent not in registry:
            raise ValueError("unknown assigned agent")
        agent = registry[step.agent]
        if not step.capabilities <= agent.capabilities or not step.capabilities <= task_policy:
            raise ValueError(
                "capability exceeds agent or task policy; explicit grants not implemented"
            )
        if any(i >= k for i in step.dependencies):
            raise ValueError("dependencies must precede their consumer")
        if any(
            step.agent not in registry[plan[i].agent].output_recipients for i in step.dependencies
        ):
            raise ValueError("agent output-flow policy violation")
        if k < len(plan) - 1 and not any(k in later.dependencies for later in plan[k + 1 :]):
            raise ValueError("nonfinal subtask output must have a later consumer")


@dataclass(frozen=True)
class Repair:
    operator: str
    target: int
    directive: str | None = None
    capabilities: frozenset[str] | None = None
    agent: str | None = None
    step: Step | None = None
    dependency: int | None = None

    def __post_init__(self):
        if self.operator not in OPERATORS or type(self.target) is not int or self.target < 0:
            raise ValueError("known operator and nonnegative target required")
        fields = {
            "directive": self.directive,
            "capabilities": self.capabilities,
            "agent": self.agent,
            "step": self.step,
            "dependency": self.dependency,
        }
        expected = {
            "re_execute": set(),
            "revise_directive": {"directive"},
            "rescope": {"capabilities"},
            "reassign": {"agent", "capabilities"},
            "insert": {"step"},
            "prune": set(),
            "rewire": {"dependency"},
        }[self.operator]
        if {k for k, v in fields.items() if v is not None} != expected:
            raise ValueError("operator arguments must match its exact signature")


def repair(
    plan: Sequence[Step],
    operators: Sequence[Repair],
    *,
    failed_index: int,
    registry: Mapping[str, Agent],
    task_policy: frozenset[str],
) -> tuple[Step, ...]:
    """Transactional copy; rejects all changes to the completed prefix.

    INSERT/PRUNE renumber dependencies after each operator. Suggested template
    resolutions are guidance, not a deterministic mapping from failure to repair.
    """
    validate(plan, registry, task_policy)
    if type(failed_index) is not int or not 0 <= failed_index < len(plan) or not operators:
        raise ValueError("valid failed position and nonempty repair sequence required")
    rows = list(plan)
    for op in operators:
        if not isinstance(op, Repair):
            raise TypeError("typed deterministic operators required")
        k = op.target
        if k < failed_index or k > len(rows) or (k == len(rows) and op.operator != "insert"):
            raise ValueError("operator target is outside uncompleted suffix")
        if op.operator == "re_execute":
            continue
        if op.operator == "revise_directive":
            rows[k] = replace(rows[k], directive=op.directive)
        elif op.operator == "rescope":
            rows[k] = replace(rows[k], capabilities=op.capabilities)
        elif op.operator == "reassign":
            # This slice carries no progress report or capability grants.
            rows[k] = replace(rows[k], agent=op.agent, capabilities=op.capabilities)
        elif op.operator == "insert":
            if not isinstance(op.step, Step) or any(i >= k for i in op.step.dependencies):
                raise ValueError("inserted subtask may depend only on prior positions")
            rows = [
                replace(s, dependencies=frozenset(i + 1 if i >= k else i for i in s.dependencies))
                for s in rows
            ]
            rows.insert(k, op.step)
        elif op.operator == "prune":
            rows.pop(k)
            rows = [
                replace(
                    s,
                    dependencies=frozenset(i - 1 if i > k else i for i in s.dependencies if i != k),
                )
                for s in rows
            ]
        else:
            i = op.dependency
            if type(i) is not int or not 0 <= i < k:
                raise ValueError("rewire source must precede target")
            rows[k] = replace(rows[k], dependencies=rows[k].dependencies ^ frozenset({i}))
    if tuple(rows[:failed_index]) != tuple(plan[:failed_index]):
        raise ValueError("completed prefix changed")
    validate(rows, registry, task_policy)
    return tuple(rows)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    registry = {
        "reader": Agent(frozenset({"read"}), frozenset({"coder"})),
        "coder": Agent(frozenset({"code"}), frozenset({"coder"})),
    }
    policy = frozenset({"read", "code"})
    plan = (
        Step("reader", frozenset({"read"}), "read inputs"),
        Step("coder", frozenset({"code"}), "compute", frozenset({0})),
    )
    patched = repair(
        plan,
        (Repair("revise_directive", 1, directive="compute from supplied data"),),
        failed_index=1,
        registry=registry,
        task_policy=policy,
    )
    blocked = False
    try:
        repair(
            plan,
            (Repair("rescope", 1, capabilities=frozenset({"terminal"})),),
            failed_index=1,
            registry=registry,
            task_policy=policy,
        )
    except ValueError:
        blocked = True
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "finite_failure_channel_deduplicates": failure_channel(("information_not_found",) * 2)
            == ("information_not_found",),
            "completed_prefix_unchanged": patched[0] == plan[0],
            "original_plan_unmodified": plan[1].directive == "compute",
            "repaired_directive_executed": patched[1].directive == "compute from supplied data",
            "capability_escalation_blocked": blocked,
        },
        "metrics": {
            "template_vocabulary_size": len(CONDITIONS),
            "repair_operator_count": len(OPERATORS),
            "validated_plan_steps": len(patched),
        },
    }
