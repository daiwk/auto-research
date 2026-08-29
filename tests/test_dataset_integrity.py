from __future__ import annotations

import io

import pytest

from auto_research.datasets import _download


def test_download_rejects_payload_that_does_not_match_pinned_checksum(monkeypatch, tmp_path):
    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    monkeypatch.setattr("urllib.request.urlopen", lambda *_args, **_kwargs: Response(b"changed"))
    target = tmp_path / "dataset.zip"
    with pytest.raises(ValueError, match="checksum mismatch"):
        _download("https://example.test/data", target, expected_sha256="0" * 64)
    assert not target.exists()
