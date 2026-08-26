from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any


SCHEMA_VERSION = 1
ARTIFACT_NAMES = {"metrics.json", "result.json", "matrix.json"}


@dataclass(frozen=True)
class ExperimentRow:
    artifact_id: str
    path: str
    domain: str
    method: str
    dataset: str
    seed: str
    created_at: str
    metrics: dict[str, float]


def _flatten_numbers(value: Any, prefix: str = "") -> dict[str, float]:
    result: dict[str, float] = {}
    if isinstance(value, bool):
        return result
    if isinstance(value, (int, float)):
        if prefix:
            result[prefix] = float(value)
        return result
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            result.update(_flatten_numbers(child, child_prefix))
    return result


def _domain_for(path: Path) -> str:
    parts = set(path.parts)
    if "post-training" in parts:
        return "post-training"
    if "agent-research" in parts:
        return "agent"
    if "multimodal-models" in parts:
        return "multimodal"
    if "foundation-models" in parts:
        return "foundation-model"
    if "reproductions" in parts:
        return "recommendation"
    if "evolution" in parts:
        return "evolution"
    return "general"


def _first(payload: dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value: Any = payload
        for part in key.split("."):
            if not isinstance(value, dict):
                value = None
                break
            value = value.get(part)
        if value not in (None, "", []):
            return str(value)
    return default


def _method_for(payload: dict[str, Any], path: Path) -> str:
    declared = _first(
        payload, "method", "adapter", "paper.adapter", "config.algorithm", "config.model",
    )
    if declared:
        return declared
    if path.parent.name == "metrics":
        container = path.parent.parent.name
        if container in {
            "docs", "experiments", "multimodal-models", "foundation-models",
            "post-training", "agent-research", "reproductions",
        }:
            return path.stem
        return container
    return path.parent.name


class ExperimentStore:
    """Idempotent SQLite index over committed and local experiment artifacts."""

    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY, value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS experiments (
                artifact_id TEXT PRIMARY KEY,
                path TEXT NOT NULL UNIQUE,
                content_hash TEXT NOT NULL,
                domain TEXT NOT NULL,
                method TEXT NOT NULL,
                dataset TEXT NOT NULL,
                seed TEXT NOT NULL,
                created_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS metrics (
                artifact_id TEXT NOT NULL,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                PRIMARY KEY (artifact_id, name),
                FOREIGN KEY (artifact_id) REFERENCES experiments(artifact_id)
                    ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS experiment_dimensions
                ON experiments(domain, method, dataset, created_at);
            CREATE INDEX IF NOT EXISTS metric_names ON metrics(name, value);
            """
        )
        self.connection.execute(
            "INSERT OR REPLACE INTO metadata(key, value) VALUES('schema_version', ?)",
            (str(SCHEMA_VERSION),),
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> ExperimentStore:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def import_artifact(self, path: Path, *, root: Path | None = None) -> str:
        raw = path.read_bytes()
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError(f"experiment artifact must be a JSON object: {path}")
        content_hash = hashlib.sha256(raw).hexdigest()
        try:
            relative = path.resolve().relative_to((root or Path.cwd()).resolve())
        except ValueError:
            relative = path.resolve()
        logical_path = relative.as_posix()
        artifact_id = hashlib.sha256(logical_path.encode()).hexdigest()[:20]
        domain = _first(payload, "domain", "track", "config.model") or _domain_for(relative)
        method = _method_for(payload, path)
        dataset = _first(payload, "dataset", "config.dataset", "protocol.dataset")
        seed = _first(payload, "seed", "config.seed", "seeds")
        created_at = _first(
            payload, "created_at", "timestamp", "run_id", default=path.stat().st_mtime_ns,
        )
        metrics = _flatten_numbers(payload.get("metrics", payload))
        with self.connection:
            self.connection.execute(
                """INSERT INTO experiments(
                    artifact_id, path, content_hash, domain, method, dataset, seed,
                    created_at, payload_json
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    artifact_id=excluded.artifact_id,
                    content_hash=excluded.content_hash,
                    domain=excluded.domain,
                    method=excluded.method,
                    dataset=excluded.dataset,
                    seed=excluded.seed,
                    created_at=excluded.created_at,
                    payload_json=excluded.payload_json""",
                (
                    artifact_id, logical_path, content_hash, domain, method, dataset,
                    seed, created_at, json.dumps(payload, ensure_ascii=False),
                ),
            )
            self.connection.execute("DELETE FROM metrics WHERE artifact_id = ?", (artifact_id,))
            self.connection.executemany(
                "INSERT INTO metrics(artifact_id, name, value) VALUES(?, ?, ?)",
                ((artifact_id, name, value) for name, value in sorted(metrics.items())),
            )
        return artifact_id

    def rows(
        self, *, domain: str | None = None, method: str | None = None,
        dataset: str | None = None, metric: str | None = None,
    ) -> list[ExperimentRow]:
        clauses: list[str] = []
        values: list[str] = []
        for column, value in (("domain", domain), ("method", method), ("dataset", dataset)):
            if value:
                clauses.append(f"e.{column} = ?")
                values.append(value)
        if metric:
            clauses.append("EXISTS (SELECT 1 FROM metrics x WHERE x.artifact_id=e.artifact_id AND x.name=?)")
            values.append(metric)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        records = self.connection.execute(
            f"SELECT e.* FROM experiments e {where} ORDER BY e.created_at DESC, e.path", values
        ).fetchall()
        result = []
        for record in records:
            metrics = {
                row["name"]: row["value"] for row in self.connection.execute(
                    "SELECT name, value FROM metrics WHERE artifact_id=? ORDER BY name",
                    (record["artifact_id"],),
                )
            }
            result.append(ExperimentRow(
                artifact_id=record["artifact_id"], path=record["path"],
                domain=record["domain"], method=record["method"],
                dataset=record["dataset"], seed=record["seed"],
                created_at=record["created_at"], metrics=metrics,
            ))
        return result

    def pareto_frontier(
        self, x_metric: str, y_metric: str, *, minimize_x: bool = True,
        minimize_y: bool = False,
    ) -> list[ExperimentRow]:
        candidates = [
            row for row in self.rows()
            if x_metric in row.metrics and y_metric in row.metrics
        ]
        frontier = []
        for candidate in candidates:
            x, y = candidate.metrics[x_metric], candidate.metrics[y_metric]
            dominated = False
            for other in candidates:
                if other is candidate:
                    continue
                ox, oy = other.metrics[x_metric], other.metrics[y_metric]
                x_better = ox <= x if minimize_x else ox >= x
                y_better = oy <= y if minimize_y else oy >= y
                x_strict = ox < x if minimize_x else ox > x
                y_strict = oy < y if minimize_y else oy > y
                if x_better and y_better and (x_strict or y_strict):
                    dominated = True
                    break
            if not dominated:
                frontier.append(candidate)
        return frontier


def discover_artifacts(roots: Iterable[Path]) -> list[tuple[Path, Path]]:
    discovered: dict[Path, Path] = {}
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            if path.name in ARTIFACT_NAMES or path.parent.name == "metrics":
                discovered[path.resolve()] = root.parent.resolve() if root.name == "docs" else root.resolve()
    return sorted(discovered.items())


def sync_experiments(database: Path, roots: Iterable[Path]) -> tuple[int, int]:
    imported = failed = 0
    with ExperimentStore(database) as store:
        for path, root in discover_artifacts(roots):
            try:
                store.import_artifact(path, root=root)
                imported += 1
            except (OSError, ValueError, json.JSONDecodeError):
                failed += 1
    return imported, failed
