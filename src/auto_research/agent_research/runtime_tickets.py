"""RuntimeTickets CPU ticket/gate kernel, not an egress proxy or sandbox.

https://arxiv.org/html/2611.03772v1 §3 Algorithm 1, Eq.1. Trusted validators
and a forwarding callback are supplied by the host. Untrusted Skill text is
hashed/cited, never evaluated. HMAC records demonstrate local integrity only;
they are not the paper's complete multi-issuer sealed observation account.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import hmac
import json
from threading import RLock

REQUIRES_GPU_VALIDATION = False
OBLIGATIONS = frozenset({"recipient", "valid", "sum"})


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


@dataclass(frozen=True)
class Grant:
    operation: str
    resource: str
    recipients: frozenset[str]

    def __post_init__(self):
        recipients = frozenset(self.recipients)
        if not self.operation or not self.resource or not recipients or any(not isinstance(x, str) or not x for x in recipients):
            raise ValueError("exact nonempty operation/resource/recipients required")
        object.__setattr__(self, "recipients", recipients)


@dataclass(frozen=True)
class SourceRef:
    first_line: int
    last_line: int
    excerpt: str


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    skill_sha256: str
    grants: tuple[Grant, ...]
    host_budget: int
    recipient: str
    validator_id: str
    limit: int
    references: tuple[tuple[str, SourceRef], ...]


def compile_ticket(*, task_id: str, skill: str, host_grants: tuple[Grant, ...],
                   selected_grants: tuple[Grant, ...], host_budget: int, recipient: str,
                   validator_id: str, limit: int, references: dict[str, SourceRef]):
    """Tighten exact grants; bind every obligation to actual numbered lines.

    The trusted caller approves the delivery contract and the chosen validator;
    this function does not infer their semantic relevance with an LLM.
    """
    if (not isinstance(task_id, str) or not task_id or not isinstance(skill, str) or not skill
            or type(host_budget) is not int or type(limit) is not int or not 0 <= limit <= host_budget
            or not recipient or not validator_id or set(references) != OBLIGATIONS):
        raise ValueError("complete trusted delivery contract and three cited obligations required")
    hosts, selected = tuple(host_grants), tuple(selected_grants)
    if not selected or any(not isinstance(g, Grant) for g in hosts + selected):
        raise ValueError("typed nonempty selected grants required")
    if any(not any(g.operation == h.operation and g.resource == h.resource and g.recipients <= h.recipients for h in hosts) for g in selected):
        raise ValueError("a ticket may tighten, never expand, the host grant")
    if not any(recipient in g.recipients for g in selected):
        raise ValueError("delivery recipient is outside the selected grant")
    lines = skill.splitlines()
    for ref in references.values():
        if (not isinstance(ref, SourceRef) or type(ref.first_line) is not int or type(ref.last_line) is not int
                or not 1 <= ref.first_line <= ref.last_line <= len(lines)
                or not ref.excerpt or ref.excerpt != "\n".join(lines[ref.first_line - 1:ref.last_line])):
            raise ValueError("source references must exactly match the bound Skill lines")
    refs = tuple(sorted(references.items()))
    digest = sha256(skill.encode()).hexdigest()
    identity = {"task": task_id, "skill_sha256": digest, "host_budget": host_budget,
                "recipient": recipient, "validator": validator_id, "limit": limit,
                "grants": [(g.operation, g.resource, sorted(g.recipients)) for g in selected],
                "references": [(name, ref.first_line, ref.last_line, ref.excerpt) for name, ref in refs]}
    return Ticket(sha256(_canonical(identity)).hexdigest(), digest, selected,
                  host_budget, recipient, validator_id, limit, refs)


@dataclass(frozen=True)
class Request:
    request_id: str
    operation: str
    resource: str
    recipient: str
    payload: bytes

    def __post_init__(self):
        if any(not isinstance(x, str) or not x for x in (self.request_id, self.operation, self.resource, self.recipient)) or not isinstance(self.payload, bytes):
            raise ValueError("named immutable request and bytes payload required")


def verify_records(records, key: bytes, ticket_id: str):
    previous = "0" * 64
    for index, record in enumerate(records):
        row = dict(record)
        tag = row.pop("mac", None)
        if row.get("sequence") != index or row.get("previous") != previous or row.get("ticket_id") != ticket_id:
            return False
        expected = hmac.new(key, _canonical(row), "sha256").hexdigest()
        if not isinstance(tag, str) or not hmac.compare_digest(tag, expected):
            return False
        previous = tag
    return True


class Gate:
    """Atomic local pre-effect decision and at-most-once callback invocation.

    Amount is bytes in this bounded implementation. A callback failure has an
    unknown delivery outcome: quota stays consumed and retries never resend.
    No claim about network delivery or complete monitoring is made.
    """

    def __init__(self, ticket: Ticket, validators: dict, *, audit_key: bytes):
        if not isinstance(ticket, Ticket) or ticket.validator_id not in validators or not callable(validators[ticket.validator_id]):
            raise ValueError("frozen ticket and trusted registered validator required")
        if not isinstance(audit_key, bytes) or len(audit_key) < 16:
            raise ValueError("host-held audit key must be at least 16 bytes")
        self.ticket, self._validator, self._key = ticket, validators[ticket.validator_id], audit_key
        self._used, self._records, self._seen = 0, [], {}
        self._lock = RLock()

    @property
    def used(self):
        with self._lock:
            return self._used

    @property
    def records(self):
        with self._lock:
            return tuple(dict(row) for row in self._records)

    def dispatch(self, request: Request, forward):
        if not isinstance(request, Request) or not callable(forward):
            raise ValueError("typed request and host forward callback required")
        binding = (request.operation, request.resource, request.recipient, sha256(request.payload).hexdigest())
        with self._lock:
            if request.request_id in self._seen:
                old_binding, decision = self._seen[request.request_id]
                if binding != old_binding:
                    raise ValueError("request identity reused with different content")
                return {"decision": decision, "forwarded": False, "replayed": True}
            covered = any(g.operation == request.operation and g.resource == request.resource and request.recipient in g.recipients for g in self.ticket.grants)
            failures, unknown = [], []
            if not covered:
                failures.append("host_grant")
            else:
                if request.recipient != self.ticket.recipient:
                    failures.append("recipient")
                if self._used + len(request.payload) > self.ticket.limit:
                    failures.append("sum")
                if self._used + len(request.payload) > self.ticket.host_budget:
                    failures.append("host_budget")
                try:
                    valid = self._validator(request.payload)
                except Exception:
                    valid = None
                if valid is False:
                    failures.append("valid")
                elif valid is not True:
                    unknown.append("valid")
            decision = "Deny" if failures else "Defer" if unknown else "Allow"
            row = {"sequence": len(self._records), "ticket_id": self.ticket.ticket_id,
                   "request_id": request.request_id, "decision": decision,
                   "reasons": failures + unknown, "amount_bytes": len(request.payload),
                   "payload_sha256": binding[-1], "previous": self._records[-1]["mac"] if self._records else "0" * 64}
            row["mac"] = hmac.new(self._key, _canonical(row), "sha256").hexdigest()
            self._records.append(row)
            self._seen[request.request_id] = (binding, decision)
            if decision == "Allow":
                self._used += len(request.payload)
                forward(request)
            return {"decision": decision, "forwarded": decision == "Allow", "replayed": False}


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU only")
    skill = "Deliver the approved result."
    ref = SourceRef(1, 1, skill)
    grant = Grant("send", "report", frozenset({"approved", "other"}))
    ticket = compile_ticket(task_id=f"task-{seed}", skill=skill, host_grants=(grant,), selected_grants=(grant,),
                            host_budget=10, recipient="approved", validator_id="object", limit=4,
                            references={name: ref for name in OBLIGATIONS})
    key = b"public-diagnostic-audit-key"
    gate = Gate(ticket, {"object": lambda payload: payload == b"ok"}, audit_key=key)
    forwarded = []
    a = Request("a", "send", "report", "approved", b"ok")
    results = [gate.dispatch(a, forwarded.append), gate.dispatch(a, forwarded.append),
               gate.dispatch(Request("b", "send", "report", "other", b"ok"), forwarded.append),
               gate.dispatch(Request("c", "send", "report", "approved", b"no"), forwarded.append)]
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"decisions_recorded": len(gate.records), "allowed_bytes": gate.used, "forward_callbacks": len(forwarded)},
            "checks": {"valid_delivery_allowed": results[0]["decision"] == "Allow", "retry_not_resent": results[1]["replayed"],
                       "recipient_blocked": results[2]["decision"] == "Deny", "same_recipient_bad_object_blocked": results[3]["decision"] == "Deny",
                       "record_chain_valid": verify_records(gate.records, key, ticket.ticket_id)}}
