"""ENGRAM v1 admission and verification gates, without model training or retrieval."""

from __future__ import annotations

import random
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Experience:
    key: str
    episode: str
    skills: tuple[str, ...]
    category: str
    order: int
    source: Literal["student", "teacher_demo", "correction"]
    succeeded: bool
    aligned_action: bool
    public_context: str = ""

    @property
    def usable_for_training(self) -> bool:
        return self.aligned_action and (self.succeeded or self.source == "correction")


@dataclass(frozen=True)
class SkillState:
    mastery: float
    previous_mastery: float | None = None


@dataclass(frozen=True)
class Probe:
    key: str
    episode: str
    skill: str
    public_input: str
    target: str


@dataclass(frozen=True)
class Approval:
    candidate: str
    retrieval: bool


@dataclass(frozen=True)
class Decision:
    skill: str
    admitted: bool
    participated: bool
    records: int
    demonstrations: int
    probes: int
    weights_score: float | None = None
    memory_score: float | None = None
    hybrid_score: float | None = None
    released: bool = False
    hybrid_activated: bool = False


@dataclass(frozen=True)
class Result:
    decisions: tuple[Decision, ...]
    approvals: tuple[tuple[str, Approval], ...]
    retrievable: tuple[Experience, ...]
    archived: tuple[Experience, ...]


@dataclass(frozen=True)
class Thresholds:
    mastery: float = 0.8
    records: int = 2
    mastery_increase: float = 0.1
    demonstrations: int = 2
    margin: float = 0.0
    floor: float = 0.5
    residual: int = 1

    def __post_init__(self) -> None:
        _bounded(self.mastery, 0, 1)
        _bounded(self.mastery_increase, 0, 1)
        _bounded(self.margin, -1, 1)
        _bounded(self.floor, 0, 1)
        if (
            any(type(value) is not int or value < 0 for value in (self.records, self.residual))
            or type(self.demonstrations) is not int or self.demonstrations < 1
        ):
            raise ValueError("invalid record, demonstration or residual count")


Actor = Callable[[str, tuple[str, ...]], str]
Grader = Callable[[str, str], bool]
Retriever = Callable[[str, tuple[Experience, ...]], tuple[str, ...]]


def _bounded(value: float, lower: int, upper: int) -> Fraction:
    if type(value) not in (float, int) or not lower <= value <= upper:
        raise ValueError("invalid probability or margin")
    return Fraction(str(value))


def _unique(keys: tuple[str, ...], description: str) -> set[str]:
    if any(not isinstance(key, str) or not key for key in keys) or len(set(keys)) != len(keys):
        raise ValueError(f"invalid or duplicate {description}")
    return set(keys)


def consolidate(
    *,
    experiences: tuple[Experience, ...],
    skills: Mapping[str, SkillState],
    probes: tuple[Probe, ...],
    trained_ids: tuple[str, ...],
    candidate: str,
    training_succeeded: bool,
    loading_succeeded: bool,
    weights_actor: Actor,
    base_actor: Actor,
    retrieve: Retriever,
    grade: Grader,
    previous: Mapping[str, Approval] | None = None,
    replay_episodes: frozenset[str] = frozenset(),
    held_out_episodes: frozenset[str] = frozenset(),
    hybrid_actor: Actor | None = None,
    thresholds: Thresholds = Thresholds(),
) -> Result:
    """Apply Eqs. 2 and 6 to one externally trained candidate.

    The caller attests which current records supplied valid training examples.
    Retrieval sees only the pre-release store, never Probe objects or replay.
    Actors see strings and public context; only the grader receives the target.
    No mutation, actual fitting, model loading, or automatic retry is performed.
    """
    keys = _unique(tuple(row.key for row in experiences), "experience IDs")
    _unique(tuple(probe.key for probe in probes), "probe IDs")
    _unique(tuple(skills), "skill IDs")
    trained = _unique(trained_ids, "current training IDs")
    if not trained <= keys or not candidate:
        raise ValueError("invalid training receipt")
    if type(training_succeeded) is not bool or type(loading_succeeded) is not bool:
        raise ValueError("invalid training or loading status")
    previous = dict(previous or {})
    if not previous.keys() <= skills.keys():
        raise ValueError("approval refers to unknown skill")
    reserved_episodes = {row.episode for row in probes}
    if (reserved_episodes | replay_episodes) & held_out_episodes or reserved_episodes & replay_episodes:
        raise ValueError("evaluation episode overlaps another split")
    if any(not row.episode or row.skill not in skills for row in probes):
        raise ValueError("probe requires a known skill and originating episode")
    for row in experiences:
        if (not row.episode or not row.category or row.episode in held_out_episodes
                or not row.skills or not _unique(row.skills, "experience skills") <= skills.keys()
                or row.source not in ("student", "teacher_demo", "correction")
                or type(row.order) is not int or type(row.succeeded) is not bool
                or type(row.aligned_action) is not bool):
            raise ValueError("invalid experience provenance")
        if row.key in trained and (row.episode in reserved_episodes or not row.usable_for_training):
            raise ValueError("training receipt includes a reserved episode or unusable action")

    admission: dict[str, tuple[bool, int, int]] = {}
    for skill, state in skills.items():
        mastery = _bounded(state.mastery, 0, 1)
        repeat = state.previous_mastery is None or (
            mastery - _bounded(state.previous_mastery, 0, 1) >= _bounded(thresholds.mastery_increase, 0, 1)
        )
        records = [row for row in experiences if skill in row.skills]
        demos = sum(row.source == "teacher_demo" and row.succeeded for row in records)
        admitted = (
            mastery >= _bounded(thresholds.mastery, 0, 1) and len(records) >= thresholds.records and repeat
        ) or demos >= thresholds.demonstrations
        admission[skill] = (admitted, len(records), demos)
    for row in experiences:
        if row.key in trained and not any(admission[skill][0] for skill in row.skills):
            raise ValueError("training receipt includes a record with no admitted skill")

    def hit(output: str, target: str) -> int:
        decision = grade(output, target)
        if type(decision) is not bool:
            raise ValueError("the shared probe grader must return a binary boolean")
        return int(decision)

    floor = _bounded(thresholds.floor, 0, 1)
    margin = _bounded(thresholds.margin, -1, 1)
    approvals = previous.copy()
    decisions = []
    released = set()
    for skill, (admitted, count, demos) in admission.items():
        participated = admitted and any(row.key in trained and skill in row.skills for row in experiences)
        local_probes = tuple(probe for probe in probes if probe.skill == skill)
        size = len(local_probes)
        prefix = (skill, admitted, participated, count, demos, size)
        if not (training_succeeded and loading_succeeded and participated and size):
            decisions.append(Decision(*prefix))
            continue
        contexts = tuple(retrieve(probe.public_input, experiences) for probe in local_probes)
        if any(not isinstance(context, tuple) or not all(isinstance(item, str) for item in context)
               for context in contexts):
            raise ValueError("retrieval must return a tuple of public strings")
        weights_score = Fraction(
            sum(hit(weights_actor(probe.public_input, ()), probe.target) for probe in local_probes), size,
        )
        memory_score = Fraction(sum(
            hit(base_actor(probe.public_input, context), probe.target)
            for probe, context in zip(local_probes, contexts, strict=True)
        ), size)
        release = weights_score - memory_score >= margin and weights_score > floor
        hybrid_score = None
        activate = False
        if release:
            released.add(skill)
            approvals[skill] = Approval(candidate, retrieval=False)
        elif hybrid_actor is not None:
            hybrid_score = Fraction(sum(
                hit(hybrid_actor(probe.public_input, context), probe.target)
                for probe, context in zip(local_probes, contexts, strict=True)
            ), size)
            activate = hybrid_score > memory_score and hybrid_score > floor
            if activate:
                approvals[skill] = Approval(candidate, retrieval=True)
        decisions.append(Decision(
            *prefix, float(weights_score), float(memory_score),
            None if hybrid_score is None else float(hybrid_score), release, activate,
        ))

    # Shared records are retained unless every associated skill independently
    # releases this round. This conservative rule protects rejected skills.
    eligible = tuple(row for row in experiences if row.key in trained and set(row.skills) <= released)
    protected: set[str] = set()
    for skill in released:
        categories = {row.category for row in eligible if skill in row.skills}
        for category in categories:
            ordered = sorted(
                (row for row in eligible if skill in row.skills and row.category == category),
                key=lambda row: (-row.order, row.key),
            )
            protected.update(row.key for row in ordered[:thresholds.residual])
    archive_ids = {row.key for row in eligible} - protected
    return Result(
        tuple(decisions), tuple(sorted(approvals.items())),
        tuple(row for row in experiences if row.key not in archive_ids),
        tuple(row for row in experiences if row.key in archive_ids),
    )


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Exercise admission, verification, and transactional retention on generated probes."""
    if device != "cpu":
        raise ValueError("ENGRAM gate diagnostic is CPU-only")
    rng = random.Random(seed)
    names = ("release", "floor", "relative", "empty", "no-participation")
    experiences = tuple(
        Experience(f"{skill}-{index}", f"acq-{skill}-{index}", (skill,), "action", index,
                   "teacher_demo", True, skill != "no-participation", f"public {skill}")
        for skill in names for index in range(3)
    ) + (Experience("shared", "acq-shared", ("release", "floor"), "action", 5, "student", True, True),)
    probes = tuple(
        Probe(f"{skill}-{index}", f"dev-{skill}-{index}", skill, f"{skill}:{index}:{a}:{b}", str(a + b))
        for skill in names if skill != "empty"
        for index, (a, b) in enumerate((rng.randrange(9), rng.randrange(9)) for _ in range(4))
    )

    def solve(prompt: str, context: tuple[str, ...], arm: str) -> str:
        if bool(context) != (arm != "weights"):
            raise AssertionError("unexpected episodic context")
        skill, index, a, b = prompt.split(":")
        cutoff = {
            "weights": {"release": 3, "floor": 2, "relative": 3},
            "base": {"release": 2, "floor": 1, "relative": 4},
            "hybrid": {"release": 3, "floor": 3, "relative": 4},
        }[arm][skill]
        return str(int(a) + int(b) + (int(index) >= cutoff))

    args = dict(
        experiences=experiences, skills=dict.fromkeys(names, SkillState(0.0, 0.0)),
        probes=probes, trained_ids=tuple(row.key for row in experiences if row.usable_for_training),
        candidate="candidate", weights_actor=lambda prompt, context: solve(prompt, context, "weights"),
        base_actor=lambda prompt, context: solve(prompt, context, "base"),
        hybrid_actor=lambda prompt, context: solve(prompt, context, "hybrid"),
        retrieve=lambda prompt, store: (f"{len(store)} pre-release records",),
        grade=lambda prediction, target: prediction == target,
        previous={"relative": Approval("approved-earlier", retrieval=True)},
        thresholds=Thresholds(margin=0.25),
    )
    outcome = consolidate(**args, training_succeeded=True, loading_succeeded=True)
    failed = consolidate(**args, training_succeeded=True, loading_succeeded=False)
    rows = {decision.skill: decision for decision in outcome.decisions}
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "metrics": {
            "admitted_skills": sum(row.admitted for row in rows.values()),
            "release_weights_score": rows["release"].weights_score,
            "release_memory_score": rows["release"].memory_score,
            "floor_weights_score": rows["floor"].weights_score,
            "archived_records": len(outcome.archived),
            "retrievable_records": len(outcome.retrievable),
            "synthetic_target_sum": sum(int(probe.target) for probe in probes),
        },
        "checks": {
            "teacher_records_admit_at_zero_mastery": all(row.admitted for row in rows.values()),
            "margin_equality_releases": rows["release"].released,
            "floor_equality_does_not_release": not rows["floor"].released,
            "hybrid_only_activation_preserves_memory": rows["floor"].hybrid_activated
            and all("floor" not in row.skills for row in outcome.archived),
            "relative_failure_keeps_old_approval": dict(outcome.approvals)["relative"] == args["previous"]["relative"],
            "missing_probe_or_current_training_cannot_release": not rows["empty"].released
            and not rows["no-participation"].participated and not rows["no-participation"].released,
            "shared_and_recent_records_stay_retrievable": {"shared", "release-2"} <= {
                row.key for row in outcome.retrievable
            },
            "failed_candidate_is_atomic": failed.retrievable == experiences and not failed.archived
            and dict(failed.approvals) == args["previous"],
        },
    }
