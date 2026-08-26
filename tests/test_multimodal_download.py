from __future__ import annotations

from contextlib import contextmanager

from auto_research.multimodal.data import _download_with_resume


def test_dataset_download_identifies_client_and_preserves_range(monkeypatch, tmp_path):
    target = tmp_path / "archive.download"
    target.write_bytes(b"old")
    captured = {}

    class Response:
        status = 206

        def read(self, _size):
            if captured.get("read"):
                return b""
            captured["read"] = True
            return b"new"

    @contextmanager
    def urlopen(request, timeout):
        captured["headers"] = dict(request.header_items())
        captured["timeout"] = timeout
        yield Response()

    monkeypatch.setattr("urllib.request.urlopen", urlopen)
    _download_with_resume("https://example.test/data", target)
    headers = {key.lower(): value for key, value in captured["headers"].items()}
    assert headers["user-agent"].startswith("auto-research-dataset-fetcher/")
    assert headers["range"] == "bytes=3-"
    assert target.read_bytes() == b"oldnew"
