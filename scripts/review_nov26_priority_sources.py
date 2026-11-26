"""Persist the finite primary-source identity review; no exhaustive claim."""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov26-latest"
CACHE = ROOT / ".cache/nov26-latest"


def load(path):
    return json.loads(path.read_text())


def main():
    current = load(CACHE/"priority-audit/priority-source-captures.json")
    previous = load(ROOT/"docs/research-audits/nov25-latest/priority-source-captures.json")
    added = set(current["google_directory_delta"]["added"])-set(previous["google_directory_delta"]["added"])
    decisions = {
        "google-research/codegen-classroom": (None, "source_only_framework_no_new_verified_paper_identity", "README dates the iterative Gemini/Gemma code-generation framework to August2025 and supplies tasks/RSI workflow, not a verified new paper. Do not execute repository instructions or count a push as a publication."),
        "google-deepmind/cryptids": ("2610.22603", "existing_historical_identity_source_release", "README links the existing Busy Beaver autonomous-discovery paper. Formal Lean artifacts and new proofs are source-release evidence, not a new first publication or permission to rerun its campaign."),
        "google-deepmind/disco": ("2611.27104", "existing_paper_public_code_observed", "The official repository is now readable and names the already-cataloged DISCO paper. This source observation does not upgrade the local binary/unboosted component into complete LLM discovery, run API experiments, or rewrite earlier dated not-found observations."),
        "facebookresearch/sphere-encoder": ("2602.15030", "historical_paper_source_release_observation", "README identifies the February2026 Sphere Encoder paper, plus historical community/sequel links. A current push is not a new November publication; no model download or retrospective full run authorized here."),
        "facebookresearch/rlr_scale4d": (None, "new_official_technical_report_identity_date_limited_cost_done", "Official SCALE4D report datedNovember25 has an arXiv submission placeholder, not a public ID; first-public UTC unverified. Method/cost reviewed separately in scale4d-primary-report.json. Code and weights remain under legal review. Full campaign terminally not reproduced, no component or retry."),
    }
    sources = []
    for repository, (identity, decision, reason) in decisions.items():
        path = CACHE/"priority-readmes"/(repository.replace("/", "--")+".md")
        sources.append({"repository": repository, "source_url": "https://github.com/"+repository,
            "capture": path.relative_to(ROOT).as_posix(), "capture_sha256": sha256(path.read_bytes()).hexdigest(),
            "paper_arxiv_identity": identity, "decision": decision, "reason": reason,
            "read_scope": "README identity/release review, not full method review except the separately documented SCALE4D report"})
    value = {"schema_version": 1, "reviewed_on": "2026-11-26", "window": current["window"],
        "all_sources_exhaustive": False, "selected_priority_papers": [],
        "new_directory_urls_relative_to_previous_batch": len(added), "new_directory_urls": sorted(added),
        "official_pages": len(current["pages"]), "parse_complete_pages": sum(r.get("parse_complete") is True for r in current["pages"]),
        "repository_query_count": len(current["repository_events"]),
        "repository_event_observations": sum(len(r["items"]) for r in current["repository_events"]),
        "directory_limit": "The bounded directory inventory differs from the Nov15 baseline. Fifteen added URLs are inherited from earlier captures, not fifteen new papers today. Pagination/link differences do not establish paper deletion. Two incomplete Meta landing pages do not establish no new Meta work.",
        "google_new_blog": {"source_url": "https://research.google/blog/verifiable-social-reasoning-for-llm-assistants/", "blog_dated_on": "2026-11-25",
            "paper_url": "https://arxiv.org/abs/2609.17496", "paper_first_published_at": "2026-09-15T17:37:29Z",
            "existing_identity": "agent-research:fuse-evaluator", "decision": "already_cataloged_not_a_new_first_release",
            "reason": "Read the actual paper link and submission history; a new blog for Fuse and its21K-example release does not create a new paper identity."},
        "repository_primary_observations": sources,
        "scale4d_primary_report_review": "scale4d-primary-report.json",
        "industrial_priority": [{"identity": "recommendation:onequery", "source": "https://arxiv.org/pdf/2611.33653v1", "location": "Section5.6", "evidence": "Real AliExpress multi-country A/B against existing QU, L2P+0.5%, human SBS+0.8points; fraction/duration/CI undisclosed"},
            {"identity": "recommendation:camar", "source": "https://arxiv.org/pdf/2611.33628v1", "location": "SectionV-E/TableV", "evidence": "Two-week May2026 NetEase production A/B with CAMAR extra recall and same rankers; Song duration+1%, Playlist likes+3%, Podcast duration+1.6%; fraction/p/CI undisclosed"}],
        "limits": ["No global absence or exhaustive Google/Meta claim.", "Repository maintenance events outside the five primary identity checks are source-only observations, not fabricated full-paper decisions.", "No existing high-cost terminal campaign automatically reopened.", "Official arXiv metadata recall hitHTTP429 before the overlap boundary; this limitation is retained and the watermark does not advance."]}
    target = AUDIT/"priority-primary-selection.json"
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"new_google_directory_urls": len(added), "priority_primary_repository_checks": len(sources), "formal_priority_new_papers_selected": 0}))


if __name__ == "__main__":
    main()
