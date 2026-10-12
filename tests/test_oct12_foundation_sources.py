import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace

import pytest

from auto_research.oct12_public_sources import (
    checkpoint_input_files, checkpoint_source, managed_stream,
    read_jsonl_mirror, verify_offline_manifest, verified_image_path,
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


def test_checkpoint_export_under_cache_ancestor_hashes_inputs_not_hf_metadata(tmp_path, monkeypatch):
    import huggingface_hub
    output = tmp_path / ".cache" / "public-checkpoint"
    output.mkdir(parents=True)
    for name, contents in {"config.json": b"{}", "model.safetensors": b"weights",
                           "tokenizer.json": b"{}", "merges.txt": b"merges"}.items():
        (output / name).write_bytes(contents)
    metadata = output / ".cache" / "huggingface" / "download"
    metadata.mkdir(parents=True)
    (metadata / "internal.json").write_bytes(b"not a model input")
    calls = []
    monkeypatch.setattr(huggingface_hub, "snapshot_download", lambda *a, **kw: calls.append((a, kw)))
    script = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/prepare_oct12_public_sources.py"))
    manifest = script["export_checkpoint"](output, "smollm")
    assert set(manifest["files"]) == {"config.json", "model.safetensors", "tokenizer.json", "merges.txt"}
    assert set(checkpoint_input_files(output)) == set(manifest["files"])
    assert calls[0][1]["revision"] == manifest["revision"]
    (output / "provenance.json").write_text(json.dumps(manifest))
    assert verify_offline_manifest(output, manifest["public_id"], manifest["revision"], "checkpoint") == manifest


def test_finite_stream_closes_generator_on_early_break_and_exception():
    closed = []
    def rows():
        try:
            yield from range(100)
        finally:
            closed.append(True)
    with managed_stream(rows()) as iterator:
        assert next(iterator) == 0
    assert closed == [True]
    with pytest.raises(RuntimeError, match="consumer failed"):
        with managed_stream(rows()) as iterator:
            assert next(iterator) == 0
            raise RuntimeError("consumer failed")
    assert closed == [True, True]


def test_parquet_prefix_stream_exits_normally_in_subprocess(tmp_path):
    pa = pytest.importorskip("pyarrow")
    pq = pytest.importorskip("pyarrow.parquet")
    path = tmp_path / "ordered.parquet"
    pq.write_table(pa.table({"id": list(range(1000)), "text": ["prefix"] * 1000}), path,
                   row_group_size=64)
    program = """
import sys
from auto_research.oct12_public_sources import managed_stream, iter_parquet_file
for _ in range(20):
    with open(sys.argv[1], 'rb') as handle:
        with managed_stream(iter_parquet_file(handle)) as iterator:
            assert next(iterator)['id'] == 0
print('normal-exit-ready', flush=True)
"""
    result = subprocess.run([sys.executable, "-c", program, str(path)],
                            check=True, text=True, capture_output=True, timeout=45)
    assert result.stdout.strip() == "normal-exit-ready"


def test_pinned_public_shards_preserve_order_and_close_on_prefix(tmp_path, monkeypatch):
    pa = pytest.importorskip("pyarrow")
    pq = pytest.importorskip("pyarrow.parquet")
    datasets = pytest.importorskip("datasets")
    import fsspec
    from auto_research.oct12_public_sources import public_parquet_rows
    paths = [tmp_path / "second.parquet", tmp_path / "first.parquet"]
    for path, ids in zip(paths, ([0, 1], [2, 3])):
        pq.write_table(pa.table({"id": ids}), path)
    calls, handles = [], []
    def builder(*args, **kwargs):
        calls.append((args, kwargs))
        return SimpleNamespace(config=SimpleNamespace(data_files={"train": [str(p) for p in paths]}))
    def opener(path, mode):
        handle = open(path, mode)
        handles.append(handle)
        return handle
    monkeypatch.setattr(datasets, "load_dataset_builder", builder)
    monkeypatch.setattr(fsspec, "open", opener)
    kwargs = {"configuration": "official-config", "data_files": "train/*.parquet", "cache_dir": tmp_path}
    with managed_stream(public_parquet_rows("public/source", "fixed-revision", "train", **kwargs)) as rows:
        assert next(rows) == {"id": 0}
    assert handles[-1].closed
    assert list(public_parquet_rows("public/source", "fixed-revision", "train", **kwargs)) == [
        {"id": i} for i in range(4)]
    assert all(handle.closed for handle in handles)
    assert calls[0] == (("public/source", "official-config"), {
        "revision": "fixed-revision", "data_files": "train/*.parquet", "cache_dir": str(tmp_path)})


def test_parquet_reader_disables_both_background_prefetch_and_cpu_workers(tmp_path, monkeypatch):
    pq = pytest.importorskip("pyarrow.parquet")
    from auto_research.oct12_public_sources import iter_parquet_file
    calls = []
    class Batch:
        def to_pylist(self):
            return [{"id": 0}, {"id": 1}]
    class Reader:
        def __init__(self, handle, **kwargs):
            calls.append(("open", kwargs))
        def iter_batches(self, **kwargs):
            calls.append(("iterate", kwargs))
            yield Batch()
        def close(self):
            calls.append(("close", {}))
    monkeypatch.setattr(pq, "ParquetFile", Reader)
    with managed_stream(iter_parquet_file(object())) as rows:
        assert next(rows) == {"id": 0}
    assert calls == [("open", {"pre_buffer": False}),
                     ("iterate", {"batch_size": 8, "use_threads": False}), ("close", {})]
