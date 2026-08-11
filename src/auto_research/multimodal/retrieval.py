"""Compact, auditable image-text retrieval predictions from public checkpoints."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from typing import Any, Iterable

from ..runtime import device_for, lock_config_output, runtime_summary
from .benchmarks import _read_payload


RETRIEVAL_BENCHMARKS = ("coco-retrieval", "flickr30k-retrieval")


@dataclass(frozen=True)
class RetrievalPredictionConfig:
    benchmark: str
    annotations: Path
    image_root: Path
    output: Path
    model_id: str = "openai/clip-vit-base-patch32"
    checkpoint_path: Path | None = None
    revision: str = "main"
    split: str = "test"
    maximum_images: int | None = None
    batch_size: int = 32
    score_batch_size: int = 256
    seed: int = 42
    offline: bool = False


@dataclass(frozen=True)
class RetrievalImage:
    identifier: str
    path: Path
    text_ids: tuple[str, ...]


@dataclass(frozen=True)
class RetrievalText:
    identifier: str
    text: str
    image_id: str


@lock_config_output
def generate_retrieval_predictions(
    config: RetrievalPredictionConfig,
    *,
    processor: Any | None = None,
    model: Any | None = None,
    torch_module: Any | None = None,
) -> dict[str, Any]:
    """Encode images/captions and persist compact top-10 plus exact positive ranks.

    Full COCO 5K rankings contain roughly 125 million identifiers.  The compact
    format keeps top-10 candidates and the exact first-positive rank, which is
    sufficient to reproduce Recall@1/5/10 and median rank without a huge file.
    """
    if config.benchmark not in RETRIEVAL_BENCHMARKS:
        raise ValueError(f"retrieval prediction supports {', '.join(RETRIEVAL_BENCHMARKS)}")
    if config.batch_size < 1 or config.score_batch_size < 1:
        raise ValueError("batch sizes must be positive")
    if config.maximum_images is not None and config.maximum_images < 1:
        raise ValueError("maximum_images must be positive")

    images, texts = retrieval_items(config)
    if not images or not texts:
        raise ValueError("no retrieval examples selected")

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
        processor, model, resolved_revision = _load_retrieval_checkpoint(config, torch, device)

    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    inference_started = time.perf_counter()
    image_embeddings = _encode_images(
        images, processor, model, torch, device, config.batch_size
    )
    text_embeddings = _encode_texts(
        texts, processor, model, torch, device, config.batch_size
    )
    rows = _compact_rankings(
        images, texts, image_embeddings, text_embeddings,
        torch, device, config.score_batch_size,
    )
    inference_seconds = time.perf_counter() - inference_started

    config.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = config.output.with_suffix(config.output.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    temporary.replace(config.output)

    metadata = {
        "schema_version": 2,
        "benchmark": config.benchmark,
        "split": config.split,
        "model_id": config.model_id,
        "checkpoint_path": "local snapshot (not committed)" if config.checkpoint_path else None,
        "requested_revision": config.revision,
        "resolved_revision": resolved_revision,
        "seed": config.seed,
        "images": len(images),
        "captions": len(texts),
        "inference_seconds": inference_seconds,
        "seconds_per_image": inference_seconds / len(images),
        "peak_gpu_memory_mb": (
            torch.cuda.max_memory_allocated(device) / (1024 * 1024)
            if device.type == "cuda" else None
        ),
        "prediction_file": config.output.name,
        "annotations": config.annotations.name,
        "image_root": config.image_root.name or "configured root",
        "format": "top-10 candidates plus exact first-positive rank",
        "runtime": runtime_summary(torch),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    metadata_path = config.output.with_suffix(config.output.suffix + ".metadata.json")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    return metadata


def retrieval_items(
    config: RetrievalPredictionConfig,
) -> tuple[list[RetrievalImage], list[RetrievalText]]:
    payload = _read_payload(config.annotations)
    source = payload.get("images", payload) if isinstance(payload, dict) else payload
    selected = [row for row in source if row.get("split", config.split) == config.split]
    if config.maximum_images is not None:
        selected = selected[: config.maximum_images]
    images: list[RetrievalImage] = []
    texts: list[RetrievalText] = []
    for image_position, row in enumerate(selected):
        image_id = str(row.get("cocoid", row.get("imgid", row.get("image_id", image_position))))
        filename = str(row.get("filename", row.get("file_name", row.get("image", ""))))
        if not filename:
            raise ValueError(f"retrieval image {image_id} has no filename")
        image_path = _resolve_retrieval_image(
            config.image_root, filename, str(row.get("filepath", ""))
        )
        text_ids = []
        for sentence_position, sentence in enumerate(row.get("sentences", [])):
            text_id = str(
                sentence.get("sentid", sentence.get("id", f"{image_id}:{sentence_position}"))
            )
            caption = str(sentence.get("raw") or " ".join(sentence.get("tokens", []))).strip()
            if not caption:
                raise ValueError(f"retrieval text {text_id} is empty")
            text_ids.append(text_id)
            texts.append(RetrievalText(text_id, caption, image_id))
        if not text_ids:
            raise ValueError(f"retrieval image {image_id} has no captions")
        images.append(RetrievalImage(image_id, image_path, tuple(text_ids)))
    return images, texts


def _load_retrieval_checkpoint(config: RetrievalPredictionConfig, torch: Any, device: Any):
    from huggingface_hub import model_info
    from transformers import AutoModel, AutoProcessor

    resolved = config.revision
    if not config.offline:
        resolved = model_info(config.model_id, revision=config.revision).sha
    common = {"revision": resolved, "local_files_only": config.offline}
    source = str(config.checkpoint_path or config.model_id)
    processor = AutoProcessor.from_pretrained(source, **common)
    dtype = torch.float32
    if device.type == "cuda":
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    elif device.type == "mps":
        dtype = torch.float16
    model = AutoModel.from_pretrained(source, dtype=dtype, **common).to(device).eval()
    if not hasattr(model, "get_image_features") or not hasattr(model, "get_text_features"):
        raise ValueError(f"checkpoint {config.model_id!r} does not expose retrieval features")
    resolved = getattr(model.config, "_commit_hash", None) or resolved
    return processor, model, resolved


def _encode_images(images, processor, model, torch, device, batch_size):
    vectors = []
    from PIL import Image
    for batch in _batches(images, batch_size):
        opened = []
        try:
            for item in batch:
                with Image.open(item.path) as source:
                    opened.append(source.convert("RGB"))
            inputs = processor(images=opened, return_tensors="pt")
            pixels = inputs["pixel_values"].to(device)
            with torch.inference_mode():
                features = _feature_tensor(model.get_image_features(pixel_values=pixels))
            vectors.append(_normalize(features, torch).float().cpu())
        finally:
            for image in opened:
                image.close()
    return torch.cat(vectors)


def _encode_texts(texts, processor, model, torch, device, batch_size):
    vectors = []
    for batch in _batches(texts, batch_size):
        inputs = processor(
            text=[item.text for item in batch], padding=True, truncation=True,
            return_tensors="pt",
        )
        kwargs = {"input_ids": inputs["input_ids"].to(device)}
        if "attention_mask" in inputs:
            kwargs["attention_mask"] = inputs["attention_mask"].to(device)
        with torch.inference_mode():
            features = _feature_tensor(model.get_text_features(**kwargs))
        vectors.append(_normalize(features, torch).float().cpu())
    return torch.cat(vectors)


def _compact_rankings(images, texts, image_embeddings, text_embeddings, torch, device, batch_size):
    image_index = {item.identifier: index for index, item in enumerate(images)}
    text_index = {item.identifier: index for index, item in enumerate(texts)}
    candidate_text = text_embeddings.to(device)
    candidate_image = image_embeddings.to(device)
    top_text_k = min(10, len(texts))
    top_image_k = min(10, len(images))
    rows: list[dict[str, Any]] = []

    for start in range(0, len(images), batch_size):
        batch = image_embeddings[start:start + batch_size].to(device)
        scores = batch @ candidate_text.T
        top = torch.topk(scores, k=top_text_k, dim=1).indices.cpu().tolist()
        for offset, indices in enumerate(top):
            item = images[start + offset]
            positives = [text_index[text_id] for text_id in item.text_ids]
            best = scores[offset, positives].max()
            rank = int((scores[offset] > best).sum().item()) + 1
            rows.append({
                "image_id": item.identifier,
                "ranked_text_ids": [texts[index].identifier for index in indices],
                "relevant_text_rank": rank,
            })

    for start in range(0, len(texts), batch_size):
        batch = text_embeddings[start:start + batch_size].to(device)
        scores = batch @ candidate_image.T
        top = torch.topk(scores, k=top_image_k, dim=1).indices.cpu().tolist()
        for offset, indices in enumerate(top):
            item = texts[start + offset]
            positive = image_index[item.image_id]
            rank = int((scores[offset] > scores[offset, positive]).sum().item()) + 1
            rows.append({
                "text_id": item.identifier,
                "ranked_image_ids": [images[index].identifier for index in indices],
                "relevant_image_rank": rank,
            })
    return rows


def _feature_tensor(value: Any):
    if hasattr(value, "pooler_output"):
        return value.pooler_output
    if hasattr(value, "image_embeds"):
        return value.image_embeds
    if hasattr(value, "text_embeds"):
        return value.text_embeds
    return value


def _normalize(features: Any, torch: Any):
    return features / torch.linalg.vector_norm(features, dim=-1, keepdim=True).clamp_min(1e-12)


def _batches(values: list[Any], size: int) -> Iterable[list[Any]]:
    for start in range(0, len(values), size):
        yield values[start:start + size]


def _resolve_retrieval_image(root: Path, filename: str, filepath: str) -> Path:
    source = Path(filename)
    candidates = [
        source if source.is_absolute() else root / source,
        root / filepath / source.name,
        root / "val2014" / source.name,
        root / "test2014" / source.name,
        root / "images" / source.name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"retrieval image {filename!r} not found under configured image root")
