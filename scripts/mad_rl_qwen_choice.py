"""Qwen3-4B MaD-RL distribution-reward diagnostic on public synthetic choices.

This is a real-checkpoint, trainable one-token policy, *not* the paper's
multilingual GSM8K/CodeContests experiment or full free-generation protocol.
The official paper's category rewards are reused without forced valid-token
renormalization: off-support tokens keep the full group denominator.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

import numpy as np

from auto_research.post_training.local_lora import attach_lora, disabled_adapters
from auto_research.post_training.mad_rl import (
    CHOICES, TOPICS, distribution_rewards, jensen_shannon,
)


QWEN_ID = "Qwen/Qwen3-4B-Instruct-2507"
QWEN_REVISION = "cdbee75f17c01a7cc42f958dc650907174af0554"
TARGET = (0.0, 0.0, 1 / 3, 1 / 3, 1 / 3)


def prompt_ids(tokenizer, topic_row):
    topic, *names = topic_row
    options = "; ".join(
        f"{letter}: {name}" for letter, name in zip(CHOICES, names, strict=True)
    )
    message = (
        f"Pick one {topic} from the following list. All five are acceptable. "
        f"{options}\nAnswer with exactly one letter A, B, C, D, or E.\nChoice:"
    )
    return tokenizer.apply_chat_template(
        [{"role": "user", "content": message}], tokenize=True,
        add_generation_prompt=True, enable_thinking=False,
    )


def _category(tokenizer, token):
    text = tokenizer.decode([int(token)], skip_special_tokens=True).strip()
    return CHOICES.index(text) if text in CHOICES else None


def _distribution(model, ids, torch):
    sequence = torch.tensor([ids], device=next(model.parameters()).device)
    return model(input_ids=sequence, attention_mask=torch.ones_like(sequence), use_cache=False).logits[0, -1].float()


def _evaluate(model, tokenizer, prompts, *, samples, seed, target, torch):
    generator = torch.Generator(device="cpu").manual_seed(seed)
    counts = np.zeros(5, dtype=np.int64)
    invalid = 0
    model.eval()
    with torch.no_grad():
        for ids in prompts:
            probabilities = _distribution(model, ids, torch).softmax(-1).cpu()
            drawn = torch.multinomial(probabilities, samples, replacement=True, generator=generator)
            for token in drawn.tolist():
                category = _category(tokenizer, token)
                if category is None:
                    invalid += 1
                else:
                    counts[category] += 1
    valid = int(counts.sum())
    observed = counts / valid if valid else np.ones(5) / 5
    return {
        "counts": counts.tolist(), "valid_rate": valid / (valid + invalid),
        "off_support_rate": invalid / (valid + invalid),
        "distribution_valid_only": observed.tolist(),
        "jsd_to_target_valid_only": jensen_shannon(observed, target) if valid else None,
        "samples": valid + invalid,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--group-size", type=int, default=16)
    parser.add_argument("--eval-samples", type=int, default=16)
    parser.add_argument("--warmup-steps", type=int, default=15)
    parser.add_argument("--divergence", choices=("l2", "forward-kl", "reverse-kl", "jsd"), default="jsd")
    args = parser.parse_args()
    if min(args.steps, args.group_size, args.eval_samples, args.warmup_steps) < 1:
        parser.error("steps, group size, eval samples and warmup steps must be positive")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not torch.cuda.is_available():
        raise RuntimeError("Qwen3-4B MaD-RL checkpoint diagnostic requires CUDA")
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint, local_files_only=True, dtype=torch.bfloat16,
        attn_implementation="sdpa",
    ).to("cuda")
    model = attach_lora(model, target_modules=("q_proj", "v_proj"), rank=8, alpha=16)
    optimizer = torch.optim.AdamW(
        (parameter for parameter in model.parameters() if parameter.requires_grad), lr=2e-5,
    )
    train = [prompt_ids(tokenizer, row) for row in TOPICS[:8]]
    validation = [prompt_ids(tokenizer, row) for row in TOPICS[8:10]]
    test = [prompt_ids(tokenizer, row) for row in TOPICS[10:]]
    label_tokens = []
    for letter in CHOICES:
        tokens = tokenizer.encode(letter, add_special_tokens=False)
        if len(tokens) != 1:
            raise RuntimeError(f"{letter} is not a single tokenizer token")
        label_tokens.append(tokens[0])

    # Balanced SFT warm start: provides category coverage but is not paper-scale.
    model.train()
    for step in range(args.warmup_steps):
        logits = _distribution(model, train[step % len(train)], torch)
        label = torch.tensor([label_tokens[step % len(label_tokens)]], device="cuda")
        loss = torch.nn.functional.cross_entropy(logits[None], label)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
    baseline = _evaluate(
        model, tokenizer, validation, samples=args.eval_samples,
        seed=args.seed + 1000, target=TARGET, torch=torch,
    )
    initial_adapters = {
        name: parameter.detach().clone()
        for name, parameter in model.named_parameters() if parameter.requires_grad
    }
    history = []
    rng = random.Random(args.seed)
    for step in range(args.steps):
        ids = train[rng.randrange(len(train))]
        model.eval()
        with torch.no_grad():
            old_logits = _distribution(model, ids, torch)
            old_log_probabilities = old_logits.log_softmax(-1)
            old_probabilities = old_log_probabilities.exp()
            sampled = torch.multinomial(old_probabilities, args.group_size, replacement=True)
            categories = [_category(tokenizer, token) for token in sampled.tolist()]
            reward, frequencies = distribution_rewards(categories, TARGET, args.divergence)
            advantages = torch.tensor(reward, dtype=torch.float32, device="cuda")
            advantages = (advantages - advantages.mean()) / advantages.std(unbiased=False).clamp_min(1e-6)
            old_logp = old_log_probabilities[sampled]
            with disabled_adapters(model):
                reference_log_probabilities = _distribution(model, ids, torch).log_softmax(-1)
        model.train()
        logits = _distribution(model, ids, torch)
        log_probabilities = logits.log_softmax(-1)
        probabilities = log_probabilities.exp()
        ratio = (log_probabilities[sampled] - old_logp).exp()
        objective = torch.minimum(ratio * advantages, ratio.clamp(0.8, 1.2) * advantages)
        kl = torch.sum(probabilities * (log_probabilities - reference_log_probabilities))
        loss = -objective.mean() + 0.04 * kl
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            (parameter for parameter in model.parameters() if parameter.requires_grad), 1.0,
        )
        optimizer.step()
        history.append({
            "step": step + 1, "valid_fraction": sum(c is not None for c in categories) / len(categories),
            "group_frequencies_full_denominator": frequencies.tolist(),
            "loss": float(loss.detach()),
        })
    final_validation = _evaluate(
        model, tokenizer, validation, samples=args.eval_samples,
        seed=args.seed + 1000, target=TARGET, torch=torch,
    )
    final_test = _evaluate(
        model, tokenizer, test, samples=args.eval_samples,
        seed=args.seed + 2000, target=TARGET, torch=torch,
    )
    adapter_delta = sum(
        (parameter.detach() - initial_adapters[name]).square().sum().item()
        for name, parameter in model.named_parameters() if name in initial_adapters
    ) ** 0.5
    payload = {
        "schema_version": 1, "diagnostic_only": True, "paper_result_reproduced": False,
        "model_id": QWEN_ID, "model_revision": QWEN_REVISION,
        "seed": args.seed, "steps": args.steps, "group_size": args.group_size,
        "warmup_steps": args.warmup_steps, "divergence": args.divergence,
        "target": TARGET, "train_topics": [row[0] for row in TOPICS[:8]],
        "validation_topics": [row[0] for row in TOPICS[8:10]],
        "test_topics": [row[0] for row in TOPICS[10:]],
        "baseline_validation": baseline, "final_validation": final_validation,
        "final_test": final_test, "history": history,
        "adapter_parameter_delta_l2": adapter_delta,
        "accelerator_model": torch.cuda.get_device_name(0),
        "test_used_for_selection": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
