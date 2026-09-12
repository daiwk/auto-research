from __future__ import annotations

import urllib.error
import urllib.request

import pytest

from auto_research.papers import ArxivClient


EMPTY_FEED = b'<feed xmlns="http://www.w3.org/2005/Atom"></feed>'


class _Response:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self):
        return EMPTY_FEED


def test_successful_arxiv_page_is_checkpointed_and_reused(tmp_path, monkeypatch):
    client = ArxivClient(cache_dir=tmp_path, maximum_retries=0)
    monkeypatch.setattr(urllib.request, "urlopen", lambda *args, **kwargs: _Response())
    assert client.search("agent") == []
    assert list(tmp_path.glob("*.xml"))

    def throttled(*args, **kwargs):
        raise urllib.error.HTTPError("url", 429, "limited", {}, None)

    monkeypatch.setattr(urllib.request, "urlopen", throttled)
    assert client.search("agent") == []
    assert len(client.cache_fallbacks) == 1


def test_arxiv_throttle_without_checkpoint_is_not_empty_result(tmp_path, monkeypatch):
    def throttled(*args, **kwargs):
        raise urllib.error.HTTPError("url", 429, "limited", {}, None)

    monkeypatch.setattr(urllib.request, "urlopen", throttled)
    with pytest.raises(urllib.error.HTTPError):
        ArxivClient(cache_dir=tmp_path, maximum_retries=0).search("agent")
