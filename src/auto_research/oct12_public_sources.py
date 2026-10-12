"""Hash-verified offline mirrors for the Oct-12 public-data diagnostics.

A provenance manifest declares public identity/revision AND hashes exact
local bytes. It is not a claim that an arbitrary unverified cache is an
official split. Preparation must originate from the pinned upstream revision.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        actual = {p.relative_to(directory).as_posix() for p in Path(directory).rglob("*") if p.is_file()
                  and (p.name.endswith(".json") or p.name.endswith(".safetensors")
                       or p.name in {"pytorch_model.bin", "merges.txt", "vocab.txt"})
                  and p.name != "provenance.json"}
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
    return rows, manifest


def verified_image_path(value: dict, directory: Path, manifest: dict) -> Path:
    relative = value.get("path")
    if relative not in manifest["files"]:
        raise ValueError("every image referenced by an offline row must be hashed in provenance")
    return Path(directory) / relative
