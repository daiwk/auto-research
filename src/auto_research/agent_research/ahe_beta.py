"""AHE-Beta requirement admission and head-bound review protocol (L0).

No user simulator, requirement synthesizer, coding agent, benchmark or merge is
executed. Typed evidence is a declared boundary, not a semantic verifier that a
natural-language requirement is true. Benchmark scores and hidden tests have no
field in the developer delivery package.
"""

from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Sequence

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Evidence:
    session: str
    runtime_log: str
    public_task: str
    conditions: str

    def __post_init__(self):
        if any(
            not isinstance(x, str) or not x.strip()
            for x in (self.session, self.runtime_log, self.public_task, self.conditions)
        ):
            raise ValueError("nonempty public/log/condition evidence required")


@dataclass(frozen=True)
class Requirement:
    identity: str
    kind: str
    text: str
    acceptance: str
    evidence: tuple[Evidence, ...]
    verified: bool
    covers: tuple[str, ...] = ()

    def __post_init__(self):
        if self.kind not in {"requirement", "consolidated", "prd"}:
            raise ValueError("only admitted artifact types, never raw issues")
        if (
            not self.identity
            or not self.text
            or not self.acceptance
            or type(self.verified) is not bool
        ):
            raise ValueError("typed requirement with acceptance criteria required")
        if not isinstance(self.evidence, tuple) or any(
            not isinstance(e, Evidence) for e in self.evidence
        ):
            raise TypeError("immutable typed evidence package required")
        if not isinstance(self.covers, tuple) or len(set(self.covers)) != len(self.covers):
            raise ValueError("covers must be unique immutable requirement IDs")
        if self.kind == "consolidated" and len(self.covers) < 2:
            raise ValueError("architect consolidation must cover at least two requirements")
        if self.kind != "consolidated" and self.covers:
            raise ValueError("only consolidated requirements have covers")


def deliverable(items: Sequence[Requirement]) -> tuple[Requirement, ...]:
    """Algorithm1: uncovered requirements plus consolidations and PRDs."""
    rows = tuple(items)
    if any(not isinstance(r, Requirement) for r in rows) or len({r.identity for r in rows}) != len(
        rows
    ):
        raise ValueError("unique typed requirement artifacts required")
    originals = {r.identity for r in rows if r.kind == "requirement"}
    for r in rows:
        if r.kind == "consolidated" and not set(r.covers) <= originals:
            raise ValueError("consolidation must cite actual original requirements")
    # Unverified consolidations do not close originals and cannot silence work.
    admitted = tuple(r for r in rows if r.verified and r.evidence)
    covered = {k for r in admitted if r.kind == "consolidated" for k in r.covers}
    return tuple(r for r in admitted if r.identity not in covered)


@dataclass(frozen=True)
class Review:
    approved_head: str
    approved_design: str
    design_passed: bool
    code_passed: bool
    full_suite_completed: bool
    acceptance_passed: bool

    def __post_init__(self):
        if (
            not self.approved_head
            or not self.approved_design
            or any(
                type(v) is not bool
                for v in (
                    self.design_passed,
                    self.code_passed,
                    self.full_suite_completed,
                    self.acceptance_passed,
                )
            )
        ):
            raise ValueError("head/design identity and strict review checks required")


def merge_eligible(requirement: Requirement, review: Review, *, head: str, design: str) -> bool:
    """Pure decision only: no git, network, deployment or implicit merge authority."""
    return (
        requirement.verified
        and bool(requirement.evidence)
        and review.approved_head == head
        and review.approved_design == design
        and review.design_passed
        and review.code_passed
        and review.full_suite_completed
        and review.acceptance_passed
    )


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    ev = (Evidence("s1", "log:sha256", "public task", "fixed budget"),)
    a = Requirement("a", "requirement", "bound control delivery", "delivery observed", ev, True)
    b = Requirement("b", "requirement", "persist state", "restore observed", ev, True)
    c = Requirement(
        "c", "consolidated", "durable control path", "both boundaries checked", ev, True, ("a", "b")
    )
    prd = Requirement("d", "prd", "visible progress", "public report delivered", ev, True)
    selected = deliverable((a, b, c, prd))
    review = Review("head1", "rfc1", True, True, True, True)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l0_interface",
        "checks": {
            "consolidation_closes_covered_only": tuple(r.identity for r in selected) == ("c", "d"),
            "current_head_approved": merge_eligible(c, review, head="head1", design="rfc1"),
            "stale_head_rejected": not merge_eligible(c, review, head="head2", design="rfc1"),
            "changed_design_rejected": not merge_eligible(c, review, head="head1", design="rfc2"),
            "no_gold_field": set(Evidence.__dataclass_fields__)
            == {"session", "runtime_log", "public_task", "conditions"},
        },
        "metrics": {
            "delivered_requirements": len(selected),
            "covered_requirements": 2,
            "model_calls": 0,
        },
    }
