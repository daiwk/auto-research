"""Auditable FIFO/embargo and bounded scorer for RSLiveBench-UAV v1.

Not a UAV acquisition system, released benchmark dataset, or VLM evaluator. Only
externally supplied, timestamped observations and predictions enter this module.
"""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import datetime
import re
from typing import Mapping, Sequence

REQUIRES_GPU_VALIDATION = False


def _aware(value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamps must include a timezone")


@dataclass(frozen=True)
class Scene:
    scene_id: str
    captured_at: datetime
    first_release_at: datetime

    def __post_init__(self) -> None:
        _aware(self.captured_at)
        _aware(self.first_release_at)
        if not self.scene_id or self.captured_at >= self.first_release_at:
            raise ValueError("a named scene must be captured before its first release")


@dataclass(frozen=True)
class RollingWindow:
    """Four scenes in admission order; the earliest admitted is retired next."""

    released_at: datetime
    scenes: tuple[Scene, ...]

    def __post_init__(self) -> None:
        _aware(self.released_at)
        if len(self.scenes) != 4 or len({s.scene_id for s in self.scenes}) != 4:
            raise ValueError("a complete release has four distinct scenes")
        dates = [s.first_release_at for s in self.scenes]
        if dates != sorted(dates) or any(d > self.released_at for d in dates):
            raise ValueError("scene roster must be in admission order")

    def advance(self, incoming: Scene, released_at: datetime) -> tuple[RollingWindow, Scene]:
        _aware(released_at)
        if released_at <= self.released_at:
            raise ValueError("release timestamps must increase")
        if not self.released_at < incoming.captured_at < released_at:
            raise ValueError("incoming images must be captured strictly between releases")
        if incoming.first_release_at != released_at:
            raise ValueError("incoming scene must first appear in this release")
        if incoming.scene_id in {s.scene_id for s in self.scenes}:
            raise ValueError("an active scene cannot be reintroduced as fresh")
        return RollingWindow(released_at, (*self.scenes[1:], incoming)), self.scenes[0]


def disclosure_allowed(
    *, first_release: datetime, retired_at: datetime | None, now: datetime
) -> bool:
    """Paper embargo = max(retirement, first release + FOUR CALENDAR months)."""
    _aware(first_release)
    _aware(now)
    if retired_at is None:
        return False
    _aware(retired_at)
    if retired_at < first_release:
        raise ValueError("retirement cannot predate first release")
    month_index = first_release.year * 12 + first_release.month - 1 + 4
    year, month_zero = divmod(month_index, 12)
    month = month_zero + 1
    minimum = first_release.replace(
        year=year, month=month,
        day=min(first_release.day, calendar.monthrange(year, month)[1]),
    )
    return now >= max(retired_at, minimum)


def strict_count_mra(prediction: str, reference: int) -> float:
    """SC decimal-only parser and 10 relative-error thresholds, score in [0,100].

Zero is a valid parsed count. The paper defines relative MRA for positive
references, so zero reference is refused rather than assigned an invented rule.
    """
    if type(reference) is not int or reference <= 0:
        raise ValueError("relative-error MRA requires a positive reference")
    if not isinstance(prediction, str) or re.fullmatch(r"[0-9]+", prediction) is None:
        return 0.0
    count = int(prediction)
    return 10.0 * sum(100 * abs(count - reference) <= 5 * k * reference for k in range(1, 11))


@dataclass(frozen=True)
class QuestionSpec:
    question_id: str
    group: str
    task: str
    component: str


def aggregate_scores(
    protocol: Sequence[QuestionSpec], scores: Mapping[str, float | None],
    *, expected_groups: Sequence[str],
) -> dict[str, object]:
    """Pool within component, then equally average components/tasks/four groups.

``None`` means an actually returned but unparseable prediction (score zero).
An absent key means not evaluated and suppresses the official overall result.
No question's answer is used by the policy; scoring is a separate input here.
    """
    if len(expected_groups) != 4 or len(set(expected_groups)) != 4:
        raise ValueError("the official protocol declares four distinct capability groups")
    ids = [q.question_id for q in protocol]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("protocol question IDs must be nonempty and unique")
    if set(scores).difference(ids):
        raise ValueError("unknown prediction IDs must not enter aggregation")
    if any(q.group not in expected_groups for q in protocol):
        raise ValueError("question has an undeclared capability group")
    if set(q.group for q in protocol) != set(expected_groups):
        raise ValueError("every declared group needs task coverage")
    components: dict[tuple[str, str, str], list[float]] = {}
    missing_components: set[tuple[str, str, str]] = set()
    for question in protocol:
        key = question.group, question.task, question.component
        components.setdefault(key, [])
        if question.question_id not in scores:
            missing_components.add(key)
            continue
        value = scores[question.question_id]
        if value is not None and (not isinstance(value, (float, int)) or not 0 <= value <= 100):
            raise ValueError("component scores must be finite and in [0,100]")
        components[key].append(0.0 if value is None else float(value))
    component_scores = {
        key: None if key in missing_components else sum(values) / len(values)
        for key, values in components.items()
    }
    tasks: dict[tuple[str, str], list[float | None]] = {}
    for (group, task, _), value in component_scores.items():
        tasks.setdefault((group, task), []).append(value)
    task_scores = {
        key: None if None in values else sum(values) / len(values)
        for key, values in tasks.items()
    }
    groups: dict[str, list[float | None]] = {g: [] for g in expected_groups}
    for (group, _), value in task_scores.items():
        groups[group].append(value)
    group_scores = {
        group: None if None in values else sum(values) / len(values)
        for group, values in groups.items()
    }
    values = list(group_scores.values())
    return {
        "overall": None if None in values else sum(values) / 4,
        "group_scores": group_scores,
        "missing_questions": sorted(set(ids).difference(scores)),
        "unparseable_predictions": sum(value is None for value in scores.values()),
        "official_complete": not missing_components,
        "scope": "caller-declared protocol; not the unreleased full 17-task benchmark",
    }


def diagnostic(seed: int, device: str = "cpu") -> dict[str, object]:
    if device != "cpu":
        raise ValueError("this release/scoring protocol supports CPU only")
    from datetime import timezone

    def at(month: int, day: int) -> datetime:
        return datetime(2026, month, day, tzinfo=timezone.utc)

    roster = tuple(Scene(f"old-{i}", at(1, 1), at(1, 2)) for i in range(4))
    next_window, retired = RollingWindow(at(1, 2), roster).advance(
        Scene("fresh", at(2, 1), at(2, 2)), at(2, 2),
    )
    future_rejected = False
    try:
        next_window.advance(Scene("future", at(4, 1), at(4, 2)), at(3, 2))
    except ValueError:
        future_rejected = True
    specs = [QuestionSpec(str(i), str(i), "task", "component") for i in range(4)]
    complete = aggregate_scores(specs, {"0": 100, "1": 50, "2": None, "3": 80}, expected_groups=list("0123"))
    missing = aggregate_scores(specs, {"0": 100, "1": 50, "2": None}, expected_groups=list("0123"))
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
        "checks": {
            "earliest_admitted_scene_is_retired": retired.scene_id == "old-0" and next_window.scenes[-1].scene_id == "fresh",
            "future_capture_rejected": future_rejected,
            "calendar_embargo_not_120_days": not disclosure_allowed(first_release=at(1, 31), retired_at=at(2, 2), now=at(5, 30)),
            "unretired_answers_stay_hidden": not disclosure_allowed(first_release=at(1, 1), retired_at=None, now=at(10, 1)),
            "free_text_not_regex_extracted": strict_count_mra("10 cars", 10) == 0,
            "returned_unparseable_keeps_denominator": complete["overall"] == 57.5,
            "missing_predictions_suppress_overall": missing["overall"] is None,
        },
        "metrics": {"fixture_count_mra": strict_count_mra("8", 10),
                    "fixture_group_macro_score": complete["overall"],
                    "missing_prediction_count": len(missing["missing_questions"])},
    }
