import pytest

from auto_research.foundation_models.frontier_replay import (
    REQUIRES_GPU_VALIDATION, Checkpoint, CheckpointPool, diagnostic, plan_boundaries, reclaim_budget, tier,
)


def cp(key, depth=256, kind="turn", **kwargs):
    return Checkpoint(key, tuple(range(depth)), kind, 0, "producer", **kwargs)


def publish(pool, row, **context):
    result = pool.prepare(row, **context)
    pool.complete(row.key, success=True)
    return result


def test_structural_boundaries_and_window():
    plan = plan_boundaries(0, 2048, template_end=647, branch_depths=(128, 256, 512, 1536),
                           chunk_ends=(640, 2048), finished_turn_end=511)
    assert plan.replay == (256, 512)
    assert plan.natural == (496, 640, 2048)
    assert plan.exact_cuts == (1024,)


def test_floor_is_inclusive_and_no_future_target():
    plan = plan_boundaries(0, 1600, template_end=1568, branch_depths=(512, 2048), falcon_h1=True)
    assert plan.replay == () and plan.exact_cuts == (1568,)
    assert plan_boundaries(1024, 1600, template_end=1568, falcon_h1=True).replay == (1568,)


def test_native_chunk_end_cannot_invent_an_earlier_page_state():
    with pytest.raises(ValueError, match="native chunk ends"):
        plan_boundaries(0, 2048, template_end=1000, chunk_ends=(1001,))
    structural = plan_boundaries(0, 2048, template_end=1000)
    assert structural.replay == (992,) and structural.natural == ()
    native = plan_boundaries(0, 2048, template_end=1000, chunk_ends=(992,))
    assert native.replay == () and native.natural == (992,)
    # The paper explicitly saves the last page passed during completed decode.
    turn = plan_boundaries(0, 2048, template_end=1000, finished_turn_end=1001)
    assert turn.replay == () and turn.natural == (992,)


@pytest.mark.parametrize("context", [{"live_anchor": False}, {"free_log_page": False}])
def test_no_anchor_or_log_falls_back_before_replay(context):
    plan = plan_boundaries(0, 2048, template_end=512, **context)
    assert plan.fallback and plan.exact_cuts == (512,) and not plan.replay


@pytest.mark.parametrize("start,end", [(3, 1024), (-16, 100), (32, 16), (True, 32)])
def test_invalid_planner_arguments(start, end):
    with pytest.raises(ValueError):
        plan_boundaries(start, end)


def test_publication_and_failed_step_never_expose_partial_state():
    pool = CheckpointPool(2)
    row = cp("pending")
    pool.prepare(row)
    assert pool.lookup(row.prefix) is None
    with pytest.raises(ValueError):
        pool.acquire(row.key, "request", 1)
    pool.complete(row.key, success=False)
    assert row.key not in pool.rows
    publish(pool, cp("complete"))
    assert pool.lookup(tuple(range(300))).key == "complete"


def test_leased_dead_state_stays_pinned_until_release():
    pool = CheckpointPool(1)
    row = cp("anchor")
    publish(pool, row)
    pool.acquire(row.key, "request", 1)
    row.kv_alive = False
    assert pool.lookup(row.prefix) is None
    with pytest.raises(RuntimeError):
        pool.prepare(cp("replacement", 16, "natural"))
    pool.release(row.key)
    assert pool.prepare(cp("replacement", 16, "natural")) == "anchor"


def test_distinct_requests_not_repeated_restores_and_running_priority():
    row = cp("anchor", published=True)
    row.restoring_requests.update(["one", "one"])
    assert tier(row, [row]) == 2
    row.restoring_requests.add("two")
    assert tier(row, [row]) == 3
    assert tier(row, [row], running=frozenset({"anchor"})) == 4


def test_superseded_needs_observed_progress_or_deeper_natural():
    old = cp("old", published=True)
    deeper = cp("deeper", 512, published=True)
    assert tier(old, [old, deeper]) == 2
    assert tier(old, [old, deeper], observed_progress={"producer": deeper.prefix}) == 2
    assert tier(old, [old, deeper], observed_progress={"other": deeper.prefix}) == 0
    junction = cp("junction", 384, "branch", published=True)
    assert tier(old, [old, deeper, junction], observed_progress={"other": deeper.prefix}) == 2
    assert tier(junction, [old, deeper, junction], observed_progress={"other": deeper.prefix}) == 3
    natural_old, natural_new = cp("a", 256, "natural", published=True), cp("b", 512, "natural", published=True)
    assert tier(natural_old, [natural_old, natural_new]) == 0


def test_long_prefix_protection_ignores_question_specific_deeper_natural():
    early = cp("early", 4096, "natural", group="doc", published=True)
    anchor = cp("long", 4608, "natural", group="doc", published=True)
    question = cp("question", 5632, "natural", group="doc", published=True)
    context = {"stable_ends": {"doc": 5000}}
    assert tier(anchor, [early, anchor, question], **context) == 3
    assert tier(early, [early, anchor, question], **context) == 0
    junction = cp("branch", 4800, "branch", group="doc", published=True)
    assert tier(anchor, [early, anchor, question, junction], **context) == 0


def test_eviction_uses_tier_then_estimated_loss_then_lru():
    pool = CheckpointPool(2)
    a = cp("a", estimated_lost_tokens=200, published=False)
    b = cp("b", estimated_lost_tokens=100, published=False)
    # Equal-depth different prefixes avoid an ancestor relation.
    b.prefix = (1000,) * 256
    publish(pool, a)
    publish(pool, b)
    assert publish(pool, cp("c", 512)) == "b"


def test_natural_admission_cannot_displace_positive_tier():
    pool = CheckpointPool(1)
    publish(pool, cp("branch", 256, "branch"))
    with pytest.raises(RuntimeError):
        pool.prepare(cp("new", 16, "natural"))
    assert list(pool.rows) == ["branch"]


def test_bad_acquire_does_not_mutate_lease():
    pool = CheckpointPool(1)
    publish(pool, cp("anchor"))
    with pytest.raises(ValueError):
        pool.acquire("anchor", "r", -1)
    assert pool.rows["anchor"].leases == 0
    with pytest.raises(ValueError):
        pool.release("anchor")


def test_reclaim_four_period_gate_period_floor_and_available_victims():
    kwargs = dict(requests=16, kv_dead_count=9, recent_positive_evictions=(0, 0, 0, 0),
                  capacity=20, working_floor=5, removable=18)
    assert reclaim_budget(**kwargs) == 15
    assert reclaim_budget(**(kwargs | {"requests": 15})) == 0
    assert reclaim_budget(**(kwargs | {"recent_positive_evictions": (0, 1, 0, 0)})) == 0
    assert reclaim_budget(**(kwargs | {"removable": 3})) == 3
    assert reclaim_budget(**(kwargs | {"kv_dead_count": 0})) == 0
    with pytest.raises(ValueError):
        reclaim_budget(**(kwargs | {"recent_positive_evictions": (0,)}))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_is_not_a_capability_score(seed):
    assert REQUIRES_GPU_VALIDATION is False
    result = diagnostic(seed)
    assert result["diagnostic_only"] and all(result["checks"].values())
    assert "accuracy" not in result["metrics"]
    with pytest.raises(ValueError):
        diagnostic(seed, "cuda")
