"""MemPrice Eq. 3 and persistent queue, not an LLM utility estimator.

Representations are supplied by a trusted caller. Rank 0 is raw and rank 4
is delete. The allocator never receives queries, answers or evaluation labels.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Representation:
    level: int
    tokens: int
    utility: float
    text: str = ""


@dataclass(frozen=True)
class Item:
    key: str
    options: tuple[Representation, ...]


@dataclass(frozen=True)
class Allocation:
    choices: tuple[tuple[str, Representation], ...]
    tokens: int
    objective: float
    price: float
    queue_before: float
    queue_after: float
    round: int


def _options(item: Item, minimum_level: int = 0) -> tuple[Representation, ...]:
    if not isinstance(item.key, str) or not item.key or not item.options:
        raise ValueError("nonempty item and options required")
    levels = []
    for option in item.options:
        if (type(option.level) is not int or not 0 <= option.level <= 4
                or type(option.tokens) is not int or option.tokens < 0
                or type(option.utility) not in (int, float)
                or not math.isfinite(option.utility) or not 0 <= option.utility <= 1
                or not isinstance(option.text, str)):
            raise ValueError("invalid representation")
        if option.level == 4 and (option.tokens != 0 or option.utility != 0 or option.text):
            raise ValueError("delete must have zero size/utility and no text")
        levels.append(option.level)
    if len(set(levels)) != len(levels) or 4 not in levels:
        raise ValueError("unique fidelity levels including delete required")
    ordered = sorted(item.options, key=lambda option: option.level)
    if any(left.tokens < right.tokens for left, right in zip(ordered, ordered[1:])):
        raise ValueError("coarser representations cannot use more tokens")
    # Conservative monotonic repair: coarser utility cannot exceed finer utility.
    repaired, ceiling = [], 1.
    for option in ordered:
        ceiling = min(ceiling, option.utility)
        if option.level >= minimum_level:
            repaired.append(Representation(option.level, option.tokens, ceiling, option.text))
    return tuple(repaired)


def allocate(items: tuple[Item, ...], *, capacity: int, price: float,
             minimum_levels: dict[str, int] | None = None) -> tuple[tuple, int, float]:
    """Exact integer multiple-choice knapsack; deterministic low-size tie break.

    Complexity O(B * sum(number of options)), with sparse reachable states.
    Token counts are tokenizer measurements supplied by the caller, not len(text).
    """
    if type(capacity) is not int or not 0 < capacity <= 1_000_000:
        raise ValueError("capacity must be a bounded positive integer")
    if type(price) not in (int, float) or not math.isfinite(price) or price < 0:
        raise ValueError("finite nonnegative price required")
    if len({item.key for item in items}) != len(items):
        raise ValueError("duplicate item keys")
    minimum_levels = minimum_levels or {}
    if any(type(v) is not int or not 0 <= v <= 4 for v in minimum_levels.values()):
        raise ValueError("invalid previous fidelity")
    states = {0: (0., ())}
    for item in items:
        candidates = _options(item, minimum_levels.get(item.key, 0))
        following = {}
        for used, (value, path) in states.items():
            for option in candidates:
                size = used + option.tokens
                if size > capacity:
                    continue
                candidate = value + option.utility - price * option.tokens / capacity
                if not math.isfinite(candidate):
                    raise ValueError("nonfinite adjusted objective")
                if size not in following or candidate > following[size][0]:
                    following[size] = (candidate, path + ((item.key, option),))
        states = following
    size, (value, path) = max(states.items(), key=lambda entry: (entry[1][0], -entry[0]))
    return path, size, value


class MemPrice:
    """No resurrection between refreshes; refresh does not reset time/pressure."""

    def __init__(self, capacity: int, *, target: float = .8, c: float = 1.):
        allocate((), capacity=capacity, price=0.)
        if (not math.isfinite(target) or not 0 < target <= 1
                or not math.isfinite(c) or c <= 0):
            raise ValueError("invalid pricing parameters")
        self.capacity, self.target, self.c = capacity, target, c
        self.round, self.queue = 1, 0.
        self.levels: dict[str, int] = {}

    def step(self, items: tuple[Item, ...]) -> Allocation:
        price = self.c * self.queue / math.sqrt(self.round)
        choices, tokens, objective = allocate(items, capacity=self.capacity, price=price,
                                              minimum_levels=self.levels)
        before = self.queue
        after = max(0., before + tokens / self.capacity - self.target)
        self.levels.update({key: option.level for key, option in choices})
        result = Allocation(choices, tokens, objective, price, before, after, self.round)
        self.queue = after
        self.round += 1
        return result

    def refresh(self) -> None:
        """Caller supplies archive-derived carried context next; no queue reset.

        The fixed compression/retrieval pipeline itself is outside this component.
        Its returned context must still pass the next hard-capacity allocation.
        """
        self.levels.clear()
