"""Synthetic evidence fixtures; no local GPU logs are a CI dependency."""
from hashlib import sha256
import importlib.util
import io
import json
from pathlib import Path
import tarfile

import pytest

SPEC = importlib.util.spec_from_file_location(
    "replay_curation", Path(__file__).resolve().parents[1] / "scripts/curate_oct14_replayssm.py")
curation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(curation)


@pytest.fixture
def evidence(tmp_path, monkeypatch):
    source = b"synthetic source fixture\n"
    hashes = {name: sha256(source).hexdigest() for name in curation.SOURCE_HASHES}
    archive = tmp_path / "source.tar"
    with tarfile.open(archive, "w") as bundle:
        for name in hashes:
            member = tarfile.TarInfo(name)
            member.size = len(source)
            bundle.addfile(member, io.BytesIO(source))
    monkeypatch.setattr(curation, "SOURCE_HASHES", hashes)
    monkeypatch.setattr(curation, "ARCHIVE_SHA256", sha256(archive.read_bytes()).hexdigest())
    raw = tmp_path / "raw"
    raw.mkdir()
    for seed in (42, 43, 44):
        stem = f"replayssm-seed{seed}"
        report = {
            "seed": seed, "diagnostic_only": True, "promotion_eligible": False,
            "dataset_revision": "replayssm-random-input-protocol-v2-gdn-rollback",
            "reference": {"accepted_tokens": 12, "max_output_error": 1e-7,
                          "native_bandwidth_speedup_claim": False},
            "reference_gdn": {"accepted_tokens": 12, "max_output_error": 1e-7,
                              "max_committed_state_error": 1e-8,
                              "read_precision_output_max_difference": 1e-4,
                              "high_anchor_read_precision_max_difference": 0.,
                              "acceptance_counts": [0, 1, 2, 3, 0, 1, 2, 3],
                              "checkpoint_refreshes": [3, 3], "native_bandwidth_speedup_claim": False},
            "author_triton": {"upstream_revision": curation.UPSTREAM, "steps": 48,
                              "accelerator": "NVIDIA A100-SXM4-80GB", "storage_format": "dequantized FP32",
                              "native_bandwidth_speedup_claim": False,
                              "upstream_source_files_sha256": {"gdn_replay_unf_vf.py": curation.GDN_FILE},
                              "jit_source_compatibility": {
                                  "original_jit_source_sha256": curation.ORIGINAL_JIT,
                                  "compiled_jit_source_sha256": curation.COMPILED_JIT,
                                  "original_author_file_sha256": curation.GDN_FILE,
                                  "function": "_gdn_unf_vf_step_kernel",
                                  "source_ranges_relative_to_jit_function": [{
                                      "line": 122, "column": 7, "end_line": 122, "end_column": 51,
                                      "operator": "and", "operands": 3}],
                                  "associative_boolean_ast_equivalent": True,
                                  "author_file_modified": False, "native_serving_claim": False},
                              "metrics": {}},
        }
        for arch in ("mamba2", "gdn"):
            report["author_triton"]["metrics"][arch + "/independent_read_cast_passed"] = True
            for mode in ("s32_rs", "tp8_hi32", "tp4_hi16_sr", "f4_sr_rs"):
                for metric in ("output_rmse", "anchor_rmse"):
                    report["author_triton"]["metrics"][f"{arch}/{mode}/{metric}"] = 0.
        status = {"commit": curation.COMMIT, "actual_source_files_sha256": hashes,
                  "returncode": 0, "output_exists": True, "failure": None,
                  "accelerator": "NVIDIA A100-SXM4-80GB", "elapsed_seconds": 1.,
                  "finished_at": "2026-10-13T17:50:33Z",
                  "command": ["python", "scripts/run_replayssm.py", "--upstream", "fixture",
                              "--steps", "48", "--seed", str(seed), "--output", "fixture"]}
        (raw / (stem + ".json")).write_text(json.dumps(report))
        (raw / (stem + ".status.json")).write_text(json.dumps(status))
        (raw / (stem + ".stdout.log")).write_text("fixture\n")
        (raw / (stem + ".stderr.log")).write_text("")
    return raw, archive


def test_curates_pinned_three_seeds_and_no_serving_claim(evidence):
    result = curation.curate(*evidence)
    assert len(result["raw_files_sha256"]) == 12
    assert result["aggregate"]["gdn_high_anchor_read_precision_max_difference"]["mean"] == 0
    assert len(result["commands"]) == 3


@pytest.mark.parametrize("mutation", ["steps", "source", "failed", "jit", "nan", "serving"])
def test_rejects_wrong_or_failed_evidence(evidence, mutation):
    raw, archive = evidence
    status_path = raw / "replayssm-seed42.status.json"
    result_path = raw / "replayssm-seed42.json"
    status, result = json.loads(status_path.read_text()), json.loads(result_path.read_text())
    if mutation == "steps":
        status["command"][status["command"].index("--steps") + 1] = "49"
    elif mutation == "source":
        status["actual_source_files_sha256"]["scripts/run_replayssm.py"] = "0" * 64
    elif mutation == "failed":
        status["returncode"] = 1
    elif mutation == "jit":
        result["author_triton"]["jit_source_compatibility"]["compiled_jit_source_sha256"] = "0" * 64
    elif mutation == "nan":
        result["author_triton"]["metrics"]["gdn/tp8_hi32/output_rmse"] = float("nan")
    else:
        result["author_triton"]["native_bandwidth_speedup_claim"] = True
    status_path.write_text(json.dumps(status))
    result_path.write_text(json.dumps(result))
    with pytest.raises(AssertionError):
        curation.curate(raw, archive)
