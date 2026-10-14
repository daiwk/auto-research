#!/usr/bin/env python3
"""Download only pinned public EmbeddingGemma 2 inputs, then bind byte hashes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.multimodal.embedding_gemma2 import MODEL_ID, REVISION, WEIGHTS_SHA256, checkpoint_inputs
from auto_research.oct12_public_sources import sha256_file


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--finalize-existing", action="store_true",
                        help="verify a mirror downloaded from the pinned URLs; never use arbitrary weights")
    args = parser.parse_args()
    if not args.finalize_existing:
        from huggingface_hub import snapshot_download
        snapshot_download(MODEL_ID, revision=REVISION, local_dir=args.output,
                          allow_patterns=["*.json", "*.safetensors", "*.model", "*.jinja"],
                          max_workers=2)
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
