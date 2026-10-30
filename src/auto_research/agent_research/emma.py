"""EMMA's scoped one-edit/overflow contract, without an LLM or task executor.

Semantic generality, reference-answer leakage and duplicate-role decisions
come from a separate explicit guard service. This module never receives gold
answers and cannot certify that external semantic checks are correct.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from types import MappingProxyType

REQUIRES_GPU_VALIDATION = False

SCOPES = {
    "execution_slip": {"revise_plan", "no_change"},
    "agent_behavior": {"refine_prompt"},
    "procedure": {"revise_skill", "create_skill"},
    "missing_capability": {"create_skill", "create_agent"},
    "routing": {"memory_note", "revise_plan", "create_agent"},
}
LEVELS = {"no_change": "none", "revise_plan": "plan", "memory_note": "controller",
          "refine_prompt": "agent", "create_agent": "agent",
          "revise_skill": "skill", "create_skill": "skill"}


def _text(value, *, limit=None):
    if not isinstance(value, str) or not value.strip() or (limit is not None and len(value) > limit):
        raise ValueError("nonempty bounded text required")
    return value


@dataclass(frozen=True)
class Skill:
    description: str
    content: str

    def __post_init__(self):
        _text(self.description)
        _text(self.content, limit=3000)


@dataclass(frozen=True)
class EpisodicMemory:
    agents: dict[str, str]
    skills: dict[str, Skill] = field(default_factory=dict)
    controller: tuple[tuple[str, str, str], ...] = ()

    def __post_init__(self):
        if "generalist" not in self.agents or not 1 <= len(self.agents) <= 10 or len(self.skills) > 40:
            raise ValueError("one seed generalist, <=10 agents and <=40 skills required")
        for name, prompt in self.agents.items():
            _text(name)
            _text(prompt, limit=6000)
        for name, skill in self.skills.items():
            _text(name)
            if not isinstance(skill, Skill):
                raise ValueError("typed skill records required")
        for topic, content, generality in self.controller:
            _text(topic)
            _text(content)
            if generality not in {"general", "domain_specific", "task_specific"}:
                raise ValueError("explicit controller generality required")
        object.__setattr__(self, "agents", MappingProxyType(dict(self.agents)))
        object.__setattr__(self, "skills", MappingProxyType(dict(self.skills)))
        object.__setattr__(self, "controller", tuple(tuple(row) for row in self.controller))

    def prompt_for(self, name: str):
        if name not in self.agents:
            raise ValueError("agent must exist in the pool")
        return self.agents[name] if name == "generalist" else self.agents["generalist"] + "\n" + self.agents[name]


@dataclass(frozen=True)
class ExternalSafety:
    """External semantic attestations, not a local heuristic claim of safety."""
    reference_answer_absent: bool
    semantic_duplicate_absent: bool
    specialization_genuine: bool
    locator_or_label_role_absent: bool
    dataset_or_run_paths_absent: bool
    structural_split_changed: bool

    def __post_init__(self):
        if any(type(x) is not bool for x in vars(self).values()):
            raise ValueError("explicit native Boolean external safety decisions required")


@dataclass(frozen=True)
class EditContext:
    public_task: str
    participating_agents: frozenset[str]
    failed_levels: tuple[str, ...]
    repeated_step_overflow: bool
    training: bool
    rerun_available: bool
    safety: ExternalSafety

    def __post_init__(self):
        _text(self.public_task)
        if any(type(v) is not bool for v in (self.repeated_step_overflow, self.training, self.rerun_available)):
            raise ValueError("explicit lifecycle/overflow flags required")
        if not isinstance(self.safety, ExternalSafety) or any(x not in set(LEVELS.values()) for x in self.failed_levels):
            raise ValueError("typed safety and chronological failed memory levels required")
        for name in self.participating_agents:
            _text(name)
        object.__setattr__(self, "participating_agents", frozenset(self.participating_agents))
        object.__setattr__(self, "failed_levels", tuple(self.failed_levels))


@dataclass(frozen=True)
class Edit:
    scope: str
    action: str
    target: str = ""
    content: str = ""
    description: str = ""
    generality: str = "general"


@dataclass(frozen=True)
class EditResult:
    memory: EpisodicMemory
    directive: str | None
    required_agent: str | None
    required_skill: str | None


def _task_span_in_artifact(task, artifact):
    words, output = task.split(), artifact.split()
    if len(words) < 15 or len(output) < 15:
        return False
    spans = {tuple(words[i:i + 15]) for i in range(len(words) - 14)}
    return any(tuple(output[i:i + 15]) in spans for i in range(len(output) - 14))


def apply_guarded_edit(memory: EpisodicMemory, edit: Edit, context: EditContext):
    """Table1 + Sec3.2.2: one scoped edit, in fixed guard order.

    No untested final-failure edits; inference writes are refused. Accepted
    durable edits are not rolled back merely because the next attempt fails.
    ``assert_exercised`` checks the required artifact in the actual rerun plan.
    """
    if not context.training or not context.rerun_available:
        raise ValueError("memory frozen at inference / no edit without a remaining rerun")
    if edit.scope not in SCOPES or edit.action not in SCOPES[edit.scope]:
        raise ValueError("scope-action incompatibility")
    if edit.action == "create_agent" and edit.scope == "routing" and not context.repeated_step_overflow:
        raise ValueError("routing creates agents only with overflow evidence")
    level = LEVELS[edit.action]
    if context.repeated_step_overflow and edit.action not in {"create_agent", "revise_plan"}:
        raise ValueError("repeated overflow requires a structural split change")
    if context.repeated_step_overflow and edit.action == "revise_plan" and not context.safety.structural_split_changed:
        raise ValueError("plan directive must change the split, not merely repeat the same attempt")
    if level not in {"none", "plan"} and context.failed_levels[-2:] == (level, level):
        raise ValueError("third consecutive failed edit at one level refused")
    if edit.action == "no_change":
        return EditResult(memory, None, None, None)
    _text(edit.content)
    artifact = edit.target + "\n" + edit.description + "\n" + edit.content
    if not context.safety.reference_answer_absent or _task_span_in_artifact(context.public_task, artifact):
        raise ValueError("answer or verbatim-task leakage guard failed")
    agents, skills, controller = dict(memory.agents), dict(memory.skills), memory.controller
    if edit.action == "refine_prompt":
        if edit.target not in context.participating_agents or edit.target not in agents:
            raise ValueError("only a participating agent can be edited")
        _text(edit.content, limit=6000)
        # Exact complete-line retention; repeated old lines are counted by
        # multiplicity rather than counted repeatedly against one new line.
        from collections import Counter
        old, new = Counter(agents[edit.target].splitlines()), Counter(edit.content.splitlines())
        retained = sum((old & new).values()) / sum(old.values())
        if retained < .6:
            raise ValueError("prompt must retain >=60% of original complete lines")
        agents[edit.target] = edit.content
    if edit.action in {"create_skill", "revise_skill"}:
        _text(edit.target)
        if (edit.action == "create_skill" and (edit.target in skills or len(skills) >= 40)) or (
            edit.action == "revise_skill" and edit.target not in skills
        ):
            raise ValueError("skill identity / pool-cap guard failed")
        skills[edit.target] = Skill(edit.description, edit.content)
    if edit.action == "create_agent":
        _text(edit.target)
        _text(edit.description)
        _text(edit.content, limit=6000)
        if len(edit.content) < 150 or len(agents) >= 10 or edit.target in agents:
            raise ValueError("bounded genuinely new specialization required")
        agents[edit.target] = edit.content
    if edit.action == "memory_note":
        _text(edit.target)
        if edit.generality not in {"general", "domain_specific", "task_specific"}:
            raise ValueError("controller memory generality required")
        controller += ((edit.target, edit.content, edit.generality),)
    if level not in {"none", "plan"} and (
        not context.safety.semantic_duplicate_absent or not context.safety.dataset_or_run_paths_absent
    ):
        raise ValueError("duplicate or dataset/run-path artifact refused")
    if edit.action == "create_agent" and (
        not context.safety.specialization_genuine or not context.safety.locator_or_label_role_absent
    ):
        raise ValueError("new agent must be a genuine narrower method, not a label/locator")
    next_memory = EpisodicMemory(agents, skills, controller)
    required_agent = edit.target if edit.action in {"create_agent", "refine_prompt"} else None
    required_skill = edit.target if edit.action in {"create_skill", "revise_skill"} else None
    return EditResult(next_memory, edit.content if edit.action == "revise_plan" else None,
                      required_agent, required_skill)


def assert_exercised(result: EditResult, *, agents: set[str], skills: set[str]):
    if result.required_agent and result.required_agent not in agents:
        raise ValueError("new/revised agent must actually be named in the rerun plan")
    if result.required_skill and result.required_skill not in skills:
        raise ValueError("new/revised skill must actually be assigned in the rerun plan")


@dataclass(frozen=True)
class Step:
    agent: str
    subtask: str
    skills: tuple[str, ...] = ()

    def __post_init__(self):
        _text(self.agent)
        _text(self.subtask)
        for name in self.skills:
            _text(name)
        object.__setattr__(self, "skills", tuple(self.skills))


def splice_overflow(plan: tuple[Step, ...], index: int, replacements: tuple[Step, ...], memory: EpisodicMemory):
    """Algorithm2: replace unfinished step at same index; preserve finished prefix.

    Decomposition is external. No new agent/skill is invented by this helper.
    The runtime's final-answer/cap policy is not implemented here.
    """
    if type(index) is not int or not 0 <= index < len(plan) or not replacements:
        raise ValueError("valid unfinished step and nonempty decomposition required")
    for step in replacements:
        if not isinstance(step, Step) or step.agent not in memory.agents or not set(step.skills) <= set(memory.skills):
            raise ValueError("decomposition must use only existing agents and skills")
        _text(step.subtask)
    return plan[:index] + replacements + plan[index + 1:]


def diagnostic(seed: int = 42, device: str = "cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("pure CPU structural contract diagnostic")
    memory = EpisodicMemory({"generalist": "check inputs\nverify evidence\nreport uncertainty\nkeep scope\nfinish artifact"})
    safety = ExternalSafety(True, True, True, True, True, True)
    context = EditContext("public task without answers", frozenset({"generalist"}), (), False, True, True, safety)
    edit = Edit("procedure", "create_skill", "verify-units", "Convert units explicitly before combining measured quantities.", "unit conversion")
    result = apply_guarded_edit(memory, edit, context)
    assert_exercised(result, agents={"generalist"}, skills={"verify-units"})
    exercise_rejected = False
    try:
        assert_exercised(result, agents={"generalist"}, skills=set())
    except ValueError:
        exercise_rejected = True
    rejected = 0
    for bad_context, bad_edit in ((replace(context, training=False), edit),
        (replace(context, rerun_available=False), edit),
        (replace(context, failed_levels=("skill", "skill")), edit),
        (replace(context, repeated_step_overflow=True), edit),
        (replace(context, safety=replace(safety, reference_answer_absent=False)), edit),
        (context, replace(edit, scope="agent_behavior"))):
        try:
            apply_guarded_edit(memory, bad_edit, bad_context)
        except ValueError:
            rejected += 1
    plan = (Step("generalist", "done"), Step("generalist", "unfinished"), Step("generalist", "later"))
    split = splice_overflow(plan, 1, (Step("generalist", "part-a"), Step("generalist", "part-b")), memory)
    narrower = "Follow a strict unit-analysis workflow. " * 5
    specialized = apply_guarded_edit(memory, Edit("missing_capability", "create_agent", "units", narrower, "unit analysis"), context).memory
    new_general = dict(specialized.agents)
    new_general["generalist"] += "\nnew shared rule"
    changed = EpisodicMemory(new_general, dict(specialized.skills), specialized.controller)
    return {"seed": seed, "diagnostic_only": True,
        "metrics": {"original_skill_count": len(memory.skills), "updated_skill_count": len(result.memory.skills),
                    "rejected_negative_controls": rejected, "original_plan_steps": len(plan), "split_plan_steps": len(split)},
        "checks": {"one_skill_entry_changed": len(result.memory.skills) == 1 and dict(result.memory.agents) == dict(memory.agents),
                   "old_snapshot_not_mutated": not memory.skills,
                   "six_contract_violations_refused": rejected == 6,
                   "overflow_preserves_completed_prefix": split[:1] == plan[:1],
                   "overflow_preserves_suffix": split[-1:] == plan[-1:],
                   "specialist_inherits_current_generalist": "new shared rule" in changed.prompt_for("units"),
                   "unused_edit_cannot_claim_exercised": exercise_rejected}}
