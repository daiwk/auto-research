"""Freeze the selected review scope separately from broad metadata recall."""

from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov18-latest"
CACHE = ROOT / ".cache/nov18-latest"


def load(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    proposals = [
        r
        for name in ("foundation", "post", "agent", "root")
        for r in load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"]
    ]
    identities = [r["paper"] for r in proposals]
    if len(identities) != 47 or len(set(identities)) != 47:
        raise ValueError("fixed47-paper intake incomplete or duplicated")
    specs = {}
    for identity in identities:
        domain, key = identity.split(":", 1)
        specs[identity] = load(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json")
    components = {k: p for k, p in specs.items() if p["implementation_status"] == "component_only"}
    reviews = {
        k: p
        for k, p in specs.items()
        if p["implementation_status"] in {"review_only", "deferred_high_cost"}
    }
    if len(components) != 35 or len(reviews) != 12:
        raise ValueError("35component/12review-only scope required")
    intake = {
        "schema_version": 1,
        "batch": "2026-11-18-latest-components",
        "requested_window": {"start": "2026-11-16", "end": "2026-11-18"},
        "accepted_papers": sorted(specs),
        "component_papers": sorted(components),
        "review_only_papers": sorted(reviews),
        "new_papers": [k for k, p in specs.items() if p["published"] >= "2026-11-16"],
        "historical_new_code": ["foundation-models:efficient-evals-tensor"],
        "scope_note": "Finite selected primary-method review and affordable delivery; broad metadata is not an eligible-paper or implementation backlog. Historical new-code release is separate from new publication.",
        "all_sources_exhaustive": False,
        "watermark_advanced": False,
        "scan_coverage_changed": False,
        "cost_policy": "High-cost full campaigns are explicitly not reproduced and review DONE; no automatic retry/implementation queue. Bounded L0/L1 components do not become capability evidence.",
    }
    dump(AUDIT / "intake-scope.json", intake)
    api = load(CACHE / "metadata-pool.json")
    announcement = load(CACHE / "announcement-pool.json")
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
            "receipts": [
                {k: v for k, v in r.items() if k not in {"path", "cache_path"}}
                for r in api["receipts"]
            ],
            "identities": [
                {
                    k: r.get(k)
                    for k in ("canonical_id", "title", "published", "updated", "repository_status")
                }
                for r in api["papers"]
            ],
            "announcement_receipts": [
                {k: v for k, v in r.items() if k not in {"path", "cache_path"}}
                for r in announcement["receipts"]
            ],
            "announced_identities": announcement.get(
                "identities", announcement.get("candidates", announcement.get("papers", []))
            ),
        },
    )
    root = CACHE / "root"

    def source(aid, locations, reason, decision):
        path = root / (aid + "v1.html")
        if not path.exists():
            path = root / (aid + "v1.pdf")
        return {
            "arxiv_id": aid,
            "source_url": f"https://arxiv.org/{'html' if path.suffix == '.html' else 'pdf'}/{aid}v1",
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "source_locations": locations,
            "review_scope": "primary-method/byline-and-production-evidence-selection",
            "decision": decision,
            "reason": reason,
            "automatic_retry": False,
            "automatic_implementation_queue": False,
        }

    priority = [
        source(
            "2611.21920",
            [
                "v1 MRS author byline",
                "§3.3 system design",
                "§4.1 setup",
                "§4.2–4.4 ranking/fidelity/serving",
                "Appendix C/D limitations and gates",
            ],
            "KVUse is genuinely Meta Recommendation Systems, not inferred from familiar names. Fixed v1 reports memory-chain/profile/throughput experiments, but no quantified randomized production A/B or qualifying explicit full-traffic evaluation was found. Offline production-like serving is not the industrial intake gate. Not selected as a capability reproduction; do not route around the gate with a tiny cache mock.",
            "industrial_online_evidence_gate_not_met",
        ),
        source(
            "2611.22309",
            [
                "PDF p1 LinkedIn byline",
                "§6.1 production-derived replay and output overlap",
                "§6.2/6.5 H200 throughput",
                "Appendix B validation and limitations",
            ],
            "LinkedIn, not Google/Meta. H200 production-derived replay is not live A/B; paper explicitly does not establish unchanged relevance or full pipeline reduction. Proposed SGLang contribution44349 and private checkpoints/catalogs are recorded without claiming an available complete reproduction.",
            "industrial_online_evidence_gate_not_met",
        ),
        source(
            "2611.20721",
            ["§5 CARE-SID/R3-VAE", "§6 CARE-LR", "§7 experiments", "§8 Deployment in Video Search"],
            "Tencent authors and an actual deployment section verified. It explains generative SID serving and refreshing mappings but provides no quantified production A/B or explicit qualifying full-traffic outcome. Deployment wording alone does not satisfy the industrial evidence gate.",
            "industrial_online_evidence_gate_not_met",
        ),
        source(
            "2611.22163",
            [
                "method trust-region decoding",
                "experiments including Efficiency and Production Deployment",
            ],
            "The production heading discusses deployment-friendly properties and local1.6–2.5ms inference, not a production randomized experiment; production conditions remain unevaluated.",
            "industrial_online_evidence_gate_not_met",
        ),
        source(
            "2611.22410",
            [
                "verbal feedback and joint GRPO method",
                "Amazon offline experimental setup/results",
                "references",
            ],
            "VerRec reports offline public Amazon experiments; the A/B string occurs in cited prior work, not a new production experiment.",
            "industrial_online_evidence_gate_not_met",
        ),
    ]
    dump(
        AUDIT / "priority-primary-selection.json",
        {
            "schema_version": 1,
            "reviewed_on": "2026-11-18",
            "reviews": priority,
            "google_new_repository": {
                "url": "https://github.com/google-deepmind/efficient_evals",
                "created_at": "2026-11-16T14:47:11Z",
                "paper": "2603.02029",
                "published_at": "2026-03-02T16:12:46Z",
                "resolution": "historical_new_code_accepted",
                "first_author_affiliation": "University of Michigan",
                "verified_collaborator": "Google DeepMind",
                "revision": "b4421d929d1078631ee890f8e4a776442c816d36",
            },
            "google_tool_release": {
                "url": "https://github.com/google-deepmind/robotics-antigravity-plugin",
                "created_at": "2026-11-16T18:50:28Z",
                "resolution": "not_a_separate_paper_method",
                "reason": "Official README describes a robotics tool/skill release and examples; not a distinct specified research-paper algorithm. Nothing installed or executed.",
            },
            "meta_new_paper": {
                "id": "2611.21839",
                "key": "vishead-spec",
                "verified_byline": "Meta Recommendation Systems (MRS)",
                "resolution": "bounded_component_accepted",
            },
            "limitations": [
                "Familiar author names and official directory membership are recall signals, not affiliation proof.",
                "Official Google directory URLs mix absolute and relative links; both are normalized and tested.",
                "Meta publication entry can return45-byte unavailable content withHTTP200; this is an archived nonblocking exception, not evidence of no new Meta papers.",
            ],
        },
    )
    dump(
        AUDIT / "source-coverage.json",
        {
            "schema_version": 1,
            "reviewed_on": "2026-11-18",
            "requested_window": api["requested_window"],
            "reviewed_overlap_start_utc": api["overlap_start_utc"],
            "metadata_only_inventory": "metadata-index.json",
            "metadata_identities": len(api["papers"]),
            "announcement_identities": len(
                announcement.get(
                    "identities", announcement.get("candidates", announcement.get("papers", []))
                )
            ),
            "priority_source_captures": "priority-source-captures.json",
            "priority_primary_selection": "priority-primary-selection.json",
            "fixed_intake": "intake-scope.json",
            "metadata_inventory_is_implementation_backlog": False,
            "all_sources_exhaustive": False,
            "watermark_advanced": False,
            "coverage_limits": [
                "Nine configured arXiv categories, updated-date API pages exhausted to Nov13 overlap boundary, plus current official bulletin pages; not every scholarly venue.",
                "Full-text method review is limited to selected papers and explicitly listed sourceful exclusions. Unselected metadata is not described as full-text reviewed or as a delivery queue.",
                "Announcement/publication/revision/new-code dates remain separate. Today bulletin may announce yesterday submissions.",
                "Google/Meta official directory/repository deltas supplement arXiv; directories can be delayed or unavailable and do not establish institution-wide exhaustion.",
            ],
        },
    )
    print(
        json.dumps(
            {
                "accepted": len(specs),
                "components": len(components),
                "review_only": len(reviews),
                "new_papers": len(intake["new_papers"]),
                "historical_new_code": 1,
            }
        )
    )


if __name__ == "__main__":
    main()
