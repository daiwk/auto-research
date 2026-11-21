"""FrontierReplay host-policy components, fixed paper v1 Sections 4.2--4.6.

These functions do not execute recurrent kernels, inspect serving traces, or
allocate GPU memory. Event completion and KV residency are explicit inputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Literal


Kind = Literal["natural", "template", "turn", "branch"]
REQUIRES_GPU_VALIDATION = False


def _integer(value: int, name: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


@dataclass(frozen=True)
class BoundaryPlan:
    replay: tuple[int, ...]
    natural: tuple[int, ...]
    exact_cuts: tuple[int, ...]
    fallback: bool


def plan_boundaries(
    start: int, end: int, *, template_end: int | None = None,
    finished_turn_end: int | None = None, branch_depths: tuple[int, ...] = (),
    chunk_ends: tuple[int, ...] = (), falcon_h1: bool = False,
    live_anchor: bool = True, free_log_page: bool = True,
) -> BoundaryPlan:
    """Plan from already observed cues; callers supply no future reuse oracle.

    Structural targets and completed-turn ends use the last 16-token page.
    Native chunk ends must already be page aligned: rounding an unaligned cue
    would invent a state that the forward pass never exposed. A mid-chunk
    structural target needs replay. Wide targets require a proactive cut.
    """
    _integer(start, "start")
    _integer(end, "end")
    if start % 16 or end < start:
        raise ValueError("start must be page aligned and end cannot precede start")
    floor = 1568 if falcon_h1 else 0

    def page(value):
        _integer(value, "boundary")
        return value // 16 * 16

    natural = set()
    for native_end in chunk_ends:
        _integer(native_end, "native chunk end")
        if native_end % 16:
            raise ValueError("native chunk ends must already be 16-token aligned")
        natural.add(native_end)
    if finished_turn_end is not None:
        natural.add(page(finished_turn_end))
    targets = {page(x) for x in branch_depths if _integer(x, "branch depth") >= 256}
    if template_end is not None:
        targets.add(page(template_end))
    allowed = lambda x: start < x <= end and x >= floor
    natural = {x for x in natural if allowed(x)}
    targets = {x for x in targets if allowed(x)} - natural
    if not targets:
        return BoundaryPlan((), tuple(sorted(natural)), (), False)
    if not live_anchor or not free_log_page:
        return BoundaryPlan((), tuple(sorted(natural)), (min(targets),), True)
    bounded = tuple(sorted(x for x in targets if x - start <= 1024))
    # Before Falcon's restore floor the engine must advance by an exact cut;
    # it must not publish a checkpoint at an otherwise convenient lower page.
    cuts = (max(start + 1024, floor),) if any(x - start > 1024 for x in targets) else ()
    return BoundaryPlan(bounded, tuple(sorted(natural)), cuts, False)


@dataclass
class Checkpoint:
    key: str
    prefix: tuple[int, ...]
    kind: Kind
    last_used: int
    producer: str
    group: str = ""
    kv_alive: bool = True
    published: bool = False
    leases: int = 0
    restoring_requests: set[str] = field(default_factory=set)
    estimated_lost_tokens: int = 0

    def __post_init__(self):
        if not self.key or not self.prefix or len(self.prefix) % 16:
            raise ValueError("checkpoint needs a key and nonempty page-aligned prefix")
        if self.kind not in {"natural", "template", "turn", "branch"}:
            raise ValueError("unknown checkpoint kind")
        for token in self.prefix:
            _integer(token, "token")
        _integer(self.last_used, "last_used")
        _integer(self.leases, "leases")
        _integer(self.estimated_lost_tokens, "estimated lost tokens")


def _ancestor(a: Checkpoint, b: Checkpoint) -> bool:
    return len(a.prefix) < len(b.prefix) and b.prefix[:len(a.prefix)] == a.prefix


def tier(
    checkpoint: Checkpoint, residents: list[Checkpoint], *,
    running: frozenset[str] = frozenset(),
    observed_progress: dict[str, tuple[int, ...]] | None = None,
    stable_ends: dict[str, int] | None = None,
) -> int:
    """Compute dead/superseded/speculative/proven/running host-policy tiers.

    Explicit progress is observed request progress, not a future trace. Lease
    protection is separately enforced by the pool even when a prefix dies.
    """
    if not checkpoint.kv_alive:
        return -1
    if checkpoint.key in running:
        return 4
    reachable = [row for row in residents if row.published and row.kv_alive]
    descendants = [row for row in reachable if _ancestor(checkpoint, row)]
    progressed = any(
        request != checkpoint.producer and len(prefix) > len(checkpoint.prefix)
        and prefix[:len(checkpoint.prefix)] == checkpoint.prefix
        for request, prefix in (observed_progress or {}).items()
    )
    superseded = checkpoint.kind != "branch" and any(
        checkpoint.kind == row.kind == "natural" or (
            progressed and not any(
                junction.kind == "branch" and _ancestor(checkpoint, junction)
                and (junction.key == row.key or _ancestor(junction, row))
                for junction in reachable
            )
        ) for row in descendants
    )
    protected_long = False
    stable_end = (stable_ends or {}).get(checkpoint.group)
    if checkpoint.kind == "natural" and stable_end is not None:
        _integer(stable_end, "stable end")
        candidates = [row for row in reachable if row.kind == "natural"
                      and row.group == checkpoint.group
                      and max(4096, stable_end - 2048) <= len(row.prefix) <= stable_end]
        protected_long = bool(candidates) and checkpoint.key == max(
            candidates, key=lambda row: (len(row.prefix), row.key)
        ).key and not any(row.kind == "branch" for row in descendants)
    if protected_long:
        return 3
    if superseded:
        return 0
    if checkpoint.kind == "branch" or len(checkpoint.restoring_requests) >= 2:
        return 3
    return 1 if checkpoint.kind == "natural" else 2


class CheckpointPool:
    """Small host state machine; publication requires an explicit completion.

    Prefixes here are synthetic token tuples, never local files or user logs.
    Actual cache/device/event ownership is outside this component.
    """

    def __init__(self, capacity: int):
        self.capacity = _integer(capacity, "capacity", 1)
        self.rows: dict[str, Checkpoint] = {}

    def prepare(self, checkpoint: Checkpoint, **context) -> str | None:
        if checkpoint.key in self.rows or checkpoint.published or checkpoint.leases:
            raise ValueError("prepare requires a fresh unpublished unleased checkpoint")
        evicted = None
        if len(self.rows) == self.capacity:
            residents = list(self.rows.values())
            candidates = [row for row in residents if row.published and not row.leases
                          and row.key not in context.get("running", frozenset())]
            if not candidates:
                raise RuntimeError("no evictable checkpoint")
            victim = min(candidates, key=lambda row: (
                tier(row, residents, **context), row.estimated_lost_tokens, row.last_used, row.key
            ))
            if checkpoint.kind == "natural" and tier(victim, residents, **context) > 0:
                raise RuntimeError("natural checkpoint cannot evict a useful resident")
            evicted = victim.key
            del self.rows[victim.key]
        self.rows[checkpoint.key] = checkpoint
        return evicted

    def complete(self, key: str, *, success: bool):
        row = self.rows[key]
        if row.published:
            raise ValueError("checkpoint already published")
        if success:
            row.published = True
        else:
            del self.rows[key]

    def lookup(self, prefix: tuple[int, ...]) -> Checkpoint | None:
        candidates = [row for row in self.rows.values() if row.published and row.kv_alive
                      and prefix[:len(row.prefix)] == row.prefix]
        return max(candidates, key=lambda row: len(row.prefix)) if candidates else None

    def acquire(self, key: str, request: str, clock: int):
        row = self.rows[key]
        if not row.published or not row.kv_alive or not request:
            raise ValueError("cannot restore pending/dead state or anonymous request")
        _integer(clock, "clock")
        row.leases += 1
        row.restoring_requests.add(request)
        row.last_used = clock

    def release(self, key: str):
        row = self.rows[key]
        if row.leases <= 0:
            raise ValueError("lease underflow")
        row.leases -= 1


def reclaim_budget(*, requests: int, kv_dead_count: int, recent_positive_evictions: tuple[int, ...],
                   capacity: int, working_floor: int, removable: int) -> int:
    """Section4.5 reclaim decision on externally observed, non-self signals.

    The caller counts only KV-caused deaths, not this controller's evictions.
    No CUDA virtual-memory mapping or autonomous periodic process is installed.
    """
    for key, value in locals().copy().items():
        if key != "recent_positive_evictions":
            _integer(value, key)
    if capacity < working_floor or len(recent_positive_evictions) != 4:
        raise ValueError("need a legal pool floor and exactly four observed periods")
    for value in recent_positive_evictions:
        _integer(value, "evictions")
    if requests == 0 or requests % 16 or any(recent_positive_evictions):
        return 0
    return min(16, 2 * kv_dead_count, capacity - working_floor, removable)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("host-policy component has no CUDA path")
    rng = random.Random(seed)
    base = tuple(rng.randrange(1000) for _ in range(512))
    pool = CheckpointPool(2)
    anchor = Checkpoint("anchor", base[:256], "turn", 0, "a")
    pool.prepare(anchor)
    pending_hidden = pool.lookup(base) is None
    pool.complete("anchor", success=True)
    pool.acquire("anchor", "b", 1)
    pool.release("anchor")
    pool.acquire("anchor", "b", 2)
    pool.release("anchor")
    one_request_not_proven = tier(anchor, [anchor]) == 2
    pool.acquire("anchor", "c", 3)
    pool.release("anchor")
    branch = Checkpoint("branch", base[:512], "branch", 0, "b")
    pool.prepare(branch)
    pool.complete("branch", success=True)
    rejected = False
    try:
        pool.prepare(Checkpoint("natural", base[:16], "natural", 4, "d"))
    except RuntimeError:
        rejected = True
    anchor.kv_alive = False
    evicted = pool.prepare(Checkpoint("new", base[:16], "natural", 4, "d"))
    pool.complete("new", success=False)
    plan = plan_boundaries(0, 2048, template_end=640, branch_depths=(128, 512, 1536), chunk_ends=(2048,))
    fallback = plan_boundaries(0, 2048, template_end=640, live_anchor=False)
    reclaimed = reclaim_budget(requests=16, kv_dead_count=9, recent_positive_evictions=(0, 0, 0, 0),
                               capacity=20, working_floor=5, removable=18)
    unaligned_native_rejected = False
    try:
        plan_boundaries(0, 2048, template_end=1000, chunk_ends=(1001,))
    except ValueError:
        unaligned_native_rejected = True
    structural_only = plan_boundaries(0, 2048, template_end=1000)
    aligned_native = plan_boundaries(0, 2048, template_end=1000, chunk_ends=(992,))
    checks = {
        "pending_checkpoint_not_visible": pending_hidden,
        "distinct_requests_required_for_proven": one_request_not_proven and tier(branch, [branch]) == 3,
        "natural_cannot_evict_useful_state": rejected,
        "dead_checkpoint_evicted_first": evicted == "anchor",
        "failed_publication_not_visible": pool.lookup(base[:16]) is None,
        "structural_targets_and_bounded_window": plan.replay == (512, 640) and plan.exact_cuts == (1024,),
        "no_anchor_falls_back_to_exact_cut": fallback.fallback and fallback.exact_cuts == (640,),
        "reclaim_respects_working_floor": reclaimed == 15,
        "falcon_restore_floor": not plan_boundaries(0, 2048, template_end=1024, falcon_h1=True).replay,
        "native_chunk_state_requires_exact_page_alignment": unaligned_native_rejected
        and structural_only.replay == (992,) and aligned_native.replay == ()
        and aligned_native.natural == (992,),
    }
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"planned_replay_targets": len(plan.replay), "planned_exact_cuts": len(plan.exact_cuts),
                        "distinct_restore_requests": len(anchor.restoring_requests), "reclaim_slots": reclaimed},
            "checks": checks}
