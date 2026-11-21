"""Compressed official sources must not silently become empty directories."""

import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import prepare_nov18_priority_sources as capture


HTML = b'<html><body><a href="/research/publications/paper/">Paper</a></body></html>'


def test_transport_gzip_and_plain_html_have_the_same_link_inventory():
    plain = capture.parsed_capture_fields(HTML)
    compressed = capture.parsed_capture_fields(gzip.compress(HTML))
    assert compressed["links"] == plain["links"] == ["/research/publications/paper/"]
    assert compressed["decoded_sha256"] == plain["decoded_sha256"] == hashlib.sha256(HTML).hexdigest()
    assert compressed["transport_gzip_decoded"] is True
    assert plain["transport_gzip_decoded"] is False
    assert plain["parse_complete"] is compressed["parse_complete"] is True


def test_non_html_or_unavailable_message_is_not_a_complete_empty_directory():
    for raw in (b'Sorry, this content is not available', b'<html><body>Unavailable</body></html>'):
        assert capture.parsed_capture_fields(raw)["parse_complete"] is False


def test_link_inventory_handles_case_entities_and_non_links():
    raw = b'''<!doctype html><HTML><body>
    <A HREF="/paper/?a=1&amp;b=2">One</A><a href='/paper/?a=1&amp;b=2'>Duplicate</a>
    <a>No href</a><script>const fake = '<a href="/not-a-link/">';</script>
    <a href="/self-closing/" /><a href=/unquoted/>Unquoted</a>
    </body></HTML>'''
    parsed = capture.parsed_capture_fields(raw)
    assert parsed["parse_complete"] is True
    assert parsed["links"] == ["/paper/?a=1&b=2", "/self-closing/", "/unquoted/"]


def test_capture_parser_runs_without_site_packages():
    script = Path(capture.__file__).resolve()
    code = (
        "import gzip, runpy; module = runpy.run_path(" + repr(str(script)) + "); "
        "raw = " + repr(HTML) + "; "
        "plain = module['parsed_capture_fields'](raw); "
        "compressed = module['parsed_capture_fields'](gzip.compress(raw)); "
        "assert plain['parse_complete'] and compressed['parse_complete']; "
        "assert plain['links'] == compressed['links'] == ['/research/publications/paper/']"
    )
    result = subprocess.run([sys.executable, "-I", "-S", "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_cached_reparse_preserves_original_compressed_response_and_receipt(tmp_path, monkeypatch):
    monkeypatch.setattr(capture, "CACHE", tmp_path)
    raw = gzip.compress(HTML)
    path = tmp_path / "response.html"
    path.write_bytes(raw)
    row = {"capture": path.name, "sha256": hashlib.sha256(raw).hexdigest(), "links": [], "http_status": 200}
    before = json.dumps(row, sort_keys=True)
    updated = capture.refresh_capture(row)
    assert updated["parse_complete"] and updated["links"]
    assert updated["sha256"] == row["sha256"]
    assert path.read_bytes() == raw and json.dumps(row, sort_keys=True) == before


def test_missing_or_changed_raw_response_is_archived_not_accepted(tmp_path, monkeypatch):
    monkeypatch.setattr(capture, "CACHE", tmp_path)
    row = {"capture": "absent.html", "sha256": "0" * 64, "links": []}
    missing = capture.refresh_capture(row)
    assert missing["parse_complete"] is False and missing["status"] == "source_exception_archived"
    (tmp_path / "absent.html").write_bytes(HTML)
    changed = capture.refresh_capture(row)
    assert changed["parse_complete"] is False and changed["error_type"] == "ValueError"
    assert changed["automatic_retry"] is changed["blocking"] is False


def test_prior_transport_exception_remains_an_exception(tmp_path, monkeypatch):
    monkeypatch.setattr(capture, "CACHE", tmp_path)
    exception = {"status": "source_exception_archived", "error_type": "TimeoutError", "blocking": False}
    assert capture.refresh_capture(exception) == exception


def test_partial_directory_cannot_claim_all_unobserved_papers_removed():
    baseline = {"/pubs/old/", "/pubs/known/"}
    current = {"/pubs/known/", "/pubs/observed-new/"}
    partial = capture.directory_delta(baseline, current, comparison_complete=False)
    assert partial["added"] == ["/pubs/observed-new/"]
    assert partial["removed"] == [] and partial["unobserved_baseline_urls"] == 1
    complete = capture.directory_delta(baseline, current, comparison_complete=True)
    assert complete["removed"] == ["/pubs/old/"]
