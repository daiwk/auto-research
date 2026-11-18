"""Paper 2611.09822v1 Appendix B/C: admission AFTER external verification.

This is not a Lean verifier or an attestation authenticator. Trusted host code
must produce the receipt after replaying the exact candidate in a clean sandbox.
Agent-provided booleans are not evidence. No agent search or quantum code runs.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
import random
import re

REQUIRES_GPU_VALIDATION = False
STANDARD_AXIOMS = frozenset({"propext", "Quot.sound", "Classical.choice"})
_DIGEST = re.compile(r"[0-9a-f]{64}")


def _digest(value: str) -> None:
    if not isinstance(value, str) or not _DIGEST.fullmatch(value):
        raise ValueError("a lowercase SHA256 digest is required")


def _cost(value: int | Fraction) -> None:
    if type(value) not in (int, Fraction) or value < 0:
        raise ValueError("cost must be a nonnegative exact int or Fraction")


@dataclass(frozen=True)
class Solution:
    """One established/candidate solution under an explicit cost convention.

    code_size is measured externally using the SAME convention for both rows;
    the paper does not specify whether size means bytes, lines, or tokens.
    """

    specification_sha256: str
    artifact_sha256: str
    cost_metric: str
    cost: int | Fraction
    code_size: int

    def __post_init__(self) -> None:
        _digest(self.specification_sha256)
        _digest(self.artifact_sha256)
        _cost(self.cost)
        if not isinstance(self.cost_metric, str) or not self.cost_metric.strip():
            raise ValueError("explicit cost convention is required")
        if type(self.code_size) is not int or self.code_size <= 0:
            raise ValueError("code_size must be a positive integer")


@dataclass(frozen=True)
class ExternalComparatorResult:
    """Typed, caller-trusted evidence boundary; not self-authenticating proof.

    Hash bindings and evidence_ref are local protocol safeguards, not a claimed
    reproduction of the author's undisclosed receipt format. A trusted caller
    must verify provenance/authenticity before passing this object.
    """

    specification_sha256: str
    artifact_sha256: str
    cost_metric: str
    proved_cost: int | Fraction
    evidence_ref: str
    clean_sandbox_replay: bool
    target_theorems_match: bool
    transitive_definitions_match: bool
    proof_terms_checked: bool
    no_sorry: bool
    resource_theorem_reduces: bool
    axioms: frozenset[str]

    def __post_init__(self) -> None:
        _digest(self.specification_sha256)
        _digest(self.artifact_sha256)
        _cost(self.proved_cost)
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise ValueError("external evidence reference is required")
        if not isinstance(self.cost_metric, str) or not self.cost_metric.strip():
            raise ValueError("explicit cost convention is required")
        for name in (
            "clean_sandbox_replay", "target_theorems_match",
            "transitive_definitions_match", "proof_terms_checked", "no_sorry",
            "resource_theorem_reduces",
        ):
            if type(getattr(self, name)) is not bool:
                raise ValueError("verification fields must be actual booleans")
        if not isinstance(self.axioms, frozenset) or any(
            not isinstance(axiom, str) for axiom in self.axioms
        ):
            raise ValueError("axioms must be a frozenset of names")


@dataclass(frozen=True)
class Admission:
    accepted: bool
    reason: str


def admit(
    current: Solution,
    candidate: Solution,
    receipt: ExternalComparatorResult | None,
) -> Admission:
    """Apply the paper's default rule to an already-established wiki solution.

    There is no wiki mutation. A real repository must apply the returned choice
    atomically against the same current revision (and re-evaluate if it changes).
    """
    if not isinstance(current, Solution) or not isinstance(candidate, Solution):
        raise TypeError("typed current and candidate solutions are required")
    if current.cost <= 0:
        raise ValueError("relative improvement requires a positive baseline cost")
    if candidate.specification_sha256 != current.specification_sha256:
        return Admission(False, "different_frozen_specification")
    if candidate.cost_metric != current.cost_metric:
        return Admission(False, "different_cost_convention")
    if not isinstance(receipt, ExternalComparatorResult):
        return Admission(False, "external_verification_missing")
    if (
        receipt.specification_sha256 != candidate.specification_sha256
        or receipt.artifact_sha256 != candidate.artifact_sha256
        or receipt.cost_metric != candidate.cost_metric
        or receipt.proved_cost != candidate.cost
    ):
        return Admission(False, "external_evidence_binding_mismatch")
    if not all((
        receipt.clean_sandbox_replay, receipt.target_theorems_match,
        receipt.transitive_definitions_match, receipt.proof_terms_checked,
        receipt.no_sorry, receipt.resource_theorem_reduces,
    )) or not receipt.axioms <= STANDARD_AXIOMS:
        return Admission(False, "external_verification_failed")
    if 100 * candidate.cost <= 95 * current.cost:
        return Admission(True, "cost_improvement_at_least_five_percent")
    if (
        5 * candidate.code_size <= 4 * current.code_size
        and candidate.cost < current.cost
    ):
        return Admission(True, "code_shortening_at_least_twenty_percent_and_lower_cost")
    return Admission(False, "insufficient_improvement")


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Synthetic receipt fixtures test admission only, NEVER proof correctness."""
    if device != "cpu":
        raise ValueError("CPU-only admission diagnostic; no GPU fallback")
    rng = random.Random(seed)
    scale, size = rng.randint(1, 1000), 100 * rng.randint(1, 100)
    current = Solution("a" * 64, "b" * 64, "fixed-Q-times-T-v1", 100 * scale, size)
    candidate = replace(current, artifact_sha256="c" * 64, cost=95 * scale)
    receipt = ExternalComparatorResult(
        candidate.specification_sha256, candidate.artifact_sha256,
        candidate.cost_metric, candidate.cost, "synthetic-fixture:not-a-proof",
        True, True, True, True, True, True, STANDARD_AXIOMS,
    )
    shorter = replace(candidate, cost=99 * scale, code_size=4 * size // 5)
    short_receipt = replace(receipt, proved_cost=shorter.cost)
    cases = {
        "five_percent_boundary": admit(current, candidate, receipt).accepted,
        "twenty_percent_shortening": admit(current, shorter, short_receipt).accepted,
        "below_cost_threshold_rejected": not admit(
            current, replace(candidate, cost=Fraction(95001, 1000) * scale),
            replace(receipt, proved_cost=Fraction(95001, 1000) * scale),
        ).accepted,
        "equal_cost_shortening_rejected": not admit(
            current, replace(shorter, cost=current.cost),
            replace(receipt, proved_cost=current.cost),
        ).accepted,
        "missing_external_result_rejected": not admit(current, candidate, None).accepted,
        "weakened_definition_rejected": not admit(
            current, candidate, replace(receipt, transitive_definitions_match=False),
        ).accepted,
        "custom_axiom_rejected": not admit(
            current, candidate, replace(receipt, axioms=STANDARD_AXIOMS | {"invented"}),
        ).accepted,
        "stale_artifact_rejected": not admit(
            current, candidate, replace(receipt, artifact_sha256="d" * 64),
        ).accepted,
        "unproved_cost_rejected": not admit(
            current, candidate, replace(receipt, proved_cost=candidate.cost - 1),
        ).accepted,
    }
    return {
        "seed": seed, "device": device, "diagnostic_only": True,
        "implementation_status": "component_only", "promotion_eligible": False,
        "evolve_integrated": False, "checks": cases,
        "metrics": {"passed_cases": sum(cases.values()), "case_count": len(cases),
                    "baseline_cost": current.cost, "baseline_code_size": size,
                    "real_proofs_checked": 0, "model_calls": 0},
    }
