from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import tarfile

import pytest


def module():
    path = Path(__file__).resolve().parents[1] / "scripts/curate_oct14_skilldreamer.py"
    spec = importlib.util.spec_from_file_location("skill_curation", path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def fixture_runs(root, curator):
    root.mkdir()
    for seed in curator.SEEDS:
        run = {"paper": "skilldreamer", "seed": seed, "device": "cuda",
            "diagnostic_only": True, "promotion_eligible": False,
            "variants": {arm: {"pass_rate": 0.0, "model_calls": 2, "executed_actions": 1}
                         for arm in curator.ARMS},
            "episodes": {arm: [{"correct": False, "capability_checks": [], "generation_errors": 1}]
                         for arm in curator.ARMS},
            "protocol": {"gold_visible_to_policy": False, "test_ids": ["0"],
                "dataset": {"public_id": "fixture", "revision": "a" * 40,
                    "source_split": "train", "official_test_opened": False},
                "checkpoint": {"public_id": "fixture-generator", "revision": "b" * 40},
                "encoder": {"public_id": "fixture-encoder", "revision": "c" * 40}}}
        (root / f"seed{seed}.json").write_text(json.dumps(run))


@pytest.mark.parametrize("field,value", [("gold_visible_to_policy", True),
                                         ("official_test_opened", True), ("source_split", "test")])
def test_skill_curation_rejects_gold_or_official_test_before_writing(tmp_path, monkeypatch, field, value):
    curator = module()
    monkeypatch.setattr(curator, "ROOT", tmp_path / "output")
    runs = tmp_path / "runs"
    fixture_runs(runs, curator)
    path = runs / "seed42.json"
    run = json.loads(path.read_text())
    target = run["protocol"] if field == "gold_visible_to_policy" else run["protocol"]["dataset"]
    target[field] = value
    path.write_text(json.dumps(run))
    with pytest.raises(ValueError):
        curator.curate(runs, "a" * 40, tmp_path / "absent.tar")
    assert not (tmp_path / "output").exists()


def test_skill_curation_retains_failed_episodes_and_binds_raw_source_hashes(tmp_path, monkeypatch):
    curator = module()
    monkeypatch.setattr(curator, "ROOT", tmp_path / "output")
    runs = tmp_path / "runs"
    fixture_runs(runs, curator)
    paths = ["scripts/run_skilldreamer.py", "src/auto_research/reproductions/skilldreamer/experiment.py",
        "src/auto_research/reproductions/skilldreamer/algorithm.py",
        "src/auto_research/reproductions/skilldreamer/gallery.json",
        "src/auto_research/reproductions/near/data.py", "src/auto_research/reproductions/near/experiment.py",
        "src/auto_research/reproductions/state_opd/environment.py"]
    archive_path = tmp_path / "source.tar"
    with tarfile.open(archive_path, "w") as archive:
        for path in paths:
            content = ("source fixture: " + path).encode()
            info = tarfile.TarInfo(path)
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))
    monkeypatch.setattr(curator.subprocess, "check_output",
                        lambda command, **kwargs: ("source fixture: " + command[-1].split(":", 1)[1]).encode())
    summary = curator.curate(runs, "a" * 40, archive_path)
    assert summary["checks"]["all_generation_failures_retained"] is True
    receipt = json.loads((tmp_path / "output/docs/gpu-validations/oct13-skilldreamer-a30.json").read_text())
    assert len(receipt["executed_source_sha256"]) == 7
    assert receipt["metrics"]["skilldreamer.pass_rate"]["mean"] == 0
    raw = json.loads((tmp_path / "output" / curator.DOC / "raw/seed42.json").read_text())
    assert raw["episodes"]["skilldreamer"][0]["generation_errors"] == 1
    assert raw["episodes"]["skilldreamer"][0]["correct"] is False
    with pytest.raises(FileExistsError):
        curator.curate(runs, "a" * 40, archive_path)
