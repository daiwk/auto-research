from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
from typing import Any

from ..industrial_ranking import evaluate_model
from ..rec_utils import load_movielens_sequences
from .model import (
    RecDistillConfig,
    build_student,
    build_teacher,
    cache_teacher_logits,
    materialize_examples,
    train_distilled_student,
    train_raw_student_phased,
    train_teacher,
)
from ..industrial_ranking import require_backend


def reproduce_rec_distill(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    config = RecDistillConfig(
        teacher_steps=int(os.environ.get("AUTO_RESEARCH_REC_DISTILL_TEACHER_STEPS", "240")),
        student_batch_steps=int(os.environ.get("AUTO_RESEARCH_REC_DISTILL_BATCH_STEPS", "160")),
        student_stream_steps=int(os.environ.get("AUTO_RESEARCH_REC_DISTILL_STREAM_STEPS", "80")),
    )
    rows, candidates = materialize_examples(data, config, seed)
    torch, _ = require_backend()
    torch.manual_seed(seed)
    teacher, teacher_training = train_teacher(
        build_teacher(data, config), rows, candidates, config, seed
    )
    signals = cache_teacher_logits(teacher, rows, candidates, config)
    torch.manual_seed(seed + 1)
    raw_student, raw_training = train_raw_student_phased(
        build_student(data, config), rows, candidates, config, seed + 1
    )
    distillation_runs = {}
    candidates_by_validation = []
    for weight in (0.1, 0.3, 1.0, 3.0):
        variant_config = replace(config, distillation_weight=weight)
        torch.manual_seed(seed + 1)
        model, metrics = train_distilled_student(
            build_student(data, variant_config), rows, candidates, signals,
            variant_config, seed + 1,
        )
        validation = evaluate_model(
            model, data, variant_config, output=lambda value: value[0],
            target="validation",
        )
        distillation_runs[str(weight)] = {
            "training": metrics, "validation": validation
        }
        candidates_by_validation.append((validation["ndcg_at_10"], weight, model))
    _, selected_weight, distilled = max(candidates_by_validation, key=lambda row: row[0])
    distilled_training = distillation_runs[str(selected_weight)]["training"]
    results = {
        "large_teacher": evaluate_model(teacher, data, config),
        "raw_student": evaluate_model(raw_student, data, config, output=lambda value: value[0]),
        "rec_distill_student": evaluate_model(distilled, data, config, output=lambda value: value[0]),
    }
    teacher_ndcg = results["large_teacher"]["ndcg_at_10"]
    raw_ndcg = results["raw_student"]["ndcg_at_10"]
    distilled_ndcg = results["rec_distill_student"]["ndcg_at_10"]
    return {
        "paper": {"arxiv_id": "2605.29755", "title": "Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models", "url": "https://arxiv.org/abs/2605.29755", "track": "recommendation"},
        "dataset": "MovieLens 100K (local batch/stream phase simulation)",
        "setup": {"users": len(data.train), "items": data.item_count, "materialized_examples": len(rows), "teacher_dimensions": config.teacher_dimensions, "student_dimensions": config.student_dimensions, "batch_steps": config.student_batch_steps, "stream_steps": config.student_stream_steps, "selected_distillation_weight": selected_weight, "seed": seed},
        "training": {"teacher": teacher_training, "raw_student": raw_training, "distilled_student": distilled_training, "distillation_search": distillation_runs, "cached_teacher_signal_mb": signals.nbytes / 1_000_000},
        "results": results,
        "transferability": (
            None if teacher_ndcg <= raw_ndcg else
            (distilled_ndcg - raw_ndcg) / (teacher_ndcg - raw_ndcg)
        ),
        "paper_online_ab": {"ads_advv_percent": 1.00, "recommendation_finish_per_user_percent": 1.2725, "live_gift_revenue_percent": 0.78},
        "scope": "Trains a larger teacher, materializes black-box logits, applies student-side sampling correction, isolates main and auxiliary towers over a shared backbone, and runs batch then streaming distillation. MovieLens chronology simulates rather than reproduces production minute-level streams.",
    }
