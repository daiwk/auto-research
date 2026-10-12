"""Preparation/isolation diagnostics; fixtures are not capability evidence."""
import csv
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/prepare_oct12_agent_inputs.py"
spec = importlib.util.spec_from_file_location("oct12_agent_input_preparation", SCRIPT)
prep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep)


def write_csv(path, fields, rows, *, bom=False):
    with path.open("w", encoding="utf-8-sig" if bom else "utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def pin_fixture(monkeypatch, source, paths):
    """Unit-only replacement: production CLI has no raw-hash override."""
    replacement = dict(prep.SOURCE_SPECS[source])
    replacement["sha256"] = {name: prep.sha256_file(path) for name, path in paths.items()}
    monkeypatch.setitem(prep.SOURCE_SPECS, source, replacement)


def memory_rows():
    return [{"question_id": str(i), "question": f"query {i}", "answer": f"gold {i}",
             "haystack_sessions": [[{"role": "user", "content": "完整历史" * 40000,
                                     "timestamp": "2025-01-01"}],
                                    [{"role": "assistant", "content": f"history {i}"}]]}
            for i in range(3)]


def rated_raw(tmp_path):
    catalog = tmp_path / "tools_clean_with_reliability.csv"
    training = tmp_path / "train_pairs.csv"
    evaluation = tmp_path / "eval_real_test.jsonl"
    write_csv(catalog, ["uid", "tool_text", "reliability_score"], [
        {"uid": "a", "tool_text": "tool A" * 30000, "reliability_score": "0.8"},
        {"uid": "b", "tool_text": "tool B", "reliability_score": "0.7"},
        {"uid": "test-only", "tool_text": "held-out tool", "reliability_score": "1.0"},
    ], bom=True)
    write_csv(training, ["query", "tool_uid", "label"], [
        {"query": "train A", "tool_uid": "a", "label": "1"},
        {"query": "duplicate UID A", "tool_uid": "a", "label": "1"},
        {"query": "negative", "tool_uid": "test-only", "label": "0"},
        {"query": "missing", "tool_uid": "unknown", "label": "1"},
        {"query": "train B", "tool_uid": "b", "label": "1"},
    ], bom=True)
    rows = [{"query": "train A", "ground_truth": ["test-only"]},
            {"query": "held-out first", "ground_truth": ["test-only"]},
            {"query": "train B", "ground_truth": ["a"]},
            {"query": "held-out second", "ground_truth": ["b"]}]
    evaluation.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return {path.name: path for path in (catalog, training, evaluation)}


def test_official_pins_urls_and_cli_defaults_are_fixed():
    assert prep.LONGMEM_REVISION == "98d7416c24c778c2fee6e6f3006e7a073259d48f"
    assert prep.ECO_REVISION == "bc5db40a20b254c5249401d2220ea71b06c86a5c"
    for source in prep.SOURCE_SPECS.values():
        assert all(len(digest) == 64 for digest in source["sha256"].values())
        assert all(source["revision"] in url for url in source["fixed_urls"].values())
    args = prep.build_parser().parse_args([
        "--source", "rated", "--raw-dir", "raw", "--output", "new-output"])
    assert (args.memory_queries, args.pool_tools, args.test_queries) == (2, 32, 8)
    assert "test" not in inspect.signature(prep.select_training_pool).parameters
    assert "ground_truth" not in inspect.getsource(prep.select_training_pool)


def test_full_memory_sessions_and_order_survive_without_gold_selection():
    rows = memory_rows()
    converted = prep.convert_memory_rows(rows)
    assert [row["question_id"] for row in converted] == ["0", "1"]
    assert all(row["sessions"] == original["haystack_sessions"]
               for row, original in zip(converted, rows))
    assert converted[0]["sessions"][0][0]["content"].endswith("完整历史")
    altered = [{**row, "answer": "arbitrary unrelated external gold"} for row in rows]
    changed = prep.convert_memory_rows(altered)
    assert [{key: value for key, value in row.items() if key != "answer"} for row in changed] == [
        {key: value for key, value in row.items() if key != "answer"} for row in converted]


def test_memory_export_is_canonical_utf8_and_manifest_has_source_hash(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    nested = raw_dir / "longmemeval"
    nested.mkdir(parents=True)
    raw_file = nested / "longmemeval_s_cleaned.json"
    rows = memory_rows()
    raw_file.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8-sig")
    pin_fixture(monkeypatch, "t2mem", {raw_file.name: raw_file})
    output = tmp_path / "output"
    manifest = prep.prepare_inputs("t2mem", raw_dir, output)
    expected = "".join(json.dumps(row, ensure_ascii=False) + "\n"
                       for row in prep.convert_memory_rows(rows)).encode("utf-8")
    exported = output / "t2mem-first2.jsonl"
    assert exported.read_bytes() == expected
    assert manifest["files"][exported.name] == hashlib.sha256(expected).hexdigest()
    assert manifest["upstream_sha256"] == prep.sha256_file(raw_file)
    assert manifest["downloads_performed"] is False
    assert "external" in manifest["gold_boundary"]
    assert json.loads((output / "provenance.json").read_text()) == manifest


def test_bom_long_csv_fields_restore_limit_and_one_pair_per_positive_uid(tmp_path):
    paths = rated_raw(tmp_path)
    old_limit = csv.field_size_limit()
    payload = prep.convert_rated_files(paths, pool_tools=2, test_queries=2)
    assert csv.field_size_limit() == old_limit
    assert list(payload["tools"]) == ["a", "b"]
    assert len(payload["tools"]["a"]["text"]) > 128 * 1024
    assert len(payload["pairs"]) == len(payload["tools"]) == 2
    assert [row["query"] for row in payload["pairs"]] == ["train A", "train B"]
    assert [row["query"] for row in payload["queries"]] == [
        "held-out first", "held-out second"]
    assert {row["query"] for row in payload["pairs"]}.isdisjoint(
        row["query"] for row in payload["queries"])
    assert "test-only" not in payload["tools"]


def test_test_gold_does_not_select_pool_or_change_selected_query_order(tmp_path):
    paths = rated_raw(tmp_path)
    before = prep.convert_rated_files(paths, 2, 2)
    evaluation = paths["eval_real_test.jsonl"]
    altered = [json.loads(line) for line in evaluation.read_text().splitlines()]
    for row in altered:
        row["ground_truth"] = ["a", "b", "invented test-only UID"]
    evaluation.write_text("".join(json.dumps(row) + "\n" for row in altered))
    after = prep.convert_rated_files(paths, 2, 2)
    assert before["tools"] == after["tools"]
    assert before["pairs"] == after["pairs"]
    assert [row["query"] for row in before["queries"]] == [
        row["query"] for row in after["queries"]]
    class ForbiddenGold(dict):
        def __getitem__(self, key):
            if key == "ground_truth":
                raise AssertionError("excluded training-query gold was accessed")
            return super().__getitem__(key)
    rows = [ForbiddenGold(query="overlap"), {"query": "test", "ground_truth": ["outside"]}]
    assert prep.select_test_queries(rows, {"overlap"}, 1)[0]["query"] == "test"


def test_rated_export_preserves_root_format_but_marks_backend_diagnostic(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    raw.mkdir()
    paths = rated_raw(raw)
    pin_fixture(monkeypatch, "rated", paths)
    output = tmp_path / "export"
    manifest = prep.prepare_inputs("rated", raw, output, pool_tools=2, test_queries=2)
    expected = (json.dumps(prep.convert_rated_files(paths, 2, 2), ensure_ascii=False,
                           indent=2) + "\n").encode("utf-8")
    assert (output / "rated-train2-test2.json").read_bytes() == expected
    assert manifest["files"]["rated-train2-test2.json"] == hashlib.sha256(expected).hexdigest()
    assert manifest["evidence_level"] == "diagnostic"
    assert manifest["tool_execution_status"] == "unbound_fail_closed"
    assert manifest["real_tool_execution_validated"] is False
    with pytest.raises(RuntimeError, match="no semantic tool success claimed"):
        exec(prep.UNAVAILABLE_TOOL_CODE, {})


def test_bad_upstream_hash_cannot_be_blessed_by_local_provenance(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    path = raw / "longmemeval_s_cleaned.json"
    path.write_text(json.dumps(memory_rows()))
    (raw / "provenance.json").write_text(json.dumps({
        "public_id": "xiaowu0162/longmemeval-cleaned", "revision": prep.LONGMEM_REVISION,
        "upstream_sha256": prep.sha256_file(path)}))
    output = tmp_path / "output"
    with pytest.raises(ValueError, match="official upstream SHA256 mismatch"):
        prep.prepare_inputs("t2mem", raw, output)
    assert not output.exists()


@pytest.mark.parametrize("source", ["rated", "t2mem"])
def test_cli_rejects_unverified_raw_without_downloading_or_emitting_success(tmp_path, source):
    result = subprocess.run([sys.executable, str(SCRIPT), "--source", source,
                             "--raw-dir", str(tmp_path), "--output", str(tmp_path / "out")],
                            text=True, capture_output=True, timeout=10)
    assert result.returncode != 0 and result.stdout == ""
    assert "required offline raw file is missing" in result.stderr
    assert not (tmp_path / "out").exists()


def test_budget_shortfall_bad_header_and_existing_output_fail_closed(tmp_path):
    with pytest.raises(ValueError, match="positive"):
        prep.convert_memory_rows([], 0)
    with pytest.raises(ValueError, match="insufficient official memory"):
        prep.convert_memory_rows([], 1)
    with pytest.raises(ValueError, match="unique training-positive"):
        prep.select_training_pool({}, [], 1)
    with pytest.raises(ValueError, match="train-disjoint"):
        prep.select_test_queries([], set(), 1)
    malformed = tmp_path / "bad.csv"
    malformed.write_text("wrong,header\n1,2\n")
    old_limit = csv.field_size_limit()
    with pytest.raises(ValueError, match="required CSV columns"):
        with prep.csv_rows(malformed, {"uid"}):
            pass
    assert csv.field_size_limit() == old_limit
    output = tmp_path / "existing"
    output.mkdir()
    with pytest.raises(FileExistsError, match="fresh output"):
        prep.prepare_inputs("t2mem", tmp_path, output)
