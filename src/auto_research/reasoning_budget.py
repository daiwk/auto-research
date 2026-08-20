"""Public multi-budget reasoning evaluation without oracle answer selection."""

from __future__ import annotations

from collections import Counter
import re
import time
from pathlib import Path

import numpy as np

from .checkpoint_backend import HFCausalLMBackend
from .post_training.generation import GenerationExample, load_generation_suite
from .evolution.models import EvolutionTrial


ANSWER = re.compile(r"(?:Answer\s*:\s*)?(-?[\d,]+(?:\.\d+)?)")


def extract_answer(text: str) -> str:
    matches = ANSWER.findall(text)
    return matches[-1].replace(",", "") if matches else ""


def select_self_consistent(outputs: tuple[str, ...]) -> tuple[str, float]:
    answers = [extract_answer(text) for text in outputs]
    usable = [answer for answer in answers if answer]
    if not usable:
        return "", 0.0
    answer, count = Counter(usable).most_common(1)[0]
    return answer, count / len(answers)


def evaluate_reasoning_budget(
    backend,
    examples: tuple[GenerationExample, ...],
    *,
    samples: int,
    max_new_tokens: int,
    stop_consensus: float,
    seed: int,
    token_cost_per_million: float = 0.0,
) -> dict[str, float]:
    correct = tokens = latency = calls = used_samples = 0.0
    started = time.perf_counter()
    for index, example in enumerate(examples):
        batch = backend.generate(
            example.prompt, samples=samples, max_new_tokens=max_new_tokens,
            seed=seed + index,
        )
        selected_count = samples
        if samples > 1 and stop_consensus < 1.0:
            for prefix in range(2, samples + 1):
                _, consensus = select_self_consistent(batch.texts[:prefix])
                if consensus >= stop_consensus:
                    selected_count = prefix
                    break
        answer, _ = select_self_consistent(batch.texts[:selected_count])
        correct += float(answer == example.answer)
        tokens += sum(batch.generated_tokens[:selected_count])
        latency += batch.latency_seconds * selected_count / samples
        calls += 1
        used_samples += selected_count
    count = max(1, len(examples))
    return {
        "accuracy": correct / count,
        "generated_tokens": tokens,
        "tokens_per_example": tokens / count,
        "latency_seconds": latency,
        "latency_seconds_per_example": latency / count,
        "model_calls": calls,
        "samples_per_example": used_samples / count,
        "estimated_cost": tokens / 1_000_000 * token_cost_per_million,
        "wall_seconds": time.perf_counter() - started,
    }


class ReasoningBudgetEvolutionEvaluator:
    def __init__(
        self, dataset_dir: Path, dataset: str, seeds: tuple[int, ...],
        allow_network: bool, maximum_examples: int, model_id: str,
        revision: str, checkpoint_path: Path | None, backend=None,
    ):
        self.dataset_dir, self.dataset, self.seeds = dataset_dir, dataset, seeds
        self.allow_network, self.maximum_examples = allow_network, maximum_examples
        self.model_id, self.revision, self.checkpoint_path = model_id, revision, checkpoint_path
        self._backend = backend

    @property
    def backend(self):
        if self._backend is None:
            self._backend = HFCausalLMBackend(
                self.model_id, self.revision, self.checkpoint_path,
                offline=not self.allow_network,
            )
        return self._backend

    def summary(self):
        return {
            "dataset": self.dataset,
            "seeds": list(self.seeds),
            "budget_axis": "reasoning_samples",
            "metrics": [
                "accuracy", "generated_tokens", "latency_seconds",
                "model_calls", "estimated_cost",
            ],
            "selection": (
                "accuracy - 0.00001 * generated_tokens; answer selected by "
                "self-consistency, never gold"
            ),
        }

    def _run(self, genome, seed, target):
        suite = load_generation_suite(
            self.dataset, self.dataset_dir, self.allow_network,
            self.maximum_examples, seed,
        )
        examples = getattr(suite, target)[: self.maximum_examples]
        return evaluate_reasoning_budget(
            self.backend, examples, samples=genome.reasoning_samples,
            max_new_tokens=genome.reasoning_max_new_tokens,
            stop_consensus=genome.reasoning_stop_consensus, seed=seed,
        )

    def evaluate(self, trial_id, generation, parent_id, genome, source_papers, rationale):
        started = time.monotonic()
        rows = [self._run(genome, seed, "validation") for seed in self.seeds]
        validation = {key: float(np.mean([row[key] for row in rows])) for key in rows[0]}
        validation["primary"] = validation["accuracy"] - 0.00001 * validation["generated_tokens"]
        validation["fitness"] = validation["primary"]
        return EvolutionTrial(
            trial_id, generation, parent_id, genome, validation,
            {"seeds": list(self.seeds), "backend": self.backend.provenance()},
            source_papers, rationale, time.monotonic() - started,
        )

    def test(self, genome):
        rows = [self._run(genome, seed + 10_000, "test") for seed in self.seeds]
        result = {key: float(np.mean([row[key] for row in rows])) for key in rows[0]}
        result["primary"] = result["accuracy"] - 0.00001 * result["generated_tokens"]
        return result
