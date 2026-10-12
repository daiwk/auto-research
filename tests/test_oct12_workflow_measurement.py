"""Injected fixture checks only; these tests are not real workflow measurements."""

import ast
from dataclasses import asdict, fields, replace
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from auto_research.agent_research.oct12_memory_tools import WorkflowOutcome, audit_workflows


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_oct12_workflow_measurement.py"
spec = importlib.util.spec_from_file_location("oct12_workflow_measurement", SCRIPT)
runner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


class FixtureBackend:
    """No model execution; intentionally cannot produce a real-measurement label."""

    device = "fixture"
    provenance = {"source": "injected unit fixture, not a public checkpoint"}
    verified = False

    def __init__(self):
        self.calls = []
        self.frozen_checks = 0
        self.synchronizations = 0

    def assert_frozen(self):
        self.frozen_checks += 1

    def synchronize(self):
        self.synchronizations += 1

    def generate(self, prompt, *, seed, max_new_tokens):
        self.calls.append((prompt, seed, max_new_tokens))
        # IDs include an EOS-like last token; decoded text length is not the cost.
        ids = (17, 0) if max_new_tokens == 64 else (17, 21, 22, 0)
        return runner.Generation("```python\nprint('unit fixture only')\n```", ids, 91, seed)


class FixtureSandbox:
    """Never executes source on the host; returns a labeled unit fixture response."""

    def __init__(self, response=("not json", "", 0)):
        self.response = response
        self.programs = []

    def execute(self, source):
        self.programs.append(source)
        return self.response


def fixture_clock(executions):
    ticks = iter(value for index in range(executions)
                 for value in (index * 2.0, index * 2.0 + 0.125, index * 2.0 + 0.5))
    return lambda: next(ticks)


def fixture_measurement(seeds=(42, 43, 44)):
    backend, sandbox = FixtureBackend(), FixtureSandbox()
    outcomes, metadata = runner.measure_pairs(
        backend, sandbox, seeds=seeds, clock=fixture_clock(len(seeds) * 2))
    return backend, sandbox, outcomes, metadata


def test_paired_same_task_seed_order_timing_and_exact_token_cost():
    backend, sandbox, outcomes, metadata = fixture_measurement()
    assert [(row.run_id, row.configuration) for row in outcomes] == [
        (42, "budget-64"), (42, "budget-256"),
        (43, "budget-256"), (43, "budget-64"),
        (44, "budget-64"), (44, "budget-256")]
    assert all(row.task_id == "public-circle-packing-26" for row in outcomes)
    assert all(row.decision_seconds == 0.125 and row.task_seconds == 0.5 for row in outcomes)
    assert [row.inference_cost for row in outcomes] == [2, 4, 4, 2, 2, 4]
    assert backend.synchronizations == 12 and backend.frozen_checks == 12
    assert sandbox.programs == ["print('unit fixture only')"] * 6
    assert metadata["audit"]["paired_executions"] == 3
    assert metadata["traces"][2]["execution_order"] == [256, 64]
    assert all(trace["prompt_tokens"] == 91 for trace in metadata["traces"])
    assert metadata["traces"][0]["generated_token_ids_sha256"] == hashlib.sha256(
        json.dumps((17, 0)).encode()).hexdigest()
    assert all(trace["generated_tokens"] == len(trace["generated_token_ids"])
               for trace in metadata["traces"])
    assert metadata["timing_source"] == "injected_fixture_clock"


def test_zero_success_denominators_and_not_applicable_failure_modes():
    _, _, outcomes, metadata = fixture_measurement()
    assert all(not row.success for row in outcomes)
    for metric in metadata["audit"]["configurations"].values():
        assert metric["successes"] == 0
        assert metric["cost_per_success"] is None
        assert metric["time_per_success"] is None
        assert metric["failure_cost_share"] == 1.0
    assert metadata["cost_unit"] == "generated_token_units"
    assert metadata["billing_currency"] is None
    assert not metadata["real_model_execution"]
    assert metadata["measurement_kind"] == "injected_fixture_timing_schema_diagnostic"
    assert metadata["diagnostic_only"] and not metadata["capability_comparison"]
    assert not metadata["evolve_promotion_eligible"]
    assert "not Jev model reproduction" in metadata["model_claim"]
    assert all(value.startswith("not_applicable:") for value in
               metadata["behavior_annotation_applicability"].values())
    assert all(not row.failed_recovery and not row.premature_completion for row in outcomes)


def test_gold_and_solved_program_never_enter_generation_or_host_execution():
    backend, sandbox, _, _ = fixture_measurement(seeds=(42,))
    assert [prompt for prompt, _, _ in backend.calls] == [runner.CIRCLE_TASK] * 2
    assert "centers =" not in runner.CIRCLE_TASK
    assert sandbox.programs == ["print('unit fixture only')"] * 2
    source = SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "CIRCLE_INITIAL" not in source
    assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                   and node.func.id in {"exec", "eval", "compile"}
                   for node in ast.walk(tree))
    assert not any(isinstance(node, (ast.Import, ast.ImportFrom)) and
                   (getattr(node, "module", "") or "").startswith("subprocess")
                   for node in ast.walk(tree))


@pytest.mark.parametrize("budgets", [(64,), (64, 128, 256), (64, 64), (0, 256),
                                     (64, -1), (True, 256), (64.0, 256)])
def test_only_two_distinct_positive_integer_configurations(budgets):
    backend = FixtureBackend()
    with pytest.raises(ValueError, match="exactly two"):
        runner.measure_pairs(backend, FixtureSandbox(), budgets=budgets)
    assert backend.calls == []


@pytest.mark.parametrize("seeds", [(), (42, 42), (-1,), (2**32,), (True,), (42.0,)])
def test_seeds_are_explicit_unique_and_reproducible(seeds):
    with pytest.raises(ValueError, match="unique integer seeds"):
        runner.validate_design(seeds, (64, 256))


def test_strict_outcome_jsonl_is_aggregator_compatible_and_output_is_fresh(tmp_path):
    _, _, outcomes, metadata = fixture_measurement(seeds=(42,))
    output = tmp_path / "fresh"
    written = runner.write_results(output, outcomes, metadata)
    raw = (output / "pairs.jsonl").read_bytes()
    rows = [json.loads(line) for line in raw.splitlines()]
    assert all(set(row) == {field.name for field in fields(WorkflowOutcome)} for row in rows)
    assert rows == [asdict(row) for row in outcomes]
    reloaded = [WorkflowOutcome(**row) for row in rows]
    assert audit_workflows(reloaded) == metadata["audit"]
    assert written["files"]["pairs.jsonl"] == hashlib.sha256(raw).hexdigest()
    assert json.loads((output / "measurement.json").read_text()) == written
    with pytest.raises(FileExistsError, match="fresh output"):
        runner.write_results(output, outcomes, metadata)
    assert (output / "pairs.jsonl").read_bytes() == raw


def test_generated_pair_file_runs_existing_jev_aggregator_without_model_claim(tmp_path):
    from auto_research.agent_research.oct12_entrypoint import run_method

    _, _, outcomes, metadata = fixture_measurement(seeds=(42,))
    output = tmp_path / "unit-fixture-only"
    runner.write_results(output, outcomes, metadata)
    aggregate = run_method("jev-workflow", dataset=output / "pairs.jsonl")
    assert aggregate["configurations"] == metadata["audit"]["configurations"]
    assert aggregate["paired_executions"] == 1
    assert aggregate["diagnostic_only"] and not aggregate["capability_comparison"]
    assert not aggregate["evolve_promotion_eligible"]
    assert "not automatically Jev" in aggregate["model_claim"]


def test_bad_pairs_or_invalid_timing_are_rejected_before_any_artifact(tmp_path):
    _, _, outcomes, metadata = fixture_measurement(seeds=(42,))
    for index, invalid in enumerate([
            outcomes[:1], [outcomes[0], replace(outcomes[1], run_id=43)],
            [replace(outcomes[0], decision_seconds=float("nan")), outcomes[1]],
            [replace(outcomes[0], task_seconds=0.0), outcomes[1]],
    ]):
        output = tmp_path / str(index)
        with pytest.raises(ValueError):
            runner.write_results(output, invalid, metadata)
        assert not output.exists()


@pytest.mark.parametrize("response", [("", "bwrap: unshare failed", 1),
                                      ("", "Operation not permitted", 1)])
def test_sandbox_infrastructure_failure_aborts_instead_of_recording_candidate_failure(response):
    with pytest.raises(RuntimeError, match="sandbox setup failed"):
        runner.measure_pairs(FixtureBackend(), FixtureSandbox(response), seeds=(42,),
                             clock=fixture_clock(2))


def test_external_geometry_and_execution_failures_are_not_fake_success():
    assert runner.evaluate_generated_program(FixtureSandbox(("", "timeout", 124)), "source") == (
        False, None, "execution failed (124): timeout", 124)
    overlapping = {"centers": [[0.5, 0.5]] * 26, "radii": [0.1] * 26}
    success, score, _, _ = runner.evaluate_generated_program(
        FixtureSandbox((json.dumps(overlapping), "", 0)), "unit fixture source")
    assert not success and score is None
    # A zero-score feasible fixture is not an optimization-capability claim.
    feasible = {"centers": [[0.5, 0.5]] * 26, "radii": [0.0] * 26}
    success, score, _, _ = runner.evaluate_generated_program(
        FixtureSandbox((json.dumps(feasible), "", 0)), "unit fixture source")
    assert success and score == 0.0


@pytest.mark.parametrize("change", [lambda row: replace(row, seed=43),
                                   lambda row: replace(row, token_ids=tuple(range(65))),
                                   lambda row: replace(row, token_ids=(True,)),
                                   lambda row: replace(row, token_ids=(-1,)),
                                   lambda row: replace(row, prompt_tokens=0)])
def test_injected_backend_must_report_actual_requested_seed_and_token_ids(change):
    backend = FixtureBackend()
    original = backend.generate
    backend.generate = lambda *args, **kwargs: change(original(*args, **kwargs))
    with pytest.raises(ValueError):
        runner.measure_pairs(backend, FixtureSandbox(), seeds=(42,), clock=fixture_clock(2))


class FixtureTokenizer:
    """Minimal tensor tokenizer used only to exercise real torch RNG code."""

    chat_template = "unit fixture template"
    eos_token_id = 0
    pad_token_id = 0

    def __init__(self):
        self.messages = []

    def apply_chat_template(self, messages, **kwargs):
        self.messages.append((messages, kwargs))
        return torch.tensor([[31, 32, 33]])

    def decode(self, emitted, *, skip_special_tokens):
        assert skip_special_tokens
        return "fixture decoded text"


class FixtureTorchModel(torch.nn.Module):
    """Tiny random tensor emitter, NOT a trained/public model or real measurement."""

    def __init__(self):
        super().__init__()
        self.weight = torch.nn.Parameter(torch.tensor([1.0]), requires_grad=False)
        self.generation_config = SimpleNamespace(eos_token_id=0)
        self.calls = []

    def generate(self, ids, **kwargs):
        self.calls.append({"rngs": (random.random(), np.random.random()), "kwargs": kwargs,
                           "inference_mode": torch.is_inference_mode_enabled()})
        tokens = torch.randint(1, 25, (1, 4))
        tokens = torch.cat((tokens, torch.zeros((1, 1), dtype=torch.long)), dim=1)
        return torch.cat((ids, tokens), dim=1)


def tensor_fixture_backend():
    backend = runner.TorchGenerationBackend.__new__(runner.TorchGenerationBackend)
    backend.device = "cpu"
    backend.tokenizer = FixtureTokenizer()
    backend.model = FixtureTorchModel().eval()
    backend.parameter_versions = backend._versions()
    backend.provenance = {"source": "tiny torch fixture; no public checkpoint"}
    backend.verified = False
    return backend


def test_torch_backend_rng_reset_exact_suffix_including_eos_and_frozen_weights():
    backend = tensor_fixture_backend()
    before = backend.model.weight.clone()
    short = backend.generate(runner.CIRCLE_TASK, seed=42, max_new_tokens=64)
    long = backend.generate(runner.CIRCLE_TASK, seed=42, max_new_tokens=256)
    assert short.token_ids == long.token_ids
    assert len(short.token_ids) == 5 and short.token_ids[-1] == 0
    assert short.prompt_tokens == 3 and not short.budget_exhausted
    assert backend.model.calls[0]["rngs"] == backend.model.calls[1]["rngs"]
    assert all(call["inference_mode"] for call in backend.model.calls)
    assert all(call["kwargs"]["pad_token_id"] == 0 for call in backend.model.calls)
    assert all(call["kwargs"]["do_sample"] for call in backend.model.calls)
    assert torch.equal(backend.model.weight, before) and backend.model.weight.grad is None
    assert backend.tokenizer.messages[0][0] == [{"role": "user", "content": runner.CIRCLE_TASK}]
    with torch.no_grad():
        backend.model.weight.add_(1)
    with pytest.raises(RuntimeError, match="parameter version changed"):
        backend.generate(runner.CIRCLE_TASK, seed=42, max_new_tokens=64)


def test_torch_backend_refuses_unfrozen_train_mode_or_unverified_source(tmp_path, monkeypatch):
    backend = tensor_fixture_backend()
    backend.model.train()
    with pytest.raises(RuntimeError, match="eval-mode and frozen"):
        backend.assert_frozen()
    backend.model.eval()
    backend.model.weight.requires_grad_(True)
    with pytest.raises(RuntimeError, match="eval-mode and frozen"):
        backend.assert_frozen()

    calls = []

    def reject_provenance(*args):
        calls.append(args)
        raise ValueError("bad upstream source hash")

    monkeypatch.setattr(runner, "verify_local_checkpoint", reject_provenance)
    with pytest.raises(ValueError, match="bad upstream source hash"):
        runner.TorchGenerationBackend(tmp_path, "official/model", "f" * 40, "cpu")
    assert calls == [(tmp_path, "official/model", "f" * 40)]


def test_cli_rejects_existing_directory_before_sandbox_or_model_load(tmp_path, monkeypatch):
    output = tmp_path / "already"
    output.mkdir()
    marker = output / "marker"
    marker.write_text("preserve user output")

    def forbidden(*args, **kwargs):
        pytest.fail("existing output must be rejected before model/sandbox initialization")

    monkeypatch.setattr(runner, "ProgramSandbox", forbidden)
    monkeypatch.setattr(runner, "TorchGenerationBackend", forbidden)
    with pytest.raises(FileExistsError, match="fresh output"):
        runner.main(["--checkpoint", "local", "--checkpoint-id", "official/model",
                     "--revision", "f" * 40, "--output", str(output)])
    assert marker.read_text() == "preserve user output"


def test_cli_injected_fixture_artifacts_keep_diagnostic_label(tmp_path, monkeypatch, capsys):
    constructed = []

    def backend_factory(*args):
        constructed.append(args)
        return FixtureBackend()

    monkeypatch.setattr(runner, "TorchGenerationBackend", backend_factory)
    monkeypatch.setattr(runner, "ProgramSandbox", FixtureSandbox)
    output = tmp_path / "fresh"
    assert runner.main([
        "--checkpoint", "local", "--checkpoint-id", "official/model", "--revision", "f" * 40,
        "--device", "cpu", "--seeds", "42,43", "--budgets", "64,256", "--output", str(output),
    ]) == 0
    assert constructed == [(Path("local"), "official/model", "f" * 40, "cpu")]
    metadata = json.loads((output / "measurement.json").read_text())
    assert not metadata["real_model_execution"]
    assert metadata["audit"]["paired_executions"] == 2
    assert len((output / "pairs.jsonl").read_text().splitlines()) == 4
    assert json.loads(capsys.readouterr().out)["cost_unit"] == "generated_token_units"
