from auto_research.checkpoint_backend import GenerationBatch
from auto_research.evolution.models import Genome
from auto_research.evolution.planner import allowed_architectures, propose
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
