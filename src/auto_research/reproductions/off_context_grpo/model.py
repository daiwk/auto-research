from __future__ import annotations

import numpy as np


def _softmax(values):
    values = values - np.max(values)
    exp = np.exp(np.clip(values, -30, 30))
    return exp / exp.sum()


def _evaluate(weights, examples):
    correct = pass8 = 0
    margins = []
    for row in examples:
        scores = row["features"] @ weights
        order = np.argsort(-scores)
        correct += int(order[0] == row["gold"])
        pass8 += int(row["gold"] in order[:8])
        others = np.delete(scores, row["gold"])
        margins.append(float(scores[row["gold"]] - np.max(others)))
    return {
        "pass_at_1": correct / len(examples),
        "pass_at_8": pass8 / len(examples),
        "gold_margin": float(np.mean(margins)),
        "examples": len(examples),
    }


def train_grpo(examples, steps: int, seed: int, off_context: bool):
    rng = np.random.default_rng(seed)
    weights = rng.normal(0.0, 0.03, examples[0]["features"].shape[1])
    group_size = 8
    learning_rate = 0.035
    successful_groups = 0
    corrections, losses = [], []
    for _ in range(steps):
        row = examples[int(rng.integers(len(examples)))]
        logits = row["features"] @ weights
        target_policy = _softmax(logits)
        if off_context:
            guided_logits = logits.copy()
            guided_logits[row["gold"]] += 3.0
            behavior_policy = _softmax(guided_logits)
        else:
            behavior_policy = target_policy
        actions = rng.choice(len(logits), size=group_size, p=behavior_policy)
        rewards = (actions == row["gold"]).astype(np.float64)
        advantages = rewards - rewards.mean()
        successful_groups += int(rewards.sum() > 0)
        if np.allclose(advantages, 0):
            losses.append(0.0)
            continue
        expected = target_policy @ row["features"]
        update = np.zeros_like(weights)
        for action, advantage in zip(actions, advantages):
            ratio = target_policy[action] / max(behavior_policy[action], 1e-9)
            correction = float(np.clip(ratio, 0.1, 5.0)) if off_context else 1.0
            update += correction * advantage * (row["features"][action] - expected)
            corrections.append(correction)
        weights += learning_rate * update / group_size
        losses.append(float(-np.mean(rewards)))
    return weights, {
        "steps": steps,
        "group_size": group_size,
        "successful_reward_groups": successful_groups,
        "successful_reward_group_rate": successful_groups / steps,
        "mean_importance_correction": float(np.mean(corrections)) if corrections else 1.0,
        "final_reward_loss": float(np.mean(losses[-20:])),
        "guided_rollouts": off_context,
        "target_objective_uses_original_prompt": off_context,
    }


def run_comparison(train, test, steps: int, seed: int):
    baseline_weights, baseline_training = train_grpo(train, steps, seed, off_context=False)
    method_weights, method_training = train_grpo(train, steps, seed, off_context=True)
    return (
        _evaluate(baseline_weights, test),
        _evaluate(method_weights, test),
        baseline_training,
        method_training,
    )
