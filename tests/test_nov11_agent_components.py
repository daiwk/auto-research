from dataclasses import replace
import math

import pytest

from auto_research.agent_research import are_bench, fgse, pase, retrace, wikitrace


@pytest.mark.parametrize("module", [are_bench, fgse, pase, retrace, wikitrace])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_component_diagnostics_are_finite_and_explicitly_not_capabilities(module, seed):
    result = module.diagnostic(seed)
    assert result["seed"] == seed
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(type(x) is bool and x for x in result["checks"].values())
    assert all(type(x) in {int, float} and math.isfinite(x) for x in result["metrics"].values())
    with pytest.raises(ValueError, match="CPU-only"):
        module.diagnostic(seed, "cuda")


def test_wikitrace_preserves_failed_raw_evidence_and_never_validates_insights():
    run = wikitrace.SourceRun("r", "public training task", (wikitrace.ToolStep("inspect", "not ready"),), False)
    compiled = wikitrace.Compilation("r", "interpretation", "Possibly failed because it was not ready.")
    contradictory = (wikitrace.Insight("a", "r", "Wait.", "not ready"),
                     wikitrace.Insight("b", "r", "Do not wait.", "not ready"))
    corpus = wikitrace.EvidenceLinkedCorpus((run,), (compiled,), contradictory)
    assert corpus.actor_memory() == contradictory
    assert corpus.descend("a")[1] is run
    assert corpus.source_digests["r"] == run.digest
    with pytest.raises(TypeError):
        corpus.insights["c"] = contradictory[0]
    with pytest.raises(KeyError):
        corpus.descend("missing")
    with pytest.raises(ValueError, match="training"):
        replace(run, split="test")
    with pytest.raises(ValueError, match="link"):
        wikitrace.EvidenceLinkedCorpus((run,), (compiled,), (replace(contradictory[0], run_id="missing"),))
    with pytest.raises(ValueError, match="three"):
        wikitrace.EvidenceLinkedCorpus((run,), (compiled,), tuple(
            replace(contradictory[0], identity=str(i)) for i in range(4)))


def test_fgse_uses_three_distinct_empirical_denominators_and_effect_failures():
    transfer = (fgse.Probe(.1, .3), fgse.Probe(.1, .5))
    falsification = (fgse.Probe(.5, .5), fgse.Probe(.5, .5, False), fgse.Probe(.5, .4))
    regression = (fgse.Probe(.8, .7), fgse.Probe(.2, .4))
    result = fgse.commitment_gate(transfer, falsification, regression,
                                  fgse.GateConfig(.1, .7, .06, .01))
    assert result.commit
    assert result.gain == pytest.approx(.3)
    assert result.failure_rate == pytest.approx(2 / 3)
    assert result.regression_damage == pytest.approx(.05)
    assert not fgse.commitment_gate(transfer, falsification, regression).commit


@pytest.mark.parametrize("group", [(), (object(),)])
def test_fgse_no_empty_or_untyped_probe_gate(group):
    with pytest.raises(ValueError, match="nonempty"):
        fgse.commitment_gate(group, (fgse.Probe(0., 1.),), (fgse.Probe(0., 1.),))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -.1, 1.1, True])
def test_fgse_rejects_invalid_verifier_scores(value):
    with pytest.raises(ValueError):
        fgse.Probe(value, .5)


def test_pase_patch_is_targeted_validation_only_and_does_not_execute_program():
    # If this source were executed, it would raise. Patching only syntax-checks it.
    skill = pase.ProgramSkill("a", "Keep a distinct description.", "raise RuntimeError('do not execute')")
    patch = pase.ProgramPatch("a", skill.program_digest, "raise RuntimeError('still do not execute')")
    better = pase.apply_validated_patch(skill, patch, baseline_score=1., candidate_score=2., split="validation")
    assert better.accepted and better.skill.description == skill.description
    assert better.skill.program != skill.program
    tied = pase.apply_validated_patch(skill, patch, baseline_score=1., candidate_score=1., split="validation")
    assert not tied.accepted and tied.skill is skill
    with pytest.raises(ValueError, match="test"):
        pase.apply_validated_patch(skill, patch, baseline_score=1., candidate_score=2., split="test")
    with pytest.raises(ValueError, match="preimage"):
        pase.apply_validated_patch(better.skill, patch, baseline_score=1., candidate_score=2., split="validation")
    with pytest.raises(SyntaxError):
        pase.apply_validated_patch(skill, replace(patch, replacement_program="def invalid("),
                                   baseline_score=1., candidate_score=2., split="validation")


def _workflow():
    observation = retrace.Binding("observation", "online")
    rule = retrace.Rule("inspect", retrace.Guard(observation, "eq", False), "inspect",
                        (("customer", retrace.Binding("input", "customer")),), ("sop:1",), False)
    return retrace.DecisionList(retrace.Guard(retrace.Binding("observation", "done"), "eq", True),
                                (rule,), {"inspect": {"customer": "integer"}})


def test_retrace_no_future_outputs_no_type_coercion_no_silent_unwitnessed_drop():
    ir = _workflow()
    result = ir.next_call(inputs={"customer": 7}, observations={"online": False, "done": False})
    assert result.tool == "inspect" and dict(result.arguments) == {"customer": 7}
    assert result.witnessed is False
    with pytest.raises(TypeError):
        result.arguments["customer"] = 8
    with pytest.raises(retrace.MissingEvidence):
        ir.next_call(inputs={"customer": 7}, observations={"done": False})
    with pytest.raises(ValueError, match="type"):
        ir.next_call(inputs={"customer": True}, observations={"online": False, "done": False})
    with pytest.raises(ValueError):
        retrace.Binding("future_result", "customer")
    assert ir.next_call(inputs={}, observations={"done": True}) is None


def test_retrace_decision_list_chooses_first_matching_rule():
    original = _workflow()
    second = replace(original.rules[0], identity="second")
    ir = retrace.DecisionList(original.completion, (*original.rules, second), original.tool_schemas)
    assert ir.next_call(inputs={"customer": 7}, observations={"online": False, "done": False}).rule_id == "inspect"
    assert not retrace.Guard(retrace.Binding("input", "x"), "eq", True).holds({"x": 1}, {})


def test_are_bench_csr_is_per_task_macro_not_pooled_item_accuracy():
    a = are_bench.ChecklistVerdict("a", ("1", "2", "3"), (("1", True), ("2", False), ("3", False)))
    b = are_bench.ChecklistVerdict("b", ("1",), (("1", True),))
    result = are_bench.score((a, b))
    assert result["instance_success_rate"] == .5
    assert result["checklist_success_rate"] == pytest.approx(2 / 3)
    assert result["checklist_success_rate"] != 2 / 4


@pytest.mark.parametrize("expected,decisions", [
    ((), ()), (("a", "a"), (("a", True), ("a", True))),
    (("a", "b"), (("a", True),)), (("a",), (("a", 1),)),
    (("a", "b"), (("a", True), ("a", True))),
])
def test_are_bench_denominator_and_binary_verdicts_fail_closed(expected, decisions):
    with pytest.raises(ValueError):
        are_bench.ChecklistVerdict("task", expected, decisions)
