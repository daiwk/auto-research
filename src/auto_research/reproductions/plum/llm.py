from __future__ import annotations

import gc
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .data import CompletionExample, retrieval_prompt
from .model import SID_END, SemanticIDIndex, TokenTrie, ranking_from_beams


BASE_MODEL = "HuggingFaceTB/SmolLM2-135M"


@dataclass(frozen=True)
class TrainingConfig:
    cpt_steps: int = 240
    sft_steps: int = 240
    batch_size: int = 16
    # PLUM Table 6 uses 1e-4 for its ~110M activated-parameter model.
    learning_rate: float = 1e-4
    max_length: int = 256
    evaluation_users: int = 200
    beam_size: int = 10
    resume_dir: Path | None = None


def require_backend():
    try:
        import torch
        from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError(
            "PLUM is a real LLM reproduction and needs optional dependencies; "
            "install with `pip install -e '.[plum]'`."
        ) from exc
    return torch, AutoConfig, AutoModelForCausalLM, AutoTokenizer


def run_ablation(
    name: str,
    llm_initialized: bool,
    use_cpt: bool,
    cpt_corpus: tuple[str, ...],
    sft_examples: tuple[CompletionExample, ...],
    sequences,
    index: SemanticIDIndex,
    seed: int,
    output_dir: Path,
    config: TrainingConfig,
    prior_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    torch, AutoConfig, AutoModelForCausalLM, AutoTokenizer = require_backend()
    _seed_everything(seed, torch)
    resume_checkpoint = _resume_checkpoint(config.resume_dir, name)
    if resume_checkpoint is not None:
        tokenizer = AutoTokenizer.from_pretrained(resume_checkpoint)
        model = AutoModelForCausalLM.from_pretrained(resume_checkpoint)
    else:
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        tokenizer.add_special_tokens(
            {"additional_special_tokens": list(index.vocabulary())}
        )
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token = tokenizer.eos_token
        if llm_initialized:
            model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)
        else:
            model_config = AutoConfig.from_pretrained(BASE_MODEL)
            model = AutoModelForCausalLM.from_config(model_config)
        model.resize_token_embeddings(len(tokenizer), mean_resizing=llm_initialized)
    device = _device(torch)
    model.to(device)
    variant_dir = output_dir / name.lower()
    variant_dir.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    cpt_metrics = None if prior_result is None else prior_result["cpt_loss"]
    cpt_checkpoint = None
    if use_cpt and resume_checkpoint is None:
        cpt_metrics = _train(
            model,
            tokenizer,
            _tokenize_text(cpt_corpus, tokenizer, config.max_length),
            config.cpt_steps,
            config.batch_size,
            config.learning_rate,
            device,
            torch,
            seed,
            f"{name}/CPT",
        )
        cpt_checkpoint = variant_dir / "cpt"
        model.save_pretrained(cpt_checkpoint, safe_serialization=True)
        tokenizer.save_pretrained(cpt_checkpoint)
    continuation_metrics = _train(
        model,
        tokenizer,
        _tokenize_completions(sft_examples, tokenizer, config.max_length),
        config.sft_steps,
        config.batch_size,
        config.learning_rate,
        device,
        torch,
        seed + 1 + (100_000 if resume_checkpoint is not None else 0),
        f"{name}/SFT",
    )
    sft_metrics = _merge_training_metrics(
        None if prior_result is None else prior_result["sft_loss"],
        continuation_metrics,
    )
    retrieval = evaluate_retrieval(
        model, tokenizer, sequences, index, config, device, torch, seed
    )
    final_checkpoint = variant_dir / "sft"
    model.save_pretrained(final_checkpoint, safe_serialization=True)
    tokenizer.save_pretrained(final_checkpoint)
    result = {
        "pretrained_llm": llm_initialized,
        "cpt": use_cpt,
        "cpt_loss": cpt_metrics,
        "sft_loss": sft_metrics,
        "training_seconds": (
            0.0 if prior_result is None else prior_result["training_seconds"]
        ) + time.perf_counter() - started,
        **retrieval,
        "cpt_checkpoint": None if cpt_checkpoint is None else str(cpt_checkpoint),
        "checkpoint": str(final_checkpoint),
    }
    del model
    gc.collect()
    if device.type == "mps":
        torch.mps.empty_cache()
    return result


def _resume_checkpoint(resume_dir: Path | None, name: str) -> Path | None:
    if resume_dir is None:
        return None
    variant = resume_dir / name.lower()
    candidates = (variant / "sft", variant)
    for candidate in candidates:
        if (candidate / "config.json").exists():
            return candidate
    raise RuntimeError(f"missing resume checkpoint for {name}: {variant}")


def _merge_training_metrics(prior, continuation):
    if prior is None:
        return continuation
    return {
        "initial": prior["initial"],
        "final": continuation["final"],
        "minimum": min(prior["minimum"], continuation["minimum"]),
        "continuation_initial": continuation["initial"],
    }


def _device(torch):
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def _seed_everything(seed: int, torch) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def _tokenize_text(corpus, tokenizer, max_length: int):
    rows = []
    for text in corpus:
        ids = tokenizer(
            text + tokenizer.eos_token,
            add_special_tokens=False,
            truncation=True,
            max_length=max_length,
        )["input_ids"]
        rows.append((ids, ids.copy()))
    return rows


def _tokenize_completions(examples, tokenizer, max_length: int):
    rows = []
    for example in examples:
        prompt = tokenizer(example.prompt, add_special_tokens=False)["input_ids"]
        completion = tokenizer(
            example.completion + tokenizer.eos_token, add_special_tokens=False
        )["input_ids"]
        if len(prompt) + len(completion) > max_length:
            prompt = prompt[-(max_length - len(completion)) :]
        rows.append((prompt + completion, [-100] * len(prompt) + completion))
    return rows


def _train(
    model,
    tokenizer,
    rows,
    steps: int,
    batch_size: int,
    learning_rate: float,
    device,
    torch,
    seed: int,
    label: str,
) -> dict[str, float]:
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    rng = random.Random(seed)
    losses: list[float] = []
    for step in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(batch_size)]
        input_ids, attention_mask, labels = _collate(
            batch, tokenizer.pad_token_id, device, torch
        )
        optimizer.zero_grad(set_to_none=True)
        output = model(
            input_ids=input_ids, attention_mask=attention_mask, labels=labels
        )
        output.loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(output.loss.detach().cpu()))
        if (step + 1) % 20 == 0 or step + 1 == steps:
            print(f"{label}: step {step + 1}/{steps}, loss={losses[-1]:.4f}", flush=True)
    tail = losses[-min(20, len(losses)) :]
    return {
        "initial": float(np.mean(losses[: min(20, len(losses))])),
        "final": float(np.mean(tail)),
        "minimum": min(losses),
    }


def _collate(rows, pad_id: int, device, torch):
    width = max(len(row[0]) for row in rows)
    inputs, masks, labels = [], [], []
    for input_ids, label_ids in rows:
        padding = width - len(input_ids)
        inputs.append(input_ids + [pad_id] * padding)
        masks.append([1] * len(input_ids) + [0] * padding)
        labels.append(label_ids + [-100] * padding)
    return (
        torch.tensor(inputs, dtype=torch.long, device=device),
        torch.tensor(masks, dtype=torch.long, device=device),
        torch.tensor(labels, dtype=torch.long, device=device),
    )


def evaluate_retrieval(
    model,
    tokenizer,
    sequences,
    index: SemanticIDIndex,
    config: TrainingConfig,
    device,
    torch,
    seed: int,
) -> dict[str, float]:
    model.eval()
    sid_token_ids = {
        token: tokenizer.convert_tokens_to_ids(token) for token in index.vocabulary()
    }
    encoded_codes: dict[tuple[int, ...], tuple[int, ...]] = {}
    trie_sequences = []
    for code in index.items_by_code():
        tokens = tuple(
            sid_token_ids[f"<sid_{level}_{value}>"]
            for level, value in enumerate(code)
        ) + (sid_token_ids[SID_END],)
        encoded_codes[tokens] = code
        trie_sequences.append(tokens)
    trie = TokenTrie(trie_sequences)
    code_to_items = index.items_by_code()
    candidates = list(range(len(sequences.test)))
    random.Random(seed).shuffle(candidates)
    candidates = candidates[: min(config.evaluation_users, len(candidates))]
    hits = ndcg = 0.0
    valid = total = 0
    with torch.inference_mode():
        for user in candidates:
            history = sequences.train[user] + (sequences.validation[user],)
            prompt = retrieval_prompt(history, index)
            prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
            generated = constrained_beam_search(
                model, prompt_ids, trie, config.beam_size, device, torch
            )
            decoded = []
            for token_sequence, score in generated:
                total += 1
                if token_sequence in encoded_codes:
                    valid += 1
                    decoded.append((encoded_codes[token_sequence], score))
            ranking = ranking_from_beams(
                decoded, code_to_items, history, sequences.popularity
            )
            expected = sequences.test[user]
            if expected in ranking:
                position = ranking.index(expected)
                hits += 1.0
                ndcg += 1.0 / math.log2(position + 2)
    count = max(1, len(candidates))
    return {
        "recall_at_10": hits / count,
        "ndcg_at_10": ndcg / count,
        "valid_sid_rate": valid / max(1, total),
        "evaluated_users": len(candidates),
    }


def constrained_beam_search(
    model, prompt_ids, trie: TokenTrie, beam_size: int, device, torch
) -> list[tuple[tuple[int, ...], float]]:
    beams: list[tuple[tuple[int, ...], float]] = [((), 0.0)]
    maximum_depth = 64
    for _ in range(maximum_depth):
        active = [(prefix, score) for prefix, score in beams if trie.allowed(prefix)]
        if not active:
            break
        batch = [prompt_ids + list(prefix) for prefix, _ in active]
        input_ids = torch.tensor(batch, dtype=torch.long, device=device)
        logits = model(input_ids=input_ids).logits[:, -1, :]
        log_probs = torch.log_softmax(logits, dim=-1)
        expanded: list[tuple[tuple[int, ...], float]] = []
        for row, (prefix, score) in enumerate(active):
            allowed = trie.allowed(prefix)
            values = log_probs[row, list(allowed)].detach().cpu().tolist()
            expanded.extend(
                (prefix + (token,), score + float(value))
                for token, value in zip(allowed, values, strict=True)
            )
        beams = sorted(expanded, key=lambda row: row[1], reverse=True)[:beam_size]
    return [(prefix, score) for prefix, score in beams if trie.contains(prefix)]
