"""Independent numerical, isolation, gradient and failure-boundary checks."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest
import torch
from torch import nn

from auto_research.foundation_models.kronlstm import TinyKronLSTM, kronecker_update, recurrent_memory
from auto_research.foundation_models.t_muon import (
    TensorMuon, pack_matrices, rank_polar, tensor_polar, transform_matrix, unpack_matrices,
)
from auto_research.foundation_models.time_jepa import (
    StateNormalizer, TinyTimeJEPA, align_nearest, physical_state_loss, pool_tubelets,
)

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/run_oct20_foundation_components.py"
spec = importlib.util.spec_from_file_location("oct20_foundation_runner", SCRIPT)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
torch.set_num_threads(1)


def test_summary_keeps_guard_boolean_and_rejects_partial_success():
    result = runner.summarize([{"metrics": {"guard": value, "count": index}}
                               for index, value in enumerate((True, True, False))])
    assert result["guard"] is False and result["count"] == {"mean": 1, "std": 1., "n": 3}


@pytest.mark.parametrize("kind", ["identity", "dct", "dst", "dft"])
@pytest.mark.parametrize("size", [1, 3, 6])
def test_orthonormal_transform_and_explicit_oracle(kind, size):
    torch.manual_seed(7)
    x = torch.randn(3, 4, size, dtype=torch.float64)
    m = transform_matrix(size, kind)
    torch.testing.assert_close(m @ m.mH, torch.eye(size, dtype=m.dtype), atol=1e-14, rtol=1e-14)
    torch.testing.assert_close(tensor_polar(x, m), runner._transform_oracle(x, m), atol=1e-10, rtol=1e-10)


def test_partial_polar_rank_zero_and_null_subspaces():
    matrix = torch.diag(torch.tensor([3., 0., 0.], dtype=torch.float64))
    torch.testing.assert_close(rank_polar(matrix), torch.diag(torch.tensor([1., 0., 0.], dtype=torch.float64)))
    assert torch.count_nonzero(rank_polar(torch.zeros(3, 5, dtype=torch.float64))) == 0


@pytest.mark.parametrize("mode,count,heads", [("stack", 3, 1), ("head", 1, 2), ("head-stack", 3, 2)])
def test_tensorization_roundtrip(mode, count, heads):
    matrices = [torch.randn(6, 4, dtype=torch.float64) for _ in range(count)]
    actual = unpack_matrices(pack_matrices(matrices, mode, heads), count, mode, heads)
    for x, y in zip(actual, matrices, strict=True):
        torch.testing.assert_close(x, y, atol=0, rtol=0)


def test_optimizer_momentum_resume_and_original_matrix_scaling():
    torch.manual_seed(10)
    a = nn.Parameter(torch.randn(6, 4, dtype=torch.float64))
    first = TensorMuon([a], mode="head", heads=2, transform="dct", lr=.01)
    a.grad = torch.randn_like(a)
    first.step()
    b = nn.Parameter(a.detach().clone())
    second = TensorMuon([b], mode="head", heads=2, transform="dct", lr=.01)
    second.load_state_dict(copy.deepcopy(first.state_dict()))
    gradient = torch.randn_like(a)
    a.grad, b.grad = gradient, gradient.clone()
    first.step()
    second.step()
    torch.testing.assert_close(a, b, atol=0, rtol=0)


def test_optimizer_rejects_partial_group_without_mutating_state():
    parameters = [nn.Parameter(torch.ones(2, 2)) for _ in range(2)]
    optimizer = TensorMuon(parameters)
    parameters[0].grad = torch.ones_like(parameters[0])
    with pytest.raises(ValueError, match="all grouped"):
        optimizer.step()
    assert not optimizer.state
    for p in parameters:
        assert torch.all(p == 1)
    with pytest.raises(ValueError):
        TensorMuon([nn.Parameter(torch.ones(2, 2, dtype=torch.float16))])
    with pytest.raises(ValueError):
        TensorMuon(parameters, mode="head", heads=2)
    with pytest.raises(ValueError):
        tensor_polar(torch.randn(2, 2, 3), torch.ones(3, 3))


def test_nearest_alignment_masks_gaps_and_earlier_ties():
    times = torch.tensor([0., .5, 1., 2.], dtype=torch.float64)
    measurement_times = torch.tensor([0., 1.], dtype=torch.float64)
    values = torch.tensor([[[10.], [20.]]], dtype=torch.float64)
    aligned, valid = align_nearest(times, measurement_times, values, torch.ones_like(values, dtype=torch.bool), max_gap=.5)
    torch.testing.assert_close(aligned.flatten(), torch.tensor([10., 10., 20., 0.], dtype=torch.float64))
    assert valid.flatten().tolist() == [True, True, True, False]
    with pytest.raises(ValueError):
        align_nearest(times, measurement_times.flip(0), values, torch.ones_like(values, dtype=torch.bool), max_gap=.5)


def test_tubelet_per_variable_valid_mean_no_nan_poison():
    values = torch.tensor([[[2., float("nan")], [4., 7.], [float("nan"), float("nan")], [8., 9.]]])
    valid = torch.tensor([[[True, False], [True, True], [False, False], [True, False]]])
    pooled, mask = pool_tubelets(values, valid)
    torch.testing.assert_close(pooled, torch.tensor([[[3., 7.], [8., 0.]]]))
    assert mask.tolist() == [[[True, True], [True, False]]]
    with pytest.raises(ValueError):
        pool_tubelets(values[:, :3], valid[:, :3])


def test_state_normalizer_train_only_and_unseen_variable_mask():
    train = torch.tensor([[[1., float("nan")], [3., float("nan")]]], dtype=torch.float64, requires_grad=True)
    valid = torch.tensor([[[True, False], [True, False]]])
    norm = StateNormalizer.fit(train, valid, split="train")
    torch.testing.assert_close(norm.mean, torch.tensor([2., 0.], dtype=torch.float64))
    assert not norm.mean.requires_grad
    test = torch.tensor([[[101., 999.]]], dtype=torch.float64)
    transformed, accepted = norm.normalize(test, torch.ones_like(test, dtype=torch.bool))
    torch.testing.assert_close(transformed, torch.tensor([[[99., 0.]]], dtype=torch.float64))
    assert accepted.tolist() == [[[True, False]]]
    assert norm.mean[0] == 2
    with pytest.raises(ValueError, match="training-only"):
        StateNormalizer.fit(test, torch.ones_like(test, dtype=torch.bool), split="test")


def test_physical_loss_exact_gradient_missing_and_stopgrad():
    prediction = torch.tensor([.1, -.8, 100.], dtype=torch.float64, requires_grad=True)
    target = torch.tensor([0., 0., float("nan")], dtype=torch.float64, requires_grad=True)
    valid = torch.tensor([True, True, False])
    loss = physical_state_loss(prediction, target, valid)
    torch.testing.assert_close(loss, torch.tensor((.01 + .55) / 2, dtype=torch.float64))
    loss.backward()
    torch.testing.assert_close(prediction.grad, torch.tensor([.1, -.5, 0.], dtype=torch.float64))
    assert target.grad is None
    prediction.grad = None
    empty = physical_state_loss(prediction, target, torch.zeros_like(valid))
    empty.backward()
    assert empty == 0 and torch.count_nonzero(prediction.grad) == 0


def test_tiny_time_jepa_context_and_state_isolation():
    torch.manual_seed(5)
    model = TinyTimeJEPA().double()
    video = torch.randn(2, 4, 3, 5, dtype=torch.float64)
    context, masked = torch.tensor([0, 3, 6, 9]), torch.tensor([1, 4, 7, 10])
    states = torch.randn(2, 4, 2, dtype=torch.float64, requires_grad=True)
    valid = torch.ones_like(states, dtype=torch.bool)
    before = model(video, context=context, masked=masked, states=states, valid=valid)
    changed = video.clone().flatten(1, 2)
    changed[:, masked] += 10
    after = model(changed.reshape_as(video), context=context, masked=masked, states=states, valid=valid)
    torch.testing.assert_close(before["latent_prediction"], after["latent_prediction"], atol=0, rtol=0)
    assert not torch.equal(before["state_prediction"], after["state_prediction"])
    other_states = model(video, context=context, masked=masked, states=states + 10, valid=valid)
    torch.testing.assert_close(before["state_prediction"], other_states["state_prediction"], atol=0, rtol=0)
    before["loss"].backward()
    assert states.grad is None and all(p.grad is None for p in model.target.parameters())
    assert any(p.grad is not None and torch.count_nonzero(p.grad) for p in model.online.parameters())
    with pytest.raises(ValueError, match="may not enter"):
        model(video, context=context, masked=context, states=states, valid=valid)


def test_kronecker_association_surgical_not_vector_overwrite():
    # k=e1, v=e1 targets one scalar association. Same-key v=e2 stays intact.
    state = torch.tensor([[2., 3.], [7., 11.]], dtype=torch.float64)
    k, v = torch.tensor([1., 0.], dtype=torch.float64), torch.tensor([1., 0.], dtype=torch.float64)
    actual = kronecker_update(state, k, v, torch.tensor(1.), torch.tensor(.5), torch.ones(2))
    torch.testing.assert_close(actual, torch.tensor([[.5, 3.], [7., 11.]], dtype=torch.float64))
    # Distinct key-axis forgetting must multiply columns, not value rows.
    decay = kronecker_update(state, k, v, torch.tensor(0.), torch.tensor(0.), torch.tensor([.2, .8]))
    torch.testing.assert_close(decay, state * torch.tensor([.2, .8]), atol=1e-7, rtol=1e-7)


def test_kronecker_oracle_random_initial_and_nonzero_gate_gradients():
    torch.manual_seed(6)
    model = TinyKronLSTM().double()
    inputs = torch.randn(1, 5, 12, dtype=torch.float64)
    _, _, audit = model(inputs)
    args = tuple(audit[name] for name in ("query", "key", "value", "beta", "write", "forget"))
    actual, state = recurrent_memory(*args)
    expected, expected_state = runner.vector_memory_oracle(*args)
    torch.testing.assert_close(actual, expected, atol=1e-12, rtol=1e-12)
    torch.testing.assert_close(state, expected_state, atol=1e-12, rtol=1e-12)
    actual.square().sum().backward()
    for gate in (model.erase, model.write, model.forget):
        assert gate.weight.grad.norm() > 0
    assert model.a_log.grad.norm() > 0


def test_kronlstm_prefix_and_chunk_state_equivalence():
    torch.manual_seed(9)
    model = TinyKronLSTM().double()
    _, _, audit = model(torch.randn(2, 6, 12, dtype=torch.float64))
    args = tuple(audit[name] for name in ("query", "key", "value", "beta", "write", "forget"))
    full_read, full_state = recurrent_memory(*args)
    left_read, left_state = recurrent_memory(*(a[:, :, :3] for a in args))
    right_read, right_state = recurrent_memory(*(a[:, :, 3:] for a in args), initial=left_state)
    torch.testing.assert_close(torch.cat((left_read, right_read), 2), full_read, atol=0, rtol=0)
    torch.testing.assert_close(right_state, full_state, atol=0, rtol=0)
    with pytest.raises(ValueError):
        recurrent_memory(*(a[:, :, :0] for a in args))
    with pytest.raises(ValueError):
        kronecker_update(torch.zeros(2, 2), torch.ones(2), torch.ones(2), torch.tensor(1.1), torch.tensor(.5), torch.ones(2))


@pytest.mark.parametrize("name", ["t_muon_diagnostic", "time_jepa_diagnostic", "kronlstm_diagnostic"])
def test_real_synthetic_component_diagnostics(name):
    result = getattr(runner, name)(42, "cpu")
    assert all(isinstance(value, (int, float, bool)) for value in result["metrics"].values())
    assert result["metrics"]["gradient_norm"] > 0
    assert result["metrics"]["parameter_update_norm"] > 0


def test_runner_immutable_sanitized_source_bound_contract(tmp_path):
    output = tmp_path / "result.json"
    command = [sys.executable, str(SCRIPT), "--methods", "kronlstm", "--seeds", "42", "--output", str(output)]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    result = json.loads(output.read_text())
    assert len(result["executed_source_sha256"]) == 4
    assert set(result["components"]) == {"kronlstm"}
    component = result["components"]["kronlstm"]
    assert component["dataset"]["id"] == "synthetic:oct20-kronlstm-v1"
    assert component["dataset"]["revision"] == "sha256:" + result["executed_source_sha256"]["scripts/run_oct20_foundation_components.py"]
    assert not result["promotion_eligible"] and not component["evolve_integrated"]
    assert component["full_experiment_status"] == "not_reproduced_high_cost"
    assert component["evaluation_tier"] == "l1_mechanism" and component["diagnostic_only"]
    original = output.read_bytes()
    again = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert again.returncode != 0 and output.read_bytes() == original


def test_runner_cuda_failure_has_no_cpu_fallback(tmp_path):
    if torch.cuda.is_available():
        pytest.skip("CPU-only failure boundary")
    output = tmp_path / "cuda.json"
    completed = subprocess.run([sys.executable, str(SCRIPT), "--device", "cuda", "--output", str(output)], cwd=ROOT, capture_output=True, text=True)
    assert completed.returncode != 0 and "no CPU fallback" in completed.stderr
    assert not output.exists()
