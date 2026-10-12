import hashlib
import json
from pathlib import Path

import pytest

from auto_research.oct12_public_sources import (
    checkpoint_source, read_jsonl_mirror, verify_offline_manifest, verified_image_path,
)


def write_manifest(root, kind="dataset", public_id="public/source", revision="revision", files=None, **extra):
    payload = {"kind": kind, "public_id": public_id, "revision": revision, "files": files, **extra}
    (root / "provenance.json").write_text(json.dumps(payload))


def test_offline_mirror_hashes_rows_images_identity_and_revision(tmp_path):
    data, image = b'{"id":"1","image":{"path":"image.png"}}\n', b"unit-test image bytes"
    (tmp_path / "rows.jsonl").write_bytes(data)
    (tmp_path / "image.png").write_bytes(image)
    files = {"rows.jsonl": hashlib.sha256(data).hexdigest(), "image.png": hashlib.sha256(image).hexdigest()}
    write_manifest(tmp_path, files=files, split="train", rows=1)
    rows, manifest = read_jsonl_mirror(tmp_path, "rows.jsonl", "public/source", "revision", "train")
    assert verified_image_path(rows[0]["image"], tmp_path, manifest) == tmp_path / "image.png"
    with pytest.raises(ValueError, match="identity/revision"):
        verify_offline_manifest(tmp_path, "public/source", "wrong-revision", "dataset")
    (tmp_path / "image.png").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="SHA256 mismatch"):
        read_jsonl_mirror(tmp_path, "rows.jsonl", "public/source", "revision", "train")


def test_checkpoint_mirror_rejects_unhashed_inputs_and_never_exports_path(tmp_path):
    (tmp_path / "config.json").write_bytes(b"{}")
    (tmp_path / "model.safetensors").write_bytes(b"weights")
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in tmp_path.iterdir()}
    write_manifest(tmp_path, kind="checkpoint", files=files)
    source, kwargs, safe = checkpoint_source("public/source", "revision", tmp_path)
    assert kwargs == {"local_files_only": True} and source == str(tmp_path)
    assert str(tmp_path) not in json.dumps(safe)
    (tmp_path / "tokenizer.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="unhashed"):
        checkpoint_source("public/source", "revision", tmp_path)


def test_unrecorded_image_and_path_traversal_are_rejected(tmp_path):
    with pytest.raises(ValueError, match="every image"):
        verified_image_path({"path": "unknown.png"}, tmp_path, {"files": {}})
    write_manifest(tmp_path, files={"../outside": "0" * 64})
    with pytest.raises(ValueError, match="safe relative"):
        verify_offline_manifest(tmp_path, "public/source", "revision", "dataset")


def test_per_row_digest_is_checked_even_when_jsonl_file_hash_matches(tmp_path):
    data = b'{"id":"1","source_row_sha256":"incorrect"}\n'
    (tmp_path / "rows.jsonl").write_bytes(data)
    write_manifest(tmp_path, files={"rows.jsonl": hashlib.sha256(data).hexdigest()}, split="train", rows=1)
    with pytest.raises(ValueError, match="per-row SHA256"):
        read_jsonl_mirror(tmp_path, "rows.jsonl", "public/source", "revision", "train")
