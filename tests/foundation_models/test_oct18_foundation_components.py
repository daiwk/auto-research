"""Actual differentiable mechanisms, independent formulas and failure boundaries."""
import json
from pathlib import Path
import runpy
import sys

import pytest
import torch

from auto_research.foundation_models.adaloop_vision import (
    QuestionConditionedVisionLoop, depth_supervised_loss, stability_stop, visual_prefix,
)
from auto_research.foundation_models.memory_mosaics_plus import MemoryMosaicsPlus, masked_average
from auto_research.foundation_models.mjev_spatial import (
    NativeSpatialReadout, crop_original, decode_count, encode_count, length_codebook, refine_region,
)
from auto_research.foundation_models.rr_vlm import RetrofittedRecurrentVLM, recovery_loss
from auto_research.foundation_models.softcache import SoftCacheSampler, cached_step, residual_extrapolation

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def one_thread():
    previous = torch.get_num_threads()
    torch.set_num_threads(1)
    yield
    torch.set_num_threads(previous)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_all_real_operator_diagnostics(seed):
    runner = runpy.run_path(str(ROOT / "scripts/run_oct18_foundation_components.py"))
    for name in ("mosaics_diagnostic", "spatial_diagnostic", "adaloop_diagnostic", "rr_diagnostic", "softcache_diagnostic"):
        result = runner[name](seed, "cpu")
        assert result["optimizer_steps"] >= 1
        assert all(isinstance(value, (int, float)) and torch.isfinite(torch.tensor(value)) for value in result.values())


def test_empty_memory_has_zero_output_and_finite_zero_gradients():
    logits = torch.randn(1, 2, 3, 3, dtype=torch.float64, requires_grad=True)
    values = torch.randn(1, 2, 3, 4, dtype=torch.float64, requires_grad=True)
    result = masked_average(logits, values, torch.zeros_like(logits, dtype=torch.bool))
    assert torch.equal(result, torch.zeros_like(result))
    result.sum().backward()
    assert torch.isfinite(logits.grad).all() and not torch.count_nonzero(logits.grad)
    assert torch.isfinite(values.grad).all() and not torch.count_nonzero(values.grad)


@pytest.mark.parametrize("starts", [[0, 0, 1, 1], [0, 1, 0, 0], [0, 0, 5, 5]])
def test_memory_rejects_non_document_causal_boundaries(starts):
    model = MemoryMosaicsPlus()
    with pytest.raises(ValueError):
        model(torch.randn(1, 4, 16), torch.tensor([starts]))


def test_memory_output_is_invariant_to_future_tokens_beyond_every_query():
    torch.manual_seed(11)
    model = MemoryMosaicsPlus(skip=2).double()
    x = torch.randn(1, 6, 16, dtype=torch.float64)
    starts = torch.tensor([[0, 0, 2, 2, 4, 4]])
    output = model(x, starts)
    for time in range(5):
        changed = x.clone()
        changed[:, time + 1:] *= -37
        assert torch.allclose(model(changed, starts)[:, time], output[:, time], atol=1e-12)


def test_spatial_native_readout_has_no_classifier_head_and_validates_end_positions():
    model = NativeSpatialReadout()
    assert all("classifier" not in name and "output" not in name for name, _ in model.named_parameters())
    hidden = torch.randn(2, 7, 16)
    with pytest.raises(ValueError):
        model(hidden, torch.tensor([6, 6]), torch.tensor([[2, 6], [3, 4]]))
    with pytest.raises(ValueError):
        NativeSpatialReadout(query_heads=3, key_heads=2)


def test_spatial_injected_final_layer_parameters_are_shared_not_copied():
    source = torch.nn.ModuleDict({"norm": torch.nn.RMSNorm(16, eps=1e-6),
                                  "query": torch.nn.Linear(16, 16, bias=False),
                                  "key": torch.nn.Linear(16, 8, bias=False)})
    scorer = NativeSpatialReadout(input_norm=source["norm"], query_projection=source["query"],
                                 key_projection=source["key"])
    assert scorer.norm is source["norm"]
    assert scorer.query is source["query"] and scorer.key is source["key"]
    assert scorer.query.weight is source["query"].weight
    previous = source["query"].weight.detach().clone()
    scores = scorer(torch.randn(1, 8, 16), torch.tensor([7]), torch.tensor([[2, 5]]))
    (-scores.log_softmax(-1)[0, 0]).backward()
    torch.optim.SGD(scorer.parameters(), lr=.01).step()
    assert (source["query"].weight - previous).norm() > 0


def test_all_count_classes_and_length_precision_contract():
    for value in range(1024):
        assert decode_count(*encode_count(value)) == value
    edges, cells = length_codebook()
    assert cells == (4,) * 6 + (8,) * 24
    for left, right, number in zip(edges[:-1], edges[1:], cells, strict=True):
        assert (right - left) / (2 * number) <= max(.01, .05 * left) + 1e-12
    for invalid in (-1, 1024, 2.5, True):
        with pytest.raises(ValueError):
            encode_count(invalid)


def test_three_level_region_prediction_uses_original_pixel_coordinates():
    bounds = (0., 0., 1., 1.)
    for choice in (1, 8, 3):
        bounds = refine_region(bounds, choice)
    assert abs(bounds[2] - bounds[0] - 1 / 27) < 1e-12
    assert abs(bounds[3] - bounds[1] - 1 / 27) < 1e-12
    image = torch.arange(3 * 81 * 81, dtype=torch.float64).reshape(3, 81, 81)
    assert crop_original(image, bounds).shape == (3, 8, 8)
    with pytest.raises(ValueError):
        crop_original(image, (-.1, 0, 1, 1))


def test_visual_prefixes_preserve_interfaces_and_detach_drafts_not_vision():
    states = tuple(torch.randn(2, 3, 8, requires_grad=True) for _ in range(3))
    question = torch.randn(2, 2, 8)
    drafts = tuple(torch.randn(2, 1, 8, requires_grad=True) for _ in range(2))
    result = visual_prefix(states, question, "C", drafts, torch.zeros(2, 1, 8))
    assert result.shape == (2, 19, 8)
    result.sum().backward()
    assert all(state.grad is not None for state in states)
    assert all(draft.grad is None for draft in drafts)
    with pytest.raises(ValueError):
        visual_prefix(states, question, "C", ())


def test_adaloop_depth_loss_and_halting_reject_bad_contracts():
    assert stability_stop(["a", "a", "b"], 3) == 2
    assert stability_stop(["a", "b", "c"], 2) == 2
    with pytest.raises(ValueError):
        depth_supervised_loss((torch.randn(2, 3),), torch.tensor([0, 1]), torch.tensor([2.]))
    with pytest.raises(ValueError):
        QuestionConditionedVisionLoop(width=7, heads=2)


def test_question_condition_detaches_input_embeddings_but_trains_pooler():
    model = QuestionConditionedVisionLoop().double()
    question = torch.randn(2, 4, 16, dtype=torch.float64, requires_grad=True)
    model.condition(question).square().mean().backward()
    assert question.grad is None
    assert model.question_query.grad is not None and model.question_query.grad.norm() > 0


def test_retrofit_shares_core_not_clones_per_iteration_and_stage_gates_are_exact():
    model = RetrofittedRecurrentVLM()
    calls = []
    hook = model.core[0].register_forward_hook(lambda *args: calls.append(1))
    model(torch.tensor([[1, 2]]), torch.randn(1, 1, 16), iterations=4)
    hook.remove()
    assert len(calls) == 4
    assert len(model.prelude) + len(model.core) + len(model.coda) == 4
    for stage in (0, 1, 2):
        model.configure_stage(stage)
        assert not any(p.requires_grad for name, p in model.named_parameters() if name.startswith("teacher_"))
        assert all(p.requires_grad == (stage != 0) for p in model.projector.parameters())
        assert all(p.requires_grad == (stage != 1) for p in model.adapter.parameters())
    with pytest.raises(ValueError):
        model.configure_stage(3)
    with pytest.raises(ValueError):
        RetrofittedRecurrentVLM(prune_start=1, prelude=2, core=1, coda=1)


def test_distillation_teacher_is_detached_and_independent_reference_matches():
    student = torch.randn(2, 3, 5, dtype=torch.float64, requires_grad=True)
    teacher = torch.randn_like(student, requires_grad=True)
    labels = torch.randint(5, (2, 3))
    actual = recovery_loss(student, teacher, labels, temperature=2, weight=.3)
    p = (teacher.detach() / 2).softmax(-1)
    reference = (.7 * torch.nn.functional.cross_entropy(student.flatten(0, 1), labels.flatten())
                 + .3 * 4 * (p * (p.log() - (student / 2).log_softmax(-1))).sum(-1).mean())
    assert torch.allclose(actual, reference)
    actual.backward()
    assert student.grad.norm() > 0 and teacher.grad is None
    with pytest.raises(ValueError):
        recovery_loss(student, teacher, labels, temperature=float("nan"))


def test_softcache_guards_headroom_and_real_time_extrapolation():
    assert cached_step(.05, .1, 0, 1, 3, 0) == .1
    assert cached_step(.2, .1, .1, 1, 3, .19) == .1
    assert abs(cached_step(.2, .1, .5, 1, 3, .1) - .2) < 1e-12
    assert abs(cached_step(.95, .1, 0, 1, 3, .1) - .05) < 1e-12
    assert torch.equal(residual_extrapolation(torch.tensor([2.]), torch.tensor([1.]), .7, .4, .1, 1.), torch.tensor([3.]))
    with pytest.raises(ValueError):
        cached_step(.2, .1, -.1, 1, 3, 0)


def test_softcache_no_cross_sample_cache_and_never_steps_past_endpoint():
    sampler = SoftCacheSampler(threshold=100)
    calls = []
    def residual(x, t):
        calls.append(t)
        return torch.ones_like(x)
    result, trace = sampler.sample(torch.zeros(1), [0., .05, .2, .9, 1.], residual,
                                   lambda x, r, t: r, lambda x, t: torch.ones_like(x))
    assert torch.allclose(result, torch.ones(1))
    assert all(row.time + row.step <= 1 + 1e-12 for row in trace)
    assert trace[0].fresh and calls == [0.]
    sampler.sample(torch.ones(1), [0., 1.], residual, lambda x, r, t: r, lambda x, t: x)
    assert calls == [0., 0.]
    with pytest.raises(ValueError):
        sampler.sample(torch.zeros(1), [0., .5, .5, 1.], residual, lambda x, r, t: r, lambda x, t: x)


def test_runner_schema_commit_source_hashes_and_immutable_outputs(tmp_path, monkeypatch):
    runner = runpy.run_path(str(ROOT / "scripts/run_oct18_foundation_components.py"))
    output = tmp_path / "components.json"
    args = ["runner", "--papers", "softcache", "--seeds", "42", "--code-commit", "a" * 40, "--output", str(output)]
    monkeypatch.setattr(sys, "argv", args)
    assert runner["main"]() == 0
    measured = json.loads(output.read_text())
    assert measured["code_commit"] == "a" * 40
    assert measured["diagnostic_only"] and not measured["promotion_eligible"]
    assert len(measured["executed_source_sha256"]) == 2
    component = measured["components"]["softcache"]
    assert component["per_seed"][0]["seed"] == 42
    assert component["dataset"]["capability_benchmark"] is False
    previous = output.read_bytes()
    with pytest.raises(SystemExit):
        runner["main"]()
    assert previous == output.read_bytes()
    monkeypatch.setattr(sys, "argv", args[:-1] + [str(tmp_path / "invalid.json")] + ["--seeds", "42,42"])
    with pytest.raises(SystemExit):
        runner["main"]()
