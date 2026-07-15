from __future__ import annotations

import ast
import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PGExample:
    user_id: str
    history_ids: tuple[int, ...]
    history_sids: tuple[str, ...]
    history_titles: tuple[str, ...]
    target_id: int
    target_sid: str


@dataclass(frozen=True)
class PGDataset:
    train: tuple[PGExample, ...]
    validation: tuple[PGExample, ...]
    test: tuple[PGExample, ...]
    items: dict[int, dict[str, str]]
    item_sids: dict[int, str]
    source: Path


def locate_office_dataset(root: Path) -> Path:
    candidates = (
        root / "minionerec-public" / "Amazon",
        root / "MiniOneRec" / "Amazon",
        root / "prompt-generation" / "Amazon",
    )
    for candidate in candidates:
        if (candidate / "train" / _filename("train")).exists():
            return candidate
    raise RuntimeError(
        "Prompt Generation needs the MiniOneRec Amazon Office data. Download "
        "https://huggingface.co/kkknight/MiniOneRec into data/minionerec-public."
    )


def load_office_dataset(root: Path, train_limit: int | None = None) -> PGDataset:
    source = locate_office_dataset(root)
    items_raw = json.loads(
        (source / "index" / "Office_Products.item.json").read_text(encoding="utf-8")
    )
    sid_raw = json.loads(
        (source / "index" / "Office_Products.index.json").read_text(encoding="utf-8")
    )
    items = {int(key): value for key, value in items_raw.items()}
    item_sids = {int(key): "".join(value) for key, value in sid_raw.items()}
    return PGDataset(
        train=_read(source / "train" / _filename("train"), train_limit),
        validation=_read(source / "valid" / _filename("valid"), None),
        test=_read(source / "test" / _filename("test"), None),
        items=items,
        item_sids=item_sids,
        source=source,
    )


def _filename(_: str) -> str:
    return "Office_Products_5_2016-10-2018-11.csv"


def _read(path: Path, limit: int | None) -> tuple[PGExample, ...]:
    rows: list[PGExample] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                PGExample(
                    user_id=row["user_id"],
                    history_ids=tuple(int(value) for value in ast.literal_eval(row["history_item_id"])),
                    history_sids=tuple(ast.literal_eval(row["history_item_sid"])),
                    history_titles=tuple(ast.literal_eval(row["history_item_title"])),
                    target_id=int(row["item_id"]),
                    target_sid=row["item_sid"],
                )
            )
            if limit is not None and len(rows) >= limit:
                break
    return tuple(rows)

