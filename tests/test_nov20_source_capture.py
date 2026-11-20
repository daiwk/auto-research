"""A failed metadata API must not discard independently retrieved bulletins."""

import json
import sys
from types import SimpleNamespace

import pytest

import prepare_nov18_latest_sources as capture


@pytest.mark.parametrize("failed_bulletin", [None, "cs.CL"])
def test_bulletins_survive_metadata_failure(tmp_path, monkeypatch, failed_bulletin):
    class UnavailableAPI:
        user_agent = "test-no-network"

        def __init__(self, **kwargs):
            pass

        def _read(self, request):
            raise OSError("metadata API unavailable")

    def fetch(url):
        if failed_bulletin and f"/{failed_bulletin}/" in url:
            raise OSError("one bulletin unavailable")
        return "<html>fixed bulletin fixture</html>"

    monkeypatch.setattr(capture, "ROOT", tmp_path)
    monkeypatch.setattr(capture, "CACHE", tmp_path / "default-unused")
    monkeypatch.setattr(capture, "ArxivClient", UnavailableAPI)
    monkeypatch.setattr(capture, "fetch_text", fetch)
    monkeypatch.setattr(capture, "repository_paper_records", lambda *args: {})
    monkeypatch.setattr(
        capture,
        "parse_bulletin",
        lambda raw: (
            [SimpleNamespace(arxiv_id="2611.25088v1", entry_kind="new")],
            {"announced_on": "2026-11-20", "parse_complete": True},
        ),
    )
    cache = tmp_path / "new-cache"
    monkeypatch.setattr(
        sys,
        "argv",
        ["capture", "--start", "2026-11-19", "--end", "2026-11-20",
         "--overlap-start", "2026-11-18", "--cache-dir", str(cache)],
    )
    capture.main()
    metadata = json.loads((cache / "metadata-pool.json").read_text())
    bulletin = json.loads((cache / "announcement-pool.json").read_text())
    assert metadata["coverage_complete_to_overlap_boundary"] is False
    assert metadata["receipts"][0]["transport_complete"] is False
    expected = len(capture.CATEGORIES) - int(failed_bulletin is not None)
    assert len(list((cache / "captures").glob("*-new.html"))) == expected
    assert len(bulletin["identities"]["2611.25088"]) == expected
    assert sum(r.get("parse_complete", False) for r in bulletin["receipts"]) == expected
    assert all("No such file" not in r.get("error", "") for r in bulletin["receipts"])


def test_frozen_namespace_does_not_mutate_prior_runner_or_load_broad_initializers():
    import run_nov18_latest_components as old
    before = (old.AUDIT, old.BATCH, old.execution_files, old.importlib)
    import run_nov20_latest_components as new

    module = new.load_component("auto_research.system_one.looproute")
    assert module.__name__ == "_nov20_frozen.system_one.looproute"
    assert not hasattr(sys.modules["_nov20_frozen.system_one"], "__file__")
    assert before == (old.AUDIT, old.BATCH, old.execution_files, old.importlib)
    with pytest.raises(ValueError):
        new.load_component("auto_research.system_one.benchmark")
