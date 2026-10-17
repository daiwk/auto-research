"""ARIA's structured cut-and-continuation interface, without a learned gate.

Schema validity is not causal attribution or proof that a repair succeeds.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Event:
    event_id: str
    role: str
    kind: str
    content: str


@dataclass(frozen=True)
class RepairPatch:
    diagnosis: str
    cut_event_id: str | None
    replacement: tuple[Event, ...]


def apply_repair(events, patch: RepairPatch, *, first_bad_event_id: str | None = None):
    """Retain the cut event; discard its suffix; never forge tool observations."""
    original = tuple(events)
    ids = [e.event_id for e in original]
    if not ids or len(set(ids)) != len(ids) or any(not i for i in ids):
        raise ValueError("unique source event IDs required")
    if not patch.diagnosis.strip() or not 1 <= len(patch.replacement) <= 8:
        raise ValueError("diagnosis and one to eight replacement events required")
    if patch.cut_event_id is not None and patch.cut_event_id not in ids:
        raise ValueError("cut must reference an observed event")
    count = 0 if patch.cut_event_id is None else ids.index(patch.cut_event_id) + 1
    if first_bad_event_id is not None:
        if first_bad_event_id not in ids or count > ids.index(first_bad_event_id):
            raise ValueError("cut must precede the localized bad event")
    replacement_ids = [e.event_id for e in patch.replacement]
    if (len(set(replacement_ids)) != len(replacement_ids) or any(not i for i in replacement_ids)
            or set(replacement_ids) & set(ids[:count])):
        raise ValueError("replacement IDs collide with retained prefix")
    if any(e.role == "tool" or e.kind in {"tool_result", "observation"} for e in patch.replacement):
        raise ValueError("model cannot fabricate tool-result observations")
    if any(e.role != "assistant" or e.kind not in {"message", "tool_call"} for e in patch.replacement):
        raise ValueError("only assistant messages or executable tool requests are allowed")
    if len(json.dumps(asdict(patch), sort_keys=True)) > 12000:
        raise ValueError("patch exceeds the canonical character budget")
    old = [(e.role, e.kind, e.content) for e in original[count:]]
    new = [(e.role, e.kind, e.content) for e in patch.replacement]
    if old == new:
        raise ValueError("replacement cannot merely rename the discarded suffix")
    return original[:count] + patch.replacement


def verified_repair(*, fresh_control_passed: bool, patched_execution_passed: bool) -> bool:
    """Training admission uses fresh paired executions, not a model vote."""
    if type(fresh_control_passed) is not bool or type(patched_execution_passed) is not bool:
        raise ValueError("explicit verified execution verdicts required")
    return not fresh_control_passed and patched_execution_passed
