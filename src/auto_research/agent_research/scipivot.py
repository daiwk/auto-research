"""SciPIvot public options-only boundary and strict paired-order grading.

No model calls, project records, training, or reference-aware policy live here.
The public prompt export is a separate artifact from the grader reference file.
"""
from __future__ import annotations

from collections import Counter
import csv
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import random

UPSTREAM_REVISION = "94a47d391893ea392fd9bb9883a65d2c8834e6f2"
BOOTSTRAP_SEED = 20261004
ORDERS = ("ab", "ba")


@dataclass(frozen=True)
class PublicCase:
    """Only the released option texts, never reference or project history."""

    case_id: str
    option_a: str
    option_b: str

    def prompt(self, order: str) -> str:
        if order not in ORDERS:
            raise ValueError("order must be ab or ba")
        a, b = (self.option_a, self.option_b) if order == "ab" else (self.option_b, self.option_a)
        return ("Below are two candidate next-step plans for a research project in a particular state. "
                "Please choose the one you think is better.\n\n"
                f"<option_A>\n(A) {a}\n</option_A>\n\n<option_B>\n(B) {b}\n</option_B>\n\n"
                'Output format:\n\n```\n{\n  "argument": "The reason for your choice",\n'
                '  "response": "A or B"\n}\n```\n')


def partition_release(rows: list[dict]) -> tuple[tuple[PublicCase, ...], dict[str, str]]:
    """Explicit allowlist at the grader-owned ingestion boundary."""
    public, references = [], {}
    for row in rows:
        cid = row["id"]
        if not isinstance(cid, str) or not cid or cid in references:
            raise ValueError("empty or duplicate case id")
        options = row["options"]
        if set(options) != {"A", "B"} or any(
                not isinstance(options[k], str) or not options[k].strip() for k in ("A", "B")):
            raise ValueError("two nonempty option texts required")
        if row["reference_answer"] not in ("A", "B"):
            raise ValueError("invalid grader reference")
        public.append(PublicCase(cid, options["A"], options["B"]))
        references[cid] = row["reference_answer"]
    if not public:
        raise ValueError("empty release")
    return tuple(public), references


def export_options_only(rows: list[dict], public_dir: Path, grader_dir: Path) -> dict:
    """Write disjoint artifacts; only public_dir may be mounted to an evaluator.

    This is not an OS sandbox: the caller must not give the evaluated process
    repository/parent-directory access. There is no evaluator invocation here.
    """
    public_dir, grader_dir = public_dir.resolve(), grader_dir.resolve()
    if public_dir == grader_dir or public_dir in grader_dir.parents or grader_dir in public_dir.parents:
        raise ValueError("public and grader directories must be disjoint")
    if public_dir.exists() or grader_dir.exists():
        raise FileExistsError("refuse to overwrite an evaluation export")
    cases, refs = partition_release(rows)
    public_dir.mkdir(parents=True)
    grader_dir.mkdir(parents=True, mode=0o700)
    prompts = [{"id": case.case_id, "order": order, "condition": "options-only",
                "prompt": case.prompt(order)} for case in cases for order in ORDERS]
    public_path, grader_path = public_dir / "prompts.jsonl", grader_dir / "references.json"
    public_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in prompts) + "\n")
    grader_path.write_text(json.dumps(refs, sort_keys=True) + "\n")
    grader_path.chmod(0o600)
    return {"cases": len(cases), "planned_runs": len(prompts), "condition": "options-only",
            "public_sha256": hashlib.sha256(public_path.read_bytes()).hexdigest(),
            "grader_sha256": hashlib.sha256(grader_path.read_bytes()).hexdigest(),
            "project_records_available": False, "evaluator_executed": False}


def _unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def parse_choice(raw) -> str | None:
    """Reject ambiguous, partial, or contradictory responses (no regex salvage)."""
    if raw in ("A", "B"):
        return raw
    if isinstance(raw, str):
        try:
            raw = json.loads(raw, object_pairs_hook=_unique_json)
        except (ValueError, TypeError):
            return None
    if isinstance(raw, dict) and raw.get("response") in ("A", "B"):
        return raw["response"]
    return None


def score_predictions(references: dict[str, str], predictions: list[dict], *,
                      resamples: int = 10000, seed: int = BOOTSTRAP_SEED) -> dict:
    """Both orders are always in the denominator, including missing/error runs."""
    if not references or any(v not in ("A", "B") for v in references.values()) or resamples < 2:
        raise ValueError("nonempty valid references and at least two bootstrap draws required")
    by_run, invalid = {}, 0
    for row in predictions:
        key = (row["id"], row["order"])
        if key[0] not in references or key[1] not in ORDERS:
            raise ValueError("prediction outside frozen case/order plan")
        if key in by_run:
            raise ValueError("duplicate case/order prediction")
        choice = None if row.get("error") or row.get("status") in {
            "timeout", "truncated", "missing", "provider_failure"} else parse_choice(row.get("response"))
        invalid += choice is None
        ref = references[key[0]]
        expected = ref if key[1] == "ab" else ("B" if ref == "A" else "A")
        by_run[key] = float(choice == expected)
    scores = [sum(by_run.get((cid, order), 0.) for order in ORDERS) / 2
              for cid in sorted(references)]
    rng = random.Random(seed)
    n = len(scores)
    boots = sorted(sum(scores[rng.randrange(n)] for _ in scores) / n for _ in range(resamples))
    return {"schema_version": 2, "implementation_status": "evaluation_protocol_interface",
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "condition": "options-only", "cases": n, "planned_runs": n * 2,
            "observed_runs": len(by_run), "missing_runs": 2 * n - len(by_run),
            "invalid_observed_runs": invalid, "accuracy": sum(scores) / n,
            "ci95": [boots[int(.025 * resamples)], boots[int(.975 * resamples) - 1]],
            "bootstrap": {"unit": "case", "resamples": resamples, "seed": seed},
            "weighting": "mean_of_two_orders_then_equal_cases", "case_scores": scores}


def audit_release(question_path: Path, aggregate_path: Path) -> dict:
    """Validate real released options and arithmetic in published aggregates.

    Per-run predictions are not released; their confidence intervals cannot be
    recomputed from aggregates and are never fabricated here.
    """
    public, references = partition_release(json.loads(question_path.read_text()))
    rows = list(csv.DictReader(aggregate_path.read_text().splitlines()))
    if len(public) != 248 or not rows:
        raise ValueError("unexpected official release size")
    keys, checked = set(), []
    for row in rows:
        key = (row["model"], row["arm"], row["effort"])
        if key in keys:
            raise ValueError("duplicate model/arm/effort aggregate")
        keys.add(key)
        n, cases, correct = int(row["n_runs"]), int(row["n_cases"]), int(row["correct"])
        if n != 496 or cases != 248 or not 0 <= correct <= n:
            raise ValueError("aggregate count outside frozen plan")
        if not math.isclose(float(row["run_accuracy"]), correct / n, abs_tol=1e-12):
            raise ValueError("aggregate arithmetic mismatch")
        unparsed = int(row["n_unparsed"])
        if not 0 <= unparsed <= n or correct > n - unparsed:
            raise ValueError("invalid unparsed/correct denominator")
        if not math.isclose(float(row["case_accuracy"]), correct / n, abs_tol=1e-12):
            raise ValueError("complete two-order aggregate case accuracy mismatch")
        if n > unparsed and not math.isclose(float(row["parsed_only_accuracy"]), correct / (n - unparsed), abs_tol=1e-12):
            raise ValueError("parsed-only aggregate arithmetic mismatch")
        if row["arm"] == "blind" and row["effort"] == "medium":
            checked.append({"model": row["model"], "correct": correct, "runs": n,
                            "official_options_only_accuracy": correct / n})
    return {"schema_version": 2, "implementation_status": "evaluation_protocol_interface",
            "evidence_kind": "official_release_dataset_and_aggregate_arithmetic_audit",
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "new_model_evaluated": False, "upstream_revision": UPSTREAM_REVISION,
            "cases": len(public), "planned_options_only_runs": len(public) * 2,
            "aggregate_rows_validated": len(rows), "official_medium_options_only": checked,
            "grader_reference_counts": dict(Counter(references.values())),
            "model_accuracy_recomputed_from_predictions": False,
            "project_records_available": False,
            "inputs": [{"file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                       for p in (question_path, aggregate_path)]}
