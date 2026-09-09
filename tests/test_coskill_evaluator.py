from dataclasses import replace

from auto_research.evolution.coskill_evaluator import CoSkillEvolutionEvaluator
from auto_research.evolution.models import EvolutionConfig, EvolutionResult, EvolutionTrial, Genome
from auto_research.evolution.report import render_dashboard, render_evolution_report
from auto_research.cli import _format_agent_evolution_summary


def test_checkpoint_evolution_defers_test_and_runs_every_seed(tmp_path, monkeypatch):
    from auto_research.agent_research import coskill_checkpoint

    calls = []

    def run(**kwargs):
        calls.append(kwargs)
        assert kwargs["include_test"] is False
        return {"validation": {"success_rate": .5}, "parameter_l1_change": 1}

    monkeypatch.setattr(coskill_checkpoint, "run", run)
    config = EvolutionConfig(model="agent", dataset="toolroute-checkpoint", output_dir=tmp_path,
                             seeds=(42, 43), steps=12)
    evaluator = CoSkillEvolutionEvaluator(config, tmp_path)
    genome = Genome(architecture="composable_agent", agent_policy="coskill")
    trial = evaluator.evaluate("g1-t1", 1, "g0-t0", genome, [], "test")
    assert len(calls) == 2
    assert all(row["train_episodes"] == 12 for row in calls)
    assert trial.training["checkpoint_policy_executed"]
    evaluator.evaluate("g0-t0", 0, None, replace(genome, agent_policy="heuristic"), [], "baseline")
    assert all(row["train_episodes"] == 0 for row in calls[-2:])


def test_checkpoint_state_identity_includes_training_budget(tmp_path):
    config = EvolutionConfig(model="agent", dataset="toolroute-checkpoint", output_dir=tmp_path)
    first = CoSkillEvolutionEvaluator(config, tmp_path)
    second = CoSkillEvolutionEvaluator(replace(config, steps=config.steps + 1), tmp_path)
    assert first._state_path(Genome(), 42) != second._state_path(Genome(), 42)


def test_checkpoint_states_are_bound_to_resumable_run(tmp_path):
    config = EvolutionConfig(model="agent", dataset="toolroute-checkpoint", output_dir=tmp_path)
    evaluator = CoSkillEvolutionEvaluator(config, tmp_path)
    run_dir = tmp_path / "runs" / "agent-example"

    evaluator.bind_run_directory(run_dir)

    assert evaluator.directory == run_dir / "coskill-policy-states"
    assert evaluator.directory.is_dir()


def test_checkpoint_proposals_only_change_executed_axes(tmp_path):
    config = EvolutionConfig(model="agent", dataset="toolroute-checkpoint", output_dir=tmp_path)
    evaluator = CoSkillEvolutionEvaluator(config, tmp_path)
    parent = Genome()
    child, _ = evaluator.propose(parent, 1, 0, [], None, None)
    assert child.agent_policy == "coskill"
    assert replace(child, agent_policy=parent.agent_policy, learning_rate=parent.learning_rate,
                   group_size=parent.group_size) == parent


def test_checkpoint_agent_report_does_not_require_legacy_cost_metrics():
    config = EvolutionConfig(model="agent", dataset="toolroute-checkpoint")
    trial = EvolutionTrial(
        "g0-t0", 0, None, Genome(),
        {"fitness": .5, "primary": .5, "joint_success": .5},
        {"seeds": [42]}, (), "baseline", 1.0,
    )
    result = EvolutionResult(
        "checkpoint-report", config, trials=[trial], champion_id=trial.trial_id,
        dataset_summary={"checkpoint_policy": True, "training_budget": "two episodes"},
    )
    assert "joint success `0.5000`" in render_evolution_report(result)
    dashboard = render_dashboard(result)
    assert "isCheckpointAgent" in dashboard and "training_budget" in dashboard
    assert _format_agent_evolution_summary(trial.validation) == "Joint success: 0.5000"
