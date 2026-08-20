from auto_research.checkpoint_backend import GenerationBatch
from auto_research.evolution.models import Genome
from auto_research.evolution.models import EvolutionConfig, EvolutionResult, EvolutionTrial
from auto_research.evolution.planner import allowed_architectures, propose
from auto_research.evolution.report import render_dashboard, render_evolution_report
from auto_research.post_training.generation import GenerationExample
from auto_research.reasoning_budget import evaluate_reasoning_budget, select_self_consistent


class FakeBackend:
    def generate(self, prompt, *, samples, max_new_tokens, seed):
        outputs = tuple(
            "reason Answer: 4" if index != 1 else "reason Answer: 5"
            for index in range(samples)
        )
        return GenerationBatch(outputs, tuple(5 for _ in outputs), 0.02 * samples)


def test_self_consistency_never_receives_gold_answer():
    answer, consensus = select_self_consistent(("Answer: 4", "Answer: 5", "Answer: 4"))
    assert answer == "4"
    assert consensus == 2 / 3


def test_reasoning_curve_reports_accuracy_tokens_latency_calls_and_early_stop():
    result = evaluate_reasoning_budget(
        FakeBackend(),
        (GenerationExample("2+2", "Answer: 4", "4", 0.1),),
        samples=8, max_new_tokens=32, stop_consensus=0.67, seed=42,
    )
    assert result["accuracy"] == 1.0
    assert result["samples_per_example"] == 4
    assert result["generated_tokens"] == 20
    assert result["latency_seconds"] == 0.08
    assert result["model_calls"] == 1
    assert "estimated_cost" in result


def test_reasoning_budget_is_an_evolve_genome_axis():
    architectures = allowed_architectures("reasoning-checkpoint", "dynamic budget", [])
    assert architectures == ["reasoning:1", "reasoning:2", "reasoning:4", "reasoning:8"]
    genome, rationale = propose(
        Genome(architecture="reasoning-checkpoint"), 1, 2, architectures,
        __import__("random").Random(42), "reasoning-checkpoint",
    )
    assert genome.reasoning_samples == 4
    assert "gold answer" in rationale


def test_reasoning_report_uses_budget_metrics_instead_of_recommendation_metrics():
    config = EvolutionConfig(
        model="reasoning-checkpoint", dataset="arithmetic-generate",
        direction="budget", generations=1, population=1, steps=1,
    )
    metrics = {
        "accuracy": 0.5, "tokens_per_example": 10.0,
        "latency_seconds_per_example": 0.1, "model_calls": 2.0,
        "estimated_cost": 0.0, "fitness": 0.49,
    }
    trial = EvolutionTrial(
        "g0-t0", 0, None, Genome(architecture="reasoning-checkpoint"),
        metrics, {}, (), "baseline", 0.1,
    )
    result = EvolutionResult(
        "run", config, trials=[trial], champion_id="g0-t0",
        baseline_test=metrics, champion_test=metrics,
        dataset_summary={"budget_axis": "reasoning_samples", "seeds": [42]},
    )
    report = render_evolution_report(result)
    dashboard = render_dashboard(result)
    assert "完整预算曲线" in report
    assert "NDCG@10" not in report
    assert "isReasoning" in dashboard
