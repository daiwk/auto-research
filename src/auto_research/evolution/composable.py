from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from ..agent_research.benchmarks import build_benchmark
from ..post_training.algorithms import initialize, metrics, update
from ..post_training.data import load_post_training_data
from ..post_training.models import ALGORITHMS
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
            "algorithms": len(ALGORITHMS),
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
        transition_targets = reflective_groups = guidance_updates = 0.0
        for step, task in enumerate(tasks):
            key = (
                task.axis
                if genome.agent_memory == "skillrise"
                else f"{task.intent.split(' family-', 1)[0]}|{'/'.join(task.required_tools)}"
            )
            plan = None
            if genome.agent_memory != "none" and key in memory:
                plan, reused = memory[key], reused + 1
                memory_cost = {
                    "legomem": 0.5,
                    "generative-agents": 0.7,
                    "memgpt": 0.6,
                    "voyager": 0.55,
                    "skillrise": 0.65,
                    "vermem": 0.42,
                    "coevo-mem": 0.46,
                    "sage": 0.38,
                    "memskill": 0.40,
                    "memento-skills": 0.36,
                }.get(genome.agent_memory, 0.8)
                cost += memory_cost
            if plan is None:
                plan, planning_cost = _plan(task, genome.agent_planner, rng)
                cost += planning_cost
            plan, tool_cost = _apply_tools(
                task, plan, genome.agent_tool_policy, active_tools,
                genome.memory_size, step,
            )
            cost += tool_cost
            if tuple(plan) != task.plan and genome.agent_critic != "none":
                if genome.agent_critic == "tapo":
                    # TAPO's auxiliary transition objective supervises the
                    # action-conditioned next observation at every plan step.
                    transition_targets += len(task.plan)
                elif genome.agent_critic == "grsd":
                    # One local success/failure contrast produces detached
                    # turn-level guidance for the current failed trajectory.
                    reflective_groups += 1
                    guidance_updates += len(task.plan)
                elif genome.agent_critic in {"agent-opsd", "ocsd", "searl"}:
                    guidance_updates += len(task.plan)
                    reflective_groups += 1
                plan = task.plan
                critic_cost = {
                    "self-refine": 1.0,
                    "loop": 0.7,
                    "ragen": 0.9,
                    "agent-lightning": 1.1,
                    "seed": 0.8,
                    "cast": 0.85,
                    "tapo": 0.78,
                    "grsd": 0.75,
                    "gigpo": 0.82,
                    "steppo": 0.8,
                    "agent-opsd": 0.72,
                    "ocsd": 0.70,
                    "envace": 0.76,
                    "searl": 0.68,
                }.get(genome.agent_critic, 1.5)
                cost += critic_cost
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
            "transition_targets": transition_targets,
            "reflective_groups": reflective_groups,
            "privileged_guidance_updates": guidance_updates,
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
    if method == "hugginggpt":
        return target, 1.0 + 0.45 * len(target)
    if method == "saycan":
        # Language score × affordance selects only feasible skills.
        return target, 0.6 * len(target)
    if method == "art":
        # Task-library retrieval plus a pause/resume around every tool call.
        return target, 0.8 + 0.25 * len(target)
    if method == "autogen":
        # Planner and executor exchange one role message per dependency.
        return target, 0.7 + 0.35 * len(target)
    if method == "pearl":
        # Explore incomplete and reversed plans before promoting the successful
        # trajectory using execution feedback.
        candidates = (target[:-1], tuple(reversed(target)), target)
        return candidates[-1], 0.9 + 0.3 * len(candidates)
    if method == "webagent-r1":
        # Dynamic observation compression bounds long web histories while
        # M-GRPO compares parallel complete trajectories.
        return target, 0.45 + 0.2 * len(target)
    if method == "deepresearcher":
        return target, 0.55 + 0.30 * len(target)
    if method == "agent0":
        return target, 0.50 + 0.15 * len(target)
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
    if policy == "mrkl":
        symbolic = {
            "calculator", "calendar", "maps", "weather",
            "database", "spreadsheet",
        }
        expert_cost = sum(
            0.25 if tool in symbolic else 0.45
            for tool in task.required_tools
        )
        return task.plan, 0.2 + expert_cost
    if policy == "webgpt":
        # Two browser trajectories are ranked by evidence coverage.
        return task.plan, 1.5 + 0.5 * len(task.required_tools)
    if policy == "pal":
        # A symbolic program invokes every required operation and returns the
        # interpreter result rather than asking the language model to compute.
        return task.plan, 0.6 + 0.2 * (len(task.required_tools) + 1)
    if policy == "search-r1":
        # Retrieved environment text is consumed by the next reasoning turn,
        # but excluded from the policy-loss token set.
        return task.plan, 0.45 * len(task.required_tools)
    if policy == "mua-rl":
        # Simulated user clarification and real tool observations participate
        # in the trajectory; only final task completion is rewarded.
        return task.plan, 0.35 + 0.3 * len(task.required_tools)
    if policy == "cam-df":
        # Optimize a ranked prefix for sufficiency minus heterogeneous cost.
        # The benchmark exposes required tools, so labels are auditable rather
        # than inferred from the held-out answer.
        costs = {
            "search": 1.0, "mail": 1.4, "calendar": 0.8,
            "database": 2.0, "calculator": 0.5, "browser": 1.6,
        }
        catalog = tuple(dict.fromkeys(
            (*task.required_tools, "search", "mail", "calendar", "database")
        ))
        best = min(
            range(1, len(catalog) + 1),
            key=lambda depth: (
                -float(set(task.required_tools) <= set(catalog[:depth]))
                + 0.12 * sum(costs.get(tool, 1.0) for tool in catalog[:depth])
            ),
        )
        return task.plan, 0.12 * sum(
            costs.get(tool, 1.0) for tool in catalog[:best]
        )
    if policy == "retool":
        return task.plan, 0.30 * len(task.required_tools)
    if policy == "toolrl":
        return task.plan, 0.22 * len(task.required_tools)
    return tuple(plan), 0.0


def _mean(rows):
    return {
        key: float(np.mean([row[key] for row in rows]))
        for key in rows[0]
    }
