"""Validate explicitly scoped human review watermarks, never advance them automatically."""

from __future__ import annotations

import datetime as dt
import calendar
import json
from pathlib import Path


POLICY = "bounded-review-with-explicit-exceptions-v1"
STATUSES = {"out_of_scope", "historical", "after_window", "known", "reviewed", "explicit_exception"}
EXCEPTION_TYPES = {"date_or_identity_unresolved", "document_unavailable", "pagination_unproven"}


def audit_review_watermark(root: Path) -> list[str]:
    path = root / "docs/paper-discovery-watermark.json"
    if not path.exists():
        return []
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(f"review watermark: {message}")

    def read(reference: str) -> dict:
        target = (root / "docs" / reference).resolve()
        if not target.is_relative_to((root / "docs").resolve()):
            raise ValueError("artifact must remain inside docs")
        return json.loads(target.read_text(encoding="utf-8"))

    def exception(row: dict, label: str) -> None:
        require(row.get("exception_type") in EXCEPTION_TYPES, f"{label}: unknown exception type")
        require(bool(row.get("reason")) and bool(row.get("attempts")), f"{label}: missing reason/attempts")
        require(bool(row.get("url")), f"{label}: missing source URL")
        require(row.get("counts_as_accepted") is False, f"{label}: exception is not an accepted paper")
        require(bool(row.get("reopen_when")), f"{label}: missing reopening condition")
        require(row.get("scope_triage_completed") is True, f"{label}: unread records cannot be ignored")

    def dates(row: dict, *, upper: bool = False) -> list[dt.date]:
        # Structured evidence retains the primary-source URL and exact location.
        result = []
        for item in row.get("date_evidence", []):
            value = item["date"] if isinstance(item, dict) else item
            if isinstance(item, dict) and item.get("precision") == "month" and len(value) == 7:
                year, month = map(int, value.split("-"))
                result.append(dt.date(year, month, calendar.monthrange(year, month)[1] if upper else 1))
            else:
                result.append(dt.date.fromisoformat(value))
        return result

    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        require(state.get("schema_version") == 1 and state.get("policy") == POLICY, "unknown policy")
        require(state.get("user_authorized_exceptions") is True, "exceptions lack user authorization")
        require(bool(state.get("authorization_record")), "missing authorization record")
        start = dt.date.fromisoformat(state["window"]["start"])
        end = dt.date.fromisoformat(state["window"]["end"])
        watermark = dt.date.fromisoformat(state["review_watermark"])
        strict = dt.date.fromisoformat(state["source_exhaustiveness_watermark"])
        require(start <= end == watermark and strict <= watermark, "inconsistent window/watermarks")
        require(state.get("all_sources_exhaustive") is False, "bounded review cannot claim all-source exhaustiveness")
        require(state.get("implementation_complete") is False, "review closure is not implementation closure")
        register = read(state["candidate_register"])
        papers = register["papers"]
        reviewed_ids = {p["id"] for p in papers}
        require(register.get("candidate_review_complete") is True, "candidate pool has not closed")
        require(not any(p.get("status") == "pending" for p in papers), "candidate pool contains unread papers")
        require(len(reviewed_ids) == len(papers), "duplicate candidate IDs")
        for paper in papers:
            if paper.get("status") == "accepted":
                require(any(r.get("decision") == "accepted" and r.get("fulltext_review_completed")
                            for r in paper.get("reviews", [])), f"{paper['id']}: acceptance lacks full text")
        receipts = state.get("retrieval_receipts", [])
        expected = {(track, mode) for track in ("recommendation", "foundation-model", "post-training", "agent")
                    for mode in ("submission-window", "late-index")}
        require({(r["track"], r["mode"]) for r in receipts} == expected and len(receipts) == 8,
                "both recall channels are required for all four tracks")
        for receipt in receipts:
            artifact = read(receipt["artifact"])
            require(artifact.get("requested_window", artifact.get("window")) == state["window"],
                    f"{receipt['artifact']}: receipt belongs to a different window")
            coverage = artifact.get("arxiv_transport", {})
            require(coverage.get("coverage_complete") is True and coverage.get("transport_complete") is True
                    and coverage.get("capped_queries") == 0 and coverage.get("failed_queries") == 0,
                    f"{receipt['artifact']}: retrieval is failed or capped")
            require(all(c["arxiv_id"] in reviewed_ids for c in artifact.get("candidates", [])),
                    f"{receipt['artifact']}: retrieved IDs are not reviewed")
        sources = state.get("source_reviews", [])
        require({s["organization"] for s in sources} >= {"Google", "Meta"}, "Google/Meta reviews are required")
        for source in sources:
            artifact = read(source["artifact"])
            require(artifact.get("window") == state["window"],
                    f"{source['organization']}: source review belongs to a different window")
            rows = artifact["records"]
            require(len({r["url"] for r in rows}) == len(rows) == artifact["expected_records"],
                    f"{source['organization']}: source record count mismatch")
            for row in rows:
                label = f"{source['organization']} / {row['url']}"
                require(row.get("review_status") in STATUSES and bool(row.get("reason")), f"{label}: undecided record")
                require(row.get("scope_triage_completed") is True, f"{label}: missing scope triage")
                if row.get("review_status") == "explicit_exception":
                    exception(row, label)
                elif row.get("review_status") == "reviewed":
                    ids = row.get("arxiv_ids") or [row.get("id")]
                    require(any(i in reviewed_ids for i in ids), f"{label}: missing reviewed candidate")
                elif row.get("review_status") == "historical":
                    evidence_dates = dates(row, upper=True)
                    ids = row.get("arxiv_ids", [])
                    dated_before = any(d < start for d in evidence_dates)
                    month_before = any(i[:4].isdigit() and i[:4] < start.strftime("%y%m") for i in ids)
                    require(dated_before or month_before, f"{label}: historical status lacks pre-window evidence")
                elif row.get("review_status") == "after_window":
                    evidence_dates = dates(row)
                    require(bool(evidence_dates) and all(d > end for d in evidence_dates),
                            f"{label}: after-window status lacks post-window evidence")
            for row in artifact.get("directory_exceptions", []):
                exception(row, source['organization'])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"review watermark: invalid artifact: {exc}")
    return errors
