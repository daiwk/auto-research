from __future__ import annotations

import copy

import pytest

torch = pytest.importorskip("torch")

from auto_research.reproductions.smrc_pmrc import PMRC, SMRC, matrix_sign


def _parameter(shape=(3, 4), dtype=torch.float64):
    return torch.nn.Parameter(torch.zeros(shape, dtype=dtype))


@pytest.mark.parametrize("shape", [(3, 5), (5, 3)])
@pytest.mark.parametrize("optimizer_class", [SMRC, PMRC])
def test_exact_single_stage_update_and_orthogonal_residual(shape, optimizer_class):
    generator = torch.Generator().manual_seed(17)
    parameter = _parameter(shape)
    optimizer = optimizer_class([parameter], lr=0.2, beta=0.3, gamma=0.8,
                                rank=1, refresh_interval=None)
    expected = parameter.detach().clone()
    momentum = None
    basis = None
    for _ in range(3):
        gradient = torch.randn(shape, generator=generator, dtype=torch.float64)
        parameter.grad = gradient.clone()
        oriented = gradient.T if shape[0] > shape[1] else gradient
        if basis is None:
            basis = torch.linalg.svd(oriented, full_matrices=False).U[:, :1]
            momentum = torch.zeros((1, oriented.shape[1]), dtype=torch.float64)
        projected = basis.T @ oriented
        residual = oriented - basis @ projected
        assert torch.linalg.vector_norm(basis.T @ residual) < 1e-12
        momentum = 0.7 * momentum + 0.3 * projected
        low = matrix_sign(momentum) if optimizer_class is PMRC else momentum
        update = basis @ low + 0.8 * residual
        expected -= 0.2 * (update.T if shape[0] > shape[1] else update)
        optimizer.step()
        torch.testing.assert_close(parameter, expected, atol=1e-12, rtol=1e-12)
    assert optimizer.state[parameter]["momentum"].numel() == max(shape)
    assert not any(value.shape == parameter.shape for value in optimizer.state[parameter].values()
                   if isinstance(value, torch.Tensor))


@pytest.mark.parametrize("optimizer_class", [SMRC, PMRC])
def test_full_rank_reduces_to_dense_ema_or_muon(optimizer_class):
    parameter = _parameter()
    optimizer = optimizer_class([parameter], lr=0.1, beta=0.2, gamma=0.7,
                                rank=100, refresh_interval=None)
    expected = parameter.detach().clone()
    momentum = torch.zeros_like(expected)
    for index in range(4):
        gradient = torch.arange(12, dtype=torch.float64).reshape(3, 4) + index + 1
        parameter.grad = gradient
        momentum = 0.8 * momentum + 0.2 * gradient
        expected -= 0.1 * (matrix_sign(momentum) if optimizer_class is PMRC else momentum)
        optimizer.step()
        torch.testing.assert_close(parameter, expected, atol=1e-12, rtol=1e-12)


@pytest.mark.parametrize("optimizer_class", [SMRC, PMRC])
def test_refresh_boundary_uses_correct_parameter_correction_and_resets(optimizer_class):
    parameter = _parameter((2, 2))
    optimizer = optimizer_class([parameter], lr=0.1, beta=0.25, gamma=0.8,
                                rank=1, refresh_interval=2)
    first = torch.tensor([[4., 0.], [0., 1.]], dtype=torch.float64)
    second = torch.tensor([[0., 2.], [0., 3.]], dtype=torch.float64)
    basis = torch.tensor([[1.], [0.]], dtype=torch.float64)
    expected = parameter.detach().clone()
    momentum = torch.zeros((1, 2), dtype=torch.float64)
    for gradient in (first, second):
        projected = basis.T @ gradient
        momentum = 0.75 * momentum + 0.25 * projected
        low = matrix_sign(momentum) if optimizer_class is PMRC else momentum
        expected -= 0.1 * (basis @ low + 0.8 * (gradient - basis @ projected))
        parameter.grad = gradient
        optimizer.step()
    uncorrected = expected.clone()
    if optimizer_class is SMRC:
        expected -= 0.1 * 0.75 / 0.25 * (basis @ momentum)
        assert torch.linalg.vector_norm(expected - uncorrected) > 0.01
    torch.testing.assert_close(parameter, expected, atol=1e-12, rtol=1e-12)
    state = optimizer.state[parameter]
    assert state["refresh_pending"] and state["stage_steps"] == 0
    assert torch.count_nonzero(state["momentum"]) == 0
    # A fresh backward after correction supplies the next gradient. The new
    # dominant direction is e2; old-basis state must not be transported.
    parameter.grad = torch.tensor([[0., 0.], [0., 6.]], dtype=torch.float64)
    optimizer.step()
    assert state["stage"] == 2
    torch.testing.assert_close(state["basis"] @ state["basis"].T,
                               torch.diag(torch.tensor([0., 1.], dtype=torch.float64)))
    torch.testing.assert_close(state["momentum"].abs(),
                               torch.tensor([[0., 1.5]], dtype=torch.float64))


@pytest.mark.parametrize("optimizer_class", [SMRC, PMRC])
@pytest.mark.parametrize("boundary_checkpoint", [False, True])
def test_state_dict_resume_exactly_matches_uninterrupted(optimizer_class, boundary_checkpoint):
    generator = torch.Generator().manual_seed(23)
    gradients = [torch.randn((4, 5), generator=generator, dtype=torch.float64) for _ in range(7)]
    parameter = _parameter((4, 5))
    optimizer = optimizer_class([parameter], rank=2, refresh_interval=3)
    split = 3 if boundary_checkpoint else 2
    for grad in gradients[:split]:
        parameter.grad = grad
        optimizer.step()
    restored = torch.nn.Parameter(parameter.detach().clone())
    resumed = optimizer_class([restored], rank=1)
    resumed.load_state_dict(copy.deepcopy(optimizer.state_dict()))
    for grad in gradients[split:]:
        parameter.grad = grad
        restored.grad = grad.clone()
        optimizer.step()
        resumed.step()
        torch.testing.assert_close(parameter, restored, atol=0, rtol=0)
    assert resumed.state[restored]["stage"] == optimizer.state[parameter]["stage"]


@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16, torch.float32, torch.float64])
def test_low_precision_state_is_fp32_and_resume_does_not_round_it(dtype):
    parameter = _parameter((3, 4), dtype)
    optimizer = PMRC([parameter], rank=1, variant="practical", refresh_interval=3)
    parameter.grad = torch.arange(12, dtype=dtype).reshape(3, 4) / 13
    optimizer.step()
    saved = copy.deepcopy(optimizer.state_dict())
    resumed = PMRC([torch.nn.Parameter(parameter.detach().clone())], rank=1)
    resumed.load_state_dict(saved)
    target = resumed.param_groups[0]["params"][0]
    expected_dtype = torch.float64 if dtype == torch.float64 else torch.float32
    assert resumed.state[target]["basis"].dtype == expected_dtype
    torch.testing.assert_close(resumed.state[target]["momentum"],
                               optimizer.state[parameter]["momentum"], atol=0, rtol=0)


@pytest.mark.parametrize("optimizer_class", [SMRC, PMRC])
def test_zero_gradients_and_missing_gradients_are_finite_no_ops(optimizer_class):
    parameter = _parameter((5, 3))
    optimizer = optimizer_class([parameter], rank=2, refresh_interval=1)
    parameter.grad = torch.zeros_like(parameter)
    optimizer.step()
    assert torch.count_nonzero(parameter) == 0
    assert bool(torch.isfinite(optimizer.state[parameter]["basis"]).all())
    parameter.grad = None
    old_step = optimizer.state[parameter]["step"]
    optimizer.step()
    assert optimizer.state[parameter]["step"] == old_step
    assert torch.count_nonzero(matrix_sign(torch.zeros(3, 5))) == 0
    assert torch.count_nonzero(matrix_sign(torch.zeros(3, 5), method="newton_schulz")) == 0


def test_practical_cap_scaling_nesterov_and_decoupled_decay_match_equation():
    parameter = torch.nn.Parameter(torch.ones((2, 3), dtype=torch.float64))
    optimizer = PMRC([parameter], lr=0.1, beta=0.25, gamma=20, rank=1,
                     refresh_interval=None, variant="practical", residual_cap=0.3,
                     weight_decay=0.2, sign_method="svd")
    first = torch.tensor([[5., 0., 0.], [0., 0., 0.]], dtype=torch.float64)
    second = torch.tensor([[1., 2., 0.], [0., 8., 2.]], dtype=torch.float64)
    basis = torch.tensor([[1.], [0.]], dtype=torch.float64)
    expected = parameter.detach().clone()
    momentum = torch.zeros((1, 3), dtype=torch.float64)
    for gradient in (first, second):
        projected = basis.T @ gradient
        residual = gradient - basis @ projected
        momentum = 0.75 * momentum + 0.25 * projected
        update = basis @ matrix_sign(0.75 * momentum + 0.25 * projected)
        cap = min(20., float(0.3 * (update.square().sum() /
                                   residual.square().sum().clamp_min(1e-30)).sqrt()))
        expected = 0.98 * expected - (0.1 * 0.2 * 3 ** 0.5) * (update + cap * residual)
        parameter.grad = gradient
        optimizer.step()
        torch.testing.assert_close(parameter, expected, atol=1e-12, rtol=1e-12)
    assert optimizer.state[parameter]["last_residual_coefficient"] < 20


def test_warm_start_refresh_matches_row_normalized_qr_formula():
    parameter = _parameter((3, 4))
    optimizer = PMRC([parameter], rank=1, variant="practical", refresh_interval=1)
    first = torch.tensor([[6., 0., 0., 0.], [0., 2., 0., 0.], [0., 0., 1., 0.]],
                         dtype=torch.float64)
    parameter.grad = first
    optimizer.step()
    old = optimizer.state[parameter]["basis"].clone()
    second = torch.tensor([[1., 2., 0., 0.], [3., 1., 0., 0.], [1., 0., 2., 0.]],
                          dtype=torch.float64)
    row = old.T @ second
    expected = torch.linalg.qr(second @ (row / row.norm(dim=1, keepdim=True)).T,
                               mode="reduced").Q
    parameter.grad = second
    optimizer.step()
    actual = optimizer.state[parameter]["basis"]
    torch.testing.assert_close(actual @ actual.T, expected @ expected.T)


@pytest.mark.parametrize("optimizer_class", [SMRC, PMRC])
def test_non_matrix_and_explicit_embedding_head_groups_use_real_adamw(optimizer_class):
    bias = torch.nn.Parameter(torch.tensor([1., -1.], dtype=torch.float64))
    embedding = torch.nn.Parameter(torch.ones((5, 2), dtype=torch.float64))
    control = [torch.nn.Parameter(t.detach().clone()) for t in (bias, embedding)]
    optimizer = optimizer_class([{"params": [bias]},
                                 {"params": [embedding], "use_subspace": False}],
                                lr=0.01, weight_decay=0.05)
    reference = torch.optim.AdamW(control, lr=0.01, weight_decay=0.05)
    for index in range(3):
        for param, target in zip((bias, embedding), control, strict=True):
            param.grad = torch.full_like(param, 0.3 + index)
            target.grad = param.grad.clone()
        optimizer.step()
        reference.step()
        for param, target in zip((bias, embedding), control, strict=True):
            torch.testing.assert_close(param, target, atol=1e-12, rtol=1e-12)
    assert "basis" not in optimizer.state[embedding]


@pytest.mark.parametrize("projection", ["auto", "left", "right"])
@pytest.mark.parametrize("shape", [(2, 5), (5, 2)])
def test_rank_is_clamped_to_both_dimensions(projection, shape):
    parameter = _parameter(shape)
    optimizer = SMRC([parameter], rank=100, projection=projection)
    parameter.grad = torch.ones_like(parameter)
    optimizer.step()
    assert optimizer.state[parameter]["momentum"].shape[0] == 2


def test_nonfinite_gradients_fail_before_other_parameters_are_changed():
    first, second = _parameter(), _parameter()
    optimizer = SMRC([first, second])
    first.grad = torch.ones_like(first)
    second.grad = torch.full_like(second, float("nan"))
    with pytest.raises(ValueError, match="non-finite"):
        optimizer.step()
    assert torch.count_nonzero(first) == 0 and not optimizer.state


@pytest.mark.parametrize("kwargs", [{"rank": 0}, {"beta": 0}, {"gamma": 0},
                                   {"gamma": 1.1}, {"refresh_interval": 0},
                                   {"projection": "wrong"}, {"lr": float("nan")}])
def test_invalid_configuration_rejected(kwargs):
    with pytest.raises(ValueError):
        SMRC([_parameter()], **kwargs)


def test_real_autograd_parameters_change_and_loss_decreases():
    torch.manual_seed(9)
    model = torch.nn.Sequential(torch.nn.Linear(4, 8), torch.nn.Tanh(), torch.nn.Linear(8, 2))
    data = torch.randn(16, 4)
    target = data[:, :2]
    optimizer = SMRC(model.parameters(), lr=0.05, rank=2, beta=0.5, refresh_interval=5)
    initial = torch.nn.functional.mse_loss(model(data), target).item()
    for _ in range(25):
        optimizer.zero_grad()
        loss = torch.nn.functional.mse_loss(model(data), target)
        loss.backward()
        optimizer.step()
    assert torch.nn.functional.mse_loss(model(data), target).item() < initial


@pytest.mark.parametrize("zero_start", [False, True])
def test_subspace_basis_does_not_retain_full_svd_or_identity_storage(zero_start):
    parameter = _parameter((16, 32))
    optimizer = SMRC([parameter], rank=2)
    generator = torch.Generator().manual_seed(93)
    parameter.grad = torch.zeros_like(parameter) if zero_start else torch.randn(
        parameter.shape, dtype=parameter.dtype, generator=generator
    )
    optimizer.step()
    basis = optimizer.state[parameter]["basis"]
    assert basis.untyped_storage().nbytes() == basis.numel() * basis.element_size()
    assert basis.numel() == 32


@pytest.mark.parametrize("method", ["svd", "newton_schulz"])
def test_matrix_sign_handles_tiny_and_large_finite_scalings(method):
    normal = torch.tensor([[1., 0.], [0., 0.5]], dtype=torch.float32)
    expected = matrix_sign(normal, method=method)
    for scale in (1e-36, 1e36):
        actual = matrix_sign(normal * scale, method=method)
        assert bool(torch.isfinite(actual).all())
        torch.testing.assert_close(actual, expected, atol=2e-6, rtol=2e-6)


def test_bounded_end_to_end_diagnostic_records_actual_updates_and_negative_results():
    from auto_research.reproductions.smrc_pmrc.experiment import render, run_diagnostic
    previous = torch.get_num_threads()
    try:
        torch.set_num_threads(1)
        result = run_diagnostic(seed=42, steps=5)
    finally:
        torch.set_num_threads(previous)
    assert result["diagnostic_only"] and not result["evolve_eligible"]
    assert max(result["numeric_controls"].values()) < 1e-9
    assert len(result["low_precision_controls"]) == 4
    for row in result["low_precision_controls"].values():
        assert row["updates"] == 6 and row["parameter_changed"]
        assert row["state_dtype"] == "float32" and row["state_restore_exact"]
        assert row["state_resume_max_abs_error"] == 0
        assert row["max_abs_error_to_fp32"] <= row["comparison_atol"]
    assert result["full_experiment"]["status"] == "not_reproduced_high_cost"
    assert set(result["paper_quadratic"]) == set(result["small_mlp"]) == {
        "smrc", "pmrc", "pmrc_practical", "full_ema_sgd", "full_muon", "adamw"
    }
    assert all(row["updates"] == 5 for row in result["small_mlp"].values())
    assert all(row["initial_validation_mse"] != row["final_validation_mse"]
               for row in result["small_mlp"].values())
    assert "审查 DONE" in render(result)


@pytest.mark.parametrize("kwargs", [{"steps": 401}, {"max_seconds": 181}, {"device": "mps"}])
def test_diagnostic_does_not_allow_unbounded_expansion(kwargs):
    from auto_research.reproductions.smrc_pmrc.experiment import run_diagnostic
    with pytest.raises(ValueError):
        run_diagnostic(**kwargs)


@pytest.mark.parametrize("requested", ["cpu", "cuda", "cuda:1"])
def test_unified_adapter_forwards_requested_device_and_seed(monkeypatch, tmp_path, requested):
    from auto_research.reproductions.smrc_pmrc import experiment
    from auto_research.runtime import DEVICE_ENV
    monkeypatch.setenv(DEVICE_ENV, requested)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "device_count", lambda: 2)
    calls = []
    monkeypatch.setattr(experiment, "run_diagnostic", lambda **kwargs: calls.append(kwargs) or kwargs)
    assert experiment.reproduce(tmp_path, 43) == {"seed": 43, "device": requested}
    assert calls == [{"seed": 43, "device": requested}]


def test_unified_adapter_auto_on_mac_selects_cpu_not_mps(monkeypatch, tmp_path):
    from auto_research.reproductions.smrc_pmrc import experiment
    from auto_research.runtime import DEVICE_ENV
    monkeypatch.setenv(DEVICE_ENV, "auto")
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    monkeypatch.setattr(torch.backends.mps, "is_available", lambda: True)
    monkeypatch.setattr(experiment, "run_diagnostic", lambda **kwargs: kwargs)
    assert experiment.reproduce(tmp_path, 42)["device"] == "cpu"


def test_unified_adapter_does_not_fallback_when_cuda_is_unavailable(monkeypatch, tmp_path):
    from auto_research.reproductions.smrc_pmrc import experiment
    from auto_research.runtime import DEVICE_ENV
    monkeypatch.setenv(DEVICE_ENV, "cuda")
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    monkeypatch.setattr(experiment, "run_diagnostic", lambda **kwargs: pytest.fail("must not run"))
    with pytest.raises(RuntimeError, match="CUDA is unavailable"):
        experiment.reproduce(tmp_path, 42)


def test_unified_adapter_rejects_explicit_mps(monkeypatch, tmp_path):
    from auto_research.reproductions.smrc_pmrc import experiment
    from auto_research.runtime import DEVICE_ENV
    monkeypatch.setenv(DEVICE_ENV, "mps")
    with pytest.raises(ValueError, match="CPU/CUDA"):
        experiment.reproduce(tmp_path, 42)
