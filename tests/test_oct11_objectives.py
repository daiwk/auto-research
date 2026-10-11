from copy import deepcopy

import pytest

torch = pytest.importorskip("torch")

from auto_research.post_training.oct11_objectives import (
    SkillActivity, conditional_kl, pivot_loss, pivot_routing, select_sguid_skills,
    sguid_coefficient, sguid_round, zcpo_coefficients, zcpo_loss,
)


def test_zcpo_zero_sum_common_shift_and_length_normalization():
    mask = torch.tensor([[1, 1, 0], [1, 1, 1]], dtype=torch.bool)
    kl = torch.tensor([[.1, .3, float("nan")], [.4, .4, .4]])
    c, active = zcpo_coefficients(torch.tensor([0., 1.]), kl, mask, .5)
    assert active and torch.allclose(c, torch.tensor([-.95, .95]))
    shifted, _ = zcpo_coefficients(torch.tensor([0., 1.]), kl + 5, mask, .5)
    assert torch.allclose(c, shifted, atol=1e-6) and abs(float(c.sum())) < 1e-6
    assert not c.requires_grad


def test_zcpo_equal_reward_skips_bad_reference_and_returns_zero_gradient():
    lp = torch.zeros(2, 3, requires_grad=True)
    loss, stats = zcpo_loss(lp, lp.detach(), None, None, torch.ones(2), torch.ones_like(lp).bool())
    loss.backward()
    assert not stats["active"] and torch.equal(lp.grad, torch.zeros_like(lp))


def test_zcpo_detaches_full_vocabulary_coefficients():
    s = torch.randn(2, 3, 8, requires_grad=True)
    ref = torch.randn_like(s, requires_grad=True)
    lp = s.log_softmax(-1)[..., 0]
    loss, stats = zcpo_loss(lp, lp.detach(), s, ref, torch.tensor([1., 0.]), torch.ones(2, 3).bool())
    loss.backward()
    assert stats["active"] and s.grad.abs().sum() > 0 and ref.grad is None
    assert conditional_kl(s, s).abs().max() < 1e-6


def test_pivot_averages_response_ppl_not_exp_of_average_nll():
    # Prompt 0: mean PPL 5; prompt 1: mean PPL 4. Geometric mean would reverse them.
    lp = -torch.tensor([[[1.], [9.]], [[4.], [4.]]]).log()
    routed, _, _ = pivot_routing(lp, torch.ones_like(lp).bool(), step=5, total_steps=10)
    assert routed.tolist() == [False, True]
    assert not pivot_routing(lp, torch.ones_like(lp).bool(), step=0, total_steps=10)[0].any()
    assert pivot_routing(lp, torch.ones_like(lp).bool(), step=10, total_steps=10)[0].all()


def test_pivot_opd_is_forward_kl_token_sum_and_teacher_frozen():
    s = torch.zeros(2, 2, 3, 4, requires_grad=True)
    t = torch.tensor([2., 0., 0., 0.]).expand_as(s).clone().requires_grad_()
    actions = torch.zeros(2, 2, 3, dtype=torch.long)
    mask = torch.ones_like(actions).bool()
    loss, stats = pivot_loss(s, t, actions, torch.full_like(actions, -1.386294, dtype=torch.float),
                             torch.zeros(2, 2), mask, step=0, total_steps=10)
    q, p = t.detach().log_softmax(-1), s.detach().log_softmax(-1)
    expected = 3 * (q.exp() * (q - p)).sum(-1).mean()
    assert torch.allclose(loss, expected) and not stats["routed_grpo"].any()
    loss.backward()
    assert s.grad.abs().sum() > 0 and t.grad is None


def test_sguid_verifier_sign_gate_and_persistence():
    student = torch.zeros(3, 2)
    teacher = torch.tensor([[.2, .2], [.2, .2], [.01, .01]])
    c, _ = sguid_coefficient(teacher, student, torch.ones_like(student).bool(),
                             torch.tensor([True, False, True]))
    assert c.tolist() == [1., -1., 0.]
    activities = {"good": SkillActivity(4, 4, 3, 2), "decayed": SkillActivity(4, 10, 4, 2),
                  "never-positive": SkillActivity(10, 10, 0, 0)}
    assert select_sguid_skills(activities, late_minimum=2, tau=2) == ("good",)


def test_sguid_compact_run_restarts_from_base_not_probe_weights():
    model = torch.nn.Linear(1, 1)
    initial = deepcopy(model.state_dict())
    rows = [{"training_problem": "only train"}]
    calls = []

    def curate(m, received):
        assert received is rows
        return {"skill": "generated training skill"}

    def distill(m, received, bank, collect):
        assert received is rows
        assert torch.equal(m.weight, initial["weight"])
        with torch.no_grad():
            m.weight.add_(1 if collect else 2)
        calls.append(collect)
        return {"skill": SkillActivity(2, 2, 2, 2)}

    report = sguid_round(model, rows, curate=curate, distill=distill)
    assert calls == [True, False] and report["restarted_from_round_base"]
    assert torch.equal(model.weight, initial["weight"] + 2)


def test_sguid_failed_probe_restores_base():
    model = torch.nn.Linear(1, 1)
    initial = deepcopy(model.state_dict())

    def fail(m, rows, bank, collect):
        with torch.no_grad():
            m.weight.add_(100)
        raise RuntimeError("failed training")

    with pytest.raises(RuntimeError):
        sguid_round(model, [], curate=lambda *_: {"s": "generated"}, distill=fail)
    assert torch.equal(model.weight, initial["weight"])
