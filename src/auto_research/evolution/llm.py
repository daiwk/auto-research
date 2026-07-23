from __future__ import annotations

from auto_research.runtime import device_for

import math
from pathlib import Path
import random
import time

import numpy as np

from .llm_data import load_llm_evolution_data
from .llm_model import MicroLMConfig, build_micro_lm
from .models import EvolutionTrial, Genome


class MicroLLMEvaluator:
    def __init__(
        self,
        dataset_dir: Path,
        dataset: str,
        steps: int,
        seeds: tuple[int, ...],
        allow_network: bool,
        maximum_train_tokens: int | None,
        maximum_eval_tokens: int | None,
        vocab_size: int,
        benchmark_suite: str = "public",
        fitness_metric: str = "primary",
    ):
        if dataset != "wikitext-2":
            raise ValueError("micro-llm currently uses wikitext-2")
        self.data = load_llm_evolution_data(
            dataset_dir,
            allow_network,
            vocab_size,
            maximum_train_tokens,
            maximum_eval_tokens,
            benchmark_suite,
        )
        self.steps, self.seeds = steps, seeds
        self.benchmark_suite = benchmark_suite
        self.fitness_metric = fitness_metric

    def summary(self):
        return {
            "train_tokens": len(self.data.train),
            "validation_tokens": len(self.data.validation),
            "test_tokens": len(self.data.test),
            "narrative_tokens": len(self.data.narrative),
            "instruction_train": len(self.data.instruction_train),
            "instruction_validation": len(self.data.instruction_validation),
            "preference_validation": len(self.data.preference_validation),
            "reasoning_validation": len(self.data.reasoning_validation),
            "benchmark_suite": self.benchmark_suite,
            "vocab_size": self.data.vocab_size,
            "tokenizer": str(self.data.tokenizer_path),
        }

    def evaluate(self, trial_id, generation, parent_id, genome, source_papers, rationale):
        started = time.monotonic()
        validations, trainings = [], []
        for seed in self.seeds:
            model, training, config = self._train(genome, seed)
            validations.append(self._metrics(model, config, self.data.validation))
            trainings.append(training)
        validation = _mean(validations)
        validation["primary"] = -(
            validation["lm_loss"] + 0.15 * validation["instruction_loss"]
        )
        validation["public_composite"] = -(
            validation["lm_loss"]
            + 0.15 * validation["instruction_loss"]
            + 0.10 * validation.get("preference_loss", 0.0)
            + 0.05 * validation.get("reasoning_nll", 0.0)
        )
        validation["composite_loss"] = -validation["public_composite"]
        validation["fitness"] = validation[
            "public_composite"
            if self.fitness_metric == "public_composite"
            else "primary"
        ]
        training = {
            "initial_loss": float(np.mean([row["initial_loss"] for row in trainings])),
            "final_loss": float(np.mean([row["final_loss"] for row in trainings])),
            "post_training_loss": float(np.mean([row["post_training_loss"] for row in trainings])),
            "reward_bearing_group_rate": float(
                np.mean([row["reward_bearing_group_rate"] for row in trainings])
            ),
            "parameters": int(np.mean([row["parameters"] for row in trainings])),
            "device": trainings[0]["device"],
            "seeds": list(self.seeds),
        }
        return EvolutionTrial(
            trial_id, generation, parent_id, genome, validation, training,
            source_papers, rationale, time.monotonic() - started,
        )

    def test(self, genome):
        rows = []
        for seed in self.seeds:
            model, _, config = self._train(genome, seed)
            rows.append(self._metrics(model, config, self.data.test))
        result = _mean(rows)
        result["primary"] = -(
            result["lm_loss"] + 0.15 * result["instruction_loss"]
        )
        result["public_composite"] = -(
            result["lm_loss"]
            + 0.15 * result["instruction_loss"]
            + 0.10 * result.get("preference_loss", 0.0)
            + 0.05 * result.get("reasoning_nll", 0.0)
        )
        result["composite_loss"] = -result["public_composite"]
        return result

    def _train(self, genome: Genome, seed: int):
        import torch

        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        device = device_for(torch)
        config = MicroLMConfig(
            vocab_size=self.data.vocab_size,
            dimensions=genome.dimensions,
            layers=genome.layers,
            heads=genome.heads,
            kv_heads=genome.kv_heads,
            sequence_length=genome.sequence_length,
            expansion=genome.expansion,
        )
        model = build_micro_lm(genome.architecture, config).to(device)
        optimizers = {"adamw": torch.optim.AdamW, "adam": torch.optim.Adam, "adagrad": torch.optim.Adagrad}
        optimizer = optimizers[genome.optimizer](model.parameters(), lr=genome.learning_rate)
        rng = np.random.default_rng(seed)
        losses = []
        model.train()
        for step in range(self.steps):
            source = self._pretrain_source(genome, step, rng)
            inputs, labels = _sample_lm_batch(source, genome.batch_size, genome.sequence_length, rng, device, torch)
            optimizer.zero_grad(set_to_none=True)
            logits = model(inputs)
            loss = torch.nn.functional.cross_entropy(logits.reshape(-1, config.vocab_size), labels.reshape(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        post_losses, post_stats = self._post_train(
            model, optimizer, genome, config, rng, device, torch
        )
        return model, {
            "initial_loss": float(np.mean(losses[: min(10, len(losses))])),
            "final_loss": float(np.mean(losses[-min(10, len(losses)) :])),
            "post_training_loss": float(np.mean(post_losses)) if post_losses else 0.0,
            "parameters": sum(parameter.numel() for parameter in model.parameters()),
            "device": device.type,
            **post_stats,
        }, config

    def _pretrain_source(self, genome, step, rng):
        if genome.data_recipe == "wikitext":
            return self.data.train
        ratio = genome.data_mix_ratio
        if genome.data_recipe == "curriculum":
            ratio *= max(0.0, 1.0 - step / max(self.steps - 1, 1))
        return self.data.narrative if rng.random() < ratio else self.data.train

    def _post_train(self, model, optimizer, genome, config, rng, device, torch):
        if genome.post_training == "none" or genome.post_steps <= 0:
            return [], {"reward_bearing_group_rate": 0.0}
        for group in optimizer.param_groups:
            group["lr"] = genome.learning_rate * (0.35 if genome.post_training == "sft_low_lr" else 0.5)
        losses = []
        reward_bearing_groups = 0
        if genome.post_training == "dynamic_rubric":
            rubric_logits = torch.zeros(4, device=device, requires_grad=True)
            optimizer.add_param_group(
                {"params": [rubric_logits], "lr": genome.learning_rate}
            )
        for _ in range(genome.post_steps):
            if genome.post_training == "dynamic_rubric":
                example = self.data.preference_train[
                    int(rng.integers(len(self.data.preference_train)))
                ]
                scores = _candidate_scores_tensor(
                    model, example, config, device, torch
                )
                hard = 1 + int(torch.argmax(scores[1:].detach()).item())
                rubrics = torch.tensor(
                    example.rubrics, dtype=torch.float32, device=device
                )
                response_variance = rubrics.var(dim=0, unbiased=False)
                weights = torch.softmax(rubric_logits + response_variance, dim=0)
                anchor = torch.tensor(
                    [0.20, 0.35, 0.20, 0.25], device=device
                )
                evaluator_gap = (
                    (rubrics[example.gold] - rubrics[hard]) * weights
                ).sum()
                evaluator_loss = torch.nn.functional.softplus(-evaluator_gap)
                evaluator_loss = evaluator_loss + 0.10 * (
                    weights - anchor
                ).pow(2).mean()
                policy_gap = scores[example.gold] - scores[hard]
                policy_loss = (
                    torch.nn.functional.softplus(-policy_gap)
                    * evaluator_gap.detach().clamp_min(0.05)
                )
                loss = policy_loss + 0.25 * evaluator_loss
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                losses.append(float(loss.detach().cpu()))
                continue
            if genome.post_training == "off_context_grpo":
                example = self.data.reasoning_train[
                    int(rng.integers(len(self.data.reasoning_train)))
                ]
                scores = _candidate_scores_tensor(
                    model, example, config, device, torch
                )
                target = torch.softmax(scores, dim=0)
                guided = scores.detach().clone()
                guided[example.gold] += 2.0
                behavior = torch.softmax(guided, dim=0)
                actions = torch.multinomial(
                    behavior, num_samples=8, replacement=True
                )
                rewards = (actions == example.gold).float()
                advantages = rewards - rewards.mean()
                reward_bearing_groups += int(
                    0 < rewards.sum().item() < len(rewards)
                )
                if torch.allclose(advantages, torch.zeros_like(advantages)):
                    continue
                ratio = (
                    target[actions].detach()
                    / behavior[actions].clamp_min(1e-8)
                ).clamp(0.1, 5.0)
                loss = -(
                    ratio
                    * advantages
                    * torch.log_softmax(scores, dim=0)[actions]
                ).mean()
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                losses.append(float(loss.detach().cpu()))
                continue
            inputs, labels = _sample_instruction_batch(
                self.data.instruction_train, genome.batch_size, genome.sequence_length, rng, device, torch
            )
            optimizer.zero_grad(set_to_none=True)
            alpha = genome.neftune_alpha if genome.post_training == "neftune" else 0.0
            logits = model(inputs, embedding_noise_alpha=alpha)
            loss = torch.nn.functional.cross_entropy(
                logits.reshape(-1, config.vocab_size), labels.reshape(-1), ignore_index=-100
            )
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        return losses, {
            "reward_bearing_group_rate": (
                reward_bearing_groups / genome.post_steps
                if genome.post_training == "off_context_grpo"
                else 0.0
            )
        }

    def _metrics(self, model, config, tokens):
        import torch

        device = next(model.parameters()).device
        model.eval()
        lm_losses = []
        with torch.inference_mode():
            stride = config.sequence_length
            maximum = min(len(tokens) - stride - 1, stride * 32)
            for start in range(0, maximum, stride):
                values = torch.tensor(tokens[start:start + stride + 1], dtype=torch.long, device=device)
                logits = model(values[:-1][None])
                loss = torch.nn.functional.cross_entropy(logits[0], values[1:])
                lm_losses.append(float(loss.cpu()))
        instruction_loss = _instruction_loss(model, self.data.instruction_validation, config, device, torch)
        lm_loss = float(np.mean(lm_losses))
        result = {
            "lm_loss": lm_loss,
            "perplexity": math.exp(min(lm_loss, 20.0)),
            "instruction_loss": instruction_loss,
        }
        if self.benchmark_suite == "public":
            preference = _candidate_metrics(
                model,
                self.data.preference_validation,
                config,
                device,
                torch,
            )
            reasoning = _candidate_metrics(
                model,
                self.data.reasoning_validation,
                config,
                device,
                torch,
            )
            result.update(
                {
                    "preference_accuracy": preference["accuracy"],
                    "preference_loss": preference["loss"],
                    "reasoning_pass_at_1": reasoning["accuracy"],
                    "reasoning_nll": reasoning["loss"],
                }
            )
        return result


def _sample_lm_batch(tokens, batch_size, length, rng, device, torch):
    starts = rng.integers(0, len(tokens) - length - 1, size=batch_size)
    rows = np.stack([tokens[start:start + length + 1] for start in starts])
    values = torch.tensor(rows, dtype=torch.long, device=device)
    return values[:, :-1], values[:, 1:]


def _sample_instruction_batch(examples, batch_size, length, rng, device, torch):
    selected = [examples[int(rng.integers(0, len(examples)))] for _ in range(batch_size)]
    inputs, labels = [], []
    for full, response_start in selected:
        if len(full) > length + 1:
            offset = max(0, min(response_start - 8, len(full) - length - 1))
            full = full[offset:offset + length + 1]
            response_start -= offset
        padded = np.pad(full, (0, max(0, length + 1 - len(full))), constant_values=0)[: length + 1]
        row_labels = padded[1:].copy()
        row_labels[: max(0, response_start - 1)] = -100
        row_labels[len(full) - 1:] = -100
        inputs.append(padded[:-1])
        labels.append(row_labels)
    return (
        torch.tensor(np.stack(inputs), dtype=torch.long, device=device),
        torch.tensor(np.stack(labels), dtype=torch.long, device=device),
    )


def _instruction_loss(model, examples, config, device, torch):
    losses = []
    rng = np.random.default_rng(0)
    with torch.inference_mode():
        for start in range(0, min(len(examples), 32), 8):
            batch = examples[start:start + 8]
            inputs, labels = _sample_instruction_batch(batch, len(batch), config.sequence_length, rng, device, torch)
            logits = model(inputs)
            loss = torch.nn.functional.cross_entropy(
                logits.reshape(-1, config.vocab_size), labels.reshape(-1), ignore_index=-100
            )
            losses.append(float(loss.cpu()))
    return float(np.mean(losses))


def _candidate_scores_tensor(model, example, config, device, torch):
    inputs, labels, masks = [], [], []
    for full, response_start in zip(
        example.candidates, example.response_starts
    ):
        row_inputs, row_labels, row_mask = _candidate_row(
            full, response_start, config.sequence_length
        )
        inputs.append(row_inputs)
        labels.append(row_labels)
        masks.append(row_mask)
    input_tensor = torch.tensor(
        np.stack(inputs), dtype=torch.long, device=device
    )
    label_tensor = torch.tensor(
        np.stack(labels), dtype=torch.long, device=device
    )
    mask_tensor = torch.tensor(
        np.stack(masks), dtype=torch.float32, device=device
    )
    logits = model(input_tensor)
    token_log_probs = torch.log_softmax(logits, dim=-1).gather(
        -1, label_tensor.unsqueeze(-1)
    ).squeeze(-1)
    return (token_log_probs * mask_tensor).sum(-1) / mask_tensor.sum(
        -1
    ).clamp_min(1.0)


def _candidate_row(full, response_start, length):
    if len(full) > length + 1:
        offset = max(
            0, min(response_start - 8, len(full) - length - 1)
        )
        full = full[offset : offset + length + 1]
        response_start -= offset
    original_length = len(full)
    padded = np.pad(
        full,
        (0, max(0, length + 1 - len(full))),
        constant_values=0,
    )[: length + 1]
    labels = padded[1:].copy()
    mask = np.zeros(length, dtype=np.float32)
    begin = max(0, response_start - 1)
    end = max(begin + 1, min(length, original_length - 1))
    mask[begin:end] = 1.0
    return padded[:-1], labels, mask


def _candidate_metrics(model, examples, config, device, torch):
    if not examples:
        return {"accuracy": 0.0, "loss": 0.0}
    correct, losses = 0, []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(examples), 4):
            batch = examples[start : start + 4]
            candidate_count = len(batch[0].candidates)
            rows = [
                _candidate_row(full, response_start, config.sequence_length)
                for example in batch
                for full, response_start in zip(
                    example.candidates, example.response_starts
                )
            ]
            input_tensor = torch.tensor(
                np.stack([row[0] for row in rows]),
                dtype=torch.long,
                device=device,
            )
            label_tensor = torch.tensor(
                np.stack([row[1] for row in rows]),
                dtype=torch.long,
                device=device,
            )
            mask_tensor = torch.tensor(
                np.stack([row[2] for row in rows]),
                dtype=torch.float32,
                device=device,
            )
            logits = model(input_tensor)
            token_log_probs = torch.log_softmax(logits, dim=-1).gather(
                -1, label_tensor.unsqueeze(-1)
            ).squeeze(-1)
            scores = (
                (token_log_probs * mask_tensor).sum(-1)
                / mask_tensor.sum(-1).clamp_min(1.0)
            ).reshape(len(batch), candidate_count)
            gold = torch.tensor(
                [example.gold for example in batch],
                dtype=torch.long,
                device=device,
            )
            correct += int((torch.argmax(scores, dim=1) == gold).sum().item())
            losses.extend(
                torch.nn.functional.cross_entropy(
                    scores, gold, reduction="none"
                )
                .detach()
                .cpu()
                .tolist()
            )
    return {
        "accuracy": correct / len(examples),
        "loss": float(np.mean(losses)),
    }


def _mean(rows):
    return {key: float(np.mean([row[key] for row in rows])) for key in rows[0]}
