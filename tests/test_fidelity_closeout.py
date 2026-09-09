import math

import pytest

from auto_research.evolution.composable import AgentEvolutionEvaluator
from auto_research.evolution.composable import PostTrainingEvolutionEvaluator
from auto_research.evolution.engine import _selection_score
from auto_research.evolution.models import EvolutionConfig, EvolutionTrial, Genome
from auto_research.agent_research.capability_methods import CapabilityPolicy


@pytest.mark.parametrize("flag", [
    {"diagnostic_only": True}, {"promotion_eligible": False},
])
def test_diagnostic_cannot_outscore_real_trial(flag):
    trial = EvolutionTrial(
        "diagnostic", 1, None, Genome(architecture="composable-agent"),
        {"fitness": 1e20}, {"seeds": [42, 43, 44], **flag}, (), "", 0,
    )
    score = _selection_score(trial, EvolutionConfig(model="agent", dataset="toolroute-l2.1"))
    assert math.isinf(score) and score < 0


@pytest.mark.parametrize("benchmark", [
    "evomem-mini", "planbench-mini", "scalemcp-mini", "swebench-local",
])
def test_legacy_agent_benchmarks_are_not_promotion_evidence(benchmark):
    evaluator = AgentEvolutionEvaluator(benchmark, (42, 43, 44), episodes=6)
    assert evaluator.summary()["diagnostic_only"] is True
    assert evaluator.summary()["promotion_eligible"] is False


@pytest.mark.parametrize("components", [
    {"agent_memory": "atomrec"}, {"agent_policy": "coskill"},
    {"agent_planner": "lats"},
])
def test_paper_names_cannot_silently_become_generic_switches(components):
    with pytest.raises(ValueError, match="No executable"):
        CapabilityPolicy.from_genome(Genome(architecture="composable-agent", **components))


def test_generic_routing_baseline_remains_executable():
    assert CapabilityPolicy.from_genome(
        Genome(architecture="composable-agent")
    ).components["policy"] == "heuristic"


def test_inventory_distinguishes_labels_and_counters():
    from scripts.audit_fidelity_boundaries import inspect_source

    rows = inspect_source("def solve(task):\n    self.calls += 1\n    return task.answer\n")
    assert {row["kind"] for row in rows} == {
        "label_access_requires_role_review", "state_update_not_execution_evidence",
    }
    assert all(row["function"] == "solve" for row in rows)


def test_gold_derived_candidate_post_training_is_diagnostic(tmp_path):
    for dataset in ("arithmetic-smoke", "gsm8k-candidate"):
        evaluator = PostTrainingEvolutionEvaluator(tmp_path, dataset, 3, (42,), False)
        assert evaluator.summary()["promotion_eligible"] is False


def test_post_training_evolve_only_advertises_free_generation_operators():
    assert PostTrainingEvolutionEvaluator.executable_operators == (
        "grpo", "ipo", "simpo",
    )


def test_candidate_policy_diagnostic_refuses_to_relabel_validation_as_test(tmp_path):
    evaluator = PostTrainingEvolutionEvaluator(
        tmp_path, "arithmetic-smoke", 3, (42,), False,
    )
    with pytest.raises(ValueError, match="no independent test split"):
        evaluator.test(Genome(post_training="none"))


def test_free_generation_test_reuses_training_seed(tmp_path, monkeypatch):
    evaluator = PostTrainingEvolutionEvaluator(tmp_path, "arithmetic-generate", 3, (42, 43), False)
    seen = []

    def run(genome, seed, test):
        seen.append((seed, test))
        return {"accuracy": .5, "mean_reward": .5}, {}

    monkeypatch.setattr(evaluator, "_run", run)
    evaluator.test(Genome())
    assert seen == [(42, True), (43, True)]


def test_free_generation_splits_are_distinct(tmp_path):
    from auto_research.post_training.generation import load_generation_suite

    suite = load_generation_suite("arithmetic-generate", tmp_path, False, 128, 42)
    sets = [{row.prompt for row in split} for split in (suite.train, suite.validation, suite.test)]
    assert len(sets[0]) == 128 and len(sets[1]) == 48 and len(sets[2]) == 48
    assert not sets[0] & sets[1] and not sets[0] & sets[2] and not sets[1] & sets[2]


def test_free_generation_rejects_unimplemented_paper_label():
    from auto_research.post_training.generation import train_free_generation

    with pytest.raises(ValueError, match="No free-generation implementation"):
        train_free_generation("lightning-opd", None, 1, .001, 2, 42)
