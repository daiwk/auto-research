"""Independent OPRD/OpCredit formulas, isolation and invalid-input contracts."""
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest
import torch
from torch import nn

from auto_research.post_training import operation_credit as oc
from auto_research.post_training import reminder_distillation as rd

ROOT = Path(__file__).resolve().parents[1]


def test_oprd_reminder_catalog_cannot_overwrite_the_existing_reverse_distillation_paper():
    directory = ROOT / "src/auto_research/paper_specs/catalog/post-training"
    previous = json.loads((directory / "oprd.json").read_text())
    reminder = json.loads((directory / "oprd-reminder.json").read_text())
    assert previous["key"] == "oprd" and "2609.08798" in previous["paper_url"]
    assert previous["detail_path"] == "post-training/2609.08798-oprd/README.md"
    assert previous["adapter"] == "oprd"
    assert reminder["key"] == "oprd-reminder" and "2610.21496" in reminder["paper_url"]
    assert reminder["detail_path"] == "post-training/2610.21496-oprd-reminder/README.md"


@pytest.mark.parametrize("key", ["oprd-reminder", "opcredit"])
def test_supplement_catalog_cannot_promote_diagnostic_components(key):
    path = ROOT / "src/auto_research/paper_specs/catalog/post-training" / f"{key}.json"
    row = json.loads(path.read_text())
    assert row["adapter"] is None and row["implementation_status"] == "component_only"
    assert row["evaluation_tier"] == "l1_mechanism" and row["diagnostic_only"] is True
    assert row["promotion_eligible"] is False and row["evolve_integrated"] is False
    assert row["full_experiment_status"] == "not_reproduced_high_cost"
    assert row["requires_gpu_validation"] is True
    assert row["gpu_validation_artifact"] == f"docs/gpu-validations/{key}-supplement-a100-20261017.json"
    assert row["published_at"].startswith("2026-10-15T") and row["first_author_affiliation"]
    assert row["code"] is None or row["code"].startswith("https://github.com/")


class RecordingPolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(64, 6)
        self.calls = []

    def forward(self, ids):
        self.calls.append(ids.detach().clone())
        return self.embedding(ids).cumsum(1)


def test_oprd_teacher_only_scope_rebuilds_and_scores_identical_response_prefixes():
    student, teacher = RecordingPolicy(), RecordingPolicy()
    turns = (rd.AssistantTurn((1, 2), (3, 4)), rd.AssistantTurn((1, 2, 3, 4, 5), (6, 7)),
             rd.AssistantTurn((1, 2, 3, 4, 5, 6, 7, 8), (9,)))
    reminders = rd.ScopedReminders((50,), ((0, (51,)),))
    current, privileged, labels = rd.score_trajectory(student, teacher, turns, reminders, device="cpu")
    assert current.shape == privileged.shape == (5, 6) and labels.tolist() == [3, 4, 6, 7, 9]
    for i, turn in enumerate(turns):
        assert student.calls[i].tolist()[0] == list(turn.history + turn.response[:-1])
        assert teacher.calls[i].tolist()[0] == list(turn.history + reminders.active(i) + turn.response[:-1])
        assert (51 in teacher.calls[i]) == (i == 1)
        assert 50 not in student.calls[i] and 51 not in student.calls[i]
    current.sum().backward()
    assert student.embedding.weight.grad is not None and not privileged.requires_grad
    assert teacher.embedding.weight.grad is None
    with pytest.raises(ValueError, match="following turn"):
        rd.score_trajectory(student, teacher, turns, rd.ScopedReminders((), ((2, (51,)),)), device="cpu")
    with pytest.raises(ValueError, match="separate"):
        rd.score_trajectory(student, student, turns, reminders, device="cpu")
    aliased = RecordingPolicy()
    aliased.embedding = student.embedding
    with pytest.raises(ValueError, match="share parameter"):
        rd.score_trajectory(student, aliased, turns, reminders, device="cpu")


def test_oprd_shared_top_support_renormalization_temperature_and_detach():
    student = torch.tensor([[[3., 1., -2., .5, 0.]]], dtype=torch.float64, requires_grad=True)
    teacher = torch.tensor([[[-2., .5, 4., -1., 0.]]], dtype=torch.float64, requires_grad=True)
    mask = torch.ones(1, 1, dtype=torch.bool)
    values, indices = rd.shared_support_reverse_kl(student, teacher, mask, top_k=3, temperature=2.)
    ps, pt = (student.detach() / 2).softmax(-1)[0, 0], (teacher.detach() / 2).softmax(-1)[0, 0]
    support = sorted(range(5), key=lambda i: max(float(ps[i]), float(pt[i])), reverse=True)[:3]
    assert set(indices[0, 0].tolist()) == set(support)
    p, q = ps[support] / ps[support].sum(), pt[support] / pt[support].sum()
    expected = 4 * sum(float(p[i]) * math.log(float(p[i] / q[i])) for i in range(3))
    torch.testing.assert_close(values[0, 0], torch.tensor(expected, dtype=torch.float64))
    values.sum().backward()
    assert student.grad is not None and torch.isfinite(student.grad).all() and teacher.grad is None
    zero, _ = rd.shared_support_reverse_kl(student, student.detach(), mask, top_k=3)
    assert zero.item() == 0


def test_oprd_outcome_loss_is_per_trajectory_and_branch_mean_not_global_token_mean():
    torch.manual_seed(3)
    logits = torch.randn(3, 3, 5, dtype=torch.float64, requires_grad=True)
    teacher = torch.randn_like(logits, requires_grad=True)
    labels = torch.tensor([[0, 2, -1], [3, -1, -1], [2, 4, 1]])
    mask = labels >= 0
    successful = torch.tensor([True, True, False])
    loss, parts = rd.outcome_routed_loss(logits, teacher, labels, mask, successful, top_k=5)
    logp, logt = logits.log_softmax(-1), teacher.detach().log_softmax(-1)
    expected_nll = ((-logp[0, 0, 0] - logp[0, 1, 2]) / 2 - logp[1, 0, 3]) / 2
    expected_kl = (logp[2].exp() * (logp[2] - logt[2])).sum(-1).mean()
    torch.testing.assert_close(loss, expected_nll + expected_kl)
    torch.testing.assert_close(parts["success_nll"], expected_nll.detach())
    loss.backward()
    assert teacher.grad is None and torch.equal(logits.grad[~mask], torch.zeros_like(logits.grad[~mask]))


def test_oprd_success_ignores_teacher_and_masked_nan_padding_has_zero_gradient():
    logits = torch.tensor([[[.4, -.2, .1], [float("nan")] * 3]], requires_grad=True)
    labels, mask = torch.tensor([[1, -1]]), torch.tensor([[True, False]])
    loss, info = rd.outcome_routed_loss(logits, torch.full_like(logits, float("nan")), labels, mask,
                                     torch.tensor([True]), top_k=2)
    assert info["failure_reverse_kl"] == 0
    loss.backward()
    assert torch.isfinite(logits.grad).all() and torch.equal(logits.grad[0, 1], torch.zeros(3))
    with pytest.raises(ValueError, match="fit"):
        rd.shared_support_reverse_kl(logits, logits.detach(), mask, top_k=4)
    with pytest.raises(ValueError, match="valid logits"):
        rd.shared_support_reverse_kl(logits, torch.full_like(logits, float("nan")), mask, top_k=2)


def test_oprd_teacher_refresh_is_frozen_and_at_20_40_60_80_percent():
    learner = nn.Linear(2, 2)
    teacher = rd.RefreshingTeacher(learner, 10)
    initial = deepcopy(teacher.model.state_dict())
    with torch.no_grad():
        learner.weight.add_(1)
    assert teacher.after_update(learner, 1) == 0
    torch.testing.assert_close(teacher.model.weight, initial["weight"])
    assert teacher.after_update(learner, 2) == 1
    torch.testing.assert_close(teacher.model.weight, learner.weight)
    assert all(not p.requires_grad for p in teacher.model.parameters()) and not teacher.model.training
    assert teacher.after_update(learner, 8) == 3 and teacher.refresh_count == 4
    assert teacher.after_update(learner, 10) == 0
    with pytest.raises(ValueError, match="increase"):
        teacher.after_update(learner, 10)


def _record(trajectory="0", operation="left", positions=(0,), phase="relation", *, question="q", budget=2,
            visited=frozenset(("root",)), active="root", before=("root",), after=("gold",)):
    state = oc.VisibleKGState(question, active, visited, budget, phase, ("gold", "near", "far"))
    return oc.OperationRecord(trajectory, state, operation, positions, before, after)


def test_opcredit_boc_matches_paper_example_and_deduplicates_trajectory_supports():
    records = [_record("0", "left"), _record("1", "right"), _record("2", "right")]
    rewards = {("q", "0"): 1., ("q", "1"): 0., ("q", "2"): 0.}
    credits, audit = oc.branch_outcome_credit(records, rewards)
    sigma = math.sqrt(2 / 9)
    torch.testing.assert_close(credits, torch.tensor([2 / 3, -1 / 3, -1 / 3], dtype=torch.float64) / (sigma + 1e-6))
    repeated, sizes = oc.branch_outcome_credit(records + [records[0], records[0]], rewards)
    torch.testing.assert_close(credits, repeated[:3])
    assert sizes["context_support_sizes"] == [3] * 5 and sizes["operation_support_sizes"][0] == 1
    assert audit["fallback_decisions"] == 0


@pytest.mark.parametrize("change", [{"phase": "answer"}, {"question": "other"}, {"active": "near"},
                                     {"visited": frozenset(("root", "near"))}, {"budget": 1}])
def test_opcredit_matching_never_mixes_phase_question_entity_visited_or_budget(change):
    records = [_record("0"), _record("1", "right", **change)]
    rewards = {("q", "0"): 1., (records[1].state.question, "1"): 0., ("q", "extra"): 0.}
    _, audit = oc.branch_outcome_credit(records, rewards)
    assert audit["context_support_sizes"] == [1, 1] and audit["fallback_decisions"] == 2


def test_opcredit_ftc_uses_max_opportunity_and_signed_local_difference_with_eligibility():
    neighborhood = oc.TrainingNeighborhood(frozenset(("gold",)), frozenset(("near",)))
    assert oc.frontier_transition_credit(_record(before=("far",), after=("near", "gold", "far")), neighborhood) == (2., True)
    assert oc.frontier_transition_credit(_record(before=("gold",), after=("far",)), neighborhood) == (-2., True)
    assert oc.frontier_transition_credit(_record(before=("gold",), after=("gold",)), neighborhood) == (0., True)
    for before, after in [((), ("gold",)), (None, ("gold",)), (("far",), (None,))]:
        assert oc.frontier_transition_credit(_record(before=before, after=after), neighborhood) == (0., False)
    assert oc.frontier_transition_credit(_record(), oc.TrainingNeighborhood(frozenset(), frozenset())) == (0., False)


def test_opcredit_training_gold_is_not_part_of_actor_observation_contract():
    state = _record().state
    public = state.policy_observation()
    assert set(public) == {"question", "active_entity", "visited_entities", "remaining_budget", "phase", "visible_entities"}
    left, right = oc.TrainingNeighborhood(frozenset(("gold",)), frozenset()), oc.TrainingNeighborhood(frozenset(("root",)), frozenset())
    assert oc.frontier_transition_credit(_record(), left)[0] != oc.frontier_transition_credit(_record(), right)[0]
    assert state.policy_observation() == public
    with pytest.raises(TypeError):
        oc.VisibleKGState(**public, gold_answers=["gold"])


def test_opcredit_span_partition_excludes_observation_and_padding_and_detaches_credit():
    records = [_record(positions=(0, 1)), _record(positions=(3,), phase="answer")]
    mask = torch.tensor([[True, True, False, True, False]])
    boc, ftc = torch.tensor([1., -1.], requires_grad=True), torch.tensor([2., -2.], requires_grad=True)
    outcome, transition = oc.align_decision_credits(records, [("q", "0")], mask, boc, ftc)
    assert outcome.tolist() == [[1., 1., 0., -1., 0.]] and transition.tolist() == [[2., 2., 0., -2., 0.]]
    assert not outcome.requires_grad and not transition.requires_grad
    with pytest.raises(ValueError, match="overlap"):
        oc.align_decision_credits([records[0], _record(positions=(1, 3))], [("q", "0")], mask, boc, ftc)
    with pytest.raises(ValueError, match="every generated"):
        oc.align_decision_credits([records[0]], [("q", "0")], mask, boc[:1], ftc[:1])


def test_opcredit_joint_dual_clip_signed_ftc_kl_entropy_and_equal_trajectory_weight():
    torch.manual_seed(5)
    current = torch.randn(2, 3, 4, dtype=torch.float64, requires_grad=True)
    old, reference = torch.randn_like(current, requires_grad=True), torch.randn_like(current, requires_grad=True)
    labels = torch.tensor([[0, 2, -1], [3, -1, -1]])
    mask = labels >= 0
    boc = torch.tensor([[1., -1., float("nan")], [-2., float("nan"), float("nan")]], dtype=torch.float64, requires_grad=True)
    ftc = torch.tensor([[-1., 2., float("nan")], [1., float("nan"), float("nan")]], dtype=torch.float64, requires_grad=True)
    loss, _ = oc.operation_policy_loss(current, old, reference, labels, mask, boc, ftc)
    rows = []
    for i in range(2):
        values = []
        for j in range(3):
            if not mask[i, j]:
                continue
            lp, lo, lr = current[i, j].log_softmax(-1), old[i, j].detach().log_softmax(-1), reference[i, j].detach().log_softmax(-1)
            rho = (lp[labels[i, j]] - lo[labels[i, j]]).exp()
            a, b = boc[i, j].detach(), ftc[i, j].detach()
            surrogate = torch.minimum(rho * a, rho.clamp(.8, 1.2) * a)
            dual = torch.maximum(surrogate, 3 * a) if a < 0 else surrogate
            values.append(-dual - .1 * b * lp[labels[i, j]] + .002 * (lp.exp() * (lp - lr)).sum() + .001 * (lp.exp() * lp).sum())
        rows.append(torch.stack(values).mean())
    torch.testing.assert_close(loss, torch.stack(rows).mean())
    loss.backward()
    assert torch.isfinite(current.grad).all() and torch.equal(current.grad[~mask], torch.zeros_like(current.grad[~mask]))
    assert all(t.grad is None for t in (old, reference, boc, ftc))


def test_opcredit_masked_nan_logits_are_sanitized_before_softmax_and_ratio_overflow_rejected():
    values = torch.tensor([[[.1, -.2], [float("nan"), float("inf")]]], requires_grad=True)
    labels, mask = torch.tensor([[0, -1]]), torch.tensor([[True, False]])
    credits = torch.tensor([[1., float("nan")]])
    loss, _ = oc.operation_policy_loss(values, values.detach(), values.detach(), labels, mask, credits, credits)
    loss.backward()
    assert torch.isfinite(values.grad).all() and torch.equal(values.grad[0, 1], torch.zeros(2))
    with pytest.raises(ValueError, match="representable"):
        oc.operation_policy_loss(torch.tensor([[[1., 0.]]]), torch.tensor([[[-2000., 0.]]]),
            torch.zeros(1, 1, 2), torch.tensor([[0]]), torch.tensor([[True]]), torch.tensor([[1.]]), torch.tensor([[0.]]))
