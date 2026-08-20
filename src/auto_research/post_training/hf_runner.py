"""Real-checkpoint SFT/DPO/ORPO with resumable mixed-precision training."""

from __future__ import annotations

from contextlib import nullcontext
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random
import re
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
    maximum_examples: int = 64
    maximum_length: int = 384
    evaluation_examples: int = 16
    seeds: tuple[int, ...] = (42, 43, 44)
    mixed_precision: str = "auto"
    save_every: int = 10
    resume_from: Path | None = None
    allow_network: bool = True

    def __post_init__(self):
        if self.objective not in {"sft", "dpo", "orpo"}:
            raise ValueError("objective must be sft, dpo or orpo")
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
        from transformers import AutoModelForCausalLM, AutoTokenizer

        config = self.config
        random.seed(config.seeds[0]); np.random.seed(config.seeds[0]); torch.manual_seed(config.seeds[0])
        source = str(config.resume_from or config.checkpoint_path or config.model_id)
        local = config.resume_from is not None or config.checkpoint_path is not None
        kwargs = {"local_files_only": local or not config.allow_network, "trust_remote_code": False}
        if not local:
            kwargs["revision"] = config.model_revision
        tokenizer = AutoTokenizer.from_pretrained(source, **kwargs)
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token = tokenizer.eos_token
        device = device_for(torch)
        precision, dtype = _precision(torch, device, config.mixed_precision)
        model = AutoModelForCausalLM.from_pretrained(source, dtype=dtype, **kwargs).to(device)
        reference = None
        if config.objective == "dpo":
            reference_source = str(config.checkpoint_path or config.model_id)
            reference_kwargs = {
                "local_files_only": config.checkpoint_path is not None or not config.allow_network,
                "trust_remote_code": False,
            }
            if config.checkpoint_path is None:
                reference_kwargs["revision"] = config.model_revision
            reference = AutoModelForCausalLM.from_pretrained(
                reference_source, dtype=dtype, **reference_kwargs
            ).to(device).eval()
            for parameter in reference.parameters():
                parameter.requires_grad_(False)
        if config.dataset == "gsm8k":
            rows, evaluation_rows = load_gsm8k_sft(config), ()
        else:
            rows, evaluation_rows = load_ultrafeedback(config)
        optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
        start_step = 0
        if config.resume_from:
            state = torch.load(config.resume_from / "trainer-state.pt", map_location="cpu")
            optimizer.load_state_dict(state["optimizer"])
            start_step = int(state["step"])
        run_dir = config.output_dir / f"{config.objective}-{config.dataset}"
        run_dir.mkdir(parents=True, exist_ok=True)
        history = []
        model.train(); optimizer.zero_grad(set_to_none=True)
        for step in range(start_step, config.steps):
            batch = [rows[(step * config.batch_size + offset) % len(rows)] for offset in range(config.batch_size)]
            context = _autocast(torch, device, precision)
            with context:
                losses = [
                    _pair_loss(
                        model, reference, tokenizer, row, device, config.maximum_length,
                        config.objective,
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
                _save_checkpoint(model, tokenizer, optimizer, run_dir / f"checkpoint-{step + 1}", step + 1, torch)
        metrics = (
            _evaluate_gsm8k(model, tokenizer, config, device)
            if config.dataset == "gsm8k"
            else _evaluate_preferences(model, tokenizer, evaluation_rows, config, device)
        )
        payload = {
            "schema_version": 2,
            "config": {**asdict(config), **{
                key: str(value) if isinstance(value, Path) else value
                for key, value in asdict(config).items()
            }},
            "metrics": metrics,
            "history": history,
            "training": {
                "backend": "transformers AutoModelForCausalLM",
                "device": device.type,
                "mixed_precision": precision,
                "batch_size": config.batch_size,
                "gradient_accumulation": config.gradient_accumulation,
                "resumed_from_step": start_step,
                "checkpoint_resume": True,
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


def _pair_loss(model, reference, tokenizer, row, device, maximum_length, objective):
    import torch
    chosen, chosen_tokens = _token_logprob(model, tokenizer, row.prompt, row.chosen, device, maximum_length)
    if objective == "sft":
        return -chosen / chosen_tokens
    rejected, _ = _token_logprob(model, tokenizer, row.prompt, row.rejected, device, maximum_length)
    if objective == "dpo":
        with torch.no_grad():
            ref_chosen, _ = _token_logprob(reference, tokenizer, row.prompt, row.chosen, device, maximum_length)
            ref_rejected, _ = _token_logprob(reference, tokenizer, row.prompt, row.rejected, device, maximum_length)
        return -torch.nn.functional.logsigmoid(0.1 * ((chosen - rejected) - (ref_chosen - ref_rejected)))
    return -chosen / chosen_tokens - 0.1 * torch.nn.functional.logsigmoid(chosen - rejected)


def _save_checkpoint(model, tokenizer, optimizer, path, step, torch):
    path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(path, safe_serialization=True)
    tokenizer.save_pretrained(path)
    torch.save({"step": step, "optimizer": optimizer.state_dict()}, path / "trainer-state.pt")


def _evaluate_preferences(model, tokenizer, rows, config, device):
    model.eval(); selected = rows[:config.evaluation_examples]
    correct = 0
    with __import__("torch").inference_mode():
        for row in selected:
            chosen, _ = _token_logprob(model, tokenizer, row.prompt, row.chosen, device, config.maximum_length)
            rejected, _ = _token_logprob(model, tokenizer, row.prompt, row.rejected, device, config.maximum_length)
            correct += int(chosen > rejected)
    model.train()
    return {"preference_accuracy": correct / len(selected), "evaluation_pairs": len(selected)}


def _evaluate_gsm8k(model, tokenizer, config, device):
    import torch
    heldout = gsm8k(config.dataset_dir, config.allow_network)["test"][: config.evaluation_examples]
    seed_rows = []
    model.eval()
    for seed in config.seeds:
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
        seed_rows.append({"seed": seed, "accuracy": correct / len(heldout), "tokens": tokens})
    model.train()
    return {
        "accuracy": float(np.mean([row["accuracy"] for row in seed_rows])),
        "accuracy_std": float(np.std([row["accuracy"] for row in seed_rows])),
        "generated_tokens": float(np.mean([row["tokens"] for row in seed_rows])),
        "seeds": list(config.seeds),
        "evaluation_examples": len(heldout),
    }
