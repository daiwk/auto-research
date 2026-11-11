from dataclasses import asdict, replace
import hashlib
import json
import math
import time

import pytest
from scipy.stats import t

from auto_research.agent_research import lisa, reprobridge as bridge


def task():
    return bridge.ActorTask("task", "https://arxiv.org/abs/example", "a" * 40,
                            "public-train", "small-model", "execute training", "MSE", "five-seed mean")


def test_actor_view_contains_neither_reference_samples_nor_success_thresholds():
    view = asdict(task())
    assert set(view) == {"identity", "paper_url", "raw_commit", "dataset", "model", "procedure",
                         "metric", "reporting_statistic"}
    assert all(x not in json.dumps(view) for x in ["observations", "coverage", "interval", "success"])


@pytest.mark.parametrize("coverage", [.8, .95])
def test_exact_student_prediction_interval_not_mean_confidence_interval(coverage):
    values = (.8, .9, 1., 1.1, 1.2)
    ref = bridge.Reference(values, coverage)
    radius = float(t.ppf((1 + coverage) / 2, 4)) * math.sqrt(.025) * math.sqrt(1.2)
    assert ref.interval == pytest.approx((1 - radius, 1 + radius))
    assert ref.compatible(1) and not ref.compatible(-100) and not ref.compatible(100)


def test_zero_variance_still_has_one_percent_floor_and_two_sided_criterion():
    ref = bridge.Reference((100.,) * 5)
    assert ref.interval == (99., 101.)
    assert ref.compatible(99) and ref.compatible(101)
    assert not ref.compatible(0)  # A lower-is-better win is not reproduction compatibility.
    assert bridge.Reference((0.,) * 5).interval == (0., 0.)


@pytest.mark.parametrize("values", [(1.,) * 4, (1.,) * 6, (True,) * 5, (math.nan,) * 5])
def test_reference_observations_are_exactly_five_finite_independent_inputs(values):
    with pytest.raises(ValueError):
        bridge.Reference(values)


def put(path, content):
    path.write_text(content)
    return path.name, hashlib.sha256(path.read_bytes()).hexdigest()


def evidence(tmp_path):
    script = put(tmp_path / "experiment.py", "print('measurement')\n")
    env = put(tmp_path / "environment.json", '{"python":"3"}')
    started = time.time_ns()
    output = put(tmp_path / "result.json", '{"validation":{"MSE":1.0}}')
    finished = time.time_ns()
    rec = bridge.ExecutionRecord("a" * 40, script, env, output, ("validation", "MSE"),
                                 started, finished, finished + 1)
    return rec


def test_file_backed_measurement_and_four_component_handoff(tmp_path):
    rec = evidence(tmp_path)
    assert bridge.read_measurement(tmp_path, task(), rec) == 1.
    code = put(tmp_path / "code.py", "# refined code\n")
    guide = put(tmp_path / "guide.md", "# exact procedure\n")
    bridge.Artifact(code, rec.environment, rec.script, guide).verify(tmp_path)
    with pytest.raises(ValueError):
        bridge.Artifact(code, rec.environment, rec.script, rec.script)


def test_stale_output_changed_bytes_commit_and_json_location_are_rejected(tmp_path):
    rec = evidence(tmp_path)
    for bad in [replace(rec, run_started_ns=rec.run_finished_ns),
                replace(rec, code_commit="b" * 40), replace(rec, value_path=("not-present",)),
                replace(rec, output=(rec.output[0], "0" * 64))]:
        with pytest.raises(ValueError):
            bridge.read_measurement(tmp_path, task(), bad)
    put(tmp_path / "result.json", '{"validation":{"MSE":0.1}}')
    with pytest.raises(ValueError, match="changed"):
        bridge.read_measurement(tmp_path, task(), rec)


def test_symlink_cannot_escape_run_root(tmp_path):
    rec = evidence(tmp_path)
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "escape").symlink_to(tmp_path / "result.json")
    with pytest.raises(ValueError, match="inside"):
        bridge._verified_file(nested, "escape", rec.output[1])


@pytest.mark.parametrize("category", sorted(bridge.VIOLATION_CLASSES))
def test_only_localized_material_findings_surviving_refutation_invalidate(category):
    ref = bridge.Reference((1.,) * 5)
    finding = bridge.Finding(category, "executed-script:line19", True, True)
    assert bridge.evaluate(1., ref, (finding,))["invalidated"]
    assert not bridge.evaluate(1., ref, (replace(finding, material_effect=False),))["invalidated"]
    assert not bridge.evaluate(1., ref, (replace(finding, refutation_failed=None),))["invalidated"]
    assert not bridge.evaluate(1., ref, (replace(finding, refutation_failed=False),))["invalidated"]


def report(i, label=0, vector=(1., 0.), domain="privacy", **kw):
    return lisa.Report(str(i), f"group-{i}", domain, f"scenario-{i}", label, vector, **kw)


def draft(i="p", label=0, vector=(1., 0.)):
    return lisa.Draft(i, f"Title-{i}", "Description", "Content", label, "broad", vector)


def test_beta_lower_is_actual_posterior_quantile_and_not_perfect_empirical_accuracy():
    for support in (0, 1, 4, 5, 50):
        assert lisa.beta_lower(support, 0) == pytest.approx(.05 ** (1 / (support + 1)))
    assert lisa.beta_lower(4, 0) < .55 < lisa.beta_lower(5, 0)
    assert lisa.beta_lower(5, 1) < lisa.beta_lower(5, 0)
    for bad in [(True, 0), (-1, 0), (0, 1.5)]:
        with pytest.raises(ValueError):
            lisa.beta_lower(*bad)


def test_average_linkage_is_not_single_linkage_connected_components():
    vectors = [(math.cos(a), math.sin(a)) for a in (0, math.pi / 6, math.pi / 3)]
    assert len(lisa._clusters(vectors)) == 2


def test_mixed_cases_generate_two_ungated_label_specific_local_cues():
    memory = lisa.Memory()
    memory.refresh(0, (report("a", 0, attributes=(("visibility", "public"),)),
                       report("b", 1, attributes=(("visibility", "private"),))),
                   (draft(),), embed_local=lambda _: (1., 0.))
    context = memory.retrieve((1., 0.))
    assert not context["broad"] and len(context["local"]) == 2
    assert not context["base_fallback"]
    assert {p.label for p in context["local"]} == {0, 1}
    assert all(p.conflict_score == .5 and "visibility: allow=public; refuse=private" in p.statement
               for p in context["local"])
    assert memory.broad[0].near_conflict
    with pytest.raises(ValueError, match="not surfaced"):
        memory.feedback("f", (memory.broad[0].identity,), 0)


def test_case_clustering_is_separate_from_policy_clusters_and_namespaced():
    memory = lisa.Memory()
    memory.refresh(0, (report("a", 0, domain="one"), report("b", 1, domain="two")), ())
    assert not memory.local and memory.retrieve((1., 0.))["base_fallback"]


def test_refresh_limits_majority_fallback_and_tied_missing_label():
    memory = lisa.Memory()
    with pytest.raises(ValueError):
        memory.refresh(0, (report("a"),), tuple(draft(str(i)) for i in range(4)))
    with pytest.raises(ValueError, match="no majority"):
        memory.refresh(0, (report("a", 0), report("b", 1)), (draft(label=None),))
    memory.refresh(0, tuple(report(i) for i in range(3)), (draft(label=None),))
    assert memory.broad[0].label == 0 and memory.broad[0].support == 3
    assert set(memory.broad[0].report_ids) == {"0", "1", "2"}
    with pytest.raises(ValueError):
        memory.refresh(0, (), ())


def test_runtime_counts_persist_once_only_for_surviving_verbatim_representative():
    memory = lisa.Memory()
    memory.refresh(0, tuple(report(i) for i in range(5)), (draft("z"),))
    assert len(memory.retrieve((1., 0.))["broad"]) == 1
    memory.feedback("feedback1", ("z",), 0)
    memory.refresh(1, (), ())
    assert memory.broad[0].support == 6
    memory.refresh(2, tuple(report(i) for i in range(5, 10)), (draft("a"),))
    assert memory.broad[0].identity == "a" and memory.broad[0].support == 10
    memory.retrieve((1., 0.))
    with pytest.raises(ValueError):
        memory.feedback("feedback1", ("a",), 0)
    with pytest.raises(ValueError):
        memory.feedback("test-feedback", ("a",), 0, split="test")


def test_retrieval_is_capped_before_confidence_gate_not_backfilled_with_far_rules():
    memory = lisa.Memory()
    angle = math.pi / 6
    drafts = (draft("near1", 1, (math.cos(angle), math.sin(angle))),
              draft("near2", 1, (math.cos(angle), -math.sin(angle))), draft("far", 0, (-1., 0.)))
    memory.refresh(0, tuple(report(i) for i in range(5)), drafts)
    context = memory.retrieve((1., 0.))
    assert set(context["broad_candidate_ids"]) == {"near1", "near2"}
    assert context["base_fallback"] and not context["broad"]


def test_heldout_scenario_group_is_never_adaptation_input_and_failures_atomic():
    memory = lisa.Memory(heldout_groups=("group-x",))
    with pytest.raises(ValueError, match="held-out"):
        memory.refresh(0, (report("x"),), (draft(),))
    assert memory.day == -1 and not memory.broad


@pytest.mark.parametrize("module", [lisa, bridge])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics_are_finite_reproducible_cpu_mechanism_not_agent_capability(module, seed):
    value = module.diagnostic(seed)
    assert value == module.diagnostic(seed)
    assert value["diagnostic_only"] and value["evaluation_tier"] == "l1_mechanism"
    assert all(value["checks"].values())
    assert all(type(v) in (int, float) and math.isfinite(v) for v in value["metrics"].values())
    assert module.REQUIRES_GPU_VALIDATION is False
    with pytest.raises(ValueError):
        module.diagnostic(seed, device="cuda")
