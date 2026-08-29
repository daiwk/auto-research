"""Real Qwen2.5-VL checkpoint evaluation for PACE APC.

The runner evaluates the same checkpoint on public RealWorldQA images at the
original resolution and at an adaptive PACE budget.  It deliberately keeps the
paper's large modeling fork external; ``--upstream-root`` records and verifies
the pinned author implementation used for cross-checking the equations.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import time
from typing import Any

from .model import apc_scores, target_resolution


@dataclass(frozen=True)
class CheckpointConfig:
    output: Path
    model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    revision: str = "main"
    model_path: Path | None = None
    dataset_id: str = "lmms-lab/RealWorldQA"
    dataset_revision: str = "main"
    split: str = "test"
    annotations: Path | None = None
    image_root: Path | None = None
    examples: int = 8
    maximum_new_tokens: int = 32
    seed: int = 42
    global_weight: float = 0.6
    detail_fraction: float = 0.1
    detail_scale: float = 1.5
    minimum_retention: float = 0.1
    upstream_root: Path | None = None
    upstream_commit: str = "7755240eb02510507c270457ed1768ddfe80c206"


def _normalise_answer(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def answer_match(prediction: str, references: list[str]) -> bool:
    prediction = _normalise_answer(prediction)
    return any(
        reference
        and (
            prediction == reference
            or re.search(rf"(?:^| ){re.escape(reference)}(?: |$)", prediction) is not None
        )
        for reference in (_normalise_answer(value) for value in references)
    )


def _extract_features(model, processor, image, torch, device):
    inputs = processor(images=[image], return_tensors="pt")
    pixel_values = inputs["pixel_values"].to(device)
    grid = inputs.get("image_grid_thw")
    if grid is not None:
        grid = grid.to(device)
    feature_owner = (
        model if hasattr(model, "get_image_features") else getattr(model, "model", model)
    )
    with torch.inference_mode():
        if hasattr(feature_owner, "get_image_features"):
            kwargs = {"pixel_values": pixel_values}
            if grid is not None:
                kwargs["image_grid_thw"] = grid
            if "pixel_attention_mask" in inputs:
                kwargs["pixel_attention_mask"] = inputs["pixel_attention_mask"].to(device)
            try:
                features = feature_owner.get_image_features(**kwargs)
            except TypeError:
                features = feature_owner.get_image_features(pixel_values=pixel_values)
        else:
            features = model.visual(pixel_values, grid_thw=grid)
    features = getattr(features, "last_hidden_state", features)
    features = getattr(features, "pooler_output", features)
    if isinstance(features, (tuple, list)):
        features = features[0]
    return features.reshape(-1, features.shape[-1])


def _generate(
    model,
    processor,
    image,
    question,
    torch,
    device,
    maximum_new_tokens,
    *,
    longest_edge: int | None = None,
):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": question},
            ],
        }
    ]
    prompt = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    image_kwargs = {"size": {"longest_edge": longest_edge}} if longest_edge else {}
    inputs = processor(
        text=[prompt], images=[image], padding=True, return_tensors="pt", **image_kwargs
    )
    inputs = {key: value.to(device) for key, value in inputs.items()}
    torch.cuda.synchronize()
    started = time.perf_counter()
    with torch.inference_mode():
        output = model.generate(**inputs, max_new_tokens=maximum_new_tokens, do_sample=False)
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - started
    generated = output[:, inputs["input_ids"].shape[1] :]
    return processor.batch_decode(generated, skip_special_tokens=True)[0], elapsed, inputs


def _references(row: dict[str, Any]) -> list[str]:
    for key in ("answer", "answers", "reference", "reference_answer"):
        if key in row:
            value = row[key]
            if isinstance(value, str):
                return [value]
            if isinstance(value, list):
                return [str(item) for item in value]
            if isinstance(value, dict):
                return [str(item) for item in value.get("text", value.values())]
    raise KeyError("RealWorldQA row has no answer/reference field")


def _load_rows(config: CheckpointConfig):
    if config.annotations and config.image_root:
        from PIL import Image

        rows = []
        with config.annotations.open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                with Image.open(config.image_root / row["image"]) as source:
                    image = source.convert("RGB")
                rows.append(
                    {
                        "image": image,
                        "question": row.get("text", row.get("question")),
                        "answer": row.get("label", row.get("answer")),
                    }
                )
                if len(rows) == config.examples:
                    break
        return rows, {
            "name": "POPE adversarial / COCO val2014",
            "revision": "public POPE release",
            "examples": len(rows),
        }
    from datasets import load_dataset
    from huggingface_hub import dataset_info

    dataset_revision = dataset_info(
        config.dataset_id,
        revision=config.dataset_revision,
    ).sha
    rows = load_dataset(
        config.dataset_id,
        revision=dataset_revision,
        split=config.split,
    ).select(range(config.examples))
    return rows, {
        "name": config.dataset_id,
        "revision": dataset_revision,
        "examples": len(rows),
    }


def run_checkpoint(config: CheckpointConfig) -> dict[str, Any]:
    import torch
    from huggingface_hub import model_info
    from transformers import AutoModelForImageTextToText, AutoProcessor

    if config.upstream_root:
        marker = config.upstream_root / ".git"
        if not marker.exists():
            raise ValueError("--upstream-root must be an author PACE git checkout")
    torch.manual_seed(config.seed)
    device = torch.device("cuda")
    revision = (
        config.revision
        if config.model_path
        else model_info(
            config.model_id,
            revision=config.revision,
        ).sha
    )
    source = str(config.model_path or config.model_id)
    processor = AutoProcessor.from_pretrained(
        source,
        revision=revision,
        local_files_only=config.model_path is not None,
    )
    model = (
        AutoModelForImageTextToText.from_pretrained(
            source,
            revision=revision,
            torch_dtype=torch.bfloat16,
            local_files_only=config.model_path is not None,
        )
        .to(device)
        .eval()
    )
    rows, dataset_metadata = _load_rows(config)
    processor_size = getattr(getattr(processor, "image_processor", None), "size", {})
    baseline_edge = (
        int(processor_size["longest_edge"])
        if isinstance(processor_size, dict) and "longest_edge" in processor_size
        else None
    )
    torch.cuda.reset_peak_memory_stats(device)
    records = []
    for row in rows:
        image = row["image"].convert("RGB")
        question = row.get("question") or row.get("query") or row.get("text")
        references = _references(row)
        features = _extract_features(model, processor, image, torch, device)
        retention, density, detail = apc_scores(
            features,
            global_weight=config.global_weight,
            detail_fraction=config.detail_fraction,
            detail_scale=config.detail_scale,
            minimum_retention=config.minimum_retention,
        )
        new_height, new_width, actual = target_resolution(
            image.height,
            image.width,
            retention=retention,
            patch_size=28,
        )
        resized = image.resize((new_width, new_height))
        method_edge = (
            max(28, round(baseline_edge * math.sqrt(actual))) if baseline_edge is not None else None
        )
        baseline_answer, baseline_seconds, baseline_inputs = _generate(
            model,
            processor,
            image,
            question,
            torch,
            device,
            config.maximum_new_tokens,
            longest_edge=baseline_edge,
        )
        method_answer, method_seconds, method_inputs = _generate(
            model,
            processor,
            resized,
            question,
            torch,
            device,
            config.maximum_new_tokens,
            longest_edge=method_edge,
        )
        baseline_tokens = int(baseline_inputs["attention_mask"].sum())
        method_tokens = int(method_inputs["attention_mask"].sum())
        records.append(
            {
                "baseline_correct": answer_match(baseline_answer, references),
                "method_correct": answer_match(method_answer, references),
                "baseline_seconds": baseline_seconds,
                "method_seconds": method_seconds,
                "baseline_input_tokens": baseline_tokens,
                "method_input_tokens": method_tokens,
                "retention": actual,
                "baseline_longest_edge": baseline_edge,
                "pace_longest_edge": method_edge,
                "global_density": density,
                "local_detail": detail,
            }
        )
    count = len(records)
    average = lambda key: sum(float(row[key]) for row in records) / count
    payload = {
        "schema_version": 3,
        "method": "pace-apc-real-checkpoint",
        "dataset": dataset_metadata,
        "checkpoint": {"model_id": config.model_id, "revision": revision},
        "setup": {
            **asdict(config),
            "output": str(config.output),
            "model_path": None,
            "upstream_root": None,
            "annotations": None,
            "image_root": None,
        },
        "metrics": {
            "baseline_accuracy": average("baseline_correct"),
            "pace_accuracy": average("method_correct"),
            "baseline_input_tokens_mean": average("baseline_input_tokens"),
            "pace_input_tokens_mean": average("method_input_tokens"),
            "token_reduction_percent": 100
            * (1 - average("method_input_tokens") / average("baseline_input_tokens")),
            "baseline_latency_seconds_mean": average("baseline_seconds"),
            "pace_latency_seconds_mean": average("method_seconds"),
            "peak_gpu_memory_mb": torch.cuda.max_memory_allocated(device) / 1024**2,
        },
        "records": records,
        "upstream": {"url": "https://github.com/jjL357/PACE", "commit": config.upstream_commit},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Real VLM checkpoint and public VQA subset; APC path, not paper-scale suite.",
    }
    config.output.parent.mkdir(parents=True, exist_ok=True)
    config.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-id", default=CheckpointConfig.model_id)
    parser.add_argument("--revision", default="main")
    parser.add_argument("--model-path", type=Path)
    parser.add_argument("--dataset-id", default=CheckpointConfig.dataset_id)
    parser.add_argument("--dataset-revision", default="main")
    parser.add_argument("--split", default="test")
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--image-root", type=Path)
    parser.add_argument("--examples", type=int, default=8)
    parser.add_argument("--maximum-new-tokens", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--global-weight", type=float, default=0.6)
    parser.add_argument("--detail-fraction", type=float, default=0.1)
    parser.add_argument("--detail-scale", type=float, default=1.5)
    parser.add_argument("--minimum-retention", type=float, default=0.1)
    parser.add_argument("--upstream-root", type=Path)
    parser.add_argument("--upstream-commit", default=CheckpointConfig.upstream_commit)
    payload = run_checkpoint(CheckpointConfig(**vars(parser.parse_args())))
    print(json.dumps(payload["metrics"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
