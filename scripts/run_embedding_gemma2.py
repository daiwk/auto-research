#!/usr/bin/env python3
"""Bounded official checkpoint image/text retrieval, no fine tuning."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from auto_research.multimodal.embedding_gemma2 import EmbeddingGemma2Encoder, MODEL_ID, REVISION, retrieval_recall
from auto_research.oct12_public_sources import verify_offline_manifest

DATA_ID = "lmms-lab-encoder/COCO-Caption2017"
DATA_REVISION = "3bdd5827e243cc3084ac69a1111e69c3ab9193ff"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--checkpoint-path", type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--images", type=int, default=16)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or not 2 <= args.images <= 40:
        raise ValueError("fresh output and at most 40 images required by cost gate")
    dataset = verify_offline_manifest(args.dataset_dir, DATA_ID, DATA_REVISION, "dataset")
    checkpoint = verify_offline_manifest(args.checkpoint_path, MODEL_ID, REVISION, "checkpoint")
    rows = [json.loads(line) for line in (args.dataset_dir / "coco.jsonl").read_text().splitlines()][:args.images]
    from PIL import Image
    import torch
    torch.manual_seed(args.seed)
    torch.set_num_threads(4)
    model = EmbeddingGemma2Encoder.load(checkpoint_path=args.checkpoint_path, device=args.device)
    images = []
    for row in rows:
        with Image.open(args.dataset_dir / row["image"]["path"]) as image:
            images.append(image.convert("RGB"))
    texts, text_ids = [], []
    for row in rows:
        references = row.get("references") or [row["caption"]]
        texts.extend(references)
        text_ids.extend([row["id"]] * len(references))
    start = time.monotonic()
    if args.device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    try:
        image_vectors = model.encode(images=images, role="document", batch_size=2)
        text_vectors = model.encode(texts=texts, role="query", batch_size=4)
    finally:
        for image in images:
            image.close()
    metrics = {}
    for dimension in (128, 256, 512, 768):
        # Four predeclared dimensions: report all, do not choose on this holdout.
        image = torch.nn.functional.normalize(image_vectors[:, :dimension], dim=-1)
        text = torch.nn.functional.normalize(text_vectors[:, :dimension], dim=-1)
        metrics[str(dimension)] = retrieval_recall(image, text, text_ids, [row["id"] for row in rows])
    payload = {"method": "embedding-gemma2", "seed": args.seed, "device": args.device,
        "measured_locally": True, "diagnostic_only": True, "dataset": dataset, "checkpoint": checkpoint,
        "metrics": metrics, "images": len(rows), "captions": len(texts),
        "elapsed_seconds": time.monotonic() - start,
        "peak_memory_bytes": torch.cuda.max_memory_allocated() if args.device == "cuda" else None,
        "protocol": {"precision": "float32", "image_soft_tokens": 70,
            "pooling": "attention-masked mean, slice then L2-normalize",
            "dimensions_predeclared": [128,256,512,768], "test_used_for_selection": False,
            "audio_tower_loaded": False, "training": False},
        "embedding_sha256": {"image": hashlib.sha256(image_vectors.numpy().tobytes()).hexdigest(),
                             "text": hashlib.sha256(text_vectors.numpy().tobytes()).hexdigest()},
        "limitations": ["Fixed small COCO validation prefix, not the official full retrieval benchmark.",
                        "No audio/video or fine-tuning claim; no comparison against retrained models.",
                        "One deterministic checkpoint inference is not a multi-seed training comparison."]}
    args.output.mkdir(parents=True)
    (args.output / "result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"metrics": metrics, "elapsed_seconds": payload["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
