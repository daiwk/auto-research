"""AlphaDiana outcome/session protocol, not a reasoning-agent implementation.

Only PublicTask and a runtime session reach the actor. References remain on the
scoring side. These Python callbacks are trusted integrations, not an OS sandbox.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
import math
import time
from typing import Any


@dataclass(frozen=True)
class PublicTask:
    task_id: str
    problem: str

    def __post_init__(self):
        if not isinstance(self.task_id, str) or not self.task_id or not isinstance(self.problem, str):
            raise ValueError("nonempty task ID and public problem text required")


@dataclass(frozen=True)
class SessionPolicy:
    memory_scope: str = "isolated"
    memory_writable: bool = False
    workers: int = 1
    max_retries: int = 0

    def __post_init__(self):
        if self.memory_scope not in {"isolated", "within_task", "cross_task", "frozen"}:
            raise ValueError("unknown memory scope")
        if (type(self.memory_writable) is not bool or type(self.workers) is not int
                or self.workers < 1 or type(self.max_retries) is not int or self.max_retries < 0):
            raise ValueError("positive workers, nonnegative retries and explicit writable flag required")
        if self.memory_scope == "frozen" and self.memory_writable:
            raise ValueError("frozen memory cannot be writable")
        shared = self.memory_scope in {"within_task", "cross_task"}
        if shared and self.workers != 1:
            raise ValueError("shared sessions must run sequentially")
        if shared and self.memory_writable and self.max_retries:
            raise ValueError("shared writable memory forbids automatic retries")


@dataclass
class SessionState:
    workspace: dict[str, Any] = field(default_factory=dict)
    memory: dict[str, Any] = field(default_factory=dict)


def _tokens(value):
    if value is not None and (type(value) is not int or value < 0):
        raise ValueError("output token count must be nonnegative integer or explicitly unavailable")


@dataclass(frozen=True)
class AgentOutput:
    answer: str
    output_tokens: int | None = None

    def __post_init__(self):
        if not isinstance(self.answer, str):
            raise ValueError("actor answer must be text")
        _tokens(self.output_tokens)


class ExecutionFailure(RuntimeError):
    """An integration may retain observed token usage even when execution fails."""

    def __init__(self, message="execution failed", *, output_tokens=None):
        super().__init__(message)
        _tokens(output_tokens)
        self.output_tokens = output_tokens


@dataclass(frozen=True)
class AttemptRecord:
    task_id: str
    sample_id: str
    attempt: int
    execution_status: str
    score_status: str
    correct: bool | None
    output_tokens: int | None
    elapsed_seconds: float
    failure_kind: str | None = None

    def __post_init__(self):
        if (not isinstance(self.task_id, str) or not self.task_id
                or not isinstance(self.sample_id, str) or not self.sample_id or type(self.attempt) is not int
                or self.attempt < 0 or self.execution_status not in {"completed", "failed"}
                or self.score_status not in {"scored", "unscored"}):
            raise ValueError("valid stable task/sample identity, attempt and statuses required")
        if (type(self.elapsed_seconds) not in (int, float) or not math.isfinite(self.elapsed_seconds)
                or self.elapsed_seconds < 0
                or (self.score_status == "scored") != (type(self.correct) is bool)
                or (self.score_status == "unscored" and self.correct is not None)
                or (self.execution_status == "failed" and self.score_status != "unscored")):
            raise ValueError("execution and scoring status are separate but must be consistent")
        _tokens(self.output_tokens)


class ProtocolRunner:
    """Execute native callbacks synchronously under an explicit scheduling policy.

The caller supplies actor/grader implementations. This adapter neither starts
containers nor implements a parallel worker pool. The workers field validates a
requested scheduling contract; shared sessions are always sequential.
"""

    def __init__(self, policy: SessionPolicy, *, initial_memory=None):
        if type(policy) is not SessionPolicy:
            raise ValueError("validated SessionPolicy required")
        self.policy = policy
        self._initial = deepcopy(dict(initial_memory or {}))
        self._memories: dict[str, dict] = {}
        self.records: list[AttemptRecord] = []
        self._started: set[tuple[str, str]] = set()
        self._active_task: str | None = None

    def run_sample(self, task: PublicTask, sample_id: str, *, actor, grader, reference):
        if type(task) is not PublicTask or not isinstance(sample_id, str) or not sample_id:
            raise ValueError("only a public task and nonempty sample ID may reach execution")
        identity = (task.task_id, sample_id)
        if identity in self._started:
            raise ValueError("sample already requested; retries retain its identity internally")
        self._started.add(identity)
        policy = self.policy
        if policy.memory_scope == "within_task" and self._active_task != task.task_id:
            self._memories.clear()
            self._active_task = task.task_id
        key = task.task_id if policy.memory_scope == "within_task" else "shared"
        for attempt in range(policy.max_retries + 1):
            if policy.memory_scope in {"within_task", "cross_task"}:
                memory = self._memories.setdefault(key, deepcopy(self._initial))
            else:
                memory = self._initial
            # Files reset independently from designated memory; no scorer state enters either.
            session = SessionState(memory=deepcopy(memory))
            started = time.monotonic()
            tokens, correct, failure = None, None, None
            execution, score = "failed", "unscored"
            try:
                output = actor(deepcopy(task), session)
                if type(output) is not AgentOutput:
                    raise ValueError("actor must return AgentOutput")
                tokens, execution = output.output_tokens, "completed"
            except Exception as error:
                tokens = error.output_tokens if isinstance(error, ExecutionFailure) else None
                failure = f"actor:{type(error).__name__}"
            finally:
                if policy.memory_scope in {"within_task", "cross_task"} and policy.memory_writable:
                    # A failed actor may already have written; do not pretend rollback happened.
                    self._memories[key] = deepcopy(session.memory)
            if execution == "completed":
                try:
                    verdict = grader(output.answer, deepcopy(reference))
                    if type(verdict) is not bool:
                        raise ValueError("native correctness scorer must return an explicit bool")
                    correct, score = verdict, "scored"
                except Exception as error:
                    failure = f"grader:{type(error).__name__}"
            record = AttemptRecord(task.task_id, sample_id, attempt, execution, score, correct,
                                   tokens, time.monotonic() - started, failure)
            self.records.append(record)
            if execution == "completed" and score == "scored":
                break
        return record


def summarize(records, *, requested_samples):
    """Latest record per task/sample; all attempts still contribute known costs.

Missing requested samples remain in the denominator. Unknown token capture is
explicit and prevents a falsely complete tokens/correct claim.
"""
    requested = tuple(requested_samples)
    if (not requested or any(not isinstance(x, tuple) or len(x) != 2
            or any(not isinstance(part, str) or not part for part in x) for x in requested)
            or len(set(requested)) != len(requested)):
        raise ValueError("distinct nonempty requested task/sample pairs required")
    rows = tuple(records)
    grouped: dict[tuple[str, str], list[AttemptRecord]] = {}
    for record in rows:
        if type(record) is not AttemptRecord:
            raise ValueError("typed attempt records required")
        identity = record.task_id, record.sample_id
        if identity not in requested:
            raise ValueError("record outside requested sample scope")
        grouped.setdefault(identity, []).append(record)
    latest = []
    for attempts in grouped.values():
        indices = sorted(r.attempt for r in attempts)
        if indices != list(range(len(attempts))):
            raise ValueError("retry indices must be unique and contiguous from zero")
        latest.append(max(attempts, key=lambda r: r.attempt))
    correct = sum(r.correct is True for r in latest)
    scored = sum(r.score_status == "scored" for r in latest)
    captured = sum(r.output_tokens is not None for r in rows)
    known_tokens = sum(r.output_tokens or 0 for r in rows)
    return {"requested_samples": len(requested), "executed_attempts": len(rows),
            "latest_samples": len(latest), "missing_samples": len(requested)-len(latest),
            "scored_samples": scored, "unscored_samples": len(requested)-scored,
            "execution_failed_samples": sum(r.execution_status == "failed" for r in latest),
            "correct_samples": correct, "success_rate_all_requested": correct/len(requested),
            "score_coverage": scored/len(requested), "known_output_tokens_all_attempts": known_tokens,
            "token_recording_coverage": captured/len(rows) if rows else 0.,
            "complete_output_tokens_per_correct": (known_tokens/correct
                if correct and captured == len(rows) else None)}
