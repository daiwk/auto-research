#!/usr/bin/env python3
"""Download small, auditable public subsets for video/audio smoke runs."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request
import zipfile


ESC50_ROOT = "https://raw.githubusercontent.com/karolpiczak/ESC-50/master"
VIDEO_MME_ID = "MME-Benchmarks/Video-MME-v2"
VIDEO_MME_REVISION = "6e4bebb03202e1ddbf3d37703e560e51c5aa2d64"


def prepare_esc10(output: Path, examples_per_class: int) -> None:
    output.mkdir(parents=True, exist_ok=True)
    metadata = output / "esc50.csv"
    _download(f"{ESC50_ROOT}/meta/esc50.csv", metadata)
    rows = list(csv.DictReader(metadata.open(encoding="utf-8")))
    selected, counts = [], {}
    for row in rows:
        if row["esc10"].lower() != "true":
            continue
        label = row["category"]
        if counts.get(label, 0) >= examples_per_class:
            continue
        counts[label] = counts.get(label, 0) + 1
        selected.append(row)
    audio = output / "audio"
    audio.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(
                _download, f"{ESC50_ROOT}/audio/{row['filename']}",
                audio / row["filename"],
            )
            for row in selected
        ]
        for future in futures:
            future.result()
    with (output / "esc10-subset.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(selected)


def prepare_video_mme(output: Path, videos: int, source: str) -> None:
    try:
        from huggingface_hub import hf_hub_download
        from datasets import Dataset
    except ImportError as exc:
        raise RuntimeError("video preparation requires the multimodal extra") from exc
    output.mkdir(parents=True, exist_ok=True)
    parquet = Path(hf_hub_download(
        VIDEO_MME_ID, "test.parquet", repo_type="dataset",
        revision=VIDEO_MME_REVISION,
    ))
    rows = list(Dataset.from_parquet(str(parquet)))
    video_root = output / "videos"
    video_root.mkdir(exist_ok=True)
    unique_rows = []
    seen = set()
    for row in rows:
        if row["video_id"] not in seen:
            unique_rows.append(row)
            seen.add(row["video_id"])
    ids = _prepare_video_archives(
        unique_rows, video_root, videos, hf_hub_download
    ) if source == "archive" else _prepare_video_urls(
        unique_rows, video_root, videos
    )
    if len(ids) < videos:
        raise RuntimeError(
            f"only downloaded {len(ids)} of {videos} public Video-MME-v2 videos"
        )
    selected = [row for row in rows if row["video_id"] in ids]
    annotations = output / "test-subset.jsonl"
    annotations.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in selected),
        encoding="utf-8",
    )


def _prepare_video_archives(rows, video_root, videos, hf_hub_download):
    ids = [str(row["video_id"]) for row in rows[:videos]]
    archives: dict[str, list[str]] = {}
    for video_id in ids:
        archive = f"{((int(video_id) - 1) // 20) + 1:03d}"
        archives.setdefault(archive, []).append(video_id)
    for archive, video_ids in archives.items():
        path = Path(hf_hub_download(
            VIDEO_MME_ID, f"videos/{archive}.zip", repo_type="dataset",
            revision=VIDEO_MME_REVISION,
        ))
        with zipfile.ZipFile(path) as handle:
            for video_id in video_ids:
                target = video_root / f"{video_id}.mp4"
                if target.exists():
                    continue
                matches = [
                    name for name in handle.namelist()
                    if Path(name).name == f"{video_id}.mp4"
                ]
                if len(matches) != 1:
                    raise RuntimeError(
                        f"archive {archive} has no unique {video_id}.mp4"
                    )
                with handle.open(matches[0]) as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
    return ids


def _prepare_video_urls(rows, video_root, videos):
    ids = []
    for row in rows:
        video_id = str(row["video_id"])
        target = video_root / f"{video_id}.mp4"
        if target.exists():
            ids.append(video_id)
        else:
            completed = subprocess.run([
                sys.executable, "-m", "yt_dlp", "--quiet", "--no-playlist",
                "--merge-output-format", "mp4",
                "-f", "bv*[height<=480]+ba/b[height<=480]", "-o", str(target),
                row["url"],
            ], check=False)
            if completed.returncode == 0 and target.exists():
                ids.append(video_id)
        if len(ids) >= videos:
            break
    return ids


def _download(url: str, path: Path) -> None:
    if path.exists():
        return
    temporary = path.with_suffix(path.suffix + ".tmp")
    last_error = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                temporary.write_bytes(response.read())
            break
        except OSError as exc:
            last_error = exc
    else:
        raise RuntimeError(f"failed to download {url}") from last_error
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    esc = commands.add_parser("esc10")
    esc.add_argument("--output", type=Path, required=True)
    esc.add_argument("--examples-per-class", type=int, default=3)
    video = commands.add_parser("video-mme-v2")
    video.add_argument("--output", type=Path, required=True)
    video.add_argument("--videos", type=int, default=1)
    video.add_argument(
        "--source", choices=("archive", "youtube"), default="archive",
        help="archive is reproducible; youtube is smaller but sources may disappear",
    )
    args = parser.parse_args()
    if args.command == "esc10":
        prepare_esc10(args.output, args.examples_per_class)
    else:
        prepare_video_mme(args.output, args.videos, args.source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
