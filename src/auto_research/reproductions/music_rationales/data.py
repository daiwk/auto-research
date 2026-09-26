"""Non-commercial HetRec Last.fm 2K artist interaction and tag data."""

from __future__ import annotations

import csv
import hashlib
import io
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from auto_research.datasets import _download


SOURCE = "https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip"
SHA256 = "6738f48195667ff03caaab4d32ca9a3133d8cc026b7c3cdaf6ce1010e913c59c"


@dataclass(frozen=True)
class Artist:
    id: int
    name: str
    tags: tuple[str, ...]


@dataclass(frozen=True)
class MusicData:
    artists: dict[int, Artist]
    train: dict[int, frozenset[int]]
    validation: dict[int, frozenset[int]]
    test: dict[int, frozenset[int]]
    total_interactions: int


def _read_tsv(archive: zipfile.ZipFile, name: str):
    with archive.open(name) as raw:
        # The official 2011 archive contains a few malformed legacy tag bytes.
        with io.TextIOWrapper(raw, encoding="utf-8", errors="replace") as stream:
            yield from csv.DictReader(stream, delimiter="\t")


def load_lastfm(root: Path, *, seed: int = 42,
                allow_network: bool = True) -> MusicData:
    target = root / "hetrec2011-lastfm-2k.zip"
    if not target.exists():
        if not allow_network:
            raise FileNotFoundError(f"official Last.fm archive missing: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        _download(SOURCE, target, expected_sha256=SHA256)
    if hashlib.sha256(target.read_bytes()).hexdigest() != SHA256:
        raise ValueError("Last.fm 2K archive checksum mismatch")
    with zipfile.ZipFile(target) as archive:
        names = {int(row["id"]): row["name"] for row in _read_tsv(archive, "artists.dat")}
        tags = {int(row["tagID"]): row["tagValue"]
                for row in _read_tsv(archive, "tags.dat")}
        tag_counts: dict[int, Counter[str]] = defaultdict(Counter)
        for row in _read_tsv(archive, "user_taggedartists.dat"):
            artist, tag = int(row["artistID"]), int(row["tagID"])
            if artist in names and tag in tags:
                tag_counts[artist][tags[tag]] += 1
        artists = {key: Artist(key, value, tuple(tag for tag, _ in tag_counts[key].most_common(5)))
                   for key, value in names.items()}
        interactions: dict[int, set[int]] = defaultdict(set)
        for row in _read_tsv(archive, "user_artists.dat"):
            artist = int(row["artistID"])
            if artist in artists:
                interactions[int(row["userID"])].add(artist)
    train, validation, test = {}, {}, {}
    for user, consumed in interactions.items():
        if len(consumed) < 10:
            continue
        ids = np.array(sorted(consumed))
        rng = np.random.default_rng(seed + user)
        rng.shuffle(ids)
        n_val = max(1, len(ids) // 10)
        n_test = max(1, len(ids) // 10)
        test[user] = frozenset(map(int, ids[:n_test]))
        validation[user] = frozenset(map(int, ids[n_test:n_test + n_val]))
        train[user] = frozenset(map(int, ids[n_test + n_val:]))
    return MusicData(artists, train, validation, test,
                     sum(map(len, interactions.values())))


def cf_candidates(data: MusicData, user: int, *, limit: int = 30) -> list[int]:
    """Find unknown artists using only the training interactions of other users."""
    history = data.train[user]
    popularity = Counter(item for artists in data.train.values() for item in artists)
    scores: Counter[int] = Counter()
    for other, consumed in data.train.items():
        if other == user:
            continue
        overlap = len(history & consumed)
        if overlap:
            for item in consumed - history:
                scores[item] += overlap / max(1, len(consumed))
    ranked = sorted(scores, key=lambda item: (-scores[item] / popularity[item] ** 0.5,
                                               -popularity[item], item))
    if len(ranked) < limit:
        ranked.extend(item for item, _ in popularity.most_common()
                      if item not in history and item not in scores)
    return ranked[:limit]
