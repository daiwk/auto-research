"""Real bounded online generation and parameter updates, never a score fixture."""
import argparse
import hashlib
from pathlib import Path
import runpy

import pytest
import torch


ROOT = Path(__file__).resolve().parents[2]


def test_six_components_run_actual_policy_steps_and_keep_frozen_roles(tmp_path):
    runner = runpy.run_path(str(ROOT / "scripts/run_oct16_post_components.py"))
    payload = b"Explicit unit-test text fixture. This is not a public language benchmark.\n" * 160
    corpus = tmp_path / "fixture.txt"
    corpus.write_bytes(payload)
    output = tmp_path / "result.json"
    args = argparse.Namespace(corpus_path=corpus, corpus_id="explicit-test-fixture",
        corpus_revision="fixture-v1", corpus_sha256=hashlib.sha256(payload).hexdigest(),
        output=output, device="cpu", seeds="42", methods="all", steps=2, teacher_steps=2, max_tokens=8)
    threads = torch.get_num_threads()
    try:
        torch.set_num_threads(1)
        result = runner["run"](args)
    finally:
        torch.set_num_threads(threads)
    assert result["diagnostic_only"] and not result["promotion_eligible"]
    assert not result["evolve_integrated"] and len(result["results"]) == 6
    for key, outcomes in result["results"].items():
        row = outcomes[0]
        assert row["parameter_delta_l2"] > 0, key
        assert row["frozen_teacher_parameter_deltas_l2"] == [0., 0.]
        assert row["frozen_rl_snapshot_parameter_deltas_l2"] == [0., 0., 0.]
        if key != "tf-opd":
            assert row["generated_tokens"] >= 8 and len(row["history"]) == 2
            assert all(h["gradient_norm"] > 0 for h in row["history"])
    assert result["results"]["ggpo"][0]["reference_refreshes"] == 1
    assert result["results"]["stopd"][0]["history"][1]["normalizer_source"] == "previous_batch"
    assert all(h["paper_default_eligible_responses"] == 0 for h in result["results"]["sif"][0]["history"])
    assert "mathematical-premise" in result["results"]["cce-opd"][0]["condition_pair_source"]
    original = output.read_bytes()
    with pytest.raises(FileExistsError):
        runner["run"](args)
    assert output.read_bytes() == original


def test_runner_rejects_false_corpus_hash_and_excess_budget_before_training(tmp_path):
    runner = runpy.run_path(str(ROOT / "scripts/run_oct16_post_components.py"))
    corpus = tmp_path / "fixture.txt"
    corpus.write_bytes(b"Explicit fixture\n" * 300)
    args = argparse.Namespace(corpus_path=corpus, corpus_id="fixture", corpus_revision="v1",
        corpus_sha256="wrong", output=tmp_path / "out.json", device="cpu", seeds="42",
        methods="ggpo", steps=2, teacher_steps=1, max_tokens=8)
    with pytest.raises(ValueError, match="immutable content hash"):
        runner["run"](args)
    args.steps = 100
    with pytest.raises(ValueError, match="bounded diagnostic"):
        runner["run"](args)


def test_runner_rejects_oversized_corpus_before_any_content_read(tmp_path, monkeypatch):
    runner = runpy.run_path(str(ROOT / "scripts/run_oct16_post_components.py"))
    corpus = tmp_path / "too-large.txt"
    with corpus.open("wb") as handle:
        handle.truncate(2_000_001)
    args = argparse.Namespace(corpus_path=corpus, corpus_id="fixture", corpus_revision="v1",
        corpus_sha256=None, output=tmp_path / "out.json", device="cpu", seeds="42",
        methods="ggpo", steps=2, teacher_steps=1, max_tokens=8)
    reads = []
    original_open = Path.open

    def tracked_open(path, *arguments, **keywords):
        if path == corpus:
            reads.append(path)
            raise AssertionError("oversized input must not be opened for reading")
        return original_open(path, *arguments, **keywords)

    def forbidden_read_bytes(path):
        if path == corpus:
            reads.append(path)
        raise AssertionError("no unbounded read_bytes path is allowed")

    monkeypatch.setattr(Path, "open", tracked_open)
    monkeypatch.setattr(Path, "read_bytes", forbidden_read_bytes)
    with pytest.raises(ValueError, match="4KB..2MB"):
        runner["run"](args)
    assert not reads and not args.output.exists()
