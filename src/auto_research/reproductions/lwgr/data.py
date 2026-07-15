from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..prompt_generation.data import PGExample, load_office_dataset


SID = re.compile(r"<([abc])_(\d+)>")


@dataclass(frozen=True)
class LWGRData:
    train: tuple[tuple[tuple[int, ...], int], ...]
    validation: tuple[tuple[tuple[int, ...], int], ...]
    test: tuple[tuple[tuple[int, ...], int], ...]
    codes: np.ndarray
    titles: tuple[str, ...]
    source: Path


def load_lwgr_data(root: Path, train_rows: int, eval_users: int, seed: int) -> LWGRData:
    raw = load_office_dataset(root, train_limit=train_rows)
    codes = np.zeros((len(raw.items), 3), dtype=np.int64)
    for item, value in raw.item_sids.items():
        parsed = {level: int(token) for level, token in SID.findall(value)}
        codes[item] = parsed["a"], parsed["b"], parsed["c"]
    return LWGRData(
        train=tuple((_history(row), row.target_id) for row in raw.train),
        validation=_select(raw.validation, eval_users, seed),
        test=_select(raw.test, eval_users, seed + 1),
        codes=codes,
        titles=tuple(str(raw.items[item].get("title", "")) for item in range(len(raw.items))),
        source=raw.source,
    )


def _select(rows, count, seed):
    ordered = sorted(
        rows,
        key=lambda row: hashlib.sha256(
            f"{seed}:{row.user_id}:{row.target_id}".encode()
        ).digest(),
    )
    return tuple((_history(row), row.target_id) for row in ordered[:count])


def _history(row: PGExample) -> tuple[int, ...]:
    return row.history_ids[-12:]
