from __future__ import annotations

from dataclasses import dataclass
import math
import random
import time

import numpy as np

from auto_research.runtime import device_for

from ..llm_lora import inject_lora, require_llm_backend
from .data import GenRecData, training_rows, verbalize


@dataclass(frozen=True)
class GenRecConfig:
    model_name: str = "HuggingFaceTB/SmolLM2-135M"
    maximum_history: int = 12
    steps: int = 120
    batch_size: int = 2
    learning_rate: float = 2e-4
    ranking_dimensions: int = 96
    ranking_weight: float = 0.8
    language_weight: float = 0.2
    evaluation_batch_size: int = 8


def _encode_examples(tokenizer, prompts, completions, maximum_length=192):
    rows = []
    labels = []
    prompt_ends = []
    for prompt, completion in zip(prompts, completions):
        prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        completion_ids = tokenizer(
            " " + completion + tokenizer.eos_token, add_special_tokens=False
        )["input_ids"]
        prompt_ids = prompt_ids[-max(1, maximum_length - len(completion_ids)):]
        rows.append(prompt_ids + completion_ids)
        labels.append([-100] * len(prompt_ids) + completion_ids)
        prompt_ends.append(len(prompt_ids) - 1)
    width = max(map(len, rows))
    input_ids = []
    attention = []
    padded_labels = []
    pooled_positions = []
    for ids, target, prompt_end in zip(rows, labels, prompt_ends):
        padding = width - len(ids)
        input_ids.append([tokenizer.pad_token_id] * padding + ids)
        attention.append([0] * padding + [1] * len(ids))
        padded_labels.append([-100] * padding + target)
        pooled_positions.append(padding + prompt_end)
    return input_ids, attention, padded_labels, pooled_positions


class GenRecRanker:
    """Actual causal LM + LoRA + catalog head used by the local Phase-2 run."""

    def __init__(self, data: GenRecData, config: GenRecConfig, seed: int):
        torch, nn, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
        torch.manual_seed(seed)
        self.torch = torch
        self.config = config
        self.data = data
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(config.model_name)
        self.trainable_lora_parameters = inject_lora(self.model, rank=4, alpha=8.0)
        hidden = self.model.config.hidden_size
        self.user_projection = nn.Linear(hidden, config.ranking_dimensions)
        self.catalog = nn.Embedding(len(data.item_texts), config.ranking_dimensions)
        self.catalog_bias = nn.Parameter(torch.zeros(len(data.item_texts)))
        self.device = device_for(torch)
        self.model.to(self.device)
        self.user_projection.to(self.device)
        self.catalog.to(self.device)
        self.catalog_bias.data = self.catalog_bias.data.to(self.device)
        self._initialize_catalog_from_text()

    def parameters(self):
        yield from (parameter for parameter in self.model.parameters() if parameter.requires_grad)
        yield from self.user_projection.parameters()
        yield from self.catalog.parameters()
        yield self.catalog_bias

    def _initialize_catalog_from_text(self):
        torch = self.torch
        vectors = []
        self.model.eval()
        with torch.inference_mode():
            for start in range(0, len(self.data.item_texts), 32):
                encoded = self.tokenizer(
                    self.data.item_texts[start:start + 32],
                    padding=True,
                    truncation=True,
                    max_length=32,
                    return_tensors="pt",
                ).to(self.device)
                output = self.model(**encoded, output_hidden_states=True, return_dict=True)
                mask = encoded["attention_mask"].unsqueeze(-1)
                pooled = (output.hidden_states[-1] * mask).sum(1) / mask.sum(1).clamp_min(1)
                vectors.append(pooled.float().cpu())
        text_vectors = torch.cat(vectors).to(self.device)
        # A fixed Johnson-Lindenstrauss projection preserves semantic geometry
        # without paying for a full SVD during every reproducibility run.
        text_vectors = text_vectors - text_vectors.mean(0, keepdim=True)
        generator = torch.Generator(device="cpu").manual_seed(17)
        projection = torch.randn(
            text_vectors.shape[1], self.config.ranking_dimensions, generator=generator
        ) / math.sqrt(self.config.ranking_dimensions)
        projected = text_vectors @ projection.to(self.device)
        self.catalog.weight.data.copy_(projected / projected.std().clamp_min(1e-6))

    def _reward_weights(self, histories, targets):
        values = []
        maximum_popularity = max(float(self.data.popularity.max()), 1.0)
        for history, target in zip(histories, targets):
            novelty = 1.0 - float(self.data.popularity[target]) / maximum_popularity
            seen_genres = {genre for item in history for genre in self.data.item_genres[item]}
            target_genres = set(self.data.item_genres[target])
            discovery = len(target_genres - seen_genres) / max(len(target_genres), 1)
            values.append(0.5 + 0.35 * novelty + 0.15 * discovery)
        weights = self.torch.tensor(values, dtype=self.torch.float32, device=self.device)
        return weights / weights.mean().clamp_min(1e-6)

    def train_phase2(self, seed: int):
        torch = self.torch
        rows = training_rows(self.data, self.config.maximum_history)
        rng = random.Random(seed)
        optimizer = torch.optim.AdamW(list(self.parameters()), lr=self.config.learning_rate)
        losses = []
        ranking_losses = []
        language_losses = []
        started = time.perf_counter()
        self.model.train()
        for _ in range(self.config.steps):
            batch = [rows[rng.randrange(len(rows))] for _ in range(self.config.batch_size)]
            histories = [row[0] for row in batch]
            targets = [row[1] for row in batch]
            prompts = [verbalize(history, self.data, self.config.maximum_history) for history in histories]
            completions = [self.data.item_texts[target] for target in targets]
            ids, masks, labels, positions = _encode_examples(self.tokenizer, prompts, completions)
            input_ids = torch.tensor(ids, device=self.device)
            output = self.model(
                input_ids=input_ids,
                attention_mask=torch.tensor(masks, device=self.device),
                labels=torch.tensor(labels, device=self.device),
                output_hidden_states=True,
                return_dict=True,
            )
            row_ids = torch.arange(len(batch), device=self.device)
            pooled = output.hidden_states[-1][row_ids, torch.tensor(positions, device=self.device)]
            users = self.user_projection(pooled.float())
            logits = users @ self.catalog.weight.T / math.sqrt(self.config.ranking_dimensions)
            logits = logits + self.catalog_bias
            per_example = torch.nn.functional.cross_entropy(
                logits, torch.tensor(targets, device=self.device), reduction="none"
            )
            ranking_loss = (per_example * self._reward_weights(histories, targets)).mean()
            language_loss = output.loss.float()
            loss = self.config.ranking_weight * ranking_loss + self.config.language_weight * language_loss
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(list(self.parameters()), 1.0)
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
            ranking_losses.append(float(ranking_loss.detach().cpu()))
            language_losses.append(float(language_loss.detach().cpu()))
        return {
            "initial_loss": float(np.mean(losses[: min(6, len(losses))])),
            "final_loss": float(np.mean(losses[-min(6, len(losses)):])),
            "final_ranking_loss": float(np.mean(ranking_losses[-6:])),
            "final_language_loss": float(np.mean(language_losses[-6:])),
            "steps": self.config.steps,
            "trainable_lora_parameters": self.trainable_lora_parameters,
            "trainable_total_parameters": sum(p.numel() for p in self.parameters()),
            "seconds": time.perf_counter() - started,
            "device": self.device.type,
        }

    def scores(self, histories):
        torch = self.torch
        prompts = [verbalize(tuple(history), self.data, self.config.maximum_history) for history in histories]
        self.model.eval()
        results = []
        with torch.inference_mode():
            for start in range(0, len(prompts), self.config.evaluation_batch_size):
                encoded = self.tokenizer(
                    prompts[start:start + self.config.evaluation_batch_size],
                    padding=True,
                    truncation=True,
                    max_length=192,
                    return_tensors="pt",
                ).to(self.device)
                output = self.model(**encoded, output_hidden_states=True, return_dict=True)
                positions = encoded["attention_mask"].sum(1) - 1
                rows = torch.arange(len(positions), device=self.device)
                pooled = output.hidden_states[-1][rows, positions]
                users = self.user_projection(pooled.float())
                logits = users @ self.catalog.weight.T / math.sqrt(self.config.ranking_dimensions)
                results.append((logits + self.catalog_bias).float().cpu())
        return torch.cat(results).numpy()
