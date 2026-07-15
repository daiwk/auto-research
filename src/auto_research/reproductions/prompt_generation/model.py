from __future__ import annotations

import hashlib
import random
import time
from dataclasses import dataclass
from typing import Any

import numpy as np

from ..llm_lora import device_for, inject_lora, require_llm_backend
from .data import PGDataset, PGExample
from .protocol import PromptCompiler, PromptConfig


@dataclass
class TrainedPG:
    model: Any
    tokenizer: Any
    compiler: PromptCompiler
    device: Any
    training: dict[str, Any]


def train_pg(
    dataset: PGDataset,
    config: PromptConfig,
    model_name: str,
    steps: int,
    batch_size: int,
    seed: int,
) -> TrainedPG:
    torch, _, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
    trainable = inject_lora(model, rank=4, alpha=8.0)
    device = device_for(torch)
    model.to(device)
    compiler = PromptCompiler(config)
    optimizer = torch.optim.AdamW(
        [parameter for parameter in model.parameters() if parameter.requires_grad],
        lr=2e-4,
    )
    rng = random.Random(seed)
    losses: list[float] = []
    token_counts: list[int] = []
    started = time.perf_counter()
    model.train()
    for _ in range(steps):
        examples = [dataset.train[rng.randrange(len(dataset.train))] for _ in range(batch_size)]
        embeddings, masks, labels, prompt_lengths = _batch(
            examples, dataset, compiler, model, tokenizer, device, torch, with_targets=True
        )
        output = model(inputs_embeds=embeddings, attention_mask=masks, labels=labels)
        optimizer.zero_grad(set_to_none=True)
        output.loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [parameter for parameter in model.parameters() if parameter.requires_grad], 1.0
        )
        optimizer.step()
        losses.append(float(output.loss.detach().cpu()))
        token_counts.extend(prompt_lengths)
    elapsed = time.perf_counter() - started
    window = min(5, len(losses))
    return TrainedPG(
        model=model,
        tokenizer=tokenizer,
        compiler=compiler,
        device=device,
        training={
            "steps": steps,
            "batch_size": batch_size,
            "trainable_lora_parameters": trainable,
            "initial_loss": float(np.mean(losses[:window])),
            "final_loss": float(np.mean(losses[-window:])),
            "mean_prompt_tokens": float(np.mean(token_counts)),
            "seconds": elapsed,
            "device": device.type,
        },
    )


def evaluate_sampled_catalog(
    trained: TrainedPG,
    dataset: PGDataset,
    examples: tuple[PGExample, ...],
    candidate_count: int,
    seed: int,
) -> dict[str, float | int]:
    torch, _, _, _ = require_llm_backend()
    rng = random.Random(seed)
    catalog = sorted(dataset.item_sids)
    ranks: list[int] = []
    trained.model.eval()
    started = time.perf_counter()
    with torch.inference_mode():
        for example in examples:
            negatives = [item for item in catalog if item != example.target_id]
            sampled = rng.sample(negatives, min(candidate_count - 1, len(negatives)))
            candidates = [example.target_id, *sampled]
            rng.shuffle(candidates)
            scores = _score_candidates(trained, dataset, example, candidates, torch)
            ordered = sorted(range(len(candidates)), key=lambda index: scores[index], reverse=True)
            ranks.append(ordered.index(candidates.index(example.target_id)) + 1)
    result: dict[str, float | int] = {
        "users": len(ranks),
        "candidate_count": len(candidates) if ranks else candidate_count,
        "mean_rank": float(np.mean(ranks)) if ranks else 0.0,
        "seconds": time.perf_counter() - started,
    }
    for k in (1, 5, 10, 20, 50):
        if k <= candidate_count:
            result[f"hr_at_{k}"] = float(np.mean([rank <= k for rank in ranks]))
    return result


def _score_candidates(trained, dataset, example, candidates, torch):
    prompt, _, _, _ = _batch(
        [example], dataset, trained.compiler, trained.model, trained.tokenizer,
        trained.device, torch, with_targets=False
    )
    prompt = prompt[0]
    prompt_length = prompt.shape[0]
    embed = trained.model.get_input_embeddings()
    scores: list[float] = []
    for start in range(0, len(candidates), 8):
        ids = candidates[start : start + 8]
        completions = [
            trained.tokenizer(dataset.item_sids[item], add_special_tokens=False)["input_ids"]
            for item in ids
        ]
        width = prompt_length + max(len(value) for value in completions)
        batch_embeddings, masks, labels = [], [], []
        for completion in completions:
            completion_ids = torch.tensor(completion, device=trained.device)
            candidate_embeddings = torch.cat((prompt, embed(completion_ids)), dim=0)
            padding = width - candidate_embeddings.shape[0]
            if padding:
                candidate_embeddings = torch.cat(
                    (candidate_embeddings, torch.zeros((padding, candidate_embeddings.shape[1]), device=trained.device, dtype=candidate_embeddings.dtype)),
                    dim=0,
                )
            batch_embeddings.append(candidate_embeddings)
            masks.append([1] * (prompt_length + len(completion)) + [0] * padding)
            labels.append([-100] * prompt_length + completion + [-100] * padding)
        labels_tensor = torch.tensor(labels, device=trained.device)
        output = trained.model(
            inputs_embeds=torch.stack(batch_embeddings),
            attention_mask=torch.tensor(masks, device=trained.device),
        )
        logits = output.logits[:, :-1].float()
        target = labels_tensor[:, 1:]
        valid = target.ne(-100)
        token_logp = torch.log_softmax(logits, dim=-1).gather(
            -1, target.clamp_min(0).unsqueeze(-1)
        ).squeeze(-1)
        sequence_scores = (token_logp * valid).sum(-1) / valid.sum(-1).clamp_min(1)
        scores.extend(sequence_scores.cpu().tolist())
    return scores


def _batch(examples, dataset, compiler, model, tokenizer, device, torch, with_targets):
    embed = model.get_input_embeddings()
    sequences, labels, prompt_lengths = [], [], []
    for example in examples:
        row = _row(example, dataset)

        def encode_text(value):
            ids = tokenizer(value, add_special_tokens=False)["input_ids"]
            if not ids:
                ids = [tokenizer.eos_token_id]
            return embed(torch.tensor(ids, device=device))

        def encode_embedding(value):
            vector = torch.as_tensor(value, device=device, dtype=embed.weight.dtype)
            if vector.ndim == 1:
                vector = vector.unsqueeze(0)
            if vector.shape[-1] != embed.weight.shape[-1]:
                raise ValueError("precomputed embedding dimension must match model hidden size")
            return vector

        def merge(values, spec):
            joined = torch.cat(values, dim=0)
            kind = spec["type"]
            output_tokens = int(spec.get("params", {}).get("out_token_len", 1))
            if kind == "mean":
                if output_tokens == 1:
                    return joined.mean(dim=0, keepdim=True)
                chunks = torch.tensor_split(joined, output_tokens)
                return torch.stack([chunk.mean(dim=0) for chunk in chunks if len(chunk)])
            if kind == "concat":
                return joined
            raise ValueError(f"unsupported runtime merger: {kind}")

        prompt = torch.cat(compiler.compile(row, encode_text, encode_embedding, merge), dim=0)
        prompt_lengths.append(prompt.shape[0])
        if with_targets:
            target = tokenizer(example.target_sid + tokenizer.eos_token, add_special_tokens=False)["input_ids"]
            target_tensor = torch.tensor(target, device=device)
            sequences.append(torch.cat((prompt, embed(target_tensor)), dim=0))
            labels.append([-100] * prompt.shape[0] + target)
        else:
            sequences.append(prompt)
            labels.append([-100] * prompt.shape[0])
    width = max(sequence.shape[0] for sequence in sequences)
    padded, masks, padded_labels = [], [], []
    for sequence, target in zip(sequences, labels):
        padding = width - sequence.shape[0]
        padded.append(torch.cat((sequence, torch.zeros((padding, sequence.shape[1]), device=device, dtype=sequence.dtype)), dim=0))
        masks.append([1] * sequence.shape[0] + [0] * padding)
        padded_labels.append(target + [-100] * padding)
    return (
        torch.stack(padded),
        torch.tensor(masks, device=device),
        torch.tensor(padded_labels, device=device),
        prompt_lengths,
    )


def _row(example: PGExample, dataset: PGDataset) -> dict[str, Any]:
    brands = [dataset.items.get(item, {}).get("brand", "") for item in example.history_ids]
    return {
        "history_sids": list(example.history_sids),
        "history_titles": list(example.history_titles),
        "history_brands": brands,
    }


def deterministic_split(examples: tuple[PGExample, ...], count: int, seed: int):
    ordered = sorted(
        examples,
        key=lambda row: hashlib.sha256(f"{seed}:{row.user_id}:{row.target_id}".encode()).digest(),
    )
    return tuple(ordered[:count])
