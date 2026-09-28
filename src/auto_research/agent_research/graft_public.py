"""No-oracle tool-policy experiment for GRAFT's graph credit assignment.

The policy is deliberately small and tabular, not an LLM.  This tests whether
graph credit can train action selection in the existing held-out L2.1 tool
environment without passing evaluator-private routes or answers to the policy.
"""

from __future__ import annotations

from collections import defaultdict
import math

import numpy as np

from .capability_benchmark import (
    CapabilityEnvironment, build_capability_tasks, evaluate_episode,
)
from .graft import Step, Trajectory, trajectory_credit


def _probabilities(actions: tuple[str, ...], weights: dict[str, float]) -> np.ndarray:
    scores = np.asarray([weights.get(action, 0.0) for action in actions], dtype=np.float64)
    scores -= scores.max()
    values = np.exp(scores)
    return values / values.sum()


def _rollout(task, weights: dict[str, float], rng: np.random.Generator):
    """Expose only observation, tool specifications and live tool feedback."""
    observation = task.observation
    environment = CapabilityEnvironment(task)
    tag_to_tool = {spec.tag: spec.name for spec in observation.tools}
    tags = observation.start_tags
    status = "start"
    answer = ""
    steps = []
    choices = []
    # Fixed public safety cap: do not read the environment's route-derived budget.
    while tags and len(environment.calls) < 12:
        actions = tuple(dict.fromkeys(tag_to_tool[tag] for tag in tags))
        probabilities = _probabilities(actions, weights)
        action = actions[int(rng.choice(len(actions), p=probabilities))]
        state = f"{status}:{','.join(sorted(tags))}"
        feedback = environment.call(action)
        answer = feedback.answer or answer
        if feedback.terminal:
            next_state = f"terminal:{feedback.status}:{int(environment.completed)}"
            next_tags = ()
        elif feedback.next_tags:
            next_tags = feedback.next_tags
            next_state = f"{feedback.status}:{','.join(sorted(next_tags))}"
        elif feedback.status == "transient_error":
            next_tags = tags
            next_state = f"{feedback.status}:{','.join(sorted(next_tags))}"
        else:
            next_tags = tuple(tag for tag in tags if tag_to_tool[tag] != action)
            next_state = f"{feedback.status}:{','.join(sorted(next_tags))}"
        steps.append(Step(state, action, next_state))
        choices.append((actions, probabilities, action))
        status, tags = feedback.status, next_tags
    # If no tag remains after a nonterminal error, this is a distinct sink.
    if steps and not environment.completed and not feedback.terminal:
        last = steps[-1]
        steps[-1] = Step(last.state, last.action, "terminal:abandoned:0")
    result = evaluate_episode(task, answer, environment)
    return Trajectory(tuple(steps), float(result["joint_ok"])), choices, result


def run_graft_tool_policy(
    *, seed: int, train_episodes: int = 36, validation_episodes: int = 60,
    test_episodes: int = 60, epochs: int = 4, learning_rate: float = 0.25,
) -> dict:
    """Compare graph TD against outcome REINFORCE with identical public tasks.

    Only training outcomes feed either update. Validation is observed after
    training; test is evaluated once and never used to select a checkpoint.
    """
    if min(train_episodes, validation_episodes, test_episodes) < 12:
        raise ValueError("each split requires at least twelve episodes")
    if epochs < 1 or learning_rate <= 0 or not math.isfinite(learning_rate):
        raise ValueError("epochs and learning_rate must be positive")
    training = build_capability_tasks(train_episodes, seed, "train")
    validation = build_capability_tasks(validation_episodes, seed, "validation")
    testing = build_capability_tasks(test_episodes, seed, "test")
    results = {}
    for method in ("outcome", "graph_td"):
        weights: dict[str, float] = defaultdict(float)
        rng = np.random.default_rng(seed)
        history = []
        for epoch in range(epochs):
            batch = [_rollout(task, weights, rng) for task in training]
            trajectories = tuple(row[0] for row in batch)
            if method == "graph_td":
                credit = trajectory_credit(trajectories)
                advantages = credit.graph_gae
            else:
                mean_outcome = float(np.mean([row.outcome for row in trajectories]))
                advantages = tuple(
                    (row.outcome - mean_outcome,) * len(row.steps) for row in trajectories
                )
            for (_, choices, _), path_advantages in zip(batch, advantages, strict=True):
                for (actions, probabilities, selected), advantage in zip(
                    choices, path_advantages, strict=True,
                ):
                    for action, probability in zip(actions, probabilities, strict=True):
                        weights[action] += learning_rate * advantage * (
                            float(action == selected) - float(probability)
                        ) / len(training)
            history.append({
                "epoch": epoch + 1,
                "train_joint_success": float(np.mean([row[2]["joint_ok"] for row in batch])),
            })

        def evaluate(tasks, split_seed):
            eval_rng = np.random.default_rng(split_seed)
            rows = [_rollout(task, weights, eval_rng)[2] for task in tasks]
            return {
                "joint_success": float(np.mean([row["joint_ok"] for row in rows])),
                "plan_step_f1": float(np.mean([row["plan_step_f1"] for row in rows])),
                "average_cost": float(np.mean([row["cost"] for row in rows])),
                "irreversible_error_rate": float(np.mean([
                    row["irreversible_errors"] > 0 for row in rows
                ])),
            }

        results[method] = {
            "history": history,
            "weight_l2_after_training": float(np.linalg.norm(list(weights.values()))),
            "validation": evaluate(validation, seed + 10_000),
            "test": evaluate(testing, seed + 20_000),
        }
    return {
        "seed": seed,
        "methods": results,
        "protocol": {
            "benchmark": "toolroute-l2.1-v1", "train_episodes": train_episodes,
            "validation_episodes": validation_episodes, "test_episodes": test_episodes,
            "epochs": epochs, "learning_rate": learning_rate,
            "policy": "tabular softmax over public tool tags, not an LLM",
            "oracle_fields_exposed": False, "diagnostic_only": True,
            "test_used_for_selection": False,
        },
    }
