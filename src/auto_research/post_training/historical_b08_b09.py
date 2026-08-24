"""B08--B09 post-training objectives on the shared candidate-policy runner."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {
    "r2-opd", "sr-opsd", "opd2", "causal-opd", "smopd", "rstg",
    "sa-mrpo", "rubric-dropout", "erils", "crpo", "serpo", "iso-rlvr",
}


def _policy_gradient(features, probabilities, sampled, advantages):
    expected = probabilities @ features
    terms = [
        float(advantage) * (features[index] - expected)
        for index, advantage in zip(sampled, advantages)
    ]
    return np.mean(terms, axis=0)


def _normalize(values):
    return (values - values.mean()) / (values.std() + 1e-6)


def update_historical(
    algorithm, state, group, probabilities, reference,
    rollout_probabilities, sampled, rng,
):
    features = group.features
    rewards = group.rewards[sampled]
    scalar = rewards @ np.asarray((.70, .05, .20, .05))
    base_advantage = _normalize(scalar)
    teacher = np.clip(.60 * rewards[:, 0] + .25 * rewards[:, 2] + .15, 0, 1)
    student = probabilities[sampled]
    diagnostics = {"mechanism_id": float(sorted(ALGORITHMS).index(algorithm) + 1)}

    if algorithm == "r2-opd":
        progress = rewards[:, 2] + .25 * rewards[:, 0]
        teacher_rank = np.argsort(np.argsort(teacher))
        progress_rank = np.argsort(np.argsort(progress))
        mask = (np.sign(teacher_rank - np.median(teacher_rank)) == np.sign(progress_rank - np.median(progress_rank))).astype(float)
        advantages = base_advantage + mask * _normalize(teacher - student)
        diagnostics["filtered_conflicts"] = float(np.sum(1 - mask))
    elif algorithm == "sr-opsd":
        beta, alpha = .65, .7
        target = teacher**beta * reference[sampled] ** (1 - beta)
        density = np.clip(target / np.maximum(student, 1e-8), .1, 10)
        renyi = (density ** (alpha - 1) - 1) / (alpha - 1)
        advantages = base_advantage + _normalize(target - student) / (1 + np.abs(renyi))
        diagnostics.update(target_interpolation=beta, renyi_order=alpha)
    elif algorithm == "opd2":
        base_teacher = np.clip(.5 * rewards[:, 0] + .5 * reference[sampled], 1e-6, 1)
        delta = np.log(teacher + 1e-6) - np.log(base_teacher)
        advantages = base_advantage + _normalize(delta)
        diagnostics["teacher_delta_mean"] = float(delta.mean())
    elif algorithm == "causal-opd":
        path = np.cumsum(rewards[:, :3], axis=1)
        first_wrong = np.argmax(path < np.maximum.accumulate(path, axis=1), axis=1)
        stage_weight = 1.0 + (2 - first_wrong) / 3
        advantages = base_advantage * stage_weight + _normalize(teacher - student)
        diagnostics["first_wrong_step_mean"] = float(first_wrong.mean())
    elif algorithm == "smopd":
        specialized = np.stack([
            _normalize(rewards[:, axis]) for axis in range(rewards.shape[1])
        ])
        reliability = 1.0 / (rewards.std(0) + .2)
        reliability /= reliability.sum()
        advantages = base_advantage + reliability @ specialized
        diagnostics["specialized_teachers"] = float(rewards.shape[1])
    elif algorithm == "rstg":
        negative_group = float(np.max(scalar) < .65 or np.std(scalar) < .08)
        entropy = -np.log(np.maximum(student, 1e-8))
        token_mask = (entropy >= np.median(entropy)).astype(float)
        advantages = base_advantage + negative_group * token_mask * _normalize(teacher - student)
        diagnostics.update(negative_group=negative_group, selected_tokens=float(token_mask.sum()))
    elif algorithm == "sa-mrpo":
        normalized = np.stack([_normalize(rewards[:, axis]) for axis in range(rewards.shape[1])])
        saturation = np.clip(rewards.mean(0), 0, 1)
        weights = (1 - saturation) / np.maximum((1 - saturation).sum(), 1e-8)
        advantages = weights @ normalized
        diagnostics["unsaturated_weight_max"] = float(weights.max())
    elif algorithm == "rubric-dropout":
        mask = (rng.random(rewards.shape[1]) > .4).astype(float)
        if not mask.any():
            mask[0] = 1
        advantages = _normalize(rewards @ mask)
        diagnostics["rubrics_retained"] = float(mask.sum())
    elif algorithm == "erils":
        external = np.arange(len(sampled)) % 2 == 1
        advantages = np.zeros(len(sampled))
        advantages[~external] = _normalize(scalar[~external]) if (~external).sum() > 1 else 0
        advantages[external] = _normalize(scalar[external] + .1) if external.sum() > 1 else 0
        advantages[external] *= .8
        diagnostics["external_rollout_fraction"] = float(external.mean())
    elif algorithm == "crpo":
        entropy = -np.log(np.maximum(student, 1e-8))
        positive = entropy >= np.median(entropy)
        contrast = np.where(positive, teacher - student, student - teacher)
        advantages = base_advantage + _normalize(contrast)
        diagnostics["reflective_positions"] = float(positive.sum())
    elif algorithm == "serpo":
        archive = np.argsort(scalar)
        good, bad = archive[-1], archive[0]
        rubric = np.abs(rewards[good] - rewards[bad])
        rubric /= np.maximum(rubric.sum(), 1e-8)
        advantages = _normalize(rewards @ rubric)
        state.reward_axis_weights = rubric
        diagnostics["rubric_margin"] = float(np.sum(np.abs(rewards[good] - rewards[bad])))
    elif algorithm == "iso-rlvr":
        advantages = base_advantage
    else:
        raise ValueError(f"unknown historical post-training algorithm: {algorithm}")

    gradient = _policy_gradient(features, probabilities, sampled, advantages)
    if algorithm == "iso-rlvr":
        # Freeze the empirical singular spectrum proxy and update only the two
        # frame complements of the rollout feature covariance.
        _u, _s, vh = np.linalg.svd(features, full_matrices=False)
        frame = vh[: max(1, min(2, vh.shape[0]))].T
        gradient = gradient - frame @ (frame.T @ gradient) * .35
        diagnostics["fixed_spectrum_rank"] = float(len(_s))
    gradient -= .02 * (features.T @ (probabilities - reference))
    loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
    diagnostics["advantage_std"] = float(np.std(advantages))
    return gradient, loss, diagnostics
