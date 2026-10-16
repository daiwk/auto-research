import importlib.util
import inspect
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from auto_research.agent_research import disagreement_routing as dr
from auto_research.agent_research import shortcut_sensitivity as ss
from auto_research.agent_research import tracer

ROOT = Path(__file__).resolve().parents[1]


def audit_fixture():
    return [ss.AuditRow(f"d{d}i{i}s{s}", str(d), str(i), f"d{d}tool{i % 2}", i % 2)
            for d in range(3) for i in range(12) for s in range(1 + i % 3)]


def test_lookup_train_labels_are_diagnostic_and_held_out_domain_not_accessed():
    rows = audit_fixture()
    result = ss.leave_one_domain_out(rows)
    assert result["metrics"]["row"]["rows"] == len(rows)
    assert result["seen_tool_fraction"] == 0
    changed = [ss.AuditRow(r.row_id, r.domain, r.interaction, r.tool,
                          1-r.label if r.domain == "0" else r.label) for r in rows]
    changed_result = ss.leave_one_domain_out(changed)
    for row, before, after in zip(rows, result["predictions"], changed_result["predictions"], strict=True):
        if row.domain == "0":
            assert before == after
    cv = ss.grouped_lookup_cv(rows, seed=42, folds=3)
    assert cv["metrics"]["row"]["f1"] > result["metrics"]["row"]["f1"]
    assert "label" not in inspect.signature(ss.lookup_predictions).parameters


def test_equal_interaction_weighting_retains_every_failed_row():
    rows = [ss.AuditRow(f"a{i}", "d", "long", "a", 1) for i in range(9)]
    rows.append(ss.AuditRow("b", "d", "short", "b", 0))
    result = ss.evaluation_units(rows, [1] * 10)
    assert result["row"]["accuracy"] == .9
    assert result["equal_interaction"]["accuracy"] == pytest.approx(.5)
    assert result["equal_interaction"]["weight_sum"] == pytest.approx(2)
    assert result["row"]["rows"] == result["equal_interaction"]["rows"] == 10


def test_paired_contrast_distinguishes_signed_effect_from_placebo():
    result = ss.paired_sensitivity([[0, 0], [1, 1]], [[1, 1], [0, 0]], [[0, 1], [1, 1]], ["a", "b"])
    assert result["signed_block_probability_change"] == 0
    assert result["placebo_adjusted_change"] == -.25


@pytest.mark.parametrize("action,expected", [
    ('Thought: do not execute\nAction: DELETE_FILE\nAction Input: {"x": 1}', "delete_file"),
    ('1. **Action**: send_email\n2. **Action Input**: {}', "send_email"),
    ('Action: earlier\nAction: latest\nAction Input: {}', "latest")])
def test_react_parser_is_inert_and_casefolded(action, expected):
    assert ss.parse_tool(action) == expected


@pytest.mark.parametrize("bad", ["Thought: no tool", "Action Input: {}", "Action:\nAction Input: {}"])
def test_malformed_action_is_not_silently_dropped(bad):
    with pytest.raises(ValueError):
        ss.parse_tool(bad)


def test_metrics_reject_missing_rows_nonfinite_weights_and_invalid_label():
    for arguments in [([1], []), ([2], [1]), ([1], [1], [float("nan")]), ([1], [1], [0])]:
        with pytest.raises(ValueError):
            ss.binary_metrics(*arguments)
    with pytest.raises(ValueError):
        ss.leave_one_domain_out([audit_fixture()[0]] * 2)


def test_corrected_targets_exclude_self_pairs_and_can_be_negative():
    d, g = dr.empirical_targets(["a", "b"], ["a", "a", "b"])
    np.testing.assert_allclose(d, [1/3, 2/3])
    assert g == pytest.approx(2/3)  # ordered distinct-index pairs, not plug-in 4/9
    assert dr.corrected_score(d, g) == pytest.approx(-1/3)
    assert "gold" not in inspect.signature(dr.empirical_targets).parameters
    with pytest.raises(ValueError):
        dr.empirical_targets(["a"], ["b"])


def test_disagreement_indicator_can_compare_parsed_transitions_without_gold():
    weak = [{"call": "find", "arg": 1}]
    strong = [{"call": "find", "arg": 2}, {"call": "find", "arg": 1}]
    d, g = dr.empirical_targets(weak, strong, lambda a, b: a["call"] != b["call"])
    np.testing.assert_array_equal(d, [0])
    assert g == 0


def test_probe_really_optimizes_soft_bce_and_standardizes_train_only():
    x = np.arange(80, dtype=float).reshape(40, 2)
    y = np.linspace(.05, .95, 40)
    model = dr.fit_probability_probe(x, y, seed=43)
    assert model.final_loss < model.initial_loss
    mean = model.mean.copy()
    predicted = model.predict(np.array([[1e9, -1e9]]))
    assert 0 <= predicted[0] <= 1
    np.testing.assert_array_equal(mean, model.mean)
    np.testing.assert_array_equal(mean, x.mean(0))


def test_budget_calibrates_on_validation_only_with_ties_and_nonpositive_scores():
    calibration = dr.calibrate_budget([.4, .4, .2, -.1], .25)
    assert calibration.validation_routed == 0  # boundary tie under-fills, never over-fills
    np.testing.assert_array_equal(calibration.route([.5, .4, -.2]), [True, False, False])
    assert dr.calibrate_budget([-.1, -.2], 1).validation_routed == 0
    assert dr.calibrate_budget([.1, .2], 0).validation_routed == 0
    with pytest.raises(ValueError, match="validation"):
        dr.calibrate_budget([.1], .5, split="test")


@pytest.mark.parametrize("d,g", [(.1, .2), ([], 0), ([.1], [.2]), ([2.], 0), ([.1], float("nan"))])
def test_corrected_score_rejects_invalid_probabilities(d, g):
    with pytest.raises(ValueError):
        dr.corrected_score(d, g)


def tracer_fixture():
    registry = {"a": (1., 0.), "b": (0., 1.), "end": (.7, .7)}
    rows = []
    for i in range(15):
        first = "a" if i % 2 else "b"
        v = registry[first]
        rows.extend([tracer.TrainingStep(str(i), (), v, 4+i % 3, i % 2, first),
                     tracer.TrainingStep(str(i), (first,), v, 4+i % 3, i % 2, "end")])
    return registry, rows


def test_tracer_crossfits_whole_trajectories_and_trains_real_head():
    registry, rows = tracer_fixture()
    examples, coverage = tracer.crossfit_examples(rows, registry, seed=42)
    assert coverage["planned_steps"] == coverage["trainable_steps"] == len(rows)
    assert all(e.target_trajectory not in e.index_trajectories for e in examples)
    model, report = tracer.fit_tracer(rows, registry, seed=42, epochs=60)
    assert report["parameter_delta_l2"] > 0
    assert report["final_crossfit_nll"] < report["initial_crossfit_nll"]
    assert "next_tool" not in inspect.signature(model.retrieve).parameters
    assert model.retrieve((), (1., 0.), query_words=4, prior_turns=0, k=1)["tools"] == ("a",)
    unknown = model.retrieve(("end",), (0., 1.), query_words=4, prior_turns=0, k=2)
    assert unknown["used_global_fallback"] and unknown["tools"][0] == "b"


def test_tracer_analytic_gradient_matches_independent_finite_difference():
    registry, rows = tracer_fixture()
    examples, _ = tracer.crossfit_examples(rows, registry)
    x = np.stack([e.features for e in examples])
    scale = np.where(x.std(0) < 1e-12, 1., x.std(0))
    z = np.column_stack(((x - x.mean(0))/scale, np.ones(len(x))))
    parameters = np.random.default_rng(7).normal(0, .1, (2, 6))
    _, actual = tracer.loss_and_gradient(parameters, z, examples)
    for position in np.ndindex(parameters.shape):
        plus, minus = parameters.copy(), parameters.copy()
        plus[position] += 1e-6
        minus[position] -= 1e-6
        high = tracer.loss_and_gradient(plus, z, examples)[0]
        low = tracer.loss_and_gradient(minus, z, examples)[0]
        assert actual[position] == pytest.approx((high-low)/2e-6, rel=2e-5, abs=1e-8)


def test_tracer_confidence_fallback_and_optional_global_union():
    registry, rows = tracer_fixture()
    model, _ = tracer.fit_tracer(rows, registry, epochs=10)
    forced = tracer.TracerRetriever(model.index, model.head, confidence_gate=1., global_extension=("end",))
    result = forced.retrieve((), (1., 0.), query_words=4, prior_turns=0, k=1)
    assert result["used_global_fallback"]
    assert result["tools"] == ("a", "end")
    assert result["returned_count"] == 2  # Tracer+G union is not silently truncated to k
    assert set(model.index.global_tools(2)) <= set(registry)


def test_tracer_uniform_nonpositive_similarities_and_leak_guard():
    registry, rows = tracer_fixture()
    index = tracer.TransitionIndex(rows, registry)
    signal = index.signals((), (-1., -1.), 3, 0)
    np.testing.assert_allclose(np.exp(signal[2]), [.5, .5])
    examples, _ = tracer.crossfit_examples(rows, registry)
    bad = examples[0]
    contaminated = tracer.CrossfitExample(bad.features, bad.empirical_log, bad.contextual_log,
        bad.target, bad.target_trajectory, frozenset([bad.target_trajectory]))
    with pytest.raises(ValueError, match="leaked"):
        tracer.fit_blend([contaminated], epochs=1)


def test_pinned_cache_rejects_tampering_before_json_parse(tmp_path):
    asset = ss.ASSETS[0]
    path = tmp_path / asset[0]
    path.parent.mkdir(parents=True)
    path.write_text("not a benchmark")
    with pytest.raises(ValueError, match="size mismatch"):
        ss.load_public_audit(tmp_path)


def test_reference_order_is_explicit_and_checks_exact_ordinal_labels(monkeypatch):
    def frozen_bytes(_cache, asset):
        name = asset[0]
        if name.startswith("reference/"):
            return json.dumps([.5, 0.] if "labels" in name else [1., 0.]).encode()
        return json.dumps([{"score": .5 if "harmful_steps" in name else 0.,
                            "id-interaction": "i", "current_action": "Action: inert\nAction Input: {}"}]).encode()
    monkeypatch.setattr(ss, "_read_asset", frozen_bytes)
    _, harm, predictions, _ = ss.load_public_audit(Path("unused"))
    assert [r.domain for r in harm] == ["harmful_steps", "benign_steps"]
    assert predictions == [1, 0]


def test_tracer_untrainable_steps_remain_in_coverage_denominator():
    registry = {"a": (1., 0.), "b": (0., 1.)}
    rows = [tracer.TrainingStep("left", (), (1., 0.), 2, 0, "a"),
            tracer.TrainingStep("right", (), (0., 1.), 2, 0, "b")]
    examples, coverage = tracer.crossfit_examples(rows, registry, folds=2)
    assert not examples
    assert coverage["planned_steps"] == coverage["unseen_prefix_or_child_steps"] == 2


def test_runner_cpu_result_contract_and_immutable_output(tmp_path):
    output = tmp_path / "diagnostic.json"
    command = [sys.executable, str(ROOT / "scripts/run_oct17_agent_components.py"),
               "--seeds", "42", "--methods", "shortcut-sensitivity,disagreement-routing", "--output", str(output)]
    done = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    result = json.loads(output.read_text())
    assert result["diagnostic_only"] and not result["promotion_eligible"]
    assert result["device"] == "cpu" and len(result["executed_source_sha256"]) == 4
    assert result["components"]["shortcut-sensitivity"]["deterministic"]["repetitions"] == 1
    assert not result["components"]["disagreement-routing"]["dataset"]["public_benchmark_evaluated"]
    again = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert again.returncode != 0 and "immutable output" in again.stderr


def test_all_three_seed_operator_diagnostics_are_executable():
    spec = importlib.util.spec_from_file_location("oct17_agent_runner", ROOT / "scripts/run_oct17_agent_components.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    for seed in (42, 43, 44):
        row = runner.tracer_diagnostic(seed)
        assert row["metrics"]["trajectory_overlap"] == 0
        assert row["metrics"]["retained_test_fraction"] == 1
