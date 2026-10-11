"""Safe public-log parsing and instance-disjoint OnTrack calibration helpers.

Commands are text only: this module never executes trajectory tool calls.
Resolution and exit-status fields are intentionally not read by parse_trace.
"""
from __future__ import annotations

import json
import re
from pathlib import PurePosixPath

import numpy as np

from .ontrack import Event


def instance_id(filename):
    match = re.search(r"([\w.-]+__[\w.-]+-\d+)", str(filename))
    if not match:
        raise ValueError("SWE-bench instance ID absent from filename")
    return match.group(1)


def partition_instances(ids, *, seed=42, calibration=64, reference_pool=32):
    unique = sorted(set(ids))
    if min(calibration, reference_pool) < 1 or len(unique) <= calibration + reference_pool:
        raise ValueError("disjoint nonempty instance partitions required")
    rng = np.random.default_rng(seed)
    rng.shuffle(unique)
    return {"calibration": unique[:calibration],
            "reference_pool": unique[calibration:calibration + reference_pool],
            "evaluation": unique[calibration + reference_pool:]}


def _path(value):
    value = value.strip("\"'[](),:;")
    value = re.sub(r"^/[\w.-]+__[\w.-]+/", "", value)
    return str(PurePosixPath(value)) if value and value != "n/a" else None


def _paths(text):
    # Deterministic identifiers only; no dynamic shell resolution or LLM
    # guesses. These heuristics cannot reconstruct every hidden dependency.
    return {_path(x) for x in re.findall(r"(?:[\w.-]+/)*[\w.-]+\.(?:py|json|yaml|yml|toml|txt|md|cfg|ini|rst|c|h|js)\b", text)} - {None}


def parse_trace(row, *, maximum_steps=None):
    trajectory = row["trajectory"]
    if isinstance(trajectory, str):
        trajectory = json.loads(trajectory)
    if not isinstance(trajectory, list) or not trajectory:
        raise ValueError("nonempty public trajectory list required")
    events = []
    for item in trajectory[:maximum_steps]:
        if not isinstance(item, dict) or not isinstance(item.get("action"), str):
            raise ValueError("malformed public action")
        action = item["action"].replace("\\n", "\n").replace('\\"', '"')
        tokens = action.split(maxsplit=1)
        if not tokens:
            continue
        tool = tokens[0]
        args = tokens[1] if len(tokens) > 1 else ""
        effect = str(item.get("observation", ""))
        state = item.get("state", {})
        if isinstance(state, str):
            try:
                state = json.loads(state.replace('\\"', '"'))
            except (ValueError, TypeError):
                state = {}
        current = _path(str(state.get("open_file", "n/a"))) if isinstance(state, dict) else None
        consumed = _paths(action)
        if tool in {"edit", "scroll_down", "scroll_up", "goto"} and current:
            consumed.add(current)
        produced = _paths(effect)
        if tool in {"open", "edit"} and current:
            produced.add(current)
        # Explicit tool errors, not task outcomes or hidden evaluation labels.
        errored = bool(re.match(r"\s*(?:Error:|ERROR\b|Traceback \(most recent call last\))", effect))
        events.append(Event(str(item.get("thought") or tool), tool, args, effect,
                            consumes=tuple(sorted(consumed)), produces=tuple(sorted(produced)), errored=errored))
    if not events:
        raise ValueError("no usable events")
    return tuple(events)


def auc(labels, scores):
    labels, scores = np.asarray(labels, dtype=bool), np.asarray(scores, dtype=float)
    if labels.shape != scores.shape or labels.ndim != 1 or not np.isfinite(scores).all():
        raise ValueError("finite aligned scalar scores required")
    positive, negative = scores[labels], scores[~labels]
    if not len(positive) or not len(negative):
        return None
    return float(((positive[:, None] > negative).sum() + .5 * (positive[:, None] == negative).sum()) /
                 (len(positive) * len(negative)))


def paired_auc_interval(labels, left, right, *, seed=42, draws=1000):
    rng = np.random.default_rng(seed)
    labels, left, right = map(np.asarray, (labels, left, right))
    differences = []
    for _ in range(draws):
        indices = rng.integers(0, len(labels), len(labels))
        a, b = auc(labels[indices], left[indices]), auc(labels[indices], right[indices])
        if a is not None and b is not None:
            differences.append(a - b)
    return None if not differences else np.quantile(differences, [.025, .975]).tolist()
