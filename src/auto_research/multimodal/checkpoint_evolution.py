"""Validation-only evolution of a real public VLM checkpoint."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import time
from typing import Any

from ..evolution.models import EvolutionTrial, Genome
from ..evolution.statistics import mean_with_std
from ..runtime import device_for
from .benchmarks import _read_payload, _scienceqa_problems, score_benchmark
from .checkpoint import (
    CheckpointPredictionConfig,
    _generate_one,
    _load_checkpoint,
    _open_image,
    iter_prediction_examples,
)


class CheckpointVLMEvaluator:
    """Evaluate inference recipes while loading the checkpoint only once.

    Evolution reads the official validation split. ``test`` is invoked by the
    shared controller only after all generations finish, for baseline and
    champion. No model weights are updated and no prediction files are written.
    """

    def __init__(
        self,
        benchmark: str,
        annotations: Path | None,
        image_root: Path | None,
        model_id: str,
        checkpoint_path: Path | None,
        revision: str,
        seeds: tuple[int, ...],
        maximum_examples: int,
        offline: bool,
        *,
        processor: Any | None = None,
        model: Any | None = None,
        torch_module: Any | None = None,
    ):
        if benchmark != "scienceqa":
            raise ValueError("checkpoint evolution currently supports ScienceQA")
        if annotations is None or image_root is None:
            raise ValueError("annotations and image_root are required")
        self.benchmark = benchmark
        self.annotations = Path(annotations)
        self.image_root = Path(image_root)
        self.model_id = model_id
        self.checkpoint_path = checkpoint_path
        self.revision = revision
        self.seeds = seeds
        self.maximum_examples = maximum_examples
        self.offline = offline
        self._processor = processor
        self._model = model
        self._torch = torch_module
        self._device = None
        self._resolved_revision = revision
        self._cache: dict[tuple[str, Genome, int], dict[str, float]] = {}

    def summary(self) -> dict[str, Any]:
        payload = _read_payload(self.annotations)
        return {
            "dataset": self.benchmark,
            "validation_examples": min(
                self.maximum_examples,
                len(_scienceqa_problems(payload, "val")),
            ),
            "test_examples": min(
                self.maximum_examples,
                len(_scienceqa_problems(payload, "test")),
            ),
            "evaluation_tier": "l2_public_checkpoint",
            "selection_split": "val",
            "final_split": "test",
            "model_id": self.model_id,
            "requested_revision": self.revision,
            "checkpoint_committed": False,
        }

    def evaluate(
        self, trial_id, generation, parent_id, genome, source_papers, rationale
    ) -> EvolutionTrial:
        started = time.monotonic()
        rows = [self._metrics(genome, "val", seed) for seed in self.seeds]
        validation = mean_with_std(rows)
        validation["primary"] = (
            validation["accuracy"] + 0.001 * validation["parse_rate"]
        )
        validation["fitness"] = validation["primary"]
        validation["fitness_std"] = validation.get("accuracy_std", 0.0)
        return EvolutionTrial(
            trial_id,
            generation,
            parent_id,
            genome,
            validation,
            {
                "parameters": self._parameter_count(),
                "device": self._device.type,
                "seeds": list(self.seeds),
                "model_id": self.model_id,
                "model_revision": self._resolved_revision,
                "weights_updated": False,
                "evaluated_examples": self.maximum_examples,
            },
            source_papers,
            rationale,
            time.monotonic() - started,
        )

    def test(self, genome: Genome) -> dict[str, float]:
        rows = [self._metrics(genome, "test", seed) for seed in self.seeds]
        result = mean_with_std(rows)
        result["primary"] = result["accuracy"] + 0.001 * result["parse_rate"]
        return result

    def _ensure_loaded(self) -> None:
        if self._torch is None:
            import torch
            self._torch = torch
        if self._device is None:
            self._device = device_for(self._torch)
        if self._processor is not None and self._model is not None:
            return
        config = self._prediction_config("val", Genome())
        self._processor, self._model, self._resolved_revision = _load_checkpoint(
            config, self._torch, self._device
        )

    def _prediction_config(self, split: str, genome: Genome):
        return CheckpointPredictionConfig(
            benchmark=self.benchmark,
            annotations=self.annotations,
            image_root=self.image_root,
            output=Path("unused-checkpoint-evolution.jsonl"),
            model_id=self.model_id,
            checkpoint_path=self.checkpoint_path,
            revision=self.revision,
            split=split,
            maximum_examples=self.maximum_examples,
            max_new_tokens=genome.checkpoint_max_new_tokens,
            offline=self.offline,
            prompt_style=genome.checkpoint_prompt_style,
            use_hint=genome.checkpoint_use_hint,
            image_size=genome.checkpoint_image_size,
        )

    def _metrics(self, genome: Genome, split: str, seed: int) -> dict[str, float]:
        cache_key = (split, genome, seed)
        if cache_key in self._cache:
            return self._cache[cache_key]
        self._ensure_loaded()
        self._torch.manual_seed(seed)
        if self._device.type == "cuda":
            self._torch.cuda.manual_seed_all(seed)
            self._torch.cuda.reset_peak_memory_stats(self._device)
        config = replace(self._prediction_config(split, genome), seed=seed)
        examples = list(iter_prediction_examples(config))[: self.maximum_examples]
        started = time.monotonic()
        predictions = []
        for example in examples:
            image = _open_image(example.image, genome.checkpoint_image_size)
            raw = _generate_one(
                self._processor,
                self._model,
                self._torch,
                self._device,
                image,
                example.prompt,
                max_new_tokens=genome.checkpoint_max_new_tokens,
            )
            from .checkpoint import normalize_prediction
            predictions.append({
                "id": example.identifier,
                "prediction": normalize_prediction(
                    self.benchmark, raw, example.choices
                ),
            })
        selected = dict(
            list(_scienceqa_problems(_read_payload(self.annotations), split).items())[
                : self.maximum_examples
            ]
        )
        metrics, count = score_benchmark(
            self.benchmark,
            {"problems": selected, "splits": {split: list(selected)}},
            predictions,
            split=split,
        )
        elapsed = time.monotonic() - started
        metrics["latency_seconds_per_example"] = elapsed / max(count, 1)
        metrics["peak_gpu_memory_mb"] = (
            self._torch.cuda.max_memory_allocated(self._device) / 1024**2
            if self._device.type == "cuda" else 0.0
        )
        self._cache[cache_key] = metrics
        return metrics

    def _parameter_count(self) -> int:
        self._ensure_loaded()
        return sum(parameter.numel() for parameter in self._model.parameters())
