"""Synthetic CPU fixtures for A100 metadata gates; not real GPU evidence."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile

import pytest


def module():
    path = Path(__file__).resolve().parents[1] / "scripts/curate_oct14_skilldreamer.py"
    spec = importlib.util.spec_from_file_location("skill_a100_curation", path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def fixture(tmp_path, monkeypatch):
    curator = module()
    monkeypatch.setattr(curator, "ROOT", tmp_path / "output")
    directory = tmp_path / "runs"
    directory.mkdir()
    commit = "47f0e9cebc196e15c991d494dc4072367f53043b"
    observer_commit = "a" * 40
    paths = ["scripts/run_skilldreamer.py", "src/auto_research/reproductions/skilldreamer/experiment.py",
             "src/auto_research/reproductions/skilldreamer/algorithm.py", "src/auto_research/reproductions/skilldreamer/gallery.json",
             "src/auto_research/reproductions/near/data.py", "src/auto_research/reproductions/near/experiment.py",
             "src/auto_research/reproductions/state_opd/environment.py"]
    observer_path = "scripts/observe_oct14_skilldreamer.py"
    def source(name):
        return ("CPU source fixture only: " + name).encode()
    source_archive = tmp_path / "algorithm.tar"
    observer_archive = tmp_path / "observer.tar"
    for archive_path, names in ((source_archive, paths), (observer_archive, [observer_path])):
        with tarfile.open(archive_path, "w") as archive:
            for name in names:
                content = source(name)
                info = tarfile.TarInfo(name)
                info.size = len(content)
                archive.addfile(info, io.BytesIO(content))
    monkeypatch.setattr(curator.subprocess, "check_output", lambda command, **kwargs: source(command[-1].split(":", 1)[1]))
    hashes = {name: hashlib.sha256(source(name)).hexdigest() for name in paths}
    observer_sha = hashlib.sha256(source(observer_path)).hexdigest()
    run_config = {"model_dir": "/tmp/auto-research-qwen2.5-7b", "encoder_dir": "/tmp/oct14-skill-validation7b-public/minilm",
                  "raw_data": "/tmp/oct14-skill-full7b-public/validation24.jsonl", "device": "cuda", "max_queries": 24,
                  "max_new_tokens": 256, "top_k": 3, "action_budget": 8}
    config = {"run_config": run_config, "algorithm_commit": commit, "source_sha256": hashes,
              "observer_source_commit": observer_commit, "observer_source_sha256": observer_sha,
              "wall_limit_seconds": 14400}
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config))
    config_sha = hashlib.sha256(config_path.read_bytes()).hexdigest()
    run_config_sha = hashlib.sha256(json.dumps(run_config, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ordered = sorted(map(str, range(24)), key=lambda value: hashlib.sha256(("skilldreamer-v1:" + value).encode()).hexdigest())
    dataset = {"public_id": "openai/grade-school-math", "revision": "3101c7d5072418e28b9008a6636bde82a006892c",
               "source_split": "train", "official_test_opened": False,
               "files": {"validation24.jsonl": "8f33a9f7a44067e362458e4daf0eb1ad629a2aac2f44ffefe731e36b19dcb8c1"}}
    model = {"public_id": "Qwen/Qwen2.5-7B-Instruct", "revision": "bb46c15ee4bb56c5b63245ef50fd7637234d6f75"}
    encoder = {"public_id": "sentence-transformers/all-MiniLM-L6-v2", "revision": "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"}
    model_files = ["config.json", "generation_config.json", "merges.txt", "model.safetensors.index.json",
                   "tokenizer.json", "tokenizer_config.json", "vocab.json", *[
                       f"model-{i:05d}-of-00004.safetensors" for i in range(1, 5)]]
    encoder_files = ["model.safetensors", "config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "vocab.txt"]
    audited_model = {**model, "files": {name: hashlib.sha256(source(name)).hexdigest() for name in model_files}}
    audited_encoder = {**encoder, "files": {name: hashlib.sha256(source(name)).hexdigest() for name in encoder_files}}
    model["files"] = {name: digest for name, digest in audited_model["files"].items() if name.endswith((".safetensors", ".json"))}
    encoder["files"] = {name: audited_encoder["files"][name] for name in ("model.safetensors", "config.json", "tokenizer.json")}
    for seed in (42, 43, 44):
        episode = {"correct": False, "submitted_answer": None, "capability_checks": [{"assessment": "CPU fixture only"}],
                   "loaded_skills": ["CPU-fixture-skill"], "executed_actions": 1, "model_calls_including_psg": 2,
                   "generated_tokens_including_psg": 10, "generation_errors": 1, "tool_errors": 0,
                   "observations": ["Calculator ready; no reference answer is available.", "Calculator result: 7"]}
        raw = {"paper": "skilldreamer", "seed": seed, "device": "cuda", "diagnostic_only": True, "promotion_eligible": False,
               "evaluation_tier": "l2_public_dataset",
               "variants": {arm: {"pass_rate": 0.0, "load_rate": 1.0, "generation_failures": 16,
                   "tool_failure_episodes": 0, "model_calls": 32, "generated_tokens": 160, "executed_actions": 16} for arm in curator.ARMS},
               "episodes": {arm: [{**episode, "id": identifier} for identifier in ordered[8:]] for arm in curator.ARMS},
               "protocol": {"gold_visible_to_policy": False, "validation_ids": ordered[:8], "test_ids": ordered[8:],
                            "raw_sha256": dataset["files"]["validation24.jsonl"], "dataset": dataset, "checkpoint": model, "encoder": encoder}}
        raw_path = directory / f"seed{seed}.json"
        raw_path.write_text(json.dumps(raw))
        trace_path = directory / f"trace-seed{seed}.jsonl"
        events = [event for call in range(1, 97) for event in (
            {"event": "generation_attempt", "call": call, "prompt": "CPU fixture only"},
            {"event": "generation_response", "call": call, "response": "CPU fixture only", "generated_tokens": 5})]
        trace_path.write_text("".join(json.dumps(event) + "\n" for event in events))
        observer = {"status": "completed_original_three_arm_diagnostic", "seed": seed, "exit_code": 0,
                    "instrumentation": {"original_call_forwarded_unchanged": True,
                        "temporary_call_instrumentation": True, "restored_after_run": True},
                    "diagnostic_only": True, "promotion_eligible": False, "calls_attempted": 96, "generation_responses": 96,
                    "generated_tokens": 480, "wall_seconds": 1.0, "peak_gpu_memory_allocated_bytes": 100,
                    "peak_gpu_memory_reserved_bytes": 200, "raw_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                    "trace_sha256": hashlib.sha256(trace_path.read_bytes()).hexdigest(), "execution_config_sha256": config_sha,
                    "accelerator": {"vendor": "NVIDIA", "model": "NVIDIA A100-SXM4-80GB"},
                    "command": ["python", f"/tmp/auto-research-oct14-aaaaaaaa/{observer_path}", "--config", str(config_path),
                                "--seed", str(seed), "--output", f"/tmp/CPU-fixture/seed{seed}"],
                    "audit": {"seed": seed, "algorithm_commit": commit, "executed_source_sha256": hashes,
                              "observer_source": {"commit": observer_commit, "sha256": observer_sha, "immutable_root_bound": True},
                              "run_config": run_config, "run_config_sha256": run_config_sha, "dataset": dataset,
                              "checkpoint": audited_model, "encoder": audited_encoder,
                              "limits": {"model_calls": 1248, "output_tokens": 319488, "wall_seconds": 14400}}}
        (directory / f"observer-seed{seed}.json").write_text(json.dumps(observer))
    return curator, directory, commit, source_archive, observer_commit, observer_archive, config_path


def invoke(value):
    curator, directory, commit, archive, observer_commit, observer_archive, config_path = value
    return curator.curate(directory, commit, archive, accelerator_model="NVIDIA A100-SXM4-80GB",
                          observer_commit=observer_commit, observer_archive=observer_archive, config_path=config_path)


def test_a100_l1_zero_accuracy_and_zero_finish_do_not_mean_unexecuted_core(tmp_path, monkeypatch):
    value = fixture(tmp_path, monkeypatch)
    result = invoke(value)
    assert result["checks"]["actual_csi_assessments"] == [16, 16, 16]
    receipt = json.loads((tmp_path / "output/docs/gpu-validations/oct13-skilldreamer-a100.json").read_text())
    assert receipt["accelerator"]["model"] == "NVIDIA A100-SXM4-80GB"
    assert receipt["metrics"]["skilldreamer.pass_rate"]["mean"] == 0
    assert [command[command.index("--seed") + 1] for command in receipt["all_sanitized_commands"]] == ["42", "43", "44"]
    artifact = json.loads((tmp_path / "output" / value[0].DOC / "public-a100-seeds42-44-47f0e9ce.json").read_text())
    assert artifact["evaluation_protocol"]["tier"] == "l1_mechanism" and artifact["promotion_eligible"] is False
    assert artifact["evaluation_protocol"]["formal_comparison"] is False
    assert artifact["evaluation_protocol"]["original_runner_tier"] == "l2_public_dataset"
    assert all(run["evaluation_tier"] == "l2_public_dataset" for run in artifact["seed_results"])
    assert "restricted arithmetic" in artifact["evaluation_protocol"]["assessed_scope_reason"]
    for seed in (42, 43, 44):
        assert (tmp_path / "output" / value[0].DOC / f"raw/a100-47f0e9ce/seed{seed}.json").read_bytes() == (value[1] / f"seed{seed}.json").read_bytes()
    assert not (tmp_path / "output/docs/gpu-validations/oct13-skilldreamer-a30.json").exists()
    assert not (tmp_path / "output" / value[0].DOC / "raw/seed42.json").exists()


@pytest.mark.parametrize("failure", ["observer_commit", "observer_sha", "algorithm_sha", "config_sha", "accelerator", "peak_nan", "peak_missing", "raw_sha", "trace_sha", "calls", "dataset", "core_csi"])
def test_a100_metadata_and_original_core_gates_fail_closed(tmp_path, monkeypatch, failure):
    value = fixture(tmp_path, monkeypatch)
    directory = value[1]
    path = directory / "observer-seed43.json"
    record = json.loads(path.read_text())
    if failure == "observer_commit":record["audit"]["observer_source"]["commit"] = "b" * 40
    elif failure == "observer_sha":record["audit"]["observer_source"]["sha256"] = "0" * 64
    elif failure == "algorithm_sha":record["audit"]["executed_source_sha256"]["scripts/run_skilldreamer.py"] = "0" * 64
    elif failure == "config_sha":record["execution_config_sha256"] = "0" * 64
    elif failure == "accelerator":record["accelerator"]["model"] = "NVIDIA A30"
    elif failure == "peak_nan":record["peak_gpu_memory_reserved_bytes"] = float("nan")
    elif failure == "peak_missing":record.pop("peak_gpu_memory_allocated_bytes")
    elif failure == "raw_sha":record["raw_sha256"] = "0" * 64
    elif failure == "trace_sha":record["trace_sha256"] = "0" * 64
    elif failure == "calls":record["generation_responses"] += 1
    else:
        raw_path = directory / "seed43.json"
        raw = json.loads(raw_path.read_text())
        if failure == "dataset":raw["protocol"]["raw_sha256"] = "0" * 64
        else:
            for row in raw["episodes"]["skilldreamer"]:row["capability_checks"] = []
        raw_path.write_text(json.dumps(raw))
        record["raw_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError):invoke(value)
    assert not (tmp_path / "output").exists()


@pytest.mark.parametrize("failure", ["episode_duplicate", "episode_order", "empty_model", "empty_encoder",
    "measured_missing", "measured_extra", "audited_missing", "audited_extra", "resource_bytes",
    "response_duplicate", "response_unknown", "response_order", "unpaired_attempt", "unknown_event",
    "instrumentation_missing", "instrumentation_unrestored", "instrumentation_false", "runner_tier"])
def test_a100_exact_ids_resource_sets_trace_pairing_and_transparency(tmp_path, monkeypatch, failure):
    value = fixture(tmp_path, monkeypatch)
    directory = value[1]
    record_path = directory / "observer-seed43.json"
    record = json.loads(record_path.read_text())
    raw_path = directory / "seed43.json"
    raw = json.loads(raw_path.read_text())
    if failure == "runner_tier":
        raw["evaluation_tier"] = "l1_mechanism"
    elif failure.startswith("episode"):
        episodes = raw["episodes"]["direct"]
        if failure == "episode_duplicate": episodes[0]["id"] = episodes[1]["id"]
        else: episodes[0], episodes[1] = episodes[1], episodes[0]
    elif failure.startswith("instrumentation"):
        if failure == "instrumentation_missing": record.pop("instrumentation")
        elif failure == "instrumentation_unrestored": record["instrumentation"]["restored_after_run"] = False
        else: record["instrumentation"]["original_call_forwarded_unchanged"] = False
    elif failure.startswith("response") or failure in ("unpaired_attempt", "unknown_event"):
        trace_path = directory / "trace-seed43.jsonl"
        events = [json.loads(line) for line in trace_path.read_text().splitlines()]
        if failure == "response_duplicate": events[3]["call"] = 1
        elif failure == "response_unknown": events[3]["call"] = 1000
        elif failure == "response_order": events[1], events[3] = events[3], events[1]
        elif failure == "unpaired_attempt": events[-1]["event"] = "generation_attempt"
        else: events.append({"event": "untracked_event"})
        trace_path.write_text("".join(json.dumps(event) + "\n" for event in events))
        record["trace_sha256"] = hashlib.sha256(trace_path.read_bytes()).hexdigest()
    else:
        measured = raw["protocol"]["encoder" if failure == "empty_encoder" else "checkpoint"]["files"]
        audited = record["audit"]["checkpoint"]["files"]
        if failure in ("empty_model", "empty_encoder"): measured.clear()
        elif failure == "measured_missing": measured.pop("config.json")
        elif failure == "measured_extra": measured["unknown.json"] = "a" * 64
        elif failure == "audited_missing": audited.pop("merges.txt")
        elif failure == "audited_extra": audited["unknown.json"] = "a" * 64
        else: audited["config.json"] = "0" * 64
    raw_path.write_text(json.dumps(raw))
    record["raw_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    record_path.write_text(json.dumps(record))
    with pytest.raises(ValueError): invoke(value)
    assert not (tmp_path / "output").exists()


def test_a100_trace_keeps_actual_generation_error_with_unique_attempt(tmp_path, monkeypatch):
    value = fixture(tmp_path, monkeypatch)
    directory = value[1]
    record_path = directory / "observer-seed43.json"
    record = json.loads(record_path.read_text())
    trace_path = directory / "trace-seed43.jsonl"
    events = [json.loads(line) for line in trace_path.read_text().splitlines()]
    events.extend([{"event": "generation_attempt", "call": 97, "prompt": "CPU error fixture only"},
                   {"event": "generation_error", "call": 97, "type": "ValueError", "message": "CPU fixture error"}])
    trace_path.write_text("".join(json.dumps(event) + "\n" for event in events))
    record["trace_sha256"] = hashlib.sha256(trace_path.read_bytes()).hexdigest()
    record["calls_attempted"] = 97
    record_path.write_text(json.dumps(record))
    result = invoke(value)
    assert result["checks"]["actual_model_calls"] == [96, 96, 96]
    assert result["checks"]["actual_generation_attempts"] == [96, 97, 96]
    assert result["checks"]["actual_generation_responses"] == [96, 96, 96]
    assert result["checks"]["actual_failed_generation_attempts"] == [0, 1, 0]
    assert result["checks"]["failed_generation_output_token_cost"] == [0, None, 0]
    assert "generation_error" in trace_path.read_text()


@pytest.mark.parametrize('arm', ['no_skills', 'direct', 'skilldreamer'])
@pytest.mark.parametrize('field', ['pass_rate', 'load_rate', 'generation_failures', 'tool_failure_episodes',
    'model_calls', 'generated_tokens', 'executed_actions'])
def test_every_arm_summary_drift_is_rejected_even_with_updated_raw_sha(tmp_path, monkeypatch, arm, field):
    value = fixture(tmp_path, monkeypatch)
    raw_path = value[1] / 'seed43.json'
    raw = json.loads(raw_path.read_text())
    raw['variants'][arm][field] += 1
    raw_path.write_text(json.dumps(raw))
    record_path = value[1] / 'observer-seed43.json'
    record = json.loads(record_path.read_text())
    record['raw_sha256'] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    record_path.write_text(json.dumps(record))
    with pytest.raises(ValueError, match='summaries'): invoke(value)
    assert not (tmp_path / 'output').exists()


@pytest.mark.parametrize('field,value_', [('correct', 1), ('correct', 'false'), ('loaded_skills', 'skill'),
    ('executed_actions', True), ('generation_errors', -1), ('tool_errors', 0.0),
    ('model_calls_including_psg', False), ('generated_tokens_including_psg', float('nan'))])
def test_episode_scalar_types_are_actual_not_truthy_or_illegal(tmp_path, monkeypatch, field, value_):
    value = fixture(tmp_path, monkeypatch)
    raw_path = value[1] / 'seed43.json'; raw = json.loads(raw_path.read_text())
    raw['episodes']['direct'][0][field] = value_
    raw_path.write_text(json.dumps(raw))
    with pytest.raises(ValueError): invoke(value)
    assert not (tmp_path / 'output').exists()


@pytest.mark.parametrize('target', ['artifact', 'receipt', 'last_raw', 'validator'])
def test_all_validation_and_collision_checks_precede_any_output_write(tmp_path, monkeypatch, target):
    value = fixture(tmp_path, monkeypatch)
    root = tmp_path / 'output'
    if target == 'validator':
        monkeypatch.setattr(value[0], 'validate_gpu_receipt', lambda _receipt: ['CPU fixture invalid receipt'])
        expected = ValueError; before = set()
    else:
        relative = {'artifact': value[0].DOC + '/public-a100-seeds42-44-47f0e9ce.json',
            'receipt': 'docs/gpu-validations/oct13-skilldreamer-a100.json',
            'last_raw': value[0].DOC + '/raw/a100-47f0e9ce/seed44.json'}[target]
        path = root / relative; path.parent.mkdir(parents=True); path.write_bytes(b'EXISTING CPU FIXTURE ONLY')
        expected = FileExistsError; before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
    with pytest.raises(expected): invoke(value)
    after = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()} if root.exists() else set()
    assert after == before


def test_pure_invalid_env_steps_cannot_pass_successful_calculator_gate(tmp_path, monkeypatch):
    value = fixture(tmp_path, monkeypatch)
    raw_path = value[1] / 'seed43.json'; raw = json.loads(raw_path.read_text())
    for row in raw['episodes']['skilldreamer']:
        row['observations'][-1] = 'Invalid action schema. Use calculator or finish with the specified JSON arguments.'
        row['tool_errors'] = 1
    raw['variants']['skilldreamer']['tool_failure_episodes'] = 16
    raw_path.write_text(json.dumps(raw))
    record_path = value[1] / 'observer-seed43.json'; record = json.loads(record_path.read_text())
    record['raw_sha256'] = hashlib.sha256(raw_path.read_bytes()).hexdigest(); record_path.write_text(json.dumps(record))
    with pytest.raises(ValueError, match='successful calculator'): invoke(value)
    assert not (tmp_path / 'output').exists()


def test_actual_calculator_submission_and_failed_step_counts_are_separate():
    curator = module()
    row = {'executed_actions': 3, 'tool_errors': 1, 'observations': ['Calculator ready; no reference answer is available.',
        'Skill loaded: CPU-fixture; reread procedure.', 'Invalid JSON/capability assessment; no tool was executed.',
        'Calculator error: ZeroDivisionError', 'Calculator result: 7',
        'Submission recorded. No correctness feedback is exposed to the policy.']}
    assert curator.observed_environment_steps(row) == {'successful_calculator_calls': 1, 'submissions': 1,
        'failed_environment_steps': 1}
    row['executed_actions'] = 4
    with pytest.raises(ValueError, match='env.step'): curator.observed_environment_steps(row)


@pytest.mark.parametrize('field,value_', [('pass_rate', False), ('load_rate', float('nan')),
    ('tool_failure_episodes', False), ('generation_failures', 16.0)])
def test_summary_types_are_strict_even_when_python_numeric_equality_matches(tmp_path, monkeypatch, field, value_):
    value = fixture(tmp_path, monkeypatch)
    path = value[1] / 'seed42.json'; raw = json.loads(path.read_text())
    raw['variants']['direct'][field] = value_; path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match='summaries'): invoke(value)
    assert not (tmp_path / 'output').exists()


def test_original_valueerror_episode_without_observations_or_error_fields_is_kept(tmp_path, monkeypatch):
    value = fixture(tmp_path, monkeypatch)
    path = value[1] / 'seed43.json'; raw = json.loads(path.read_text())
    original = raw['episodes']['direct'][0]
    raw['episodes']['direct'][0] = {'id': original['id'], 'correct': False, 'loaded_skills': [], 'executed_actions': 0,
        'failure': 'CPU fixture original PSG ValueError', 'model_calls': 0,
        'model_calls_including_psg': 2, 'generated_tokens_including_psg': 10}
    raw['variants']['direct']['load_rate'] = 15 / 16
    raw['variants']['direct']['executed_actions'] = 15
    path.write_text(json.dumps(raw))
    record_path = value[1] / 'observer-seed43.json'; record = json.loads(record_path.read_text())
    record['raw_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest(); record_path.write_text(json.dumps(record))
    result = invoke(value)
    assert result['metrics']['direct.generation_failures']['mean'] == 16
    copied = json.loads((tmp_path / 'output' / value[0].DOC / 'raw/a100-47f0e9ce/seed43.json').read_text())
    assert copied['episodes']['direct'][0] == raw['episodes']['direct'][0]


def test_per_arm_tokens_cannot_be_shifted_while_total_and_trace_still_match(tmp_path, monkeypatch):
    value = fixture(tmp_path, monkeypatch)
    path = value[1] / 'seed43.json'; raw = json.loads(path.read_text())
    raw['variants']['direct']['generated_tokens'] += 1
    raw['variants']['no_skills']['generated_tokens'] -= 1
    path.write_text(json.dumps(raw))
    record_path = value[1] / 'observer-seed43.json'; record = json.loads(record_path.read_text())
    record['raw_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest(); record_path.write_text(json.dumps(record))
    with pytest.raises(ValueError, match='summaries'): invoke(value)
    assert not (tmp_path / 'output').exists()


def test_identical_existing_raw_is_not_rewritten_during_valid_publication(tmp_path, monkeypatch):
    value = fixture(tmp_path, monkeypatch)
    existing = tmp_path / 'output' / value[0].DOC / 'raw/a100-47f0e9ce/seed42.json'
    existing.parent.mkdir(parents=True)
    existing.write_bytes((value[1] / 'seed42.json').read_bytes())
    original_open = Path.open
    def protected(path, mode='r', *args, **kwargs):
        if path == existing and any(flag in mode for flag in ('w', 'a', 'x')):
            pytest.fail('identical immutable raw must never be rewritten')
        return original_open(path, mode, *args, **kwargs)
    monkeypatch.setattr(Path, 'open', protected)
    invoke(value)
    assert existing.read_bytes() == (value[1] / 'seed42.json').read_bytes()


@pytest.mark.parametrize('field,value_', [('observations', ['Calculator result: 7', 'Calculator result: 8']),
    ('tool_errors', 1)])
def test_observation_counter_mismatch_rejects_before_any_write(tmp_path, monkeypatch, field, value_):
    value = fixture(tmp_path, monkeypatch)
    path = value[1] / 'seed43.json'; raw = json.loads(path.read_text())
    raw['episodes']['direct'][0][field] = value_
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match='env.step'): invoke(value)
    assert not (tmp_path / 'output').exists()
