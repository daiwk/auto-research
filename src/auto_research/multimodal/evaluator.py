from __future__ import annotations

import copy
import time

import numpy as np

from auto_research.runtime import device_for
from ..evolution.models import EvolutionTrial, Genome
from ..evolution.statistics import mean_with_std
from .data import MultimodalSplit, load_multimodal_data
from .model import build_micro_vlm


class MicroVLMEvaluator:
    def __init__(
        self, dataset_dir, dataset: str, steps: int, seeds: tuple[int, ...],
        allow_network: bool = True, maximum_examples: int | None = None,
    ):
        self.data = load_multimodal_data(
            dataset, dataset_dir, allow_network, maximum_examples
        )
        self.dataset, self.steps, self.seeds = dataset, steps, seeds

    def summary(self):
        return {
            "dataset": self.dataset,
            "train_examples": len(self.data.train.answers),
            "validation_examples": len(self.data.validation.answers),
            "test_examples": len(self.data.test.answers),
            "modalities": ["image", "question", "answer"],
            "controls": ["original", "shuffled-image", "blank-image"],
            "source": self.data.source,
            "license": self.data.license,
            "evaluation_tier": self.data.evaluation_tier,
            "offline": self.dataset == "visual-shapes",
        }

    def evaluate(self, trial_id, generation, parent_id, genome,
                 source_papers, rationale):
        started = time.monotonic()
        rows, training = [], []
        for seed in self.seeds:
            model, diagnostics = self._train(genome, seed)
            rows.append(self._metrics(model, self.data.validation))
            training.append(diagnostics)
        validation = mean_with_std(rows)
        validation["primary"] = validation["accuracy"] + 0.25 * max(
            0.0, validation["visual_dependency_delta"]
        )
        validation["fitness"] = validation["primary"]
        validation["fitness_std"] = validation["accuracy_std"]
        return EvolutionTrial(
            trial_id, generation, parent_id, genome, validation,
            {
                "initial_loss": float(np.mean([x["initial_loss"] for x in training])),
                "final_loss": float(np.mean([x["final_loss"] for x in training])),
                "parameters": int(np.mean([x["parameters"] for x in training])),
                "device": training[0]["device"],
                "architecture_stats": training[0]["architecture_stats"],
                "seeds": list(self.seeds),
            },
            source_papers, rationale, time.monotonic() - started,
        )

    def test(self, genome):
        rows = []
        for seed in self.seeds:
            model, _ = self._train(genome, seed)
            rows.append(self._metrics(model, self.data.test))
        result = mean_with_std(rows)
        result["primary"] = result["accuracy"] + 0.25 * max(
            0.0, result["visual_dependency_delta"]
        )
        return result

    def _train(self, genome: Genome, seed: int):
        import torch

        torch.manual_seed(seed)
        np.random.seed(seed)
        device = device_for(torch)
        model = build_micro_vlm(
            genome.architecture, genome.dimensions, min(genome.heads, 4),
            num_questions=len(self.data.question_names),
            num_answers=len(self.data.answer_names),
        ).to(device)
        generation_branch = None
        target_patch = None
        parameters = list(model.parameters())
        if genome.multimodal_objective == "gas-nep":
            generation_branch = torch.nn.Sequential(
                torch.nn.Linear(genome.dimensions, genome.dimensions),
                torch.nn.GELU(),
                torch.nn.Linear(genome.dimensions, genome.dimensions),
            ).to(device)
            target_patch = copy.deepcopy(model.patch).to(device).eval()
            for parameter in target_patch.parameters():
                parameter.requires_grad_(False)
            parameters += list(generation_branch.parameters())
        optimizer = torch.optim.AdamW(parameters, lr=genome.learning_rate)
        rng = np.random.default_rng(seed)
        split = self.data.train
        losses = []
        model.train()
        generation_losses = []
        for step in range(self.steps):
            indices = rng.integers(0, len(split.answers), size=genome.batch_size)
            images = torch.from_numpy(split.images[indices]).to(device)
            questions = torch.from_numpy(split.questions[indices]).to(device)
            answers = torch.from_numpy(split.answers[indices]).to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(images, questions)
            if genome.multimodal_objective == "siglip2":
                targets = torch.nn.functional.one_hot(
                    answers, num_classes=logits.shape[-1]
                ).float()
                loss = torch.nn.functional.binary_cross_entropy_with_logits(
                    logits, targets
                )
                masked = images.clone()
                masked[:, :, 8:24, 8:24] = 0
                masked_logits = model(masked, questions)
                loss = loss + 0.15 * torch.nn.functional.mse_loss(
                    torch.sigmoid(masked_logits), torch.sigmoid(logits.detach())
                )
            else:
                loss = torch.nn.functional.cross_entropy(logits, answers)
                if generation_branch is not None:
                    shared = model.patch(images).flatten(2).transpose(1, 2)
                    predicted = generation_branch(shared[:, :-1])
                    with torch.no_grad():
                        target = target_patch(images.flip(-1)).flatten(2).transpose(1, 2)
                    generation_loss = 1 - torch.nn.functional.cosine_similarity(
                        predicted, target[:, 1:], dim=-1
                    ).mean()
                    weight = 0.015 + 0.985 * min(1.0, step / max(1, self.steps * 2 / 3))
                    loss = loss + weight * generation_loss
                    generation_losses.append(float(generation_loss.detach().cpu()))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(parameters, 1.0)
            optimizer.step()
            if target_patch is not None:
                with torch.no_grad():
                    for ema, online in zip(target_patch.parameters(), model.patch.parameters()):
                        ema.mul_(0.999).add_(online, alpha=0.001)
            losses.append(float(loss.detach().cpu()))
        return model, {
            "initial_loss": float(np.mean(losses[: min(10, len(losses))])),
            "final_loss": float(np.mean(losses[-min(10, len(losses)) :])),
            "parameters": sum(p.numel() for p in model.parameters()),
            "device": device.type,
            "architecture_stats": {
                **model.architecture_stats(),
                "training_only_generation_parameters": (
                    sum(p.numel() for p in generation_branch.parameters())
                    if generation_branch is not None else 0
                ),
                "generation_branch_discarded_at_inference": generation_branch is not None,
                "final_generation_loss": (
                    float(np.mean(generation_losses[-10:])) if generation_losses else None
                ),
            },
        }

    def _metrics(self, model, split: MultimodalSplit):
        import torch

        device = next(model.parameters()).device
        images = torch.from_numpy(split.images).to(device)
        questions = torch.from_numpy(split.questions).to(device)
        answers = torch.from_numpy(split.answers).to(device)
        model.eval()
        with torch.no_grad():
            predictions = model(images, questions).argmax(-1)
            shuffled = model(images.roll(1, 0), questions).argmax(-1)
            blank = model(torch.zeros_like(images), questions).argmax(-1)
        accuracy = float((predictions == answers).float().mean().cpu())
        shuffled_accuracy = float((shuffled == answers).float().mean().cpu())
        blank_accuracy = float((blank == answers).float().mean().cpu())
        return {
            "accuracy": accuracy,
            "shuffled_image_accuracy": shuffled_accuracy,
            "blank_image_accuracy": blank_accuracy,
            "visual_dependency_delta": accuracy - shuffled_accuracy,
            "blank_image_delta": accuracy - blank_accuracy,
        }
