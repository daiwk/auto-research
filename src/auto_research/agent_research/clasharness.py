"""Bounded CLASHarness imports and explicit public/scorer input contracts.

No trajectory command, reference solution, model API, or generated task code is
executed here. Published audit adjustments are kept distinct from new scoring.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Mapping, Sequence
from urllib.request import urlopen

REVISION = "234161ddc44755017215dd734d38be15419a45e0"
REPOSITORY = "https://github.com/google-research/CLASHarness"
FILE_HASHES = {
    "analysis/dead_rounds_exclusion.json": "cfbf94aecddf386ac97973b89c6e8c4ad775a34f3dbad87480ea44ffa18fa611",
    "analysis/v8_check_fairness_audit.json": "25a69bbc4c76183ec4e4c7795a9411dd68afc465d1957ee3199c406e94613509",
    "analysis/cost_high.json": "84e058226436bd2fb4d4a9715899e50694d7fd1f5f496e9e698f47127fdcae4e",
    "docs/analysis/analysis_v8/curated_rounds.json": "41a29d41b1b3c64604e152b4c617f025d70cbd6aaf4fa36321215d17c96576b0",
}
MAX_BYTES = 1024 * 1024
FORBIDDEN_SOLVER_FIELDS = frozenset({
    "ground_truth", "solution_commands", "expert_trajectory", "evaluation_checks",
    "answer", "reference", "private", "hidden_constraints", "check_results",
    "success", "score", "judge", "verdict", "passed", "gold", "gold_answer",
    "gold_solution", "reference_solution", "reference_answer", "ground_truth_value",
    "expected_answer", "solution", "solution_code", "private_state", "hidden_state",
    "reference_commands", "oracle_answer",
})
_FORBIDDEN_NORMALIZED = frozenset(re.sub(r"[^a-z0-9]", "", key.lower()) for key in FORBIDDEN_SOLVER_FIELDS)
POLICIES = {"as_published": frozenset(), "conservative": frozenset({"value_conflict", "protocol_unrequested_both_judges"})}


class ProtocolError(ValueError):
    """Invalid release, identity, verdict, or solver/scorer boundary."""


def _bounded_cache(path: Path, relative: str) -> bytes:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ProtocolError(f"invalid bounded source: {relative}")
    with path.open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ProtocolError(f"invalid bounded source: {relative}")
    return data


def fetch_release(directory: Path) -> dict:
    """Explicitly fetch <0.6 MB of pinned JSON; not the 8.5 GB task corpus."""
    for relative, expected in FILE_HASHES.items():
        target = directory / relative
        if any(p.is_symlink() for p in (target, *target.parents)):
            raise ProtocolError("release paths must not contain symlinks")
        if target.exists():
            data = _bounded_cache(target, relative)
        else:
            with urlopen(f"https://raw.githubusercontent.com/google-research/CLASHarness/{REVISION}/{relative}", timeout=30) as response:
                data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES or hashlib.sha256(data).hexdigest() != expected:
            raise ProtocolError(f"pinned source mismatch: {relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            with target.open("xb") as handle:
                handle.write(data)
    return {"revision": REVISION, "files": dict(FILE_HASHES), "task_archives_downloaded": False}


def load_release(directory: Path) -> dict:
    release = {}
    for relative, expected in FILE_HASHES.items():
        path = directory / relative
        data = _bounded_cache(path, relative)
        if hashlib.sha256(data).hexdigest() != expected:
            raise ProtocolError(f"pinned source mismatch: {relative}")
        release[relative] = json.loads(data)
    return release


def _identity(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ProtocolError("invalid task/check identity")
    return value


def _declared_public(value):
    """Reject known scorer fields; this cannot audit gold hidden in free text."""
    if isinstance(value, dict):
        copied = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ProtocolError("public data keys must be strings")
            if re.sub(r"[^a-z0-9]", "", key.lower()) in _FORBIDDEN_NORMALIZED:
                raise ProtocolError("hidden/scorer field found in caller-declared public data")
            copied[key] = _declared_public(item)
        return copied
    if isinstance(value, list):
        return [_declared_public(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        raise ProtocolError("public JSON numbers must be finite")
    if value is None or isinstance(value, (str, int, float, bool)):
        return deepcopy(value)
    raise ProtocolError("solver view must be JSON data")


def solver_view(task: Mapping) -> dict:
    """Expose only caller-declared public fields, not an attestation of no gold.

    Top-level scorer/private fields are omitted and known hidden aliases inside
    public data are rejected. The caller must independently audit instruction,
    visible constraints and free text; arbitrary answer leakage is not decidable
    from field names alone.
    """
    if not isinstance(task, Mapping):
        raise ProtocolError("task must be a mapping")
    task_id = _identity(task.get("task_id"))
    instruction = task.get("instruction")
    if not isinstance(instruction, str) or not instruction.strip():
        raise ProtocolError("nonempty public instruction required")
    data = task.get("data", {})
    if not isinstance(data, dict) or not isinstance(data.get("public", {}), dict):
        raise ProtocolError("public task data must be a mapping")
    visible = task.get("visible_constraints", [])
    if not isinstance(visible, list):
        raise ProtocolError("visible constraints must be a list")
    return {"task_id": task_id, "instruction": instruction,
            "public_data": _declared_public(data.get("public", {})),
            "visible_constraints": _declared_public(visible),
            "upstream_revision": REVISION, "solver_reference_access": None,
            "reference_isolation_verified": False,
            "public_input_trust_boundary": "caller_declared_public_not_content_audited"}


def audit_index(audit: Mapping, *, policy: str = "conservative") -> dict[str, frozenset[int]]:
    if policy not in POLICIES:
        raise ProtocolError("choose a preregistered as_published/conservative policy")
    result, seen = {}, set()
    for row in audit.get("checks", []):
        task_id = _identity(row.get("task_id"))
        index = row.get("check_index")
        if isinstance(index, bool) or not isinstance(index, int) or index < 0:
            raise ProtocolError("original nonnegative check_index required")
        key = (task_id, index)
        if key in seen:
            raise ProtocolError("duplicate audited check index")
        seen.add(key)
        tags = row.get("in_sets", [])
        if not isinstance(tags, list) or any(not isinstance(t, str) for t in tags):
            raise ProtocolError("invalid fairness tags")
        if set(tags) & POLICIES[policy]:
            result.setdefault(task_id, set()).add(index)
    return {key: frozenset(value) for key, value in result.items()}


def score_checks(task_id: str, checks: Sequence[Mapping], *, audit: Mapping,
                 policy: str = "conservative", expected_checks: Sequence[Mapping] | None = None) -> dict:
    """Aggregate external verdicts; only a complete declared inventory yields all_pass.

    Inventory verification is relative to the caller's explicit role/index list,
    not proof of coverage of an official CLASHarness task or the full corpus.
    """
    task_id = _identity(task_id)
    demoted = audit_index(audit, policy=policy).get(task_id, frozenset())
    if not isinstance(checks, Sequence) or isinstance(checks, (str, bytes)):
        raise ProtocolError("check verdicts must be a sequence")
    seen, roles, required, diagnostics, removed = set(), {}, [], [], []
    for check in checks:
        if not isinstance(check, Mapping):
            raise ProtocolError("check verdict must be a mapping")
        index, role, passed = check.get("check_index"), check.get("role"), check.get("passed")
        if isinstance(index, bool) or not isinstance(index, int) or index < 0 or index in seen:
            raise ProtocolError("missing/duplicate original check index")
        seen.add(index)
        if not isinstance(role, str) or role not in {"required", "diagnostic"} or not isinstance(passed, bool):
            raise ProtocolError("strict boolean verdict and explicit check role required")
        roles[index] = role
        if role == "required" and index not in demoted:
            required.append(passed)
        else:
            diagnostics.append(passed)
            if role == "required":
                removed.append(index)
    coverage_verified = expected_checks is not None
    if coverage_verified:
        if not isinstance(expected_checks, Sequence) or isinstance(expected_checks, (str, bytes)):
            raise ProtocolError("expected check inventory must be a sequence")
        expected = {}
        for check in expected_checks:
            if not isinstance(check, Mapping):
                raise ProtocolError("inventory entry must be a mapping")
            index, role = check.get("check_index"), check.get("role")
            if isinstance(index, bool) or not isinstance(index, int) or index < 0 or index in expected:
                raise ProtocolError("inventory requires unique original nonnegative check indices")
            if not isinstance(role, str) or role not in {"required", "diagnostic"}:
                raise ProtocolError("inventory requires explicit original check roles")
            expected[index] = role
        if expected != roles:
            raise ProtocolError("verdict indices/roles must exactly cover the complete expected inventory")
    observed_all_pass = all(required) if required else None
    observed_fraction = sum(required)/len(required) if required else None
    return {"task_id": task_id, "policy": policy, "required_checks": len(required),
            "required_passed": sum(required), "diagnostic_checks": len(diagnostics),
            "demoted_indices": sorted(removed),
            "observed_checks_all_pass": observed_all_pass,
            "observed_required_pass_fraction": observed_fraction,
            "coverage_verified": coverage_verified,
            "coverage_basis": "caller_supplied_complete_check_inventory" if coverage_verified else "unverified_observed_checks_only",
            "official_task_inventory_verified": False,
            "all_pass": observed_all_pass if coverage_verified else None,
            "required_pass_fraction": observed_fraction if coverage_verified else None,
            "kind": "external_check_verdict_aggregation", "semantic_judging_performed": False,
            "local_capability_score": None, "diagnostic_only": True, "promotion_eligible": False}


def _strict_count(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ProtocolError(f"{name} must be a nonnegative integer")
    return value


def summarize_curated(curated: Mapping) -> dict:
    """Import the authors' selected 8-round analyses, not a complete leaderboard."""
    rounds = curated.get("rounds")
    if not isinstance(rounds, dict) or not rounds:
        raise ProtocolError("curated round mapping required")
    by_model, unknown = {}, []
    for task, models in rounds.items():
        _identity(task)
        if not isinstance(models, dict) or not models:
            raise ProtocolError("empty round model mapping")
        for model, row in models.items():
            _identity(model)
            if not isinstance(row.get("success"), bool):
                raise ProtocolError("strict published success boolean required")
            score = row.get("score")
            if isinstance(score, bool) or not isinstance(score, (float, int)) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ProtocolError("finite [0,1] recorded score required")
            count = _strict_count(row.get("n_required"), "n_required")
            passed = _strict_count(row.get("n_required_passed"), "n_required_passed")
            checks = row.get("checks")
            if not isinstance(checks, list):
                raise ProtocolError("check list required")
            for c in checks:
                if c.get("role") not in {"required", "diagnostic"} or not isinstance(c.get("passed"), bool):
                    raise ProtocolError("invalid recorded check verdict")
            required = [c for c in checks if c["role"] == "required"]
            if count != len(required) or passed != sum(c["passed"] for c in required):
                raise ProtocolError("recorded required-check counts disagree")
            recomputed = all(c["passed"] for c in required) if count else None
            if recomputed is not None and recomputed != row["success"]:
                raise ProtocolError("published success disagrees with required verdicts")
            if count == 0:
                unknown.append({"round": task, "model": model, "reason": "no_required_checks_in_curated_record"})
            bucket = by_model.setdefault(model, {"records": 0, "published_successes": 0, "recorded_scores": []})
            bucket["records"] += 1
            bucket["published_successes"] += int(row["success"])
            bucket["recorded_scores"].append(score)
    return {"selected_rounds": len(rounds), "models": {
        model: {"records": r["records"], "published_successes": r["published_successes"],
                "selected_mean_recorded_score": sum(r["recorded_scores"])/r["records"]}
        for model, r in sorted(by_model.items())}, "unscorable_required_checks": unknown,
        "fairness_recomputed_from_curated": False,
        "limitation": "Curated records omit original check indices; do not join audit indices to list positions or infer full-corpus rates."}


def import_release(directory: Path) -> dict:
    release = load_release(directory)
    dead = release["analysis/dead_rounds_exclusion.json"]
    audit = release["analysis/v8_check_fairness_audit.json"]
    counts = Counter(tag for row in audit["checks"] for tag in row["in_sets"])
    if len(audit["checks"]) != audit["totals"]["checks_listed"]:
        raise ProtocolError("audit summary/check inventory mismatch")
    for tag, row in audit["sets"].items():
        if counts[tag] != row["checks"]:
            raise ProtocolError(f"audit set count mismatch: {tag}")
    conservative = audit_index(audit)
    if sum(map(len, conservative.values())) != 306:
        raise ProtocolError("pinned conservative audit set should have 306 checks")
    dead_counts = {corpus: len(row["pre_repair_unwinnable"]) for corpus, row in dead["corpora"].items()}
    curated = summarize_curated(release["docs/analysis/analysis_v8/curated_rounds.json"])
    costs = release["analysis/cost_high.json"]
    return {"schema_version": 2, "method": "clasharness", "kind": "official_reference_import",
            "upstream_revision": REVISION, "input_sha256": dict(FILE_HASHES),
            "audit": {"listed_checks": len(audit["checks"]), "set_counts": dict(counts),
                      "conservative_demoted_checks": 306, "pre_repair_dead_rounds": dead_counts,
                      "sensitivity": audit["sensitivity"], "sensitivity_is_upstream_report": True},
            "curated": curated, "cost_reference": {"effort": costs["effort"], "models": len(costs["models"]),
                "source": "authors' published cost estimates; not local spending"},
            "local_agent_executed": False, "local_capability_score": None,
            "diagnostic_only": True, "promotion_eligible": False,
            "full_experiment_status": "not_reproduced_high_cost"}
