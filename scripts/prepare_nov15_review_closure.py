"""Freeze the Nov10--15 review pool; recall is not paper-method review."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from auto_research.discovery import repository_paper_records
from auto_research.discovery_review import priority_organizations
from auto_research.papers import ArxivClient, canonical_arxiv_id
from screen_nov09_p2_selection import protection_signals

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov15-closure"
AUDIT = ROOT / "docs/research-audits/nov15-review-closure"
WINDOW = {"start": "2026-11-10", "end": "2026-11-15"}
RUN = "43827485506"
TRACKS = ("recommendation", "foundation-model", "post-training", "agent")
MODES = {"submission-window": "candidates", "late-index": "late-index"}


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def local_day(value: str) -> str:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(ZoneInfo("Asia/Shanghai")).date().isoformat()


def metadata_digest(row: dict) -> str:
    value = {"title": " ".join(row["title"].split()), "abstract": " ".join(row["abstract"].split()),
             "authors": [" ".join(author.split()) for author in row["authors"]]}
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def repair_llm() -> None:
    """Actually split the capped month union, preserving every query report."""
    client = ArxivClient(minimum_interval_seconds=3, maximum_retries=2,
                         cache_dir=CACHE / "arxiv", checkpoint_dir=CACHE / "replacement-progress", resume=True)
    for month in ("2610", "2611"):
        path = CACHE / f"llm-{month}-replacement.json"
        if path.exists():
            continue
        papers = client.search_pages("LLM", categories=("cs.CL", "cs.LG"),
                                     page_size=200, maximum_results=10000, identifier_months=(month,))
        from dataclasses import asdict
        write(path, {"schema_version": 1, "query": client.query_reports[-1],
                     "captured_on": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
                     "papers": [asdict(p) for p in papers]})
        print(month, len(papers), client.query_reports[-1]["state"], flush=True)


def prepare() -> dict:
    observed, receipts = {}, []
    for track in TRACKS:
        for mode, prefix in MODES.items():
            path = CACHE / "captures" / RUN / f"{track}-paper-candidates" / f"paper-{prefix}-{track}.json"
            payload = json.loads(path.read_bytes())
            receipt = {"run_id": RUN, "track": track, "mode": mode,
                       "capture": path.relative_to(CACHE).as_posix(),
                       "artifact_sha256": sha256(path.read_bytes()).hexdigest(),
                       "captured_window": payload["window"], "queries": payload["arxiv_transport"]["queries"]}
            receipts.append(receipt)
            rows = payload["candidates"]
            for row in rows:
                identity = canonical_arxiv_id(row["arxiv_id"])
                rank = (row.get("revision") or 1, row.get("updated", ""))
                if identity not in observed:
                    observed[identity] = {"row": row, "rank": rank, "tracks": set(), "captures": []}
                record = observed[identity]
                record["tracks"].add(track)
                record["captures"].append(receipt["capture"])
                if rank > record["rank"]:
                    record.update(row=row, rank=rank)
    for month in ("2610", "2611"):
        path = CACHE / f"llm-{month}-replacement.json"
        if not path.exists():
            continue
        payload = json.loads(path.read_bytes())
        query = payload["query"]
        if not (query["state"] == "exhausted" and query["coverage_complete"]
                and query["transport_complete"] and not query["cache_fallback_pages"]):
            raise ValueError("replacement is not actually exhausted")
        receipts.append({"track": "foundation-model", "mode": "late-index", "replacement_month": month,
                         "source_path": path.relative_to(ROOT).as_posix(), "source_sha256": sha256(path.read_bytes()).hexdigest(),
                         "query": query, "captured_on": payload["captured_on"]})
        for row in payload["papers"]:
            identity = canonical_arxiv_id(row["arxiv_id"])
            rank = (row.get("revision") or 1, row.get("updated", ""))
            if identity not in observed:
                observed[identity] = {"row": row, "rank": rank, "tracks": set(), "captures": []}
            record = observed[identity]
            record["tracks"].add("foundation-model")
            record["captures"].append(path.relative_to(ROOT).as_posix())
            if rank > record["rank"]:
                record.update(row=row, rank=rank)
    supplement = CACHE / "supplemental-metadata.json"
    if supplement.exists():
        payload = json.loads(supplement.read_bytes())
        if payload["window"] != WINDOW:
            raise ValueError("independent source has wrong window")
        for row in payload["records"]:
            identity = canonical_arxiv_id(row["arxiv_id"])
            source = row["metadata_source"]
            if sha256((ROOT / source["capture"]).read_bytes()).hexdigest() != source["source_sha256"]:
                raise ValueError("independent metadata source bytes changed")
            observed[identity] = {"row": row | {"priority_review_required": True,
                                      "source_provenance": [{"organization": "Google", "source_url": source["source_url"]}]},
                                  "rank": (row["revision"], row["updated"]),
                                  "tracks": {"foundation-model"}, "captures": [source["capture"]]}
            receipts.append({"source_kind": "independent-official-source-exact-identity", "id": identity, **source})
    known = repository_paper_records(ROOT / "docs/research-manifest.json", ROOT / "docs/paper-discovery-ledger.json")
    primary_recalled = {"2611.13442": "Meta official ForeSpark source", "2611.17501": "plausible Meta recommendation hardware authors", "2611.16028": "Google verified author co-occurrence"}
    rows = []
    for identity, value in sorted(observed.items()):
        row = value["row"]
        digest = metadata_digest(row)
        if row.get("metadata_sha256") and row["metadata_sha256"] != digest:
            raise ValueError(f"Captured metadata digest mismatch: {identity}")
        row = row | {"metadata_sha256": digest}
        dates = [local_day(row[k]) for k in ("published", "updated") if row.get(k)]
        in_window = any(WINDOW["start"] <= d <= WINDOW["end"] for d in dates)
        status = known.get(identity, {}).get("repository_status")
        terminal = status and status not in {"new", "selection-reviewed", "review-deferred", "implementation-pending", "accepted-unimplemented"}
        signals = protection_signals(row, "generic", {"always_protected_identities": primary_recalled})
        if in_window and row.get("revision_review_required"):
            signals["metadata_conflict"] = "captured newer revision requires bounded original-source review"
            terminal = False
        if priority_organizations(row):
            signals["source_priority_organization"] = ", ".join(priority_organizations(row))
        # Purely topical recollisions are still P2, but actual consumer ranking
        # proposals get original production-evidence review even without A/B in abs.
        if "recommendation" in value["tracks"] and re.search(
            r"recommendation|recommender|click-through|advertis|conversion rate|e-commerce|\bCTR\b", row["title"], re.I):
            signals["frozen_industrial_route"] = "industrial consumer application title; inspect original production evidence"
        disposition = "outside_window_date_screen" if not in_window else "known" if terminal else "protected" if signals else "p2_pending_selection"
        rows.append({"id": identity, "revision": row.get("revision") or 1, "tracks": sorted(value["tracks"]),
                     "capture_refs": sorted(set(value["captures"])), "metadata": row,
                     "inherited_repository_record": known.get(identity), "routing": disposition,
                     "positive_signal_matches": signals})
    result = {"schema_version": 1, "window": WINDOW, "capture_receipts": receipts,
              "counts": dict(Counter(r["routing"] for r in rows)), "records": rows,
              "all_sources_exhaustive": False, "candidate_review_complete": False}
    write(CACHE / "frozen-inventory.json", result)
    write(CACHE / "protected.json", {"window": WINDOW, "records": [r for r in rows if r["routing"] == "protected"]})
    assignments = {name: [] for name in ("google", "meta", "agent", "root")}
    for row in rows:
        if row["routing"] != "protected":
            continue
        combined = json.dumps(row["positive_signal_matches"], ensure_ascii=False)
        owner = ("meta" if row["id"] in {"2611.13442", "2611.17501"} or "Meta" in combined else
                 "google" if row["id"] == "2611.16028" or "Google" in combined else
                 "root" if "frozen_industrial_route" in row["positive_signal_matches"] else
                 "agent" if "agent" in row["tracks"] else "root")
        assignments[owner].append(row)
    for owner, assigned in assignments.items():
        write(CACHE / f"assigned-{owner}.json", {"window": WINDOW, "records": assigned})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repair-llm", action="store_true")
    args = parser.parse_args()
    if args.repair_llm:
        repair_llm()
    else:
        print(json.dumps(prepare()["counts"]))
