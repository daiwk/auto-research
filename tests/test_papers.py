import urllib.error
import urllib.parse
from pathlib import Path

import pytest

from auto_research.papers import ArxivClient, canonical_arxiv_id, parse_arxiv_feed


def test_parse_arxiv_feed():
    payload = b'''<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry><id>http://arxiv.org/abs/2607.00001v1</id><published>2026-07-01T00:00:00Z</published>
      <title> A useful\n paper </title><summary> Abstract text. </summary>
      <author><name>A. Researcher</name></author></entry>
    </feed>'''
    papers = parse_arxiv_feed(payload)
    assert papers[0].title == "A useful paper"
    assert papers[0].arxiv_id == "2607.00001v1"
    assert papers[0].authors == ["A. Researcher"]


def test_search_builds_quoted_category_query(monkeypatch):
    captured = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self):
            return b'<feed xmlns="http://www.w3.org/2005/Atom" />'

    def fake_open(request, timeout):
        captured["url"] = request.full_url
        return Response()

    monkeypatch.setattr("urllib.request.urlopen", fake_open)
    ArxivClient().search("post-training LLM", 2, ("cs.CL", "cs.LG"))
    assert "all%3A%22post-training%22" in captured["url"]
    assert "cat%3Acs.CL" in captured["url"]


def test_canonical_arxiv_id_removes_only_version_suffix():
    assert canonical_arxiv_id("2608.10257v1") == "2608.10257"
    assert canonical_arxiv_id("2608.10257") == "2608.10257"


def test_search_bounds_late_index_by_identifier_month_not_submission_date(monkeypatch):
    client = ArxivClient(minimum_interval_seconds=0)
    urls = []
    def read(request):
        urls.append(request.full_url)
        return b'<feed xmlns="http://www.w3.org/2005/Atom" />'
    monkeypatch.setattr(client, "_read", read)
    client.search_pages("agent", categories=("cs.AI",), identifier_months=("2609", "2610"))
    query = urllib.parse.parse_qs(urllib.parse.urlparse(urls[0]).query)["search_query"][0]
    assert '(id:2609.* OR id:2610.*)' in query
    assert 'all:"agent"' in query
    assert 'cat:cs.AI' in query
    assert 'submittedDate' not in query
    assert client.query_reports[0]["identifier_months"] == ["2609", "2610"]


@pytest.mark.parametrize("month", ["2613", "2600", "202610", "2610 OR all:agent"])
def test_identifier_month_rejects_invalid_values_before_network(month):
    with pytest.raises(ValueError, match="identifier months"):
        ArxivClient().search("agent", identifier_months=(month,))


def test_discovery_respects_arxiv_shared_api_limit():
    workflow = Path(".github/workflows/paper-discovery.yml").read_text(
        encoding="utf-8"
    )
    strategy = workflow.split("    strategy:\n", 1)[1].split("    steps:\n", 1)[0]
    assert "      max-parallel: 1\n" in strategy
    assert ArxivClient().minimum_interval_seconds >= 3.0
    assert ArxivClient().retry_backoff_seconds >= 3.0


def test_search_retries_transient_arxiv_throttling(monkeypatch):
    calls = []

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self):
            return b'<feed xmlns="http://www.w3.org/2005/Atom" />'

    def fake_open(request, timeout):
        calls.append(request.full_url)
        if len(calls) == 1:
            raise urllib.error.HTTPError(request.full_url, 429, "rate limited", {}, None)
        return Response()

    sleeps = []
    monkeypatch.setattr("urllib.request.urlopen", fake_open)
    monkeypatch.setattr("time.sleep", sleeps.append)
    assert ArxivClient(maximum_retries=1, retry_backoff_seconds=0.25).search("agent") == []
    assert len(calls) == 2
    assert sleeps == [0.25]


def test_search_retries_intermittent_406_without_changing_query(monkeypatch):
    calls = []

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self):
            return b'<feed xmlns="http://www.w3.org/2005/Atom" />'

    def fake_open(request, timeout):
        calls.append(request.full_url)
        if len(calls) == 1:
            raise urllib.error.HTTPError(request.full_url, 406, "intermittent", {}, None)
        return Response()

    monkeypatch.setattr("urllib.request.urlopen", fake_open)
    monkeypatch.setattr("time.sleep", lambda _: None)
    assert ArxivClient(maximum_retries=1).search("agent") == []
    assert len(calls) == 2
    assert calls[0] == calls[1]


def test_search_retries_transient_read_timeout(monkeypatch):
    calls = []

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self):
            return b'<feed xmlns="http://www.w3.org/2005/Atom" />'

    def fake_open(request, timeout):
        calls.append((request.full_url, timeout))
        if len(calls) == 1:
            raise TimeoutError("arXiv announcement burst")
        return Response()

    sleeps = []
    monkeypatch.setattr("urllib.request.urlopen", fake_open)
    monkeypatch.setattr("time.sleep", sleeps.append)
    assert ArxivClient(maximum_retries=1, retry_backoff_seconds=0.5).search("agent") == []
    assert len(calls) == 2
    assert sleeps == [0.5]
