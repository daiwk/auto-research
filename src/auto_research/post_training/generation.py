from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import random
import re

import numpy as np

from ..datasets import gsm8k
from ..runtime import device_for


@dataclass(frozen=True)
class GenerationExample:
    prompt: str
    completion: str
    answer: str
    difficulty: float


@dataclass(frozen=True)
class GenerationSuite:
    train: tuple[GenerationExample, ...]
    validation: tuple[GenerationExample, ...]
    test: tuple[GenerationExample, ...]
    source: str


class CharacterTokenizer:
    """Small auditable tokenizer used by the local free-generation benchmark."""

    SPECIAL = ("<pad>", "<bos>", "<eos>", "<sep>", "<unk>")

    def __init__(self, texts):
        characters = sorted(set("".join(texts)))
        self.tokens = self.SPECIAL + tuple(characters)
        self.token_to_id = {token: index for index, token in enumerate(self.tokens)}
        self.pad_id, self.bos_id, self.eos_id, self.sep_id, self.unk_id = range(5)

    def encode(self, text: str) -> list[int]:
        return [self.token_to_id.get(character, self.unk_id) for character in text]

    def decode(self, ids) -> str:
        return "".join(
            self.tokens[int(index)] for index in ids
            if int(index) >= len(self.SPECIAL)
        )

    def sequence(self, example: GenerationExample) -> tuple[list[int], int]:
        prompt = [self.bos_id, *self.encode(example.prompt), self.sep_id]
        return [*prompt, *self.encode(example.completion), self.eos_id], len(prompt)

    def __len__(self):
        return len(self.tokens)


def load_generation_suite(
    dataset: str, root: Path, allow_network: bool, maximum_examples: int, seed: int
) -> GenerationSuite:
    if dataset == "gsm8k-generate":
        rows = gsm8k(root, allow_network)
        train = tuple(_gsm_example(row) for row in rows["train"][:maximum_examples])
        heldout = tuple(
            _gsm_example(row)
            for row in rows["test"][: max(48, maximum_examples // 2)]
        )
        middle = len(heldout) // 2
        return GenerationSuite(
            train, heldout[:middle], heldout[middle:],
            "OpenAI GSM8K official JSONL; model emits unrestricted token sequences",
        )
    rng = random.Random(seed)
    train = tuple(_arithmetic_example(rng, index) for index in range(maximum_examples))
    validation = tuple(
        _arithmetic_example(random.Random(seed + 10_000), index)
        for index in range(max(48, maximum_examples // 3))
    )
    test = tuple(
        _arithmetic_example(random.Random(seed + 20_000), index)
        for index in range(max(48, maximum_examples // 3))
    )
    return GenerationSuite(
        train, validation, test,
        "deterministic arithmetic free-generation suite with exact-answer verifier",
    )


def _arithmetic_example(rng: random.Random, index: int) -> GenerationExample:
    # Include the index in the RNG stream while keeping every split reproducible.
    for _ in range(index % 5 + 1):
        a, b = rng.randint(1, 30), rng.randint(1, 20)
    operator = ("+", "-", "*")[index % 3]
    value = a + b if operator == "+" else a - b if operator == "-" else a * b
    prompt = f"Problem: {a} {operator} {b}\nShow concise reasoning, then write Answer:"
    completion = f" {a} {operator} {b} = {value}. Answer: {value}"
    difficulty = min(1.0, (abs(value) + (20 if operator == "*" else 0)) / 300)
    return GenerationExample(prompt, completion, str(value), difficulty)


def _gsm_example(row) -> GenerationExample:
    match = re.search(r"####\s*(-?[\d,]+(?:\.\d+)?)", row["answer"])
    answer = match.group(1).replace(",", "") if match else ""
    reasoning = row["answer"].split("####", 1)[0].strip()
    return GenerationExample(
        f"Problem: {row['question']}\nShow concise reasoning, then write Answer:",
        f" {reasoning} Answer: {answer}",
        answer,
        min(1.0, len(row["question"]) / 300),
    )


def build_policy(vocabulary: int, dimensions: int = 64):
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError("free-generation post-training requires the neural-recs extra") from exc

    class TinyCausalPolicy(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(vocabulary, dimensions)
            self.recurrent = nn.GRU(dimensions, dimensions, batch_first=True)
            self.output = nn.Linear(dimensions, vocabulary)

        def forward(self, tokens, hidden=None):
            values, hidden = self.recurrent(self.embedding(tokens), hidden)
            return self.output(values), hidden

    return TinyCausalPolicy()


def train_free_generation(
    algorithm: str,
    suite: GenerationSuite,
    steps: int,
    learning_rate: float,
    group_size: int,
    seed: int,
    target: str = "validation",
    teacher=None,
    teacher_cache_path: Path | None = None,
    boundary_cache_path: Path | None = None,
    boundary_samples: int = 8,
    teacher_input_cost_per_million: float = 0.0,
    teacher_output_cost_per_million: float = 0.0,
):
    import torch

    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    all_examples = (*suite.train, *suite.validation, *suite.test)
    tokenizer = CharacterTokenizer(
        [text for row in all_examples for text in (row.prompt, row.completion)]
    )
    device = device_for(torch)
    policy = build_policy(len(tokenizer)).to(device)
    optimizer = torch.optim.AdamW(policy.parameters(), lr=min(learning_rate, 3e-3))
    rng = random.Random(seed)
    warmup_steps = max(20, min(80, steps))
    warmup_losses = []
    policy.train()
    for _ in range(warmup_steps):
        example = suite.train[rng.randrange(len(suite.train))]
        loss = _completion_nll(policy, tokenizer, example, device)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
        optimizer.step()
        warmup_losses.append(float(loss.detach().cpu()))
    reference = deepcopy(policy).eval()
    for parameter in reference.parameters():
        parameter.requires_grad_(False)
    baseline = evaluate_generation(
        policy, tokenizer, getattr(suite, target), device, seed
    )
    baseline_boundary_curve = (
        evaluate_pass_at_k(
            policy, tokenizer, getattr(suite, target), device, seed,
            (1, 2, 4, boundary_samples),
        )
        if algorithm == "coba-rl" and teacher is not None else {}
    )

    boundary_rows = {}
    if algorithm == "coba-rl" and teacher is not None:
        boundary_rows = _boundary_pass_at_k(
            policy, tokenizer, suite.train, device, seed,
            boundary_samples, boundary_cache_path,
        )
    teacher_cache = _load_teacher_cache(teacher_cache_path, teacher)
    teacher_calls = teacher_cache_hits = teacher_input_tokens = teacher_output_tokens = 0

    history, boundary = [], 0.5
    for step in range(steps):
        if algorithm == "coba-rl":
            candidates = [suite.train[rng.randrange(len(suite.train))] for _ in range(8)]
            example = min(candidates, key=lambda row: abs(
                boundary_rows.get(_prompt_key(row.prompt), {}).get(
                    "pass_rate", row.difficulty
                ) - boundary
            ))
        else:
            example = suite.train[rng.randrange(len(suite.train))]
        rollouts = [
            generate(policy, tokenizer, example.prompt, device, rng, sample=True)
            for _ in range(max(2, group_size))
        ]
        verified = [
            verify_completion(text, example.answer) for text in rollouts
        ]
        rewards = np.asarray([row[0] for row in verified], dtype=np.float32)
        exacts = np.asarray(
            [row[1]["exact"] for row in verified], dtype=np.float32
        )
        chosen = example.completion
        rejected = rollouts[int(np.argmin(rewards))]
        if algorithm == "ipo":
            loss = _ipo_loss(
                policy, reference, tokenizer, example.prompt, chosen, rejected, device
            )
            diagnostic = {"preference_gap_target": 5.0}
        elif algorithm == "simpo":
            loss = _simpo_loss(
                policy, tokenizer, example.prompt, chosen, rejected, device
            )
            diagnostic = {"length_normalized": 1.0, "reference_model": 0.0}
        else:
            loss, diagnostic = _sequence_rl_loss(
                policy, reference, tokenizer, example.prompt, rollouts,
                rewards, device, length_unbiased=algorithm == "luspo",
            )
            if algorithm == "coba-rl":
                pass_rate = float(rewards.mean())
                boundary = float(np.clip(
                    0.9 * boundary + 0.1 * (
                        example.difficulty + (0.08 if pass_rate > 0.5 else -0.04)
                    ), 0.05, 1.0,
                ))
                diagnostic.update({
                    "curriculum_boundary": boundary,
                    "teacher_guidance": float(exacts.max() == 0),
                })
                if teacher is not None and exacts.max() == 0:
                    key = _prompt_key(example.prompt)
                    cached = teacher_cache.get(key)
                    if cached is None:
                        completion = teacher.complete(example.prompt)
                        cached = {
                            "text": completion.text,
                            "input_tokens": completion.input_tokens,
                            "output_tokens": completion.output_tokens,
                        }
                        teacher_cache[key] = cached
                        teacher_calls += 1
                        teacher_input_tokens += completion.input_tokens
                        teacher_output_tokens += completion.output_tokens
                        _write_teacher_cache(teacher_cache_path, teacher, teacher_cache)
                    else:
                        teacher_cache_hits += 1
                    teacher_example = GenerationExample(
                        example.prompt, cached["text"], example.answer,
                        example.difficulty,
                    )
                    teacher_loss = _completion_nll(
                        policy, tokenizer, teacher_example, device
                    )
                    loss = loss + 0.25 * teacher_loss
                    teacher_reward, teacher_checks = verify_completion(
                        cached["text"], example.answer
                    )
                    diagnostic.update({
                        "real_teacher_used": 1.0,
                        "teacher_exact": float(teacher_checks["exact"]),
                        "teacher_reward": float(teacher_reward),
                        "teacher_sft_weight": 0.25,
                    })
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
        optimizer.step()
        if step == 0 or (step + 1) % max(1, steps // 5) == 0:
            history.append({
                "step": step + 1,
                "loss": float(loss.detach().cpu()),
                "rollout_reward": float(rewards.mean()),
                **diagnostic,
            })
    final = evaluate_generation(
        policy, tokenizer, getattr(suite, target), device, seed + 1
    )
    final_boundary_curve = (
        evaluate_pass_at_k(
            policy, tokenizer, getattr(suite, target), device, seed + 1,
            (1, 2, 4, boundary_samples),
        )
        if algorithm == "coba-rl" and teacher is not None else {}
    )
    teacher_cost = (
        teacher_input_tokens * teacher_input_cost_per_million
        + teacher_output_tokens * teacher_output_cost_per_million
    ) / 1_000_000
    return baseline, final, {
        "seed": seed,
        "tokenizer": "auditable character tokenizer",
        "vocabulary_size": len(tokenizer),
        "model": "GRU causal LM",
        "parameters": sum(parameter.numel() for parameter in policy.parameters()),
        "warmup_steps": warmup_steps,
        "warmup_initial_loss": warmup_losses[0],
        "warmup_final_loss": warmup_losses[-1],
        "rl_steps": steps,
        "free_generation": True,
        "verifier": "exact final numeric answer + format/length diagnostics",
        "boundary_cache": {
            "enabled": bool(boundary_rows),
            "entries": len(boundary_rows),
            "samples_per_example": boundary_samples if boundary_rows else 0,
            "pass_at_k": float(np.mean([
                row["pass_at_k"] for row in boundary_rows.values()
            ])) if boundary_rows else None,
        },
        "teacher": {
            "enabled": teacher is not None,
            "actual_calls": teacher_calls,
            "cache_hits": teacher_cache_hits,
            "input_tokens": teacher_input_tokens,
            "output_tokens": teacher_output_tokens,
            "estimated_cost": teacher_cost,
            "input_cost_per_million": teacher_input_cost_per_million,
            "output_cost_per_million": teacher_output_cost_per_million,
            "provenance": teacher.provenance() if teacher is not None else None,
        },
        "capability_boundary_curve": {
            "baseline_pass_at_k": baseline_boundary_curve,
            "final_pass_at_k": final_boundary_curve,
        },
        "history": history,
    }


def _boundary_pass_at_k(
    policy, tokenizer, examples, device, seed, samples, cache_path,
):
    fingerprint = hashlib.sha256(json.dumps({
        "seed": seed,
        "samples": samples,
        "prompts": [row.prompt for row in examples],
    }, sort_keys=True).encode()).hexdigest()
    if cache_path and cache_path.exists():
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if payload.get("fingerprint") != fingerprint:
            raise ValueError("CoBA-RL boundary cache fingerprint mismatch")
        return payload["entries"]
    rng = random.Random(seed + 31_337)
    entries = {}
    for example in examples:
        exact = []
        for _ in range(samples):
            text = generate(policy, tokenizer, example.prompt, device, rng, sample=True)
            exact.append(verify_completion(text, example.answer)[1]["exact"])
        entries[_prompt_key(example.prompt)] = {
            "pass_rate": float(np.mean(exact)),
            "pass_at_k": float(any(exact)),
            "samples": samples,
        }
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        _write_json(cache_path, {"fingerprint": fingerprint, "entries": entries})
    return entries


def _load_teacher_cache(path, teacher):
    if path is None or not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if teacher is None:
        raise ValueError("teacher cache provided without a real teacher")
    if (
        payload.get("teacher_model_id") != teacher.model_id
        or payload.get("teacher_revision") != teacher.requested_revision
    ):
        raise ValueError("CoBA-RL teacher cache fingerprint mismatch")
    return payload.get("entries", {})


def _write_teacher_cache(path, teacher, entries):
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(path, {
        "teacher_model_id": teacher.model_id,
        "teacher_revision": teacher.requested_revision,
        "entries": entries,
    })


def _prompt_key(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()


def _write_json(path, payload):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _completion_nll(model, tokenizer, example, device):
    import torch

    sequence, prompt_length = tokenizer.sequence(example)
    tokens = torch.tensor([sequence], dtype=torch.long, device=device)
    logits, _ = model(tokens[:, :-1])
    targets = tokens[:, 1:]
    loss = torch.nn.functional.cross_entropy(
        logits.flatten(0, 1), targets.flatten(), reduction="none"
    )
    mask = torch.arange(targets.shape[1], device=device) >= prompt_length - 1
    return (loss * mask).sum() / mask.sum().clamp_min(1)


def _text_logprob(model, tokenizer, prompt, completion, device, normalize=False):
    import torch

    prefix = [tokenizer.bos_id, *tokenizer.encode(prompt), tokenizer.sep_id]
    output = [*tokenizer.encode(completion), tokenizer.eos_id]
    tokens = torch.tensor([[*prefix, *output]], dtype=torch.long, device=device)
    logits, _ = model(tokens[:, :-1])
    log_probs = torch.log_softmax(logits, -1)
    targets = tokens[:, 1:]
    selected = log_probs.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
    values = selected[:, len(prefix) - 1:].sum()
    return values / max(1, len(output)) if normalize else values


def _ipo_loss(policy, reference, tokenizer, prompt, chosen, rejected, device):
    import torch

    policy_gap = (
        _text_logprob(policy, tokenizer, prompt, chosen, device)
        - _text_logprob(policy, tokenizer, prompt, rejected, device)
    )
    with torch.no_grad():
        reference_gap = (
            _text_logprob(reference, tokenizer, prompt, chosen, device)
            - _text_logprob(reference, tokenizer, prompt, rejected, device)
        )
    return (policy_gap - reference_gap - 5.0) ** 2


def _simpo_loss(policy, tokenizer, prompt, chosen, rejected, device):
    import torch

    margin = (
        _text_logprob(policy, tokenizer, prompt, chosen, device, normalize=True)
        - _text_logprob(policy, tokenizer, prompt, rejected, device, normalize=True)
    )
    return -torch.nn.functional.logsigmoid(2.0 * margin - 0.5)


def _sequence_rl_loss(
    policy, reference, tokenizer, prompt, outputs, rewards, device,
    length_unbiased: bool,
):
    import torch

    advantages = torch.tensor(
        (rewards - rewards.mean()) / (rewards.std() + 1e-6),
        dtype=torch.float32, device=device,
    )
    logps = torch.stack([
        _text_logprob(
            policy, tokenizer, prompt, output, device,
            normalize=length_unbiased,
        )
        for output in outputs
    ])
    with torch.no_grad():
        reference_logps = torch.stack([
            _text_logprob(
                reference, tokenizer, prompt, output, device,
                normalize=length_unbiased,
            )
            for output in outputs
        ])
    ratios = torch.exp(torch.clamp(logps - reference_logps, -4, 4))
    loss = -(torch.clamp(ratios, 0.8, 1.2) * advantages * logps).mean()
    lengths = np.asarray([max(1, len(output)) for output in outputs])
    return loss, {
        "length_unbiased": float(length_unbiased),
        "mean_response_characters": float(lengths.mean()),
        "length_reward_correlation": float(
            np.corrcoef(lengths, rewards)[0, 1]
            if len(set(lengths)) > 1 and len(set(rewards)) > 1 else 0.0
        ),
    }


def generate(model, tokenizer, prompt, device, rng, sample=True, max_new_tokens=48):
    import torch

    prefix = [tokenizer.bos_id, *tokenizer.encode(prompt), tokenizer.sep_id]
    tokens = torch.tensor([prefix], dtype=torch.long, device=device)
    model.eval()
    with torch.no_grad():
        logits, hidden = model(tokens)
        generated = []
        for _ in range(max_new_tokens):
            values = logits[0, -1] / 0.8
            if sample:
                probabilities = torch.softmax(values, -1).cpu().numpy()
                next_id = int(rng.choices(range(len(probabilities)), weights=probabilities)[0])
            else:
                next_id = int(values.argmax())
            if next_id == tokenizer.eos_id:
                break
            generated.append(next_id)
            current = torch.tensor([[next_id]], dtype=torch.long, device=device)
            logits, hidden = model(current, hidden)
    model.train()
    return tokenizer.decode(generated)


def verify_completion(text: str, expected: str) -> tuple[float, dict[str, float]]:
    matches = re.findall(r"(?:Answer\s*:\s*)?(-?[\d,]+(?:\.\d+)?)", text)
    predicted = matches[-1].replace(",", "") if matches else ""
    exact = float(predicted == expected)
    format_reward = float("Answer:" in text)
    brevity = math.exp(-max(0, len(text) - 96) / 96)
    return (
        0.8 * exact + 0.1 * format_reward + 0.1 * brevity,
        {"exact": exact, "format": format_reward, "characters": float(len(text))},
    )


def evaluate_generation(model, tokenizer, examples, device, seed):
    rng = random.Random(seed)
    exact = reward = format_rate = length = 0.0
    for example in examples:
        output = generate(
            model, tokenizer, example.prompt, device, rng, sample=False
        )
        value, diagnostics = verify_completion(output, example.answer)
        exact += diagnostics["exact"]
        format_rate += diagnostics["format"]
        length += diagnostics["characters"]
        reward += value
    count = max(1, len(examples))
    return {
        "accuracy": exact / count,
        "mean_reward": reward / count,
        "format_rate": format_rate / count,
        "mean_response_characters": length / count,
        "kl_from_reference": 0.0,
    }


def evaluate_pass_at_k(model, tokenizer, examples, device, seed, k_values):
    """Measure empirical pass@k using the same verifier and sampled policy."""
    values = tuple(sorted(set(int(value) for value in k_values)))
    if not values or values[0] < 1:
        raise ValueError("pass@k values must be positive")
    rng = random.Random(seed)
    hits = {value: 0 for value in values}
    maximum = values[-1]
    for example in examples:
        exact = [
            verify_completion(
                generate(model=model, tokenizer=tokenizer, prompt=example.prompt,
                         device=device, rng=rng, sample=True),
                example.answer,
            )[1]["exact"]
            for _ in range(maximum)
        ]
        for value in values:
            hits[value] += int(any(exact[:value]))
    count = max(1, len(examples))
    return {f"pass@{value}": hits[value] / count for value in values}
