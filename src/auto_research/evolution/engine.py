from __future__ import annotations

import datetime as dt
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import random
from pathlib import Path

from .hyformer import HyFormerEvaluator
from .models import EvolutionConfig, EvolutionResult, Genome
from .papers import discover_papers
from .planner import allowed_architectures, propose, round_record
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
        query = config.query or f"{config.model} {config.direction} recommendation efficient architecture"
        papers = discover_papers(query, config.max_papers, config.allow_network)
        result = EvolutionResult(run_id, config, papers=papers)
        evaluator = self.evaluator or _make_evaluator(config, self.project_dir)
        result.dataset_summary = evaluator.summary() if hasattr(evaluator, "summary") else {}
        baseline_genome = Genome(architecture="hyformer" if config.model == "hyformer" else "rankmixer_dense")
        baseline = evaluator.evaluate("g0-t0", 0, None, baseline_genome, (), f"冻结的 {config.model} 初始基线")
        result.trials.append(baseline)
        result.champion_id = baseline.trial_id
        write_evolution_artifacts(result, run_dir)

        rng = random.Random(config.seeds[0])
        seen = {_fingerprint(baseline_genome)}
        champion = baseline
        architectures = allowed_architectures(config.model, config.direction, papers)
        for generation in range(1, config.generations + 1):
            parent = champion
            specs = []
            for index in range(config.population):
                genome, rationale = propose(parent.genome, generation, index, architectures, rng)
                attempts = 0
                while _fingerprint(genome) in seen and attempts < 20:
                    genome, rationale = propose(parent.genome, generation, index + attempts + 1, architectures, rng)
                    attempts += 1
                if _fingerprint(genome) in seen:
                    continue
                seen.add(_fingerprint(genome))
                paper_ids = _paper_ids(genome.architecture, papers)
                specs.append((f"g{generation}-t{index + 1}", generation, parent.trial_id, genome, paper_ids, rationale))
            children = []
            for trial in self._run_generation(evaluator, specs):
                children.append(trial)
                result.trials.append(trial)
                write_evolution_artifacts(result, run_dir)
            completed = [trial for trial in children if trial.status == "completed"]
            champion = max([parent, *completed], key=lambda trial: trial.fitness)
            result.champion_id = champion.trial_id
            result.rounds.append(round_record(generation, parent, children, champion))
            write_evolution_artifacts(result, run_dir)

        result.baseline_test = evaluator.test(baseline_genome)
        result.champion_test = evaluator.test(champion.genome)
        write_evolution_artifacts(result, run_dir)
        return result, run_dir

    def _run_generation(self, evaluator, specs):
        if self.config.workers == 1:
            for spec in specs:
                yield _safe_evaluate(evaluator, spec)
            return
        if self.evaluator is not None:
            with ThreadPoolExecutor(max_workers=self.config.workers) as pool:
                futures = [pool.submit(_safe_evaluate, evaluator, spec) for spec in specs]
                for future in as_completed(futures):
                    yield future.result()
            return
        with ProcessPoolExecutor(max_workers=self.config.workers) as pool:
            futures = [pool.submit(_evaluate_worker, self.config, self.project_dir, spec) for spec in specs]
            for future in as_completed(futures):
                yield future.result()


def _make_evaluator(config, project_dir):
    arguments = ((project_dir / config.dataset_dir).resolve(), config.dataset, config.steps,
                 config.seeds, config.maximum_users, config.maximum_items, config.evaluation_users)
    return HyFormerEvaluator(*arguments) if config.model == "hyformer" else RankMixerEvaluator(*arguments)


def _evaluate_worker(config, project_dir, spec):
    return _safe_evaluate(_make_evaluator(config, project_dir), spec)


def _safe_evaluate(evaluator, spec):
    try:
        return evaluator.evaluate(*spec)
    except Exception as exc:
        from .models import EvolutionTrial
        trial_id, generation, parent_id, genome, papers, rationale = spec
        return EvolutionTrial(trial_id, generation, parent_id, genome,
            {"ndcg_at_10": -1.0, "hit_at_10": 0.0},
            {"parameters": 0, "seeds": []}, papers, rationale, 0.0, "failed", f"{type(exc).__name__}: {exc}")


def _paper_ids(architecture, papers):
    terms = set(architecture.split("_"))
    return tuple(p.arxiv_id for p in papers if p.architecture == architecture or p.architecture in terms)


def _fingerprint(genome: Genome):
    return tuple(sorted(genome.to_dict().items()))
