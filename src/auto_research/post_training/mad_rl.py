"""MaD-RL reward kernels and a small, auditable synthetic-choice experiment.

The reward equations match Table 1 of the Meta paper. The local policy is a
one-token character LM, *not* the paper's Qwen3-4B checkpoint.
"""

from __future__ import annotations

import json
from pathlib import Path
import random

import numpy as np


CHOICES = "ABCDE"
TOPICS = (
    ("oceans", "Pacific", "Atlantic", "Indian", "Southern", "Arctic"),
    ("continents", "Africa", "Asia", "Europe", "Australia", "Antarctica"),
    ("planets", "Mercury", "Venus", "Earth", "Mars", "Jupiter"),
    ("metals", "Iron", "Copper", "Silver", "Gold", "Tin"),
    ("trees", "Oak", "Pine", "Maple", "Birch", "Cedar"),
    ("colors", "Red", "Blue", "Green", "Yellow", "Purple"),
    ("instruments", "Piano", "Violin", "Flute", "Drum", "Guitar"),
    ("birds", "Eagle", "Owl", "Swan", "Robin", "Sparrow"),
    ("languages", "English", "Spanish", "French", "Hindi", "Chinese"),
    ("shapes", "Circle", "Square", "Triangle", "Oval", "Hexagon"),
    ("sports", "Tennis", "Football", "Cricket", "Rugby", "Hockey"),
    ("fruits", "Apple", "Banana", "Orange", "Pear", "Peach"),
)
TEMPLATES = (
    "Choose one {topic}. {options} Answer with its letter:",
    "Name a {topic} from this list: {options} Letter:",
    "Pick any valid {topic}. Options: {options} Choice:",
)


def validate_target(target) -> np.ndarray:
    values = np.asarray(target, dtype=np.float64)
    if values.shape != (5,) or not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("target must contain five finite nonnegative probabilities")
    if not np.isclose(values.sum(), 1.0, atol=1e-8):
        raise ValueError("target probabilities must sum to one")
    return values


def distribution_rewards(categories, target, divergence: str, *, epsilon=1e-6):
    """Table 1 plug-in rewards; invalid outputs retain the full denominator.

    ``categories`` contains 0..4 or None. The fixed invalid penalty is a
    local protocol choice, not a distributional-gradient identity.
    """
    if divergence not in {"correctness", "l2", "forward-kl", "reverse-kl", "jsd"}:
        raise ValueError(f"unknown MaD-RL divergence: {divergence}")
    target = validate_target(target)
    if not categories:
        raise ValueError("at least one sampled output is required")
    if any(category is not None and category not in range(5) for category in categories):
        raise ValueError("category must be 0..4 or None")
    frequencies = np.bincount(
        [category for category in categories if category is not None], minlength=5,
    ).astype(np.float64) / len(categories)
    safe_frequency = np.maximum(frequencies, epsilon)
    # Reverse KL has a singularity at a zero target; use the paper's
    # epsilon-smoothed target for the truncated-target experiment.
    safe_target = np.maximum(target, epsilon)
    if divergence == "correctness":
        by_category = np.ones(5)
    elif divergence == "l2":
        by_category = target - frequencies
    elif divergence == "forward-kl":
        by_category = target / safe_frequency - 1.0
    elif divergence == "reverse-kl":
        by_category = np.log(safe_target) - np.log(safe_frequency)
    else:
        mixture = (target + frequencies) / 2.0
        by_category = 0.5 * (np.log(np.maximum(mixture, epsilon)) - np.log(safe_frequency))
    return np.asarray([
        -1.0 if category is None else by_category[category]
        for category in categories
    ]), frequencies


def jensen_shannon(observed, target) -> float:
    target = validate_target(target)
    observed = np.asarray(observed, dtype=np.float64)
    if observed.shape != (5,) or (observed < 0).any() or not np.isclose(observed.sum(), 1.0):
        raise ValueError("observed distribution must have five normalized bins")
    midpoint = (observed + target) / 2
    def kl(left):
        nonzero = left > 0
        return float(np.sum(left[nonzero] * np.log(left[nonzero] / midpoint[nonzero])))
    return 0.5 * (kl(target) + kl(observed))


def _prompts(topics):
    for topic, *names in topics:
        options = "; ".join(f"{letter}: {name}" for letter, name in zip(CHOICES, names, strict=True))
        for template in TEMPLATES:
            yield template.format(topic=topic, options=options)


def _evaluate(policy, tokenizer, prompts, target, seed, samples_per_prompt, device):
    import torch

    # Evaluation samples from CPU probabilities on every accelerator.
    rng = torch.Generator(device="cpu").manual_seed(seed)
    counts = np.zeros(5, dtype=np.int64)
    invalid = 0
    policy.eval()
    with torch.no_grad():
        for prompt in prompts:
            inputs = torch.tensor(
                [[tokenizer.bos_id, *tokenizer.encode(prompt), tokenizer.sep_id]],
                device=device,
            )
            logits, _ = policy(inputs)
            probabilities = logits[0, -1].softmax(-1).cpu()
            sampled = torch.multinomial(probabilities, samples_per_prompt, replacement=True, generator=rng)
            for token in sampled.tolist():
                text = tokenizer.decode([token])
                if text in CHOICES:
                    counts[CHOICES.index(text)] += 1
                else:
                    invalid += 1
    valid = int(counts.sum())
    observed = counts / valid if valid else np.ones(5) / 5
    return {
        "valid_rate": valid / (valid + invalid),
        "off_support_rate": invalid / (valid + invalid),
        "category_counts": counts.tolist(),
        "category_distribution_valid_only": observed.tolist(),
        "jsd_to_target_valid_only": jensen_shannon(observed, target) if valid else None,
        "valid_samples": valid,
    }


def run_choice_seed(*, seed: int, divergence: str, target, steps: int = 60,
                    group_size: int = 16, learning_rate: float = 0.003,
                    samples_per_prompt: int = 32):
    """One-token free sampling with group-relative, clipped, KL-regularized RL.

    All five answers are valid. Topic-held-out validation is not used for
    model or hyperparameter selection; test is read only after training.
    """
    import torch
    from copy import deepcopy

    from ..runtime import device_for
    from .generation import CharacterTokenizer, build_policy

    target = validate_target(target)
    if steps < 1 or group_size < 2 or samples_per_prompt < 1:
        raise ValueError("steps, group size and evaluation samples must be positive")
    if learning_rate <= 0:
        raise ValueError("learning rate must be positive")
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.set_num_threads(min(torch.get_num_threads(), 2))
    train_prompts = tuple(_prompts(TOPICS[:8]))
    validation_prompts = tuple(_prompts(TOPICS[8:10]))
    test_prompts = tuple(_prompts(TOPICS[10:]))
    tokenizer = CharacterTokenizer([*train_prompts, *CHOICES])
    device = device_for(torch)
    policy = build_policy(len(tokenizer), dimensions=32).to(device)
    optimizer = torch.optim.AdamW(policy.parameters(), lr=learning_rate)
    rng = random.Random(seed)

    # Short balanced SFT warm start, like the paper's category-coverage init.
    for warmup in range(50):
        prompt = train_prompts[warmup % len(train_prompts)]
        letter = CHOICES[warmup % 5]
        inputs = torch.tensor([[tokenizer.bos_id, *tokenizer.encode(prompt), tokenizer.sep_id]], device=device)
        logits, _ = policy(inputs)
        label = torch.tensor([tokenizer.token_to_id[letter]], device=device)
        loss = torch.nn.functional.cross_entropy(logits[:, -1], label)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
    reference = deepcopy(policy).eval()
    baseline = _evaluate(policy, tokenizer, validation_prompts, target, seed + 1000, samples_per_prompt, device)
    history = []
    for step in range(steps):
        prompt = train_prompts[rng.randrange(len(train_prompts))]
        inputs = torch.tensor([[tokenizer.bos_id, *tokenizer.encode(prompt), tokenizer.sep_id]], device=device)
        with torch.no_grad():
            old_logits, _ = policy(inputs)
            old_distribution = old_logits[0, -1].softmax(-1)
            sampled = torch.multinomial(old_distribution, group_size, replacement=True)
            categories = [
                CHOICES.index(text) if text in CHOICES else None
                for text in (tokenizer.decode([token]) for token in sampled.tolist())
            ]
            reward, frequencies = distribution_rewards(categories, target, divergence)
            advantage = torch.tensor(reward, dtype=torch.float32, device=device)
            advantage = (advantage - advantage.mean()) / advantage.std(unbiased=False).clamp_min(1e-6)
            old_logps = old_distribution.log()[sampled]
            ref_logits, _ = reference(inputs)
            ref_distribution = ref_logits[0, -1].softmax(-1)
        for _ in range(2):
            logits, _ = policy(inputs)
            distribution = logits[0, -1].softmax(-1)
            ratio = (distribution.log()[sampled] - old_logps).exp()
            surrogate = torch.minimum(ratio * advantage, ratio.clamp(0.8, 1.2) * advantage)
            kl = torch.sum(distribution * (distribution.log() - ref_distribution.log()))
            loss = -surrogate.mean() + 0.04 * kl
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
            optimizer.step()
        if step == 0 or (step + 1) % max(1, steps // 5) == 0:
            history.append({
                "step": step + 1, "loss": float(loss.detach().cpu()),
                "valid_rollout_fraction": sum(category is not None for category in categories) / group_size,
                "group_frequencies_full_denominator": frequencies.tolist(),
            })
    validation = _evaluate(policy, tokenizer, validation_prompts, target, seed + 1000, samples_per_prompt, device)
    baseline_test = _evaluate(reference, tokenizer, test_prompts, target, seed + 2000, samples_per_prompt, device)
    test = _evaluate(policy, tokenizer, test_prompts, target, seed + 2000, samples_per_prompt, device)
    return {
        "seed": seed, "divergence": divergence, "target": target.tolist(),
        "baseline_validation": baseline, "final_validation": validation,
        "baseline_test_after_training": baseline_test,
        "final_test": test, "history": history,
        "protocol": {
            "model": "32-dimension one-token character GRU (not Qwen3-4B)",
            "train_topics": [row[0] for row in TOPICS[:8]],
            "validation_topics": [row[0] for row in TOPICS[8:10]],
            "test_topics": [row[0] for row in TOPICS[10:]],
            "sft_warmup_updates": 50, "rl_steps": steps, "group_size": group_size,
            "samples_per_eval_prompt": samples_per_prompt,
            "kl_coefficient": 0.04, "ppo_clip": 0.2,
            "diagnostic_only": True,
        },
    }


def run_choice_experiment(*, seeds=(42, 43, 44), divergences=("correctness", "l2", "forward-kl", "reverse-kl", "jsd"),
                          target=(0.0, 0.0, 1/3, 1/3, 1/3), steps=60,
                          group_size=16, output_dir: Path):
    target = validate_target(target)
    if len(set(seeds)) != len(seeds):
        raise ValueError("seeds must be unique")
    if not seeds or not divergences or len(set(divergences)) != len(divergences):
        raise ValueError("nonempty unique seeds and divergences are required")
    runs = [run_choice_seed(
        seed=seed, divergence=divergence, target=target,
        steps=steps, group_size=group_size,
    ) for divergence in divergences for seed in seeds]
    summary = {}
    for divergence in divergences:
        subset = [row for row in runs if row["divergence"] == divergence]
        summary[divergence] = {
            "baseline_test_jsd_mean": float(np.mean([row["baseline_test_after_training"]["jsd_to_target_valid_only"] for row in subset])),
            "validation_jsd_mean": float(np.mean([row["final_validation"]["jsd_to_target_valid_only"] for row in subset])),
            "test_jsd_mean": float(np.mean([row["final_test"]["jsd_to_target_valid_only"] for row in subset])),
            "test_valid_rate_mean": float(np.mean([row["final_test"]["valid_rate"] for row in subset])),
        }
    payload = {
        "method": "mad-rl", "paper": "Meta MaD-RL, 2026-09-24",
        "target": target.tolist(), "seeds": list(seeds), "runs": runs,
        "summary": summary, "diagnostic_only": True,
        "conclusion_boundary": "Small-model synthetic choice mechanism; not a Qwen3-4B, GSM8K, MATH or CodeContests reproduction.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "metrics.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# MaD-RL 小模型机制对照", "", "仅验证分布奖励路径；不是论文大模型结果。test 只在训练结束后评估基线与终态。", "", "| 奖励 | 基线 test JSD↓ | 最终验证 JSD↓ | 最终 test JSD↓ | test 有效率↑ |", "|---|---:|---:|---:|---:|"]
    for name, row in summary.items():
        lines.append(f"| {name} | {row['baseline_test_jsd_mean']:.4f} | {row['validation_jsd_mean']:.4f} | {row['test_jsd_mean']:.4f} | {row['test_valid_rate_mean']:.4f} |")
    (output_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload, output_dir
