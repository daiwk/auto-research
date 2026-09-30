import numpy as np
import pytest

torch = pytest.importorskip("torch")

from auto_research.agent_research.latest_20260930_followup import (
    gaussian_evsi, premature_disclosure_rate, set_level_uplift, user_fidelity_score,
)
from auto_research.foundation_latest_20260930_followup import (
    lift_fuse, lift_loss, lift_topk_state, triadic_linear_attention,
)
from auto_research.post_training.latest_20260930_followup import (
    graft_peer_objective, oasis_forward_kl, oasis_select_scaffold,
    pr_opd_alignment, ride_loss, ride_target,
)
from auto_research.reproductions.grp.model import GRPHeads, block_causal_mask, m_grpo_loss


def test_lift_sparse_state_fusion_and_loss_keep_teacher_detached():
    logits = torch.tensor([[[0.0, 2.0, 1.0, -1.0]]], requires_grad=True)
    teacher = torch.tensor([[[0.5, 1.5, 0.0, -0.5]]], requires_grad=True)
    state = lift_topk_state(teacher, k=2)
    assert torch.allclose(state.sum(-1), torch.ones(1, 1))
    assert int((state > 0).sum()) == 2
    hidden = torch.randn(1, 1, 3)
    embedding = torch.randn(4, 3)
    gate = torch.nn.Linear(6, 6)
    up = torch.nn.Linear(6, 6)
    down = torch.nn.Linear(6, 3)
    assert lift_fuse(hidden, state, embedding, gate, up, down).shape == hidden.shape
    loss, audit = lift_loss(logits, teacher, torch.tensor([[1]]), k=2)
    loss.backward()
    assert audit["state_kl"] >= 0
    assert teacher.grad is None
    assert torch.isfinite(logits.grad).all()


def test_triadic_attention_matches_explicit_recurrence_and_e1_reduces_to_linear():
    torch.manual_seed(0)
    q = torch.randn(1, 4, 3)
    k = torch.randn(1, 4, 3)
    value = torch.randn(1, 4, 2)
    q2 = torch.ones(1, 4, 1)
    k2 = torch.ones(1, 4, 1)
    output, state = triadic_linear_attention(q, q2, k, k2, value)
    matrix = torch.zeros(1, 3, 2)
    expected = []
    for index in range(4):
        matrix += torch.einsum("bi,bj->bij", k[:, index], value[:, index])
        expected.append(torch.einsum("bi,bij->bj", q[:, index], matrix))
    assert state.shape == (1, 3, 1, 2)
    assert torch.allclose(output, torch.stack(expected, 1), atol=1e-6)


def test_oasis_uses_shortest_verified_scaffold_and_distinct_failed_context():
    rollouts = [
        {"id": "long", "tokens": [1, 2, 3], "verified": True},
        {"id": "failed", "tokens": [4], "verified": False},
        {"id": "short", "tokens": [5, 6], "verified": True},
    ]
    scaffold, context = oasis_select_scaffold(rollouts)
    assert scaffold["id"] == "short"
    assert context["id"] == "failed"
    assert oasis_select_scaffold([{**rollouts[1]}]) is None
    student = torch.log_softmax(torch.randn(1, 2, 3), -1).requires_grad_()
    teacher = torch.softmax(torch.randn(1, 2, 3), -1)
    loss = oasis_forward_kl(student, teacher, torch.tensor([[1, 0]], dtype=torch.bool))
    loss.backward()
    assert student.grad[:, 1].abs().sum() == 0


def test_graft_ride_and_pr_opd_gradient_boundaries():
    current = torch.tensor([[-0.2, -0.4], [-2.0, -2.0]], requires_grad=True)
    old = current.detach() + 0.1
    loss, audit = graft_peer_objective(
        current, old, torch.tensor([1.0, -1.0]), torch.tensor([-0.2, -3.0]), torch.ones_like(current, dtype=torch.bool),
    )
    loss.backward()
    assert audit["mean_compatibility"] == pytest.approx(1.0)
    assert torch.isfinite(current.grad).all()

    base = torch.zeros(1, 2, 3, requires_grad=True)
    teacher = torch.ones(1, 2, 3, requires_grad=True)
    target = ride_target(base, teacher, extrapolation=1.5)
    assert torch.allclose(target, torch.full_like(target, 1.5))
    student = torch.zeros_like(target, requires_grad=True)
    ride_loss(student, base, teacher, token_mask=torch.tensor([[1, 0]])).backward()
    assert base.grad is None and teacher.grad is None
    assert student.grad[:, 1].abs().sum() == 0

    privileged = [torch.randn(1, 2, 4, requires_grad=True) for _ in range(2)]
    learner = [value.detach().clone().requires_grad_() for value in privileged]
    alignment = pr_opd_alignment(learner, privileged, torch.ones(1, 2))
    assert alignment.item() == pytest.approx(0.0, abs=1e-6)
    alignment.backward()
    assert all(value.grad is None for value in privileged)


def test_user_proxy_and_uplift_metrics_preserve_contracts():
    score = user_fidelity_score([[1, 1, 1], [1, 0, 1]])
    assert score["user_fidelity_score"] == pytest.approx(0.5)
    audit = premature_disclosure_rate([
        {"disclosed_fields": ["phone"]},
        {"requested_fields": ["name"], "disclosed_fields": ["name"]},
    ], {"phone", "name"})
    assert audit == {"premature_disclosures": 1, "private_disclosures": 2, "rate": 0.5}
    uplift, report = set_level_uplift([1, 0, 1], [0, 1, 1])
    assert uplift.tolist() == [1.0, -1.0, 0.0]
    assert report["mean_uplift"] == 0.0
    selected, scores = gaussian_evsi([0.2, 0.1], [[0.1, 0.0], [0.0, 1.0]], [0, 1])
    assert selected == 1 and scores[1] > scores[0]


def test_grp_block_mask_detached_ranker_and_m_grpo_guard():
    mask = block_causal_mask(2, 3)
    assert bool(mask[:3, 3:].all()) and bool(mask[3:, :3].all())
    assert not bool(mask.diag().any())
    model = GRPHeads(8, 11, heads=2)
    history = torch.randn(1, 4, 8, requires_grad=True)
    targets = torch.randn(1, 6, 8)
    candidates = torch.randn(1, 2, 8, requires_grad=True)
    generation, ranking = model(history, targets, candidates, items=2, codes_per_item=3)
    ranking.sum().backward()
    assert candidates.grad is None and history.grad is None
    assert generation.shape == (1, 6, 11) and ranking.shape == (1, 2, 2)
    policy = torch.tensor([-0.1, -1.0], requires_grad=True)
    loss, audit = m_grpo_loss(
        policy, torch.tensor([-0.5, -0.9]), torch.tensor([-0.5, -0.9]),
        torch.tensor([1.0, 0.0]), torch.tensor(-0.6), margin=0.1,
    )
    loss.backward()
    assert audit["recall_guard"] > 0 and torch.isfinite(policy.grad).all()
