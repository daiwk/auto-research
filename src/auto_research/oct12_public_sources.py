"""Hash-verified offline mirrors for the Oct-12 public-data diagnostics.

A provenance manifest declares public identity/revision AND hashes exact
local bytes. It is not a claim that an arbitrary unverified cache is an
official split. Preparation must originate from the pinned upstream revision.
"""
from __future__ import annotations
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checkpoint_input_files(directory: Path) -> dict[str, Path]:
    """Select model inputs relative to the mirror, not its absolute ancestors."""
    root = Path(directory)
    files = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts[:2] == (".cache", "huggingface"):
            continue  # snapshot_download bookkeeping, never a model input
        if path.is_file() and path.name != "provenance.json" and (
            path.suffix in {".json", ".safetensors"}
            or path.name in {"pytorch_model.bin", "merges.txt", "vocab.txt"}
        ):
            files[relative.as_posix()] = path
    return files


@contextmanager
def managed_stream(dataset):
    """Close a streaming generator even when its ordered prefix is sufficient."""
    iterator = iter(dataset)
    try:
        yield iterator
    finally:
        close = getattr(iterator, "close", None)
        if close is not None:
            close()


def iter_parquet_file(handle, batch_size: int = 8):
    """Strictly synchronous Arrow reads, including CPU column decoding.

    Arrow #50482 documents Python-file threaded shutdown hangs. Disabling
    pre_buffer alone does not disable the default CPU decode worker pool.
    Both official switches are needed for finite prefix reads, and both
    reader/batch iterator are explicitly closed before the file context ends.
    """
    from pyarrow.parquet import ParquetFile
    parquet = ParquetFile(handle, pre_buffer=False)
    try:
        with managed_stream(parquet.iter_batches(batch_size=batch_size, use_threads=False)) as batches:
            for batch in batches:
                yield from batch.to_pylist()
    finally:
        parquet.close()


def public_parquet_rows(public_id: str, revision: str, split: str,
                        *, configuration: str | None = None, data_files=None,
                        cache_dir: Path | None = None):
    """Resolve ordered official shard paths at the pinned revision, then read.

    DatasetBuilder is used only for the public config/split/shard resolution;
    its threaded Arrow scanner is not started. Image structs remain raw and
    are decoded by the existing visual-input loader without changing text.
    """
    import fsspec
    from datasets import load_dataset_builder
    builder = load_dataset_builder(public_id, configuration, revision=revision,
                                   data_files=data_files, cache_dir=str(cache_dir) if cache_dir else None)
    paths = builder.config.data_files.get(split, [])
    if not paths or any(not str(path).endswith(".parquet") for path in paths):
        raise ValueError("pinned public source must resolve the requested split to parquet shards")
    for path in paths:
        # The builder's DataFilesList preserves official shard order. fsspec
        # supplies a bounded seekable range reader instead of downloading the
        # complete multi-gigabyte dataset just to consume an ordered prefix.
        with fsspec.open(str(path), "rb") as handle:
            yield from iter_parquet_file(handle)


def verify_offline_manifest(directory: Path, public_id: str, revision: str, kind: str) -> dict:
    path = Path(directory) / "provenance.json"
    manifest = json.loads(path.read_text())
    if (manifest.get("kind"), manifest.get("public_id"), manifest.get("revision")) != (kind, public_id, revision):
        raise ValueError("offline provenance identity/revision does not match the requested public source")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("offline provenance must hash exact source files")
    for relative, expected in files.items():
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("offline manifest file keys must be safe relative paths")
        if not isinstance(expected, str) or len(expected) != 64:
            raise ValueError("invalid SHA256 in provenance")
        if sha256_file(Path(directory) / relative) != expected:
            raise ValueError(f"offline source SHA256 mismatch: {relative}")
    if kind == "checkpoint":
        if "config.json" not in files or not any(
            key.endswith(".safetensors") or key.endswith("pytorch_model.bin") for key in files):
            raise ValueError("checkpoint provenance must cover config and actual weight files")
        actual = set(checkpoint_input_files(directory))
        if not actual <= set(files):
            raise ValueError("checkpoint contains unhashed model/tokenizer/processor input files")
    return manifest


def checkpoint_source(public_id: str, revision: str, checkpoint_path: Path | None):
    if checkpoint_path is None:
        return public_id, {"revision": revision}, None
    manifest = verify_offline_manifest(checkpoint_path, public_id, revision, "checkpoint")
    return str(checkpoint_path), {"local_files_only": True}, {
        "public_id": public_id, "revision": revision, "file_sha256": manifest["files"]}


def recorded_verified_files(directory: Path | None) -> dict | None:
    """Use only after a successful loader verified this manifest; no host paths."""
    if directory is None or not (Path(directory) / "provenance.json").exists():
        return None
    manifest = json.loads((Path(directory) / "provenance.json").read_text())
    return {"public_id": manifest["public_id"], "revision": manifest["revision"],
            "file_sha256": manifest["files"], "rows": manifest.get("rows")}


def read_jsonl_mirror(directory: Path, filename: str, public_id: str, revision: str,
                      split: str) -> tuple[list[dict], dict]:
    manifest = verify_offline_manifest(directory, public_id, revision, "dataset")
    if manifest.get("split") != split or filename not in manifest["files"]:
        raise ValueError("offline data mirror must identify/hash the expected upstream split JSONL")
    rows = [json.loads(line) for line in (Path(directory) / filename).read_text().splitlines() if line.strip()]
    if manifest.get("rows") != len(rows):
        raise ValueError("offline mirror row count does not match provenance")
    for row in rows:
        if "source_row_sha256" in row:
            original = {key: value for key, value in row.items() if key != "source_row_sha256"}
            actual = hashlib.sha256(json.dumps(original, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if actual != row["source_row_sha256"]:
                raise ValueError("offline mirror per-row SHA256 mismatch")
    return rows, manifest


def verified_image_path(value: dict, directory: Path, manifest: dict) -> Path:
    relative = value.get("path")
    if relative not in manifest["files"]:
        raise ValueError("every image referenced by an offline row must be hashed in provenance")
    return Path(directory) / relative
