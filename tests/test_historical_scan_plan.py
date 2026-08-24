import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs/paper-audits/2026-historical-candidates.json"
MARKDOWN_PATH = ROOT / "docs/paper-audits/2026-historical-scan-plan.md"


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
    assert len(planned) == 70
    assert len(completed) == 4
    assert {paper["implementation_batch"] for paper in planned} == {
        f"B{number:02d}" for number in range(1, 12)
    }

    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    for paper in papers:
        if paper["full_text_review_required"]:
            assert paper["arxiv_id"] in markdown
    for batch in range(12):
        assert f"B{batch:02d}" in markdown


def test_historical_scan_does_not_call_unreviewed_backlog_rejected():
    papers = json.loads(JSON_PATH.read_text(encoding="utf-8"))["papers"]
    backlog = [paper for paper in papers if paper["plan_status"] == "fulltext-review-backlog"]
    assert len(backlog) == 331
    assert all(paper["implementation_batch"] is None for paper in backlog)
    assert all("retain" in paper["plan_reason"] for paper in backlog)
