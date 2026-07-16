from __future__ import annotations

import datetime as dt
import random
from dataclasses import replace
from pathlib import Path

from .models import EvolutionConfig, EvolutionResult, Genome
from .papers import discover_papers
from .rankmixer import RankMixerEvaluator
from .report import write_evolution_artifacts


class ModelEvolutionEngine:
    def __init__(self, config: EvolutionConfig, project_dir: Path | None = None, evaluator=None):
        config.validate()
        self.config = config
        self.project_dir = (project_dir or Path.cwd()).resolve()
        self.evaluator = evaluator

    def run(self) -> tuple[EvolutionResult, Path]:
        config = self.config
        run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        run_dir = (self.project_dir / config.output_dir / f"{config.model}-{run_id}").resolve()
        query = config.query or f"{config.model} mixer ranking feature interaction recommender"
        papers = discover_papers(query, config.max_papers, config.allow_network)
        result = EvolutionResult(run_id, config, papers=papers)
        evaluator = self.evaluator or RankMixerEvaluator((self.project_dir / config.dataset_dir).resolve(), config.steps, config.seeds)
        baseline_genome = Genome()
        baseline = evaluator.evaluate("g0-t0", 0, None, baseline_genome, ("2507.15551",), "初始 RankMixer dense 基线")
        result.trials.append(baseline)
        result.champion_id = baseline.trial_id
        write_evolution_artifacts(result, run_dir)

        rng = random.Random(config.seeds[0])
        seen = {_fingerprint(baseline_genome)}
        champion = baseline
        architectures = [paper.architecture for paper in papers if paper.architecture]
        architectures = list(dict.fromkeys(architectures)) or ["rankmixer_dense"]
        for generation in range(1, config.generations + 1):
            children = []
            for index in range(config.population):
                genome, rationale = _mutate(champion.genome, generation, index, architectures, rng)
                attempts = 0
                while _fingerprint(genome) in seen and attempts < 12:
                    genome, rationale = _mutate(champion.genome, generation, index + attempts + 1, architectures, rng)
                    attempts += 1
                seen.add(_fingerprint(genome))
                paper_ids = tuple(p.arxiv_id for p in papers if p.architecture == genome.architecture)
                trial = evaluator.evaluate(f"g{generation}-t{index + 1}", generation, champion.trial_id, genome, paper_ids, rationale)
                result.trials.append(trial)
                children.append(trial)
                write_evolution_artifacts(result, run_dir)
            candidate = max([champion, *children], key=lambda trial: trial.fitness)
            champion = candidate
            result.champion_id = champion.trial_id
            write_evolution_artifacts(result, run_dir)

        result.baseline_test = evaluator.test(baseline_genome)
        result.champion_test = evaluator.test(champion.genome)
        write_evolution_artifacts(result, run_dir)
        return result, run_dir


def _mutate(parent: Genome, generation: int, index: int, architectures: list[str], rng: random.Random):
    genome = parent
    mutations = []
    if generation == 1:
        architecture = architectures[index % len(architectures)]
        genome = replace(genome, architecture=architecture)
        mutations.append(f"采用论文映射结构 {architecture}")
    else:
        if index % 3 == 0:
            architecture = architectures[rng.randrange(len(architectures))]
            genome = replace(genome, architecture=architecture)
            mutations.append(f"结构切换为 {architecture}")
    field = (generation + index) % 5
    if field == 0:
        value = rng.choice([32, 64, 96, 128]); genome = replace(genome, dimensions=value); mutations.append(f"dimensions={value}")
    elif field == 1:
        value = rng.choice([1, 2, 3, 4]); genome = replace(genome, layers=value); mutations.append(f"layers={value}")
    elif field == 2:
        value = rng.choice([1e-4, 3e-4, 6e-4, 1e-3]); genome = replace(genome, learning_rate=value); mutations.append(f"learning_rate={value}")
    elif field == 3:
        value = rng.choice(["adamw", "adam", "adagrad"]); genome = replace(genome, optimizer=value); mutations.append(f"optimizer={value}")
    else:
        value = rng.choice([24, 32, 48, 64]); genome = replace(genome, batch_size=value); mutations.append(f"batch_size={value}")
    return genome, "；".join(mutations)


def _fingerprint(genome: Genome):
    return tuple(sorted(genome.to_dict().items()))
