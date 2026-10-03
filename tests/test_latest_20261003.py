import pytest

torch = pytest.importorskip("torch")

from auto_research.agent_research.latest_20261003 import (
    MemFitStore,
    autocorrect_compaction,
    jev_spawn,
    pace_authorize,
    rule_evolve_select,
    update_belief_state,
)
from auto_research.foundation_latest_20261003 import (
    af_muon_vocab_direction,
    dense_caption_distillation,
    hawk_draft_target,
    ireko_nested_subnetwork,
    llm2jev_distribution,
    llm2jev_objective,
    mwop_masks,
    rea_select_context,
)
from auto_research.latest_20261003_catalog import LATEST_METHOD_PAPERS
from auto_research.post_training.latest_20261003 import (
    carm_response_mask,
    drift_opd_loss,
    gradient_aligned_rejected_weights,
    group_mass_cap,
    lego_opd_teacher,
    sharpening_tax,
    sharpo_segment_advantages,
    token_level_video_credit,
)
from auto_research.recommendation_latest_20261003 import (
    agent_web_evidence,
    rptune_curate,
)
from auto_research.reproductions.latest_20261003 import make_adapter


def test_oct03_catalog_has_complete_review_metadata():
    assert len(LATEST_METHOD_PAPERS) == 23
    assert {paper["priority"] for paper in LATEST_METHOD_PAPERS} == {"P0", "P1"}
    required = {
        "domain",
        "key",
        "title",
        "paper_url",
        "detail_path",
        "topic",
        "first_author",
        "first_author_affiliation",
        "published",
        "code",
        "adapter",
        "priority",
    }
    for paper in LATEST_METHOD_PAPERS:
        assert required <= paper.keys()
        assert paper["published"] and paper["first_author_affiliation"]


@pytest.mark.parametrize("key", ["rptune", "agent-web-rec"])
def test_oct03_recommendation_adapters_are_executable_l1_diagnostics(key, tmp_path):
    adapter = make_adapter(key)
    result = adapter.run(tmp_path, seed=42)
    assert result["manifest_ref"] == f"reproduction:{key}"
    assert result["setup"]["diagnostic_only"] is True
    assert result["results"]


def test_rptune_prunes_and_puts_highest_priority_nearest_suffix():
    query = torch.tensor([1.0, 0.0])
    items = torch.tensor([[1.0, 0.0], [.5, .5], [0.0, 1.0], [-1.0, 0.0]])
    order, scores = rptune_curate(query, items, torch.zeros(4), prune_rate=.5)
    assert order.tolist()[-1] == int(scores.argmax())
    assert len(order) == 2


def test_agent_web_keeps_memory_private_and_gates_collaboration():
    chosen, patterns, audit = agent_web_evidence(
        torch.tensor([.9, .4, .2]), torch.tensor([10., 1., 0.]),
        semantic_weight=.8, memory_budget=2, confidence=.3,
        confidence_threshold=.7, collaborator_patterns=("pattern",),
    )
    assert len(chosen) == 2 and patterns == ("pattern",)
    assert audit == {"collaboration_activated": True, "private_records_exposed": 0, "patterns_fused": 1}


def test_llm2jev_returns_distribution_and_anchors_auxiliary_behavior():
    probabilities = llm2jev_distribution(torch.tensor([[0., 0.], [1., 1.]]))
    assert probabilities.sum() == pytest.approx(1) and probabilities[1] > probabilities[0]
    decision = torch.tensor([.1, .9], requires_grad=True)
    auxiliary = torch.tensor([.2, .8], requires_grad=True)
    loss = llm2jev_objective(decision, torch.tensor(1), auxiliary, torch.tensor([.5, .5]), kl_weight=.2)
    loss.backward()
    assert decision.grad is not None and auxiliary.grad is not None


def test_omni_distillation_stops_teacher_gradient():
    student = torch.randn(3, 4, requires_grad=True)
    teacher = torch.randn(3, 4, requires_grad=True)
    dense_caption_distillation(student, teacher).backward()
    assert student.grad is not None and teacher.grad is None


def test_mwop_separates_attention_paths_and_modal_ffn_channels():
    attention, visual, text = mwop_masks(
        torch.arange(12.0).reshape(4, 3), torch.arange(8.0), torch.arange(8.0).flip(0), keep=3
    )
    assert attention.sum() == visual.sum() == text.sum() == 3
    assert not torch.equal(visual, text)


def test_af_muon_vocab_direction_is_support_aware_and_capped():
    gradient = torch.tensor([[3.0, 4.0], [0.0, 0.0], [6.0, 8.0]])
    direction = af_muon_vocab_direction(gradient, cap=2.0)
    assert direction[1].abs().sum() == 0
    assert direction[0].norm() == pytest.approx(2.0)
    assert direction[2].norm() == pytest.approx(2.0)


def test_rea_persists_instructions_and_selects_episodes():
    instructions, episodes = rea_select_context(("never delete",), ("old", "useful"), (.1, .9), episode_budget=1)
    assert instructions == ("never delete",) and episodes == ("useful",)


def test_hawk_uses_layer_mixture_and_detached_shifted_teacher():
    shifted = torch.randn(2, 3, requires_grad=True)
    hidden, target = hawk_draft_target((torch.zeros(2, 3), torch.ones(2, 3)), torch.tensor([-2., 2.]), shifted)
    assert hidden.mean() > .9 and not target.requires_grad


def test_ireko_subnetworks_are_nested():
    weight = torch.eye(4)
    projection = torch.eye(4)
    small, small_basis = ireko_nested_subnetwork(weight, projection, width=2)
    large, large_basis = ireko_nested_subnetwork(weight, projection, width=3)
    assert small.shape == (2, 2) and large.shape == (3, 3)
    assert torch.equal(small_basis, large_basis[:, :2])


def test_carm_detects_signed_ratio_cancellation():
    current = torch.log(torch.tensor([[10.0, .1], [1.01, .99]]))
    rollout = torch.zeros_like(current)
    mask, drift = carm_response_mask(current, rollout, threshold=1.1)
    assert mask.tolist() == [False, True] and drift[0] > drift[1]


def test_group_mass_cap_bounds_each_group():
    weights = group_mass_cap(torch.tensor([[2., 2.], [.2, .3]]), mass_cap=1.0)
    assert weights.sum(-1).tolist() == pytest.approx([1.0, .5])


def test_gradient_alignment_preserves_useful_rejected_tokens():
    weights = gradient_aligned_rejected_weights(torch.tensor([[1., 0.], [-1., 0.]]), torch.tensor([1., 0.]))
    assert weights.tolist() == pytest.approx([0., 1.])


def test_sharpo_varies_credit_by_interaction_segment():
    result = sharpo_segment_advantages(
        torch.tensor(1.0), torch.tensor([2., 2., -2., -2.]), torch.zeros(4), ((0, 2), (2, 4))
    )
    assert result[:2].mean() > result[2:].mean()


def test_tvrl_credit_is_dense_normalized_and_detached():
    gradient = torch.tensor([[[3., 4.], [0., 2.]]], requires_grad=True)
    credit = token_level_video_credit(gradient, group_advantage=2.0)
    assert credit.mean() == pytest.approx(2.0) and not credit.requires_grad


def test_sharpening_tax_exposes_coverage_loss():
    tax = sharpening_tax(torch.tensor(.25), torch.tensor(.5), samples=8)
    assert tax < 0  # Higher post-training single-shot success improves this synthetic case.
    concentrated = sharpening_tax(torch.tensor(.3), torch.tensor(.1), samples=8)
    assert concentrated > 0


def test_lego_opd_composes_normalized_language_and_grounding_factors():
    teacher = lego_opd_teacher(torch.tensor([[2., 0.]]), torch.tensor([[0., 2.]]), grounding_strength=1.0)
    assert teacher.sum() == pytest.approx(1.0)
    assert teacher[0, 0] == pytest.approx(teacher[0, 1])


def test_drift_opd_stops_teacher_gradient_and_uses_potential():
    student = torch.randn(2, 4, requires_grad=True)
    teacher = torch.randn(2, 4, requires_grad=True)
    potential = torch.tensor([.2, .4])
    loss = drift_opd_loss(student, teacher, potential, potential_weight=.5)
    loss.backward()
    assert student.grad is not None and teacher.grad is None


def test_autocompact_executes_judge_corrections_in_place():
    corrected, audit = autocorrect_compaction(False, "stale", "repeat", lambda _: {
        "decision": True, "summary": "root cause found", "next_action": "patch",
    })
    assert corrected["next_action"] == "patch" and all(audit.values())


def test_belief_state_reports_trapping_without_progress():
    state, trapped = update_belief_state(
        {"facts": {"door": False}, "unresolved": ("door",)}, {}, ("door",)
    )
    assert state["unresolved"] == ("door",) and trapped
    state, trapped = update_belief_state(state, {"door": True}, ("door",))
    assert not state["unresolved"] and not trapped


def test_pace_checks_effect_authority_and_provenance_at_execution():
    call = {"tool": "shell", "effects": ("write",), "influenced_by": ("request",)}
    allowed, _ = pace_authorize(call, {"shell": ("read", "write")}, {"trusted_sources": ("request",)})
    denied, audit = pace_authorize(call, {"shell": ("read", "write")}, {"trusted_sources": ()})
    assert allowed and not denied and audit["tainted"]


def test_rule_evolve_uses_validation_not_mutator_preference():
    selected, audit = rule_evolve_select(("baseline",), ("short", "best-rule"), len)
    assert selected == "best-rule" and audit["evaluated"] == 3


def test_jev_spawn_retains_multiple_feedback_weighted_actions():
    actions, posterior = jev_spawn(torch.tensor([.6, .3, .1]), ("a", "b", "c"), (0., 2., 0.), branches=2)
    assert actions[0] == "b" and len(actions) == 2 and posterior.sum() == pytest.approx(1)


def test_memfit_is_append_only_and_retrieves_without_rewriting_turns():
    memory = MemFitStore()
    memory.append("budget is ten", segment="finance")
    memory.append("launch on Friday", segment="release")
    result = memory.retrieve(("budget",), {1: .1}, limit=1)
    assert result[0]["text"] == "budget is ten" and len(memory.turns) == 2
