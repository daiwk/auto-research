from types import SimpleNamespace

import pytest

torch = pytest.importorskip("torch")

from auto_research.post_training.oct11_objectives import SkillActivity
from auto_research.post_training.sguid_checkpoint import (
    _response_logits, adapter_digest, co_evolve, curation_prompt, parse_skill,
    signed_forward_kl, skill_teacher_prompt, snapshot_adapters,
    step_if_finite_nonzero_gradient,
)


def test_generated_skill_json_rejects_missing_fields_and_no_fallback():
    good = parse_skill('```json\n{"title":"Ratios","principle":"Reduce a ratio to common units before comparing quantities."}\n```')
    assert good["title"] == "Ratios"
    for text in ('{"title":"Skill"}', "handwritten fallback", '{"title":"a","principle":"short"}'):
        with pytest.raises(ValueError, match="valid skill JSON"):
            parse_skill(text)


def test_privileged_training_reference_never_enters_skill_teacher_question_prompt():
    prompt = curation_prompt("QUESTION", "STUDENT_TRACE", "PRIVATE_TRAIN_REFERENCE", False)
    assert "PRIVATE_TRAIN_REFERENCE" in prompt and "Verifier correct: False" in prompt
    skill = {"title": "Units", "principle": "Normalize units before computing a sum."}
    teacher = skill_teacher_prompt("QUESTION", skill)
    assert "QUESTION" in teacher and "PRIVATE_TRAIN_REFERENCE" not in teacher
    assert "reference" not in skill_teacher_prompt.__code__.co_varnames


def test_two_rounds_use_updated_student_and_restore_exact_round_base():
    model = torch.nn.Linear(1, 1)
    calls, bases = [], []
    rows = [{"question": "training only", "answer": "#### 1"}]

    def curate(current, received, r):
        assert received is rows
        bases.append(current.weight.detach().clone())
        return {f"r{r}": {"title": "generated", "principle": "student procedure"}}, [{"round": r}]

    def distill(current, received, bank, probe, r):
        assert received is rows
        assert torch.equal(current.weight, bases[r])
        calls.append((r, probe, tuple(bank)))
        with torch.no_grad():
            current.weight.add_(100 if probe else 1)
        return {f"r{r}": SkillActivity(2, 2, 2, 2)}, [{"actual_update": True}]

    records = co_evolve(model, rows, curate=curate, distill=distill)
    assert calls == [(0, True, ("r0",)), (0, False, ("r0",)),
                     (1, True, ("r1",)), (1, False, ("r1",))]
    assert torch.equal(bases[1], bases[0] + 1)
    assert all(r["restored_sha256"] == r["round_base_sha256"] for r in records)
    assert records[0]["next_policy_sha256"] == records[1]["round_base_sha256"]


def test_no_eligible_bank_stops_without_compact_training_or_second_round():
    model = torch.nn.Linear(1, 1)
    original = adapter_digest(snapshot_adapters(model))
    calls = []

    def distill(current, rows, bank, probe, r):
        calls.append(probe)
        with torch.no_grad():
            current.weight.add_(50)
        return {"s": SkillActivity(3, 3, 0, 0)}, [{"negative_only": True}]

    records = co_evolve(model, [], curate=lambda *_: ({"s": "generated"}, []), distill=distill)
    assert calls == [True] and len(records) == 1 and records[0]["status"] == "failed"
    assert "persistence" in records[0]["failure"]
    assert adapter_digest(snapshot_adapters(model)) == original


def test_empty_generated_bank_is_explicit_failure():
    model = torch.nn.Linear(1, 1)
    records = co_evolve(model, [], curate=lambda *_: ({}, [{"rejected": True}]),
                        distill=lambda *_: pytest.fail("must not distill empty bank"))
    assert records[0]["status"] == "failed" and records[0]["candidate_bank"] == {}


def test_probe_failure_restores_actual_round_adapters():
    model = torch.nn.Linear(1, 1)
    original = adapter_digest(snapshot_adapters(model))
    journal = []

    def fail(current, *_):
        with torch.no_grad():
            current.weight.add_(100)
        raise RuntimeError("actual training failed")

    with pytest.raises(RuntimeError, match="training failed"):
        co_evolve(model, [], curate=lambda *_: ({"s": "generated"}, []), distill=fail,
                  journal=lambda records: journal.append(records[0].copy()))
    assert adapter_digest(snapshot_adapters(model)) == original
    assert len(journal) == 1 and journal[0]["status"] == "failed"
    assert "actual training failed" in journal[0]["failure"]
    assert journal[0]["restored_sha256"] == original


def test_zero_gradient_does_not_advance_existing_optimizer_momentum():
    parameter = torch.nn.Parameter(torch.tensor([1.]))
    optimizer = torch.optim.AdamW([parameter], lr=.1, weight_decay=.1)
    parameter.grad = torch.ones_like(parameter)
    gradient, active = step_if_finite_nonzero_gradient([parameter], optimizer)
    assert gradient == 1 and active
    previous = parameter.detach().clone()
    step = optimizer.state[parameter]["step"].clone()
    momentum = optimizer.state[parameter]["exp_avg"].clone()
    parameter.grad.zero_()
    gradient, active = step_if_finite_nonzero_gradient([parameter], optimizer)
    assert gradient == 0 and not active
    assert torch.equal(parameter, previous)
    assert torch.equal(optimizer.state[parameter]["step"], step)
    assert torch.equal(optimizer.state[parameter]["exp_avg"], momentum)


@pytest.mark.parametrize("invalid", [float("nan"), float("inf")])
def test_nonfinite_gradient_is_a_failure_not_an_update(invalid):
    parameter = torch.nn.Parameter(torch.tensor([1.]))
    optimizer = torch.optim.AdamW([parameter], lr=.1)
    parameter.grad = torch.tensor([invalid])
    with pytest.raises(RuntimeError, match="non-finite"):
        step_if_finite_nonzero_gradient([parameter], optimizer)
    assert float(parameter.detach()) == 1. and not optimizer.state


def test_signed_full_vocab_kl_detaches_teacher_and_preserves_negative_signal():
    student = torch.zeros(2, 3, 5, requires_grad=True)
    teacher = torch.zeros_like(student, requires_grad=True)
    with torch.no_grad():
        teacher[..., 0] = 2
    mask = torch.tensor([[True, True, False], [True, True, False]])
    actions = torch.zeros(2, 3, dtype=torch.long)
    loss, c, support = signed_forward_kl(student, teacher, actions, mask,
                                        torch.tensor([True, False]))
    assert c.tolist() == [1., -1.] and bool((support > .05).all())
    loss.backward()
    assert teacher.grad is None and not c.requires_grad
    assert torch.allclose(student.grad[0], -student.grad[1])
    assert float(student.grad[:, 2].abs().sum()) == 0


def test_weak_signal_does_not_force_update():
    student = torch.zeros(1, 2, 3, requires_grad=True)
    teacher = student.detach().clone()
    loss, c, _ = signed_forward_kl(student, teacher, torch.zeros(1, 2, dtype=torch.long),
                                  torch.ones(1, 2, dtype=torch.bool), torch.tensor([True]))
    loss.backward()
    assert c.tolist() == [0.] and float(student.grad.abs().sum()) == 0


def test_nonzero_signed_gates_can_cancel_and_must_not_claim_an_update():
    shared = torch.nn.Parameter(torch.zeros(1, 2, 3))
    teacher = torch.tensor([2., 0., 0.]).expand(2, 2, 3)
    loss, coefficients, _ = signed_forward_kl(
        shared.expand(2, 2, 3), teacher, torch.zeros(2, 2, dtype=torch.long),
        torch.ones(2, 2, dtype=torch.bool), torch.tensor([True, False]))
    assert coefficients.tolist() == [1., -1.]
    loss.backward()
    optimizer = torch.optim.AdamW([shared], lr=.1)
    gradient, active = step_if_finite_nonzero_gradient([shared], optimizer)
    assert gradient == 0 and not active and not optimizer.state


def test_teacher_and_student_response_scores_align_despite_different_prefix_lengths():
    class Model:
        def __call__(self, *, input_ids, use_cache):
            assert not use_cache
            return SimpleNamespace(logits=torch.arange(input_ids.shape[1]).float()[None, :, None])

    response = torch.tensor([[7, 8, 9]])
    short = _response_logits(Model(), torch.tensor([[1, 2]]), response)
    long = _response_logits(Model(), torch.tensor([[1, 2, 3, 4, 5]]), response)
    assert short.shape == long.shape == (1, 3, 1)
    assert short.flatten().tolist() == [1., 2., 3.]
    assert long.flatten().tolist() == [4., 5., 6.]
