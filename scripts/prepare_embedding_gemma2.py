#!/usr/bin/env python3
"""Download only pinned public EmbeddingGemma 2 inputs, then bind byte hashes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import time

from auto_research.multimodal.embedding_gemma2 import MODEL_ID, REVISION, WEIGHTS_SHA256, checkpoint_inputs
from auto_research.oct12_public_sources import sha256_file

FILES = ("config.json", "processor_config.json", "preprocessor_config.json", "tokenizer_config.json",
         "tokenizer.json", "tokenizer.model", "chat_template.jinja", "config_sentence_transformers.json",
         "sentence_bert_config.json", "modules.json", "model.safetensors")


def download_inputs(output, *, maximum_seconds=600):
    """Finite one-pass public download; retain partial weight for explicit resume."""
    if not 1 <= maximum_seconds <= 900:
        raise ValueError("download budget must be 1..900 seconds; no unbounded retry")
    output.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + maximum_seconds
    for name in FILES:
        path = output / name
        if name == "model.safetensors" and path.is_file() and sha256_file(path) == WEIGHTS_SHA256:
            continue  # Immutable large input can be reused, never trusted by filename alone.
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("public checkpoint download budget exhausted")
        command = ["curl", "--fail", "--location", "--silent", "--show-error",
                   "--connect-timeout", "10", "--max-time", str(remaining)]
        if name == "model.safetensors":
            command += ["--continue-at", "-"]
        command += ["--output", str(path), f"https://huggingface.co/{MODEL_ID}/resolve/{REVISION}/{name}"]
        subprocess.run(command, check=True, timeout=remaining + 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--finalize-existing", action="store_true",
                        help="verify a mirror downloaded from the pinned URLs; never use arbitrary weights")
    parser.add_argument("--download-budget-seconds", type=int, default=600)
    args = parser.parse_args()
    if not args.finalize_existing:
        download_inputs(args.output, maximum_seconds=args.download_budget_seconds)
    files = {relative: sha256_file(args.output / relative)
             for relative in checkpoint_inputs(args.output)}
    required = {"config.json", "processor_config.json", "preprocessor_config.json",
                "tokenizer.json", "tokenizer_config.json", "model.safetensors"}
    if not required <= set(files):
        raise ValueError("complete public model inputs required")
    if files["model.safetensors"] != WEIGHTS_SHA256:
        raise ValueError("official pinned weights SHA256 mismatch")
    (args.output / "provenance.json").write_text(json.dumps({"kind": "checkpoint", "public_id": MODEL_ID,
        "revision": REVISION, "source": f"https://huggingface.co/{MODEL_ID}/tree/{REVISION}",
        "files": files}, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"public_id": MODEL_ID, "revision": REVISION, "files": len(files)}))


if __name__ == "__main__":
    main()
