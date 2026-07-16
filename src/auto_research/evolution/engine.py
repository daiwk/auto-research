from __future__ import annotations

import datetime as dt
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import random
from pathlib import Path

from .hyformer import HyFormerEvaluator
from .llm import MicroLLMEvaluator
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
        domain = "language model" if config.model == "micro-llm" else "recommendation"
        query = config.query or f"{config.model} {config.direction} {domain} efficient architecture"
        papers = discover_papers(query, config.max_papers, config.allow_network, track="llm" if config.model == "micro-llm" else "recommendation")
        result = EvolutionResult(run_id, config, papers=papers)
        evaluator = self.evaluator or _make_evaluator(config, self.project_dir)
        result.dataset_summary = evaluator.summary() if hasattr(evaluator, "summary") else {}
        if config.model == "micro-llm":
            baseline_genome = Genome(
                architecture="gpt_baseline", dimensions=config.llm_dimensions,
                layers=config.llm_layers, learning_rate=3e-4,
                batch_size=config.llm_batch_size,
                sequence_length=config.llm_sequence_length,
            )
        else:
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
                genome, rationale = propose(parent.genome, generation, index, architectures, rng, config.model)
                attempts = 0
                while _fingerprint(genome) in seen and attempts < 20:
                    genome, rationale = propose(parent.genome, generation, index + attempts + 1, architectures, rng, config.model)
                    attempts += 1
                if _fingerprint(genome) in seen:
                    continue
                seen.add(_fingerprint(genome))
                paper_ids = _paper_ids(genome, papers)
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
    if config.model == "micro-llm":
        return MicroLLMEvaluator(
            (project_dir / config.dataset_dir).resolve(), config.dataset, config.steps,
            config.seeds, config.allow_network, config.maximum_train_tokens,
            config.maximum_eval_tokens, config.vocab_size,
        )
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
            {"fitness": -1e9, "ndcg_at_10": -1.0, "hit_at_10": 0.0,
             "perplexity": 1e9, "instruction_loss": 1e9, "lm_loss": 1e9},
            {"parameters": 0, "seeds": []}, papers, rationale, 0.0, "failed", f"{type(exc).__name__}: {exc}")


def _paper_ids(genome, papers):
    terms = set(genome.architecture.split("_"))
    matched = []
    for paper in papers:
        if paper.architecture == genome.architecture or paper.architecture in terms:
            matched.append(paper.arxiv_id)
        elif paper.architecture == "data_mixture" and genome.data_recipe != "wikitext":
            matched.append(paper.arxiv_id)
        elif paper.architecture == "neftune" and genome.post_training == "neftune":
            matched.append(paper.arxiv_id)
        elif paper.architecture == "parallel_block" and "parallel" in terms:
            matched.append(paper.arxiv_id)
        elif paper.architecture == "small_llm" and genome.architecture != "gpt_baseline":
            matched.append(paper.arxiv_id)
    return tuple(dict.fromkeys(matched))


def _fingerprint(genome: Genome):
    return tuple(sorted(genome.to_dict().items()))
