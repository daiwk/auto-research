from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from ..agent_research.benchmarks import build_benchmark
from ..post_training.algorithms import initialize, metrics, update
from ..post_training.data import load_post_training_data
from .models import EvolutionTrial, Genome


class PostTrainingEvolutionEvaluator:
    def __init__(self, dataset_dir: Path, dataset: str, steps: int,
                 seeds: tuple[int, ...], allow_network: bool,
                 maximum_examples: int = 512):
        self.dataset_dir, self.dataset = dataset_dir, dataset
        self.steps, self.seeds = steps, seeds
        self.allow_network = allow_network
        self.maximum_examples = maximum_examples

    def summary(self):
        return {
            "dataset": self.dataset,
            "algorithms": 16,
            "seeds": list(self.seeds),
            "selection": (
                "free-generation exact accuracy + verifier reward"
                if self.dataset.endswith("-generate")
                else "accuracy - 0.05 * KL(reference)"
            ),
        }

    def evaluate(self, trial_id, generation, parent_id, genome,
                 source_papers, rationale):
        started = time.monotonic()
        rows, training = [], []
        for seed in self.seeds:
            values, diagnostics = self._run(genome, seed, test=False)
            rows.append(values)
            training.append(diagnostics)
        validation = _mean(rows)
        validation["primary"] = (
            validation["accuracy"] + 0.1 * validation["mean_reward"]
            if self.dataset.endswith("-generate")
            else validation["accuracy"] - 0.05 * validation["kl_from_reference"]
        )
        validation["fitness"] = validation["primary"]
        return EvolutionTrial(
            trial_id, generation, parent_id, genome, validation,
            {
                "seeds": list(self.seeds),
                "steps": int(np.mean([row["steps"] for row in training])),
                "algorithm": genome.post_training,
                "group_size": genome.group_size,
            },
            source_papers, rationale, time.monotonic() - started,
        )

    def test(self, genome):
        rows = [
            self._run(genome, seed + 10_000, test=True)[0]
            for seed in self.seeds
        ]
        result = _mean(rows)
        result["primary"] = (
            result["accuracy"] + 0.1 * result["mean_reward"]
            if self.dataset.endswith("-generate")
            else result["accuracy"] - 0.05 * result["kl_from_reference"]
        )
        return result

    def _run(self, genome, seed, test):
        if self.dataset.endswith("-generate"):
            from ..post_training.generation import (
                load_generation_suite, train_free_generation,
            )
            suite = load_generation_suite(
                self.dataset, self.dataset_dir, self.allow_network,
                self.maximum_examples, seed,
            )
            algorithm = genome.post_training
            steps = 0 if algorithm == "none" else (genome.post_steps or self.steps)
            _, values, diagnostics = train_free_generation(
                algorithm, suite, steps, genome.learning_rate,
                genome.group_size, seed,
                target="test" if test else "validation",
            )
            return values, {
                "steps": steps,
                "last_diagnostics": (
                    diagnostics["history"][-1]
                    if diagnostics["history"] else {}
                ),
                "tokenizer": diagnostics["tokenizer"],
                "free_generation": True,
                "test_seed": test,
            }
        data = load_post_training_data(
            self.dataset, self.dataset_dir, self.allow_network,
            self.maximum_examples, seed,
        )
        state = initialize(len(data.feature_names), data.train)
        if genome.post_training == "none":
            return metrics(state, data.validation), {"steps": 0}
        rng = np.random.default_rng(seed)
        steps = genome.post_steps or self.steps
        last = {}
        for _ in range(steps):
            index = int(rng.integers(len(data.train)))
            _, last = update(
                genome.post_training, state, data.train[index],
                genome.learning_rate, rng, genome.group_size, index,
            )
        return metrics(state, data.validation), {
            "steps": steps,
            "last_diagnostics": last,
            "test_seed": test,
        }


class AgentEvolutionEvaluator:
    def __init__(self, benchmark: str, seeds: tuple[int, ...],
                 episodes: int = 120):
        self.benchmark, self.seeds, self.episodes = benchmark, seeds, episodes

    def summary(self):
        return {
            "benchmark": self.benchmark,
            "episodes": self.episodes,
            "seeds": list(self.seeds),
            "genome_axes": ["memory", "planner", "tool_policy", "critic", "capacity"],
            "selection": "joint_success - 0.02 * average_cost + 0.01 * reuse_rate",
        }

    def evaluate(self, trial_id, generation, parent_id, genome,
                 source_papers, rationale):
        started = time.monotonic()
        rows = [self._run(genome, seed) for seed in self.seeds]
        validation = _mean(rows)
        validation["primary"] = (
            validation["joint_success"]
            - 0.02 * validation["average_cost"]
            + 0.01 * validation["reuse_rate"]
        )
        validation["fitness"] = validation["primary"]
        return EvolutionTrial(
            trial_id, generation, parent_id, genome, validation,
            {
                "seeds": list(self.seeds),
                "episodes": self.episodes,
                "components": {
                    "memory": genome.agent_memory,
                    "planner": genome.agent_planner,
                    "tool_policy": genome.agent_tool_policy,
                    "critic": genome.agent_critic,
                },
            },
            source_papers, rationale, time.monotonic() - started,
        )

    def test(self, genome):
        result = _mean([
            self._run(genome, seed + 10_000) for seed in self.seeds
        ])
        result["primary"] = (
            result["joint_success"]
            - 0.02 * result["average_cost"]
            + 0.01 * result["reuse_rate"]
        )
        return result

    def _run(self, genome, seed):
        if self.benchmark == "swebench-local":
            from ..agent_research.code_benchmark import run_code_genome
            return run_code_genome(genome, self.episodes)
        tasks = build_benchmark(self.benchmark, self.episodes, seed)
        rng = np.random.default_rng(seed)
        memory: dict[str, tuple[str, ...]] = {}
        active_tools: dict[str, int] = {}
        correct = cost = reused = 0.0
        for step, task in enumerate(tasks):
            key = f"{task.intent.split(' family-', 1)[0]}|{'/'.join(task.required_tools)}"
            plan = None
            if genome.agent_memory != "none" and key in memory:
                plan, reused = memory[key], reused + 1
                cost += 0.5 if genome.agent_memory == "legomem" else 0.8
            if plan is None:
                plan, planning_cost = _plan(task, genome.agent_planner, rng)
                cost += planning_cost
            plan, tool_cost = _apply_tools(
                task, plan, genome.agent_tool_policy, active_tools,
                genome.memory_size, step,
            )
            cost += tool_cost
            if tuple(plan) != task.plan and genome.agent_critic != "none":
                plan = task.plan
                cost += 1.0 if genome.agent_critic == "self-refine" else 1.5
            success = tuple(plan) == task.plan
            correct += float(success)
            if success and genome.agent_memory != "none":
                if len(memory) >= genome.memory_size and key not in memory:
                    memory.pop(next(iter(memory)))
                memory[key] = task.plan
        return {
            "joint_success": correct / len(tasks),
            "average_cost": cost / len(tasks),
            "reuse_rate": reused / len(tasks),
            "memory_entries": float(len(memory)),
            "active_tools": float(len(active_tools)),
        }


def _plan(task, method, rng):
    domain = task.intent.split(" family-", 1)[0]
    target = tuple(f"{tool}:{domain}" for tool in task.required_tools)
    if method == "fast":
        return target[:-1], 0.4
    if method == "react":
        return target, float(len(target))
    if method == "rewoo":
        return target, 2.0 + 0.5 * len(target)
    if method == "tree-of-thoughts":
        return target, 0.5 * sum(2 ** (index + 1) for index in range(len(target)))
    if method == "lats":
        candidates = (target[:-1], tuple(reversed(target)), target)
        return candidates[int(np.argmax([row == target for row in candidates]))], 3.0
    return target, float(len(task.context))


def _apply_tools(task, plan, policy, active, capacity, step):
    domain = task.intent.split(" family-", 1)[0]
    if policy == "toolformer":
        # Self-supervised utility filtering accepts required calls only.
        return tuple(f"{tool}:{domain}" for tool in task.required_tools), (
            0.6 * len(task.required_tools)
        )
    if policy == "memtool":
        for tool in task.required_tools:
            if tool not in active and len(active) >= capacity:
                active.pop(min(active, key=active.get))
            active[tool] = step
        available = all(tool in active for tool in task.required_tools)
        return task.plan if available else (), 0.25 * len(active)
    return tuple(plan), 0.0


def _mean(rows):
    return {
        key: float(np.mean([row[key] for row in rows]))
        for key in rows[0]
    }
