"""Auditable prediction generation with public multimodal checkpoints."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import time
from typing import Any, Iterable

from ..runtime import device_for, lock_config_output, runtime_summary
from .benchmarks import _read_payload, _records, _scienceqa_problems


GENERATIVE_BENCHMARKS = ("scienceqa", "pope")


@dataclass(frozen=True)
class CheckpointPredictionConfig:
    benchmark: str
    annotations: Path
    image_root: Path
    output: Path
    model_id: str
    checkpoint_path: Path | None = None
    revision: str = "main"
    split: str = "test"
    maximum_examples: int | None = None
    max_new_tokens: int = 16
    seed: int = 42
    offline: bool = False
    prompt_style: str = "direct"
    use_hint: bool = True
    image_size: int = 0
    batch_size: int = 1


@dataclass(frozen=True)
class PredictionExample:
    identifier: str
    prompt: str
    image: Path | None
    choices: tuple[str, ...] = ()


@lock_config_output
def generate_checkpoint_predictions(
    config: CheckpointPredictionConfig,
    *,
    processor: Any | None = None,
    model: Any | None = None,
    torch_module: Any | None = None,
) -> dict[str, Any]:
    """Generate resumable JSONL predictions and a provenance sidecar.

    ``processor`` and ``model`` injection keeps unit tests download-free. Normal
    CLI use resolves the requested Hugging Face revision to an immutable commit.
    """
    if config.benchmark not in GENERATIVE_BENCHMARKS:
        raise ValueError(
            f"checkpoint prediction supports {', '.join(GENERATIVE_BENCHMARKS)}"
        )
    if config.max_new_tokens < 1:
        raise ValueError("max_new_tokens must be positive")
    if config.maximum_examples is not None and config.maximum_examples < 1:
        raise ValueError("maximum_examples must be positive")
    if config.batch_size < 1:
        raise ValueError("batch_size must be positive")

    examples = list(iter_prediction_examples(config))
    if config.maximum_examples is not None:
        examples = examples[: config.maximum_examples]
    if not examples:
        raise ValueError("no benchmark examples selected")

    torch = torch_module
    if torch is None:
        import torch as torch_import
        torch = torch_import
    device = device_for(torch)
    torch.manual_seed(config.seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(config.seed)
    resolved_revision = config.revision
    if processor is None or model is None:
        processor, model, resolved_revision = _load_checkpoint(
            config, torch, device
        )

    config.output.parent.mkdir(parents=True, exist_ok=True)
    completed = _completed_ids(
        config.output, model_id=config.model_id, model_revision=resolved_revision
    )
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    inference_started = time.perf_counter()
    pending = [example for example in examples if example.identifier not in completed]
    written = 0
    with config.output.open("a", encoding="utf-8") as handle:
        for start in range(0, len(pending), config.batch_size):
            batch = pending[start:start + config.batch_size]
            images = [_open_image(example.image, config.image_size) for example in batch]
            if len(batch) > 1 and all(image is not None for image in images):
                raw_predictions = _generate_many(
                    processor, model, torch, device, images,
                    [example.prompt for example in batch],
                    max_new_tokens=config.max_new_tokens,
                )
            else:
                raw_predictions = [
                    _generate_one(
                        processor, model, torch, device, image, example.prompt,
                        max_new_tokens=config.max_new_tokens,
                    )
                    for example, image in zip(batch, images)
                ]
            for example, raw in zip(batch, raw_predictions):
                prediction = normalize_prediction(
                    config.benchmark, raw, example.choices
                )
                row = {
                    "id": example.identifier,
                    "prediction": prediction,
                    "raw_prediction": raw,
                    "model_id": config.model_id,
                    "model_revision": resolved_revision,
                    "seed": config.seed,
                    "prediction_valid": prediction != "__invalid__",
                }
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                written += 1
            handle.flush()
    inference_seconds = time.perf_counter() - inference_started

    metadata = {
        "schema_version": 1,
        "benchmark": config.benchmark,
        "split": config.split,
        "model_id": config.model_id,
        "checkpoint_path": (
            "local snapshot (not committed)" if config.checkpoint_path else None
        ),
        "requested_revision": config.revision,
        "resolved_revision": resolved_revision,
        "deterministic_decoding": True,
        "seed": config.seed,
        "max_new_tokens": config.max_new_tokens,
        "batch_size": config.batch_size,
        "selected_examples": len(examples),
        "new_predictions": written,
        "inference_seconds": inference_seconds,
        "seconds_per_new_prediction": inference_seconds / written if written else None,
        "peak_gpu_memory_mb": (
            torch.cuda.max_memory_allocated(device) / (1024 * 1024)
            if device.type == "cuda" else None
        ),
        "prediction_file": config.output.name,
        "annotations": config.annotations.name,
        "image_root": config.image_root.name,
        "runtime": runtime_summary(torch),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    metadata_path = prediction_metadata_path(config.output)
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return metadata


def iter_prediction_examples(
    config: CheckpointPredictionConfig,
) -> Iterable[PredictionExample]:
    payload = _read_payload(config.annotations)
    if config.benchmark == "scienceqa":
        for identifier, row in _scienceqa_problems(payload, config.split).items():
            choices = tuple(str(choice) for choice in row["choices"])
            yield PredictionExample(
                identifier=identifier,
                prompt=scienceqa_prompt(
                    row, style=config.prompt_style, use_hint=config.use_hint
                ),
                image=resolve_scienceqa_image(
                    config.image_root, config.split, identifier, row.get("image")
                ),
                choices=choices,
            )
        return
    for position, row in enumerate(_records(payload)):
        identifier = str(row.get("question_id", row.get("id", position)))
        question = str(row.get("text", row.get("question", ""))).strip()
        if not question:
            raise ValueError(f"POPE record {identifier} has no question text")
        image_name = row.get("image", row.get("image_path"))
        if not image_name:
            raise ValueError(f"POPE record {identifier} has no image")
        yield PredictionExample(
            identifier=identifier,
            prompt=f"{question}\nAnswer only yes or no.",
            image=resolve_image(config.image_root, str(image_name)),
        )


def scienceqa_prompt(
    row: dict[str, Any], *, style: str = "direct", use_hint: bool = True
) -> str:
    if style not in {"direct", "context-first", "elimination"}:
        raise ValueError(f"unknown ScienceQA prompt style: {style}")
    choices = "\n".join(
        f"{chr(65 + index)}. {choice}"
        for index, choice in enumerate(row["choices"])
    )
    context = str(row.get("hint") or "").strip() if use_hint else ""
    prefix = f"Context: {context}\n" if context else ""
    instruction = {
        "direct": "Answer with only the option letter.",
        "context-first": (
            "Use the image and context first, then return only the option letter."
        ),
        "elimination": (
            "Silently eliminate incompatible choices and return only the option letter."
        ),
    }[style]
    return (
        f"{prefix}Question: {str(row['question']).strip()}\n"
        f"Choices:\n{choices}\n{instruction}"
    )


def resolve_scienceqa_image(
    image_root: Path, split: str, identifier: str, image_name: Any
) -> Path | None:
    if not image_name:
        return None
    candidates = (
        image_root / split / identifier / str(image_name),
        image_root / identifier / str(image_name),
        image_root / split / str(image_name),
        image_root / str(image_name),
    )
    return _first_existing(candidates, identifier)


def resolve_image(image_root: Path, image_name: str) -> Path:
    source = Path(image_name)
    candidates = (
        source if source.is_absolute() else image_root / source,
        image_root / "val2014" / source.name,
        image_root / "test2014" / source.name,
    )
    return _first_existing(candidates, image_name)


def normalize_prediction(
    benchmark: str, raw: str, choices: tuple[str, ...] = ()
) -> str:
    text = raw.strip()
    if benchmark == "pope":
        match = re.search(r"\b(yes|no)\b", text, flags=re.IGNORECASE)
        if not match:
            return "__invalid__"
        return match.group(1).lower()
    for pattern in (
        r"(?:answer|option|choice)\s*(?:is|:)?\s*\(?([A-Z])\)?",
        r"^\s*\(?([A-Z])\)?(?:[.\s]|$)",
    ):
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match and ord(match.group(1)) - 65 < len(choices):
            return match.group(1).upper()
    lowered = text.casefold().strip(" .")
    for index, choice in enumerate(choices):
        if lowered == choice.casefold().strip(" ."):
            return chr(65 + index)
    return "__invalid__"


def prediction_metadata_path(output: Path) -> Path:
    return output.with_suffix(output.suffix + ".metadata.json")


def _load_checkpoint(config: CheckpointPredictionConfig, torch: Any, device: Any):
    from huggingface_hub import model_info
    from transformers import AutoModelForImageTextToText, AutoProcessor
    from transformers.utils import logging as transformers_logging

    transformers_logging.set_verbosity_error()

    resolved = config.revision
    if not config.offline:
        resolved = model_info(config.model_id, revision=config.revision).sha
    common = {
        "revision": resolved,
        "local_files_only": config.offline,
    }
    source = str(config.checkpoint_path or config.model_id)
    processor = AutoProcessor.from_pretrained(source, **common)
    dtype = torch.float32
    if device.type == "cuda":
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    elif device.type == "mps":
        dtype = torch.float16
    model = AutoModelForImageTextToText.from_pretrained(
        source, dtype=dtype, **common
    ).to(device).eval()
    resolved = getattr(model.config, "_commit_hash", None) or resolved
    return processor, model, resolved


def _generate_one(
    processor: Any, model: Any, torch: Any, device: Any,
    image: Any | None, prompt: str, *, max_new_tokens: int,
) -> str:
    content = []
    if image is not None:
        content.append({"type": "image"})
    content.append({"type": "text", "text": prompt})
    rendered = processor.apply_chat_template(
        [{"role": "user", "content": content}],
        add_generation_prompt=True,
        tokenize=False,
    )
    kwargs: dict[str, Any] = {"text": rendered, "return_tensors": "pt"}
    if image is not None:
        kwargs["images"] = [image]
    inputs = processor(**kwargs)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    prompt_tokens = inputs["input_ids"].shape[-1]
    with torch.inference_mode():
        generated = model.generate(
            **inputs, max_new_tokens=max_new_tokens, do_sample=False
        )
    return processor.decode(
        generated[0, prompt_tokens:], skip_special_tokens=True
    ).strip()


def _generate_many(
    processor: Any, model: Any, torch: Any, device: Any,
    images: list[Any], prompts: list[str], *, max_new_tokens: int,
) -> list[str]:
    rendered = [
        processor.apply_chat_template(
            [{"role": "user", "content": [
                {"type": "image"}, {"type": "text", "text": prompt},
            ]}],
            add_generation_prompt=True,
            tokenize=False,
        )
        for prompt in prompts
    ]
    tokenizer = getattr(processor, "tokenizer", None)
    original_padding_side = getattr(tokenizer, "padding_side", None)
    if tokenizer is not None:
        # Decoder-only checkpoints continue after the padded batch width.  With
        # right padding, shorter prompts generate from PAD instead of their last
        # real token and can return unrelated fragments despite valid tensors.
        tokenizer.padding_side = "left"
    try:
        inputs = processor(
            text=rendered, images=[[image] for image in images],
            padding=True, return_tensors="pt"
        )
    finally:
        if tokenizer is not None and original_padding_side is not None:
            tokenizer.padding_side = original_padding_side
    inputs = {key: value.to(device) for key, value in inputs.items()}
    prompt_width = inputs["input_ids"].shape[-1]
    with torch.inference_mode():
        generated = model.generate(
            **inputs, max_new_tokens=max_new_tokens, do_sample=False
        )
    return [
        processor.decode(row[prompt_width:], skip_special_tokens=True).strip()
        for row in generated
    ]


def _open_image(path: Path | None, image_size: int = 0):
    if path is None:
        return None
    from PIL import Image
    with Image.open(path) as source:
        image = source.convert("RGB")
        if image_size > 0:
            image.thumbnail((image_size, image_size))
        return image


def _first_existing(candidates: Iterable[Path], label: str) -> Path:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    rendered = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"image {label!r} not found; tried: {rendered}")


def _completed_ids(
    output: Path, *, model_id: str, model_revision: str
) -> set[str]:
    if not output.exists():
        return set()
    completed = set()
    for line_number, line in enumerate(
        output.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            if row.get("model_id") != model_id:
                raise ValueError(
                    f"prediction file model mismatch at line {line_number}: "
                    f"{row.get('model_id')!r} != {model_id!r}"
                )
            if row.get("model_revision") != model_revision:
                raise ValueError(
                    f"prediction file revision mismatch at line {line_number}: "
                    f"{row.get('model_revision')!r} != {model_revision!r}"
                )
            completed.add(str(row["id"]))
        except (json.JSONDecodeError, KeyError) as error:
            raise ValueError(
                f"invalid resumable prediction file at line {line_number}"
            ) from error
    return completed
