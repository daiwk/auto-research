from __future__ import annotations

import random
import time
from dataclasses import dataclass

import numpy as np

from ..llm_lora import device_for, inject_lora, lora_sft, require_llm_backend
from .data import AdsData, AdsExample


@dataclass
class AdvertiserPredictor:
    model: object
    tokenizer: object
    device: object
    names: tuple[str, ...]


def train_predictor(data: AdsData, model_name: str, sft_steps: int, seed: int):
    torch, _, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
    trainable = inject_lora(model, rank=4, alpha=8.0)
    device = device_for(torch)
    model.to(device)
    rows = [
        (sft_prompt(row), data.advertiser_names[row.target_advertiser])
        for row in data.train
    ]
    started = time.perf_counter()
    losses = lora_sft(model, tokenizer, rows, sft_steps, 2, 2e-4, seed)
    return AdvertiserPredictor(model, tokenizer, device, data.advertiser_names), {
        "trainable_lora_parameters": trainable,
        "initial_loss": losses["initial"],
        "final_loss": losses["final"],
        "sft_steps": sft_steps,
        "seconds": time.perf_counter() - started,
        "device": device.type,
    }


def train_grpo(
    predictor: AdvertiserPredictor,
    data: AdsData,
    steps: int,
    seed: int,
    group_size: int = 4,
    list_size: int = 5,
):
    torch, _, _, _ = require_llm_backend()
    optimizer = torch.optim.AdamW(
        [parameter for parameter in predictor.model.parameters() if parameter.requires_grad],
        lr=8e-5,
    )
    rng = random.Random(seed)
    losses, rewards, clipped = [], [], []
    started = time.perf_counter()
    predictor.model.train()
    for _ in range(steps):
        row = data.train[rng.randrange(len(data.train))]
        responses, group_rewards = _response_group(
            row, data.advertiser_names, rng, group_size, list_size
        )
        prompt = grpo_prompt(row, list_size)
        with torch.no_grad():
            old = completion_log_probs(predictor, prompt, responses, torch)
        reward = torch.tensor(group_rewards, device=predictor.device, dtype=torch.float32)
        advantage = (reward - reward.mean()) / reward.std().clamp_min(1e-4)
        for _epoch in range(2):
            current = completion_log_probs(predictor, prompt, responses, torch)
            ratio = torch.exp(current - old)
            bounded = ratio.clamp(0.8, 1.2)
            policy = -torch.min(ratio * advantage, bounded * advantage).mean()
            kl = 0.02 * ((current - old) ** 2).mean()
            loss = policy + kl
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                [p for p in predictor.model.parameters() if p.requires_grad], 1.0
            )
            optimizer.step()
        losses.append(float(loss.detach().cpu()))
        rewards.append(float(reward.mean().cpu()))
        clipped.append(float((ratio.detach().sub(1).abs() > 0.2).float().mean().cpu()))
    return {
        "grpo_steps": steps,
        "mean_loss": float(np.mean(losses)) if losses else 0.0,
        "mean_group_reward": float(np.mean(rewards)) if rewards else 0.0,
        "clip_fraction": float(np.mean(clipped)) if clipped else 0.0,
        "seconds": time.perf_counter() - started,
    }


def predict_scores(predictor, row, use_grpo_prompt: bool):
    torch, _, _, _ = require_llm_backend()
    prompt = (
        grpo_prompt(row, len(predictor.names))
        if use_grpo_prompt
        else sft_prompt(row)
    )
    completions = list(predictor.names)
    predictor.model.eval()
    with torch.inference_mode():
        return completion_log_probs(predictor, prompt, completions, torch).cpu().numpy()


def completion_log_probs(predictor, prompt, completions, torch):
    tokenizer = predictor.tokenizer
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"][-100:]
    rows, labels = [], []
    for completion in completions:
        target = tokenizer(completion, add_special_tokens=False)["input_ids"]
        rows.append(prompt_ids + target)
        labels.append([-100] * len(prompt_ids) + target)
    width = max(map(len, rows))
    input_ids, masks, padded_labels = [], [], []
    for ids, target in zip(rows, labels):
        padding = width - len(ids)
        input_ids.append(ids + [tokenizer.pad_token_id] * padding)
        masks.append([1] * len(ids) + [0] * padding)
        padded_labels.append(target + [-100] * padding)
    input_ids = torch.tensor(input_ids, device=predictor.device)
    target = torch.tensor(padded_labels, device=predictor.device)
    output = predictor.model(
        input_ids=input_ids,
        attention_mask=torch.tensor(masks, device=predictor.device),
    )
    logits = output.logits[:, :-1].float()
    shifted = target[:, 1:]
    valid = shifted.ne(-100)
    token_logp = torch.log_softmax(logits, -1).gather(
        -1, shifted.clamp_min(0).unsqueeze(-1)
    ).squeeze(-1)
    return (token_logp * valid).sum(-1) / valid.sum(-1).clamp_min(1)


def train_two_tower(data: AdsData, steps: int, seed: int):
    torch, nn, _, _ = require_llm_backend()
    torch.manual_seed(seed)
    device = device_for(torch)
    vectors = torch.tensor(data.item_vectors, device=device)
    user = nn.Linear(vectors.shape[1], 48, bias=False).to(device)
    item = nn.Linear(vectors.shape[1], 48, bias=False).to(device)
    optimizer = torch.optim.AdamW([*user.parameters(), *item.parameters()], lr=2e-3)
    rng = random.Random(seed)
    losses = []
    for _ in range(steps):
        rows = [data.train[rng.randrange(len(data.train))] for _ in range(32)]
        histories = torch.stack(
            [vectors[list(row.history)].mean(0) for row in rows]
        )
        targets = torch.tensor([row.target_item for row in rows], device=device)
        candidates = torch.cat(
            (targets[:, None], torch.randint(0, len(vectors), (len(rows), 31), device=device)),
            1,
        )
        user_vector = torch.nn.functional.normalize(user(histories), dim=-1)
        item_vector = torch.nn.functional.normalize(item(vectors[candidates]), dim=-1)
        logits = torch.einsum("bd,bnd->bn", user_vector, item_vector) / 0.1
        loss = torch.nn.functional.cross_entropy(logits, torch.zeros(len(rows), dtype=torch.long, device=device))
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return user, item, {
        "steps": steps,
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
    }


def tower_scores(user, item, data, row):
    torch, _, _, _ = require_llm_backend()
    device = next(user.parameters()).device
    vectors = torch.tensor(data.item_vectors, device=device)
    with torch.inference_mode():
        history = vectors[list(row.history)].mean(0, keepdim=True)
        query = torch.nn.functional.normalize(user(history), dim=-1)
        catalog = torch.nn.functional.normalize(item(vectors), dim=-1)
        return (query @ catalog.T).squeeze(0).cpu().numpy()


def sft_prompt(row: AdsExample) -> str:
    return row.prompt + "Return exactly one advertiser.\nAdvertiser: "


def grpo_prompt(row: AdsExample, list_size: int) -> str:
    return (
        row.prompt
        + f"Return exactly {list_size} ranked advertisers in XML.\n"
        + "<answer><advertiser_names>["
    )


def _response_group(row, names, rng, group_size, list_size):
    target = names[row.target_advertiser]
    others = [name for name in names if name != target]
    responses, rewards = [], []
    for index in range(group_size):
        length = list_size - 1 if index == group_size - 1 else list_size
        values = rng.sample(others, length)
        position = None
        if index < group_size - 1:
            position = min(index * 2, length - 1)
            values[position] = target
        responses.append("|".join(values) + "]</advertiser_names><interests>[]</interests></answer>")
        reward = 0.0
        if position is not None:
            one_based = position + 1
            reward = 0.1 * (list_size - one_based) + (2.0 if one_based <= 4 else 0.0)
        if length != list_size:
            reward -= min(0.1 * abs(length - list_size), 1.0) + 1.0
        rewards.append(reward)
    return responses, rewards
