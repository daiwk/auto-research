"""Fix the finite accepted scope separately from metadata recall and old papers."""

from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov19-latest"
CACHE = ROOT / ".cache/nov19-latest"


def load(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def main():
    identities = [
        r["paper"]
        for name in ("foundation", "post", "agent", "root")
        for r in load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"]
    ]
    if len(identities) != 23 or len(set(identities)) != 23:
        raise ValueError("fixed23-paper intake missing/duplicated")
    specs = {
        i: load(ROOT / "src/auto_research/paper_specs/catalog" / f"{i.replace(':', '/')}.json")
        for i in identities
    }
    components = {i: p for i, p in specs.items() if p["implementation_status"] == "component_only"}
    reviews = {i: p for i, p in specs.items() if p["implementation_status"] == "deferred_high_cost"}
    if len(components) != 18 or len(reviews) != 5:
        raise ValueError("expected18components/5review-only")
    intake = {
        "schema_version": 1,
        "batch": "2026-11-19-latest-components",
        "requested_window": {"start": "2026-11-18", "end": "2026-11-19"},
        "accepted_papers": sorted(specs),
        "component_papers": sorted(components),
        "review_only_papers": sorted(reviews),
        "new_papers": [i for i, p in specs.items() if p["published"] >= "2026-11-18"],
        "announcement_overlap_backfill": ["multimodal-models:autoregressive-view-model"],
        "historical_directory_backfill": ["agent-research:searchinject"],
        "supplemental_cpu_papers": ["system-one:egojev"],
        "scope_note": "Finite high-value primary-method review, not full-text review of every metadata identity or institution-wide exhaustion. API publication, bulletin announcement, directory observation and repository pushes are separate events.",
        "all_sources_exhaustive": False,
        "watermark_advanced": False,
        "scan_coverage_changed": False,
        "cost_policy": "High-cost full experiments not reproduced; review DONE, terminal and no automatic retry/implementation queue.",
    }
    dump(AUDIT / "intake-scope.json", intake)
    config = {
        p["key"]: {
            "domain": p["domain"],
            "module": p["local_operator"]
            .removeprefix("auto_research.")
            .removesuffix(".diagnostic")
            .replace(".", "/")
            + ".py",
            "evaluation_tier": p["evaluation_tier"],
            "cuda": p["requires_gpu_validation"],
        }
        for p in components.values()
        if p["key"] != "egojev"
    }
    dump(
        AUDIT / "preflight.json",
        {
            "schema_version": 1,
            "batch": intake["batch"],
            "seeds": [42, 43, 44],
            "maximum_run_seconds": 180,
            "maximum_cuda_devices": 1,
            "model_and_dataset_downloads": 0,
            "api_calls": 0,
            "automatic_retry": False,
            "full_experiments_executed": False,
            "scope": "Seventeen bounded L0/L1 protocol/formula diagnostics only. No pretrained model, generator, paid API, public capability benchmark or Evolve promotion.",
            "cost_sources": [
                "foundation-review.json",
                "post-review.json",
                "agent-review.json",
                "root-review.json",
            ],
            "components": config,
        },
    )
    api = load(CACHE / "metadata-pool.json")
    bulletin = load(CACHE / "announcement-pool.json")
    dump(
        AUDIT / "metadata-index.json",
        {
            "schema_version": 1,
            "metadata_only": True,
            "captured_at": api["captured_at"],
            "requested_window": api["requested_window"],
            "overlap_start_utc": api["overlap_start_utc"],
            "categories": api["categories"],
            "coverage_complete_to_overlap_boundary": api["coverage_complete_to_overlap_boundary"],
            "all_sources_exhaustive": False,
            "metadata_inventory_is_implementation_backlog": False,
            "receipts": api["receipts"],
            "identities": [
                {
                    k: r.get(k)
                    for k in ("canonical_id", "title", "published", "updated", "repository_status")
                }
                for r in api["papers"]
            ],
            "announcement_receipts": bulletin["receipts"],
            "announced_identities": bulletin["identities"],
        },
    )
    dump(
        AUDIT / "source-coverage.json",
        {
            "schema_version": 1,
            "reviewed_on": "2026-11-19",
            "requested_window": api["requested_window"],
            "metadata_identities": len(api["papers"]),
            "announcement_identities": len(bulletin["identities"]),
            "metadata_only_inventory": "metadata-index.json",
            "overlap_start_utc": api["overlap_start_utc"],
            "priority_source_captures": "priority-source-captures.json",
            "fixed_intake": "intake-scope.json",
            "all_sources_exhaustive": False,
            "watermark_advanced": False,
            "coverage_limits": [
                "Nine configured arXiv categories with overlapping updated-date recall, plus current bulletins and finite official directories; not every source/venue.",
                "529 metadata identities initially marked new with publication since Nov18 are a selection pool, not an implementation backlog.",
                "Full-text review is limited to accepted papers and explicit primary-source exclusions.",
                "Meta publication landing page returns45bytes withHTTP200; archive this nonblocking source exception rather than infer no new Meta work.",
                "Newly observed Google SearchInject directory listing is a Nov2historical backfill, not a Nov19publication.",
            ],
        },
    )
    exclusions = []
    for aid, locations, reason in [
        (
            "2611.24757",
            ["§3 method", "§4 synthetic environment", "§5 results"],
            "Policy A/B design is evaluated with simulations, not a new production A/B. Not selected for industrial reproduction; do not promote the title A/B phrase into production evidence.",
        ),
        (
            "2611.24426",
            ["fixed-v1 author byline", "§5 TGB experiments"],
            "DyNA-Mixer reports academic dynamic graph benchmarks, not qualifying industrial online A/B. Not selected in this finite industrial intake.",
        ),
    ]:
        path = CACHE / "root" / (aid + "v1.html")
        exclusions.append(
            {
                "arxiv_id": aid,
                "source_url": f"https://arxiv.org/html/{aid}v1",
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "source_locations": locations,
                "review_scope": "selected_primary_method_and_industrial_evidence",
                "decision": "not_selected_industrial_online_evidence_gate",
                "reason": reason,
                "automatic_retry": False,
                "automatic_implementation_queue": False,
            }
        )
    dump(
        AUDIT / "priority-primary-selection.json",
        {
            "schema_version": 1,
            "reviewed_on": "2026-11-19",
            "priority_admissions": {
                "recommendation:mle-agents": "Fixed-v1 byline explicitly Meta Platforms; §1.3 actual productionA/B with guardrail regression preserved.",
                "multimodal-models:autoregressive-view-model": "Fixed-v1 first author Meta/Oxford; high-cost8Mscene/video campaign review-only.",
                "agent-research:searchinject": "Fixed-v1 Google LLC first author; newly observed official directory, historicalNov2paper; exposure not attack-success.",
            },
            "affiliation_corrections": {
                "foundation-models:counterfactual-wm": "Brown/AMI Labs and NYU/AMI Labs in fixed PDF; familiar names do not make this a Meta paper.",
                "recommendation:xsplit-argus": "No institution in fixed byline; do not infer Yandex from an earlier ARGUS paper.",
            },
            "primary_source_exclusions": exclusions,
            "repository_event_policy": "Push events are not new papers; zero newly-created repos in the three checked official organizations is only a query result, not evidence of no new research.",
            "all_sources_exhaustive": False,
        },
    )
    print(
        json.dumps(
            {
                "accepted": len(specs),
                "components": len(components),
                "cuda": sum(x["cuda"] for x in config.values()),
                "review_only": len(reviews),
            }
        )
    )


if __name__ == "__main__":
    main()
