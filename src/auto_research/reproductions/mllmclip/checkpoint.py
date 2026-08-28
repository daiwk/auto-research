"""Real-checkpoint CUDA path for MLLMCLIP feature-level distillation."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import statistics
import time
from typing import Any

from ...runtime import device_for


@dataclass(frozen=True)
class CheckpointConfig:
    output: Path
    data_dir: Path = Path("data")
    annotations: Path | None = None
    image_root: Path | None = None
    teacher_id: str = "HuggingFaceTB/SmolVLM2-256M-Video-Instruct"
    teacher_revision: str = "main"
    teacher_path: Path | None = None
    student_id: str = "openai/clip-vit-base-patch32"
    student_revision: str = "main"
    student_path: Path | None = None
    train_examples: int = 128
    test_examples: int = 64
    batch_size: int = 8
    steps: int = 40
    learning_rate: float = 3e-3
    seeds: tuple[int, ...] = (42, 43, 44)
    seed: int | None = None


def _normalize(values, torch):
    return values / values.norm(dim=-1, keepdim=True).clamp_min(1e-8)


def linear_cka(left, right, torch) -> float:
    left = left.float() - left.float().mean(0)
    right = right.float() - right.float().mean(0)
    cross = (left.T @ right).square().sum()
    denominator = (left.T @ left).square().sum().sqrt() * (
        right.T @ right
    ).square().sum().sqrt()
    return float((cross / denominator.clamp_min(1e-9)).detach().cpu())


def _knn_accuracy(train, train_labels, test, test_labels, torch) -> float:
    scores = _normalize(test, torch) @ _normalize(train, torch).T
    predictions = train_labels[scores.argmax(-1)]
    return float((predictions == test_labels).float().mean().cpu())


def _neighbor_overlap(left, right, torch, k: int = 5) -> float:
    count = len(left)
    if count < 2:
        return 0.0
    k = min(k, count - 1)
    left_scores = _normalize(left, torch) @ _normalize(left, torch).T
    right_scores = _normalize(right, torch) @ _normalize(right, torch).T
    left_scores.fill_diagonal_(-float("inf"))
    right_scores.fill_diagonal_(-float("inf"))
    left_neighbors = left_scores.topk(k, dim=-1).indices
    right_neighbors = right_scores.topk(k, dim=-1).indices
    overlap = (
        left_neighbors.unsqueeze(-1) == right_neighbors.unsqueeze(-2)
    ).any(-1).float().mean()
    return float(overlap.cpu())


def fit_projection(train_student, train_teacher, test_student, test_teacher,
                   train_labels, test_labels, config: CheckpointConfig, torch, device):
    projection = torch.nn.Linear(
        train_student.shape[-1], train_teacher.shape[-1], bias=False,
    ).to(device)
    train_student = train_student.to(device)
    train_teacher = train_teacher.to(device)
    split = max(2, int(0.8 * len(train_student)))
    generator = torch.Generator(device="cpu").manual_seed(
        config.seed if config.seed is not None else config.seeds[0]
    )
    order = torch.randperm(len(train_student), generator=generator)
    fit_indices, validation_indices = order[:split], order[split:]
    fit_x = train_student[fit_indices].float()
    validation_x = train_student[validation_indices].float()
    fit_y = train_teacher[fit_indices].float()
    validation_y = train_teacher[validation_indices].float()
    # Choose ridge initialization on an internal validation slice.  The held-out
    # test tensors below are never consulted by model selection.
    identity = torch.eye(fit_x.shape[1], device=device)
    ridge_trials = []
    for ridge in (0.1, 1.0, 10.0, 100.0):
        solution = torch.linalg.solve(
            fit_x.T @ fit_x + ridge * identity, fit_x.T @ fit_y,
        )
        score = linear_cka(validation_x @ solution, validation_y, torch)
        ridge_trials.append((score, ridge, solution))
    selected_validation_cka, selected_ridge, solution = max(
        ridge_trials, key=lambda row: row[0]
    )
    with torch.no_grad():
        projection.weight.copy_(solution.T)
    optimizer = torch.optim.AdamW(
        projection.parameters(), lr=config.learning_rate, weight_decay=1e-2,
    )
    baseline_train = projection(train_student).detach()
    baseline_test = projection(test_student.to(device)).detach()
    initial_loss = None
    losses = []
    best_validation_cka = selected_validation_cka
    best_weight = projection.weight.detach().clone()
    projection.train()
    for _ in range(config.steps):
        predicted = projection(fit_x)
        target = fit_y
        cosine = 1 - torch.nn.functional.cosine_similarity(predicted, target).mean()
        cka_loss = 1 - _differentiable_cka(predicted, target, torch)
        loss = cosine + 2.0 * cka_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        if initial_loss is None:
            initial_loss = losses[-1]
        with torch.inference_mode():
            validation_cka = linear_cka(
                projection(validation_x), validation_y, torch,
            )
        if validation_cka > best_validation_cka:
            best_validation_cka = validation_cka
            best_weight = projection.weight.detach().clone()
    with torch.no_grad():
        projection.weight.copy_(best_weight)
    projection.eval()
    with torch.inference_mode():
        method_train = projection(train_student)
        method_test = projection(test_student.to(device))
    label_classes = int(torch.unique(train_labels).numel())
    baseline_knn = (
        _knn_accuracy(
            baseline_train, train_labels.to(device), baseline_test,
            test_labels.to(device), torch,
        ) if label_classes > 1 else None
    )
    method_knn = (
        _knn_accuracy(
            method_train, train_labels.to(device), method_test,
            test_labels.to(device), torch,
        ) if label_classes > 1 else None
    )
    return {
        "initial_loss": initial_loss,
        "final_loss": losses[-1],
        "baseline": {
            "linear_cka": linear_cka(baseline_test, test_teacher.to(device), torch),
            "knn_accuracy": baseline_knn,
            "neighbor_overlap_at_5": _neighbor_overlap(
                baseline_test, test_teacher.to(device), torch,
            ),
        },
        "method": {
            "linear_cka": linear_cka(method_test, test_teacher.to(device), torch),
            "knn_accuracy": method_knn,
            "neighbor_overlap_at_5": _neighbor_overlap(
                method_test, test_teacher.to(device), torch,
            ),
        },
        "parameters": sum(parameter.numel() for parameter in projection.parameters()),
        "model_selection": {
            "selected_ridge": selected_ridge,
            "best_validation_cka": best_validation_cka,
            "test_used_for_selection": False,
            "label_classes": label_classes,
            "label_diagnostic_valid": label_classes > 1,
        },
    }


def _differentiable_cka(left, right, torch):
    left = left.float() - left.float().mean(0)
    right = right.float() - right.float().mean(0)
    cross = (left.T @ right).square().sum()
    denominator = (left.T @ left).square().sum().sqrt() * (
        right.T @ right
    ).square().sum().sqrt()
    return cross / denominator.clamp_min(1e-9)


def _features(images, processor, model, *, teacher: bool, torch, device, batch_size):
    vectors = []
    for start in range(0, len(images), batch_size):
        batch = images[start:start + batch_size]
        inputs = processor(images=batch, return_tensors="pt")
        with torch.inference_mode():
            if teacher:
                kwargs = {"pixel_values": inputs["pixel_values"].to(device)}
                if "pixel_attention_mask" in inputs:
                    kwargs["pixel_attention_mask"] = inputs["pixel_attention_mask"].to(device)
                output = model.model.get_image_features(**kwargs)
                value = getattr(output, "pooler_output", output)
                if value.ndim > 2:
                    value = value.reshape(len(batch), -1, value.shape[-1]).mean(1)
            else:
                value = model.get_image_features(
                    pixel_values=inputs["pixel_values"].to(device)
                )
                # Transformers 5 may return a structured pooling output while
                # earlier releases returned the tensor directly.
                value = getattr(value, "pooler_output", value)
            vectors.append(value.float().cpu())
    return torch.cat(vectors)


def _load_public_images(config: CheckpointConfig, torch):
    if config.annotations and config.image_root:
        from PIL import Image

        grouped: dict[str, list[str]] = {}
        with config.annotations.open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                grouped.setdefault(row["image"], []).append(row["label"])
        rows = sorted(grouped.items())
        needed = config.train_examples + config.test_examples
        if len(rows) < needed:
            raise ValueError(f"POPE annotations provide {len(rows)} images, need {needed}")
        images, labels = [], []
        for name, answers in rows[:needed]:
            with Image.open(config.image_root / name) as source:
                images.append(source.convert("RGB"))
            # Public POPE groups three object-presence probes per image.  The
            # count of positive probes is a compact semantic-strata label for
            # the held-out kNN diagnostic; it is never exposed to distillation.
            labels.append(sum(answer == "yes" for answer in answers))
        return (
            images[:config.train_examples], images[config.train_examples:],
            torch.tensor(labels[:config.train_examples]),
            torch.tensor(labels[config.train_examples:]),
            "POPE adversarial / COCO val2014",
        )

    from torchvision.datasets import CIFAR10

    training = CIFAR10(config.data_dir, train=True, download=True)
    testing = CIFAR10(config.data_dir, train=False, download=True)
    train_images = [training[index][0] for index in range(config.train_examples)]
    test_images = [testing[index][0] for index in range(config.test_examples)]
    train_labels = torch.tensor([training[index][1] for index in range(config.train_examples)])
    test_labels = torch.tensor([testing[index][1] for index in range(config.test_examples)])
    return train_images, test_images, train_labels, test_labels, "CIFAR-10"


def run_checkpoint_distillation(config: CheckpointConfig) -> dict[str, Any]:
    import torch
    from huggingface_hub import model_info
    from transformers import AutoModel, AutoModelForImageTextToText, AutoProcessor

    device = device_for(torch, "cuda")
    seeds = (config.seed,) if config.seed is not None else config.seeds
    if len(seeds) < 3 and config.seed is None:
        raise ValueError("formal checkpoint distillation requires at least three seeds")
    teacher_revision = (
        config.teacher_revision if config.teacher_path else
        model_info(config.teacher_id, revision=config.teacher_revision).sha
    )
    student_revision = (
        config.student_revision if config.student_path else
        model_info(config.student_id, revision=config.student_revision).sha
    )
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    teacher_processor = AutoProcessor.from_pretrained(
        str(config.teacher_path or config.teacher_id), revision=teacher_revision,
        local_files_only=config.teacher_path is not None,
    )
    teacher = AutoModelForImageTextToText.from_pretrained(
        str(config.teacher_path or config.teacher_id), revision=teacher_revision, dtype=dtype,
        local_files_only=config.teacher_path is not None,
    ).to(device).eval()
    student_processor = AutoProcessor.from_pretrained(
        str(config.student_path or config.student_id), revision=student_revision,
        local_files_only=config.student_path is not None,
    )
    student = AutoModel.from_pretrained(
        str(config.student_path or config.student_id), revision=student_revision, dtype=dtype,
        local_files_only=config.student_path is not None,
    ).to(device).eval()
    for model in (teacher, student):
        for parameter in model.parameters():
            parameter.requires_grad_(False)

    train_images, test_images, train_labels, test_labels, dataset_name = (
        _load_public_images(config, torch)
    )
    torch.cuda.reset_peak_memory_stats(device)
    started = time.perf_counter()
    train_teacher = _features(
        train_images, teacher_processor, teacher, teacher=True, torch=torch,
        device=device, batch_size=config.batch_size,
    )
    test_teacher = _features(
        test_images, teacher_processor, teacher, teacher=True, torch=torch,
        device=device, batch_size=config.batch_size,
    )
    train_student = _features(
        train_images, student_processor, student, teacher=False, torch=torch,
        device=device, batch_size=config.batch_size,
    )
    test_student = _features(
        test_images, student_processor, student, teacher=False, torch=torch,
        device=device, batch_size=config.batch_size,
    )
    seed_results = []
    for seed in seeds:
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        seed_config = CheckpointConfig(**{**asdict(config), "seed": seed})
        fit = fit_projection(
            train_student, train_teacher, test_student, test_teacher,
            train_labels, test_labels, seed_config, torch, device,
        )
        seed_results.append({"seed": seed, **fit})
    first = seed_results[0]
    aggregate = {
        "baseline_linear_cka": _aggregate([
            row["baseline"]["linear_cka"] for row in seed_results
        ]),
        "method_linear_cka": _aggregate([
            row["method"]["linear_cka"] for row in seed_results
        ]),
        "baseline_neighbor_overlap_at_5": _aggregate([
            row["baseline"]["neighbor_overlap_at_5"] for row in seed_results
        ]),
        "method_neighbor_overlap_at_5": _aggregate([
            row["method"]["neighbor_overlap_at_5"] for row in seed_results
        ]),
    }
    payload = {
        "schema_version": 3,
        "method": "mllmclip-real-checkpoint-cka",
        "dataset": {
            "name": dataset_name, "train_examples": config.train_examples,
            "test_examples": config.test_examples,
        },
        "checkpoints": {
            "teacher": {"model_id": config.teacher_id, "revision": teacher_revision},
            "student": {"model_id": config.student_id, "revision": student_revision},
        },
        "setup": {
            **asdict(config), "output": str(config.output), "data_dir": str(config.data_dir),
            "teacher_path": "local snapshot (not committed)" if config.teacher_path else None,
            "student_path": "local snapshot (not committed)" if config.student_path else None,
            "annotations": config.annotations.name if config.annotations else None,
            "image_root": "configured public image root" if config.image_root else None,
        },
        "metrics": {
            "baseline": first["baseline"],
            "method": first["method"],
            "seed_results": seed_results,
            "aggregate": aggregate,
        },
        "evaluation_protocol": {
            "feature_extraction_reused_across_seeds": True,
            "independent_projection_initialization_and_train_validation_split": True,
            "test_used_for_selection": False,
            "seeds": list(seeds),
        },
        "runtime": {
            "accelerator": torch.cuda.get_device_name(device),
            "duration_seconds": time.perf_counter() - started,
            "peak_gpu_memory_mb": torch.cuda.max_memory_allocated(device) / 1024**2,
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": (
            "Real SmolVLM teacher and CLIP student checkpoints; frozen encoders, "
            f"trained CKA projection; {dataset_name} public subset."
        ),
    }
    config.output.parent.mkdir(parents=True, exist_ok=True)
    config.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return payload


def _aggregate(values: list[float]) -> dict[str, float]:
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    radius = 1.96 * std / math.sqrt(len(values))
    return {"mean": mean, "std": std, "ci95_low": mean - radius, "ci95_high": mean + radius}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--image-root", type=Path)
    parser.add_argument("--teacher-id", default=CheckpointConfig.teacher_id)
    parser.add_argument("--teacher-revision", default="main")
    parser.add_argument("--teacher-path", type=Path)
    parser.add_argument("--student-id", default=CheckpointConfig.student_id)
    parser.add_argument("--student-revision", default="main")
    parser.add_argument("--student-path", type=Path)
    parser.add_argument("--train-examples", type=int, default=128)
    parser.add_argument("--test-examples", type=int, default=64)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--learning-rate", type=float, default=3e-3)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--seed", type=int, help="legacy one-seed diagnostic mode")
    args = parser.parse_args()
    values = vars(args)
    values["seeds"] = tuple(int(value) for value in values["seeds"].split(",") if value)
    payload = run_checkpoint_distillation(CheckpointConfig(**values))
    print(json.dumps(payload["metrics"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
