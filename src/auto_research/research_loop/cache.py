from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from ..models import Trial


class TrialCache:
    """Content-addressed cache for completed experiment trials.

    The cache deliberately stores metrics only. Model checkpoints and datasets remain
    owned by the experiment implementation and are never copied into the research log.
    """

    SCHEMA_VERSION = 1

    def __init__(self, root: Path):
        self.root = root

    @staticmethod
    def fingerprint(context: dict[str, Any], params: dict[str, Any]) -> str:
        payload = json.dumps(
            {"schema": TrialCache.SCHEMA_VERSION, "context": context, "params": params},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def load(
        self, context: dict[str, Any], params: dict[str, Any], number: int
    ) -> Trial | None:
        path = self._path(context, params)
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload.get("schema_version") != self.SCHEMA_VERSION:
                return None
            return Trial(
                number=number,
                params=params,
                metric=float(payload["metric"]),
                status="cached",
                duration_seconds=0.0,
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError, OSError):
            return None

    def save(self, context: dict[str, Any], trial: Trial) -> Path:
        if trial.metric is None:
            raise ValueError("only completed trials can be cached")
        path = self._path(context, trial.params)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": self.SCHEMA_VERSION,
            "metric": trial.metric,
            "params": trial.params,
        }
        _atomic_write_json(path, payload)
        return path

    def _path(self, context: dict[str, Any], params: dict[str, Any]) -> Path:
        digest = self.fingerprint(context, params)
        track = _safe_component(str(context.get("track", "unknown")))
        experiment = _safe_component(str(context.get("experiment", "default")))
        return self.root / track / experiment / f"{digest}.json"


def _safe_component(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "-_." else "-" for char in value)
    return cleaned.strip("-.")[:80] or "unknown"


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(f"{path.suffix}.tmp-{os.getpid()}")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)
