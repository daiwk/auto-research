"""One conservative evidence policy shared by aggregation, display and selection."""
from __future__ import annotations

from typing import Any
import math


def sections(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from sections(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from sections(child)


def diagnostic_reasons(payload: dict) -> list[str]:
    reasons = set()
    for section in sections(payload):
        if section.get("diagnostic_only") is True or section.get("promotion_eligible") is False:
            reasons.add("diagnostic_or_ineligible")
        if section.get("gold_derived_candidate_set") is True or section.get("gold_fields_available") is True:
            reasons.add("gold_derived_evaluation")
        if section.get("fidelity") == "concept_demo" or section.get("level") == "concept_demo":
            reasons.add("concept_demo")
        tier = str(section.get("tier", section.get("evaluation_tier", ""))).lower()
        if tier.startswith(("l0", "l1")):
            reasons.add("mechanism_or_contract_only")
        dataset = section.get("dataset", "")
        if isinstance(dataset, dict):
            dataset = dataset.get("id", dataset.get("name", ""))
        if str(dataset) in {"arithmetic-smoke", "gsm8k-candidate"}:
            reasons.add("diagnostic_dataset")
    return sorted(reasons)


def assess_evidence(payload: dict, *, seeds=None, minimum_seeds=3) -> dict[str, Any]:
    protocol = payload.get("evaluation_protocol", {})
    protocol = protocol if isinstance(protocol, dict) else {}
    tier = str(protocol.get("tier", payload.get("evaluation_tier", "unclassified")))
    reasons = diagnostic_reasons(payload)
    diagnostic = bool(reasons)
    if any(isinstance(value, float) and not math.isfinite(value)
           for section in sections(payload) for value in section.values()):
        reasons.append("non_finite_result")
    actual_seeds = list(seeds if seeds is not None else protocol.get("seeds", payload.get("seeds", ())))
    if len(set(actual_seeds)) != len(actual_seeds):
        reasons.append("duplicate_seeds")
    if len(set(actual_seeds)) < minimum_seeds:
        reasons.append("insufficient_independent_seeds")
    if not tier.lower().startswith(("l2", "l3")):
        reasons.append("capability_tier_not_established")
    contract = payload.get("comparison_contract", {})
    required = ("protocol_id", "dataset_revision", "split_revision", "baseline", "code_revision")
    if not isinstance(contract, dict) or any(not contract.get(key) for key in required):
        reasons.append("comparison_contract_missing")
    if not isinstance(contract, dict) or contract.get("test_isolated") is not True:
        reasons.append("test_isolation_not_established")
    rows = payload.get("seed_results")
    if rows is not None:
        if len(rows) != len(actual_seeds) or any(row.get("seed") != seed for row, seed in zip(rows, actual_seeds)):
            reasons.append("seed_results_not_aligned")
        if any(row.get("status", "completed") != "completed" for row in rows):
            reasons.append("failed_seed")
        for row in rows:
            other = row.get("comparison_contract")
            if other is not None and other != contract:
                reasons.append("incompatible_seed_protocols")
    formal = not reasons
    return {
        "policy_version": 1,
        "tier": "l1_mechanism_diagnostic" if diagnostic else tier,
        "diagnostic_only": diagnostic,
        "formal_comparison": formal,
        "claim_policy": ("formal multi-seed capability comparison; improvement requires a separate statistical decision"
                         if formal else "not a formal capability comparison; " + "; ".join(sorted(set(reasons)))),
        "eligibility_reasons": sorted(set(reasons)),
    }


def selection_eligible(payload: dict, seeds, minimum_seeds: int) -> bool:
    """Validation search is not itself a formal improvement claim."""
    finite = all(not isinstance(value, float) or math.isfinite(value)
                 for section in sections(payload) for value in section.values())
    return (finite and not diagnostic_reasons(payload) and len(set(seeds)) == len(seeds)
            and len(set(seeds)) >= minimum_seeds)
