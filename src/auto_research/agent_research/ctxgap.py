"""CTXGAP frozen-score reproduction and gold-isolated public-text interfaces.

Numerical conventions follow the authors' MIT reproduce_all.py. This module
does not run a coding agent, expose private reasoning, or generate model scores.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import csv
import hashlib
import io
import json
import math
from numbers import Real
from pathlib import Path
import random
from typing import Callable, Mapping, Sequence
from urllib.request import urlopen

REVISION = "04d8c618238923c1e797b9b154b977091222c1a2"
REPOSITORY = "https://github.com/Kaguraaaaaa/Ctxgap"
FILE_HASHES = {
    "data/anon/main37_units.csv": "920b345138bfa8a5ca6712f333677de4b36fd6d74f679e84497d156e8230568e",
    "data/anon/e2_units.csv": "64bfcc685956c1b582cbf8c83f8c7f10dfc78d6be3c6ebd4722d0ce7a07b44a3",
    "data/anon/cross_harness_units.csv": "a19811ac734de97cbc09aaee9e0daf1993fa4c444f1a713820e88bcf4a576e12",
    "data/anon/task_success.csv": "fee5deed1fe9d29db706752f8a7ecc8c1acd851b5c251e7eae5bc3f87c654a14",
    "data/reproduced_all.json": "93832f4b9d12e3f4612d9713e84e8fa02e1e8a5d1a07b64f236627df6e3cfd09",
}
HEADERS = {
    "main37_units.csv": ("run", "k", "qid", "category", "importance", "w", "valid", "acc_U", "acc_T_full", "acc_agent", "acc_prior"),
    "cross_harness_units.csv": ("harness", "run", "task", "k", "qid", "category", "w", "valid", "acc_U", "acc_T_full"),
    "e2_units.csv": ("run", "k", "arm", "qid", "w", "valid", "score"),
    "task_success.csv": ("run", "fixed_k4", "regression_k4", "resolved_k4"),
}
LABEL_SCORES = {"correct": 1.0, "partial": 0.5, "wrong": 0.0, "unknown": 0.0}
MAX_BYTES = 2 * 1024 * 1024


class ProtocolError(ValueError):
    """An input violates identity, scoring or evidence boundaries."""


def _number(value: object, *, score: bool = False) -> float:
    if isinstance(value, bool):
        raise ProtocolError("boolean is not a numeric score/weight")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ProtocolError("expected a finite number") from error
    if not math.isfinite(result) or (score and not 0 <= result <= 1):
        raise ProtocolError("invalid finite score")
    return result


def _finite_sum(values, *, name: str) -> float:
    try:
        total = math.fsum(values)
    except OverflowError as error:
        raise ProtocolError(f"{name} must have a finite total") from error
    if not math.isfinite(total):
        raise ProtocolError(f"{name} must have a finite total")
    return total


def _bounded_cache(path: Path, relative: str) -> bytes:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ProtocolError(f"invalid bounded input: {relative}")
    with path.open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ProtocolError(f"invalid bounded input: {relative}")
    return data


def fetch_release(directory: Path) -> dict:
    """Explicitly fetch about 1.65 MB of fixed numeric tables, never trajectories."""
    for relative, expected in FILE_HASHES.items():
        target = directory / relative
        if any(p.is_symlink() for p in (target, *target.parents)):
            raise ProtocolError("release paths must not contain symlinks")
        if target.exists():
            data = _bounded_cache(target, relative)
        else:
            url = f"https://raw.githubusercontent.com/Kaguraaaaaa/Ctxgap/{REVISION}/{relative}"
            with urlopen(url, timeout=30) as response:
                data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES or hashlib.sha256(data).hexdigest() != expected:
            raise ProtocolError(f"pinned source mismatch: {relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            with target.open("xb") as handle:
                handle.write(data)
    return {"revision": REVISION, "files": dict(FILE_HASHES), "models_called": False}


def _verified(directory: Path, relative: str) -> bytes:
    path = directory / relative
    data = _bounded_cache(path, relative)
    if hashlib.sha256(data).hexdigest() != FILE_HASHES[relative]:
        raise ProtocolError(f"pinned source mismatch: {relative}")
    return data


def _csv_rows(data: bytes, filename: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(data.decode("utf-8")), strict=True)
    if tuple(reader.fieldnames or ()) != HEADERS[filename]:
        raise ProtocolError(f"unexpected columns: {filename}")
    rows, seen = [], set()
    for raw in reader:
        if None in raw or any(v is None for v in raw.values()):
            raise ProtocolError("malformed CSV row")
        identity = tuple(raw.get(k, "") for k in ("harness", "run", "k", "qid", "arm"))
        if identity in seen or not raw["run"]:
            raise ProtocolError("duplicate or missing probe/run identity")
        seen.add(identity)
        row = dict(raw)
        if filename == "task_success.csv":
            if any(raw[k] not in {"0", "1"} for k in HEADERS[filename][1:]):
                raise ProtocolError("success flags must be 0/1")
        else:
            if raw["valid"] not in {"0", "1"} or raw["k"] not in {"1", "2", "3", "4"}:
                raise ProtocolError("invalid validity/checkpoint")
            row["w"] = _number(raw["w"])
            if row["w"] < 0:
                raise ProtocolError("weight must be nonnegative; zero-weight categories are retained")
            for key in ("acc_U", "acc_T_full", "acc_agent", "acc_prior", "score"):
                if key in raw:
                    row[key] = _number(raw[key], score=True)
            if "arm" in raw and raw["arm"] not in {"A", "B", "C"}:
                raise ProtocolError("unknown rewrite arm")
        rows.append(row)
    if not rows:
        raise ProtocolError("empty score table")
    return rows


def weighted_mean(rows: Sequence[Mapping], key: str) -> float:
    if not rows:
        raise ProtocolError("cannot average an empty probe set")
    weights = [_number(r["w"]) for r in rows]
    if any(w < 0 for w in weights):
        raise ProtocolError("weights must be nonnegative")
    den = _finite_sum(weights, name="weights")
    if den <= 0:
        raise ProtocolError("positive total weight required")
    return _finite_sum((_number(r["w"]) * _number(r[key], score=True) for r in rows), name="weighted scores") / den


def clustered_interval(rows: Sequence[Mapping], first: str, second: str | None = None,
                       *, group: str = "run", draws: int = 10000, seed: int = 0,
                       task_equal: bool = False) -> list[float] | None:
    """Paper's task-cluster percentile bootstrap; no probe-wise resampling."""
    if isinstance(draws, bool) or not isinstance(draws, int) or draws < 40:
        raise ProtocolError("bootstrap requires at least 40 draws")
    by = defaultdict(list)
    for row in rows:
        by[str(row[group])].append(row)
    keys = sorted(by)
    stats = {}
    for key in keys:
        part = by[key]
        weights = [_number(r["w"]) for r in part]
        if any(w < 0 for w in weights):
            raise ProtocolError("cluster weights must be nonnegative")
        den = _finite_sum(weights, name="cluster weights")
        if den <= 0:
            raise ProtocolError("every bootstrap cluster must have positive total weight; zero-mass clusters are not silently dropped")
        diff = _finite_sum((w * (_number(r[first], score=True) - (_number(r[second], score=True) if second else 0))
                            for w, r in zip(weights, part, strict=True)), name="cluster weighted scores")
        stats[key] = (diff / den, 1.0) if task_equal else (diff, den)
    if len(keys) < 2:
        return None
    rng, values = random.Random(seed), []
    for _ in range(draws):
        picks = [keys[rng.randrange(len(keys))] for _ in keys]
        values.append(_finite_sum((stats[k][0] for k in picks), name="bootstrap numerator") /
                      _finite_sum((stats[k][1] for k in picks), name="bootstrap denominator"))
    values.sort()
    return [round(values[int(.025 * draws)], 6), round(values[int(.975 * draws) - 1], 6)]


def reproduce_tables(main: Sequence[Mapping], success: Sequence[Mapping],
                     cross: Sequence[Mapping], rewrite: Sequence[Mapping], *, draws: int = 10000) -> dict:
    valid = [r for r in main if r["valid"] == "1"]
    u, t = weighted_mean(valid, "acc_U"), weighted_mean(valid, "acc_T_full")
    result = {"main": {"n_valid_probes": len(valid), "n_tasks": len({r["run"] for r in valid}),
                         "acc_U": round(u, 6), "acc_T_full": round(t, 6),
                         "acc_actor": round(weighted_mean(valid, "acc_agent"), 6),
                         "gap": round(t-u, 6), "gap_ci95": clustered_interval(valid, "acc_T_full", "acc_U", draws=draws)}}
    fixed = {r["run"] for r in success if r["fixed_k4"] == "1"}
    if fixed - {r["run"] for r in main}:
        raise ProtocolError("successful-task IDs absent from main table")
    part = [r for r in valid if r["run"] in fixed and r["k"] == "4"]
    if part:
        u, t = weighted_mean(part, "acc_U"), weighted_mean(part, "acc_T_full")
        result["successful_tasks_k4"] = {"n_tasks": len(fixed), "n_probes": len(part),
                                         "acc_U": round(u, 6), "acc_T_full": round(t, 6), "gap": round(t-u, 6),
                                         "gap_ci95": clustered_interval(part, "acc_T_full", "acc_U", draws=draws)}
    result["cross_harness"] = {}
    for harness in sorted({r["harness"] for r in cross}):
        part = [r for r in cross if r["valid"] == "1" and r["harness"] == harness]
        if not part:
            raise ProtocolError("harness has no valid probes")
        tasks = sorted({r["task"] for r in part})
        gaps = [weighted_mean([r for r in part if r["task"] == task], "acc_T_full") -
                weighted_mean([r for r in part if r["task"] == task], "acc_U") for task in tasks]
        result["cross_harness"][harness] = {"n_probes": len(part), "n_tasks": len(tasks),
            "acc_U_pooled": round(weighted_mean(part, "acc_U"), 6),
            "acc_T_full_pooled": round(weighted_mean(part, "acc_T_full"), 6),
            "gap_task_equal": round(math.fsum(gaps)/len(gaps), 6),
            "gap_ci95": clustered_interval(part, "acc_T_full", "acc_U", group="task", draws=draws, task_equal=True)}
    pivot = defaultdict(dict)
    for row in rewrite:
        if row["valid"] == "1":
            key = (row["run"], row["k"], row["qid"])
            if pivot[key] and any(r["w"] != row["w"] for r in pivot[key].values()):
                raise ProtocolError("paired rewrite weights differ")
            if row["arm"] in pivot[key]:
                raise ProtocolError("duplicate rewrite arm")
            pivot[key][row["arm"]] = row
    paired = [{"run": key[0], "w": rows["A"]["w"], **{a: rows[a]["score"] for a in "ABC"}}
              for key, rows in pivot.items() if set(rows) == set("ABC")]
    if paired:
        acc = {a: weighted_mean(paired, a) for a in "ABC"}
        result["e2"] = {"n_probes": len(paired), "acc": {a: round(v, 6) for a, v in acc.items()}}
        for x, y in (("B", "A"), ("C", "A"), ("C", "B")):
            result["e2"][f"{x}-{y}"] = {"diff": round(acc[x]-acc[y], 6),
                "ci95": clustered_interval(paired, x, y, draws=draws)}
    return result


def reproduce_release(directory: Path, *, draws: int = 10000) -> dict:
    tables = [_csv_rows(_verified(directory, f"data/anon/{name}"), name) for name in HEADERS]
    main, cross, rewrite, success = tables
    result = reproduce_tables(main, success, cross, rewrite, draws=draws)
    expected = json.loads(_verified(directory, "data/reproduced_all.json"))
    reference_matches = result == expected if draws == 10000 else None
    if reference_matches is False:
        raise ProtocolError("frozen numeric reproduction differs from the pinned author's output")
    return {"schema_version": 2, "method": "ctxgap", "kind": "frozen_score_reproduction",
            "upstream_revision": REVISION, "input_sha256": dict(FILE_HASHES), "metrics": result,
            "bootstrap": {"group": "task/run", "seed": 0, "draws": draws, "paired": True},
            "reference_matches": reference_matches, "models_called": False,
            "local_capability_score": None, "diagnostic_only": True, "promotion_eligible": False,
            "full_experiment_status": "not_reproduced_high_cost"}


@dataclass(frozen=True)
class PublicProbe:
    probe_id: str
    unit_id: str
    question: str
    public_view: str
    reference: str
    weight: float

    def __post_init__(self):
        if not all(isinstance(v, str) and v.strip() for v in
                   (self.probe_id, self.unit_id, self.question, self.public_view, self.reference)):
            raise ProtocolError("public probe requires nonempty identities, question, view and scorer reference")
        if isinstance(self.weight, bool) or not isinstance(self.weight, Real):
            raise ProtocolError("probe weight must be a finite real number, not a string/boolean")
        weight = _number(self.weight)
        if weight < 0:
            raise ProtocolError("probe weight must be nonnegative")
        object.__setattr__(self, "weight", weight)


def validate_public_plan(probes: Sequence[PublicProbe]) -> None:
    """Preflight the entire planned denominator before export or external calls."""
    if not probes or any(not isinstance(p, PublicProbe) for p in probes):
        raise ProtocolError("planned probes must be a nonempty sequence of PublicProbe")
    if len({p.probe_id for p in probes}) != len(probes):
        raise ProtocolError("planned probe IDs must be unique")
    for probe in probes:
        probe.__post_init__()
    if _finite_sum((p.weight for p in probes), name="planned probe weights") <= 0:
        raise ProtocolError("planned probes require positive total weight")


def observer_input(probe: PublicProbe) -> dict:
    """Allow-list view: no gold, reference, cached verdict, importance or hidden context."""
    return {"probe_id": probe.probe_id, "unit_id": probe.unit_id,
            "question": probe.question, "view": probe.public_view, "condition": "U_public"}


def score_public_labels(probes: Sequence[PublicProbe], labels: Mapping[str, str]) -> dict:
    validate_public_plan(probes)
    by_id = {p.probe_id: p for p in probes}
    if not isinstance(labels, Mapping) or set(labels) - set(by_id) or any(
            not isinstance(label, str) or label not in LABEL_SCORES for label in labels.values()):
        raise ProtocolError("unknown probe or judge label")
    den = math.fsum(p.weight for p in probes)
    observed_den = math.fsum(by_id[k].weight for k in labels)
    numerator = math.fsum(by_id[k].weight * LABEL_SCORES[v] for k, v in labels.items())
    return {"kind": "new_public_text_measurement", "condition": "U_public", "planned": len(probes),
            "scored": len(labels), "coverage": len(labels)/len(probes),
            "acc_U_public_on_scored": numerator/observed_den if observed_den else None,
            "intention_to_evaluate_accuracy": numerator/den,
            "gap_view": None, "T_full_available": False, "frozen_score_reproduction": False,
            "diagnostic_only": True, "promotion_eligible": False}


def evaluate_public(probes: Sequence[PublicProbe], observer: Callable[[dict], str],
                    judge: Callable[[dict], str]) -> dict:
    """User-supplied real observer/judge; failed calls remain in planned coverage."""
    validate_public_plan(probes)
    if not callable(observer) or not callable(judge):
        raise ProtocolError("observer and judge must be callable")
    labels, failures = {}, []
    for probe in probes:
        try:
            answer = observer(observer_input(probe))
            if not isinstance(answer, str) or not answer.strip():
                raise ProtocolError("empty/non-text observer answer")
            label = judge({"probe_id": probe.probe_id, "question": probe.question,
                           "answer": answer, "reference": probe.reference})
            if label not in LABEL_SCORES:
                raise ProtocolError("invalid judge label")
            labels[probe.probe_id] = label
        except Exception as error:
            failures.append({"probe_id": probe.probe_id, "error_type": type(error).__name__})
    return {**score_public_labels(probes, labels), "labels": labels, "failures": failures}
