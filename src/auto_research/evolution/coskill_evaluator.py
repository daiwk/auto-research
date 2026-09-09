"""Executable checkpoint policy operator with delayed test evaluation."""
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
from statistics import mean, pstdev
import time

from .models import EvolutionTrial


class CoSkillEvolutionEvaluator:
    executable_operators = ("policy:coskill",)

    def __init__(self, config, project_dir):
        self.config = config
        self.directory = Path(project_dir) / config.output_dir / "coskill-policy-states"
        self.directory.mkdir(parents=True, exist_ok=True)

    def bind_run_directory(self, run_dir):
        """Persist learned states beside the resumable evolution result."""
        self.directory = Path(run_dir) / "coskill-policy-states"
        self.directory.mkdir(parents=True, exist_ok=True)

    def summary(self):
        return {"benchmark": "toolroute-checkpoint", "selection_split": "validation",
                "final_split": "test", "checkpoint_policy": True,
                "operator_scope": "shared checkpoint CoSkill; learning rate and rollout-group evolution",
                "training_budget": "frozen checkpoint baseline vs fixed-episode CoSkill; not compute-matched RL baseline"}

    def _state_path(self, genome, seed):
        from ..agent_research.coskill_checkpoint import MODEL, REVISION

        source = Path(__file__).parents[1] / "agent_research"
        implementation = {name: hashlib.sha256((source / name).read_bytes()).hexdigest()
                          for name in ("coskill_checkpoint.py", "coskill_rollout.py", "capability_benchmark.py")}
        identity = {"genome": asdict(genome), "model": MODEL, "revision": REVISION,
                    "train_episodes": self.config.steps, "eval_episodes": self.config.agent_episodes,
                    "implementation": implementation}
        fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:20]
        return self.directory / f"{fingerprint}-{seed}.pt"

    def propose(self, parent, generation, index, operators, rng, model):
        # Do not allow unrelated paper components to turn into no-op switches.
        return replace(parent, agent_policy="coskill", learning_rate=(5e-6, 1e-5, 2e-5)[index % 3],
                       group_size=(2, 4)[(generation + index) % 2]), (
            "真实共享 checkpoint CoSkill：只进化学习率和 rollout group；其余预算冻结"
        )

    def evaluate(self, trial_id, generation, parent_id, genome, source_papers, rationale):
        from ..agent_research.coskill_checkpoint import run

        if genome.agent_policy not in {"heuristic", "coskill"}:
            raise ValueError("unsupported checkpoint agent policy")
        started = time.monotonic()
        rows = []
        for seed in self.config.seeds:
            row = run(seed=seed, train_episodes=self.config.steps if genome.agent_policy == "coskill" else 0,
                      eval_episodes=self.config.agent_episodes, group_size=genome.group_size,
                      learning_rate=genome.learning_rate, include_test=False,
                      state_path=self._state_path(genome, seed))
            rows.append(row)
        values = [row["validation"]["success_rate"] for row in rows]
        training = {"seeds": list(self.config.seeds), "fitness_by_seed": values,
                    "diagnostic_only": False, "checkpoint_policy_executed": True,
                    "parameter_changes": [row["parameter_l1_change"] for row in rows],
                    "operator": genome.agent_policy,
                    "benchmark_scope": "public ToolRoute simulator, not ALFWorld/WebShop"}
        return EvolutionTrial(trial_id, generation, parent_id, genome,
                              {"fitness": mean(values), "primary": mean(values),
                               "fitness_std": pstdev(values), "joint_success": mean(values)},
                              training, source_papers, rationale, time.monotonic() - started)

    def test(self, genome):
        import torch
        from ..agent_research.coskill_checkpoint import SharedCheckpoint, evaluate
        from ..agent_research.sep7_mechanisms import HierarchicalSkills

        rows = []
        for seed in self.config.seeds:
            state = torch.load(self._state_path(genome, seed), map_location="cpu", weights_only=True)
            policy = SharedCheckpoint()
            policy.block.load_state_dict(state["block"])
            skills = HierarchicalSkills(similarity=policy.similarity)
            skills.bundles = state["skills"]
            rows.append(evaluate(policy, skills, seed, "test", self.config.agent_episodes, 8))
            del policy
            torch.cuda.empty_cache()
        return {"joint_success": mean(row["success_rate"] for row in rows),
                "primary": mean(row["success_rate"] for row in rows)}
