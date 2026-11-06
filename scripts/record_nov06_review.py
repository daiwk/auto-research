"""Publish the bounded Nov 5–6 bulletin review after component evidence is accepted."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import UTC, date, datetime
import hashlib
import json
from pathlib import Path
import re
import sys

from curate_nov04_components import aggregate_metrics
from curate_nov06_components import validate_raw
from run_nov06_components import AUDIT, COMPONENTS, CUDA_KEYS, ROOT, SEEDS, preflight

BATCH = "2026-11-06-priority-components"
DAY = "2026-11-06"
PREVIOUS_DAY = "2026-11-05"
DAYS = (PREVIOUS_DAY, DAY)
CATEGORIES = {"cs.AI", "cs.CL", "cs.CV", "cs.IR", "cs.LG", "cs.RO", "cs.SD", "eess.AS"}
PAPERS = {
    "convpe": "2611.07749",
    "cord-rollout": "2611.07959",
    "envopt": "2611.07372",
    "ice": "2611.07591",
    "pipnn-ii": "2611.05690",
    "ragcompass": "2611.05596",
    "ured": "2611.05997",
    "xstack": "2611.08472",
}
REFERENCES = set(PAPERS) - COMPONENTS.keys()
PRIORITY_REVIEW = "docs/research-audits/nov06-priority-components/priority-review.json"
BASELINE = "docs/research-audits/nov04-bulletin-components/source-coverage.json"
LEDGER = ROOT / "docs/paper-discovery-ledger.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def timestamp(raw: str) -> datetime:
    value = datetime.fromisoformat(raw)
    if value.tzinfo is None:
        raise ValueError("a time without an offset cannot establish chronology")
    return value.astimezone(UTC)


def identity(versioned: str) -> str:
    matched = re.fullmatch(r"(\d{4}\.\d{4,5})(?:v[1-9]\d*)?", versioned)
    if not matched:
        raise ValueError(f"invalid bulletin identity: {versioned!r}")
    return matched[1]


def validate_capture(pages: list[dict]) -> dict:
    expected_routes = {(category, route) for category in CATEGORIES for route in ("new", "recent")}
    if len(pages) != len(expected_routes) or {
        (page["category"], page["route"]) for page in pages
    } != expected_routes:
        raise ValueError("need exactly one new and one recent receipt per category")
    observations = defaultdict(list)
    recent = defaultdict(set)
    counts = Counter()
    nonreplacements = {}
    recent_nov06 = {}
    receipts = []
    for page in sorted(pages, key=lambda row: (row["category"], row["route"])):
        category, route = page["category"], page["route"]
        url = f"https://arxiv.org/list/{category}/{route}?show=2000"
        checked = timestamp(page["checked_at"])
        records = page["records"]
        sections = page["sections"]
        if page["url"] != url or page["status"] != "retrieved" or checked.date().isoformat() != DAY:
            raise ValueError(f"not an actual {DAY} capture of {url}")
        if route == "new":
            kinds = {"new", "cross-list", "replacement"}
            observed = Counter(r["entry_kind"] for r in records)
            if (
                page.get("announced_on") != DAY or page.get("parse_complete") is not True
                or not re.fullmatch(r"[0-9a-f]{64}", page.get("sha256", ""))
                or not page["expected_entries"] == page["parsed_entries"] == len(records)
                or any(r["announced_on"] != DAY for r in records)
                or len(sections) != len(kinds) or {s["kind"] for s in sections} != kinds
                or observed.keys() - kinds
                or any(not s["expected"] == s["shown"] == observed[s["kind"]] for s in sections)
            ):
                raise ValueError(f"bad new-bulletin counts/date: {url}")
            nonreplacements[category] = {
                identity(r["arxiv_id"]) for r in records if r["entry_kind"] != "replacement"
            }
            counts["new_route_category_entries"] += len(records)
            counts["new_route_replacement_entries"] += observed["replacement"]
        else:
            observed = Counter(r["announced_on"] for r in records)
            if (
                len(sections) != len(DAYS) or {s["announced_on"] for s in sections} != set(DAYS)
                or set(observed) != set(DAYS) or any(r["entry_kind"] != "recent-list" for r in records)
                or any(
                    s.get("parse_complete") is not True
                    or not s["expected_entries"] == s["parsed_entries"] == observed[s["announced_on"]]
                    for s in sections
                )
            ):
                raise ValueError(f"bad recent-bulletin counts/dates: {url}")
            recent_nov06[category] = {
                identity(r["arxiv_id"]) for r in records if r["announced_on"] == DAY
            }
            for day, count in observed.items():
                counts[f"recent_route_category_entries_{day}"] += count
        compact = []
        for record in records:
            arxiv_id, day, kind = (record[field] for field in ("arxiv_id", "announced_on", "entry_kind"))
            base_id = identity(arxiv_id)
            if route == "recent":
                recent[day].add(base_id)
            observations[base_id].append({
                "source_kind": "arxiv-announcement-list",
                "source_url": url,
                "category": category,
                "route": route,
                "entry_kind": kind,
                "announced_on": day,
                "listed_arxiv_id": arxiv_id,
            })
            compact.append({"arxiv_id": arxiv_id, "announced_on": day, "entry_kind": kind})
        receipts.append({k: v for k, v in page.items() if k != "records"} | {"identities": compact})
    if nonreplacements != recent_nov06:
        raise ValueError("Nov 6 non-replacement identities disagree across the two routes")
    if set(PAPERS.values()) - (recent[PREVIOUS_DAY] | recent[DAY]):
        raise ValueError("the fixed review cohort must all be evidenced by the captured announcements")
    return {
        "receipts": receipts,
        "observations": observations,
        "counts": dict(counts)
        | {f"recent_route_unique_identities_{day}": len(recent[day]) for day in DAYS}
        | {
            "unique_recent_route_identities": len(recent[PREVIOUS_DAY] | recent[DAY]),
            "unique_captured_identities_including_replacements": len(observations),
            "captured_identities_outside_this_fixed_review": len(observations) - len(PAPERS),
        },
    }


def load_specs() -> dict:
    result = {}
    for path in (ROOT / "src/auto_research/paper_specs/catalog").glob("*/*.json"):
        spec = read_json(path)
        key = spec["key"]
        if key in PAPERS:
            if key in result:
                raise ValueError(f"ambiguous catalog key: {key}")
            result[key] = spec
    if set(result) != set(PAPERS):
        raise ValueError("the fixed eight-paper catalog is incomplete")
    return result


def check_component(key: str, spec: dict, run: dict, frozen: dict) -> str:
    from auto_research.gpu_validation import load_gpu_receipt

    _, device = COMPONENTS[key]
    artifact = Path("docs") / Path(spec["detail_path"]).parent / f"metrics/component-{device}-seeds42-44.json"
    metric = read_json(ROOT / artifact)
    rows = run["components"][key]["per_seed"]
    provenance = metric.get("provenance", {})
    is_cuda = device == "cuda"
    if (
        spec.get("implementation_status") != "component_only"
        or not spec.get("local_operator")
        or spec.get("requires_gpu_validation") is not is_cuda
        or spec.get("gpu_validation_passed") is not is_cuda
        or metric.get("method") != key or metric.get("seeds") != SEEDS
        or metric.get("evaluation_tier") != "l1_mechanism" or metric.get("diagnostic_only") is not True
        or metric.get("formal_comparison") is not False
        or metric.get("promotion_eligible") is not False or metric.get("evolve_integrated") is not False
        or metric.get("per_seed") != rows or metric.get("metrics") != aggregate_metrics(rows)
        or provenance.get("commit") != frozen["commit"]
        or provenance.get("artifact_path") != artifact.as_posix()
        or provenance.get("accelerator") != run["accelerator"]
    ):
        raise ValueError(f"{key}: missing accepted metrics, flags, or matching frozen provenance")
    if is_cuda:
        path = spec.get("gpu_validation_artifact")
        if path != f"docs/gpu-validations/{key}-a100-20261106.json":
            raise ValueError(f"{key}: missing expected CUDA receipt path")
        receipt = load_gpu_receipt(ROOT / path)
        proof = receipt["provenance"]
        if (
            receipt["adapter_key"] != key or receipt["seeds"] != SEEDS
            or receipt.get("metrics") != metric["metrics"] or receipt.get("diagnostic_only") is not True
            or receipt["accelerator"]["model"] != run["accelerator"]
            or proof.get("metric_artifact_path") != artifact.as_posix()
            or proof.get("artifact_path") != path or proof.get("commit") != frozen["commit"]
        ):
            raise ValueError(f"{key}: GPU receipt does not match the executed component")
    elif spec.get("gpu_validation_artifact"):
        raise ValueError(f"{key}: CPU component must not claim GPU evidence")
    return artifact.as_posix()


def prepare(capture: Path) -> tuple[list[tuple[Path, dict]], dict]:
    specs = load_specs()
    captured = validate_capture(read_json(capture))
    observations = captured["observations"]
    watermark = read_json(ROOT / "docs/paper-discovery-watermark.json")["review_watermark"]
    date.fromisoformat(watermark)
    ledger = read_json(LEDGER)
    if any(batch["batch"] == BATCH for batch in ledger["batches"]):
        raise ValueError("the ledger already contains this batch")
    if any((AUDIT / name).exists() for name in ("task-scope.json", "source-coverage.json")):
        raise ValueError("accepted scope or coverage is already present")
    if (
        preflight()["batch"] != BATCH or set(preflight()["reference_only_keys"]) != REFERENCES
        or set(PAPERS) != set(COMPONENTS) | {"xstack"}
    ):
        raise ValueError("review cohort differs from fixed preflight")
    baseline = ROOT / BASELINE
    baseline_at = max(
        timestamp(row["checked_at"]) for row in read_json(baseline)["retrieval_receipts"] if row.get("checked_at")
    )
    first_checked_at = min(timestamp(p["checked_at"]) for p in captured["receipts"])
    if baseline_at >= first_checked_at:
        raise ValueError("the comparison baseline must predate these announcement captures")
    frozen = read_json(AUDIT / "frozen-sources.json")
    runs = {device: read_json(AUDIT / f"raw-{device}.json") for device in ("cpu", "cuda")}
    for device, raw in runs.items():
        validate_raw(raw, device, frozen)
    rows = []
    for key, arxiv_id in sorted(PAPERS.items()):
        spec = specs[key]
        primary = spec["reviewed_version_url"]
        submitted = timestamp(spec["published_at"])
        listings = [row for row in observations[arxiv_id] if row["entry_kind"] != "replacement"]
        announcement_days = sorted({row["announced_on"] for row in listings})
        if (
            not re.fullmatch(rf"https://arxiv\.org/(?:abs|html|pdf)/{re.escape(arxiv_id)}v1", primary)
            or identity(spec["paper_url"].rsplit("/", 1)[-1]) != arxiv_id
            or submitted.date().isoformat() != spec["published"] or submitted > first_checked_at
            or not announcement_days or submitted.date() > date.fromisoformat(announcement_days[0])
            or not any(row["listed_arxiv_id"] == f"{arxiv_id}v1" for row in listings)
            or not (ROOT / "docs" / spec["detail_path"]).is_file()
        ):
            raise ValueError(f"{key}: cannot establish distinct v1 publication and announcement evidence")
        component = key in COMPONENTS
        if (
            spec.get("review_done") is not True or spec.get("full_experiment_review_done") is not True
            or spec.get("full_experiment_status") != "not_reproduced_high_cost"
            or spec.get("promotion_eligible") is not False or spec.get("evolve_integrated") is not False
            or not spec.get("cost_assessment")
        ):
            raise ValueError(f"{key}: an explicit terminal high-cost review and no promotion required")
        row = {
            field: spec[field] for field in (
                "domain", "key", "title", "paper_url", "detail_path", "published", "published_at",
                "first_author", "first_author_affiliation", "priority", "cost_assessment",
                "implementation_status",
            )
        }
        row.update(
            id=arxiv_id, doc=spec["detail_path"], catalog_key=key, catalog_detail=spec["detail_path"],
            track={"agent-research": "agent", "foundation-models": "foundation-model"}.get(
                spec["domain"], spec["domain"]
            ),
            intake_class="observed_first_version_announcement_overlap",
            announced_on=announcement_days[0], observed_announcement_days=announcement_days,
            status="implemented" if component else "deferred",
            resolution="bounded_l1_component_accepted" if component else "not_reproduced_high_cost",
            component_implemented=component, component_accepted=component, review_done=True,
            first_publication_after_previous_capture=submitted > baseline_at,
            full_experiment_status="not_reproduced_high_cost", full_experiment_review_done=True,
            requires_gpu_validation=key in CUDA_KEYS, gpu_validation_passed=key in CUDA_KEYS,
            automatic_retry=False, automatic_implementation_queue=False, promotion_eligible=False,
            evolve_integrated=False,
            full_text_review={
                "scope": "defining method, cost, author affiliation/code and original figure; not every appendix claim",
                "full_article_read": False,
            },
            source_provenance=[
                {"source_kind": "reviewed-fixed-primary-paper", "source_url": primary},
                *listings,
            ],
        )
        if component:
            row["component_evidence"] = check_component(key, spec, runs[COMPONENTS[key][1]], frozen)
            if key in CUDA_KEYS:
                row["gpu_validation_artifact"] = spec["gpu_validation_artifact"]
        else:
            reason = spec.get("deferral_reason") or ""
            if (
                "不复现（审查 DONE）" not in reason or spec.get("implementation_status") != "deferred_high_cost"
                or spec.get("local_operator") is not None or spec.get("requires_gpu_validation")
                or spec.get("gpu_validation_passed") or spec.get("gpu_validation_artifact")
            ):
                raise ValueError(f"{key}: reference-only review needs an explicit reason and no pretend implementation")
            row["reason"] = reason
        rows.append(row)

    counts = captured["counts"] | {
        "selected_papers": len(PAPERS),
        "component_implementations": len(COMPONENTS),
        "cuda_validated_components": len(CUDA_KEYS),
        "cpu_only_components": len(COMPONENTS) - len(CUDA_KEYS),
        "reference_only_high_cost_review_done": len(REFERENCES),
        "selected_first_publications_after_previous_capture": sum(
            row["first_publication_after_previous_capture"] for row in rows
        ),
        "full_capability_reproductions": 0,
    }
    common = {
        "schema_version": 1, "batch": BATCH, "selected_scope_complete": True,
        "delivery_status": "bounded_scope_complete", "all_sources_exhaustive": False,
        "review_watermark_advanced": False, "review_watermark": {"before": watermark, "after": watermark},
        "counts": counts,
    }
    scope = common | {
        "fixed_component_keys": sorted(COMPONENTS), "reference_only_keys": sorted(REFERENCES),
        "papers": rows,
    }
    coverage = common | {
        "checked_on": DAY, "announcement_days": list(DAYS), "baseline": BASELINE,
        "baseline_sha256": digest(baseline), "baseline_last_checked_at": baseline_at.isoformat(),
        "raw_capture_sha256": digest(capture), "retrieval_receipts": captured["receipts"],
        "new_recent_nov06_nonreplacement_identities_equal": True,
        "full_bulletin_full_text_review_complete": False,
        "priority_institution_review_artifact": PRIORITY_REVIEW,
        "limitations": [
            "This is eight fixed, reviewed identities, not full-text review of every captured identity.",
            "Publication is the fixed v1 UTC timestamp; arXiv announcement day and capture time are separate.",
            "Counts sum categories and cross-lists where stated; unique identities deduplicate version suffixes.",
            "Unreviewed or unavailable sources are not zero qualifying papers; see the separate priority evidence.",
            "L1 diagnostics are not model capability, production lift, serving speed or Evolve integration.",
            "High-cost complete experiments are review DONE/not reproduced, with no automatic retry queue.",
        ],
    }
    ledger["batches"].append(common | {
        "date": DAY, "source_artifact": "research-audits/nov06-priority-components/README.md",
        "candidates": rows,
    })
    return [
        (AUDIT / "source-coverage.json", coverage),
        (AUDIT / "task-scope.json", scope),
        (LEDGER, ledger),
    ], counts


def main() -> None:
    sys.path.insert(0, str(ROOT / "src"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path, help="path to the reviewed captured.json")
    parser.add_argument("--dry-run", action="store_true", help="validate without writing audit or ledger files")
    args = parser.parse_args()
    outputs, counts = prepare(args.capture)
    if not args.dry_run:
        # Serialize every output before writing anything; the ledger is written last.
        encoded = [
            (path, json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
            for path, payload in outputs
        ]
        for path, payload in encoded:
            with path.open("w" if path == LEDGER else "x", encoding="utf-8") as output:
                output.write(payload)
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
