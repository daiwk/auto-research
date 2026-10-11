#!/usr/bin/env python3
"""Frozen public checkpoint generates/revises executable black-box grid models.

Gymnasium FrozenLake is an L1 substitute environment, NOT ARC-AGI-3/Pong.
Generated programs run only in the bounded AST interpreter, never Python exec.
All interaction/revision failures and generated versions are saved in artifacts.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import subprocess

from auto_research.agent_research.memento3 import Memento3, ProgramError, replay
from auto_research.agent_research.search_checkpoint import FrozenGenerator, LARGE_MODEL, LARGE_REVISION


GYM_VERSION = "1.1.1"


class BlackBoxGrid:
    """Expose only observed grid/completion/action IDs; no transition table."""

    def __init__(self, seed, budget):
        import gymnasium as gym
        from gymnasium.envs.toy_text.frozen_lake import generate_random_map

        if importlib.metadata.version("gymnasium") != GYM_VERSION:
            raise ValueError(f"this receipt requires gymnasium=={GYM_VERSION}")
        # The environment constructor uses public Gymnasium, not the generated
        # model. These dynamics/latent fields never enter Memento3 prompts.
        self.env = gym.make("FrozenLake-v1", desc=generate_random_map(size=4, p=.9, seed=seed),
                            is_slippery=False, max_episode_steps=budget)
        self.desc = self.env.unwrapped.desc.copy()
        self.position, _ = self.env.reset(seed=seed)
        self.completed = self.terminated = False
        self.actions = tuple(range(self.env.action_space.n))

    def observe(self):
        colors = {b"S": 1, b"F": 0, b"H": 2, b"G": 3}
        grid = [[colors[cell] for cell in row] for row in self.desc]
        row, column = divmod(int(self.position), len(grid[0]))
        grid[row][column] = 4
        return {"grid": grid, "completed": self.completed, "terminated": self.terminated}

    def act(self, action):
        self.position, reward, terminated, truncated, _ = self.env.step(action)
        self.completed = bool(reward > 0)
        self.terminated = bool(terminated or truncated)
        return self.observe()

    def close(self):
        self.env.close()


class GitMemory:
    """Version only generated artifacts in a fresh run-owned Git repository."""

    def __init__(self, path):
        self.path, self.written = Path(path), 0
        self.path.mkdir(parents=True, exist_ok=False)
        subprocess.run(["git", "-c", "init.templateDir=", "init", "--quiet", str(self.path)], check=True)

    def save(self, versions):
        for version in versions[self.written:]:
            member = version["member"]
            # Fixed filenames, never generated pathnames or commands.
            (self.path / f"member-{member}-rulebook.md").write_text(version["rulebook"], encoding="utf-8")
            (self.path / f"member-{member}-world-model.py").write_text(version["source"], encoding="utf-8")
            subprocess.run(["git", "-C", str(self.path), "add", "--", "."], check=True)
            subprocess.run(["git", "-C", str(self.path), "-c", "user.name=Memento3 artifact",
                            "-c", "user.email=artifact@invalid", "-c", "commit.gpgsign=false",
                            "-c", "core.hooksPath=/dev/null",
                            "commit", "--quiet", "--allow-empty", "-m", f"iteration {self.written}"], check=True)
            subprocess.run(["git", "-C", str(self.path), "tag", f"iteration-{self.written}"], check=True)
            self.written += 1


def run_episode(generator, *, seed, budget, population, revisions, max_tokens, memory, journal=None):
    environment = BlackBoxGrid(seed, budget)
    calls = []
    limits = {"compile": max_tokens, "rulebook": 512, "faithfulness": 256,
              "reflection": 256, "explore": 256}

    def generate(role, prompt):
        completion = generator.generate(prompt, limits[role], seed + 10000 + len(calls))
        calls.append({"role": role, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                      **asdict(completion),
                      "output_budget": limits[role],
                      "budget_reached": completion.output_tokens >= limits[role]})
        if journal is not None:
            with journal.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps({"stage": "model_generation", **calls[-1]}, ensure_ascii=False) + "\n")
        return completion.text

    controller = Memento3(generate, environment.actions, population=population, seed=seed,
                          repair_attempts=1, horizon=min(budget, 8), planner_nodes=256,
                          revision_budget=revisions)
    interactions = []
    try:
        controller.start(environment.observe())
        controller.update()
        memory.save(controller.versions)
        for index in range(budget):
            action = controller.choose(budget - index)
            if action is None:
                break
            observed = environment.act(action)
            mismatch = controller.observe(action, observed)
            interactions.append({"action": action, "observation": observed, "mismatch": mismatch})
            if journal is not None:
                with journal.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps({"stage": "real_interaction", **interactions[-1]}) + "\n")
            if observed["terminated"]:
                # Final evidence still invalidates a stale model even if no
                # further environment action remains in budget.
                controller.update()
                memory.save(controller.versions)
                break
            if mismatch or all(member is None for member in controller.members):
                controller.update()
                memory.save(controller.versions)
        final_valid = 0
        for member in controller.members:
            if member:
                try:
                    replay(member.program, controller.histories)
                    final_valid += 1
                except ProgramError:
                    pass
        return {"seed": seed, "population": population, "real_action_budget": budget,
                "real_actions": len(interactions), "goal_completed": environment.completed,
                "terminated": environment.terminated, "valid_final_members": final_valid,
                "accepted_versions": len(controller.versions), "versions": controller.versions,
                "events": controller.events, "calls": calls, "interactions": interactions,
                "initial_observation": controller.histories[0].initial,
                "claim_policy": "L1 black-box substitute; success alone does not establish learned-model improvement"}
    finally:
        environment.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--action-budget", type=int, default=8)
    parser.add_argument("--population", type=int, default=2)
    parser.add_argument("--revisions", type=int, default=2)
    parser.add_argument("--max-tokens", type=int, default=1600)
    parser.add_argument("--source-commit", required=True,
                        help="exact 40-hex locally committed source; remote scratch directory is not a Git checkout")
    args = parser.parse_args()
    if min(args.action_budget, args.population, args.revisions, args.max_tokens) < 1:
        parser.error("positive budgets required")
    if not re.fullmatch(r"[0-9a-f]{40}", args.source_commit):
        parser.error("source commit must be a full 40-hex immutable revision")
    if args.output.exists():
        parser.error("output exists; use a fresh immutable run path")
    generator = FrozenGenerator(LARGE_MODEL, LARGE_REVISION, path=args.checkpoint)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    memory = GitMemory(args.output.with_suffix(".memory"))
    report = {"schema_version": 1, "paper": "2610.11794", "method": "memento3",
              "evaluation_tier": "l1_core_mechanism", "diagnostic_only": True,
              "formal_comparison": False, "paper_benchmark_reproduced": False,
              "checkpoint": generator.provenance(),
              "environment": {"id": "Gymnasium/FrozenLake-v1", "version": GYM_VERSION,
                              "map_seed": args.seed, "slippery": False, "size": 4},
              "protocol": {"underlying_llm_frozen": True, "gold_plan_read": False,
                           "environment_source_read_by_policy": False, "test_read": False,
                           "generated_code_execution": "restricted AST interpreter; no exec/eval",
                           "semantic_judge_human_calibrated": False,
                           "code_as_model_not_handwritten_fallback": True},
              "accelerator": generator.torch.cuda.get_device_name(),
              "implementation_commit": args.source_commit,
              "source_sha256": {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in (
                  "scripts/run_memento3_checkpoint.py", "src/auto_research/agent_research/memento3.py",
                  "src/auto_research/agent_research/memento3_python.py",
                  "src/auto_research/agent_research/search_checkpoint.py",
                  "src/auto_research/agent_research/frugalevo.py")}}
    try:
        report["run"] = run_episode(generator, seed=args.seed, budget=args.action_budget,
                                    population=args.population, revisions=args.revisions,
                                    max_tokens=args.max_tokens, memory=memory,
                                    journal=args.output.with_suffix(".events.jsonl"))
        report["status"] = "completed"
    except Exception as exc:
        report["status"] = "failed"
        report["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        report["checkpoint_calls"] = generator.calls
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "accepted_versions": report["run"]["accepted_versions"],
                      "valid_final_members": report["run"]["valid_final_members"],
                      "goal_completed": report["run"]["goal_completed"]}), flush=True)


if __name__ == "__main__":
    main()
