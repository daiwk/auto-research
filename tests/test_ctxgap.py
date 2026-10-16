from __future__ import annotations

import csv
import io
import json
from pathlib import Path
import runpy
import sys

import pytest

from auto_research.agent_research import ctxgap as c


def test_weighting_and_task_cluster_bootstrap_are_not_probe_macro():
    rows = [{"run": "a", "w": 1., "a": 1., "b": 0.},
            {"run": "b", "w": 9., "a": 0., "b": 1.}]
    assert c.weighted_mean(rows, "a") == .1
    assert c.clustered_interval(rows, "a", "b", draws=1000) == [-1., 1.]
    assert c.clustered_interval(rows[:1], "a", draws=1000) is None
    assert c.clustered_interval(rows, "a", draws=1000) == c.clustered_interval(rows, "a", draws=1000)
    assert c.weighted_mean(rows + [{"run": "c", "w": 0., "a": 1., "b": 0.}], "a") == .1


def test_csv_duplicate_invalid_and_nonfinite_scores_rejected():
    raw = {k: "1" for k in c.HEADERS["main37_units.csv"]}
    raw.update(run="run_a", qid="q1", category="plan")
    def data(rows):
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=c.HEADERS["main37_units.csv"])
        writer.writeheader()
        writer.writerows(rows)
        return out.getvalue().encode()
    assert len(c._csv_rows(data([raw]), "main37_units.csv")) == 1
    for rows in ([raw, raw], [{**raw, "valid": "true"}], [{**raw, "w": "-1"}],
                 [{**raw, "acc_U": "nan"}], [{**raw, "acc_U": "1.01"}]):
        with pytest.raises(c.ProtocolError):
            c._csv_rows(data(rows), "main37_units.csv")


def test_observer_never_receives_scorer_reference_and_failures_stay_in_denominator():
    probes = [c.PublicProbe("one", "u1", "what?", "visible report", "SECRET", 1.),
              c.PublicProbe("two", "u2", "where?", "another report", "HIDDEN", 3.)]
    seen = []
    def observer(packet):
        seen.append(packet)
        assert "reference" not in packet and "SECRET" not in str(packet) and "HIDDEN" not in str(packet)
        if packet["probe_id"] == "two":
            raise RuntimeError("real provider failure")
        return "an observed answer"
    def judge(packet):
        assert packet["reference"] == "SECRET"
        return "correct"
    result = c.evaluate_public(probes, observer, judge)
    assert len(seen) == 2 and result["planned"] == 2 and result["scored"] == 1
    assert result["coverage"] == .5 and result["intention_to_evaluate_accuracy"] == .25
    assert result["acc_U_public_on_scored"] == 1. and result["gap_view"] is None
    assert len(result["failures"]) == 1 and not result["T_full_available"]


def test_public_scores_reject_unknown_or_duplicate_identities():
    probe = c.PublicProbe("p", "u", "q", "view", "gold", 1.)
    for probes, labels in (([probe, probe], {}), ([probe], {"unknown": "correct"}),
                           ([probe], {"p": "all-pass"}), ([], {})):
        with pytest.raises(c.ProtocolError):
            c.score_public_labels(probes, labels)
    assert c.score_public_labels([probe], {})["acc_U_public_on_scored"] is None


def test_pinned_release_does_not_accept_arbitrary_numeric_input(tmp_path):
    path = tmp_path / "data/anon/main37_units.csv"
    path.parent.mkdir(parents=True)
    path.write_text("invented")
    with pytest.raises(c.ProtocolError, match="pinned source mismatch"):
        c.reproduce_release(tmp_path)


def test_incomplete_e2_pairs_are_not_imputed():
    main = [{"run": "a", "k": "1", "w": 1., "valid": "1", "acc_U": 0., "acc_T_full": 1., "acc_agent": 1.}]
    result = c.reproduce_tables(main, [], [], [{"run": "a", "k": "1", "qid": "q", "arm": "A", "w": 1., "valid": "1", "score": 1.}], draws=40)
    assert "e2" not in result and result["main"]["gap"] == 1.


@pytest.mark.parametrize("task_equal", [False, True])
def test_zero_mass_cluster_is_explicitly_rejected(task_equal):
    rows = [{"run": "zero", "w": 0., "a": 1., "b": 0.},
            {"run": "positive", "w": 1., "a": 0., "b": 1.}]
    with pytest.raises(c.ProtocolError, match="cluster.*positive"):
        c.clustered_interval(rows, "a", "b", draws=40, task_equal=task_equal)
    with pytest.raises(c.ProtocolError, match="cluster.*positive"):
        c.clustered_interval(rows[:1], "a", draws=40, task_equal=task_equal)


@pytest.mark.parametrize("weight", ["1.0", True, float("nan"), float("inf"), -1., 10**1000])
def test_public_probe_weight_requires_a_finite_nonnegative_real(weight):
    with pytest.raises(c.ProtocolError):
        c.PublicProbe("p", "u", "q", "view", "reference", weight)


def test_invalid_plan_is_rejected_before_any_external_calls():
    calls = []
    def observer(packet):
        calls.append(packet)
        return "answer"
    def judge(packet):
        calls.append(packet)
        return "correct"
    probe = c.PublicProbe("p", "u", "q", "view", "reference", 0.)
    for probes in ([], [probe], [probe, probe],
                   [c.PublicProbe("a", "u", "q", "view", "r", 1e308),
                    c.PublicProbe("b", "u", "q", "view", "r", 1e308)]):
        with pytest.raises(c.ProtocolError):
            c.evaluate_public(probes, observer, judge)
    assert calls == []


def test_fetch_rejects_oversized_cache_before_reading(tmp_path, monkeypatch):
    path = tmp_path / next(iter(c.FILE_HASHES))
    path.parent.mkdir(parents=True)
    with path.open("wb") as handle:
        handle.truncate(c.MAX_BYTES + 1)
    def forbidden_read(*args, **kwargs):
        raise AssertionError("oversized cache must be rejected before reading")
    monkeypatch.setattr(Path, "read_bytes", forbidden_read)
    with pytest.raises(c.ProtocolError, match="bounded"):
        c.fetch_release(tmp_path)


def test_public_export_cli_validates_plan_and_keeps_reference_on_scorer_side(tmp_path, monkeypatch):
    module = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_ctxgap.py"))
    probes = tmp_path / "probes.json"
    output = tmp_path / "public.json"
    row = {"probe_id": "p", "unit_id": "u", "question": "q", "public_view": "v", "reference": "SECRET", "weight": 0.}
    probes.write_text(json.dumps([row]))
    monkeypatch.setattr(sys, "argv", ["run_ctxgap.py", "export-observer-inputs", "--probes", str(probes), "--output", str(output)])
    with pytest.raises(SystemExit):
        module["main"]()
    assert not output.exists()
    probes.write_text(json.dumps([{**row, "weight": 1.}]))
    assert module["main"]() == 0
    exported = json.loads(output.read_text())
    assert not exported["contains_references"] and "SECRET" not in str(exported)
