"""Independent linear algebra/gradient references, not an LLM benchmark."""
import hashlib
import json
import math
from pathlib import Path

import pytest
import torch
from torch.nn import functional as F

from auto_research.foundation_models.ttr_compressor import TTRCompressor, diagnostic, ttr_compress


def primal_reference(tokens, a, rho, floor=0.):
    keys = tokens / tokens.norm(dim=-1, keepdim=True)
    targets = tokens @ a
    matrix = keys.transpose(-1, -2) @ keys + torch.diag(F.softplus(rho) + floor)
    rhs = keys.transpose(-1, -2) @ targets.unsqueeze(-1)
    return torch.linalg.solve(matrix, rhs).squeeze(-1)


@pytest.mark.parametrize("shape", [(4, 9), (2, 4, 9), (2, 3, 7, 4)])
def test_dual_matches_independent_primal(shape):
    generator = torch.Generator().manual_seed(123)
    x = torch.randn(shape, dtype=torch.float64, generator=generator)
    a = torch.randn(shape[-1], dtype=torch.float64, generator=generator)
    rho = torch.linspace(-3., 2., shape[-1], dtype=torch.float64)
    for floor in (0., .01):
        actual = ttr_compress(x, a, rho, ridge_floor=floor)
        torch.testing.assert_close(actual, primal_reference(x, a, rho, floor), atol=1e-12, rtol=1e-12)
        # Check the normal equations, not just the two implementations' output.
        key = x / x.norm(dim=-1, keepdim=True)
        residual = (key.transpose(-1, -2) @ key + torch.diag(F.softplus(rho) + floor)) @ actual.unsqueeze(-1)
        torch.testing.assert_close(residual.squeeze(-1), (key.transpose(-1, -2) @ (x @ a).unsqueeze(-1)).squeeze(-1))


def test_outer_gradients_match_eq9_and_gradcheck():
    generator = torch.Generator().manual_seed(4)
    x = torch.randn(2, 3, 5, dtype=torch.float64, generator=generator).requires_grad_()
    a = torch.randn(5, dtype=torch.float64, generator=generator).requires_grad_()
    rho = torch.linspace(-1., 1., 5, dtype=torch.float64).requires_grad_()
    assert torch.autograd.gradcheck(ttr_compress, (x, a, rho), eps=1e-6, atol=1e-5, rtol=1e-4)
    summary = ttr_compress(x, a, rho)
    upstream = torch.randn(2, 5, dtype=torch.float64, generator=generator)
    ga, gr = torch.autograd.grad((summary * upstream).sum(), (a, rho))
    key = x.detach() / x.detach().norm(dim=-1, keepdim=True)
    matrix = key.transpose(-1, -2) @ key + torch.diag(F.softplus(rho.detach()))
    adjoint = torch.linalg.solve(matrix, upstream.unsqueeze(-1)).squeeze(-1)
    expected_a = (x.detach().transpose(-1, -2) @ (key @ adjoint.unsqueeze(-1))).squeeze(-1).sum(0)
    expected_rho = (-rho.detach().sigmoid() * summary.detach() * adjoint).sum(0)
    torch.testing.assert_close(ga, expected_a, atol=1e-12, rtol=1e-12)
    torch.testing.assert_close(gr, expected_rho, atol=1e-12, rtol=1e-12)


def test_asymmetric_normalization_and_magnitude_negative_controls():
    x = torch.tensor([[2., 0.], [0., 3.], [1., 1.]], dtype=torch.float64)
    a = torch.tensor([1., 2.], dtype=torch.float64)
    rho = torch.tensor([-2., -.7], dtype=torch.float64)
    result = ttr_compress(x, a, rho)
    torch.testing.assert_close(ttr_compress(3 * x, a, rho), 3 * result)
    keys = x / x.norm(dim=-1, keepdim=True)
    matrix = keys.T @ keys + torch.diag(F.softplus(rho))
    both_normalized = torch.linalg.solve(matrix, keys.T @ (keys @ a))
    assert not torch.allclose(result, both_normalized)
    # Raw keys plus raw targets give a different ridge problem, not TTR.
    raw_keys = torch.linalg.solve(x.T @ x + torch.diag(F.softplus(rho)), x.T @ (x @ a))
    assert not torch.allclose(result, raw_keys)
    torch.testing.assert_close(ttr_compress(x[[2, 0, 1]], a, rho), result)


def test_redundant_group_saturation_and_nonadditivity():
    ridge_one = torch.full((2,), math.log(math.expm1(1.)), dtype=torch.float64)
    a = torch.ones(2, dtype=torch.float64)
    for count in (1, 2, 8):
        x = torch.tensor([[1., 0.]] * count + [[0., 1.]], dtype=torch.float64)
        actual = ttr_compress(x, a, ridge_one)
        torch.testing.assert_close(actual, torch.tensor([count / (count + 1), .5], dtype=torch.float64))
        assert actual[0] / actual[1] < count or count == 1
    # A mean/attention-pool replacement does not implement the ridge solution.
    x = torch.tensor([[1., 0.]] * 8 + [[0., 1.]], dtype=torch.float64)
    assert not torch.allclose(ttr_compress(x, a, ridge_one), x.mean(0))


def test_module_has_only_2d_parameters_and_actual_outer_update():
    torch.manual_seed(7)
    module = TTRCompressor(6, initial_ridge=.2, ridge_floor=.01).double()
    assert sum(parameter.numel() for parameter in module.parameters()) == 12
    torch.testing.assert_close(F.softplus(module.ridge_logits) + module.ridge_floor,
                               torch.full((6,), .2, dtype=torch.float64), atol=1e-8, rtol=1e-8)
    x = torch.randn(2, 4, 6, dtype=torch.float64)
    torch.testing.assert_close(module(x), ttr_compress(x, module.target_vector, module.ridge_logits, ridge_floor=.01))
    old = [p.detach().clone() for p in module.parameters()]
    optimizer = torch.optim.SGD(module.parameters(), lr=.001)
    optimizer.zero_grad()
    module(x).square().mean().backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() and p.grad.norm() > 0 for p in module.parameters())
    optimizer.step()
    assert all(not torch.equal(before, after) for before, after in zip(old, module.parameters(), strict=True))


@pytest.mark.parametrize("invalid", ["zero", "nan", "inf", "integer", "half", "empty", "mismatch", "rho_underflow", "overflow"])
def test_invalid_numerics_fail_without_silent_fallback(invalid):
    x, a, rho = torch.ones(3, 4), torch.ones(4), torch.zeros(4)
    if invalid == "zero":
        x[0].zero_()
    elif invalid == "nan":
        x[0, 0] = float("nan")
    elif invalid == "inf":
        rho[0] = float("inf")
    elif invalid == "integer":
        x = x.long()
    elif invalid == "half":
        x, a, rho = x.half(), a.half(), rho.half()
    elif invalid == "empty":
        x = x[:0]
    elif invalid == "mismatch":
        a = a[:3]
    elif invalid == "rho_underflow":
        rho.fill_(-1000)
    elif invalid == "overflow":
        x.fill_(1e30)
    with pytest.raises(ValueError):
        ttr_compress(x, a, rho)


def test_cost_initialization_and_floor_rejections():
    with pytest.raises(ValueError, match="cost gate"):
        ttr_compress(torch.ones(129, 3), torch.ones(3), torch.zeros(3))
    for floor in (-1., float("inf"), float("nan")):
        with pytest.raises(ValueError):
            ttr_compress(torch.ones(2, 3), torch.ones(3), torch.zeros(3), ridge_floor=floor)
    for options in ({"dimension": 0}, {"dimension": 2, "initial_ridge": 0.}, {"dimension": 2, "ridge_floor": .2}):
        with pytest.raises(ValueError):
            TTRCompressor(**options)
    with pytest.raises(ValueError):
        diagnostic(42, "mps")


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic_defining_contracts(seed):
    result = diagnostic(seed)
    assert result["seed"] == seed and all(result["checks"].values())
    assert all(type(value) in (int, float, bool) and math.isfinite(value) for value in result["metrics"].values())


def test_documented_metadata_and_original_figure():
    root = Path(__file__).resolve().parents[1]
    spec = json.loads((root / "src/auto_research/paper_specs/catalog/foundation-models/ttr-compressor.json").read_text())
    assert spec["published_at"] == "2026-10-22T17:14:38Z"
    assert spec["first_author_affiliation"] == "The Chinese University of Hong Kong"
    assert spec["adapter"] is None and spec["diagnostic_only"]
    assert not spec["promotion_eligible"] and not spec["evolve_integrated"]
    assert spec["requires_gpu_validation"] and spec["gpu_validation_artifact"] == "docs/gpu-validations/ttr-compressor-a100-20261024.json"
    assert spec["full_experiment_status"] == "not_reproduced_high_cost"
    assert spec["automatic_retry"] is False and spec["automatic_implementation_queue"] is False
    readme = root / "docs" / spec["detail_path"]
    text = readme.read_text()
    for marker in ("论文信息", "论文链接", "公司 / 机构 / 学校", "首次公开日期", "原作者代码", "本地 adapter / 稳定键", "本地复现代码目录", "未找到", "核心公式", "未报告生产线上 A/B", "成本过高，不复现（审查 DONE）"):
        assert marker in text
    provenance = json.loads((readme.parent / "assets/provenance.json").read_text())
    assert provenance["visually_verified"]
    assert hashlib.sha256((readme.parent / "assets" / provenance["image"]).read_bytes()).hexdigest() == provenance["image_sha256"]
