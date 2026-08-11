#!/usr/bin/env python3
"""Execute paper adapters on CUDA and retain per-path device evidence.

This is an engineering audit, not a paper benchmark. Each adapter runs in its
normal isolated worker with a hard smoke timeout. A pass requires both a
successful result and at least one actual ``device_for`` resolution to CUDA;
adapters without a PyTorch device call are reported separately as CPU-only
execution rather than being mislabeled as GPU-validated.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import inspect
import os
from pathlib import Path
import time

from auto_research.reproductions.execution import run_with_budget
from auto_research.reproductions.registry import list_adapters
from auto_research.runtime import configure_runtime, runtime_summary


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--dataset-dir", type=Path, default=Path("data"))
    result.add_argument("--output", type=Path, required=True)
    result.add_argument("--timeout-seconds", type=int, default=30)
    result.add_argument("--seed", type=int, default=42)
    result.add_argument("--paper", action="append", default=[])
    result.add_argument("--include-concept-demos", action="store_true")
    result.add_argument("--resume", action="store_true")
    result.add_argument(
        "--only-explicit-device-packages", action="store_true",
        help="select adapters whose implementation package contains a CUDA/device hook",
    )
    result.add_argument("--shards", type=int, default=1)
    result.add_argument("--shard-index", type=int, default=0)
    return result


def main() -> int:
    args = parser().parse_args()
    if args.timeout_seconds < 1:
        raise SystemExit("--timeout-seconds must be positive")
    if args.shards < 1 or not 0 <= args.shard_index < args.shards:
        raise SystemExit("require shards >= 1 and 0 <= shard-index < shards")
    configure_runtime("cuda")
    import torch
    runtime = runtime_summary(torch)
    if runtime["resolved_device"] != "cuda":
        raise SystemExit(f"CUDA audit resolved {runtime['resolved_device']}")
    selected = [
        adapter for adapter in list_adapters()
        if (not args.paper or adapter.key in args.paper)
        and (args.include_concept_demos or adapter.fidelity.value != "concept_demo")
        and (
            not args.only_explicit_device_packages
            or _package_has_device_hook(adapter)
        )
    ]
    selected = [
        adapter for position, adapter in enumerate(selected)
        if position % args.shards == args.shard_index
    ]
    existing = _read_existing(args.output) if args.resume else {}
    rows = dict(existing)
    evidence_dir = args.output.with_suffix("").with_name(
        args.output.stem + "-device-evidence"
    )
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for position, adapter in enumerate(selected, start=1):
        if adapter.key in rows:
            continue
        evidence = evidence_dir / f"{adapter.key}.jsonl"
        evidence.unlink(missing_ok=True)
        os.environ["AUTO_RESEARCH_DEVICE_AUDIT_LOG"] = str(evidence.resolve())
        started = time.monotonic()
        try:
            result = run_with_budget(
                adapter, args.dataset_dir, args.seed, "smoke",
                timeout_override=args.timeout_seconds,
            )
            calls = _read_evidence(evidence)
            cuda_calls = [item for item in calls if item["resolved"].startswith("cuda")]
            status = "gpu_pass" if cuda_calls else "completed_without_device_call"
            row = {
                "status": status,
                "duration_seconds": time.monotonic() - started,
                "device_calls": len(calls),
                "cuda_calls": len(cuda_calls),
                "callers": sorted({
                    f"{Path(item['caller_file']).name}:{item['caller_line']}"
                    for item in cuda_calls
                }),
                "result_keys": sorted(result),
            }
        except Exception as exc:
            calls = _read_evidence(evidence)
            row = {
                "status": "timeout" if isinstance(exc, TimeoutError) else "failed",
                "duration_seconds": time.monotonic() - started,
                "device_calls": len(calls),
                "cuda_calls": sum(
                    item["resolved"].startswith("cuda") for item in calls
                ),
                "error": f"{type(exc).__name__}: {exc}",
            }
        rows[adapter.key] = row
        _write(args.output, runtime, rows, len(selected))
        print(
            f"[{position}/{len(selected)}] {adapter.key}: {row['status']} "
            f"({row['duration_seconds']:.1f}s)",
            flush=True,
        )
    _write(args.output, runtime, rows, len(selected))
    return int(any(row["status"] in {"failed", "timeout"} for row in rows.values()))


def _read_evidence(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _package_has_device_hook(adapter) -> bool:
    source = inspect.getsourcefile(adapter.run)
    if not source:
        return False
    needles = ("device_for(", "torch.cuda", ".cuda(")
    for path in _implementation_files(Path(source)):
        text = path.read_text(encoding="utf-8")
        if any(needle in text for needle in needles):
            return True
    return False


def _implementation_files(source: Path) -> tuple[Path, ...]:
    """Keep shared flat adapters from inheriting unrelated GPU hooks.

    Most adapters live in their own package, where sibling modules form one
    implementation. Batch-generated adapters instead point to one shared file
    directly under ``reproductions``; scanning that entire parent directory
    would incorrectly classify every one of them as a GPU adapter merely
    because some unrelated common module uses PyTorch.
    """
    if source.parent.name == "reproductions":
        return (source,)
    return tuple(source.parent.glob("*.py"))


def _read_existing(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8")).get("adapters", {})


def _write(path: Path, runtime: dict, rows: dict, selected: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for row in rows.values():
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    payload = {
        "schema_version": 1,
        "purpose": "engineering CUDA path audit; not paper benchmark metrics",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runtime": runtime,
        "selected_adapters": selected,
        "completed_adapters": len(rows),
        "status_counts": counts,
        "adapters": dict(sorted(rows.items())),
    }
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


if __name__ == "__main__":
    raise SystemExit(main())
