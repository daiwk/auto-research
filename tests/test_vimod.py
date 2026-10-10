import pytest
from types import SimpleNamespace

torch = pytest.importorskip("torch")

from auto_research.multimodal.vimod import (DART, TRACE, auxiliary_call_loss,
    balanced_set_loss, capacities, dart_distillation, joint_kv,
    online_teacher_loss, trace_policy_loss)


def test_capacity_implicit_gradient_and_shift_invariance():
    score = torch.tensor([.3, -.5, .9], dtype=torch.double, requires_grad=True)
    counts = torch.tensor([3, 2, 3])
    assert torch.autograd.gradcheck(lambda x: capacities(x, counts, 5), (score,))
    actual = capacities(score, counts, 5)
    assert actual.sum().item() == pytest.approx(8)
    torch.testing.assert_close(actual, capacities(score + 17, counts, 5))
    assert torch.autograd.grad(actual.sum(), score)[0].abs().max() < 1e-12


def test_dart_hard_support_surrogate_gradient_and_kv_recovery():
    torch.manual_seed(4)
    dart = DART(8, 4, affinity_dim=3, upper=6)
    fine = torch.randn(12, 8)
    grid = torch.arange(12) // 4
    memory = dart(fine, grid)
    assert memory.counts.sum() == 12
    assert (memory.counts == torch.bincount(memory.membership, minlength=3)).all()
    support = torch.nn.functional.one_hot(memory.membership, 3).bool()
    assert memory.weights[~support].abs().max() < 1e-7
    torch.testing.assert_close(memory.weights.sum(0), torch.ones(3))
    (memory.coarse.square().sum()).backward()
    assert dart.capacity.weight.grad.abs().sum() > 0
    assert dart.fine_projection.weight.grad.abs().sum() > 0
    key, value = torch.randn(2, 12, 4), torch.randn(2, 12, 4)
    coarse = dart.coarse_kv(memory, key, value)
    text = (torch.randn(2, 2, 4), torch.randn(2, 2, 4))
    active = torch.tensor([True, False, True])
    joined = joint_kv(memory, active, coarse, (key, value), text)
    assert joined[0].shape[-2] == 3 + memory.counts[active].sum() + 2
    selected = memory.fine_indices(active)
    torch.testing.assert_close(joined[0][:, 3:3 + len(selected)], key[:, selected])
    empty = joint_kv(memory, torch.zeros(3, dtype=torch.bool), coarse, (key, value), text)
    assert empty[0].shape[-2] == 5
    # Recovering fine values uses the original bank, not encoded/coarse values.
    torch.testing.assert_close(joined[1][:, 3:3 + len(selected)], value[:, selected])


def test_trace_recurrence_and_replace_not_union():
    model = TRACE(8, 8, layers=2, state_dim=4, key_dim=3)
    hidden, coarse = torch.randn(2, 8), torch.randn(3, 8)
    previous = torch.tensor([True, True, False])
    out = model(hidden, coarse, previous)
    later = model(hidden, coarse, previous, state=out["state"])
    assert not torch.equal(out["state"], later["state"])
    forced = {"gate_logits": torch.tensor([-100., 100.]),
              "region_logits": torch.tensor([-100., -100., 100.])}
    active, _, _, gate = model.choose(forced, previous)
    assert gate == 1 and active.tolist() == [False, False, True]
    forced["gate_logits"] = torch.tensor([100., -100.])
    assert torch.equal(model.choose(forced, previous)[0], previous)


def test_training_objectives_stop_grad_and_skipped_annotations():
    logits = torch.tensor([0., .2, -.4], requires_grad=True)
    loss = balanced_set_loss(logits, torch.tensor([1, 0, 0]))
    assert loss > 0
    assert online_teacher_loss(logits, torch.ones(3), torch.ones(3)).item() == 0
    assert online_teacher_loss(logits, torch.zeros(3), torch.ones(3)).item() == 0
    assert auxiliary_call_loss(logits, True, False) > 0
    assert auxiliary_call_loss(logits, True, True) == 0
    student = torch.randn(2, 3, 7, requires_grad=True)
    teacher = torch.randn(2, 3, 7, requires_grad=True)
    dart_distillation(student, teacher, torch.randint(0, 7, (2, 3)),
                      torch.ones(2, 3, dtype=torch.bool)).backward()
    assert teacher.grad is None and student.grad is not None
    lp = torch.randn(3, requires_grad=True)
    success = torch.tensor([1., 1., 0.], requires_grad=True)
    occupancy = torch.tensor([.1, .4, .2], requires_grad=True)
    trace_policy_loss(lp, lp, success, occupancy).backward()
    assert success.grad is None and occupancy.grad is None


def test_checkpoint_trace_training_contracts_without_gold_observation():
    from auto_research.multimodal.vimod_checkpoint import CheckpointMemory, SmolVLMJointKV

    dart, trace = DART(8, 4, affinity_dim=3, upper=6), TRACE(8, 8, layers=2, state_dim=4, key_dim=3)
    memory = dart(torch.randn(8, 8), torch.arange(8) // 4)
    backend = SmolVLMJointKV.__new__(SmolVLMJointKV)
    backend.dart, backend.trace = dart, trace

    class Tokenizer:
        eos_token_id = 99

        def __call__(self, text, **kwargs):
            return {"input_ids": torch.tensor([[1, 2, 3, 4]])}

        def decode(self, tokens, **kwargs):
            return "generated-prefix-only"

    backend.processor = SimpleNamespace(tokenizer=Tokenizer())
    backend.prefill = lambda *_: CheckpointMemory(memory, [], [], [], torch.tensor([[1]]), 1, torch.randn(2, 8))
    backend.decode_step = lambda bank, active: (torch.tensor([[1., 0.]]), [], torch.randn(2, 8))
    loss = backend.trace_supervised_loss(None, "question", "training reference",
                                        [[0], [4]], stage="joint", routing_interval=2)
    loss.backward()
    assert trace.gate.weight.grad.norm() > 0
    assert not trace.query[1].weight.requires_grad
    assert not trace.threshold.weight.requires_grad
    observed = []

    def teacher(**request):
        observed.append(request)
        assert set(request) == {"image", "question", "prefix"}
        assert request["question"] == "question"
        return {"labels": [1, 0], "valid": [1, 1]}

    trace.zero_grad()
    loss, _ = backend.trace_rl_loss(None, "question", lambda _: False, teacher,
                                    group=2, maximum_tokens=2, routing_interval=1)
    loss.backward()
    assert observed and trace.threshold.weight.grad is not None
    assert all(parameter.requires_grad for parameter in trace.parameters())
