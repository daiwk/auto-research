import numpy as np
import pytest

torch = pytest.importorskip("torch")

from auto_research.agent_research.latest_20260930_closure import (
    bootstrap_error_certificate, continuous_context, local_suffix_edit, mnemon_view,
    rubric_process_credit, symbolic_gate,
)
from auto_research.foundation_latest_20260930_closure import (
    frac_modes, frac_recurrence, telescopic_loss,
)
from auto_research.post_training.latest_20260930_closure import (
    mas_privileged_coordination, mas_role_advantage, olive_loss,
    reward_aligned_weights, rfpo_advantages, ross_selective_loss,
)
from auto_research.recommendation_latest_20260930_closure import (
    Skill, SkillGenome, SkillGenomeController, promptshift_metrics,
    promptshift_rerank,
)
from auto_research.evolution.compatibility import operator_registry
from auto_research.reproductions.rankmixer.model import RankMixerConfig, build_model


def test_evoskillrec_executes_validates_promotes_and_reuses():
    controller = SkillGenomeController(lambda values: -float(np.square(values - 3).mean()))
    controller.register(Skill("scale", "features", "features", lambda x: x * 2))
    controller.register(Skill("bias", "features", "score", lambda x: x + 1))
    genome = SkillGenome(("scale", "bias"), "features", "score")
    result = controller.evaluate_and_promote(genome, np.array([1.0]), baseline=-2.0)
    assert result["promoted"] is True
    assert result["output"].tolist() == [3.0]
    assert controller.reuse() == (genome,)
    with pytest.raises(TypeError):
        controller.validate(SkillGenome(("bias", "scale"), "features", "features"))
    spec = operator_registry()["rankmixer_evoskill"]
    assert spec.paper_ids == ("2609.34552",)
    assert spec.compatible_models == ("rankmixer",)

    class Data:
        item_count = 7
        item_features = np.eye(7, 4, dtype=np.float32)

    model = build_model(
        "rankmixer_evoskill", Data,
        RankMixerConfig(dimensions=8, tokens=4, heads=4, layers=1),
    )
    scores = model(torch.tensor([[0, 1, 2, 3]]))
    assert scores.shape == (1, 7)
    assert model.blocks[0].skill_genome[0] == ("head-mix", "tokens", "tokens")


def test_promptshift_reports_drift_and_reranks_toward_tail_for_mainstream_user():
    metrics = promptshift_metrics([0, 1, 2], [0, 2, 3], [.9, .8, .1, .2], {2, 3}, k=3)
    assert metrics["drift"] > 0 and metrics["difficulty_at_k"] > 0
    reranked, _ = promptshift_rerank([0, 1, 2], [.9, .8, .7], [.9, .8, .1], 1.0)
    assert reranked[0] == 2


def test_telescopic_full_anchor_always_receives_gradient():
    logits = [torch.randn(2, 3, 7, requires_grad=True) for _ in range(3)]
    loss, audit = telescopic_loss(logits, torch.randint(0, 7, (2, 3)), 1)
    loss.backward()
    assert audit["sampled_depth"] == 1
    assert logits[0].grad is not None and logits[-1].grad is not None
    assert logits[1].grad is None


def test_frac_uses_bounded_modes_and_retains_slower_tail_than_single_fast_mode():
    rates, weights = frac_modes(8, .01, 1.0, .5)
    outputs, state = frac_recurrence(np.r_[np.ones((1, 1)), np.zeros((49, 1))], rates, weights)
    assert state.shape == (8, 1) and outputs[-1, 0] > np.exp(-49)
    assert weights.sum() == pytest.approx(1.0)


def test_rfpo_olive_ross_and_reward_alignment_boundaries():
    advantages, audit = rfpo_advantages([.1, .7, .8, .2], length_bias=.01)
    assert advantages.shape == (3,) and audit["critic_frozen"]

    logits = torch.randn(2, 5, 9, requires_grad=True)
    tokens = torch.randint(0, 9, (2, 5))
    olive, mask = olive_loss(logits, tokens, [2, 3])
    olive.backward(retain_graph=True)
    assert not mask[0, 1] and mask[0, 2]
    assert logits.grad[0, :2].abs().sum() == 0

    logits.grad.zero_()
    selected = torch.tensor([[0, 1, 0, 1, 0], [0, 0, 1, 0, 0]], dtype=torch.bool)
    ross_selective_loss(logits, tokens, selected).backward()
    assert logits.grad[~selected].abs().sum() == 0

    teacher = torch.log_softmax(torch.randn(2, 4, 7), -1)
    student = torch.log_softmax(torch.randn(2, 4, 7), -1)
    weights = reward_aligned_weights(teacher, student, torch.ones(2, 4))
    assert weights.mean() == pytest.approx(1.0, rel=1e-5)


def test_mas_opd_detaches_role_and_privileged_teacher_signals():
    target = torch.randn(1, 3, requires_grad=True)
    other = torch.randn(1, 3, requires_grad=True)
    advantage, audit = mas_role_advantage(target, other, torch.tensor([[1., 1., 0.]]))
    assert not advantage.requires_grad and audit["active_tokens"] == 2
    student = torch.log_softmax(torch.randn(1, 3, 5), -1).detach().requires_grad_()
    teacher = torch.log_softmax(torch.randn(1, 3, 5), -1).detach().requires_grad_()
    loss = mas_privileged_coordination(student, teacher, torch.tensor([[1., 0., 1.]]))
    loss.backward()
    assert teacher.grad is None and student.grad[:, 1].abs().sum() == 0


def test_agent_kernels_keep_history_and_gold_boundaries_explicit():
    credit, report = rubric_process_credit([.2, .5], [.7, .4])
    assert credit.tolist() == pytest.approx([.5, 0]) and report["new_support"] == pytest.approx(.5)
    prompt = continuous_context("task", ["old", "recent"], "new obs", memory_budget=1)
    assert prompt == {"task": "task", "memory": ("recent",), "observation": "new obs"}
    accepted, blocked = symbolic_gate(
        ["open", "take"], {"at-door"},
        {"open": ({"at-door"}, {"open"}), "take": ({"object-visible"}, {"holding"})},
    )
    assert accepted == ["open"] and blocked[0]["missing"] == ["object-visible"]
    assert local_suffix_edit(["a", "b", "c"], 1, ["x", "y"]) == ["a", "x", "y"]


def test_cluster_certificate_and_mnemon_view_are_deterministic():
    result = bootstrap_error_certificate([[0, 0], [0], [0, 1]], budget=.8, samples=300, seed=42)
    assert result["tasks"] == 3 and result["certified"]
    view, audit = mnemon_view([
        {"date": "2026-01-01", "text": "likes jazz"},
        {"date": "2026-02-01", "text": "likes rock now"},
        {"date": "2026-03-01", "text": "weather"},
    ], ["likes"], budget=1)
    assert view[0]["date"] == "2026-02-01" and audit["view_size"] == 1
