from __future__ import annotations

import numpy as np


def _sigmoid(value):
    return 1.0 / (1.0 + np.exp(-np.clip(value, -30, 30)))


def train_static_policy(examples, steps: int, seed: int):
    rng = np.random.default_rng(seed)
    policy = rng.normal(0.0, 0.02, examples[0]["candidate_vectors"].shape[1])
    static = np.asarray([0.20, 0.35, 0.20, 0.25])
    losses = []
    for _ in range(steps):
        row = examples[int(rng.integers(len(examples)))]
        good, bad = row["candidate_vectors"][0], row["candidate_vectors"][1]
        target_gap = float((row["rubrics"][0] - row["rubrics"][1]) @ static)
        probability = _sigmoid((good - bad) @ policy)
        loss = -np.log(max(probability, 1e-9))
        policy += 0.08 * max(target_gap, 0.1) * (1.0 - probability) * (good - bad)
        losses.append(loss)
    return policy, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:]))}


def train_dynamic_rubric(examples, steps: int, seed: int):
    rng = np.random.default_rng(seed)
    width = examples[0]["prompt_vector"].shape[0]
    policy = rng.normal(0.0, 0.02, width)
    generator = rng.normal(0.0, 0.02, (width, 4))
    anchor = np.asarray([0.20, 0.35, 0.20, 0.25])
    losses, gaps = [], []
    generations = max(2, steps // 20)
    per_generation = max(1, steps // generations)
    journal = []
    for generation in range(generations):
        generation_losses, generation_gaps = [], []
        for _ in range(per_generation):
            row = examples[int(rng.integers(len(examples)))]
            policy_scores = row["candidate_vectors"] @ policy
            hard_negative = 1 + int(np.argmax(policy_scores[1:]))
            context = row["prompt_vector"] + row["candidate_vectors"][[0, hard_negative]].mean(0)
            rubric_weights = _sigmoid(context @ generator)
            rubric_weights /= max(rubric_weights.sum(), 1e-9)
            rubric_gap = row["rubrics"][0] - row["rubrics"][hard_negative]
            evaluator_gap = float(rubric_gap @ rubric_weights)
            evaluator_probability = _sigmoid(evaluator_gap)
            evaluator_loss = -np.log(max(evaluator_probability, 1e-9))
            # Discriminability increases the current response-set gap; the
            # anchor term prevents arbitrary criteria from replacing quality.
            gradient_weights = (1.0 - evaluator_probability) * rubric_gap
            gradient_weights -= 0.10 * (rubric_weights - anchor)
            local = rubric_weights * (1.0 - rubric_weights) * gradient_weights
            generator += 0.04 * np.outer(context, local)
            difference = row["candidate_vectors"][0] - row["candidate_vectors"][hard_negative]
            policy_probability = _sigmoid(difference @ policy)
            policy += 0.08 * max(evaluator_gap, 0.05) * (1.0 - policy_probability) * difference
            generation_losses.append(evaluator_loss)
            generation_gaps.append(evaluator_gap)
        losses.extend(generation_losses)
        gaps.extend(generation_gaps)
        journal.append({
            "generation": generation + 1,
            "evaluator_loss": float(np.mean(generation_losses)),
            "relative_score_gap": float(np.mean(generation_gaps)),
        })
    return policy, generator, {
        "initial_evaluator_loss": float(np.mean(losses[:10])),
        "final_evaluator_loss": float(np.mean(losses[-10:])),
        "mean_relative_score_gap": float(np.mean(gaps[-min(20, len(gaps)):])),
        "co_evolution_journal": journal,
        "objectives": ["response-set discriminability", "anchor calibration"],
    }


def evaluate_policy(policy, examples):
    correct, margins = 0, []
    for row in examples:
        scores = row["candidate_vectors"] @ policy
        correct += int(np.argmax(scores) == row["gold"])
        margins.append(float(scores[0] - np.max(scores[1:])))
    return {
        "alpaca_preference_accuracy": correct / len(examples),
        "mean_good_vs_hard_negative_margin": float(np.mean(margins)),
        "examples": len(examples),
    }
