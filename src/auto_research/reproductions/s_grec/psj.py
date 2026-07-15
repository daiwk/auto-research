from __future__ import annotations

import random
import time
from dataclasses import dataclass

import numpy as np

from ..llm_lora import device_for, inject_lora, require_llm_backend
from .data import ASPECT_VALUES, AspectExample, SGreCData, aspect_prompt, user_prompt


@dataclass
class PersonalizedSemanticJudge:
    model: object
    tokenizer: object
    device: object


def train_psj(
    data: SGreCData,
    model_name: str,
    sft_steps: int,
    aspect_grpo_steps: int,
    pair_grpo_steps: int,
    seed: int,
):
    torch, nn, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    lm = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
    trainable = inject_lora(lm, rank=4, alpha=8.0)
    hidden = lm.get_input_embeddings().weight.shape[1]

    class PSJ(nn.Module):
        def __init__(self):
            super().__init__()
            self.lm = lm
            self.aspect_heads = nn.ModuleList(
                [nn.Linear(hidden, len(values)) for values in ASPECT_VALUES]
            )
            self.weight_head = nn.Linear(hidden, 3 * 5)

        def encode(self, prompts):
            encoded = tokenizer(
                prompts,
                padding=True,
                truncation=True,
                max_length=160,
                return_tensors="pt",
            ).to(device)
            output = self.lm(
                **encoded, output_hidden_states=True, use_cache=False, return_dict=True
            )
            positions = encoded["attention_mask"].sum(1) - 1
            return output.hidden_states[-1][torch.arange(len(prompts), device=device), positions]

        def aspects(self, prompts):
            hidden_state = self.encode(prompts)
            return [head(hidden_state) for head in self.aspect_heads]

        def weights(self, prompts):
            return self.weight_head(self.encode(prompts)).view(-1, 3, 5)

    device = device_for(torch)
    model = PSJ().to(device)
    judge = PersonalizedSemanticJudge(model, tokenizer, device)
    optimizer = torch.optim.AdamW(
        [parameter for parameter in model.parameters() if parameter.requires_grad], lr=2e-4
    )
    rng = random.Random(seed)
    started = time.perf_counter()
    sft_losses = []
    model.train()
    for _ in range(sft_steps):
        rows = [data.aspects[rng.randrange(len(data.aspects))] for _ in range(4)]
        logits = model.aspects([aspect_prompt(data, row) for row in rows])
        loss = sum(
            torch.nn.functional.cross_entropy(
                value,
                torch.tensor([row.labels[index] for row in rows], device=device),
            )
            for index, value in enumerate(logits)
        ) / len(logits)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [parameter for parameter in model.parameters() if parameter.requires_grad], 1.0
        )
        optimizer.step()
        sft_losses.append(float(loss.detach().cpu()))
    sft_accuracy = aspect_accuracy(judge, data, data.aspects[: min(128, len(data.aspects))])
    aspect_grpo = _train_aspect_grpo(judge, data, optimizer, aspect_grpo_steps, rng, torch)
    aligned_accuracy = aspect_accuracy(judge, data, data.aspects[: min(128, len(data.aspects))])
    pair_grpo = _train_pair_grpo(judge, data, optimizer, pair_grpo_steps, rng, torch)
    pair_accuracy = preference_accuracy(judge, data, data.pairs[: min(32, len(data.pairs))])
    window = min(5, len(sft_losses))
    return judge, {
        "model": model_name,
        "trainable_lora_parameters": trainable,
        "sft_steps": sft_steps,
        "sft_initial_loss": float(np.mean(sft_losses[:window])),
        "sft_final_loss": float(np.mean(sft_losses[-window:])),
        "sft_point_accuracy": sft_accuracy,
        "aligned_point_accuracy": aligned_accuracy,
        "aspect_grpo": aspect_grpo,
        "pair_grpo": pair_grpo,
        "pairwise_accuracy": pair_accuracy,
        "seconds": time.perf_counter() - started,
        "device": device.type,
    }


def _train_aspect_grpo(judge, data, optimizer, steps, rng, torch, group_size=4):
    model, device = judge.model, judge.device
    pool = list(data.aspects[: min(32, len(data.aspects))])
    model.eval()
    with torch.inference_mode():
        reference_batch = model.aspects([aspect_prompt(data, row) for row in pool])
        reference = {
            index: [value[index : index + 1].detach() for value in reference_batch]
            for index in range(len(pool))
        }
    losses, rewards, clips = [], [], []
    model.train()
    for _ in range(steps):
        index = rng.randrange(len(pool))
        row = pool[index]
        logits = model.aspects([aspect_prompt(data, row)])
        distributions = [torch.distributions.Categorical(logits=value[0]) for value in logits]
        actions = torch.stack(
            [torch.stack([distribution.sample() for distribution in distributions]) for _ in range(group_size)]
        )
        old_logp = sum(
            distributions[dimension].log_prob(actions[:, dimension])
            for dimension in range(3)
        ).detach()
        target = torch.tensor(row.labels, device=device)
        exact = actions.eq(target).float().sum(1)
        proximity = torch.stack(
            [
                1.0
                - (actions[:, dimension] - target[dimension]).abs()
                / max(1, len(ASPECT_VALUES[dimension]) - 1)
                for dimension in range(3)
            ],
            1,
        ).sum(1)
        reward = exact + proximity
        advantage = (reward - reward.mean()) / reward.std().clamp_min(1e-4)
        current = sum(
            torch.log_softmax(logits[dimension][0], -1)[actions[:, dimension]]
            for dimension in range(3)
        )
        ratio = torch.exp(current - old_logp)
        clipped = ratio.clamp(0.8, 1.2)
        policy = -torch.min(ratio * advantage, clipped * advantage).mean()
        kl = sum(
            torch.nn.functional.kl_div(
                torch.log_softmax(logits[dimension], -1),
                torch.softmax(reference[index][dimension], -1),
                reduction="batchmean",
            )
            for dimension in range(3)
        ) / 3
        loss = policy + 0.04 * kl
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [parameter for parameter in model.parameters() if parameter.requires_grad], 1.0
        )
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        rewards.append(float(reward.mean().cpu()))
        clips.append(float((ratio.detach().sub(1).abs() > 0.2).float().mean().cpu()))
    return {
        "steps": steps,
        "mean_loss": float(np.mean(losses)) if losses else 0.0,
        "mean_reward": float(np.mean(rewards)) if rewards else 0.0,
        "clip_fraction": float(np.mean(clips)) if clips else 0.0,
        "kl_coefficient": 0.04,
    }


def _train_pair_grpo(judge, data, optimizer, steps, rng, torch, group_size=8):
    model, device = judge.model, judge.device
    pool = list(data.pairs[: min(32, len(data.pairs))])
    model.eval()
    with torch.inference_mode():
        weight_reference = model.weights(
            [user_prompt(data, row.history) for row in pool]
        ).detach()
        aspect_rows = [
            AspectExample(row.history, candidate, (0, 0, 0))
            for row in pool
            for candidate in (row.preferred, row.rejected)
        ]
        aspect_values = _expected_aspects(
            model.aspects([aspect_prompt(data, row) for row in aspect_rows]), torch, device
        ).view(len(pool), 2, 3)
    losses, rewards, clips = [], [], []
    model.train()
    for _ in range(steps):
        index = rng.randrange(len(pool))
        row = pool[index]
        logits = model.weights([user_prompt(data, row.history)])[0]
        distributions = [torch.distributions.Categorical(logits=logits[d]) for d in range(3)]
        actions = torch.stack(
            [torch.stack([distribution.sample() for distribution in distributions]) for _ in range(group_size)]
        )
        raw_weights = actions.float() + 1e-3
        weights = raw_weights / raw_weights.sum(1, keepdim=True)
        values = aspect_values[index]
        score = weights @ values.T
        reward = (score[:, 0] > score[:, 1]).float()
        advantage = (reward - reward.mean()) / reward.std().clamp_min(1e-4)
        old_logp = sum(
            distributions[dimension].log_prob(actions[:, dimension]) for dimension in range(3)
        ).detach()
        current = sum(
            torch.log_softmax(logits[dimension], -1)[actions[:, dimension]] for dimension in range(3)
        )
        ratio = torch.exp(current - old_logp)
        policy = -torch.min(
            ratio * advantage, ratio.clamp(0.8, 1.2) * advantage
        ).mean()
        kl = torch.nn.functional.kl_div(
            torch.log_softmax(logits, -1),
            torch.softmax(weight_reference[index], -1),
            reduction="batchmean",
        )
        loss = policy + 0.04 * kl
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [parameter for parameter in model.parameters() if parameter.requires_grad], 1.0
        )
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        rewards.append(float(reward.mean().cpu()))
        clips.append(float((ratio.detach().sub(1).abs() > 0.2).float().mean().cpu()))
    return {
        "steps": steps,
        "mean_loss": float(np.mean(losses)) if losses else 0.0,
        "mean_pair_reward": float(np.mean(rewards)) if rewards else 0.0,
        "clip_fraction": float(np.mean(clips)) if clips else 0.0,
        "group_size": group_size,
    }


def semantic_aspects(judge, data, history, candidates, torch=None):
    if torch is None:
        torch, _, _, _ = require_llm_backend()
    rows = [AspectExample(history, candidate, (0, 0, 0)) for candidate in candidates]
    judge.model.eval()
    with torch.inference_mode():
        logits = judge.model.aspects([aspect_prompt(data, row) for row in rows])
        return _expected_aspects(logits, torch, judge.device)


def semantic_rewards(judge, data, history, candidates):
    torch, _, _, _ = require_llm_backend()
    judge.model.eval()
    with torch.inference_mode():
        aspects = semantic_aspects(judge, data, history, candidates, torch)
        logits = judge.model.weights([user_prompt(data, history)])[0]
        levels = torch.arange(5, device=judge.device, dtype=torch.float32)
        weights = (torch.softmax(logits, -1) * levels).sum(-1).clamp_min(1e-3)
        weights /= weights.sum()
        return (aspects @ weights).cpu().numpy()


def aspect_accuracy(judge, data, rows):
    torch, _, _, _ = require_llm_backend()
    if not rows:
        return 0.0
    correct = total = 0
    judge.model.eval()
    with torch.inference_mode():
        for start in range(0, len(rows), 16):
            batch = rows[start : start + 16]
            logits = judge.model.aspects([aspect_prompt(data, row) for row in batch])
            for dimension, value in enumerate(logits):
                predicted = value.argmax(-1).cpu().tolist()
                correct += sum(
                    int(prediction == row.labels[dimension])
                    for prediction, row in zip(predicted, batch)
                )
                total += len(batch)
    return correct / max(1, total)


def preference_accuracy(judge, data, rows):
    torch, _, _, _ = require_llm_backend()
    if not rows:
        return 0.0
    aspect_rows = [
        AspectExample(row.history, candidate, (0, 0, 0))
        for row in rows
        for candidate in (row.preferred, row.rejected)
    ]
    judge.model.eval()
    with torch.inference_mode():
        aspects = _expected_aspects(
            judge.model.aspects([aspect_prompt(data, row) for row in aspect_rows]),
            torch,
            judge.device,
        ).view(len(rows), 2, 3)
        logits = judge.model.weights([user_prompt(data, row.history) for row in rows])
        levels = torch.arange(5, device=judge.device, dtype=torch.float32)
        weights = (torch.softmax(logits, -1) * levels).sum(-1).clamp_min(1e-3)
        weights /= weights.sum(-1, keepdim=True)
        scores = (aspects * weights[:, None]).sum(-1)
        return float((scores[:, 0] > scores[:, 1]).float().mean().cpu())


def _expected_aspects(logits, torch, device):
    output = []
    for dimension, values in enumerate(ASPECT_VALUES):
        scale = torch.tensor(values, device=device)
        output.append((torch.softmax(logits[dimension], -1) * scale).sum(-1))
    return torch.stack(output, 1)
