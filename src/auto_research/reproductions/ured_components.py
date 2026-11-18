"""Bounded URED candidate mining reference, arXiv:2611.05997v1 §3.

The caller supplies ranker-scored sessions and an observed exposure history;
this module does not train a ranker or simulate a production treatment effect.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Iterable

REQUIRES_GPU_VALIDATION = False
DAY = 86_400


@dataclass(frozen=True)
class Candidate:
    item: str
    category: str
    score: float

    def __post_init__(self) -> None:
        if not all(isinstance(s, str) and s for s in (self.item, self.category)):
            raise ValueError("item and category must be nonempty strings")
        if not isinstance(self.score, (int, float)) or isinstance(self.score, bool) or not math.isfinite(self.score):
            raise ValueError("score must be finite")


@dataclass(frozen=True)
class ScoredSession:
    user: str
    time: int
    candidates: tuple[Candidate, ...]
    shown: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not isinstance(self.user, str) or not self.user or type(self.time) is not int:
            raise ValueError("a user and integer timestamp are required")
        if (not isinstance(self.candidates, tuple) or not all(isinstance(row, Candidate) for row in self.candidates)
                or len({row.item for row in self.candidates}) != len(self.candidates)):
            raise ValueError("a tuple of unique scored items is required")
        if not isinstance(self.shown, frozenset) or not all(isinstance(item, str) and item for item in self.shown):
            raise ValueError("shown must contain explicit item identifiers")


@dataclass(frozen=True)
class Exposure:
    user: str
    time: int
    item: str
    category: str

    def __post_init__(self) -> None:
        if (type(self.time) is not int
                or not all(isinstance(s, str) and s for s in (self.user, self.item, self.category))):
            raise ValueError("an exposure requires user, timestamp, item and category")


def mine_ured(
    user: str,
    as_of: int,
    sessions: Iterable[ScoredSession],
    exposures: Iterable[Exposure],
    *,
    window_days: int = 30,
    discovery_days: int = 15,
    session_limit: int = 200,
    user_limit: int = 10_000,
    recall_limit: int = 1_000,
) -> tuple[Candidate, ...]:
    """Session top-score, user recency dedup/truncation, then novelty and quota.

    Windows are left-closed/right-open in UTC seconds. Exact ties use stable
    item/category ordering; an event at or after as_of can never affect mining.
    The item-level dedup uses only the impression history supplied by the caller.
    """
    if not isinstance(user, str) or not user or type(as_of) is not int:
        raise ValueError("a user and integer as_of timestamp are required")
    for value in (window_days, discovery_days, session_limit, user_limit, recall_limit):
        if type(value) is not int or value < 1:
            raise ValueError("windows and quotas must be positive integers")
    recent: list[tuple[int, Candidate]] = []
    for session in sessions:
        if session.user != user or not as_of - window_days * DAY <= session.time < as_of:
            continue
        unshown = (row for row in session.candidates if row.item not in session.shown)
        top = sorted(unshown, key=lambda row: (-row.score, row.item))[:session_limit]
        recent.extend((session.time, row) for row in top)
    recent.sort(key=lambda pair: (-pair[0], -pair[1].score, pair[1].item, pair[1].category))
    pool: dict[str, Candidate] = {}
    for _, row in recent:
        pool.setdefault(row.item, row)
        if len(pool) >= user_limit:
            break
    observed_items: set[str] = set()
    exposed_categories: set[str] = set()
    for event in exposures:
        if event.user != user or event.time >= as_of:
            continue
        observed_items.add(event.item)
        if event.time >= as_of - discovery_days * DAY:
            exposed_categories.add(event.category)
    return tuple(row for row in pool.values()
                 if row.item not in observed_items and row.category not in exposed_categories)[:recall_limit]


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("URED reference is CPU-only")
    rng = random.Random(seed)
    now = 40 * DAY
    rows = (
        ScoredSession("u", now - 3 * DAY, (Candidate("older", "novel", rng.uniform(.5, 1)),)),
        ScoredSession("u", now - 1, (Candidate("shown", "novel", 1), Candidate("fresh", "new", .8),
                                    Candidate("seen", "known", .9), Candidate("weak", "rare", .1)),
                      frozenset({"shown"})),
        ScoredSession("u", now, (Candidate("future", "future", 1),)),
    )
    exposures = (Exposure("u", now - DAY, "past", "known"), Exposure("u", now, "fresh", "new"))
    result = mine_ured("u", now, rows, exposures, session_limit=2)
    short = mine_ured("u", now, rows, exposures, window_days=1, session_limit=2)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"recalled_items": len(result), "one_day_recalled_items": len(short),
                        "retained_score_sum": math.fsum(row.score for row in result)},
            "checks": {"long_window_retains_older_candidate": tuple(row.item for row in result) == ("fresh", "older"),
                       "short_window_excludes_old_candidate": tuple(row.item for row in short) == ("fresh",),
                       "future_events_do_not_affect_recall": result == mine_ured("u", now, rows[:-1], exposures[:1], session_limit=2)}}
