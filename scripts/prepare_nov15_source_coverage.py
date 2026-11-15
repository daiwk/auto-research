"""Preserve finite official recall receipts without creating a fake backlog."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov15-refresh"
AUDIT = ROOT / "docs/research-audits/nov15-refresh"


def write(name, payload):
    (AUDIT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main():
    pool = json.loads((CACHE / "announcement-pool.json").read_text())
    if len(pool["receipts"]) != 6 or any(not row["parse_complete"] for row in pool["receipts"]):
        raise ValueError("all six official capture pages must parse completely")
    receipts = [{k: v for k, v in row.items() if k != "path"} for row in pool["receipts"]]
    inventory = [{k: row.get(k) for k in ("canonical_id", "title", "entry_kind", "announced_on")}
                 for row in pool["candidates"]]
    write("announcement-index.json", {"schema_version": 1, "metadata_only": True,
                                     "scope": "Official November13 bulletin entries including replacements; not 1403 eligible papers or an implementation queue",
                                     "receipts": receipts, "identities": inventory})
    paper = CACHE / "root/2611.15137v1.html"
    write("source-coverage.json", {
        "schema_version": 1, "reviewed_on": "2026-11-15",
        "official_bulletin_date": "2026-11-13", "unique_metadata_identities": len(inventory),
        "metadata_inventory_is_implementation_backlog": False,
        "inventory": "announcement-index.json", "receipts": receipts,
        "coverage_limits": [
            "Exactly six current arXiv new/cross-list/replacement pages: cs.IR, cs.LG, cs.CL, cs.AI, cs.CV, cs.RO; not every arXiv category or every interval since the review watermark",
            "Selected full-text methods are separately source-bound in the fixed18-paper intake; unselected metadata is not labeled full-text reviewed",
            "Google/Meta author-name matches are recall signals, never affiliation evidence; primary bylines are versioned",
            "Official announcements can point to old papers; blog date does not replace original v1 publication date"
        ],
        "official_priority_checks": [
            {"organization": "Google", "source_url": "https://research.google/blog/2026/11/",
             "result": "Read visible November index and November13 teamwork article; Stellar Colosseum is historical backfill, product features are not new-paper algorithms"},
            {"organization": "Google DeepMind", "source_url": "https://deepmind.google/research/publications/",
             "result": "One bounded publication-page capture; not institution-exhaustive. AlphaProof Code already catalogued; LEAP is revised historical backfill"},
            {"organization": "Google DeepMind", "source_url": "https://deepmind.google/blog/opening-the-datasets-behind-our-ai-weather-models/",
             "result": "November13 PARDIG/SatWeave release describes weather-specific observations/datasets; outside current LLM/recommendation/Agent/JEPA selection; no generic algorithm is invented"},
            {"organization": "Google DeepMind", "source_url": "https://deepmind.google/blog/alphagenome-2-deciphering-how-cells-read-dna-to-better-understand-disease/",
             "result": "November11 biological sequence/condition model,107M cell profiles and domain genomics outputs; not selected into current topic scope"},
            {"organization": "Google DeepMind", "source_url": "https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/",
             "result": "Product/partner robotics announcement; no independently specified paper algorithm in the reviewed entry point. Retained as a source lead, not called implemented"},
            {"organization": "Meta", "source_url": "https://ai.meta.com/research/publications/",
             "result": "Official entry returned content unavailable; archived source exception, not evidence of no new Meta papers. Meta Unbundling is independently verified from fixed paper byline"}
        ],
        "source_exceptions": [
            {"source_url": "https://ai.meta.com/research/publications/", "resolution": "source_exception_archived", "automatic_retry": False},
            {"source_url": "https://github.com/cxli2333/KuaiRecV2", "resolution": "source_unavailable_archived",
             "reason": "Paper-linked repository returned404; do not claim downloadable code/data or a fully integrated benchmark", "automatic_retry": False}
        ],
        "sourceful_exclusions": [
            {"arxiv_id": "2611.15137", "title": "Serving-Aligned Entire-Space Conversion Modeling via Click-Through Rate Knowledge Distillation",
             "track": "recommendation", "reason": "Full text reports Ali-CCP offline CTR/CVR/CTCVR metrics and ten seeds, no quantified production A/B or qualifying full-traffic evidence. Not a user-approved classical exception; cheap KD arithmetic alone does not satisfy industrial intake.",
             "full_text_review": {"scope": "full-text", "version": "v1", "source_url": "https://arxiv.org/html/2611.15137v1",
                                  "source_sha256": hashlib.sha256(paper.read_bytes()).hexdigest(),
                                  "source_locations": ["byline", "method serving-space CTR KD", "experimental setup and results on Ali-CCP"]}},
            {"arxiv_id": "2611.15117", "title": "PolyMorphWBC: Whole-Body Control from End-Effector Trajectories for Quadrupedal Mobile Manipulation across Arm Morphologies with Extended Reach",
             "track": "agent", "reason": "Primary contribution is specialized morphology-generalized whole-body robot control, not the current LLM-agent/post-training/JEPA selection. Fixed v1 byline lists no institution; a familiar author name is not Google affiliation evidence.",
             "source_url": "https://arxiv.org/html/2611.15117v1", "review_scope": "primary-method-and-byline-selection"}
        ],
        "watermark_advanced": False, "all_sources_exhaustive": False,
        "full_campaign_policy": "Not reproduced due to high cost is review DONE; no model/data download or automatic retry. Theory-only no-experiment papers retain their actual status."
    })


if __name__ == "__main__":
    main()
