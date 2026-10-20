"""Non-invasive SID insertion from arXiv:2610.26105, not a learned retriever.

Prefixes must be supplied by an external quantizer. Tail group size is an
explicit caller choice: the paper does not publish its production value.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping, Sequence

SID = tuple[int, int, int]


@dataclass(frozen=True)
class Item:
    key: str
    prefix: tuple[int, int]
    clicks: float
    carts: float
    buys: float
    exposures: float

    def __post_init__(self):
        if not isinstance(self.key, str) or not self.key:
            raise ValueError("nonempty item ID required")
        if len(self.prefix) != 2 or any(type(x) is not int or x < 0 for x in self.prefix):
            raise ValueError("two nonnegative integer semantic tokens required")
        for value in (self.clicks, self.carts, self.buys, self.exposures):
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise ValueError("finite nonnegative counts required")

    @property
    def value(self) -> float:
        return (.1 * self.clicks + .3 * self.carts + self.buys) / (self.exposures + 10.)


def _validate_sid(value):
    if not isinstance(value, tuple) or len(value) != 3 or any(type(x) is not int or x < 0 for x in value):
        raise ValueError("three nonnegative integer SID tokens required")


def ranked_assignment(items: Sequence[Item], *, head: int = 100,
                      tail_buckets: int = 1024, tail_group_size: int) -> dict[str, SID]:
    """Initial/full-remap HC assignment, with deterministic ID tie-breaking."""
    if any(type(x) is not int or x < 1 for x in (head, tail_buckets, tail_group_size)):
        raise ValueError("positive explicit HC allocation parameters required")
    if len({i.key for i in items}) != len(items):
        raise ValueError("duplicate item IDs")
    groups = {}
    for item in items:
        groups.setdefault(item.prefix, []).append(item)
    result = {}
    for prefix, rows in sorted(groups.items()):
        for rank, item in enumerate(sorted(rows, key=lambda i: (-i.value, i.key)), 1):
            token = rank if rank <= head else head + 1 + (rank - head - 1) // tail_group_size
            if token > head + tail_buckets:
                raise ValueError("declared tail capacity exhausted; no silent wrapping/remapping")
            result[item.key] = (*prefix, token)
    return result


def insert_preserving(old: Mapping[str, SID], items: Sequence[Item], *,
                      head: int = 100, tail_buckets: int = 1024,
                      tail_group_size: int) -> dict[str, SID]:
    """Retain every old path, insert new items at current value rank.

    An insertion into the head may collide with a formerly unique old token.
    Do not shift incumbents, force uniqueness, prune unobserved old items, or
    quietly accept a re-quantized prefix for an old item.
    """
    for key, sid in old.items():
        if not isinstance(key, str) or not key:
            raise ValueError("nonempty old IDs required")
        _validate_sid(sid)
    proposed = ranked_assignment(items, head=head, tail_buckets=tail_buckets,
                                 tail_group_size=tail_group_size)
    for item in items:
        if item.key in old and item.prefix != old[item.key][:2]:
            raise ValueError("old-item semantic prefix must remain frozen")
    return {**proposed, **old}


def remapped_fraction(old: Mapping[str, SID], current: Mapping[str, SID]) -> float:
    """Equation 3 over the old item set; disappearance counts as changed."""
    if not old:
        raise ValueError("old-item denominator must be nonempty")
    return sum(current.get(key) != sid for key, sid in old.items()) / len(old)


def resolve_paths(mapping: Mapping[str, SID], paths: Sequence[SID]) -> tuple[str, ...]:
    """Resolve all collision members, without inventing within-bucket ranking."""
    reverse = {}
    for key, sid in mapping.items():
        _validate_sid(sid)
        reverse.setdefault(sid, []).append(key)
    result = []
    seen = set()
    for sid in paths:
        _validate_sid(sid)
        for key in sorted(reverse.get(sid, ())):
            if key not in seen:
                result.append(key)
                seen.add(key)
    return tuple(result)
