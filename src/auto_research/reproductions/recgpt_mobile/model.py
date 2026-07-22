from __future__ import annotations

import io
import math
import random
import time
from dataclasses import dataclass

import numpy as np

from ..llm_lora import device_for, inject_lora, lora_sft, require_llm_backend


@dataclass(frozen=True)
class MobileConfig:
    model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct"
    sft_steps: int = 80
    eval_users: int = 32
    token_budget: int = 96
    trigger_threshold: float = 0.8


@dataclass
class IntentLM:
    model: object
    tokenizer: object
    device: object


def load_model(config: MobileConfig, seed: int):
    torch, _, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(config.model_name, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(config.model_name, local_files_only=True)
    device = device_for(torch); model.to(device)
    return IntentLM(model, tokenizer, device)


def prompt_for(example, data, tokenizer, budget: int):
    genre_count = len({genre for item in example.history for genre in data.item_genres[item]})
    keep = 8 if genre_count >= 5 else 5
    items = [data.item_texts[item] for item in example.history[-keep:]]
    header = "Infer the user's next shopping intent from recent interactions.\n"
    if genre_count >= 5:
        header += "The behavior is diverse; prioritize the most recent coherent interest.\n"
    body = "\n".join(f"{index + 1}. watched {text}" for index, text in enumerate(items))
    suffix = "\nReturn exactly one intent category.\nIntent: "
    while len(tokenizer(header + body + suffix, add_special_tokens=False)["input_ids"]) > budget and len(items) > 2:
        items.pop(0)
        body = "\n".join(f"{index + 1}. watched {text}" for index, text in enumerate(items))
    return header + body + suffix


def target_query(example, data):
    return data.item_genres[example.target][0]


def train_lora(intent_lm: IntentLM, data, config: MobileConfig, seed: int):
    trainable = inject_lora(intent_lm.model, rank=4, alpha=8.0)
    examples = [(prompt_for(row, data, intent_lm.tokenizer, config.token_budget), target_query(row, data)) for row in data.train]
    started = time.perf_counter()
    losses = lora_sft(intent_lm.model, intent_lm.tokenizer, examples, config.sft_steps, 2, 2e-4, seed)
    return {"trainable_lora_parameters": trainable, "initial_loss": losses["initial"], "final_loss": losses["final"], "steps": config.sft_steps, "seconds": time.perf_counter() - started}


def completion_scores(intent_lm: IntentLM, prompt: str, completions):
    torch, _, _, _ = require_llm_backend(); tokenizer = intent_lm.tokenizer
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    rows = []; labels = []
    for completion in completions:
        target = tokenizer(completion, add_special_tokens=False)["input_ids"]
        rows.append(prompt_ids + target); labels.append([-100] * len(prompt_ids) + target)
    width = max(map(len, rows)); inputs = []; masks = []; targets = []
    for ids, label in zip(rows, labels):
        padding = width - len(ids); inputs.append(ids + [tokenizer.pad_token_id] * padding)
        masks.append([1] * len(ids) + [0] * padding); targets.append(label + [-100] * padding)
    input_ids = torch.tensor(inputs, device=intent_lm.device)
    with torch.inference_mode():
        logits = intent_lm.model(input_ids=input_ids, attention_mask=torch.tensor(masks, device=intent_lm.device)).logits[:, :-1].float()
    shifted = torch.tensor(targets, device=intent_lm.device)[:, 1:]; valid = shifted.ne(-100)
    token_logp = torch.log_softmax(logits, -1).gather(-1, shifted.clamp_min(0).unsqueeze(-1)).squeeze(-1)
    return ((token_logp * valid).sum(-1) / valid.sum(-1).clamp_min(1)).cpu().numpy()


def evaluate(intent_lm, rows, data, config):
    rows = rows[:config.eval_users]; correct = semantic = latency = 0.0
    for row in rows:
        prompt = prompt_for(row, data, intent_lm.tokenizer, config.token_budget)
        started = time.perf_counter(); scores = completion_scores(intent_lm, prompt, data.genres); latency += time.perf_counter() - started
        predicted = data.genres[int(np.argmax(scores))]; truth = set(data.item_genres[row.target])
        correct += predicted == data.item_genres[row.target][0]; semantic += predicted in truth
    return {"examples": len(rows), "primary_intent_accuracy": correct / len(rows), "semantic_intent_accuracy": semantic / len(rows), "mean_latency_ms": 1000 * latency / len(rows)}


def quantize_weight_only(intent_lm: IntentLM):
    torch, nn, _, _ = require_llm_backend()
    intent_lm.model.to("cpu")

    class WeightOnlyInt8Linear(nn.Module):
        def __init__(self, linear):
            super().__init__()
            weight = linear.weight.detach().float()
            scale = weight.abs().amax(1, keepdim=True).clamp_min(1e-8) / 127
            self.register_buffer("qweight", torch.round(weight / scale).clamp(-127, 127).to(torch.int8))
            self.register_buffer("scale", scale)
            if linear.bias is None:
                self.bias = None
            else:
                self.register_buffer("bias", linear.bias.detach().float())

        def forward(self, values):
            return torch.nn.functional.linear(values, self.qweight.float() * self.scale, self.bias)

    def replace(module):
        for name, child in list(module.named_children()):
            if isinstance(child, nn.Linear):
                setattr(module, name, WeightOnlyInt8Linear(child))
            else:
                replace(child)

    replace(intent_lm.model)
    return IntentLM(intent_lm.model, intent_lm.tokenizer, torch.device("cpu"))


def serialized_megabytes(model):
    torch, _, _, _ = require_llm_backend(); buffer = io.BytesIO(); torch.save(model.state_dict(), buffer)
    return len(buffer.getvalue()) / (1024 * 1024)


def intent_drift(previous_items, current_items, genre_count, item_genres):
    previous = _distribution(previous_items, genre_count, item_genres)
    current = _distribution(current_items, genre_count, item_genres)
    entropy_delta = abs(_entropy(current) - _entropy(previous))
    left = set(np.flatnonzero(previous)); right = set(np.flatnonzero(current))
    jaccard = len(left & right) / max(len(left | right), 1)
    middle = 0.5 * (previous + current)
    js = 0.5 * (_kl(previous, middle) + _kl(current, middle))
    return 0.4 * entropy_delta + 0.3 * (1 - jaccard) + 0.3 * js


def trigger_diagnostics(rows, data, threshold: float):
    values = []
    for row in rows:
        split = max(1, len(row.history) // 2)
        values.append(intent_drift(row.history[:split], row.history[split:], len(data.genres), data.item_genres))
    return {"threshold": threshold, "mean_intent_drift": float(np.mean(values)), "trigger_rate": float(np.mean(np.asarray(values) > threshold)), "inference_saved_percent": 100 * float(np.mean(np.asarray(values) <= threshold))}


def _distribution(items, genre_count, item_genres):
    values = np.zeros(genre_count, dtype=np.float64)
    # genres are alphabetically ordered in the loader.
    vocabulary = {genre: index for index, genre in enumerate(sorted({g for item in item_genres for g in item}))}
    for item in items:
        for genre in item_genres[item]: values[vocabulary[genre]] += 1
    return values / max(values.sum(), 1)


def _entropy(values):
    active = values[values > 0]; return float(-(active * np.log(active)).sum())


def _kl(left, right):
    active = left > 0; return float((left[active] * np.log(left[active] / np.maximum(right[active], 1e-12))).sum())
