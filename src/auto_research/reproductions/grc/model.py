from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, hierarchical_codes, softmax


def train_grc(data, seed: int):
    rng = np.random.default_rng(seed)
    codes = hierarchical_codes(data.sequences.features, seed=seed)
    draft = data.transition.copy()
    corrected = draft.copy()
    location_counts = np.ones((codes.shape[1] + 1, codes.shape[1] + 1))
    semantic_correct = np.ones((data.domains.max() + 1, 2))
    trajectories = 0
    # Structured SFT targets: draft SID, first mismatch, semantic consistency, corrected SID.
    for history, target in zip(data.sequences.train, data.sequences.validation):
        source = history[-1]
        candidates = np.argsort(-draft[source])[:6]
        for candidate in candidates:
            mismatch = np.flatnonzero(codes[candidate] != codes[target])
            location = int(mismatch[0]) if mismatch.size else codes.shape[1]
            location_counts[min(data.domains[source], location_counts.shape[0] - 1), location] += 1
            same_domain = int(data.domains[candidate] == data.domains[target])
            semantic_correct[data.domains[candidate], same_domain] += 1
            corrected[source, target] += 1.0 + 0.5 * (codes[candidate] == codes[target]).sum()
            trajectories += 1
    corrected /= corrected.sum(1, keepdims=True)
    # GRPO over complete generate-reflect-correct trajectories.
    old = corrected.copy()
    reward_trace = []
    for _ in range(10):
        rewards = []
        for history, target in zip(data.sequences.train, data.sequences.validation):
            source = history[-1]
            group = rng.choice(data.item_count, 4, p=old[source])
            group_reward = []
            for candidate in group:
                draft_hit = (codes[candidate] == codes[target]).sum()
                final = target if rng.random() < corrected[source, target] else candidate
                final_hit = (codes[final] == codes[target]).sum()
                reflection = float(data.domains[candidate] == data.domains[target])
                group_reward.append(draft_hit + 2.0 * final_hit + reflection + max(final_hit - draft_hit, 0))
            group_reward = np.asarray(group_reward, dtype=float)
            advantage = (group_reward - group_reward.mean()) / max(group_reward.std(), 1e-6)
            for item, adv in zip(group, advantage):
                ratio = corrected[source, item] / max(old[source, item], 1e-9)
                corrected[source, item] *= np.exp(0.015 * min(ratio * adv, np.clip(ratio, .8, 1.2) * adv))
            corrected[source] /= corrected[source].sum()
            rewards.extend(group_reward.tolist())
        reward_trace.append(float(np.mean(rewards)))
        old = 0.9 * old + 0.1 * corrected
    return codes, location_counts, semantic_correct, corrected, {"structured_sft_trajectories": trajectories, "template_tokens": 2 * codes.shape[1] + 1 + 4, "grpo_reward_initial": reward_trace[0], "grpo_reward_final": reward_trace[-1], "grpo_iterations": 10, "egrs": True}


def score_grc(data, codes, location, semantic, corrected, history):
    source = history[-1]
    initial = 0.55 * base_scores(data, history) + 0.45 * data.transition[source]
    beams = np.argsort(-initial)[:12]
    entropy = []
    for item in beams:
        loc = softmax(location[min(data.domains[source], location.shape[0] - 1)])
        sem = softmax(semantic[data.domains[item]])
        entropy.append(float(-(loc * np.log(np.maximum(loc, 1e-12))).sum() - (sem * np.log(np.maximum(sem, 1e-12))).sum()))
    scheduled = set(beams[np.argsort(-np.asarray(entropy))[:6]].tolist())
    scores = initial.copy()
    for item in scheduled:
        scores[item] = 0.35 * initial[item] + 0.65 * corrected[source, item]
    return scores
