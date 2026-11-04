"""Meta² deployment-state component, not a learned evolver or agent executor.

Paper: https://arxiv.org/html/2611.05139v1, §3.1/3.3 and Appendix B.2.
Only caller-approved public observations enter checkpoint views. This typed
boundary is not an OS sandbox and cannot detect secrets pasted into text.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from types import MappingProxyType

REQUIRES_GPU_VALIDATION = False
CHANNELS = frozenset({"notice", "instruction", "hook", "tool"})


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("nonempty text required")
    return value


@dataclass(frozen=True)
class MetaSkill:
    text: str
    training_tasks: tuple[str, ...]

    def __post_init__(self):
        _text(self.text)
        tasks = tuple(self.training_tasks)
        if not tasks or len(set(tasks)) != len(tasks):
            raise ValueError("distinct training task identities required")
        for task in tasks:
            _text(task)
        object.__setattr__(self, "training_tasks", tasks)

    @property
    def digest(self):
        return sha256(self.text.encode()).hexdigest()


@dataclass(frozen=True)
class Edit:
    action: str
    channel: str = ""
    content: str = ""

    def __post_init__(self):
        if self.action == "KEEP":
            if self.channel or self.content:
                raise ValueError("KEEP cannot smuggle an edit")
        elif self.action == "EVOLVE":
            if self.channel not in CHANNELS or not _text(self.content):
                raise ValueError("bounded supported edit required")
        else:
            raise ValueError("KEEP or EVOLVE required")


@dataclass(frozen=True)
class Checkpoint:
    task_id: str
    environment_id: str
    instruction: str
    step: int
    trajectory: tuple[str, ...]
    workspace_observations: tuple[str, ...]
    prior_edit_status: str
    edit_status_history: tuple[str, ...]
    terminal_claim: bool
    meta_skill: str
    edits: tuple[Edit, ...]


class DeploymentRun:
    """Frozen knowledge, chronological public deltas and run-local edits.

    Returns an immutable edit state for an external host to load; never executes
    supplied code, modifies a workspace, learns a skill or reads a verifier.
    Terminal EVOLVE keeps the same run alive; terminal KEEP closes it.
    """

    def __init__(self, skill: MetaSkill, task_id: str, environment_id: str,
                 instruction: str, *, edit_limit: int = 4096):
        if not isinstance(skill, MetaSkill) or type(edit_limit) is not int or edit_limit < 1:
            raise ValueError("frozen skill and positive edit bound required")
        if task_id in skill.training_tasks:
            raise ValueError("deployment task overlaps skill training")
        self.skill, self.task_id = skill, _text(task_id)
        self.environment_id, self.instruction = _text(environment_id), _text(instruction)
        self.edit_limit = edit_limit
        self._step, self._trajectory, self._workspace, self._statuses, self._edits = -1, (), (), (), ()
        self._closed = False

    @property
    def state(self):
        return MappingProxyType({"step": self._step, "closed": self._closed,
                                 "edits": self._edits, "meta_skill_sha256": self.skill.digest})

    def checkpoint(self, evidence: dict, evolver):
        allowed = {"step", "trajectory_delta", "workspace_observations", "prior_edit_status", "terminal_claim"}
        if self._closed or not isinstance(evidence, dict) or set(evidence) != allowed:
            raise ValueError("open run and exact public checkpoint schema required")
        step, status, terminal = evidence["step"], evidence["prior_edit_status"], evidence["terminal_claim"]
        if type(step) is not int or step <= self._step or status not in {"none", "loaded", "retained", "rolled_back"} or type(terminal) is not bool:
            raise ValueError("monotone step, observed edit status and terminal flag required")
        if any(not isinstance(evidence[key], (tuple, list)) for key in ("trajectory_delta", "workspace_observations")):
            raise ValueError("explicit public observation sequences required")
        delta, workspace = tuple(evidence["trajectory_delta"]), tuple(evidence["workspace_observations"])
        for text in delta + workspace:
            _text(text)
        trajectory = self._trajectory + delta
        workspace = self._workspace + workspace
        statuses = self._statuses + (status,)
        view = Checkpoint(self.task_id, self.environment_id, self.instruction, step,
                          trajectory, workspace, status, statuses, terminal, self.skill.text, self._edits)
        edit = evolver(view)
        if not isinstance(edit, Edit) or len(edit.content) > self.edit_limit:
            raise ValueError("typed edit exceeds the bounded host channel")
        self._step, self._trajectory, self._workspace, self._statuses = step, trajectory, workspace, statuses
        if edit.action == "EVOLVE":
            self._edits += (edit,)
        elif terminal:
            self._closed = True
        return edit


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU only")
    skill = MetaSkill("Check visible evidence before declaring completion.", ("train-1",))
    run = DeploymentRun(skill, f"heldout-{seed}", "one-environment", "Build an artifact")
    evidence = {"step": 1, "trajectory_delta": ["Artifact not yet present"],
                "workspace_observations": [], "prior_edit_status": "none", "terminal_claim": True}
    run.checkpoint(evidence, lambda _: Edit("EVOLVE", "notice", "Verify the artifact before completion"))
    kept_open = not run.state["closed"]
    run.checkpoint(evidence | {"step": 2, "trajectory_delta": ["Artifact now visible"],
                              "prior_edit_status": "loaded"}, lambda _: Edit("KEEP"))
    fresh = DeploymentRun(skill, f"other-{seed}", "next-environment", "Another task")
    rejected = False
    try:
        fresh.checkpoint(evidence | {"hidden_verifier": "not public"}, lambda _: Edit("KEEP"))
    except ValueError:
        rejected = True
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"accepted_edits": len(run.state["edits"]), "public_checkpoints": 2},
            "checks": {"terminal_evolve_continues": kept_open, "terminal_keep_closes": run.state["closed"],
                       "task_edits_do_not_transfer": not fresh.state["edits"], "unknown_feedback_field_rejected": rejected,
                       "knowledge_unchanged": skill.digest == fresh.skill.digest}}
