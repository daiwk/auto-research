from __future__ import annotations

import datetime as dt
import json
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import random
from pathlib import Path

from .models import EvolutionConfig, EvolutionResult, Genome
from .papers import discover_papers
from .planner import allowed_architectures, propose, round_record
from .providers import get_provider
from .report import write_evolution_artifacts
from .research_memory import methodology_order, update_research_memory, verify_trial
from ..runtime import configure_runtime


class ModelEvolutionEngine:
    def __init__(self, config: EvolutionConfig, project_dir: Path | None = None, evaluator=None):
        config.validate()
        self.config = config
        self.project_dir = (project_dir or Path.cwd()).resolve()
        self.evaluator = evaluator

    def run(self) -> tuple[EvolutionResult, Path]:
        config = self.config
        configure_runtime(None if config.device == "auto" else config.device, config.cpu_threads)
        provider = get_provider(config.model)
        run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        run_dir = (
            config.resume_dir.resolve() if config.resume_dir
            else (self.project_dir / config.output_dir / f"{config.model}-{run_id}").resolve()
        )
        domain = provider.search_domain
        query = config.query or f"{config.model} {config.direction} {domain} efficient architecture"
        track = provider.track
        if config.resume_dir:
            state_path = run_dir / "result.json"
            if not state_path.exists():
                raise ValueError(f"resume directory has no result.json: {run_dir}")
            result = EvolutionResult.from_dict(
                json.loads(state_path.read_text(encoding="utf-8")), config=config,
            )
            papers = result.papers
        else:
            papers = discover_papers(
                query, config.max_papers, config.allow_network, track=track
            )
            result = EvolutionResult(run_id, config, papers=papers)
        evaluator = self.evaluator or _make_evaluator(config, self.project_dir)
        result.dataset_summary = evaluator.summary() if hasattr(evaluator, "summary") else {}
        baseline_genome = provider.baseline_factory(config)
        if result.trials:
            baseline = result.trials[0]
            champion = next(
                trial for trial in result.trials if trial.trial_id == result.champion_id
            )
        else:
            baseline = evaluator.evaluate("g0-t0", 0, None, baseline_genome, (), f"冻结的 {config.model} 初始基线")
            result.trials.append(baseline)
            result.verification_records.append(verify_trial(baseline))
            result.champion_id = baseline.trial_id
            champion = baseline
            write_evolution_artifacts(result, run_dir)

        rng = random.Random(config.seeds[0])
        seen = {_fingerprint(trial.genome) for trial in result.trials}
        architectures = allowed_architectures(config.model, config.direction, papers)
        if config.model == "post-training" and config.dataset.endswith("-generate"):
            generation_algorithms = {"ipo", "simpo", "luspo", "coba-rl"}
            architectures = [
                architecture for architecture in architectures
                if architecture in generation_algorithms
            ]
            if not architectures:
                architectures = sorted(generation_algorithms)
        start_generation = 1 + max((round_["generation"] for round_ in result.rounds), default=0)
        for generation in range(start_generation, config.generations + 1):
            parent = champion
            architectures = methodology_order(architectures, result.research_memory)
            specs = []
            children = [
                trial for trial in result.trials if trial.generation == generation
            ]
            existing_ids = {trial.trial_id for trial in children}
            for index in range(config.population):
                trial_id = f"g{generation}-t{index + 1}"
                if trial_id in existing_ids:
                    continue
                genome, rationale = propose(parent.genome, generation, index, architectures, rng, config.model)
                attempts = 0
                while _fingerprint(genome) in seen and attempts < 20:
                    genome, rationale = propose(parent.genome, generation, index + attempts + 1, architectures, rng, config.model)
                    attempts += 1
                if _fingerprint(genome) in seen:
                    continue
                seen.add(_fingerprint(genome))
                paper_ids = _paper_ids(genome, papers)
                specs.append((trial_id, generation, parent.trial_id, genome, paper_ids, rationale))
            for trial in self._run_generation(evaluator, specs):
                children.append(trial)
                result.trials.append(trial)
                result.verification_records.append(verify_trial(trial, parent))
                write_evolution_artifacts(result, run_dir)
            completed = [trial for trial in children if trial.status == "completed"]
            champion = max(
                [parent, *completed], key=lambda trial: _selection_score(trial, config)
            )
            result.champion_id = champion.trial_id
            result.research_memory = update_research_memory(
                result.research_memory,
                parent,
                children,
                champion,
                result.verification_records,
            )
            result.rounds.append(round_record(generation, parent, children, champion))
            write_evolution_artifacts(result, run_dir)

        result.baseline_test = evaluator.test(baseline_genome)
        result.champion_test = evaluator.test(champion.genome)
        write_evolution_artifacts(result, run_dir)
        return result, run_dir

    def _run_generation(self, evaluator, specs):
        workers = _effective_workers(self.config)
        if workers == 1:
            for spec in specs:
                yield _safe_evaluate(evaluator, spec, self.config.retries)
            return
        if self.evaluator is not None:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(_safe_evaluate, evaluator, spec, self.config.retries) for spec in specs]
                for future in as_completed(futures):
                    yield future.result()
            return
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(_evaluate_worker, self.config, self.project_dir, spec) for spec in specs]
            for future in as_completed(futures):
                yield future.result()


def _make_evaluator(config, project_dir):
    return get_provider(config.model).evaluator_factory(config, project_dir)


def _evaluate_worker(config, project_dir, spec):
    return _safe_evaluate(_make_evaluator(config, project_dir), spec, config.retries)


def _safe_evaluate(evaluator, spec, retries=0):
    last_error = None
    for _ in range(retries + 1):
        try:
            return evaluator.evaluate(*spec)
        except Exception as exc:
            last_error = exc
    exc = last_error
    if exc is not None:
        from .models import EvolutionTrial
        trial_id, generation, parent_id, genome, papers, rationale = spec
        return EvolutionTrial(trial_id, generation, parent_id, genome,
            {"fitness": -1e9, "ndcg_at_10": -1.0, "hit_at_10": 0.0,
             "perplexity": 1e9, "instruction_loss": 1e9, "lm_loss": 1e9},
            {"parameters": 0, "seeds": []}, papers, rationale, 0.0, "failed", f"{type(exc).__name__}: {exc}")


def _effective_workers(config: EvolutionConfig) -> int:
    if config.device.startswith("cuda"):
        return max(1, min(config.workers, config.gpu_slots))
    return config.workers


def _selection_score(trial, config: EvolutionConfig) -> float:
    seed_count = len(trial.training.get("seeds", config.seeds))
    if seed_count < config.promotion_min_seeds:
        return -1e30
    std = float(
        trial.validation.get("fitness_std", trial.validation.get("std", 0.0))
    )
    return trial.fitness - config.confidence_z * std / max(seed_count, 1) ** 0.5


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
        elif (
            paper.architecture in {"dynamic_rubric", "off_context_grpo"}
            and genome.post_training == paper.architecture
        ):
            matched.append(paper.arxiv_id)
        elif paper.architecture == "parallel_block" and "parallel" in terms:
            matched.append(paper.arxiv_id)
        elif paper.architecture == "small_llm" and genome.architecture != "gpt_baseline":
            matched.append(paper.arxiv_id)
        elif paper.architecture == genome.post_training:
            matched.append(paper.arxiv_id)
        elif (
            paper.architecture == "native_sparse_attention"
            and genome.architecture == "nsa_gated_attention"
        ):
            matched.append(paper.arxiv_id)
        elif (
            paper.architecture == "gated_attention"
            and genome.architecture == "nsa_gated_attention"
        ):
            matched.append(paper.arxiv_id)
        elif (
            paper.architecture == "optimizer:muon"
            and genome.optimizer == "muon"
        ):
            matched.append(paper.arxiv_id)
        elif paper.architecture and ":" in paper.architecture:
            component, value = paper.architecture.split(":", 1)
            selected = {
                "memory": genome.agent_memory,
                "planner": genome.agent_planner,
                "tool": genome.agent_tool_policy,
                "critic": genome.agent_critic,
            }.get(component)
            if selected == value:
                matched.append(paper.arxiv_id)
    return tuple(dict.fromkeys(matched))


def _fingerprint(genome: Genome):
    return tuple(sorted(genome.to_dict().items()))
