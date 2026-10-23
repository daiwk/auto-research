import hashlib
import json
from pathlib import Path
import statistics

import pytest

from auto_research.agent_research.physical_engineering_exam import (
    DATASET_REVISION, DEV_MANIFEST_SOURCE_SHA256, UPSTREAM_REVISION,
    FileEntry, aggregate_three_runs, audit_artifacts, design_item_score,
    dev_set_digest, dev_tasks, diagnostic, git_blob_id, harness_digest,
    reproduction_check, rubric_score,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT/"tests/fixtures/physical_engineering_exam/dev_set.json"
DOC = ROOT/"docs/agent-research/2610.30537-physical-engineering-exam/README.md"


def setup():
    data = {"tasks": [{"id": "design", "deliverables": ["/out/"], "grading": "checks", "final_message": False},
                       {"id": "memo", "deliverables": ["/out/"], "grading": "rubric", "final_message": True}]}
    entry = FileEntry("artifacts/design/files/out/x.csv", b"x,y\n1,2\n")
    harness = harness_digest([FileEntry("serve.py", b"server, never executed")])
    manifest = {"format": 1, "dev_set": dev_set_digest(data), "harness": {"tree": harness},
                "tasks": {"design": {"files": {"out/x.csv": git_blob_id(entry.data)}, "reward": 1.0}}}
    return data, entry, harness, manifest


def audit(entries=None, manifest_override=False):
    data, entry, harness, manifest = setup()
    return audit_artifacts(dev_tasks(data), entries if entries is not None else [entry],
                           manifest=manifest if manifest_override is False else manifest_override,
                           expected_dev_digest=dev_set_digest(data), expected_harness_digest=harness)


def test_paper_equations_preserve_hard_constraint_gate_and_naive_baseline():
    assert design_item_score([True, True], [True, False], 0.75, 0.5) == pytest.approx(0.7)
    assert design_item_score([False, True], [True, False], 1) == pytest.approx(0.2)
    assert design_item_score([True, True], [True, False], 0.25, 0.5) == pytest.approx(0.4)
    assert design_item_score([True, True], [True, False], 1, 0.9) == 1
    assert rubric_score([True, False], [10, 1]) == pytest.approx(10/11)
    assert rubric_score([True, False], [1e308, 1e308]) == 0.5
    assert rubric_score([True, True], [1e308, 1e308]) == 1.0
    with pytest.raises(ValueError):
        design_item_score([True], [True], 1, 1)
    with pytest.raises(ValueError):
        design_item_score([1], [True], 1)


def test_official29_task_manifest_and_dataset_identity_are_frozen():
    fixture = json.loads(FIXTURE.read_text())
    assert fixture["upstream_revision"] == UPSTREAM_REVISION
    assert fixture["source_sha256"] == DEV_MANIFEST_SOURCE_SHA256
    data = fixture["dev_set_data"]
    assert data["tasks_revision"] == DATASET_REVISION
    assert len(dev_tasks(data)) == 29
    assert dev_set_digest(data) == fixture["canonical_digest"] == "d9d0e20eccffc8b105f34ae46b50bb4bb7bdc5ab35402d453bcd644bcde4cbfb"
    # Hash depends on parsed data rather than object insertion order or YAML comments.
    assert dev_set_digest(dict(reversed(list(data.items())))) == dev_set_digest(data)
    mutated = json.loads(json.dumps(data))
    mutated["tasks"][0]["sha256"] = "0"*64
    assert dev_set_digest(mutated) != dev_set_digest(data)


def test_blob_and_harness_hashes_include_mode_ignore_artifacts_and_env():
    assert git_blob_id(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
    a = FileEntry("serve.py", b"print(1)")
    expected = hashlib.sha256(f"100644 {git_blob_id(a.data)} serve.py\n".encode()).hexdigest()
    assert harness_digest([a]) == expected
    assert harness_digest([a, FileEntry(".env", b"not a real key"), FileEntry("artifacts/a", b"x"),
                           FileEntry("dev_artifacts/a", b"x"), FileEntry("runs/old/artifacts/a", b"x")]) == expected
    assert harness_digest([FileEntry(a.path, a.data, "100755")]) != expected
    with pytest.raises(ValueError):
        harness_digest([a, a])


def test_valid_artifact_provenance_never_scores_claimed_reward():
    result = audit()
    assert not result["refused"] and result["tasks"]["design"]["usable"]
    assert not result["tasks"]["memo"]["usable"]
    assert result["provenance"] == {"manifest": "ok", "dev_set": "same", "harness": "same", "edited_tasks": []}
    assert not result["grades_computed"]
    assert "score" not in result["tasks"]["design"]


def test_missing_or_stale_manifest_warns_not_refuses_usable_deliverables():
    assert not audit(manifest_override=None)["refused"]
    assert audit(manifest_override=None)["provenance"]["manifest"] == "missing"
    _, entry, _, manifest = setup()
    manifest["dev_set"] = "stale"
    manifest["harness"]["tree"] = "stale"
    manifest["tasks"]["design"]["files"]["out/x.csv"] = "0"*40
    result = audit([entry], manifest)
    assert not result["refused"]
    assert result["provenance"]["dev_set"] == "other"
    assert result["provenance"]["harness"] == "changed"
    assert result["provenance"]["edited_tasks"] == ["design"]


@pytest.mark.parametrize("path,mode,data", [
    ("artifacts/design/files/out/../x", "100644", b"x"),
    ("artifacts/design/files/out/x", "120000", b"/etc/passwd"),
    ("artifacts/design/files/out/x", "160000", b"gitlink"),
    ("artifacts/design/files/out/x", "100644", b"version https://git-lfs.github.com/spec/v1\n"),
    ("artifacts/design/files/out/a\\b", "100644", b"x"),
    ("artifacts/design/files/out/a\0b", "100644", b"x"),
    ("artifacts/design/files/out/"+"a"*256, "100644", b"x"),
])
def test_invalid_task_artifacts_are_unusable(path, mode, data):
    result = audit([FileEntry(path, data, mode)])
    assert result["refused"] and not result["tasks"]["design"]["usable"]


def test_file_and_folder_case_collisions_and_file_directory_overlap():
    for names in (("out/x", "out/X"), ("out/A/x", "out/a/y"), ("out/a", "out/a/y")):
        result = audit([FileEntry("artifacts/design/files/"+name, b"x") for name in names])
        assert not result["tasks"]["design"]["usable"]


def test_final_message_permissions_and_metadata_ignore():
    result = audit([FileEntry("artifacts/design/final_message.md", b"report"),
                    FileEntry("artifacts/memo/final_message.md", b"report")])
    assert not result["tasks"]["design"]["usable"]
    assert result["tasks"]["memo"]["usable"]
    result = audit([FileEntry("artifacts/design/files/out/.gitignore", b"secret"),
                    FileEntry("artifacts/design/trajectory.json", b"[]")])
    assert result["refused"]
    assert not result["tasks"]["design"]["files"]


def test_three_runs_use_full_denominator_and_missing_zero():
    result = aggregate_three_runs(["a", "b"], [{"a": 1}, {"b": 1}, {}])
    assert result["run_means"] == [0.5, 0.5, 0]
    assert result["mean"] == pytest.approx(1/3)
    assert result["population_std"] == statistics.pstdev([0.5, 0.5, 0])
    assert result["sample_std"] == statistics.stdev([0.5, 0.5, 0])
    assert result["missing_tasks_per_run"] == [["b"], ["a"], ["a", "b"]]
    for bad in ([{}, {}], [{"unknown": 1}, {}, {}], [{"a": float("nan")}, {}, {}], [{"a": True}, {}, {}]):
        with pytest.raises(ValueError):
            aggregate_three_runs(["a", "b"], bad)


def test_reproduction_flag_is_strict_and_not_disqualification():
    assert not reproduction_check([0.5], [0.25])["flag_for_human_review"]
    result = reproduction_check([0.6], [0.25])
    assert result["flag_for_human_review"] and not result["automatic_disqualification"]


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic_standard_types_and_no_capability_claim(seed):
    result = diagnostic(seed)
    assert all(value is True for value in result["checks"].values())
    assert result["diagnostic_only"] and not result["promotion_eligible"]
    assert not result["requires_gpu_validation"] and not result["evolve_integrated"]
    assert result["metrics"]["model_calls"] == result["metrics"]["external_commands"] == 0


def test_complete_metadata_and_scope_documentation():
    text = DOC.read_text()
    for required in ("论文信息", "https://arxiv.org/abs/2610.30537v1", "Rujun Han", "Google Cloud AI Research",
                     "2026-10-21 23:45:56 UTC", UPSTREAM_REVISION, "Apache-2.0", "CC BY 4.0",
                     "adapter: null", "src/auto_research/agent_research/physical_engineering_exam.py",
                     "原始论文总结", "核心公式", "本地复现", "未报告生产线上 A/B",
                     "不执行", "paper-figure-01.png", "成本过高，不复现（审查 DONE）", "56"):
        assert required in text
