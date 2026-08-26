#!/usr/bin/env python3
"""Generate, validate or scaffold declarative paper.yaml files."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.paper_specs.schema import (  # noqa: E402
    adapter_directory, load_spec, spec_from_adapter, validate_spec, write_spec,
)
from auto_research.reproductions.registry import get_adapter, list_adapters  # noqa: E402


def spec_path(adapter) -> Path:
    return adapter_directory(adapter, ROOT) / "paper.yaml"


def generate(keys: set[str] | None, check: bool) -> int:
    failures = []
    for adapter in list_adapters():
        if keys and adapter.key not in keys:
            continue
        path = spec_path(adapter)
        expected = spec_from_adapter(adapter, ROOT)
        expected_text = __import__("json").dumps(
            expected.to_dict(), ensure_ascii=False, indent=2
        ) + "\n"
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != expected_text:
                failures.append(adapter.key)
        else:
            write_spec(expected, path)
    if failures:
        raise SystemExit("stale or missing paper.yaml: " + ", ".join(failures))
    return 0


def validate(keys: set[str] | None) -> int:
    failures = []
    for adapter in list_adapters():
        if keys and adapter.key not in keys:
            continue
        path = spec_path(adapter)
        if not path.exists():
            failures.append(f"{adapter.key}: missing paper.yaml")
            continue
        failures.extend(
            f"{adapter.key}: {error}"
            for error in validate_spec(load_spec(path), root=ROOT, adapter=adapter)
        )
    if failures:
        raise SystemExit("\n".join(failures))
    return 0


def scaffold(path: Path, destination: Path) -> int:
    spec = load_spec(path)
    errors = validate_spec(spec)
    if errors:
        raise SystemExit("invalid spec: " + "; ".join(errors))
    if destination.exists():
        raise SystemExit(f"refusing to overwrite {destination}")
    destination.mkdir(parents=True)
    (destination / "__init__.py").write_text("", encoding="utf-8")
    (destination / "paper.yaml").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    (destination / "adapter.py").write_text(
        "\"\"\"Generated adapter skeleton; implement run/render before registration.\"\"\"\n"
        f"# Paper: {spec.paper_url}\n# Adapter key: {spec.key}\n",
        encoding="utf-8",
    )
    (destination / "experiment.py").write_text(
        "def run(dataset_dir, seed):\n    raise NotImplementedError('implement paper mechanism')\n",
        encoding="utf-8",
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["generate", "check", "validate", "scaffold"])
    parser.add_argument("--keys", default="")
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()
    keys = {value.strip() for value in args.keys.split(",") if value.strip()} or None
    if args.action in {"generate", "check"}:
        return generate(keys, args.action == "check")
    if args.action == "validate":
        return validate(keys)
    if not args.spec or not args.destination:
        raise SystemExit("scaffold requires --spec and --destination")
    return scaffold(args.spec, args.destination)


if __name__ == "__main__":
    raise SystemExit(main())
