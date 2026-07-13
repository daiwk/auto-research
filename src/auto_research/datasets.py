from __future__ import annotations

import csv
import io
import urllib.request
import zipfile
from pathlib import Path

SHAKESPEARE_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"


def tiny_shakespeare(root: Path, allow_network: bool = True) -> str:
    target = root / "tiny_shakespeare.txt"
    if not target.exists():
        if not allow_network:
            raise FileNotFoundError(f"dataset missing and network disabled: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        _download(SHAKESPEARE_URL, target)
    return target.read_text(encoding="utf-8")


def movielens_100k(root: Path, allow_network: bool = True) -> list[tuple[int, int, float, int]]:
    target = root / "ml-100k" / "u.data"
    if not target.exists():
        if not allow_network:
            raise FileNotFoundError(f"dataset missing and network disabled: {target}")
        archive = root / "ml-100k.zip"
        archive.parent.mkdir(parents=True, exist_ok=True)
        _download(MOVIELENS_URL, archive)
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(root)
    rows: list[tuple[int, int, float, int]] = []
    with target.open(encoding="utf-8") as stream:
        for row in csv.reader(stream, delimiter="\t"):
            rows.append((int(row[0]), int(row[1]), float(row[2]), int(row[3])))
    return rows


def _download(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "auto-research/0.1"})
    with urllib.request.urlopen(request, timeout=120) as response:
        target.write_bytes(response.read())
