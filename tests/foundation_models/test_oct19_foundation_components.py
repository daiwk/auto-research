"""Independent scalar oracles, real updates and strict split/failure boundaries."""
from dataclasses import replace
import json
from pathlib import Path
import runpy
import sys

import pytest
import torch
from torch.nn import functional as F

from auto_research.foundation_models.fpot import (
    FPoTCodes, dequantize, integer_accumulate, quantize_weights, straight_through_weights,
)
from auto_research.foundation_models.lamp import (
    FeatureBatch, LampPredictor, Mixture, evaluate_test, resnet_regions, select_mixture, vit_regions,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def single_thread():
    previous = torch.get_num_threads()
    torch.set_num_threads(1)
    yield
    torch.set_num_threads(previous)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_real_scalar_reference_negative_controls_and_updates(seed):
    runner = runpy.run_path(str(ROOT / "scripts/run_oct19_foundation_components.py"))
    for function in ("fpot_diagnostic", "lamp_diagnostic"):
        result = runner[function](seed, "cpu")
        assert result["optimizer_steps"] == 1
        assert all(isinstance(value, (int, float)) and torch.isfinite(torch.tensor(value)) for value in result.values())


def test_fpot_zero_rows_reserved_code_and_arithmetic_signed_rounding():
    zero = quantize_weights(torch.zeros(2, 5, dtype=torch.float64))
    assert torch.equal(dequantize(zero), torch.zeros(2, 5, dtype=torch.float64))
    # m=2 recovers e=1 (odd), whereas treating m as the exponent is incorrect.
    codes = FPoTCodes(torch.tensor([[1, -1, 0]]), torch.tensor([[2, 2, 0]]), torch.ones(1), 4, 2, True)
    assert torch.equal(dequantize(codes), torch.tensor([[1.5, -1.5, 0.]]))
    assert integer_accumulate(torch.tensor([[3, -3, 999]], dtype=torch.int64), codes).item() == 9
    assert integer_accumulate(torch.tensor([[-3, 3, -999]], dtype=torch.int64), codes).item() == -9
    with pytest.raises(ValueError, match="overflow"):
        integer_accumulate(torch.full((1, 3), 2 ** 62, dtype=torch.int64), codes)


@pytest.mark.parametrize("kwargs", [{"bits": 1}, {"resolution": 0}, {"resolution": 3},
                                    {"phase_steps": 0}, {"clip_ratios": ()}, {"clip_ratios": (float("nan"),)}])
def test_fpot_invalid_calibration_configuration(kwargs):
    with pytest.raises(ValueError):
        quantize_weights(torch.randn(2, 3), **kwargs)


def test_fpot_invalid_values_codes_and_ste_shape():
    with pytest.raises(ValueError):
        quantize_weights(torch.tensor([[float("inf")]]))
    good = quantize_weights(torch.randn(2, 3))
    with pytest.raises(ValueError, match="zero-gating"):
        dequantize(replace(good, signs=torch.zeros_like(good.signs), magnitudes=torch.ones_like(good.magnitudes)))
    with pytest.raises(ValueError):
        straight_through_weights(torch.randn(2, 4), good)
    with pytest.raises(ValueError):
        integer_accumulate(torch.randn(2, 3), good)


def test_fpot_ste_forward_quantized_backward_identity():
    weights = torch.randn(3, 4, dtype=torch.float64, requires_grad=True)
    codes = quantize_weights(weights)
    output = straight_through_weights(weights, codes)
    assert torch.allclose(output, dequantize(codes), atol=1e-14)
    output.sum().backward()
    assert torch.equal(weights.grad, torch.ones_like(weights))


@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16])
def test_fpot_small_half_precision_weights_calibrate_in_float32_and_ste_casts_back(dtype):
    weights = torch.tensor([[1e-7, -2e-7], [0., 0.]], dtype=dtype, requires_grad=True)
    codes = quantize_weights(weights)
    reconstruction = dequantize(codes)
    assert codes.scales.dtype == reconstruction.dtype == torch.float32
    assert torch.isfinite(codes.scales).all() and (codes.scales > 0).all()
    assert torch.isfinite(reconstruction).all() and reconstruction[0].abs().min() > 0
    assert torch.equal(reconstruction[1], torch.zeros(2))
    float32_reference = quantize_weights(weights.detach().float())
    assert torch.equal(codes.magnitudes, float32_reference.magnitudes)
    assert torch.equal(codes.scales, float32_reference.scales)
    output = straight_through_weights(weights, codes)
    assert output.dtype == dtype and torch.equal(output, reconstruction.to(dtype))
    output.sum().backward()
    assert weights.grad.dtype == dtype and torch.equal(weights.grad, torch.ones_like(weights))


def fixture_model():
    torch.manual_seed(25)
    def features(prefix, n):
        return FeatureBatch(F.normalize(torch.randn(n, 6, dtype=torch.float64), dim=-1),
                            tuple(F.normalize(torch.randn(n, 4, width, dtype=torch.float64), dim=-1) for width in (5, 7, 9)),
                            tuple(f"{prefix}-{i}" for i in range(n)))
    support = features("support", 6)
    model = LampPredictor(support, torch.tensor([0, 0, 1, 1, 2, 2]), F.normalize(torch.randn(3, 6, dtype=torch.float64), dim=-1),
                          support_image_ids=("a", "a", "b", "b", "c", "c"))
    return model, features("validation", 4), features("test", 3)


def test_region_pooling_is_formula_exact_and_not_global_averaging():
    torch.manual_seed(4)
    tokens = torch.randn(2, 4, 4, 5, dtype=torch.float64)
    normalized = F.normalize(F.layer_norm(tokens, (5,)), dim=-1)
    expected = torch.stack([F.normalize(normalized[:, y:y + 2, x:x + 2].mean((1, 2)), dim=-1)
                            for y in (0, 2) for x in (0, 2)], 1)
    assert torch.allclose(vit_regions(tokens), expected, atol=1e-12)
    activation = torch.rand(2, 5, 4, 4, dtype=torch.float64)
    gem = torch.stack([F.normalize(activation[:, :, y:y + 2, x:x + 2].pow(3).mean((2, 3)).pow(1 / 3), dim=-1)
                       for y in (0, 2) for x in (0, 2)], 1)
    assert torch.allclose(resnet_regions(activation), gem, atol=1e-12)
    with pytest.raises(ValueError):
        resnet_regions(-activation)


def test_support_statistics_are_frozen_and_query_batch_invariant():
    model, _, query = fixture_model()
    original = tuple(t.clone() for t in model.support_means)
    first = replace(query, global_features=query.global_features[:1],
                    regional_features=tuple(t[:1] for t in query.regional_features), sample_ids=query.sample_ids[:1])
    for all_rows, one in zip(model.query_kernels(query), model.query_kernels(first), strict=True):
        assert torch.allclose(all_rows[:1], one, atol=1e-12)
    assert all(torch.equal(a, b) for a, b in zip(original, model.support_means, strict=True))
    permuted = replace(query, regional_features=tuple(t[:, [3, 1, 0, 2]] for t in query.regional_features))
    for a, b in zip(model.query_kernels(query), model.query_kernels(permuted), strict=True):
        assert torch.allclose(a, b, atol=1e-12)


def test_selection_uses_validation_only_and_test_cannot_mutate_selection():
    model, validation, test = fixture_model()
    candidates = (Mixture(0., (1., 0., 0.)), Mixture(1., (0., .5, .5)))
    labels = torch.tensor([0, 1, 2, 0])
    chosen, score = select_mixture(model, validation, labels, candidates)
    coefficients = chosen.coefficients()
    statistics = tuple(t.clone() for t in model.support_means)
    evaluate_test(model, test, torch.tensor([0, 1, 2]), chosen, validation_ids=validation.sample_ids)
    evaluate_test(model, test, torch.tensor([2, 0, 1]), chosen, validation_ids=validation.sample_ids)
    assert chosen.coefficients() == coefficients
    assert select_mixture(model, validation, labels, candidates) == (chosen, score)
    assert all(torch.equal(a, b) for a, b in zip(statistics, model.support_means, strict=True))
    with pytest.raises(ValueError, match="support/validation"):
        select_mixture(model, model.support, model.labels, candidates)
    with pytest.raises(ValueError, match="test identities"):
        evaluate_test(model, validation, labels, chosen, validation_ids=validation.sample_ids)


def test_prototype_objective_means_views_without_renormalization_and_encoder_frozen():
    model, _, query = fixture_model()
    prototype = model.text.clone().requires_grad_()
    means = torch.stack([model.support.global_features[i:i + 2].mean(0) for i in (0, 2, 4)])
    expected = F.cross_entropy(100 * means @ prototype.T, torch.tensor([0, 1, 2]))
    assert torch.allclose(model.prototype_loss(prototype), expected, atol=1e-10)
    query = replace(query, global_features=query.global_features.clone().requires_grad_(),
                    regional_features=tuple(t.clone().requires_grad_() for t in query.regional_features))
    mixture = Mixture(.5, (.2, .3, .5))
    cache = model.cache(query, mixture)
    with torch.no_grad():
        prototype.add_(.05 * torch.randn_like(prototype))
    assert torch.allclose(cache.predict(prototype), model.predict(query, mixture, prototype), atol=1e-12)
    cache.predict(prototype).square().mean().backward()
    assert prototype.grad.norm() > 0 and query.global_features.grad is None
    assert all(t.grad is None for t in query.regional_features)


@pytest.mark.parametrize("mixture", [Mixture(-1, (.2, .3, .5)), Mixture(.5, (0., 0., 0.)), Mixture(.5, (float("nan"), 0., 1.))])
def test_invalid_mixture_is_rejected(mixture):
    with pytest.raises(ValueError):
        mixture.coefficients()


def test_runner_schema_source_hashes_and_immutable_output(tmp_path, monkeypatch):
    runner = runpy.run_path(str(ROOT / "scripts/run_oct19_foundation_components.py"))
    path = tmp_path / "result.json"
    args = ["runner", "--papers", "fpot", "--seeds", "42", "--code-commit", "a" * 40, "--output", str(path)]
    monkeypatch.setattr(sys, "argv", args)
    assert runner["main"]() == 0
    payload = json.loads(path.read_text())
    assert payload["diagnostic_only"] and not payload["promotion_eligible"] and not payload["evolve_integrated"]
    assert payload["code_commit"] == "a" * 40
    assert len(payload["executed_source_sha256"]) == 2
    assert payload["components"]["fpot"]["per_seed"][0]["seed"] == 42
    assert payload["components"]["fpot"]["dataset"]["capability_benchmark"] is False
    original = path.read_bytes()
    with pytest.raises(SystemExit):
        runner["main"]()
    assert path.read_bytes() == original
    monkeypatch.setattr(sys, "argv", args[:-1] + [str(tmp_path / "invalid.json"), "--seeds", "42,42"])
    with pytest.raises(SystemExit):
        runner["main"]()
