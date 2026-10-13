#!/usr/bin/env python3
"""Prepare a class-balanced, image-disjoint CV-OPD diagnostic from COCO train2017.

The official test/val sets are not opened. The answer category is never put in
the model question. A fixed public annotation archive and exact image bytes are
recorded; this is not the paper's fine-grained VisualOPD dataset.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import requests
from PIL import Image

from auto_research.oct12_public_sources import sha256_file

# Official public bucket via TLS-valid path-style endpoint. The custom
# images.cocodataset.org HTTPS hostname currently fails certificate matching;
# do not disable certificate verification to work around it.
ANNOTATIONS = "https://s3.amazonaws.com/images.cocodataset.org/annotations/annotations_trainval2017.zip"
CATEGORIES = ("person", "cat", "dog", "car", "bus", "bird", "horse", "bicycle")
QUESTION = "Name the main object in this picture. Reply with one COCO category name and no other words."


def download(url: str, path: Path) -> None:
    with requests.get(url, stream=True, timeout=(20, 120)) as response:
        response.raise_for_status()
        with path.open("wb") as output:
            for chunk in response.iter_content(1 << 20):
                output.write(chunk)


def prepare(archive: Path, output: Path) -> dict:
    if output.exists():
        raise FileExistsError("choose a fresh public-data mirror directory")
    archive_hash = sha256_file(archive)
    with zipfile.ZipFile(archive) as bundle:
        raw = bundle.read("annotations/instances_train2017.json")
    annotations = json.loads(raw)
    names = {row["id"]: row["name"] for row in annotations["categories"]}
    images = {row["id"]: row for row in annotations["images"]}
    by_image = {}
    for box in annotations["annotations"]:
        by_image.setdefault(box["image_id"], []).append(box)
    selected = {name: [] for name in CATEGORIES}
    for image_id in sorted(images):
        boxes = by_image.get(image_id, [])
        labels = {names[box["category_id"]] for box in boxes}
        # One annotated category only; no hidden negative-class construction.
        if len(labels) != 1:
            continue
        category = next(iter(labels))
        if category not in selected or len(selected[category]) >= 4:
            continue
        eligible = [box for box in boxes if not box.get("iscrowd")]
        if not eligible:
            continue
        largest = max(eligible, key=lambda box: box["area"])
        image = images[image_id]
        x, y, width, height = largest["bbox"]
        if largest["area"] / (image["width"] * image["height"]) < .1 or min(width, height) < 32:
            continue
        # Require at least one true same-size corner crop at IoU<=.1.
        # Never resize the negative crop or replace it with a different image.
        overlaps = []
        for left in (0, image["width"] - width):
            for top in (0, image["height"] - height):
                intersect = max(0, min(x + width, left + width) - max(x, left)) * max(
                    0, min(y + height, top + height) - max(y, top))
                overlaps.append(intersect / max(1, 2 * width * height - intersect))
        if min(overlaps) > .1:
            continue
        selected[category].append((image, [x, y, x + width, y + height]))
    if any(len(rows) != 4 for rows in selected.values()):
        raise ValueError("the fixed public annotations do not satisfy the declared class-balanced protocol")
    output.mkdir(parents=True)
    (output / "images").mkdir()
    rows, files = [], {}
    for category, choices in selected.items():
        for index, (image, bbox) in enumerate(choices):
            relative = "images/" + image["file_name"]
            url = "https://s3.amazonaws.com/images.cocodataset.org/train2017/" + image["file_name"]
            path = output / relative
            download(url, path)
            with Image.open(path) as decoded:
                decoded.verify()
            files[relative] = sha256_file(path)
            rows.append({"id": image["id"], "image": relative, "question": QUESTION,
                         "answer": category, "bbox": bbox, "verified": True,
                         "split": "train" if index < 2 else "validation" if index == 2 else "test"})
    records = output / "records.jsonl"
    records.write_text("".join(json.dumps(row) + "\n" for row in rows))
    files[records.name] = sha256_file(records)
    manifest = {"kind": "dataset", "public_id": "COCO2017/train2017",
                "revision": archive_hash, "source_split": "train2017", "test_opened": False,
                "source": ANNOTATIONS, "annotations_sha256": hashlib.sha256(raw).hexdigest(),
                "files": files, "rows": len(rows), "categories": list(CATEGORIES),
                "counts": {split: sum(row["split"] == split for row in rows)
                           for split in ("train", "validation", "test")},
                "selection": "first 4 image IDs per category with one annotated category; largest noncrowd box >=10% image area and >=32px sides; same-size corner negative crop IoU<=.1 feasible",
                "split": "per-category ordered 2 train / 1 validation / 1 test; image-disjoint, all from official train2017",
                "scope": "class-balanced object-name mechanism diagnostic, not VisualOPD or official COCO evaluation"}
    (output / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return {key: manifest[key] for key in ("public_id", "revision", "rows", "counts", "scope")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.annotations_archive, args.output), indent=2))


if __name__ == "__main__":
    main()
