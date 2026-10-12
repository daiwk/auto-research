#!/usr/bin/env python3
"""Export small PINNED official subsets / public checkpoints with byte hashes.

Run on a host that can access Hugging Face, then synchronize the resulting
directory. Never use this to relabel legacy/unverified local data as a pinned
source. It downloads the explicitly pinned revision before sealing hashes.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path

from auto_research.multimodal.oct12_reward_transition import (
    COCO_DATASET, COCO_REVISION, VLM_CHECKPOINT, VLM_REVISION,
    WOVEN_REVISION, load_coco, load_woven,
)
from auto_research.oct12_public_sources import sha256_file
from auto_research.reproductions.oct12_foundation_multimodal import (
    SMOLLM_CHECKPOINT, SMOLLM_REVISION, WIKITEXT_REVISION,
)


def export_wikitext(output: Path, train_bytes: int, eval_bytes: int):
    from datasets import load_dataset
    dataset = load_dataset("Salesforce/wikitext", "wikitext-2-raw-v1", revision=WIKITEXT_REVISION,
                           streaming=True)
    files, counts = {}, {}
    for split in ("train", "validation", "test"):
        budget = train_bytes if split == "train" else eval_bytes
        chunks, size = [], 0
        for row in dataset[split]:
            piece = (row["text"] + "\n").encode("utf-8")
            chunks.append(piece)
            size += len(piece)
            if size >= budget:
                break
        raw = b"".join(chunks)[:budget]
        target = output / f"{split}.txt"
        target.write_bytes(raw)
        files[target.name], counts[split] = hashlib.sha256(raw).hexdigest(), len(raw)
    return {"kind": "dataset", "public_id": "Salesforce/wikitext", "revision": WIKITEXT_REVISION,
            "configuration": "wikitext-2-raw-v1", "source_splits": ["train", "validation", "test"],
            "transformation": "ordered official raw text rows + newline, deterministic byte cap",
            "bytes_per_split": counts, "files": files}


def export_images(output: Path, paper: str, maximum: int):
    rows = load_woven(output / "hf-cache", maximum) if paper == "woven" else load_coco(output / "hf-cache", maximum)
    if paper == "woven" and len({row["source_id"] for row in rows}) < 5:
        raise ValueError("prefix has <5 source groups: increase --maximum; no nongrouped split fallback")
    (output / "images").mkdir()
    files = {}
    def store_image(image):
        buffer = io.BytesIO()
        image.convert("RGB").save(buffer, format="PNG")
        raw = buffer.getvalue()
        digest = hashlib.sha256(raw).hexdigest()
        relative = f"images/{digest}.png"
        if relative not in files:
            (output / relative).write_bytes(raw)
            files[relative] = digest
        return {"path": relative}
    serializable = []
    for original in rows:
        row = dict(original)
        if paper == "woven":
            row["images"] = [store_image(image) for image in original["images"]]
        else:
            row["image"] = store_image(original["image"])
        row["source_row_sha256"] = hashlib.sha256(
            json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        serializable.append(row)
    filename = "woven.jsonl" if paper == "woven" else "coco.jsonl"
    target = output / filename
    target.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in serializable))
    files[filename] = sha256_file(target)
    return {"kind": "dataset", "public_id": "MLL-Lab/WOVEN" if paper == "woven" else COCO_DATASET,
            "revision": WOVEN_REVISION if paper == "woven" else COCO_REVISION,
            "split": "train" if paper == "woven" else "val", "rows": len(rows),
            "transformation": "ordered public subset; decoded RGB images encoded as lossless PNG; question/option/reference text unchanged",
            "files": files}


def export_checkpoint(output: Path, name: str):
    from huggingface_hub import snapshot_download
    public_id, revision = ((VLM_CHECKPOINT, VLM_REVISION) if name == "smolvlm" else
                            (SMOLLM_CHECKPOINT, SMOLLM_REVISION))
    snapshot_download(public_id, revision=revision, local_dir=output,
                       allow_patterns=["*.json", "*.safetensors", "*.txt"], ignore_patterns=["onnx/*"])
    files = {p.relative_to(output).as_posix(): sha256_file(p) for p in output.rglob("*")
             if p.is_file() and (p.name.endswith(".json") or p.name.endswith(".safetensors")
                                or p.name in {"merges.txt", "vocab.txt"}) and ".cache" not in p.parts}
    return {"kind": "checkpoint", "public_id": public_id, "revision": revision, "files": files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, choices=["wikitext", "woven", "coco", "smolvlm", "smollm"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum", type=int, default=96)
    parser.add_argument("--train-bytes", type=int, default=32768)
    parser.add_argument("--eval-bytes", type=int, default=4096)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("a fresh output directory is required")
    args.output.mkdir(parents=True)
    if args.source == "wikitext":
        metadata = export_wikitext(args.output, args.train_bytes, args.eval_bytes)
    elif args.source in {"woven", "coco"}:
        metadata = export_images(args.output, args.source, args.maximum)
    else:
        metadata = export_checkpoint(args.output, args.source)
    (args.output / "provenance.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"source": args.source, "public_id": metadata["public_id"],
                      "revision": metadata["revision"], "files": len(metadata["files"]),
                      "rows": metadata.get("rows")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
