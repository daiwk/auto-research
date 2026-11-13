"""PolicyBank v1 structured capability memory, not semantic policy repair.

External trusted Policy Agents decide Add/Revise/Omit after developer feedback.
The bank neither interprets permissions nor upgrades feedback into ground truth.
"""
from dataclasses import dataclass
from typing import Literal

REQUIRES_GPU_VALIDATION = False


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("explicit nonempty policy text/provenance required")


@dataclass(frozen=True)
class Capability:
    identity: str
    tool: str
    header: str
    trigger: str
    preconditions: str
    eligibility: str
    action: str
    key_insight: str

    def __post_init__(self):
        for value in self.__dict__.values():
            _text(value)


@dataclass(frozen=True)
class Change:
    operation: Literal["add", "revise", "omit"]
    capability: Capability | None
    task_trace_ref: str
    developer_feedback_ref: str

    def __post_init__(self):
        if self.operation not in ("add", "revise", "omit"):
            raise ValueError("PolicyBank supports Add/Revise/Omit, not inferred operations")
        if (self.operation == "omit") != (self.capability is None):
            raise ValueError("only Omit has no capability payload")
        if self.capability is not None and not isinstance(self.capability, Capability):
            raise ValueError("typed capability required")
        _text(self.task_trace_ref)
        _text(self.developer_feedback_ref)


class PolicyBank:
    def __init__(self, entries=()):
        rows = tuple(entries)
        if any(not isinstance(row, Capability) for row in rows) or len({e.identity for e in rows}) != len(rows):
            raise ValueError("unique typed initial capabilities required")
        self._entries = {row.identity:row for row in rows}
        self._changes: list[Change] = []

    def headers(self):
        """Stage1: expose capability headers, not automatic semantic retrieval."""
        return tuple((e.identity, e.tool, e.header) for e in self._entries.values())

    def retrieve(self, selected_ids):
        """Stage2: return only explicitly selected full entries; no gold scorer."""
        if isinstance(selected_ids, (str, bytes)):
            raise ValueError("explicit capability identity sequence required")
        ids = tuple(selected_ids)
        if any(not isinstance(i, str) for i in ids) or len(set(ids)) != len(ids) or any(i not in self._entries for i in ids):
            raise ValueError("unique existing selected capability identities required")
        return tuple(self._entries[i] for i in ids)

    @property
    def changes(self):
        return tuple(self._changes)

    def apply_after_task(self, change: Change):
        """Commit an externally authored update; this method does not learn it."""
        if not isinstance(change, Change):
            raise ValueError("typed change with feedback provenance required")
        if change.operation != "omit":
            entry = change.capability
            exists = entry.identity in self._entries
            if (change.operation == "add" and exists) or (change.operation == "revise" and not exists):
                raise ValueError("Add requires new identity; Revise requires an existing identity")
            self._entries[entry.identity] = entry
        self._changes.append(change)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only memory contract required")
    first = Capability("cancel-insured", "cancel", "insured cancellation", "cancellation request",
                       "verify reservation", "old written rule", "cancel after approval", "initial interpretation")
    second = Capability("cancel-insured", "cancel", "insured cancellation", "cancellation request",
                        "verify reservation", "externally supplied corrected rule", "cancel after approval", "explicit correction, not learned here")
    bank = PolicyBank([first])
    initial = bank.headers()
    bank.apply_after_task(Change("revise", second, "fixture:trace", "fixture:developer-feedback"))
    bank.apply_after_task(Change("omit", None, "fixture:trace-2", "fixture:no-new-information"))
    checks = {"header_selection_before_full_entry":initial[0] == (first.identity, first.tool, first.header),
              "revision_same_capability_not_duplicate":len(bank.headers()) == 1 and bank.retrieve([first.identity]) == (second,),
              "omit_does_not_rewrite_memory":bank.retrieve([first.identity])[0] is second,
              "developer_feedback_provenance_preserved":bank.changes[0].developer_feedback_ref == "fixture:developer-feedback"}
    return {"seed":seed,"diagnostic_only":True,"evaluation_tier":"l0_interface","checks":checks,
            "metrics":{"capabilities":len(bank.headers()),"audited_changes":len(bank.changes),"semantic_repairs_measured":0}}
