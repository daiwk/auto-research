"""Real-video evidence-view audit for Video-OPSD.

This is deliberately an evaluation bridge rather than a counterfeit full
8-H100 training reproduction: the same pinned VLM sees the full sampled video
and an annotation-provided privileged evidence view under equal decoding.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import statistics

from ..multimodal.video import (
    SMOLVLM2_VIDEO_ID,
    SMOLVLM2_VIDEO_REVISION,
    VIDEO_MME_V2_ID,
    VIDEO_MME_V2_REVISION,
    VideoBenchmarkConfig,
    _load_video_frames,
    run_video_benchmark,
)


@dataclass(frozen=True)
class VideoOPSDEvalConfig:
    annotations: Path
    video_root: Path
    output_dir: Path = Path("runs/video-opsd-checkpoint")
    model_id: str = SMOLVLM2_VIDEO_ID
    model_revision: str = SMOLVLM2_VIDEO_REVISION
    checkpoint_path: Path | None = None
    seeds: tuple[int, ...] = (42, 43, 44)
    maximum_examples: int = 12
    num_frames: int = 32
    max_new_tokens: int = 12
    offline: bool = False

    def validate(self) -> None:
        if len(self.seeds) != 3 or len(set(self.seeds)) != 3:
            raise ValueError("Video-OPSD evidence audit requires three distinct seeds")
        if min(self.maximum_examples, self.num_frames, self.max_new_tokens) < 1:
            raise ValueError("Video-OPSD evaluation sizes must be positive")


def run_video_opsd_evaluation(
    config: VideoOPSDEvalConfig,
    *,
    processor=None,
    model=None,
    torch_module=None,
    frame_loader=None,
) -> tuple[dict, Path]:
    config.validate()
    evidence = _evidence_map(config.annotations)
    common = dict(
        annotations=config.annotations,
        video_root=config.video_root,
        model_id=config.model_id,
        model_revision=config.model_revision,
        checkpoint_path=config.checkpoint_path,
        seeds=config.seeds,
        maximum_examples=config.maximum_examples,
        num_frames=config.num_frames,
        max_new_tokens=config.max_new_tokens,
        do_sample=False,
        offline=config.offline,
    )
    load = frame_loader or _load_video_frames
    full, _ = run_video_benchmark(
        VideoBenchmarkConfig(output_dir=config.output_dir / "full-video", **common),
        processor=processor, model=model, torch_module=torch_module, video_loader=load,
    )

    privileged, _ = run_video_benchmark(
        VideoBenchmarkConfig(
            output_dir=config.output_dir / "evidence-view",
            frame_indices_by_id=evidence,
            **common,
        ),
        processor=processor, model=model, torch_module=torch_module,
        video_loader=load,
    )
    agreement = []
    for seed in config.seeds:
        full_predictions = _predictions(config.output_dir / "full-video" / f"predictions-seed{seed}.jsonl")
        evidence_predictions = _predictions(config.output_dir / "evidence-view" / f"predictions-seed{seed}.jsonl")
        shared = sorted(set(full_predictions) & set(evidence_predictions))
        agreement.append(statistics.fmean(
            full_predictions[key] == evidence_predictions[key] for key in shared
        ))
    payload = {
        "schema_version": 1,
        "method": "video-opsd",
        "config": {
            **asdict(config),
            "annotations": str(config.annotations),
            "video_root": str(config.video_root),
            "output_dir": str(config.output_dir),
            "checkpoint_path": str(config.checkpoint_path) if config.checkpoint_path else None,
        },
        "metrics": {
            "full_video_accuracy": full["metrics"],
            "privileged_evidence_accuracy": privileged["metrics"],
            "answer_agreement": _aggregate(agreement),
        },
        "provenance": {
            "benchmark_id": VIDEO_MME_V2_ID,
            "benchmark_revision": VIDEO_MME_V2_REVISION,
            "model_id": config.model_id,
            "model_revision": config.model_revision,
        },
        "protocol": {
            "three_seed_equal_decoding": True,
            "annotation_required": "evidence_frame_indices over uniformly sampled frames",
            "claim_boundary": (
                "real public-checkpoint evidence-view audit; it does not claim the paper's "
                "6,500-example on-policy self-distillation training or 8-H100 result"
            ),
        },
    }
    config.output_dir.mkdir(parents=True, exist_ok=True)
    path = config.output_dir / "metrics.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload, path


def _evidence_map(path):
    if path.suffix == ".jsonl":
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload.get("test", payload) if isinstance(payload, dict) else payload
    result = {}
    for position, row in enumerate(rows):
        indices = row.get("evidence_frame_indices")
        if indices is None:
            raise ValueError("every Video-OPSD row requires evidence_frame_indices")
        question_id = str(row.get("question_id", row.get("id", position)))
        result[question_id] = tuple(int(index) for index in indices)
    return result


def _predictions(path):
    return {
        str(row["id"]): str(row["prediction"])
        for row in (
            json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line
        )
    }


def _aggregate(values):
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    radius = 1.96 * std / math.sqrt(len(values))
    return {"mean": mean, "std": std, "ci95_low": mean - radius, "ci95_high": mean + radius}
