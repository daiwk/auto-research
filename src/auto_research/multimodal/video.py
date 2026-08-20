"""Resumable Video-MME-v2 evaluation with a real public video checkpoint."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
from typing import Any, Callable

import numpy as np

from ..runtime import device_for, exclusive_file_lock, runtime_summary


VIDEO_MME_V2_ID = "MME-Benchmarks/Video-MME-v2"
VIDEO_MME_V2_REVISION = "6e4bebb03202e1ddbf3d37703e560e51c5aa2d64"
SMOLVLM2_VIDEO_ID = "HuggingFaceTB/SmolVLM2-256M-Video-Instruct"
SMOLVLM2_VIDEO_REVISION = "067788b187b95ebe7b2e040b3e4299e342e5b8fd"


@dataclass(frozen=True)
class VideoBenchmarkConfig:
    annotations: Path
    video_root: Path
    output_dir: Path = Path("runs/video-mme-v2")
    model_id: str = SMOLVLM2_VIDEO_ID
    model_revision: str = SMOLVLM2_VIDEO_REVISION
    checkpoint_path: Path | None = None
    seeds: tuple[int, ...] = (42, 43, 44)
    maximum_examples: int | None = None
    num_frames: int = 32
    max_new_tokens: int = 12
    do_sample: bool = False
    temperature: float = 0.2
    offline: bool = False

    def validate(self) -> None:
        if len(self.seeds) < 3:
            raise ValueError("video benchmark requires at least three seeds")
        if len(set(self.seeds)) != len(self.seeds):
            raise ValueError("video benchmark seeds must be unique")
        if self.maximum_examples is not None and self.maximum_examples < 1:
            raise ValueError("maximum_examples must be positive")
        if self.num_frames < 1 or self.max_new_tokens < 1 or self.temperature <= 0:
            raise ValueError("generation limits must be positive")


def run_video_benchmark(
    config: VideoBenchmarkConfig,
    *,
    processor: Any | None = None,
    model: Any | None = None,
    torch_module: Any | None = None,
    video_loader: Callable[[Path, int], Any] | None = None,
) -> tuple[dict[str, Any], Path]:
    """Run a three-seed Video-MME-v2-compatible MCQ evaluation."""
    config.validate()
    rows = _video_rows(config.annotations, config.video_root)
    if config.maximum_examples is not None:
        rows = rows[: config.maximum_examples]
    if not rows:
        raise ValueError("video benchmark selected no examples")
    torch = torch_module
    if torch is None:
        import torch as torch_import
        torch = torch_import
    device = device_for(torch)
    resolved = config.model_revision
    if processor is None or model is None:
        processor, model, resolved = _load_video_checkpoint(config, torch, device)
    digest = _video_digest(config, rows, resolved)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    seed_metrics = []
    video_cache: dict[Path, tuple[Any, Any]] = {}
    load_frames = video_loader or _load_video_frames
    with exclusive_file_lock(config.output_dir / "metrics.json"):
        for seed in config.seeds:
            torch.manual_seed(seed)
            if device.type == "cuda":
                torch.cuda.manual_seed_all(seed)
            output = config.output_dir / f"predictions-seed{seed}.jsonl"
            completed = _completed_video_ids(output, digest, seed)
            started = time.perf_counter()
            with output.open("a", encoding="utf-8") as handle:
                for row in rows:
                    if row["id"] in completed:
                        continue
                    raw = _generate_video_answer(
                        processor, model, torch, device, row, config, seed,
                        video_cache, load_frames,
                    )
                    prediction = _answer_letter(raw)
                    handle.write(json.dumps({
                        "id": row["id"],
                        "video_id": row["video_id"],
                        "prediction": prediction,
                        "raw_prediction": raw,
                        "answer": row["answer"],
                        "seed": seed,
                        "model_id": config.model_id,
                        "model_revision": resolved,
                        "config_digest": digest,
                    }, ensure_ascii=False) + "\n")
                    handle.flush()
            predictions = {
                item["id"]: item for item in _jsonl(output)
                if item.get("config_digest") == digest and item.get("seed") == seed
            }
            correct = sum(
                predictions[row["id"]]["prediction"] == row["answer"]
                for row in rows
            )
            parsed = sum(
                predictions[row["id"]]["prediction"] != "__invalid__"
                for row in rows
            )
            seed_metrics.append({
                "seed": seed,
                "accuracy": correct / len(rows),
                "parse_rate": parsed / len(rows),
                "examples": len(rows),
                "wall_seconds": time.perf_counter() - started,
            })
        accuracy = np.asarray([row["accuracy"] for row in seed_metrics])
        payload = {
            "schema_version": 2,
            "kind": "video_checkpoint_benchmark",
            "benchmark": "Video-MME-v2",
            "benchmark_id": VIDEO_MME_V2_ID,
            "benchmark_revision": VIDEO_MME_V2_REVISION,
            "model_id": config.model_id,
            "requested_model_revision": config.model_revision,
            "resolved_model_revision": resolved,
            "config_digest": digest,
            "metrics": {
                "accuracy_mean": float(accuracy.mean()),
                "accuracy_std": float(accuracy.std()),
                "accuracy_ci95_radius": float(
                    1.96 * accuracy.std(ddof=1) / np.sqrt(len(accuracy))
                ),
                "parse_rate_mean": float(np.mean([
                    row["parse_rate"] for row in seed_metrics
                ])),
                "seed_runs": seed_metrics,
            },
            "protocol": {
                "seeds": list(config.seeds),
                "num_frames": config.num_frames,
                "deterministic_decoding": not config.do_sample,
                "resume": "per-example JSONL with config digest",
                "video_cache": "decode and uniformly sample each MP4 once per run",
                "frame_metadata": "preserve source fps and uniform-sample timestamps",
                "claim_boundary": (
                    "subset score when maximum_examples is set; not an official full "
                    "Video-MME-v2 leaderboard result"
                ),
            },
            "provenance": {
                "annotations_sha256": _sha256(config.annotations),
                "checkpoint_path": (
                    "local snapshot (not committed)" if config.checkpoint_path else None
                ),
            },
            "runtime": runtime_summary(torch),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _write_json(config.output_dir / "metrics.json", payload)
        (config.output_dir / "report.md").write_text(
            _video_report(payload), encoding="utf-8"
        )
    return payload, config.output_dir


def _video_rows(path: Path, video_root: Path) -> list[dict[str, Any]]:
    if path.suffix == ".jsonl":
        source = _jsonl(path)
    elif path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        source = payload.get("test", payload) if isinstance(payload, dict) else payload
    elif path.suffix == ".parquet":
        try:
            from datasets import Dataset
        except ImportError as exc:
            raise RuntimeError("parquet Video-MME-v2 requires the multimodal extra") from exc
        source = list(Dataset.from_parquet(str(path)))
    else:
        raise ValueError("video annotations must be JSON, JSONL or Parquet")
    rows = []
    for position, item in enumerate(source):
        video_id = str(item.get("video_id", item.get("video", position)))
        filename = str(item.get("video", f"{video_id}.mp4"))
        video = video_root / filename
        if not video.exists():
            candidate = video_root / f"{video_id}.mp4"
            if candidate.exists():
                video = candidate
            else:
                raise FileNotFoundError(f"Video-MME-v2 video not found: {video}")
        options = item.get("options", item.get("choices", ""))
        if isinstance(options, list):
            options = " ".join(
                value if re.match(r"^[A-H][.)]", str(value))
                else f"{chr(65 + index)}. {value}"
                for index, value in enumerate(options)
            )
        rows.append({
            "id": str(item.get("question_id", item.get("id", position))),
            "video_id": video_id,
            "video": video,
            "question": str(item["question"]),
            "options": str(options),
            "answer": str(item["answer"]).strip().upper()[:1],
        })
    return rows


def _load_video_checkpoint(config, torch, device):
    from huggingface_hub import model_info
    from transformers import AutoModelForImageTextToText, AutoProcessor
    resolved = config.model_revision
    if not config.offline:
        resolved = model_info(config.model_id, revision=config.model_revision).sha
    source = str(config.checkpoint_path or config.model_id)
    kwargs = {"local_files_only": config.offline, "revision": resolved}
    processor = AutoProcessor.from_pretrained(source, **kwargs)
    dtype = torch.float32
    if device.type == "cuda":
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    elif device.type == "mps":
        dtype = torch.float16
    model = AutoModelForImageTextToText.from_pretrained(
        source, dtype=dtype, **kwargs
    ).to(device).eval()
    return processor, model, getattr(model.config, "_commit_hash", None) or resolved


def _generate_video_answer(
    processor, model, torch, device, row, config, seed, video_cache, load_frames,
):
    prompt = (
        f"{row['question']}\n{row['options']}\n"
        "Answer with only the option letter."
    )
    cached = video_cache.get(row["video"])
    if cached is None:
        cached = load_frames(row["video"], config.num_frames)
        video_cache[row["video"]] = cached
    frames, metadata = cached
    messages = [{"role": "user", "content": [
        {"type": "video", "video": frames},
        {"type": "text", "text": prompt},
    ]}]
    inputs = processor.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True,
        return_dict=True, return_tensors="pt",
        processor_kwargs={
            "do_sample_frames": False,
            "video_metadata": [metadata],
        },
    )
    inputs = {
        key: value.to(device) if hasattr(value, "to") else value
        for key, value in dict(inputs).items()
    }
    prompt_tokens = inputs["input_ids"].shape[-1]
    kwargs = {
        "max_new_tokens": config.max_new_tokens,
        "do_sample": config.do_sample,
    }
    if config.do_sample:
        kwargs.update({"temperature": config.temperature, "generator": _generator(torch, device, seed)})
    with torch.inference_mode():
        generated = model.generate(**inputs, **kwargs)
    return processor.decode(
        generated[0, prompt_tokens:], skip_special_tokens=True
    ).strip()


def _load_video_frames(path: Path, num_frames: int):
    from transformers.video_utils import load_video
    return load_video(
        str(path), num_frames=num_frames, backend="torchvision"
    )


def _generator(torch, device, seed):
    generator = torch.Generator(device=device.type if device.type != "mps" else "cpu")
    generator.manual_seed(seed)
    return generator


def _answer_letter(text: str) -> str:
    match = re.search(r"(?:answer|option|choice)?\s*(?:is|:)?\s*\(?([A-H])\)?", text, re.I)
    return match.group(1).upper() if match else "__invalid__"


def _completed_video_ids(path: Path, digest: str, seed: int) -> set[str]:
    completed = set()
    for row in _jsonl(path) if path.exists() else []:
        if row.get("config_digest") != digest or row.get("seed") != seed:
            raise ValueError("existing video predictions do not match this config")
        completed.add(str(row["id"]))
    return completed


def _video_digest(config, rows, resolved):
    payload = {
        **asdict(config),
        "annotations": str(config.annotations.resolve()),
        "video_root": str(config.video_root.resolve()),
        "output_dir": None,
        "checkpoint_path": str(config.checkpoint_path) if config.checkpoint_path else None,
        "resolved_revision": resolved,
        "frame_sampling": "uniform_with_source_metadata_v1",
        "ids": [row["id"] for row in rows],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _video_report(payload: dict[str, Any]) -> str:
    metrics = payload["metrics"]
    return f"""# Video-MME-v2 真实 checkpoint 评测

- checkpoint：`{payload['model_id']}` @ `{payload['resolved_model_revision']}`
- benchmark：`{payload['benchmark_id']}` @ `{payload['benchmark_revision']}`
- accuracy：`{metrics['accuracy_mean']:.4f} ± {metrics['accuracy_std']:.4f}`
- 95% CI 半径：`{metrics['accuracy_ci95_radius']:.4f}`
- parse rate：`{metrics['parse_rate_mean']:.4f}`

每个 seed 使用独立、逐样本可恢复的 JSONL。设置 `maximum_examples` 时结果只是公开
benchmark 子集 smoke，不得写成官方 Video-MME-v2 leaderboard 分数。
"""
