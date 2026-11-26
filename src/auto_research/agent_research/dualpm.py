"""DualPM block/memory callback contracts (2611.33612v1), L0 only.

The caller supplies real reflection, drafting and maintenance models. The local
diagnostic uses controlled callbacks to test plumbing, NOT memory/agent quality.
No scorer, hidden tool configuration, reference plan or future episode is passed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

REQUIRES_GPU_VALIDATION = False
Polarity = Literal["success", "failure"]


def _text(value: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError("nonblank text required")


def _tuple_text(values: tuple[str, ...], *, allow_empty: bool = True) -> None:
    if type(values) is not tuple or (not values and not allow_empty):
        raise ValueError("immutable text tuple required")
    for value in values:
        _text(value)
    if len(set(values)) != len(values):
        raise ValueError("duplicate references/evidence")


@dataclass(frozen=True)
class VisibleEpisode:
    episode_id: str
    task: str
    instructions: tuple[str, ...]
    visible_steps: tuple[str, ...]
    final_answer: str

    def __post_init__(self) -> None:
        for value in (self.episode_id, self.task, self.final_answer):
            _text(value)
        _tuple_text(self.instructions)
        # Repeated visible actions are valid and must not be silently removed.
        if type(self.visible_steps) is not tuple:
            raise ValueError("immutable visible steps required")
        for step in self.visible_steps:
            _text(step)


@dataclass(frozen=True)
class Lesson:
    polarity: Polarity
    title: str
    content: str
    evidence: tuple[str, ...]
    applicability: str
    confidence: Literal["low", "medium", "high"]

    def __post_init__(self) -> None:
        if self.polarity not in ("success", "failure") or self.confidence not in ("low", "medium", "high"):
            raise ValueError("invalid polarity/confidence")
        for value in (self.title, self.content, self.applicability):
            _text(value)
        _tuple_text(self.evidence, allow_empty=False)


@dataclass(frozen=True)
class Draft:
    lesson: Lesson
    episode_ref: str


@dataclass(frozen=True)
class MemoryClaim:
    lesson: Lesson
    source_memory_refs: tuple[str, ...]
    source_draft_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _tuple_text(self.source_memory_refs)
        _tuple_text(self.source_draft_refs)


@dataclass(frozen=True)
class DraftRequest:
    episode: VisibleEpisode
    reflection: str
    draft_limit: int


@dataclass(frozen=True)
class MaintenanceRequest:
    polarity: Polarity
    memories: tuple[tuple[str, Lesson], ...]
    drafts: tuple[tuple[str, Draft], ...]
    pool_limit: int
    evidence_limit: int


class DualPM:
    """One frozen memory snapshot per block; atomic two-polarity maintenance.

    Models receive immutable, typed requests. Syntactic provenance is checked;
    semantic grounding, causal correctness and future utility are NOT checked.
    Callbacks are trusted Python code, not process-isolated adversaries.
    """

    def __init__(self, reflect: Callable[[VisibleEpisode], str],
                 draft: Callable[[DraftRequest], tuple[Lesson, ...]],
                 maintain: Callable[[MaintenanceRequest], tuple[MemoryClaim, ...]],
                 *, draft_limit: int = 2, pool_limit: int = 10, evidence_limit: int = 3):
        for value in (draft_limit, pool_limit, evidence_limit):
            if type(value) is not int or value < 1:
                raise ValueError("positive integer capacities required")
        if not all(callable(callback) for callback in (reflect, draft, maintain)):
            raise ValueError("three explicit model callbacks required")
        self.reflect, self.draft, self.maintain = reflect, draft, maintain
        self.draft_limit, self.pool_limit, self.evidence_limit = draft_limit, pool_limit, evidence_limit
        self._pools: tuple[tuple[Lesson, ...], tuple[Lesson, ...]] = ((), ())
        self._seen: frozenset[str] = frozenset()
        self._active: tuple[Lesson, ...] | None = None

    @property
    def memory(self) -> tuple[Lesson, ...]:
        return self._pools[0] + self._pools[1]

    def begin_block(self) -> tuple[Lesson, ...]:
        if self._active is not None:
            raise ValueError("a block is already active")
        self._active = self.memory
        return self._active

    def finish_block(self, episodes: tuple[VisibleEpisode, ...]) -> tuple[Lesson, ...]:
        if self._active is None:
            raise ValueError("begin a frozen-memory block first")
        if type(episodes) is not tuple or not episodes or any(type(e) is not VisibleEpisode for e in episodes):
            raise ValueError("completed visible episodes required")
        ids = tuple(e.episode_id for e in episodes)
        if len(set(ids)) != len(ids) or self._seen.intersection(ids):
            raise ValueError("episode replay is not a new prequential observation")
        drafts: dict[str, list[Draft]] = {"success": [], "failure": []}
        for index, episode in enumerate(episodes):
            reflection = self.reflect(episode)
            _text(reflection)
            lessons = self.draft(DraftRequest(episode, reflection, self.draft_limit))
            if type(lessons) is not tuple or any(type(lesson) is not Lesson for lesson in lessons):
                raise ValueError("draft model must return an immutable Lesson tuple")
            for polarity in ("success", "failure"):
                local = [lesson for lesson in lessons if lesson.polarity == polarity]
                if len(local) > self.draft_limit:
                    raise ValueError("draft limit exceeded for a polarity")
                drafts[polarity].extend(Draft(lesson, f"E{index}") for lesson in local)
        updated = []
        for polarity, previous in zip(("success", "failure"), self._pools):
            request = MaintenanceRequest(polarity,
                tuple((f"M{i}", value) for i, value in enumerate(previous)),
                tuple((f"D{i}", value) for i, value in enumerate(drafts[polarity])),
                self.pool_limit, self.evidence_limit)
            claims = self.maintain(request)
            if type(claims) is not tuple or len(claims) > self.pool_limit:
                raise ValueError("maintenance must return a bounded immutable complete pool")
            memory_refs, draft_refs = {k for k, _ in request.memories}, {k for k, _ in request.drafts}
            for claim in claims:
                if type(claim) is not MemoryClaim or type(claim.lesson) is not Lesson:
                    raise ValueError("typed memory claim required")
                if claim.lesson.polarity != polarity or len(claim.lesson.evidence) > self.evidence_limit:
                    raise ValueError("cross-polarity or over-capacity evidence")
                if not set(claim.source_memory_refs) <= memory_refs or not set(claim.source_draft_refs) <= draft_refs:
                    raise ValueError("source references must be call-local and same-polarity")
                if not claim.source_memory_refs and not claim.source_draft_refs:
                    raise ValueError("a new memory requires at least one current draft")
            updated.append(tuple(claim.lesson for claim in claims))
        # No partial pool writes if any model or contract validation fails.
        self._pools = (updated[0], updated[1])
        self._seen = self._seen.union(ids)
        self._active = None
        return self.memory


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Controlled callback execution proves L0 wiring, not learned lessons."""
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    calls = []
    def reflection(episode: VisibleEpisode) -> str:
        calls.append("reflect")
        return "Controlled observation: " + episode.visible_steps[-1]
    def drafting(request: DraftRequest) -> tuple[Lesson, ...]:
        calls.append("draft")
        return tuple(Lesson(p, "Controlled lesson", "Use visible tool outcomes only.",
                           (request.reflection,), "tool use: visible outcome", "low") for p in ("success", "failure"))
    def maintenance(request: MaintenanceRequest) -> tuple[MemoryClaim, ...]:
        calls.append(request.polarity)
        return tuple(MemoryClaim(d.lesson, (), (ref,)) for ref, d in request.drafts)
    workflow = DualPM(reflection, drafting, maintenance)
    frozen = workflow.begin_block()
    episode = VisibleEpisode(f"episode-{seed}", "Inspect a toy tool output", ("Use only visible observations",),
                             ("tool returned an explicit response",), "Observed response")
    memory = workflow.finish_block((episode,))
    rejected = False
    bad = DualPM(reflection, drafting, lambda request: (
        MemoryClaim(Lesson(request.polarity, "x", "x", ("visible",), "tool: visible", "low"), (), ("D999",)),))
    bad.begin_block()
    try:
        bad.finish_block((episode,))
    except ValueError:
        rejected = True
    checks = {"cold_start_empty": frozen == (), "block_snapshot_unchanged": frozen == (),
              "reflect_precedes_draft": calls[:2] == ["reflect", "draft"],
              "both_polarities_maintained": {m.polarity for m in memory} == {"success", "failure"},
              "foreign_reference_rejected": rejected, "invalid_update_is_atomic": bad.memory == (),
              "episode_has_no_hidden_fields": set(episode.__dataclass_fields__) == {
                  "episode_id", "task", "instructions", "visible_steps", "final_answer"}}
    return {"seed": seed, "device": "cpu", "evaluation_tier": "l0_interface", "diagnostic_only": True,
            "checks": checks, "metrics": {"maintained_memories": len(memory), "successful_contract_checks": sum(checks.values())}}
