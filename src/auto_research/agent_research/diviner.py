"""Diviner's bounded evidence and human-governance contracts, not an RCA agent.

No model, production telemetry, mitigation action or private incident is loaded.
The caller owns semantic entailment; structural admission is deliberately stricter
than treating every nonempty tool response as evidence.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
import math
from typing import Mapping


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    incident_id: str
    target: str
    window_start: float
    window_end: float
    available_at: float
    status: str
    source: str
    payload: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class InvestigationScope:
    incident_id: str
    target: str
    window_start: float
    window_end: float
    as_of: float


class EvidenceLedger:
    """Admit only point-in-time, target-matched, complete observations."""

    def __init__(self, scope: InvestigationScope):
        if (not scope.incident_id or not scope.target
                or not all(math.isfinite(x) for x in (
                    scope.window_start, scope.window_end, scope.as_of))
                or scope.window_start > scope.window_end or scope.window_end > scope.as_of):
            raise ValueError("valid point-in-time incident scope required")
        self.scope = scope
        self.observations: dict[str, Evidence] = {}
        self.rejected: dict[str, str] = {}
        self.hypotheses: dict[str, dict] = {}

    def admit(self, item: Evidence) -> bool:
        if not item.evidence_id or item.evidence_id in self.observations or item.evidence_id in self.rejected:
            raise ValueError("unique evidence identity required")
        reason = None
        if not all(math.isfinite(x) for x in (item.window_start, item.window_end, item.available_at)):
            reason = "nonfinite_time"
        elif item.incident_id != self.scope.incident_id or item.target != self.scope.target:
            reason = "scope_mismatch"
        elif (item.window_start < self.scope.window_start or item.window_end > self.scope.window_end
              or item.window_start > item.window_end):
            reason = "window_mismatch"
        elif item.available_at > self.scope.as_of:
            reason = "future_evidence"
        elif not item.source:
            reason = "missing_provenance"
        elif item.status not in {"data", "valid_empty"}:
            reason = "incomplete_or_failed_tool"
        if reason is not None:
            self.rejected[item.evidence_id] = reason
            return False
        self.observations[item.evidence_id] = deepcopy(item)
        return True

    def update_hypothesis(self, key: str, state: str, evidence_ids=()) -> None:
        ids = tuple(evidence_ids)
        if not key or state not in {"supported", "refuted", "unresolved"}:
            raise ValueError("identified three-state hypothesis required")
        if len(set(ids)) != len(ids) or any(i not in self.observations for i in ids):
            raise ValueError("hypothesis cites unadmitted evidence")
        if state != "unresolved" and not ids:
            raise ValueError("decisive hypotheses require evidence")
        if state == "supported" and any(self.observations[i].status == "valid_empty" for i in ids):
            raise ValueError("valid-empty supports absence/refutation, not a positive finding")
        self.hypotheses[key] = {"state": state, "evidence_ids": ids}


@dataclass(frozen=True)
class KnowledgeUpdate:
    artifact_id: str
    owner: str
    current_version: int
    candidate_version: int
    replay_passed: bool = False
    approved_by: str | None = None


def publish_update(update: KnowledgeUpdate) -> int:
    """No agent can self-authorize a durable operational-knowledge update."""
    if (not update.artifact_id or not update.owner or update.current_version < 0
            or update.candidate_version != update.current_version + 1):
        raise ValueError("identified monotone version update required")
    if not update.replay_passed or update.approved_by != update.owner:
        raise ValueError("passing replay and explicit artifact-owner approval required")
    return update.candidate_version
