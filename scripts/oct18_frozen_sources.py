"""Portable Git commit/tree proofs for the small Oct18 executed-source scope.

Capture requires the real Git objects and matching current source. Verification
is offline and independent of .git, ancestry, branches, fetch depth or squash
merges. Blobs are not copied: current source bytes supply their Git/SHA256 hashes.
This proves source membership, not that an experiment actually ran on hardware.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
from pathlib import Path
import re
import subprocess
from typing import Mapping

MAX_OBJECTS = 256
MAX_RAW_BYTES = 2 * 1024 * 1024
MAX_PATHS = 128
OID = re.compile(r"[0-9a-f]{40}")
SHA256 = re.compile(r"[0-9a-f]{64}")


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _oid(kind: str, raw: bytes) -> str:
    return hashlib.sha1(f"{kind} {len(raw)}\0".encode("ascii") + raw).hexdigest()


def _parts(path: str) -> tuple[str, ...]:
    _require(isinstance(path, str) and 0 < len(path) <= 4096
             and "\\" not in path and "\0" not in path, "invalid portable source path")
    parts = tuple(path.split("/"))
    _require(all(part not in {"", ".", "..", ".git"} and len(part.encode("utf-8")) <= 255
                 for part in parts), "source paths must be normalized relative paths")
    return parts


def _paths(paths) -> tuple[str, ...]:
    try:
        values = tuple(paths)
    except TypeError as error:
        raise ValueError("source paths must be an iterable of strings") from error
    _require(0 < len(values) <= MAX_PATHS and all(isinstance(path, str) for path in values)
             and len(set(values)) == len(values),
             "bounded unique source paths required")
    for path in values:
        _parts(path)
    return tuple(sorted(values))


def _current(root: Path, path: str) -> bytes:
    base = Path(root).resolve()
    candidate = base
    for part in _parts(path):
        candidate = candidate / part
        _require(not candidate.is_symlink(), "source symlinks are not admissible")
    _require(candidate.resolve().is_relative_to(base) and candidate.is_file(), "source must be a current regular file")
    try:
        return candidate.read_bytes()
    except OSError as error:
        raise ValueError("current source is unreadable") from error


def _tree_entries(raw: bytes) -> dict[bytes, tuple[bytes, str]]:
    entries, position = {}, 0
    while position < len(raw):
        end = raw.find(b"\0", position)
        _require(end > position and end + 21 <= len(raw), "malformed Git tree entry")
        prefix = raw[position:end]
        _require(b" " in prefix, "tree entry mode is missing")
        mode, name = prefix.split(b" ", 1)
        _require(mode in {b"40000", b"040000", b"100644", b"100755", b"120000", b"160000"},
                 "unsupported Git tree mode")
        _require(name and name not in {b".", b"..", b".git"} and b"/" not in name
                 and name not in entries, "invalid or duplicate Git tree name")
        entries[name] = (mode, raw[end+1:end+21].hex())
        position = end + 21
    return entries


def _root_tree(raw: bytes) -> str:
    first = raw.split(b"\n", 1)[0]
    _require(first.startswith(b"tree "), "commit is missing its root tree")
    try:
        tree = first[5:].decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("invalid commit tree identity") from error
    _require(OID.fullmatch(tree), "invalid commit root tree identity")
    return tree


def _walk(tree_oid: str, path: str, read_tree) -> str:
    parts = _parts(path)
    for index, part in enumerate(parts):
        entries = _tree_entries(read_tree(tree_oid))
        entry = entries.get(part.encode("utf-8"))
        _require(entry is not None, "source path absent from proven tree")
        mode, child = entry
        if index == len(parts) - 1:
            _require(mode in {b"100644", b"100755"}, "source leaf must be a regular Git blob")
            return child
        _require(mode in {b"40000", b"040000"}, "source path traverses a non-tree entry")
        tree_oid = child
    raise ValueError("empty source path")


def capture_sources(root: Path, commit: str, paths) -> dict:
    """Capture commit/tree bytes only after checking current files are members.

    The raw commit contains existing public Git author/committer metadata; a
    publisher must inspect that metadata before publishing the proof artifact.
    """
    _require(isinstance(commit, str) and OID.fullmatch(commit), "full lowercase commit OID required")
    names = _paths(paths)
    objects: dict[str, dict[str, str]] = {}
    total = 0

    def read_object(kind, identity):
        nonlocal total
        if identity in objects:
            _require(objects[identity]["type"] == kind, "Git object type mismatch")
            return base64.b64decode(objects[identity]["data_base64"], validate=True)
        try:
            raw = subprocess.check_output(["git", "cat-file", kind, identity], cwd=root,
                                          stderr=subprocess.DEVNULL)
        except (OSError, subprocess.CalledProcessError) as error:
            raise ValueError("required frozen Git object is unavailable") from error
        _require(_oid(kind, raw) == identity, "captured Git object hash mismatch")
        total += len(raw)
        _require(len(objects) < MAX_OBJECTS and total <= MAX_RAW_BYTES, "source proof exceeds bounded object budget")
        objects[identity] = {"type": kind, "data_base64": base64.b64encode(raw).decode("ascii")}
        return raw

    root_tree = _root_tree(read_object("commit", commit))
    for path in names:
        leaf = _walk(root_tree, path, lambda identity: read_object("tree", identity))
        _require(_oid("blob", _current(root, path)) == leaf, "current source differs from frozen commit")
    return {"schema_version": 1, "object_format": "sha1", "commit": commit,
            "paths": list(names), "objects": objects}


def verify_sources(root: Path, commit: str, hashes: Mapping[str, str], proof: dict) -> None:
    """Verify commit -> tree path -> current Git blob and measured SHA256.

    No Git command or network call is made, including when .git is absent.
    """
    _require(isinstance(commit, str) and OID.fullmatch(commit), "full lowercase commit OID required")
    _require(isinstance(hashes, Mapping), "source hash mapping required")
    names = _paths(hashes)
    _require(all(isinstance(digest, str) and SHA256.fullmatch(digest) for digest in hashes.values()),
             "full lowercase source SHA256 required")
    _require(isinstance(proof, dict) and proof.get("schema_version") == 1
             and proof.get("object_format") == "sha1" and proof.get("commit") == commit,
             "portable source proof commit/schema differs")
    _require(isinstance(proof.get("paths"), list) and _paths(proof["paths"]) == names,
             "portable source proof path coverage differs")
    encoded = proof.get("objects")
    _require(isinstance(encoded, dict) and 0 < len(encoded) <= MAX_OBJECTS, "bounded Git object map required")
    decoded, total, commit_count = {}, 0, 0
    for identity, item in encoded.items():
        _require(isinstance(identity, str) and OID.fullmatch(identity) and isinstance(item, dict),
                 "invalid portable Git object identity")
        kind, data = item.get("type"), item.get("data_base64")
        _require(kind in {"commit", "tree"} and isinstance(data, str)
                 and len(data) <= 4 * ((MAX_RAW_BYTES + 2) // 3), "only bounded commit/tree objects are allowed")
        try:
            raw = base64.b64decode(data, validate=True)
        except (ValueError, binascii.Error) as error:
            raise ValueError("invalid portable object base64") from error
        total += len(raw)
        _require(total <= MAX_RAW_BYTES and _oid(kind, raw) == identity, "portable Git object hash/budget mismatch")
        if kind == "commit":
            commit_count += 1
            _require(identity == commit, "unexpected commit object in source proof")
        decoded[identity] = (kind, raw)
    _require(commit_count == 1 and commit in decoded, "proven commit object missing")
    root_tree = _root_tree(decoded[commit][1])

    def read_tree(identity):
        _require(identity in decoded and decoded[identity][0] == "tree", "proven tree object missing or wrong type")
        return decoded[identity][1]

    for path in names:
        leaf = _walk(root_tree, path, read_tree)
        raw = _current(root, path)
        _require(hashlib.sha256(raw).hexdigest() == hashes[path], "current source SHA256 differs")
        _require(_oid("blob", raw) == leaf, "current source is not the proven commit/path blob")
