"""ARE-bench actor/evaluator contract and exact metrics, not its private task set."""
from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class TaskInput:
    identity: str
    background: str
    requirements: str
    environment: str
    workspace_files: tuple[str, ...]

    def __post_init__(self):
        if (not all(isinstance(value, str) and value for value in (
                self.identity, self.background, self.requirements, self.environment))
                or not isinstance(self.workspace_files, tuple)
                or not all(isinstance(value, str) for value in self.workspace_files)):
            raise ValueError("identified task context and immutable workspace references required")

    def actor_payload(self):
        """The actor never receives rubric/checklist verdicts through this interface."""
        return {"id": self.identity, "background": self.background,
                "requirements": self.requirements, "environment": self.environment,
                "workspace_files": list(self.workspace_files)}


@dataclass(frozen=True)
class ChecklistVerdict:
    task_id: str
    expected_item_ids: tuple[str, ...]
    decisions: tuple[tuple[str, bool], ...]

    def __post_init__(self):
        items = self.expected_item_ids
        if (not self.task_id or not items or len(set(items)) != len(items)
                or not all(isinstance(x, str) and x for x in items)):
            raise ValueError("an empty checklist is a construction error, never a perfect score")
        if (len(self.decisions) != len(items)
                or {key for key, _ in self.decisions} != set(items)
                or not all(type(value) is bool for _, value in self.decisions)):
            raise ValueError("exactly one binary verdict is required for every checklist item")


def score(verdicts):
    """Equations 6-7: strict task conjunction and task-macro checklist score."""
    rows = tuple(verdicts)
    if (not rows or not all(isinstance(row, ChecklistVerdict) for row in rows)
            or len({row.task_id for row in rows}) != len(rows)):
        raise ValueError("nonempty unique task verdicts required per evaluation round")
    return {
        "instance_success_rate": sum(all(value for _, value in row.decisions) for row in rows) / len(rows),
        "checklist_success_rate": math.fsum(
            sum(value for _, value in row.decisions) / len(row.decisions) for row in rows) / len(rows),
        "tasks": len(rows), "checklist_items": sum(len(row.decisions) for row in rows),
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("ARE-bench scoring protocol is CPU-only")
    task = TaskInput("a", "Keep the validation split fixed.", "Repair the parser.", "CPU only.",
                     ("parser.py", "failed-run.json"))
    a = ChecklistVerdict("a", ("repair", "preserve-split"), (("repair", True), ("preserve-split", False)))
    b = ChecklistVerdict("b", ("deliver",), (("deliver", True),))
    metrics = score((a, b))
    empty_rejected = False
    try:
        ChecklistVerdict("empty", (), ())
    except ValueError:
        empty_rejected = True
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": metrics,
            "checks": {"strict_conjunction": metrics["instance_success_rate"] == .5,
                       "task_macro_not_item_micro": metrics["checklist_success_rate"] == .75,
                       "rubric_excluded_from_actor_payload": set(task.actor_payload()) == {
                           "id", "background", "requirements", "environment", "workspace_files"},
                       "existing_workspace_preserved": task.actor_payload()["workspace_files"] == [
                           "parser.py", "failed-run.json"],
                       "empty_checklist_is_error": empty_rejected}}
