"""CPU observer contract fixtures; never model/GPU capability evidence."""
import hashlib
import importlib.util
import json
import random
from pathlib import Path
from types import SimpleNamespace

import pytest


def module():
    path = Path(__file__).resolve().parents[1] / "scripts/observe_oct14_skilldreamer.py"
    spec = importlib.util.spec_from_file_location("skill_full_observer", path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def config(observer):
    return {"run_config": {**observer.RESOURCE_PATHS, "device": "cuda", "max_queries": 24,
                            "max_new_tokens": 256, "top_k": 3, "action_budget": 8},
            "wall_limit_seconds": 14400}


def test_exact_original_three_arm_caps_without_content_selection():
    observer = module()
    assert observer.MAX_CALLS == 16 * (24 + 24 + 1 + 5 + 24) == 1248
    assert observer.MAX_TOKENS == observer.MAX_CALLS * 256 == 319488
    assert observer.fixed_config(config(observer), 42) == config(observer)["run_config"]


@pytest.mark.parametrize("field,value", [("max_queries", 25), ("max_new_tokens", 257),
                                         ("top_k", 4), ("action_budget", 9), ("action_budget", True),
                                         ("model_dir", "/tmp/arbitrary-model")])
def test_original_run_config_cannot_raise_caps_or_replace_resources(field, value):
    observer = module()
    value_config = config(observer)
    value_config["run_config"][field] = value
    with pytest.raises(ValueError):
        observer.fixed_config(value_config, 42)


def source_fixture(observer, tmp_path, monkeypatch):
    root = tmp_path / "auto-research-oct14-47f0e9ce"
    hashes, modules = {}, {}
    for name in observer.SOURCE_SHA256:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("CPU source fixture only: " + name)
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        if name.startswith("src/") and name.endswith(".py"):
            modules[name.removeprefix("src/").removesuffix(".py").replace("/", ".")] = SimpleNamespace(__file__=str(path))
    (root / ".source-commit").write_text(observer.ALGORITHM_COMMIT)
    commit = "a" * 40
    own_root = tmp_path / "auto-research-oct14-aaaaaaaa"
    own = own_root / "scripts/observe_oct14_skilldreamer.py"
    own.parent.mkdir(parents=True)
    own.write_text("CPU observer binding fixture only")
    (own_root / ".source-commit").write_text(commit)
    monkeypatch.setattr(observer, "SOURCE_SHA256", hashes)
    monkeypatch.setattr(observer.importlib, "import_module", lambda name: modules[name])
    monkeypatch.setattr(observer, "__file__", str(own))
    return {"algorithm_commit": observer.ALGORITHM_COMMIT, "algorithm_source_root": str(root),
            "source_sha256": hashes, "observer_source_commit": commit, "observer_source_root": str(own_root),
            "observer_source_sha256": hashlib.sha256(own.read_bytes()).hexdigest()}, root, own


def test_fixed_seven_file_algorithm_and_independent_observer_are_bound(tmp_path, monkeypatch):
    observer = module()
    value, _, _ = source_fixture(observer, tmp_path, monkeypatch)
    actual = observer.source_binding(value)
    assert len(actual["executed_source_sha256"]) == 7
    assert actual["observer_source"]["immutable_root_bound"] is True


@pytest.mark.parametrize("failure", ["algorithm_commit", "algorithm_marker", "algorithm_bytes", "missing_script", "observer_commit", "observer_sha", "observer_marker", "outer"])
def test_unbound_algorithm_or_observer_cannot_run(tmp_path, monkeypatch, failure):
    observer = module()
    value, root, own = source_fixture(observer, tmp_path, monkeypatch)
    if failure == "algorithm_commit":
        value["algorithm_commit"] = "701f45007be75cf6153f98812ef94e087c94a8f0"
    elif failure == "algorithm_marker":
        (root / ".source-commit").write_text("b" * 40)
    elif failure == "algorithm_bytes":
        (root / "src/auto_research/reproductions/skilldreamer/algorithm.py").write_text("changed")
    elif failure == "missing_script":
        value["source_sha256"] = {key: digest for key, digest in value["source_sha256"].items() if key != "scripts/run_skilldreamer.py"}
    elif failure == "observer_commit":
        value["observer_source_commit"] = "b" * 40
    elif failure == "observer_sha":
        value["observer_source_sha256"] = "0" * 64
    elif failure == "observer_marker":
        (own.parents[1] / ".source-commit").write_text("b" * 40)
    else:
        monkeypatch.setattr(observer, "__file__", str(tmp_path / "dirty-outer/observe.py"))
    with pytest.raises(ValueError):
        observer.source_binding(value)


def test_hard_wall_interrupts_one_blocking_call():
    import time
    observer = module()
    with pytest.raises(TimeoutError):
        with observer.hard_wall(0.03):
            time.sleep(1)


@pytest.mark.parametrize("failure", [False, "native", "generate"])
@pytest.mark.parametrize("keyword_prompt", [False, True])
def test_observer_delegates_original_sampling_and_retains_trace_peaks(tmp_path, monkeypatch, failure, keyword_prompt):
    observer = module()
    from auto_research.reproductions.skilldreamer import experiment
    import torch
    supplied, prompts = [], []
    error = RuntimeError("CPU fixture native failure")
    expected_response = "CPU fixture response unchanged"
    random.seed(123)
    torch.manual_seed(123)
    expected_rng = (random.random(), torch.rand(1))
    random.seed(123)
    torch.manual_seed(123)
    parameter = object()

    class Generator:
        generated_tokens = 0
        def __call__(self, prompt, *, unchanged):
            assert unchanged is parameter
            prompts.append(prompt)
            assert random.random() == expected_rng[0]
            assert torch.equal(torch.rand(1), expected_rng[1])
            if failure == "generate":
                raise error
            self.generated_tokens += 5
            return expected_response

    original = Generator.__call__
    def native(run_config, seed):
        supplied.append((run_config, seed))
        generator = Generator()
        if keyword_prompt:
            response = generator(prompt="CPU fixture prompt without gold", unchanged=parameter)
        else:
            response = generator("CPU fixture prompt without gold", unchanged=parameter)
        assert response is expected_response
        if failure:
            raise error
        return {"variants": {"fixture": {"model_calls": 1, "generated_tokens": 5}}}

    monkeypatch.setattr(experiment, "LocalGenerator", Generator)
    monkeypatch.setattr(experiment, "run_skilldreamer", native)
    monkeypatch.setattr(observer, "audit", lambda *args, **kwargs: {"CPU_fixture_only": True})
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "get_device_name", lambda *_: "NVIDIA A100-SXM4-80GB")
    monkeypatch.setattr(torch.cuda, "set_device", lambda *_: None)
    monkeypatch.setattr(torch.cuda, "reset_peak_memory_stats", lambda *_: None)
    monkeypatch.setattr(torch.cuda, "synchronize", lambda: None)
    monkeypatch.setattr(torch.cuda, "max_memory_allocated", lambda *_: 100)
    monkeypatch.setattr(torch.cuda, "max_memory_reserved", lambda *_: 200)
    directory = tmp_path / "fresh"
    if failure:
        with pytest.raises(RuntimeError, match="native failure") as caught:
            observer.run(config(observer), 42, directory, invocation=["CPU fixture only"], config_file_sha256="a" * 64)
        assert caught.value is error
    else:
        observer.run(config(observer), 42, directory, invocation=["CPU fixture only"], config_file_sha256="a" * 64)
    assert supplied == [(config(observer)["run_config"], 42)] and prompts == ["CPU fixture prompt without gold"]
    assert Generator.__call__ is original
    record = json.loads((directory / "observer.json").read_text())
    assert record["peak_gpu_memory_allocated_bytes"] == 100 and record["peak_gpu_memory_reserved_bytes"] == 200
    assert record["generation_responses"] == (0 if failure == "generate" else 1)
    assert record["generated_tokens"] == (0 if failure == "generate" else 5)
    assert record["instrumentation"] == {"original_call_forwarded_unchanged": True,
            "temporary_call_instrumentation": True, "restored_after_run": True}
    assert "no_monkeypatch" not in record
    assert record["status"] == ("failed" if failure else "completed_original_three_arm_diagnostic")
    assert (directory / "trace.jsonl").read_text().count("generation_response") == (0 if failure == "generate" else 1)
    assert (directory / "seed42.json").exists() is (not failure)


def test_generator_exception_survives_secondary_allocator_observation_failure(tmp_path, monkeypatch):
    observer = module()
    from auto_research.reproductions.skilldreamer import experiment
    import torch
    error = ValueError("CPU fixture original generator error")
    class Generator:
        generated_tokens = 0
        def __call__(self, prompt):
            raise error
    original = Generator.__call__
    monkeypatch.setattr(experiment, "LocalGenerator", Generator)
    monkeypatch.setattr(experiment, "run_skilldreamer", lambda *args: Generator()("CPU fixture only"))
    monkeypatch.setattr(observer, "audit", lambda *args, **kwargs: {})
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "get_device_name", lambda *_: "NVIDIA A100-SXM4-80GB")
    monkeypatch.setattr(torch.cuda, "set_device", lambda *_: None)
    monkeypatch.setattr(torch.cuda, "reset_peak_memory_stats", lambda *_: None)
    def peak_failure(*args):
        raise RuntimeError("CPU fixture secondary peak error")
    monkeypatch.setattr(torch.cuda, "max_memory_allocated", peak_failure)
    directory = tmp_path / "fresh"
    with pytest.raises(ValueError) as caught:
        observer.run(config(observer), 42, directory, invocation=["CPU fixture only"], config_file_sha256="a" * 64)
    assert caught.value is error and Generator.__call__ is original
    record = json.loads((directory / "observer.json").read_text())
    assert record["failure"]["message"] == str(error)
    assert record["allocator_observation_failure"]["type"] == "RuntimeError"
    assert record["instrumentation"]["restored_after_run"] is True
