import pytest

torch = pytest.importorskip("torch")

from auto_research.agent_research.latest_20261002 import (
    CurriculumArm,
    NonDestructiveMemory,
    active_saddler_choice,
    defa_decisive_error,
    flowright_hierarchical_credit,
    safe_self_improvement_select,
    veriharness_select,
)
from auto_research.foundation_latest_20261002 import (
    TACO,
    gfg_mixed_objective,
    taco_direction,
    veto_compress,
)
from auto_research.latest_20261002_catalog import LATEST_METHOD_PAPERS
from auto_research.post_training.latest_20261002 import (
    dependency_shaped_rewards,
    fault_terminal_redistribution,
    range_grpo_advantages,
    where_opd_loss,
)
from auto_research.recommendation_latest_20261002 import (
    basis_vq,
    effective_training_time,
    gear_collision_rerank,
    gris_hierarchical_ids,
    repair_preference_state,
)
from auto_research.reproductions.latest_20261002 import make_adapter


def test_dars_preserves_independent_work_and_restores_repaired_dependency():
    rewards, state = dependency_shaped_rewards(
        [
            {"verify": ["root", "independent"]},
            {"verify": ["child"]},
            {"invalidate": ["root"]},
            {"repair": ["root"], "verify": ["root"]},
        ],
        {"child": ("root",)},
        discount=.5,
    )
    assert rewards[2] < 0 < rewards[3]
    assert state == {"verified": ("child", "independent", "root"), "broken": ()}


def test_range_grpo_uses_only_confident_pairwise_interval_ordering():
    advantages = range_grpo_advantages(
        torch.tensor([0.0, .5, 2.0]), torch.tensor([.8, 1.2, 2.1])
    )
    assert advantages[2] > advantages[1] > advantages[0]
    overlapping = range_grpo_advantages(torch.tensor([0.0, .1]), torch.tensor([1.0, .9]))
    assert torch.allclose(overlapping, torch.zeros(2))


def test_fault_redistribution_is_verified_and_terminal_conserved():
    rows, audit = fault_terminal_redistribution(
        [1.0, 0.0],
        [
            [{"step": 1, "category": "tool", "verified": True}],
            [{"step": 1, "category": "tool", "verified": False}],
        ],
        {"tool": 2.0},
    )
    assert rows[0].sum() == pytest.approx(1.0)
    assert rows[1].sum() == 0
    assert audit["signal_coverage"] == .5


def test_where_opd_uses_spatial_positions_and_stops_teacher_gradient():
    student = torch.randn(2, 3, 5, requires_grad=True)
    teacher = torch.randn(2, 3, 5, requires_grad=True)
    loss = where_opd_loss(student, teacher, torch.tensor([[1, 0, 1], [0, 1, 0]]))
    loss.backward()
    assert student.grad is not None and teacher.grad is None


def test_active_saddler_discovers_then_prioritizes_failure_arms():
    action, target, _ = active_saddler_choice([], ("unseen",), iteration=1)
    assert (action, target) == ("draw", "unseen")
    action, target, scores = active_saddler_choice(
        [CurriculumArm("tool", .9, 2), CurriculumArm("plan", .1, 2)],
        (),
        iteration=5,
    )
    assert action == "pull" and target == "tool" and scores["tool"] > scores["plan"]


def test_safe_rsi_validates_current_candidate_and_rolls_back_founder():
    founder = {"name": "founder", "score": 0}
    selected, audit = safe_self_improvement_select(
        [{"name": "stale", "score": 100}],
        lambda _: {"safe": False, "correct": True},
        founder=founder,
    )
    assert selected is founder and audit["rollback"]


def test_veriharness_checks_consensus_against_evidence():
    selected, audit = veriharness_select(
        [
            {"id": "minimal", "claims": ["supported"]},
            {"id": "extra", "claims": ["supported", "unsupported"]},
        ],
        lambda claim: claim == "supported",
    )
    assert selected == "minimal" and audit["consensus_claims_challenged"] == 1


def test_mem_plus_plus_never_destroys_history_and_obeys_as_of_date():
    memory = NonDestructiveMemory()
    memory.write(text="budget is ten", date="2026-01", author="a")
    memory.write(text="budget is twenty", date="2026-08", author="b")
    before = memory.retrieve(["budget"], {}, as_of="2026-06")
    after = memory.retrieve(["budget"], {}, as_of="2026-09")
    assert len(memory.documents) == 2
    assert [row["text"] for row in before] == ["budget is ten"]
    assert {row["text"] for row in after} == {"budget is ten", "budget is twenty"}


def test_defa_traces_failure_to_earliest_high_error_dependency():
    decisive, audit = defa_decisive_error(
        [
            {"id": "source", "step": 0, "error_score": .9},
            {"id": "middle", "step": 1, "error_score": .2},
            {"id": "visible", "step": 2, "error_score": 0, "violates": True},
        ],
        {"visible": ("middle",), "middle": ("source",)},
    )
    assert decisive["id"] == "source"
    assert set(audit["propagation_nodes"]) == {"source", "middle", "visible"}


def test_flowright_credit_is_structural_and_conserved():
    credit = flowright_hierarchical_credit(
        {"lead": {}, "worker": {"parents": ("lead",)}},
        2.0,
        {"lead": 1, "worker": 1},
    )
    assert sum(credit.values()) == pytest.approx(2.0)
    assert credit["lead"] > credit["worker"]


def test_taco_is_column_one_sparse_and_uses_column_state():
    gradient = torch.tensor([[1.0, -4.0], [3.0, 2.0], [-2.0, 1.0]])
    direction = taco_direction(gradient)
    assert (direction != 0).sum(0).tolist() == [1, 1]
    assert direction.tolist() == [[0.0, -1.0], [1.0, 0.0], [0.0, 0.0]]
    layer = torch.nn.Linear(3, 2, bias=False)
    layer(torch.ones(1, 3)).sum().backward()
    optimizer = TACO(layer.parameters(), lr=.1)
    optimizer.step()
    assert optimizer.state_elements == layer.weight.shape[1]
    assert optimizer.state_elements < layer.weight.numel()


def test_veto_compresses_space_before_time_with_exact_budget():
    compressed, audit = veto_compress(torch.randn(6, 10, 4), spatial_keep=3, temporal_keep=2)
    assert compressed.shape == (2, 3, 4)
    assert audit["compression_ratio"] == pytest.approx(.1)
    assert len(audit["spatial_indices"]) == 3 and len(audit["frame_indices"]) == 2


def test_gfg_replay_objective_exposes_forgetting_tradeoff():
    current = torch.tensor(2.0, requires_grad=True)
    replay = torch.tensor(1.0, requires_grad=True)
    loss = gfg_mixed_objective(current, replay, replay_fraction=.25)
    loss.backward()
    assert loss == 1.75 and current.grad == .75 and replay.grad == .25


def test_gear_basisvq_and_collision_reranker_are_executable():
    basis, _ = torch.linalg.qr(torch.randn(4, 4))
    quantized, codes = basis_vq(torch.randn(5, 4), basis, torch.randn(3, 4))
    assert quantized.shape == (5, 4) and codes.shape == (5,)
    order, scores = gear_collision_rerank(
        torch.tensor([1.0, 0.0]),
        torch.tensor([[.1, 0.0], [.9, 0.0], [.2, 0.0]]),
        [(0,), (0,), (1,)],
    )
    assert order[:2].tolist() == [1, 0] and scores[1] > scores[0]


def test_effective_training_time_separates_lifecycle_owners():
    ett, losses = effective_training_time(
        {"training": 80, "compile": 10, "checkpoint": 5, "recovery": 5}
    )
    assert ett == .8 and sum(losses.values()) == pytest.approx(.2)


def test_gris_uses_graph_and_emits_hierarchical_binary_ids():
    features = torch.arange(24, dtype=torch.float32).reshape(6, 4)
    adjacency = torch.eye(6)
    adjacency[:3, :3] = 1
    adjacency[3:, 3:] = 1
    ids = gris_hierarchical_ids(features, adjacency, levels=2)
    assert ids.shape == (6, 2)
    assert set(ids.unique().tolist()) <= {0, 1}
    assert ids.unique(dim=0).shape[0] > 1


def test_repair_selects_cached_evidence_without_reencoding_history():
    state = torch.zeros(3)
    cached = torch.tensor([[1.0, 0, 0], [0, 2.0, 0], [0, 0, .1]])
    repaired, audit = repair_preference_state(
        state,
        cached,
        torch.tensor([0.0, 1.0, 0.0]),
        top_k=1,
    )
    assert audit["selected_timesteps"].tolist() == [1]
    assert torch.allclose(repaired, cached[1])


def test_batch_catalog_has_complete_metadata_and_explicit_evidence_boundaries():
    assert len(LATEST_METHOD_PAPERS) == 17
    assert {paper["priority"] for paper in LATEST_METHOD_PAPERS} == {"P0", "P1"}
    for paper in LATEST_METHOD_PAPERS:
        assert all(
            paper[field]
            for field in (
                "paper_url",
                "first_author_affiliation",
                "published",
                "adapter",
                "detail_path",
            )
        )
        assert "code" in paper

    by_key = {paper["key"]: paper for paper in LATEST_METHOD_PAPERS}
    assert by_key["dars"]["code"] is None
    assert "仍在准备" in by_key["dars"]["upstream_note"]
    assert by_key["effective-training-time"]["selection_exception"]
    assert by_key["gris"]["selection_exception"]
    assert by_key["repair-state"]["selection_exception"]
    for key in ("taco-optimizer", "veto"):
        assert by_key[key]["requires_gpu_validation"] is True
        assert by_key[key]["gpu_validation_artifact"].endswith("20261002.json")


@pytest.mark.parametrize(
    "key", ("gear", "effective-training-time", "gris", "repair-state")
)
def test_recommendation_batch_adapters_execute_their_declared_mechanism(tmp_path, key):
    adapter = make_adapter(key)
    result = adapter.run(tmp_path, 42)
    assert result["manifest_ref"] == f"reproduction:{key}"
    assert result["setup"]["diagnostic_only"] is True
    assert result["results"]
