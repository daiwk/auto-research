"""Pinned CLAP zero-shot evaluation on the public ESC-50 benchmark."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import time
from typing import Any, Callable

import numpy as np

from ..runtime import device_for, exclusive_file_lock, runtime_summary


CLAP_ID = "laion/clap-htsat-unfused"
CLAP_REVISION = "8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a"
ESC50_ID = "karolpiczak/ESC-50"


@dataclass(frozen=True)
class AudioBenchmarkConfig:
    annotations: Path
    audio_root: Path
    output_dir: Path = Path("runs/esc50-clap")
    model_id: str = CLAP_ID
    model_revision: str = CLAP_REVISION
    checkpoint_path: Path | None = None
    maximum_examples: int | None = None
    fold: int | None = None
    prompt_template: str = "This is a sound of {label}."
    offline: bool = False

    def validate(self) -> None:
        if self.maximum_examples is not None and self.maximum_examples < 1:
            raise ValueError("maximum_examples must be positive")
        if self.fold is not None and self.fold not in range(1, 6):
            raise ValueError("ESC-50 fold must be between 1 and 5")
        if "{label}" not in self.prompt_template:
            raise ValueError("audio prompt template must contain {label}")


AudioLoader = Callable[[Path], tuple[np.ndarray, int]]


def run_audio_benchmark(
    config: AudioBenchmarkConfig,
    *,
    processor: Any | None = None,
    model: Any | None = None,
    torch_module: Any | None = None,
    audio_loader: AudioLoader | None = None,
) -> tuple[dict[str, Any], Path]:
    config.validate()
    rows = _esc50_rows(config)
    if config.maximum_examples is not None:
        rows = rows[: config.maximum_examples]
    if not rows:
        raise ValueError("ESC-50 selected no examples")
    labels = tuple(sorted({row["label"] for row in _esc50_rows(config, ignore_fold=True)}))
    torch = torch_module
    if torch is None:
        import torch as torch_import
        torch = torch_import
    device = device_for(torch)
    resolved = config.model_revision
    if processor is None or model is None:
        processor, model, resolved = _load_clap(config, torch, device)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    digest = _audio_digest(config, rows, labels, resolved)
    output = config.output_dir / "predictions.jsonl"
    with exclusive_file_lock(config.output_dir / "metrics.json"):
        text_features, cache_hit = _cached_text_features(
            config, processor, model, torch, device, labels, resolved
        )
        completed = _completed_audio_ids(output, digest)
        load_audio = audio_loader or _load_audio
        started = time.perf_counter()
        with output.open("a", encoding="utf-8") as handle:
            for row in rows:
                if row["id"] in completed:
                    continue
                waveform, sampling_rate = load_audio(row["audio"])
                target_rate = int(processor.feature_extractor.sampling_rate)
                waveform = _resample(waveform, sampling_rate, target_rate)
                inputs = processor(
                    audio=waveform, sampling_rate=target_rate, return_tensors="pt"
                )
                inputs = {
                    key: value.to(device) if hasattr(value, "to") else value
                    for key, value in dict(inputs).items()
                }
                with torch.inference_mode():
                    audio_features = model.get_audio_features(**inputs)
                audio_features = _normalized(audio_features, torch)
                scores = (audio_features @ text_features.T)[0]
                order = scores.argsort(descending=True).detach().cpu().tolist()
                handle.write(json.dumps({
                    "id": row["id"],
                    "label": row["label"],
                    "prediction": labels[order[0]],
                    "top5": [labels[index] for index in order[:5]],
                    "model_id": config.model_id,
                    "model_revision": resolved,
                    "config_digest": digest,
                }, ensure_ascii=False) + "\n")
                handle.flush()
        predictions = {
            row["id"]: row for row in _jsonl(output)
            if row.get("config_digest") == digest
        }
        top1 = sum(
            predictions[row["id"]]["prediction"] == row["label"] for row in rows
        ) / len(rows)
        top5 = sum(
            row["label"] in predictions[row["id"]]["top5"] for row in rows
        ) / len(rows)
        payload = {
            "schema_version": 2,
            "kind": "audio_text_checkpoint_benchmark",
            "benchmark": "ESC-50",
            "benchmark_id": ESC50_ID,
            "model_id": config.model_id,
            "requested_model_revision": config.model_revision,
            "resolved_model_revision": resolved,
            "config_digest": digest,
            "metrics": {
                "zero_shot_top1_accuracy": top1,
                "zero_shot_top5_accuracy": top5,
                "examples": len(rows),
                "classes": len(labels),
                "fold": config.fold,
            },
            "cache": {
                "text_embedding_cache_hit": cache_hit,
                "cache_fingerprint": _text_cache_digest(config, labels, resolved),
                "validation": "reject mismatched checkpoint revision, labels or prompt",
            },
            "protocol": {
                "deterministic": True,
                "resume": "per-example JSONL with config digest",
                "claim_boundary": (
                    "zero-shot CLAP evaluation; a limited fold/subset is not the full "
                    "five-fold supervised ESC-50 protocol"
                ),
            },
            "provenance": {
                "annotations_sha256": _sha256(config.annotations),
                "dataset_license": "CC BY-NC; ESC-10 subset CC BY",
                "checkpoint_path": (
                    "local snapshot (not committed)" if config.checkpoint_path else None
                ),
            },
            "runtime": runtime_summary(torch),
            "wall_seconds": time.perf_counter() - started,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _write_json(config.output_dir / "metrics.json", payload)
        (config.output_dir / "report.md").write_text(
            _audio_report(payload), encoding="utf-8"
        )
    return payload, config.output_dir


def _esc50_rows(config: AudioBenchmarkConfig, ignore_fold: bool = False):
    with config.annotations.open(newline="", encoding="utf-8") as handle:
        source = list(csv.DictReader(handle))
    rows = []
    for position, item in enumerate(source):
        fold = int(item.get("fold", 0) or 0)
        if not ignore_fold and config.fold is not None and fold != config.fold:
            continue
        filename = item.get("filename", item.get("file", ""))
        if not filename:
            raise ValueError(f"ESC-50 row {position} has no filename")
        audio = config.audio_root / filename
        if not audio.exists():
            raise FileNotFoundError(f"ESC-50 audio not found: {audio}")
        rows.append({
            "id": filename,
            "audio": audio,
            "label": str(item.get("category", item.get("label", ""))).replace("_", " "),
            "fold": fold,
        })
    return rows


def _load_clap(config, torch, device):
    from huggingface_hub import model_info
    from transformers import ClapModel, ClapProcessor
    resolved = config.model_revision
    if not config.offline:
        resolved = model_info(config.model_id, revision=config.model_revision).sha
    source = str(config.checkpoint_path or config.model_id)
    kwargs = {"revision": resolved, "local_files_only": config.offline}
    processor = ClapProcessor.from_pretrained(source, **kwargs)
    model = ClapModel.from_pretrained(source, **kwargs).to(device).eval()
    return processor, model, getattr(model.config, "_commit_hash", None) or resolved


def _cached_text_features(config, processor, model, torch, device, labels, resolved):
    cache = config.output_dir / "text-embeddings.npz"
    metadata = config.output_dir / "text-embeddings.metadata.json"
    fingerprint = _text_cache_digest(config, labels, resolved)
    if cache.exists() or metadata.exists():
        if not cache.exists() or not metadata.exists():
            raise ValueError("incomplete CLAP text embedding cache")
        stored = json.loads(metadata.read_text(encoding="utf-8"))
        if stored.get("fingerprint") != fingerprint:
            raise ValueError("CLAP text embedding cache fingerprint mismatch")
        values = np.load(cache)["features"]
        return torch.tensor(values, dtype=torch.float32, device=device), True
    prompts = [config.prompt_template.format(label=label) for label in labels]
    inputs = processor(text=prompts, padding=True, return_tensors="pt")
    inputs = {
        key: value.to(device) if hasattr(value, "to") else value
        for key, value in dict(inputs).items()
    }
    with torch.inference_mode():
        features = _normalized(model.get_text_features(**inputs), torch)
    np.savez_compressed(cache, features=features.detach().float().cpu().numpy())
    _write_json(metadata, {"fingerprint": fingerprint, "labels": list(labels)})
    return features, False


def _normalized(values, torch):
    if not hasattr(values, "shape"):
        values = getattr(values, "pooler_output", None)
    if values is None or not hasattr(values, "shape"):
        raise TypeError("CLAP feature API returned no tensor or pooler_output")
    return values / torch.linalg.vector_norm(values, dim=-1, keepdim=True).clamp_min(1e-12)


def _load_audio(path: Path) -> tuple[np.ndarray, int]:
    try:
        import soundfile
    except ImportError as exc:
        raise RuntimeError("audio benchmark requires the multimodal extra") from exc
    audio, rate = soundfile.read(path, dtype="float32", always_2d=False)
    if audio.ndim == 2:
        audio = audio.mean(axis=1)
    return np.asarray(audio, dtype=np.float32), int(rate)


def _resample(audio: np.ndarray, source_rate: int, target_rate: int) -> np.ndarray:
    if source_rate == target_rate:
        return audio
    if source_rate < 1 or target_rate < 1 or not len(audio):
        raise ValueError("invalid audio sampling rate or empty waveform")
    length = max(1, round(len(audio) * target_rate / source_rate))
    source = np.linspace(0.0, 1.0, len(audio), endpoint=False)
    target = np.linspace(0.0, 1.0, length, endpoint=False)
    return np.interp(target, source, audio).astype(np.float32)


def _completed_audio_ids(path: Path, digest: str):
    completed = set()
    for row in _jsonl(path) if path.exists() else []:
        if row.get("config_digest") != digest:
            raise ValueError("existing audio predictions do not match this config")
        completed.add(row["id"])
    return completed


def _text_cache_digest(config, labels, resolved):
    return hashlib.sha256(json.dumps({
        "model_id": config.model_id,
        "resolved_revision": resolved,
        "prompt_template": config.prompt_template,
        "labels": list(labels),
    }, sort_keys=True).encode()).hexdigest()


def _audio_digest(config, rows, labels, resolved):
    payload = {
        **asdict(config),
        "annotations": str(config.annotations.resolve()),
        "audio_root": str(config.audio_root.resolve()),
        "output_dir": None,
        "checkpoint_path": str(config.checkpoint_path) if config.checkpoint_path else None,
        "resolved_revision": resolved,
        "ids": [row["id"] for row in rows],
        "labels": list(labels),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def _sha256(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _jsonl(path: Path):
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_json(path: Path, payload):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _audio_report(payload):
    metrics = payload["metrics"]
    return f"""# ESC-50 × CLAP 真实音频 checkpoint 评测

- checkpoint：`{payload['model_id']}` @ `{payload['resolved_model_revision']}`
- zero-shot top-1 / top-5：`{metrics['zero_shot_top1_accuracy']:.4f}` / `{metrics['zero_shot_top5_accuracy']:.4f}`
- 样本 / 类别：`{metrics['examples']}` / `{metrics['classes']}`
- text embedding cache hit：`{payload['cache']['text_embedding_cache_hit']}`

缓存同时绑定 checkpoint commit、完整类别集合与 prompt template；任一变化都会拒绝旧缓存。
有限 fold 或子集结果不是完整五折监督 ESC-50 指标。
"""
