import datetime as dt
from dataclasses import replace
import urllib.error

from auto_research.discovery_announcements import discover_announcements, parse_bulletin
from auto_research.discovery import DiscoveredPaper, paper_metadata_sha256, triage_candidates
from auto_research.discovery_review import classify_candidate, unresolved_candidates
from auto_research.models import Paper
from auto_research.papers import ArxivClient, parse_arxiv_feed
from scripts.discover_papers import effective_start_date


HTML = '''<h3>Showing new listings for Monday, 12 October 2026</h3>
<dl><h3>New submissions (showing 1 of 1 entries)</h3>
<dt><a href="/abs/2610.13238">arXiv:2610.13238</a>
<a href="https://arxiv.org/html/2610.13238v1">html</a></dt>
<dd><div class="meta"><div class="list-title"><span>Title:</span>State-OPD</div>
<div class="list-authors"><a>A. One</a>, <a>B. Two</a></div>
<p class="mathjax">State-only teacher <a>context</a>.</p></div></dd></dl>
<dl><h3>Replacement submissions (showing 1 of 1 entries)</h3>
<dt><a href="/abs/2605.09040">arXiv:2605.09040</a> (replaced)
<a href="https://arxiv.org/html/2605.09040v4">html</a></dt>
<dd><div class="list-title"><span>Title:</span>UxSID</div>
<p class="mathjax">Semantic user interests.</p></dd></dl>'''


def test_bulletin_keeps_original_identity_version_and_entry_kind():
    entries, receipt = parse_bulletin(HTML)
    assert receipt["parse_complete"]
    assert receipt["announced_on"] == "2026-10-12"
    assert receipt["expected_entries"] == receipt["parsed_entries"] == 2
    assert entries[0].title == "State-OPD"
    assert entries[0].authors == ["A. One", "B. Two"]
    assert entries[1].arxiv_id == "2605.09040v4"
    assert entries[1].entry_kind == "replacement"


def test_failed_api_does_not_erase_independent_recall_or_invent_v1_date():
    class Offline:
        def lookup(self, ids):
            raise urllib.error.URLError("API throttled")
    papers, provenance, reports = discover_announcements(
        track="recommendation", start_date=dt.date(2026, 10, 11),
        end_date=dt.date(2026, 10, 13), client=Offline(), fetch=lambda url: HTML,
    )
    assert len(papers) == 2
    assert all(paper.published == "" for paper in papers)
    assert len(provenance["2605.09040"]) == 2
    assert provenance["2605.09040"][0]["announced_on"] == "2026-10-12"
    assert all(report["coverage_complete"] for report in reports)
    assert all(not report["publication_dates_resolved"] for report in reports)
    assert all(not report["watermark_eligible"] for report in reports)


def test_stale_or_capped_bulletin_is_not_complete_coverage():
    class Empty:
        def lookup(self, ids):
            return []
    papers, _, reports = discover_announcements(
        track="recommendation", start_date=dt.date(2026, 10, 13),
        end_date=dt.date(2026, 10, 13), client=Empty(), fetch=lambda url: HTML,
    )
    assert papers == []
    assert all(row["status"] == "outside-window" for row in reports)
    _, receipt = parse_bulletin(HTML.replace("showing 1 of 1", "showing 1 of 2", 1))
    assert not receipt["parse_complete"]


def test_old_api_cache_cannot_overwrite_explicit_new_bulletin_revision():
    class Stale:
        def lookup(self, ids):
            return [Paper("old title", "old abstract", [], "2026-05-09", "url", "2605.09040v1")]
    rows, provenance, reports = discover_announcements(
        track="recommendation", start_date=dt.date(2026, 10, 11), end_date=dt.date(2026, 10, 13),
        client=Stale(), fetch=lambda url: HTML,
    )
    revised = next(row for row in rows if row.arxiv_id.startswith("2605.09040"))
    assert revised.arxiv_id == "2605.09040v4" and revised.title == "UxSID"
    assert revised.published == "2026-05-09"
    assert provenance["2605.09040"][0]["revision_metadata_unresolved"]
    assert reports[0]["metadata_resolution_failures"]


def test_known_revision_enters_review_without_becoming_new_v1():
    original = Paper("UxSID", "Semantics", ["A"], "2026-05-09", "url", "2605.09040v1")
    revised = replace(original, arxiv_id="2605.09040v4", updated="2026-10-09")
    rows = triage_candidates([DiscoveredPaper(revised, ("priority-org-google",))],
                             {"2605.09040": "implemented"}, repository_versions={
        "2605.09040": {"revision": 1, "metadata_sha256": paper_metadata_sha256(original)},
    })
    assert rows[0]["repository_status"] == "implemented"
    assert rows[0]["revision_review_required"]
    assert rows[0]["priority_review_required"]
    assert rows[0]["revision_review_reason"] == "newer-version"
    classified = classify_candidate("recommendation", rows[0])
    assert classified["full_text_review_required"]
    assert unresolved_candidates([{"candidates": [classified]}]) == [classified]


def test_google_meta_official_recall_is_priority_even_without_a_keyword_query():
    paper = Paper("Publication", "", [], "2026-10-09", "url", "2610.00001v1")
    for organization in ("Google", "Google DeepMind", "Meta", "Netflix"):
        candidate = triage_candidates([DiscoveredPaper(paper, (), ({"organization": organization},))], {})[0]
        assert candidate["priority_review_required"] == (organization != "Netflix")
        if organization != "Netflix":
            assert classify_candidate("foundation-model", candidate)["review_bucket"] == "priority-fulltext-review"


def test_whitespace_is_not_substantive_metadata_change_and_old_revision_is_not_promoted():
    paper = Paper("A title", "Words here", ["Author"], "2026-05-09", "url", "2605.09040v4")
    changed = replace(paper, title="A  title\n", abstract="Words  here")
    baseline = {"2605.09040": {"revision": 4, "metadata_sha256": paper_metadata_sha256(paper)}}
    rows = triage_candidates([DiscoveredPaper(changed, ())], {"2605.09040": "implemented"},
                             repository_versions=baseline)
    assert not rows[0]["revision_review_required"]
    rows = triage_candidates([DiscoveredPaper(replace(paper, arxiv_id="2605.09040v2", title="Old"), ())],
                             {"2605.09040": "implemented"}, repository_versions=baseline)
    assert not rows[0]["revision_review_required"]


def test_revision_missing_baseline_is_queued_not_silently_closed():
    paper = Paper("UxSID", "", [], "", "url", "2605.09040v4")
    row = triage_candidates([DiscoveredPaper(paper, (), ({"entry_kind": "replacement"},))],
                            {"2605.09040": "implemented"})[0]
    assert row["revision_review_reason"] == "replacement-without-reviewed-baseline"
    assert row["review_required"]


def test_atom_keeps_updated_separate_from_first_publication():
    rows = parse_arxiv_feed(b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
    <id>https://arxiv.org/abs/2605.09040v4</id><published>2026-05-09T00:00:00Z</published>
    <updated>2026-10-09T00:00:00Z</updated><title>UxSID</title><summary>Text</summary>
    </entry></feed>''')
    assert rows[0].published.startswith("2026-05-09")
    assert rows[0].updated.startswith("2026-10-09")


def test_weekend_overlap_reaches_prior_submission_business_day():
    assert effective_start_date(dt.date(2026, 10, 12), announcement_overlap_days=1) == dt.date(2026, 10, 9)
    assert effective_start_date(dt.date(2026, 10, 12), announcement_overlap_days=0) == dt.date(2026, 10, 12)


def test_retry_after_is_bounded_and_failure_not_relabelled_success(monkeypatch):
    def fail(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 429, "busy", {"Retry-After": "3600"}, None)
    sleeps = []
    monkeypatch.setattr("urllib.request.urlopen", fail)
    monkeypatch.setattr("time.sleep", sleeps.append)
    client = ArxivClient(maximum_retries=1, maximum_retry_delay_seconds=10)
    client.search_pages("OPD", tolerate_failures=True)
    assert sleeps == []  # respect the server's hour-long delay by stopping this query
    assert client.query_reports[0]["state"] == "failed"
    assert not client.query_reports[0]["coverage_complete"]
