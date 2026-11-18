"""Materialize bounded source receipts from already retrieved public captures."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from bs4 import BeautifulSoup

from run_nov12_components import AUDIT, BATCH, ROOT, write_new
from record_nov12_components import specifications

PAPERS = {
    "agent-gym": ("agent/agent-gym-v3", "§3.4.3 and §3.5, ALF engine; author block and experiments"),
    "bats": ("agent/bats-v2", "§4, Eq.2, Appendix B/D; author block and experimental budgets"),
    "bopd": ("post-training/2611.13680v1", "Eqs.4/7, Algorithm1, Appendix A; author block and configuration"),
    "apmd-reference-reset": ("post-training/2611.14467v1", "§3.1, §4.1-4.3, Eqs.13/36/37/42/44, Appendix C; author block"),
    "lcs-reference-opd": ("post-training/2611.13135v1", "§3, Appendices A/D/I/J; author block, reference selection and cost"),
    "real-loss": ("foundation/real", "defining EAL estimators, counterexample, Eqs.9/15/16/19; byline and experiment requirements"),
    "c2-routing": ("foundation/c2-routing", "joint-correctness harm/benefit, validation utility and FLOP protocol; byline and configuration"),
    "onlyact": ("foundation/onlyact", "scene-swapped positives, same-video negatives, full contrastive bank and fixed projection; byline and training setup"),
}


def receipt(path, url):
    return {"capture": path.relative_to(ROOT).as_posix(), "source_url": url,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}


def decoded(path):
    data = path.read_bytes()
    return (gzip.decompress(data) if data.startswith(b"\x1f\x8b") else data).decode("utf-8")


def urls(path, kind):
    parsed = BeautifulSoup(decoded(path), "html.parser")
    if kind == "google":
        return sorted({a["href"] for a in parsed.select("a[href]") if "/pubs/" in a["href"]
                       and "?" not in a["href"] and a["href"].rstrip("/") != "/pubs"})
    return sorted({a["href"] for a in parsed.select("a[href]") if len(a.get_text(" ", strip=True)) > 15
                   and any(part in a["href"] for part in ("/blog/", "/research/", "/publications/"))})


def main():
    cache = ROOT / ".cache/nov12-components"
    specs = specifications()
    primary = {}
    for key, (stem, sections) in PAPERS.items():
        html_url = specs[key]["reviewed_version_url"]
        primary[key] = {"reviewed_version_url": html_url, "reviewed_sections": sections,
                        "whole_paper_verified": False, "captures": [
                            receipt(cache / (stem + ".html"), html_url),
                            receipt(cache / (stem + ".pdf"), html_url.replace("/html/", "/pdf/")),
                        ]}
    write_new(AUDIT / "primary-source-receipts.json", {"schema_version": 1, "checked_on": "2026-11-12",
                                                       "papers": primary})
    index = json.loads((AUDIT / "announcement-index.json").read_text())
    captures = [{key: row[key] for key in ("capture", "source_url", "sha256", "bytes")}
                for row in index["sources"]]
    differences = []
    configs = [
        ("Google first page", "google2026-first-exact", "google2026-first", "google",
         "https://research.google/pubs/?category=2026&sort=-publication__year"),
        ("Google last page", "google2026-last", "google2026-last", "google",
         "https://research.google/pubs/?category=2026&sort=-publication__year&page=31"),
        ("Meta curated research home", "meta-research-home", "meta-home", "research",
         "https://research.meta.ai/"),
        ("DeepMind publications landing", "deepmind-publications", "deepmind-publications", "research",
         "https://deepmind.google/research/publications/"),
    ]
    for label, current, prior, kind, url in configs:
        path = cache / "priority" / (current + ".html")
        previous = ROOT / ".cache/nov11-components/priority" / (prior + ".html")
        old, new = urls(previous, kind), urls(path, kind)
        if not old or not new:
            raise ValueError("zero parsed links is not evidence of zero added links")
        differences.append({"source": label, "source_url": url, "previous_urls": old, "current_urls": new,
                            "added_urls": sorted(set(new) - set(old)), "removed_urls": sorted(set(old) - set(new)),
                            "previous_capture_sha256": hashlib.sha256(previous.read_bytes()).hexdigest(),
                            "current_capture_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "decoded_body_unchanged": decoded(previous) == decoded(path),
                            "coverage": "bounded pages, not an institution-wide census"})
        captures.append(receipt(path, url))
    path = cache / "priority/meta-publications.html"
    captures.append(receipt(path, "https://ai.meta.com/research/publications/"))
    coverage = {
        "schema_version": 1, "batch": BATCH, "checked_on": "2026-11-12", "announcement_date": "2026-11-11",
        "scope_kind": "bounded-component-intake", "all_sources_exhaustive": False,
        "full_window_review_complete": False, "review_watermark_advanced": False,
        "review_watermark": {"before": "2026-11-09", "after": "2026-11-09"},
        "baseline": "research-audits/nov11-components/source-coverage.json",
        "capture_receipts": captures, "official_page_differences": differences,
        "announcement_index": "research-audits/nov12-components/announcement-index.json",
        "official_limitations": [
            "All eight official new lists still show November 11; recent/date checks did not establish a November 12 announcement.",
            "The Google first/last pages contain 15/12 papers; their empty URL difference is not a full-site absence claim.",
            "The Meta main directory again returned unavailable content. Its alternate results page was readable through web rendering, but direct capture timed out and visible ordering mixes historical years.",
            "The Meta curated home and DeepMind landing show no added links within the saved bounded comparison; neither is a publication census.",
            "956 cross-listed/replacement-inclusive identities are a source index, not 956 qualifying new papers or accepted tasks. Unselected identities are not method-reviewed or automatically queued.",
        ],
        "meta_fallback": {"url": "https://ai.meta.com/results/?content_types%5B0%5D=publication",
                          "web_rendering": "readable", "local_capture": "45-second timeout",
                          "top_visible_publication": "GSLM2, November 4, already catalogued",
                          "chronological_exhaustiveness": False},
        "selected_scope": {"components": 8, "same_announcement_carryover": 6, "official_historical_backfills": 2,
                           "new_first_publications_since_prior_delivery": 0, "large_empirical_cost_deferrals": 7,
                           "theory_only_no_large_empirical_protocol": 1},
        "industrial_exception": "research-audits/nov12-components/industrial-source-exception.json",
        "automatic_implementation_queue": False,
    }
    write_new(AUDIT / "source-coverage.json", coverage)
    print("captured eight primary reviews and bounded announcement/official-page receipts")


if __name__ == "__main__":
    main()
