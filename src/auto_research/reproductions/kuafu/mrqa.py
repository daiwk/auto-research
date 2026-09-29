"""Strict loader for the official MRQA 2019 public JSONL.GZ format."""

from __future__ import annotations

from dataclasses import dataclass
import gzip
import json
from pathlib import Path
import re
from typing import Sequence


@dataclass(frozen=True)
class MRQAExample:
    qid: str
    items: tuple[str, ...]
    question: str
    answers: tuple[str, ...]


def _context_items(context: str, max_words: int) -> tuple[str, ...]:
    if max_words < 1:
        raise ValueError("max_words must be positive")
    parts = re.split(r"\[(?:PAR|DOC|TLE)\]", context)
    items = []
    for part in parts:
        words = part.split()
        for start in range(0, len(words), max_words):
            items.append(" ".join(words[start:start + max_words]))
    return tuple(items)


def load_mrqa(path: Path, *, expected_split: str, limit: int | None = None,
              max_words_per_item: int = 96,
              one_per_context: bool = False) -> list[MRQAExample]:
    """No implicit download, split conversion, or generated gold answers."""
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive")
    records: list[MRQAExample] = []
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        header = json.loads(next(stream))
        actual = header.get("header", {}).get("split")
        if actual != expected_split:
            raise ValueError(f"MRQA split mismatch: expected {expected_split}, got {actual}")
        for line in stream:
            row = json.loads(line)
            items = _context_items(row["context"], max_words_per_item)
            if not items:
                continue
            for qa in row["qas"]:
                answers = tuple(str(value) for value in qa["answers"] if str(value).strip())
                if not answers:
                    continue
                records.append(MRQAExample(str(qa["qid"]), items,
                                           str(qa["question"]), answers))
                if limit is not None and len(records) >= limit:
                    return records
                if one_per_context:
                    break
    return records


def validate_disjoint_qids(*splits: Sequence[MRQAExample]) -> None:
    seen: set[str] = set()
    for split in splits:
        ids = {example.qid for example in split}
        if len(ids) != len(split) or ids & seen:
            raise ValueError("MRQA question overlap between or within splits")
        seen.update(ids)
