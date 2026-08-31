"""Real-checkpoint SFT/DPO/ORPO with resumable mixed-precision training."""

from __future__ import annotations

from contextlib import nullcontext
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import random
import re
import statistics
import time

import numpy as np

from ..checkpoint_backend import SMOLLM2_135M_ID, SMOLLM2_135M_REVISION
from ..datasets import gsm8k
from ..runtime import device_for, runtime_summary


ULTRAFEEDBACK_ID = "HuggingFaceH4/ultrafeedback_binarized"
ULTRAFEEDBACK_REVISION = "292c16329d921287c4166934cac1a6ad1e13a6c5"


@dataclass(frozen=True)
class HFPostTrainingConfig:
    objective: str
    dataset: str
    output_dir: Path = Path("runs/checkpoint-post-training")
    dataset_dir: Path = Path("data")
    model_id: str = SMOLLM2_135M_ID
    model_revision: str = SMOLLM2_135M_REVISION
    checkpoint_path: Path | None = None
    dataset_revision: str = ULTRAFEEDBACK_REVISION
    preference_data_path: Path | None = None
    steps: int = 20
    batch_size: int = 2
    gradient_accumulation: int = 1
    learning_rate: float = 5e-6
    beta: float = 0.1
    maximum_examples: int = 64
    maximum_length: int = 384
    evaluation_examples: int = 16
    seeds: tuple[int, ...] = (42, 43, 44)
    mixed_precision: str = "auto"
    save_every: int = 10
    resume_from: Path | None = None
    allow_network: bool = True

    def __post_init__(self):
        if self.objective not in {"sft", "dpo", "normalized-dpo", "orpo"}:
            raise ValueError("objective must be sft, dpo, normalized-dpo or orpo")
        if self.dataset not in {"gsm8k", "ultrafeedback"}:
            raise ValueError("dataset must be gsm8k or ultrafeedback")
        if self.dataset == "gsm8k" and self.objective != "sft":
            raise ValueError("gsm8k checkpoint training uses the SFT objective")
        if self.dataset == "ultrafeedback" and self.objective == "sft":
            raise ValueError("UltraFeedback comparison requires DPO or ORPO")
        if self.mixed_precision not in {"auto", "no", "fp16", "bf16"}:
            raise ValueError("mixed precision must be auto, no, fp16 or bf16")
        if min(
            self.steps, self.batch_size, self.gradient_accumulation,
            self.maximum_examples, self.maximum_length, self.evaluation_examples,
            self.save_every,
        ) < 1:
            raise ValueError("training sizes and steps must be positive")
        if len(self.seeds) != 3:
            raise ValueError("checkpoint post-training requires exactly three evaluation seeds")
        if len(set(self.seeds)) != 3:
            raise ValueError("checkpoint post-training requires three distinct seeds")
        if self.beta <= 0:
            raise ValueError("beta must be positive")


@dataclass(frozen=True)
class PreferenceExample:
    prompt: str
    chosen: str
    rejected: str


def _message_text(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(
            str(item.get("content", "")) if isinstance(item, dict) else str(item)
            for item in value
        )
    return str(value)


def _completion_text(value) -> str:
    if isinstance(value, list):
        assistant = [
            str(item.get("content", "")) for item in value
            if isinstance(item, dict) and item.get("role") == "assistant"
        ]
        if assistant:
            return assistant[-1]
    return _message_text(value)


def _preference_rows(rows, limit: int) -> tuple[PreferenceExample, ...]:
    result = []
    for row in rows:
        prompt = _message_text(row.get("prompt", ""))
        chosen = _completion_text(row.get("chosen", ""))
        rejected = _completion_text(row.get("rejected", ""))
        if prompt and chosen and rejected:
            result.append(PreferenceExample(prompt, chosen, rejected))
        if len(result) >= limit:
            break
    if len(result) < 2:
        raise RuntimeError("UltraFeedback produced fewer than two usable preference pairs")
    return tuple(result)


def _load_preference_jsonl(path: Path, limit: int) -> tuple[PreferenceExample, ...]:
    return _preference_rows(
        (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line),
        limit,
    )


def load_ultrafeedback(
    config: HFPostTrainingConfig,
) -> tuple[tuple[PreferenceExample, ...], tuple[PreferenceExample, ...]]:
    if config.preference_data_path:
        root = config.preference_data_path
        if root.is_dir():
            return (
                _load_preference_jsonl(root / "train.jsonl", config.maximum_examples),
                _load_preference_jsonl(root / "test.jsonl", config.evaluation_examples),
            )
        rows = _load_preference_jsonl(
            root, config.maximum_examples + config.evaluation_examples
        )
        split = min(config.maximum_examples, len(rows) - 2)
        return rows[:split], rows[split:]
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("UltraFeedback requires the post-training-gpu extra") from exc
    dataset = load_dataset(
        ULTRAFEEDBACK_ID,
        split={"train": "train_prefs", "test": "test_prefs"},
        revision=config.dataset_revision,
        cache_dir=str(config.dataset_dir / "huggingface"),
        download_mode="reuse_dataset_if_exists",
    )
    return (
        _preference_rows(dataset["train"], config.maximum_examples),
        _preference_rows(dataset["test"], config.evaluation_examples),
    )


def load_gsm8k_sft(config: HFPostTrainingConfig) -> tuple[PreferenceExample, ...]:
    rows = gsm8k(config.dataset_dir, config.allow_network)["train"][: config.maximum_examples]
    return tuple(
        PreferenceExample(
            f"Problem: {row['question']}\nShow concise reasoning, then write Answer:",
            " " + row["answer"].replace("####", "Answer:"),
            "",
        )
        for row in rows
    )


class HFPostTrainingRunner:
    def __init__(self, config: HFPostTrainingConfig):
        self.config = config

    def run(self) -> tuple[dict, Path]:
        import torch
        from transformers import AutoTokenizer

        config = self.config
        source = str(config.checkpoint_path or config.model_id)
        local = config.checkpoint_path is not None
        kwargs = {"local_files_only": local or not config.allow_network, "trust_remote_code": False}
        if not local:
            kwargs["revision"] = config.model_revision
        tokenizer = AutoTokenizer.from_pretrained(source, **kwargs)
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token = tokenizer.eos_token
        device = device_for(torch)
        precision, dtype = _precision(torch, device, config.mixed_precision)
        if config.dataset == "gsm8k":
            rows, evaluation_rows = load_gsm8k_sft(config), ()
        else:
            rows, evaluation_rows = load_ultrafeedback(config)
        run_dir = config.output_dir / f"{config.objective}-{config.dataset}"
        run_dir.mkdir(parents=True, exist_ok=True)
        seed_results = [
            self._run_seed(
                seed, source, kwargs, tokenizer, rows, evaluation_rows,
                run_dir / f"seed-{seed}", torch, device, precision, dtype,
            )
            for seed in config.seeds
        ]
        metric_name = "accuracy" if config.dataset == "gsm8k" else "preference_accuracy"
        payload = {
            "schema_version": 3,
            "config": {**asdict(config), **{
                key: str(value) if isinstance(value, Path) else value
                for key, value in asdict(config).items()
            }},
            "seed_results": seed_results,
            "metrics": {
                "metric": metric_name,
                "baseline": _aggregate([
                    row["baseline"][metric_name] for row in seed_results
                ]),
                "final": _aggregate([
                    row["final"][metric_name] for row in seed_results
                ]),
                **({
                    "baseline_preference_margin": _aggregate([
                        row["baseline"]["preference_margin"] for row in seed_results
                    ]),
                    "final_preference_margin": _aggregate([
                        row["final"]["preference_margin"] for row in seed_results
                    ]),
                } if config.dataset == "ultrafeedback" else {}),
            },
            "training": {
                "backend": "transformers AutoModelForCausalLM",
                "device": device.type,
                "mixed_precision": precision,
                "batch_size": config.batch_size,
                "gradient_accumulation": config.gradient_accumulation,
                "independent_checkpoint_updates": len(config.seeds),
                "checkpoint_resume": True,
            },
            "evaluation_protocol": {
                "three_independent_training_seeds": True,
                "fixed_public_test_split": True,
                "test_used_for_model_selection": False,
            },
            "provenance": {
                "model_id": config.model_id,
                "model_revision": config.model_revision,
                "dataset_id": "openai/gsm8k" if config.dataset == "gsm8k" else ULTRAFEEDBACK_ID,
                "dataset_revision": config.dataset_revision if config.dataset == "ultrafeedback" else "official main JSONL",
                "dataset_license": "MIT" if config.dataset == "ultrafeedback" else "MIT",
            },
            "runtime": runtime_summary(torch),
        }
        (run_dir / "metrics.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8"
        )
        return payload, run_dir

    def _run_seed(
        self, seed, source, kwargs, tokenizer, rows, evaluation_rows,
        seed_dir, torch, device, precision, dtype,
    ):
        from transformers import AutoModelForCausalLM

        config = self.config
        random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        seed_source = source
        seed_kwargs = dict(kwargs)
        resume = None
        if config.resume_from:
            candidate = config.resume_from / f"seed-{seed}"
            resume_root = candidate if candidate.exists() else config.resume_from
            checkpoints = sorted(
                resume_root.glob("checkpoint-*"),
                key=lambda path: int(path.name.rsplit("-", 1)[-1]),
            )
            resume = checkpoints[-1] if checkpoints else resume_root
            seed_source = str(resume)
            seed_kwargs = {"local_files_only": True, "trust_remote_code": False}
        model = AutoModelForCausalLM.from_pretrained(
            seed_source, dtype=dtype, **seed_kwargs
        ).to(device)
        reference = None
        if config.objective in {"dpo", "normalized-dpo"}:
            reference = AutoModelForCausalLM.from_pretrained(
                source, dtype=dtype, **kwargs
            ).to(device).eval()
            for parameter in reference.parameters():
                parameter.requires_grad_(False)
        baseline = (
            _evaluate_gsm8k(model, tokenizer, config, device, seed)
            if config.dataset == "gsm8k"
            else _evaluate_preferences(model, tokenizer, evaluation_rows, config, device)
        )
        optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
        start_step = 0
        if resume and (resume / "trainer-state.pt").exists():
            state = torch.load(resume / "trainer-state.pt", map_location="cpu")
            optimizer.load_state_dict(state["optimizer"])
            start_step = int(state["step"])
        history = []
        model.train(); optimizer.zero_grad(set_to_none=True)
        order = list(range(len(rows)))
        random.Random(seed).shuffle(order)
        for step in range(start_step, config.steps):
            batch = [
                rows[order[(step * config.batch_size + offset) % len(order)]]
                for offset in range(config.batch_size)
            ]
            with _autocast(torch, device, precision):
                losses = [
                    _pair_loss(
                        model, reference, tokenizer, row, device,
                        config.maximum_length, config.objective, config.beta,
                    )
                    for row in batch
                ]
                loss = torch.stack(losses).mean() / config.gradient_accumulation
            loss.backward()
            update = (step + 1) % config.gradient_accumulation == 0 or step + 1 == config.steps
            if update:
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step(); optimizer.zero_grad(set_to_none=True)
            history.append({"step": step + 1, "loss": float(loss.detach().cpu())})
            if (step + 1) % config.save_every == 0 or step + 1 == config.steps:
                _save_checkpoint(
                    model, tokenizer, optimizer,
                    seed_dir / f"checkpoint-{step + 1}", step + 1, torch,
                )
        final = (
            _evaluate_gsm8k(model, tokenizer, config, device, seed)
            if config.dataset == "gsm8k"
            else _evaluate_preferences(model, tokenizer, evaluation_rows, config, device)
        )
        result = {
            "seed": seed, "baseline": baseline, "final": final,
            "history": history, "resumed_from_step": start_step,
        }
        del model, optimizer, reference
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return result


def _precision(torch, device, requested):
    if device.type != "cuda" or requested == "no":
        return "no", torch.float32
    if requested == "bf16" or (requested == "auto" and torch.cuda.is_bf16_supported()):
        return "bf16", torch.bfloat16
    return "fp16", torch.float16


def _autocast(torch, device, precision):
    if device.type == "cuda" and precision != "no":
        return torch.autocast("cuda", dtype=torch.bfloat16 if precision == "bf16" else torch.float16)
    return nullcontext()


def _token_logprob(model, tokenizer, prompt, response, device, maximum_length):
    import torch
    prompt_ids = tokenizer(prompt, add_special_tokens=True)["input_ids"]
    response_ids = tokenizer(response, add_special_tokens=False)["input_ids"] + [tokenizer.eos_token_id]
    ids = (prompt_ids + response_ids)[:maximum_length]
    prompt_length = min(len(prompt_ids), len(ids) - 1)
    tokens = torch.tensor([ids], dtype=torch.long, device=device)
    logits = model(tokens[:, :-1]).logits
    targets = tokens[:, 1:]
    selected = torch.log_softmax(logits, -1).gather(-1, targets.unsqueeze(-1)).squeeze(-1)
    mask = torch.arange(targets.shape[1], device=device) >= max(0, prompt_length - 1)
    return selected[0, mask].sum(), mask.sum().clamp_min(1)


def _pair_loss(
    model, reference, tokenizer, row, device, maximum_length, objective, beta=0.1,
):
    import torch
    chosen, chosen_tokens = _token_logprob(model, tokenizer, row.prompt, row.chosen, device, maximum_length)
    if objective == "sft":
        return -chosen / chosen_tokens
    rejected, _ = _token_logprob(model, tokenizer, row.prompt, row.rejected, device, maximum_length)
    if objective in {"dpo", "normalized-dpo"}:
        with torch.no_grad():
            ref_chosen, _ = _token_logprob(reference, tokenizer, row.prompt, row.chosen, device, maximum_length)
            ref_rejected, _ = _token_logprob(reference, tokenizer, row.prompt, row.rejected, device, maximum_length)
        margin = (chosen - rejected) - (ref_chosen - ref_rejected)
        if objective == "normalized-dpo":
            # Centering keeps zero preference margin at zero loss; dividing by
            # beta removes beta's direct gradient-scale effect while retaining
            # its intended preference-temperature role.
            return normalized_dpo_loss(margin, beta)
        return -torch.nn.functional.logsigmoid(beta * margin)
    return -chosen / chosen_tokens - 0.1 * torch.nn.functional.logsigmoid(chosen - rejected)


def normalized_dpo_loss(margin, beta: float):
    """Centered-softplus DPO objective with beta-normalized gradients."""
    import torch

    if beta <= 0:
        raise ValueError("beta must be positive")
    return (torch.nn.functional.softplus(-beta * margin) - math.log(2.0)) / beta


def _save_checkpoint(model, tokenizer, optimizer, path, step, torch):
    path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(path, safe_serialization=True)
    tokenizer.save_pretrained(path)
    torch.save({"step": step, "optimizer": optimizer.state_dict()}, path / "trainer-state.pt")


def _evaluate_preferences(model, tokenizer, rows, config, device):
    model.eval(); selected = rows[:config.evaluation_examples]
    correct = 0
    margins = []
    with __import__("torch").inference_mode():
        for row in selected:
            chosen, _ = _token_logprob(model, tokenizer, row.prompt, row.chosen, device, config.maximum_length)
            rejected, _ = _token_logprob(model, tokenizer, row.prompt, row.rejected, device, config.maximum_length)
            correct += int(chosen > rejected)
            margins.append(float((chosen - rejected).detach().cpu()))
    model.train()
    return {
        "preference_accuracy": correct / len(selected),
        "preference_margin": float(np.mean(margins)),
        "evaluation_pairs": len(selected),
    }


def _evaluate_gsm8k(model, tokenizer, config, device, seed):
    import torch
    heldout = gsm8k(config.dataset_dir, config.allow_network)["test"][: config.evaluation_examples]
    model.eval()
    torch.manual_seed(seed); correct = tokens = 0
    for row in heldout:
        prompt = f"Problem: {row['question']}\nShow concise reasoning, then write Answer:"
        encoded = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.inference_mode():
            output = model.generate(**encoded, max_new_tokens=96, do_sample=False)
        generated = output[0, encoded["input_ids"].shape[1]:]
        text = tokenizer.decode(generated, skip_special_tokens=True)
        expected_match = re.search(r"####\s*(-?[\d,]+(?:\.\d+)?)", row["answer"])
        actual = re.findall(r"(?:Answer\s*:\s*)?(-?[\d,]+(?:\.\d+)?)", text)
        expected = expected_match.group(1).replace(",", "") if expected_match else ""
        correct += int(bool(actual) and actual[-1].replace(",", "") == expected)
        tokens += len(generated)
    model.train()
    return {
        "accuracy": correct / len(heldout),
        "generated_tokens": tokens,
        "seed": seed,
        "evaluation_examples": len(heldout),
    }


def _aggregate(values):
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    radius = 1.96 * std / math.sqrt(len(values))
    return {
        "mean": mean, "std": std,
        "ci95_low": mean - radius, "ci95_high": mean + radius,
    }
