from __future__ import annotations

import csv
import gzip
import io
import json
import urllib.request
import zipfile
from pathlib import Path

SHAKESPEARE_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
MOVIELENS_1M_URL = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"
AMAZON_BEAUTY_5CORE_URL = (
    "https://snap.stanford.edu/data/amazon/productGraph/"
    "categoryFiles/reviews_Beauty_5.json.gz"
)
MDCNS_BEAUTY_BASE_URL = (
    "https://raw.githubusercontent.com/Lyz103/SIGIR26-MDCNS/main/"
    "MDCNS_Code/data"
)


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


def movielens_1m(root: Path, allow_network: bool = True) -> list[tuple[int, int, float, int]]:
    target = root / "ml-1m" / "ratings.dat"
    if not target.exists():
        _download_and_extract(root, "ml-1m.zip", MOVIELENS_1M_URL, target, allow_network)
    rows: list[tuple[int, int, float, int]] = []
    with target.open(encoding="utf-8") as stream:
        for line in stream:
            user, item, rating, timestamp = line.rstrip().split("::")
            rows.append((int(user), int(item), float(rating), int(timestamp)))
    return rows


def amazon_beauty_5core(
    root: Path, allow_network: bool = True
) -> list[tuple[str, str, float, int]]:
    target = root / "amazon-beauty-5core" / "reviews_Beauty_5.json.gz"
    if not target.exists():
        if not allow_network:
            raise FileNotFoundError(f"dataset missing and network disabled: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        _download(AMAZON_BEAUTY_5CORE_URL, target)
    rows: list[tuple[str, str, float, int]] = []
    with gzip.open(target, "rt", encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            rows.append(
                (
                    record["reviewerID"],
                    record["asin"],
                    float(record.get("overall", 1.0)),
                    int(record["unixReviewTime"]),
                )
            )
    return rows


def mdcns_beauty_sequences(
    root: Path, allow_network: bool = True
) -> dict[str, list[tuple[int, ...]]]:
    directory = root / "mdcns-beauty"
    result: dict[str, list[tuple[int, ...]]] = {}
    for split in ("train", "val", "test"):
        target = directory / f"Beauty_{split}.txt"
        if not target.exists():
            if not allow_network:
                raise FileNotFoundError(f"dataset missing and network disabled: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            _download(f"{MDCNS_BEAUTY_BASE_URL}/Beauty_{split}.txt", target)
        with target.open(encoding="utf-8") as stream:
            result[split] = [tuple(map(int, line.split())) for line in stream if line.strip()]
    return result


def _download_and_extract(
    root: Path, archive_name: str, url: str, target: Path, allow_network: bool
) -> None:
    if not allow_network:
        raise FileNotFoundError(f"dataset missing and network disabled: {target}")
    archive = root / archive_name
    archive.parent.mkdir(parents=True, exist_ok=True)
    _download(url, archive)
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(root)


def _download(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "auto-research/0.1"})
    with urllib.request.urlopen(request, timeout=120) as response:
        target.write_bytes(response.read())
