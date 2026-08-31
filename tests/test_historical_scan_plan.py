import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs/paper-audits/2026-historical-candidates.json"
MARKDOWN_PATH = ROOT / "docs/paper-audits/2026-historical-scan-plan.md"
DECISIONS_PATH = ROOT / "docs/paper-audits/2026-historical-fulltext-decisions.json"
REVIEW_PATH = ROOT / "docs/paper-audits/2026-historical-fulltext-review.md"


def test_historical_scan_keeps_every_candidate_and_fixed_batch_visible():
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    papers = payload["papers"]
    assert payload["date_from"] == "2026-01-01"
    assert payload["date_to"] == "2026-08-24"
    assert payload["unique_new_candidates"] == len(papers) == 3906
    assert len({paper["arxiv_id"] for paper in papers}) == len(papers)
    assert sum(paper["full_text_review_required"] for paper in papers) == 404

    planned = [paper for paper in papers if paper["plan_status"] == "planned-implementation"]
    completed = [paper for paper in papers if paper["plan_status"] == "implemented-in-current-pr"]
    assert len(planned) == 0
    assert len(completed) == 74

    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    for paper in papers:
        if paper["full_text_review_required"]:
            assert paper["arxiv_id"] in markdown
    for batch in range(12):
        assert f"B{batch:02d}" in markdown


def test_historical_fulltext_backlog_has_auditable_terminal_decisions():
    papers = json.loads(JSON_PATH.read_text(encoding="utf-8"))["papers"]
    backlog = [paper for paper in papers if paper["plan_status"] == "fulltext-review-backlog"]
    assert len(backlog) == 331
    payload = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))
    decisions = payload["decisions"]
    assert {paper["arxiv_id"] for paper in backlog} == {
        decision["arxiv_id"] for decision in decisions
    }
    assert len(decisions) == len({decision["arxiv_id"] for decision in decisions}) == 331
    assert {decision["decision"] for decision in decisions} == {
        "promoted-p0", "p2-after-fulltext", "rejected-unavailable"
    }
    promoted = [decision for decision in decisions if decision["decision"] == "promoted-p0"]
    assert len(promoted) == 55
    assert all(decision["full_text_sha256"] for decision in promoted)
    assert all(decision["metric_tokens"] for decision in promoted)
    review = REVIEW_PATH.read_text(encoding="utf-8")
    assert "| 未决全文 backlog | **0**" in review
    assert all(decision["arxiv_id"] in review for decision in promoted)
