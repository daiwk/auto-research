"""Portable source proofs survive squash deletion and reject identity tampering."""
from __future__ import annotations

import base64
from copy import deepcopy
import hashlib
import importlib.util
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("oct18_frozen_sources", ROOT / "scripts/oct18_frozen_sources.py")
proofs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(proofs)


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL).decode().strip()


@pytest.fixture
def frozen(tmp_path):
    root = tmp_path / "original"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Public Source Proof Test")
    git(root, "config", "user.email", "source-proof@example.invalid")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "config", "core.hooksPath", str(root / "no-hooks"))
    files = {"src/pkg/model.py": b"def predict(x):\n    return x + 1\n", "scripts/run.py": b"print('public fixture')\n"}
    for path, raw in files.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "public source fixture")
    commit = git(root, "rev-parse", "HEAD")
    proof = proofs.capture_sources(root, commit, files)
    hashes = {path: hashlib.sha256(raw).hexdigest() for path, raw in files.items()}
    return root, commit, files, hashes, proof


def test_proof_uses_only_commit_and_path_tree_objects_not_source_blobs(frozen):
    root, commit, files, hashes, proof = frozen
    proofs.verify_sources(root, commit, hashes, proof)
    assert {item["type"] for item in proof["objects"].values()} == {"commit", "tree"}
    assert len(proof["objects"]) == 5  # Commit, root, src, src/pkg, scripts.
    assert not any(raw in base64.b64decode(item["data_base64"])
                   for raw in files.values() for item in proof["objects"].values())


def test_verification_is_offline_without_git_or_ancestor_objects(frozen, tmp_path, monkeypatch):
    _, commit, files, hashes, proof = frozen
    checkout = tmp_path / "squashed-checkout-without-git"
    for path, raw in files.items():
        target = checkout / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **k: pytest.fail("persistent verification must not invoke Git"))
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: pytest.fail("persistent verification must not invoke a subprocess"))
    proofs.verify_sources(checkout, commit, hashes, proof)


@pytest.mark.parametrize("mutation", ["wrong_commit", "retagged_commit", "changed_commit_bytes", "changed_tree_bytes", "missing_tree",
                                      "wrong_type", "missing_path", "extra_path", "invalid_base64", "wrong_hash"])
def test_tampered_identity_objects_paths_or_measurement_are_rejected(frozen, mutation):
    root, commit, _, hashes, original = frozen
    proof = deepcopy(original)
    hashes = dict(hashes)
    tree = next(identity for identity, item in proof["objects"].items() if item["type"] == "tree")
    if mutation == "wrong_commit":
        commit = "0" * 40
    elif mutation == "retagged_commit":
        original_commit = commit
        commit = "0" * 40
        proof["commit"] = commit
        proof["objects"][commit] = proof["objects"].pop(original_commit)
    elif mutation == "changed_commit_bytes":
        item = proof["objects"][commit]
        item["data_base64"] = base64.b64encode(base64.b64decode(item["data_base64"]) + b"tampered").decode()
    elif mutation == "changed_tree_bytes":
        item = proof["objects"][tree]
        raw = bytearray(base64.b64decode(item["data_base64"]))
        raw[-1] ^= 1
        item["data_base64"] = base64.b64encode(raw).decode()
    elif mutation == "missing_tree":
        del proof["objects"][tree]
    elif mutation == "wrong_type":
        proof["objects"][tree]["type"] = "blob"
    elif mutation == "missing_path":
        proof["paths"].pop()
    elif mutation == "extra_path":
        proof["paths"].append("extra.py")
    elif mutation == "invalid_base64":
        proof["objects"][tree]["data_base64"] = "not!base64"
    else:
        hashes[next(iter(hashes))] = "0" * 64
    with pytest.raises(ValueError):
        proofs.verify_sources(root, commit, hashes, proof)


def test_recomputing_source_sha256_cannot_hide_changed_git_blob(frozen):
    root, commit, _, hashes, proof = frozen
    path = next(iter(hashes))
    (root / path).write_bytes(b"def predict(x):\n    return 'changed'\n")
    hashes[path] = hashlib.sha256((root / path).read_bytes()).hexdigest()
    with pytest.raises(ValueError, match="proven"):
        proofs.verify_sources(root, commit, hashes, proof)


@pytest.mark.parametrize("path", ["../outside.py", "/absolute.py", "src/../model.py", "./model.py", "src//model.py",
                                  "src\\model.py", ".git/config", "src/./model.py"])
def test_capture_and_verify_reject_traversal_or_ambiguous_paths(frozen, path):
    root, commit, _, _, proof = frozen
    with pytest.raises(ValueError):
        proofs.capture_sources(root, commit, [path])
    with pytest.raises(ValueError):
        proofs.verify_sources(root, commit, {path: "0" * 64}, proof)


def test_worktree_symlink_cannot_impersonate_a_proven_regular_source(frozen, tmp_path):
    root, commit, files, hashes, proof = frozen
    path = next(iter(files))
    outside = tmp_path / "outside.py"
    outside.write_bytes(files[path])
    (root / path).unlink()
    (root / path).symlink_to(outside)
    with pytest.raises(ValueError, match="symlink"):
        proofs.verify_sources(root, commit, hashes, proof)


def test_git_symlink_leaf_is_not_an_executable_source_proof(frozen):
    root, _, files, _, _ = frozen
    link = root / "link.py"
    link.symlink_to(next(iter(files)))
    git(root, "add", "link.py")
    git(root, "commit", "-q", "-m", "public symlink fixture")
    commit = git(root, "rev-parse", "HEAD")
    with pytest.raises(ValueError, match="regular Git blob"):
        proofs.capture_sources(root, commit, ["link.py"])


def test_directory_leaf_is_not_a_blob_and_budget_is_bounded(frozen):
    root, commit, _, hashes, proof = frozen
    with pytest.raises(ValueError, match="regular Git blob"):
        proofs.capture_sources(root, commit, ["src"])
    oversized = deepcopy(proof)
    tree = next(identity for identity, item in oversized["objects"].items() if item["type"] == "tree")
    oversized["objects"][tree]["data_base64"] = "a" * (4 * ((proofs.MAX_RAW_BYTES+2)//3) + 1)
    with pytest.raises(ValueError, match="bounded"):
        proofs.verify_sources(root, commit, hashes, oversized)
