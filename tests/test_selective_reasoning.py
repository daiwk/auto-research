from __future__ import annotations

import hashlib
import io
from pathlib import Path
from types import MappingProxyType
import zipfile

import pytest

from auto_research.system_one import selective_reasoning as s


def test_release_identity_is_immutable_and_model_downloads_absent():
    assert s.REVISION == "26795854fe148e7a4caa37ef6cc051431b8b8790"
    assert sum(size for _, size in s.ARCHIVES.values()) == 3_059_419
    with pytest.raises(TypeError):
        s.ARCHIVES["weights.bin"] = ("a" * 64, 1)
    assert all("data/" in path or path.endswith(("recompute.py", "README.md"))
               for paths in s.EXTRACT.values() for path in paths)


def test_modified_release_is_rejected_before_output_or_execution(tmp_path):
    archives = tmp_path / "release"
    archives.mkdir()
    for name, (_, size) in s.ARCHIVES.items():
        (archives / name).write_bytes(b"x" * size)
    output = tmp_path / "run"
    with pytest.raises(s.ProtocolError, match="hash mismatch"):
        s.replay_official(archives, output)
    assert not output.exists()


def test_allowlisted_extraction_ignores_historical_jobs_and_cannot_escape(tmp_path, monkeypatch):
    raw = io.BytesIO()
    with zipfile.ZipFile(raw, "w") as archive:
        archive.writestr("allowed/a.txt", "public measurements")
        archive.writestr("../outside.txt", "bad")
        archive.writestr("output/historical-job.py", "raise RuntimeError('do not run')")
    content = raw.getvalue()
    name = "fixture.zip"
    monkeypatch.setattr(s, "ARCHIVES", MappingProxyType({name: (hashlib.sha256(content).hexdigest(), len(content))}))
    monkeypatch.setattr(s, "EXTRACT", MappingProxyType({name: ("allowed/a.txt",)}))
    (tmp_path / name).write_bytes(content)
    output = tmp_path / "extract"
    result = s.extract_release(tmp_path, output)
    assert set(result) == {"allowed/a.txt"}
    assert not (tmp_path / "outside.txt").exists()
    assert not (output / "output").exists()
    with pytest.raises(s.ProtocolError, match="immutable"):
        s.extract_release(tmp_path, output)


def test_entropy_certainty_is_normalized_by_candidate_inventory():
    assert s.entropy_certainty((.5, .5)) == pytest.approx(0)
    assert s.entropy_certainty((1., 0.)) == pytest.approx(1)
    assert s.entropy_certainty((.25, .25, .25, .25)) == pytest.approx(0)
    for probabilities in ((0.4, .4), (float("nan"), 0), (1.1, -.1), (1.,)):
        with pytest.raises(s.ProtocolError):
            s.entropy_certainty(probabilities)


def test_frozen_gate_standardization_and_numeric_stability():
    gate = s.LinearGate((2., -1.), .5, (1., 0.), (2., 1.))
    assert gate.probability((1., 0.)) == pytest.approx(0.6224593312018546)
    assert gate.probability((1e9, 0.)) == 1
    assert gate.probability((-1e9, 0.)) == 0
    with pytest.raises(s.ProtocolError):
        gate.probability((1.,))
    with pytest.raises(s.ProtocolError):
        s.LinearGate((1.,), 0., (0.,), (0.,))


def test_start_read_stop_interface_uses_no_gold_and_distinguishes_forced_budget():
    gate = s.LinearGate((1.,), 0., (0.,), (1.,))
    controller = s.SelectiveController(gate, gate, .5, .6, minimum_sentence_gap=2, token_budget=32)
    assert controller.start((.3, .7), (-2.,))["candidate_index"] == 1
    assert controller.start((.3, .7), (2.,))["action"] == "reason"
    assert not controller.request_read((2.,), sentences_since_read=1)
    assert not controller.request_read((-2.,), sentences_since_read=3)
    assert controller.request_read((2.,), sentences_since_read=2)
    assert controller.accept_read((.5, .5), generated_tokens=8)["action"] == "continue"
    accepted = controller.accept_read((.99, .01), generated_tokens=8)
    assert accepted["candidate_index"] == 0 and accepted["entropy_accepted"]
    forced = controller.accept_read((.5, .5), generated_tokens=32)
    assert forced["budget_forced"] and not forced["entropy_accepted"]
    public = {"question": "choose", "candidates": ["first", "second"]}
    assert s.PublicDecision.from_mapping(public).candidates == ("first", "second")
    for field in ("gold", "answer", "correct", "plan", "reward"):
        with pytest.raises(s.ProtocolError, match="public"):
            s.PublicDecision.from_mapping({**public, field: "secret"})


def test_replay_bounds_and_existing_outputs_rejected(tmp_path):
    with pytest.raises(s.ProtocolError, match="budget"):
        s.replay_official(tmp_path, tmp_path / "run", maximum_seconds=3600)
    output = tmp_path / "existing"
    output.mkdir()
    with pytest.raises(s.ProtocolError, match="immutable"):
        s.replay_official(tmp_path, output)


def test_public_release_script_is_not_eagerly_imported():
    source = Path(s.__file__).read_text()
    assert "importlib" not in source and "exec(" not in source
    assert '"-I"' in source and '"--check"' in source
