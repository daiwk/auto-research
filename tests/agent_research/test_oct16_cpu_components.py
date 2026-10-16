from dataclasses import replace
import hashlib
import importlib.util
import hashlib
import json
from pathlib import Path

import pytest

from auto_research.agent_research.formcraft import Library, compose_from_examples, run_sequence_study
from auto_research.agent_research.transparent_compact import compact, load_session, recompact


def test_compaction_preserves_prose_calls_and_exact_recovery():
    source = [{"id": "u", "role": "user", "content": "保留原话\nDon't modify README."},
              {"id": "a", "role": "assistant", "content": [
                  {"type": "thinking", "thinking": "private"},
                  {"type": "text", "text": "I'll inspect it."},
                  {"type": "toolCall", "id": "t", "name": "read", "arguments": {"path": "a"}}]},
              {"id": "t", "role": "tool", "tool_call_id": "t", "content": "output" * 1000}]
    checkpoint = compact(source)
    assert checkpoint.messages[0]["content"][0]["text"] == source[0]["content"]
    assert checkpoint.messages[1]["content"][1] == source[1]["content"][1]
    assert checkpoint.messages[1]["content"][2] == source[1]["content"][2]
    assert checkpoint.recover("a:thinking-0") == source[1]["content"][0]
    assert checkpoint.recover("t:tool-output-0")["text"] == source[2]["content"]
    assert checkpoint.messages[2]["tool_call_id"] == "t"
    assert checkpoint.output_characters < checkpoint.input_characters
    assert checkpoint.to_dict()["capability_score"] is None
    assert source[1]["content"][0]["thinking"] == "private"


def test_cap_is_explicit_and_recovery_hash_is_checked():
    checkpoint = compact([{"role": "user", "content": "old"},
                          {"role": "assistant", "content": "new"}], max_prose_characters=3)
    assert checkpoint.prose_dropped == 1
    assert checkpoint.messages[0]["content"][0]["reason"].startswith("cap-prose")
    assert checkpoint.messages[1]["content"][0]["text"] == "new"
    key = next(iter(checkpoint.recovery))
    checkpoint.recovery[key]["payload"] = "tampered"
    with pytest.raises(ValueError, match="hash"):
        checkpoint.recover(key)


def test_pi_bash_execution_is_archived_without_running_command():
    checkpoint = compact([{"id": "bash", "role": "bashExecution", "command": "exit 7",
                           "output": "actual stdout", "exitCode": 7, "cancelled": False,
                           "truncated": True, "excludeFromContext": True}])
    assert checkpoint.messages[0]["command"] == "exit 7"
    assert checkpoint.messages[0]["exitCode"] == 7
    assert checkpoint.messages[0]["cancelled"] is False
    assert checkpoint.messages[0]["truncated"] is True
    assert checkpoint.messages[0]["excludeFromContext"] is True
    assert checkpoint.recover("bash:tool-output-0")["text"] == "actual stdout"


def test_repeated_compaction_preserves_original_archive():
    first = compact([{"id": "u", "role": "user", "content": "keep exact"},
                     {"id": "t", "role": "tool", "content": "original stdout"}])
    second = recompact(first, [{"id": "a", "role": "assistant", "content": "new prose"}])
    assert second.recover("t:tool-output-0")["text"] == "original stdout"
    assert second.messages[0] == first.messages[0]
    assert second.messages[1] == first.messages[1]
    with pytest.raises(ValueError, match="archive"):
        compact(list(first.messages))


def test_pi_branch_does_not_merge_siblings(tmp_path):
    path = tmp_path / "session.jsonl"
    rows = [{"type": "session", "id": "session"},
            {"type": "message", "id": "a", "parentId": None,
             "message": {"role": "user", "content": "start"}},
            {"type": "message", "id": "b", "parentId": "a",
             "message": {"role": "assistant", "content": "sibling"}},
            {"type": "message", "id": "c", "parentId": "a",
             "message": {"role": "assistant", "content": "chosen"}}]
    path.write_text("\n".join(json.dumps(row) for row in rows))
    assert [row["content"] for row in load_session(path)] == ["start", "chosen"]
    assert [row["content"] for row in load_session(path, leaf_id="b")] == ["start", "sibling"]
    with pytest.raises(ValueError, match="missing"):
        load_session(path, leaf_id="absent")


@pytest.mark.parametrize("is_error", [False, True])
def test_pi_tool_result_pairing_and_error_metadata_survive_compaction_and_recompaction(tmp_path, is_error):
    path = tmp_path / "pi-session.jsonl"
    call = {"type": "toolCall", "id": "call-1", "name": "read", "arguments": {"path": "public.txt"}}
    body = [{"type": "text", "text": "error output" if is_error else "full original output"}]
    rows = [
        {"type": "message", "id": "a", "parentId": None,
         "message": {"role": "assistant", "content": [call]}},
        {"type": "message", "id": "t", "parentId": "a",
         "message": {"role": "toolResult", "toolCallId": "call-1", "toolName": "read",
                     "isError": is_error, "content": body}},
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows))
    first = compact(load_session(path))
    second = recompact(first, [{"id": "new", "role": "assistant", "content": "next message"}])
    for checkpoint in (first, second):
        visible_call, result = checkpoint.messages[:2]
        assert visible_call["content"][0]["id"] == result["toolCallId"] == "call-1"
        assert result["toolName"] == "read" and result["isError"] is is_error
        assert result["content"][0]["type"] == "omission"
        assert checkpoint.recover(result["content"][0]["recovery_key"]) == body[0]
    assert second.messages[1] == first.messages[1]


def test_formcraft_formation_admission_and_cold_reload(tmp_path):
    library = Library()
    zero, one = tuple(library.records)
    composite = library.form((zero, one))
    assert composite.identity not in library.records
    assert library.admit(composite, [(3,), (7, 9)], lambda value: (*value, 0, 1))
    assert library.invoke(composite.identity, (77,)) == (77, 0, 1)
    assert not library.admit(library.form((one, zero)), [(3,)], lambda value: (*value, 0, 1))
    assert library.failures[-1]["reason"] == "holdout_semantic_mismatch"
    path = tmp_path / "library.json"
    library.save(path)
    restored = Library.load(path)
    assert restored.invoke(composite.identity, (8,)) == (8, 0, 1)
    assert restored.failures == library.failures
    with pytest.raises(ValueError):
        library.evaluate(replace(composite, identity="bad"), ())


def test_composer_has_only_examples_and_real_bounded_search():
    library = Library()
    ids = tuple(library.records)
    examples = [((9,), (9, 1, 0)), ((), (1, 0))]
    selected, work = compose_from_examples(library, ids, examples, max_depth=2)
    assert selected is not None and work > 1
    assert library.evaluate(selected, (22, 33)) == (22, 33, 1, 0)
    missing, work = compose_from_examples(library, ids, examples, max_depth=2, candidate_limit=1)
    assert missing is None and work == 1


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_formcraft_paired_reuse_study(seed, tmp_path):
    snapshot = tmp_path / "libraries" / f"seed{seed}.json"
    result = run_sequence_study(seed=seed, snapshot_path=snapshot)
    assert result["metrics"]["goals_admitted"] == 12
    assert result["metrics"]["all_paired_holdouts_pass"]
    assert result["metrics"]["first_class_candidate_attempts"] < result["metrics"]["expanded_candidate_attempts"]
    assert len(result["paired_results"]) == 24
    assert result["promotion_eligible"] is False
    assert result["paper_exact_replication"] is False
    assert all(row["split"] == "isolated_final_test" for row in result["paired_results"])
    digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    assert result["library_snapshot"]["sha256"] == digest
    assert result["library_snapshot"]["cold_loaded"] is True
    assert result["library_snapshot"]["same_snapshot_for_both_views"] is True
    assert all(row["library_snapshot_sha256"] == digest and row["cold_loaded_library"]
               for row in result["paired_results"])


def test_formcraft_final_pairs_really_use_cold_loaded_object(tmp_path, monkeypatch):
    import auto_research.agent_research.formcraft as module
    original_load = Library.load
    original_compose = module.compose_from_examples
    restored, paired_libraries = [], []

    def tracking_load(cls, path):
        instance = original_load(path)
        restored.append(instance)
        return instance

    def tracking_compose(library, *args, **kwargs):
        if restored:
            paired_libraries.append(library)
            assert library is restored[0]
        return original_compose(library, *args, **kwargs)

    monkeypatch.setattr(Library, "load", classmethod(tracking_load))
    monkeypatch.setattr(module, "compose_from_examples", tracking_compose)
    result = run_sequence_study(snapshot_path=tmp_path / "library.json", goals=4, holdout_count=8)
    assert len(restored) == 1 and len(paired_libraries) == 8
    assert result["metrics"]["all_paired_holdouts_pass"]


def test_formcraft_snapshot_cannot_be_silently_overwritten(tmp_path):
    snapshot = tmp_path / "library.json"
    run_sequence_study(snapshot_path=snapshot, goals=3, holdout_count=8)
    before = snapshot.read_bytes()
    with pytest.raises(FileExistsError, match="immutable"):
        run_sequence_study(snapshot_path=snapshot, goals=3, holdout_count=8)
    assert snapshot.read_bytes() == before
    with pytest.raises(FileExistsError):
        Library().save(snapshot)
    assert snapshot.read_bytes() == before


def _formcraft_runner():
    path = Path(__file__).resolve().parents[2] / "scripts/run_formcraft.py"
    spec = importlib.util.spec_from_file_location("formcraft_runner", path)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    return runner


def test_formcraft_runner_real_adjacent_snapshots_and_no_overwrite(tmp_path):
    runner = _formcraft_runner()
    output = tmp_path / "study.json"
    result = runner.run(seeds=[42], output=output)
    assert result["status"] == "completed"
    snapshot = output.parent / result["reports"][0]["library_snapshot"]["path"]
    assert snapshot == tmp_path / "study.libraries/seed42.json" and snapshot.is_file()
    assert Library.load(snapshot).records
    before = output.read_bytes(), snapshot.read_bytes()
    with pytest.raises(FileExistsError, match="immutable"):
        runner.run(seeds=[42], output=output)
    assert (output.read_bytes(), snapshot.read_bytes()) == before
    output.unlink()  # A missing result must not authorize overwriting snapshots.
    with pytest.raises(FileExistsError, match="immutable"):
        runner.run(seeds=[42], output=output)
    assert not output.exists() and snapshot.read_bytes() == before[1]


def test_formcraft_cold_load_failure_retains_attempt_and_snapshot(tmp_path, monkeypatch):
    runner = _formcraft_runner()
    output = tmp_path / "failed-study.json"

    def failed_load(cls, path):
        assert path.is_file()
        raise ValueError("injected cold-load validation failure")

    monkeypatch.setattr(Library, "load", classmethod(failed_load))
    with pytest.raises(ValueError, match="cold-load"):
        runner.run(seeds=[42, 43], output=output)
    failure = json.loads(output.read_text())
    assert failure["status"] == "failed" and failure["reports"] == []
    assert failure["failure"]["error_type"] == "ValueError"
    snapshot = tmp_path / "failed-study.libraries/seed42.json"
    assert snapshot.is_file() and json.loads(snapshot.read_text())["records"]
    with pytest.raises(FileExistsError):
        runner.run(seeds=[42, 43], output=output)


def test_formcraft_committed_results_bind_actual_cold_loaded_snapshots():
    page = Path(__file__).resolve().parents[2] / "docs/agent-research/2610.19414-formcraft"
    metric_path = page / "metrics/sequence-cpu-seeds42-44.json"
    metrics = json.loads(metric_path.read_text())
    raw_path = page / "validation/persistent-cpu-v2/result.json"
    assert hashlib.sha256(raw_path.read_bytes()).hexdigest() == metrics["provenance"]["raw_artifact_sha256"]
    raw = json.loads(raw_path.read_text())
    assert raw["status"] == "completed"
    assert [row["seed"] for row in raw["reports"]] == [42, 43, 44]
    for stable, report in zip(metrics["per_seed_results"], raw["reports"], strict=True):
        snapshot = raw_path.parent / report["library_snapshot"]["path"]
        assert not Path(report["library_snapshot"]["path"]).is_absolute()
        assert snapshot.resolve() == (metric_path.parent / stable["library_snapshot"]["path"]).resolve()
        digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        assert digest == report["library_snapshot"]["sha256"] == stable["library_snapshot"]["sha256"]
        assert len(Library.load(snapshot).records) == report["metrics"]["library_records"] == 13
        assert all(stable[key] == value for key, value in report["metrics"].items())
        assert len(report["paired_results"]) == 24
        assert all(row["cold_loaded_library"] and row["library_snapshot_sha256"] == digest
                   for row in report["paired_results"])
    assert metrics["prior_protocol"]["counts_unchanged_in_persistent_v2"]


@pytest.mark.parametrize("identity,key", [("2610.20116", "transparent-compact"),
                                         ("2610.19414", "formcraft")])
def test_cpu_component_documentation_and_catalog_contract(identity, key):
    root = Path(__file__).resolve().parents[2]
    page = root / "docs" / "agent-research" / f"{identity}-{key}"
    text = (page / "README.md").read_text()
    for field in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "本地 Adapter", "本地复现代码"):
        assert f"| {field} |" in text
    assert (page / "assets" / "paper-figure-01.png").stat().st_size > 1000
    spec = json.loads((root / "src" / "auto_research" / "paper_specs" / "catalog" /
                       "agent-research" / f"{key}.json").read_text())
    assert spec["adapter"] is None
    assert spec["promotion_eligible"] is False
    assert spec["requires_gpu_validation"] is False
    for artifact in (page / "metrics").glob("*.json"):
        metrics = json.loads(artifact.read_text())
        assert metrics["schema_version"] == 2 and metrics["diagnostic_only"]
        assert not metrics["evaluation_protocol"]["formal_comparison"]


def test_transparent_public_validation_receipt_binds_fixed_source_and_metadata_checks():
    root = Path(__file__).resolve().parents[2]
    path = root / "docs/agent-research/2610.20116-transparent-compact/validation/public-session-cpu.json"
    receipt = json.loads(path.read_text())
    assert receipt["metrics"]["output_characters"] == 138550
    assert receipt["metrics"]["model_calls"] == 0 and not receipt["promotion_eligible"]
    assert receipt["metadata_checks"]["first_compaction_checked_fields"] == 208
    assert receipt["metadata_checks"]["recompaction_checked_fields"] == 208
    assert receipt["metadata_checks"]["all_preserved"]
    assert receipt["metadata_checks"]["recompaction_messages_equal"]
    assert receipt["before_fix_history"][0]["output_characters"] == 129010
    assert not receipt["before_fix_history"][0]["valid_for_final_acceptance"]
    for relative, expected in receipt["provenance"]["executed_source_sha256"].items():
        assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected
    assert not (path.parent.parent / "metrics/public-session-cpu.json").exists()
