"""MR-B boundaries: minimal imports, canonical metadata and recoverable scans."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import subprocess
import sys

import pytest

from auto_research.discovery import DiscoveryQuery, discover_candidates
from auto_research.discovery_checkpoint import coverage_summary
from auto_research.models import Paper
from auto_research.papers import ArxivClient, parse_arxiv_feed


def test_help_and_catalog_work_without_optional_runtimes(tmp_path):
    code = r"""
import importlib.abc, sys
class BlockOptional(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname.split('.')[0] in {'torch','transformers','tokenizers','datasets','PIL','av','torchvision'}:
            raise AssertionError('optional runtime imported: ' + fullname)
sys.meta_path.insert(0, BlockOptional())
from auto_research.cli import build_parser, main
parser = build_parser()
parser.parse_args(['reproduce', '--paper', 'din', '--write-manifest', sys.argv[1]])
assert main(['reproduce','--write-manifest',sys.argv[1]]) == 0
assert main(['init',sys.argv[2]]) == 0
assert main(['protocols','list']) == 0
from auto_research.reproductions.registry import list_adapters
assert len(list_adapters()) >= 371
assert not any(name.endswith('.adapter') for name in sys.modules if name.startswith('auto_research.reproductions.'))
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            code,
            str(tmp_path / "manifest.json"),
            str(tmp_path / "config.json"),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_lazy_binding_is_picklable_and_only_loads_selected_paper():
    code = """
import pickle, sys
from auto_research.reproductions.registry import get_adapter
a = pickle.loads(pickle.dumps(get_adapter('rptune')))
assert not any(x.endswith('.adapter') for x in sys.modules)
result = a.run(__import__('pathlib').Path('.'), 42)
assert result['setup']['diagnostic_only'] is True
assert pickle.loads(pickle.dumps(get_adapter('rptune'))).key == 'rptune'
loaded = [x for x in sys.modules if x.startswith('auto_research.reproductions.') and x.endswith('.adapter')]
assert loaded == ['auto_research.reproductions.rptune.adapter'], loaded
"""
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_specs_are_source_not_inferred_from_docs():
    from auto_research.paper_specs.runtime import spec_index
    from auto_research.paper_specs.schema import validate_spec

    for spec in spec_index().values():
        assert spec.schema_version == 2
        assert not validate_spec(spec)
    from scripts.generate_research_manifest import synchronize

    assert synchronize({}) == json.loads(Path("docs/research-manifest.json").read_text())


def _paper(number):
    return Paper(
        f"paper {number}",
        "agent",
        [],
        "2026-10-01T00:00:00Z",
        f"https://arxiv.org/abs/2610.{number:05d}",
        f"2610.{number:05d}",
    )


class Client(ArxivClient):
    def __init__(self, pages, **kwargs):
        super().__init__(**kwargs)
        self.pages = pages
        self.calls = []

    def search(self, query, limit=8, categories=(), *, start=0, **kwargs):
        self.calls.append((query, start))
        page = self.pages[(query, start)]
        if isinstance(page, BaseException):
            raise page
        return page


def _scan(client, queries=None):
    return discover_candidates(
        client,
        queries or (DiscoveryQuery("agent", "agent", ()),),
        start_date=dt.date(2026, 10, 1),
        end_date=dt.date(2026, 10, 7),
        page_size=2,
        maximum_results_per_query=4,
    )


def test_discovery_failure_retains_pages_and_continues_other_queries(tmp_path):
    queries = (DiscoveryQuery("one", "one", ()), DiscoveryQuery("two", "two", ()))
    c = Client(
        {
            ("one", 0): [_paper(1), _paper(2)],
            ("one", 2): TimeoutError("interrupted"),
            ("two", 0): [_paper(3)],
        },
        checkpoint_dir=tmp_path,
    )
    assert len(_scan(c, queries)) == 3
    summary = coverage_summary(c.query_reports)
    assert not summary["coverage_complete"] and summary["failed_queries"] == 1
    resumed = Client({("one", 2): [_paper(4)]}, checkpoint_dir=tmp_path, resume=True)
    assert len(_scan(resumed, queries)) == 4
    assert resumed.calls == [("one", 2)]
    summary = coverage_summary(resumed.query_reports)
    assert summary["coverage_complete"] and not summary["watermark_eligible"]
    assert not summary["review_complete"]


def test_capped_success_is_not_complete(tmp_path):
    c = Client(
        {("agent", 0): [_paper(1), _paper(2)], ("agent", 2): [_paper(3), _paper(4)]},
        checkpoint_dir=tmp_path,
    )
    _scan(c)
    summary = coverage_summary(c.query_reports)
    assert summary["transport_complete"]
    assert not summary["coverage_complete"] and summary["capped_queries"] == 1
    resumed = Client({}, checkpoint_dir=tmp_path, resume=True)
    _scan(resumed)
    assert resumed.query_reports[0]["state"] == "capped"


def test_resume_rejects_changed_query_matrix_and_new_scan_ignores_old_pages(tmp_path):
    c = Client({("agent", 0): [_paper(1)]}, checkpoint_dir=tmp_path)
    _scan(c)
    with pytest.raises(ValueError, match="query matrix"):
        _scan(
            Client({}, checkpoint_dir=tmp_path, resume=True),
            (DiscoveryQuery("changed", "agent", ()),),
        )
    fresh = Client({("agent", 0): [_paper(2)]}, checkpoint_dir=tmp_path)
    assert _scan(fresh)[0].paper.arxiv_id.endswith("00002")
    assert fresh.calls == [("agent", 0)]


def test_cached_page_never_advances_verified_checkpoint(tmp_path):
    class Cached(Client):
        def search(self, *args, **kwargs):
            self.cache_fallbacks.append("url")
            return [_paper(1)]

    c = Cached({}, checkpoint_dir=tmp_path)
    assert len(_scan(c)) == 1
    assert c.query_reports[0]["state"] == "cached"
    assert c.query_reports[0]["next_offset"] == 0
    resumed = Client({("agent", 0): [_paper(2)]}, checkpoint_dir=tmp_path, resume=True)
    assert _scan(resumed)[0].paper.arxiv_id.endswith("00002")


def test_arxiv_error_feed_is_not_an_empty_success():
    with pytest.raises(ValueError, match="arXiv API error"):
        parse_arxiv_feed(
            b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/api/errors</id><title>Error</title><summary>invalid query</summary></entry></feed>'
        )
