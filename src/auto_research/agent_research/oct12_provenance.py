"""Verify an immutable public revision against existing local HF cache metadata."""
from __future__ import annotations
import hashlib
from pathlib import Path
import re


def _etag(path, expected):
    if re.fullmatch(r"[0-9a-f]{64}", expected):
        digest = hashlib.sha256()
    elif re.fullmatch(r"[0-9a-f]{40}", expected):
        digest = hashlib.sha1()
        digest.update(b"blob " + str(path.stat().st_size).encode() + b"\0")
    else:
        raise ValueError("unsupported HF file etag")
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest() == expected


def verify_local_checkpoint(path, model_id, revision):
    if not isinstance(model_id,str) or not re.fullmatch(r"[^/\s]+/[^/\s]+",model_id):
        raise ValueError("explicit public owner/model identifier required")
    if not isinstance(revision,str) or not re.fullmatch(r"[0-9a-f]{40}",revision):
        raise ValueError("checkpoint revision must be immutable 40-hex commit")
    root = Path(path).resolve()
    if (root/"provenance.json").is_file():
        from auto_research.oct12_public_sources import verify_offline_manifest
        manifest = verify_offline_manifest(root,model_id,revision,"checkpoint")
        return {"id":model_id,"revision":revision,"immutable_revision_verified":True,
                "file_sha256":manifest["files"],"local_files_only":True,"trust_remote_code":False,
                "verification":"pinned official-source offline byte-hash manifest"}
    required = [root / "config.json", root / "tokenizer_config.json"]
    weights = sorted(root.glob("*.safetensors"))
    if not weights or any(not item.is_file() for item in required):
        raise ValueError("local safe checkpoint requires config/tokenizer metadata and safetensors")
    files = sorted(set(required+weights+list(root.glob("*.json"))+[
        p for p in root.iterdir() if p.name in {"merges.txt","vocab.txt","tokenizer.model",
                                              "spiece.model","sentencepiece.bpe.model"}]))
    repo_component = "models--" + model_id.replace("/","--")
    canonical = root.parent.name == "snapshots" and root.name == revision and (
        root.parent.parent.name == repo_component)
    verified = []
    for file in files:
        if canonical:
            target = file.resolve()
            if target.parent.name != "blobs" or not _etag(file,target.name):
                raise ValueError("HF cache file does not match content-addressed blob: " + file.name)
        else:
            metadata = root / ".cache/huggingface/download" / (file.name + ".metadata")
            if not metadata.is_file():
                raise ValueError("local checkpoint lacks original HF download metadata: " + file.name)
            lines = metadata.read_text().splitlines()
            if len(lines) < 2 or lines[0] != revision or not _etag(file,lines[1].strip('"')):
                raise ValueError("checkpoint revision/content mismatch: " + file.name)
        verified.append(file.name)
    return {"id":model_id,"revision":revision,"immutable_revision_verified":True,
            "verified_files":verified,"local_files_only":True,"trust_remote_code":False,
            "verification":"HF content-addressed cache" if canonical else "HF local_dir commit/etag metadata"}
