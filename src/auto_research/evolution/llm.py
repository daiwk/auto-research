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
    ):
        if dataset != "wikitext-2":
            raise ValueError("micro-llm currently uses wikitext-2")
        self.data = load_llm_evolution_data(
            dataset_dir, allow_network, vocab_size, maximum_train_tokens, maximum_eval_tokens
        )
        self.steps, self.seeds = steps, seeds

    def summary(self):
        return {
            "train_tokens": len(self.data.train),
            "validation_tokens": len(self.data.validation),
            "test_tokens": len(self.data.test),
            "narrative_tokens": len(self.data.narrative),
            "instruction_train": len(self.data.instruction_train),
            "instruction_validation": len(self.data.instruction_validation),
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
        validation["composite_loss"] = validation["lm_loss"] + 0.15 * validation["instruction_loss"]
        validation["fitness"] = -validation["composite_loss"]
        training = {
            "initial_loss": float(np.mean([row["initial_loss"] for row in trainings])),
            "final_loss": float(np.mean([row["final_loss"] for row in trainings])),
            "post_training_loss": float(np.mean([row["post_training_loss"] for row in trainings])),
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
        result["composite_loss"] = result["lm_loss"] + 0.15 * result["instruction_loss"]
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
        post_losses = self._post_train(model, optimizer, genome, config, rng, device, torch)
        return model, {
            "initial_loss": float(np.mean(losses[: min(10, len(losses))])),
            "final_loss": float(np.mean(losses[-min(10, len(losses)) :])),
            "post_training_loss": float(np.mean(post_losses)) if post_losses else 0.0,
            "parameters": sum(parameter.numel() for parameter in model.parameters()),
            "device": device.type,
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
            return []
        for group in optimizer.param_groups:
            group["lr"] = genome.learning_rate * (0.35 if genome.post_training == "sft_low_lr" else 0.5)
        losses = []
        for _ in range(genome.post_steps):
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
        return losses

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
        return {
            "lm_loss": lm_loss,
            "perplexity": math.exp(min(lm_loss, 20.0)),
            "instruction_loss": instruction_loss,
        }


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


def _mean(rows):
    return {key: float(np.mean([row[key] for row in rows])) for key in rows[0]}
