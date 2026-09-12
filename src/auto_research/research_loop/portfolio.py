from __future__ import annotations

import datetime as dt
import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class IdeaStage(str, Enum):
    """Durable stages for one independently scheduled research idea."""

    IDEATING = "ideating"
    IMPLEMENTING = "implementing"
    VALIDATING = "validating"
    TRAINING = "training"
    ANALYZING = "analyzing"
    DEBUGGING = "debugging"
    COMPLETE = "complete"
    REJECTED = "rejected"


_TRANSITIONS = {
    IdeaStage.IDEATING: {IdeaStage.IMPLEMENTING, IdeaStage.REJECTED},
    IdeaStage.IMPLEMENTING: {
        IdeaStage.VALIDATING,
        IdeaStage.DEBUGGING,
        IdeaStage.REJECTED,
    },
    IdeaStage.VALIDATING: {
        IdeaStage.TRAINING,
        IdeaStage.DEBUGGING,
        IdeaStage.REJECTED,
    },
    IdeaStage.TRAINING: {
        IdeaStage.ANALYZING,
        IdeaStage.DEBUGGING,
        IdeaStage.REJECTED,
    },
    IdeaStage.ANALYZING: {
        IdeaStage.COMPLETE,
        IdeaStage.IMPLEMENTING,
        IdeaStage.REJECTED,
    },
    IdeaStage.DEBUGGING: {
        IdeaStage.IMPLEMENTING,
        IdeaStage.VALIDATING,
        IdeaStage.TRAINING,
        IdeaStage.REJECTED,
    },
    IdeaStage.COMPLETE: set(),
    IdeaStage.REJECTED: set(),
}


@dataclass
class ResearchIdea:
    idea_id: str
    hypothesis: str
    baseline_id: str
    stage: str = IdeaStage.IDEATING.value
    payload: dict[str, Any] = field(default_factory=dict)
    attempts: int = 0
    last_error: str | None = None
    resume_stage: str | None = None
    owner: str | None = None
    score: float | None = None
    created_at: str = ""
    updated_at: str = ""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _safe_id(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-")
    if not normalized or normalized != value:
        raise ValueError("idea_id must contain only letters, digits, '.', '_' or '-'")
    return normalized


class ResearchPortfolio:
    """Persistent multi-idea controller inspired by A-MLE and Auto-RecSys.

    The controller deliberately owns orchestration rather than model code.  A
    worker claims one idea, invokes the repository's existing implementation,
    evaluator or trainer, and records the resulting transition.  Each idea is
    stored separately so a failed worker cannot corrupt unrelated experiments.
    """

    def __init__(self, root: Path, baseline_id: str):
        if not baseline_id.strip():
            raise ValueError("baseline_id cannot be empty")
        self.root = root
        self.baseline_id = baseline_id
        self.ideas_dir = root / "ideas"
        self.claims_dir = root / "claims"
        self.events_path = root / "events.jsonl"
        self.playbooks_path = root / "playbooks.json"
        self.outcomes_path = root / "outcomes.jsonl"
        self.ideas_dir.mkdir(parents=True, exist_ok=True)
        self.claims_dir.mkdir(parents=True, exist_ok=True)
        metadata = root / "portfolio.json"
        if metadata.exists():
            saved = json.loads(metadata.read_text(encoding="utf-8"))
            if saved["baseline_id"] != baseline_id:
                raise ValueError("baseline_id differs from the persisted portfolio")
        else:
            self._atomic_json(metadata, {"schema_version": 1, "baseline_id": baseline_id})

    def create_idea(
        self,
        idea_id: str,
        hypothesis: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> ResearchIdea:
        idea_id = _safe_id(idea_id)
        if not hypothesis.strip():
            raise ValueError("hypothesis cannot be empty")
        path = self._idea_path(idea_id)
        if path.exists():
            raise ValueError(f"idea already exists: {idea_id}")
        timestamp = _now()
        idea = ResearchIdea(
            idea_id=idea_id,
            hypothesis=hypothesis,
            baseline_id=self.baseline_id,
            payload=dict(payload or {}),
            created_at=timestamp,
            updated_at=timestamp,
        )
        self._save(idea)
        self._event(idea, "created")
        return idea

    def get(self, idea_id: str) -> ResearchIdea:
        path = self._idea_path(_safe_id(idea_id))
        if not path.exists():
            raise KeyError(idea_id)
        return ResearchIdea(**json.loads(path.read_text(encoding="utf-8")))

    def list(self, stages: Iterable[IdeaStage | str] | None = None) -> list[ResearchIdea]:
        allowed = None if stages is None else {IdeaStage(stage).value for stage in stages}
        ideas = [
            ResearchIdea(**json.loads(path.read_text(encoding="utf-8")))
            for path in sorted(self.ideas_dir.glob("*.json"))
        ]
        return [idea for idea in ideas if allowed is None or idea.stage in allowed]

    def claim(self, idea_id: str, owner: str) -> ResearchIdea:
        if not owner.strip():
            raise ValueError("owner cannot be empty")
        idea_id = _safe_id(idea_id)
        idea = self.get(idea_id)
        if idea.stage in {IdeaStage.COMPLETE.value, IdeaStage.REJECTED.value}:
            raise ValueError("terminal ideas cannot be claimed")
        claim_path = self.claims_dir / f"{idea_id}.lock"
        try:
            descriptor = os.open(claim_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError as exc:
            claimed_by = claim_path.read_text(encoding="utf-8").strip() or "another worker"
            if claimed_by != owner:
                raise ValueError(f"idea is already claimed by {claimed_by}") from exc
        else:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(owner + "\n")
                stream.flush()
                os.fsync(stream.fileno())
        idea.owner = owner
        idea.attempts += 1
        idea.updated_at = _now()
        self._save(idea)
        self._event(idea, "claimed", owner=owner)
        return idea

    def release(self, idea_id: str, owner: str) -> ResearchIdea:
        idea = self.get(idea_id)
        if idea.owner != owner:
            raise ValueError("only the current owner can release an idea")
        idea.owner = None
        idea.updated_at = _now()
        self._save(idea)
        (self.claims_dir / f"{idea.idea_id}.lock").unlink(missing_ok=True)
        self._event(idea, "released", owner=owner)
        return idea

    def transition(
        self,
        idea_id: str,
        target: IdeaStage | str,
        *,
        payload_update: dict[str, Any] | None = None,
        score: float | None = None,
    ) -> ResearchIdea:
        idea = self.get(idea_id)
        source = IdeaStage(idea.stage)
        target = IdeaStage(target)
        if target not in _TRANSITIONS[source]:
            raise ValueError(f"invalid idea transition: {source.value} -> {target.value}")
        idea.stage = target.value
        idea.payload.update(payload_update or {})
        idea.score = score if score is not None else idea.score
        idea.last_error = None if target is not IdeaStage.DEBUGGING else idea.last_error
        idea.resume_stage = None if target is not IdeaStage.DEBUGGING else idea.resume_stage
        idea.updated_at = _now()
        self._save(idea)
        self._event(idea, "transition", source=source.value, target=target.value)
        if target in {IdeaStage.COMPLETE, IdeaStage.REJECTED}:
            self._append_jsonl(self.outcomes_path, asdict(idea))
        return idea

    def fail(self, idea_id: str, error: str) -> ResearchIdea:
        idea = self.get(idea_id)
        source = IdeaStage(idea.stage)
        if IdeaStage.DEBUGGING not in _TRANSITIONS[source]:
            raise ValueError(f"stage {source.value} cannot enter debugging")
        idea.stage = IdeaStage.DEBUGGING.value
        idea.resume_stage = source.value
        idea.last_error = error
        idea.owner = None
        idea.updated_at = _now()
        self._save(idea)
        (self.claims_dir / f"{idea.idea_id}.lock").unlink(missing_ok=True)
        self._event(idea, "failed", source=source.value, error=error)
        return idea

    def recover(self, idea_id: str) -> ResearchIdea:
        idea = self.get(idea_id)
        if idea.stage != IdeaStage.DEBUGGING.value or not idea.resume_stage:
            raise ValueError("only a failed debugging idea can be recovered")
        target = IdeaStage(idea.resume_stage)
        if target not in _TRANSITIONS[IdeaStage.DEBUGGING]:
            target = IdeaStage.IMPLEMENTING
        idea.stage = target.value
        idea.last_error = None
        idea.resume_stage = None
        idea.updated_at = _now()
        self._save(idea)
        self._event(idea, "recovered", target=target.value)
        return idea

    def remember_playbook(self, key: str, guidance: str) -> None:
        """Upsert execution guidance learned across runs (the execution loop)."""

        if not key.strip() or not guidance.strip():
            raise ValueError("playbook key and guidance cannot be empty")
        playbooks: dict[str, dict[str, Any]] = {}
        if self.playbooks_path.exists():
            playbooks = json.loads(self.playbooks_path.read_text(encoding="utf-8"))
        previous = playbooks.get(key, {})
        playbooks[key] = {
            "guidance": guidance,
            "observations": int(previous.get("observations", 0)) + 1,
            "updated_at": _now(),
        }
        self._atomic_json(self.playbooks_path, playbooks)

    def related_outcomes(self, hypothesis: str, limit: int = 5) -> list[ResearchIdea]:
        """Retrieve prior idea outcomes by token overlap, then measured score."""

        query = set(re.findall(r"[\w-]+", hypothesis.lower()))
        outcomes: list[ResearchIdea] = []
        if self.outcomes_path.exists():
            for line in self.outcomes_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    outcomes.append(ResearchIdea(**json.loads(line)))

        def rank(idea: ResearchIdea) -> tuple[int, float]:
            tokens = set(re.findall(r"[\w-]+", idea.hypothesis.lower()))
            return len(query & tokens), float("-inf") if idea.score is None else idea.score

        return sorted(outcomes, key=rank, reverse=True)[: max(0, limit)]

    def _idea_path(self, idea_id: str) -> Path:
        return self.ideas_dir / f"{idea_id}.json"

    def _save(self, idea: ResearchIdea) -> None:
        self._atomic_json(self._idea_path(idea.idea_id), asdict(idea))

    def _event(self, idea: ResearchIdea, event: str, **payload: Any) -> None:
        self._append_jsonl(
            self.events_path,
            {
                "timestamp": _now(),
                "idea_id": idea.idea_id,
                "stage": idea.stage,
                "event": event,
                "payload": payload,
            },
        )

    @staticmethod
    def _atomic_json(path: Path, value: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def _append_jsonl(path: Path, value: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o644)
        try:
            line = json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n"
            os.write(descriptor, line.encode("utf-8"))
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
