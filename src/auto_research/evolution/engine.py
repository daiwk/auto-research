from __future__ import annotations

import datetime as dt
import json
from concurrent.futures import (
    FIRST_COMPLETED, ThreadPoolExecutor, wait,
)
import multiprocessing as mp
import queue
import random
import time
from pathlib import Path

from .models import EvolutionConfig, EvolutionResult, Genome
from .candidate_design import (
    generate_and_verify_candidates, write_candidate_specs,
)
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
            specs_path = write_candidate_specs(
                run_dir / "paper-candidates.json", papers, config.model
            )
            if config.candidate_generator_command:
                result.verification_records.extend(
                    generate_and_verify_candidates(
                        config.candidate_generator_command, specs_path,
                        self.project_dir, config.candidate_timeout_seconds,
                    )
                )
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
            pool = ThreadPoolExecutor(max_workers=workers)
            yield from _collect_with_deadlines(
                [
                    (spec, pool.submit(
                        _safe_evaluate, evaluator, spec, self.config.retries
                    ))
                    for spec in specs
                ], self.config.trial_timeout_seconds,
            )
            pool.shutdown(wait=False, cancel_futures=True)
            return
        yield from _run_isolated_trials(
            self.config, self.project_dir, specs, workers,
            self.config.trial_timeout_seconds,
        )


def _make_evaluator(config, project_dir):
    return get_provider(config.model).evaluator_factory(config, project_dir)


def _evaluate_worker(config, project_dir, spec):
    return _safe_evaluate(_make_evaluator(config, project_dir), spec, config.retries)


def _isolated_evaluate_entry(config, project_dir, spec, output):
    try:
        output.put(("ok", _evaluate_worker(config, project_dir, spec)))
    except BaseException as exc:  # serialize failures across the process boundary
        output.put(("error", f"{type(exc).__name__}: {exc}"))


def _run_isolated_trials(config, project_dir, specs, workers, timeout_seconds):
    """Bounded process scheduler whose timeouts terminate actual trial workers."""

    context = mp.get_context("spawn")
    queued = list(specs)
    active = {}
    while queued or active:
        while queued and len(active) < workers:
            spec = queued.pop(0)
            output = context.Queue(maxsize=1)
            process = context.Process(
                target=_isolated_evaluate_entry,
                args=(config, project_dir, spec, output),
                name=f"evolve-{spec[0]}",
            )
            process.start()
            active[process.pid] = (process, output, spec, time.monotonic())

        completed = []
        now = time.monotonic()
        for pid, (process, output, spec, started) in tuple(active.items()):
            if process.is_alive() and now - started < timeout_seconds:
                continue
            if process.is_alive():
                process.terminate()
                process.join(5)
                if process.is_alive():
                    process.kill()
                    process.join()
                yield _failed_trial(
                    spec,
                    f"TimeoutError: trial exceeded hard limit of {timeout_seconds}s",
                    now - started,
                )
            else:
                process.join()
                try:
                    kind, payload = output.get(timeout=1)
                except queue.Empty:
                    yield _failed_trial(
                        spec, f"WorkerExitError: process exited with {process.exitcode}",
                        now - started,
                    )
                else:
                    yield payload if kind == "ok" else _failed_trial(
                        spec, payload, now - started,
                    )
            output.close()
            completed.append(pid)
        for pid in completed:
            active.pop(pid)
        if active and not completed:
            time.sleep(0.05)


def _safe_evaluate(evaluator, spec, retries=0):
    last_error = None
    for _ in range(retries + 1):
        try:
            return evaluator.evaluate(*spec)
        except Exception as exc:
            last_error = exc
    exc = last_error
    if exc is not None:
        return _failed_trial(spec, f"{type(exc).__name__}: {exc}")


def _failed_trial(spec, error, duration_seconds=0.0):
    from .models import EvolutionTrial
    trial_id, generation, parent_id, genome, papers, rationale = spec
    return EvolutionTrial(
        trial_id, generation, parent_id, genome,
        {"fitness": -1e9, "ndcg_at_10": -1.0, "hit_at_10": 0.0,
         "perplexity": 1e9, "instruction_loss": 1e9, "lm_loss": 1e9},
        {"parameters": 0, "seeds": []}, papers, rationale,
        duration_seconds, "failed", error,
    )


def _effective_workers(config: EvolutionConfig) -> int:
    if config.device.startswith("cuda"):
        slots = config.gpu_slots
        if config.gpu_memory_per_trial_mb:
            try:
                import torch
                free_bytes, _ = torch.cuda.mem_get_info()
                memory_slots = free_bytes // (config.gpu_memory_per_trial_mb * 1024**2)
                slots = min(slots, max(1, int(memory_slots)))
            except (ImportError, RuntimeError):
                slots = 1
        return max(1, min(config.workers, slots))
    return config.workers


def _collect_with_deadlines(submitted, timeout_seconds):
    """Collect futures with per-trial deadlines and explicit timeout records."""

    pending = {future: (spec, time.monotonic()) for spec, future in submitted}
    while pending:
        done, _ = wait(pending, timeout=0.1, return_when=FIRST_COMPLETED)
        for future in done:
            pending.pop(future)
            yield future.result()
        now = time.monotonic()
        expired = [
            future for future, (_, started) in pending.items()
            if now - started >= timeout_seconds
        ]
        for future in expired:
            spec, started = pending.pop(future)
            future.cancel()
            yield _failed_trial(
                spec,
                f"TimeoutError: trial exceeded {timeout_seconds}s scheduling deadline",
                now - started,
            )


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
        elif (
            paper.architecture == "small_llm"
            and genome.architecture != "gpt_baseline"
            and not genome.architecture.startswith("micro_vlm_")
        ):
            matched.append(paper.arxiv_id)
        elif paper.architecture == genome.post_training:
            matched.append(paper.arxiv_id)
        elif (
            paper.architecture
            and paper.architecture.startswith("objective:")
            and genome.multimodal_objective == paper.architecture.split(":", 1)[1]
        ):
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
                "policy": genome.agent_policy,
                "recovery": genome.agent_failure_recovery,
                "context": genome.genrec_context,
                "head": genome.genrec_head,
                "reward": genome.genrec_reward,
                "distillation": genome.genrec_distillation,
            }.get(component)
            if selected == value:
                matched.append(paper.arxiv_id)
    return tuple(dict.fromkeys(matched))


def _fingerprint(genome: Genome):
    return tuple(sorted(genome.to_dict().items()))
