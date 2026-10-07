#!/usr/bin/env python3
"""Contract gate for a base-only installed wheel (no repo docs or ML extras)."""

from __future__ import annotations

import importlib.abc
import json
from pathlib import Path
import sys
import tempfile


class RejectOptionalRuntime(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {
            "torch",
            "torchvision",
            "transformers",
            "tokenizers",
            "datasets",
            "PIL",
            "av",
            "safetensors",
            "huggingface_hub",
            "soundfile",
        }:
            raise AssertionError(f"base-only command imported optional runtime: {fullname}")
        return None


def main():
    sys.meta_path.insert(0, RejectOptionalRuntime())
    from auto_research.cli import build_parser, main as cli
    from auto_research.reproductions.registry import list_adapters
    from auto_research.paper_specs.catalog import catalog_records

    parser = build_parser()
    assert parser.parse_args(["reproduce", "--paper", "din"]).paper == "din"
    assert len(list_adapters()) >= 371
    assert len(catalog_records()) >= 736
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "manifest.json"
        assert cli(["reproduce", "--write-manifest", str(path)]) == 0
        assert len(json.loads(path.read_text())["papers"]) >= 371
        assert cli(["init", str(Path(directory) / "research.json")]) == 0
    assert not any(
        name.startswith("auto_research.reproductions.") and name.endswith(".adapter")
        for name in sys.modules
    )
    print("minimal-install metadata/help/init contracts passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
