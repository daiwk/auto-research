"""ScientistOne CoE's deterministic audit core, not an autonomous scientist.

Implements hash-linked numerical provenance, canonical evaluator reruns, adaptive
noise tolerance, and independent audit verdict aggregation. Semantic/citation
checks without external evidence remain unverified, never default to passed.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Callable, Mapping, Sequence


@dataclass(frozen=True)
class Artifact:
    key: str
    sha256: str
    kind: str

    def __post_init__(self) -> None:
        if not self.key or not self.kind or len(self.sha256) != 64:
            raise ValueError("artifact requires a key, kind and SHA256 digest")
        try:
            int(self.sha256, 16)
        except ValueError as error:
            raise ValueError("invalid SHA256 digest") from error

    @classmethod
    def from_bytes(cls, key: str, payload: bytes, kind: str) -> Artifact:
        return cls(key, hashlib.sha256(payload).hexdigest(), kind)


@dataclass(frozen=True)
class Measurement:
    artifact: str
    metric: str
    value: float
    stage: str
    unit: str
    direction: str

    def __post_init__(self) -> None:
        if not math.isfinite(self.value) or self.direction not in {"min", "max"}:
            raise ValueError("finite value and explicit metric direction required")
        if not all((self.artifact, self.metric, self.stage, self.unit)):
            raise ValueError("measurement provenance fields required")


@dataclass(frozen=True)
class Claim:
    key: str
    kind: str
    supports: tuple[str, ...]
    metric: str | None = None
    value: float | None = None
    stage: str | None = None
    unit: str | None = None
    direction: str | None = None

    def __post_init__(self) -> None:
        if not self.key or self.kind not in {"numerical", "citation", "method", "conclusion"}:
            raise ValueError("invalid claim key/type")
        if self.kind == "numerical":
            if self.value is None or not math.isfinite(self.value):
                raise ValueError("numerical claim requires a finite value")
            if not all((self.metric, self.stage, self.unit)) or self.direction not in {"min", "max"}:
                raise ValueError("numerical metric, stage, unit and direction required")


def verify_bundle(
    artifacts: Sequence[Artifact], claims: Sequence[Claim], payloads: Mapping[str, bytes]
) -> dict:
    """Verify source bytes and a DAG from every claim to at least one artifact.

    Structural provenance is not logical or semantic entailment. Missing bytes,
    dangling nodes, cycles and a claim with no grounding source all fail closed.
    """
    artifact_map = {artifact.key: artifact for artifact in artifacts}
    claim_map = {claim.key: claim for claim in claims}
    if len(artifact_map) != len(artifacts) or len(claim_map) != len(claims) or set(artifact_map) & set(claim_map):
        raise ValueError("artifact/claim IDs must be unique and disjoint")
    hash_valid = {
        key: key in payloads and hashlib.sha256(payloads[key]).hexdigest() == artifact.sha256
        for key, artifact in artifact_map.items()
    }

    def grounded(key: str, active: frozenset[str]) -> bool:
        if key in active:
            return False
        if key in artifact_map:
            return hash_valid[key]
        if key not in claim_map:
            return False
        claim = claim_map[key]
        return bool(claim.supports) and all(grounded(child, active | {key}) for child in claim.supports)

    return {
        "artifact_hash_valid": hash_valid,
        "structurally_grounded": {claim.key: grounded(claim.key, frozenset()) for claim in claims},
        "semantic_entailment": "unverified",
    }


def score_verification(
    reported: Measurement,
    *, solution: Artifact, solution_bytes: bytes, evaluator: Artifact,
    evaluator_bytes: bytes,
    evaluate: Callable[[bytes, bytes, int], Measurement],
    repeats: int = 5,
) -> dict:
    """I1 canonical evaluator reruns, not a supplied list of claimed scores.

    The evaluator callback is caller-audited trusted code. No arbitrary source is
    executed by this module. The same solution/evaluator bytes are used each run.
    """
    if repeats != 5:
        raise ValueError("paper I1 protocol requires five evaluator reruns")
    for artifact, payload in ((solution, solution_bytes), (evaluator, evaluator_bytes)):
        if hashlib.sha256(payload).hexdigest() != artifact.sha256:
            raise ValueError("canonical evaluator/solution hash mismatch")
    runs = [evaluate(solution_bytes, evaluator_bytes, index) for index in range(repeats)]
    signature = (reported.metric, reported.stage, reported.unit, reported.direction)
    if any((run.metric, run.stage, run.unit, run.direction) != signature for run in runs):
        return {"status": "mismatch", "reason": "metric_stage_unit_or_direction_mismatch", "reruns": repeats}
    values = [run.value for run in runs]
    average, sigma = mean(values), pstdev(values)
    absolute_tolerance = max(0.01 * abs(average), 3 * sigma)
    # At a deterministic zero mean the relative formula is undefined. Require
    # exact zero rather than inventing a permissive epsilon tolerance.
    difference = abs(reported.value - average)
    return {
        "status": "match" if difference <= absolute_tolerance else "mismatch",
        "reruns": repeats,
        "canonical_mean": average,
        "canonical_population_std": sigma,
        "absolute_tolerance": absolute_tolerance,
        "relative_tolerance": absolute_tolerance / abs(average) if average else None,
        "absolute_difference": difference,
        "solution_sha256": solution.sha256,
        "evaluator_sha256": evaluator.sha256,
    }


def numerical_cpr(
    claims: Sequence[Claim], measurements: Sequence[Measurement],
    artifacts: Sequence[Artifact], payloads: Mapping[str, bytes], *, atol: float = 1e-12,
) -> dict:
    """Numerical CPR counts matching log entries, not merely a source hyperlink.

    The artifact referenced by a measurement must be a valid execution log. The
    same metric/stage/unit/direction must appear in the declared support chain.
    """
    if not math.isfinite(atol) or atol < 0:
        raise ValueError("finite nonnegative matching tolerance required")
    structural = verify_bundle(artifacts, claims, payloads)
    artifact_map = {artifact.key: artifact for artifact in artifacts}
    # A caller-supplied Measurement is not evidence unless its complete record
    # is actually present in the verified log bytes. No numeric claims are
    # accepted merely because their metadata points at a real, unrelated file.
    logged = set()
    for artifact in artifacts:
        if artifact.kind != "execution_log" or not structural["artifact_hash_valid"][artifact.key]:
            continue
        try:
            document = json.loads(payloads[artifact.key])
            for record in document["measurements"]:
                logged.add(Measurement(artifact=artifact.key, **record))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            raise ValueError("execution log must contain canonical measurement records") from error
    if any(measurement not in logged for measurement in measurements):
        raise ValueError("measurement is not present in verified execution-log bytes")
    claim_map = {claim.key: claim for claim in claims}
    matched = {}

    def supports(key: str, seen: frozenset[str]) -> set[str]:
        if key in seen:
            return set()
        if key in artifact_map:
            return {key}
        if key not in claim_map:
            return set()
        return set().union(*(supports(child, seen | {key}) for child in claim_map[key].supports))

    for claim in claims:
        if claim.kind != "numerical":
            continue
        sources = supports(claim.key, frozenset())
        matched[claim.key] = structural["structurally_grounded"][claim.key] and any(
            measurement.artifact in sources
            and artifact_map[measurement.artifact].kind == "execution_log"
            and (measurement.metric, measurement.stage, measurement.unit, measurement.direction)
            == (claim.metric, claim.stage, claim.unit, claim.direction)
            and math.isclose(measurement.value, claim.value, rel_tol=0.0, abs_tol=atol)
            for measurement in measurements
        )
    return {
        "quantitative_claims": len(matched), "matched_claims": sum(matched.values()),
        "cpr": sum(matched.values()) / len(matched) if matched else None,
        "claims": matched,
        "semantic_support_verified": False,
    }


@dataclass(frozen=True)
class AuditVote:
    verdict: str
    evidence: str
    judge_id: str


def majority_audit(votes: Sequence[AuditVote], *, pass_verdict: str, fail_verdict: str) -> dict:
    """I2/I4 independent judgment aggregation with abstentions and evidence IDs."""
    if pass_verdict == fail_verdict:
        raise ValueError("pass/fail must differ")
    if not votes:
        return {"status": "unverified", "reason": "no_external_judgments", "votes": 0}
    if len({vote.judge_id for vote in votes}) != len(votes):
        raise ValueError("each judgment needs a distinct invocation ID")
    allowed = {pass_verdict, fail_verdict, "unverified"}
    if any(vote.verdict not in allowed or not vote.judge_id or not vote.evidence.strip() for vote in votes):
        raise ValueError("invalid or ungrounded audit vote")
    threshold = len(votes) // 2 + 1
    counts = {name: sum(vote.verdict == name for vote in votes) for name in allowed}
    status = next((name for name in (pass_verdict, fail_verdict) if counts[name] >= threshold), "unverified")
    return {"status": status, "votes": len(votes), "counts": counts, "threshold": threshold}


def reference_verification(
    *, reference_id: str, resolve: Callable[[str], Sequence[Mapping[str, str]]] | None,
    disambiguate: Callable[[str, tuple[Mapping[str, str], ...]], AuditVote] | None,
) -> dict:
    """I3 requires actual resolver + semantic disambiguation, not URL existence.

    No results is unverified here: without proof of completed independent source
    queries it is not justified to label a citation hallucinated.
    """
    if resolve is None or disambiguate is None:
        return {"status": "unverified", "reason": "resolver_or_disambiguator_unavailable"}
    records = tuple(resolve(reference_id))
    if not records:
        return {"status": "unverified", "reason": "no_resolver_records_not_a_proof_of_absence"}
    if any(not record.get("source_url", "").startswith("https://") for record in records):
        raise ValueError("resolver records require source URLs")
    vote = disambiguate(reference_id, records)
    if vote.verdict not in {"verified", "hallucinated", "unverified"} or not vote.evidence.strip():
        raise ValueError("grounded disambiguation verdict required")
    return {"status": vote.verdict, "evidence": vote.evidence, "records": len(records)}
