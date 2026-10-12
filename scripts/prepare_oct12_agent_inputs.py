#!/usr/bin/env python3
"""Prepare bounded, pinned Oct12 inputs offline; --output is a fresh directory.

Example: python scripts/prepare_oct12_agent_inputs.py --source rated
  --raw-dir .cache/oct12-public --output runs/rated-inputs

No download, checkpoint loading, or tool invocation occurs. Exact official raw
hashes are checked before parsing. Labels are copied only for external scoring.
RATED's unbound tool code deliberately fails; this export is not live-tool
capability evidence. Real bindings must be explicitly supplied by the caller.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import csv
import hashlib
from itertools import islice
import json
import math
from pathlib import Path
from typing import Iterable, Mapping


LONGMEM_REVISION = "98d7416c24c778c2fee6e6f3006e7a073259d48f"
ECO_REVISION = "bc5db40a20b254c5249401d2220ea71b06c86a5c"
ECO_PATHS = {
    "tools_clean_with_reliability.csv": "data/processed/tools_clean_with_reliability.csv",
    "train_pairs.csv": "data/ecoagent_syn/train_pairs.csv",
    "eval_real_test.jsonl": "data/ecoagent_real_toolbench/eval_real_test.jsonl",
}
SOURCE_SPECS = {
    "t2mem": {
        "public_id": "xiaowu0162/longmemeval-cleaned",
        "revision": LONGMEM_REVISION,
        "sha256": {
            "longmemeval_s_cleaned.json":
                "d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442",
        },
        "fixed_urls": {
            "longmemeval_s_cleaned.json":
                "https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/"
                + LONGMEM_REVISION + "/longmemeval_s_cleaned.json",
        },
    },
    "rated": {
        "public_id": "Elliotes/EcoAgent",
        "revision": ECO_REVISION,
        "sha256": {
            "tools_clean_with_reliability.csv":
                "1b388d317aeb1004c266eb65ff64a4864e7907412a2fbfb4667c492a871e8d8e",
            "train_pairs.csv":
                "e89aed2b42bba90ed6133bb64d1918591b50c60e9ec8561dce9799ae857f4760",
            "eval_real_test.jsonl":
                "922ba0256f49205f7b5225467e20d0d45ed4af243fc3f7313267327818a8e93c",
        },
        "fixed_urls": {
            name: "https://media.githubusercontent.com/media/Elliotes/EcoAgent/"
                  + ECO_REVISION + "/" + relative
            for name, relative in ECO_PATHS.items()
        },
        "git_lfs_pointer_urls": {
            name: "https://raw.githubusercontent.com/Elliotes/EcoAgent/"
                  + ECO_REVISION + "/" + relative
            for name, relative in ECO_PATHS.items()
        },
    },
}
UNAVAILABLE_TOOL_CODE = (
    'raise RuntimeError("Original public-catalog API backend and credentials are '
    'unavailable; no semantic tool success claimed")'
)
EXECUTION_LIMITATION = (
    "original service bindings unavailable; explicit fail-closed sandbox errors, "
    "not fake metadata-only successes"
)
CSV_FIELD_LIMIT = 16 * 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def positive_budget(value: int) -> int:
    if value <= 0:
        raise ValueError("budgets must be positive")
    return value


def verify_raw_files(source: str, raw_dir: Path) -> dict[str, Path]:
    """Validate hard-coded pins, not a caller-written provenance claim."""
    spec = SOURCE_SPECS[source]
    paths = {}
    for name, expected in spec["sha256"].items():
        path = raw_dir / name
        if source == "t2mem" and not path.exists():
            path = raw_dir / "longmemeval" / name
        if not path.is_file():
            raise FileNotFoundError(f"required offline raw file is missing: {path}")
        if sha256_file(path) != expected:
            raise ValueError(f"official upstream SHA256 mismatch: {name}")
        paths[name] = path
    return paths


@contextmanager
def csv_rows(path: Path, required: set[str]):
    """BOM-aware parsing with bounded long fields; restore process-global limit."""
    previous_limit = csv.field_size_limit()
    csv.field_size_limit(CSV_FIELD_LIMIT)
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not required.issubset(reader.fieldnames or []):
                raise ValueError(f"required CSV columns missing: {path.name}")
            yield reader
    finally:
        csv.field_size_limit(previous_limit)


def convert_memory_rows(rows: Iterable[Mapping], maximum: int = 2) -> list[dict]:
    """Select by official order only, preserving complete sessions and labels."""
    selected = list(islice(rows, positive_budget(maximum)))
    if len(selected) != maximum:
        raise ValueError("insufficient official memory queries for requested budget")
    return [
        {"source_revision": LONGMEM_REVISION, "question_id": row["question_id"],
         "question": row["question"], "sessions": row["haystack_sessions"],
         "answer": row["answer"]}
        for row in selected
    ]


def select_training_pool(catalog: Mapping[str, Mapping],
                         training_rows: Iterable[Mapping], maximum: int = 32):
    """No test rows/labels are accepted; each positive UID supplies one pair."""
    positive_budget(maximum)
    tools, pairs = {}, []
    for row in training_rows:
        key = row["tool_uid"]
        if row["label"] != "1" or key not in catalog or key in tools:
            continue
        metadata = catalog[key]
        prior = float(metadata["reliability_score"])
        if not math.isfinite(prior) or not 0 <= prior <= 1:
            raise ValueError(f"invalid public reliability score: {key}")
        tools[key] = {"text": metadata["tool_text"], "prior": prior,
                      "code": UNAVAILABLE_TOOL_CODE}
        pairs.append({"split": "train", "query": row["query"],
                      "tool_text": metadata["tool_text"]})
        if len(tools) == maximum:
            break
    if len(tools) != maximum:
        raise ValueError("insufficient unique training-positive tool UIDs")
    return tools, pairs


def select_test_queries(test_rows: Iterable[Mapping], train_queries: set[str],
                        maximum: int = 8) -> list[dict]:
    """Selection uses order/query overlap only; reference is opaque scorer data."""
    positive_budget(maximum)
    queries = []
    for row in test_rows:
        if row["query"] in train_queries:
            continue
        queries.append({"split": "test", "query": row["query"],
                        "reference_tool": row["ground_truth"]})
        if len(queries) == maximum:
            break
    if len(queries) != maximum:
        raise ValueError("insufficient train-disjoint official test queries")
    return queries


def jsonl_rows(path: Path):
    with path.open(encoding="utf-8-sig") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def convert_rated_files(paths: Mapping[str, Path], pool_tools: int = 32,
                        test_queries: int = 8) -> dict:
    with csv_rows(paths["tools_clean_with_reliability.csv"],
                  {"uid", "tool_text", "reliability_score"}) as rows:
        catalog = {row["uid"]: row for row in rows}
    with csv_rows(paths["train_pairs.csv"], {"query", "tool_uid", "label"}) as rows:
        tools, pairs = select_training_pool(catalog, rows, pool_tools)
    test_rows = jsonl_rows(paths["eval_real_test.jsonl"])
    try:
        queries = select_test_queries(test_rows, {row["query"] for row in pairs},
                                      test_queries)
    finally:
        test_rows.close()
    return {"source_revision": ECO_REVISION, "tools": tools, "pairs": pairs,
            "queries": queries}


def prepare_inputs(source: str, raw_dir: Path, output: Path, *,
                   memory_queries: int = 2, pool_tools: int = 32,
                   test_queries: int = 8) -> dict:
    """Verify and convert before creating output; never overwrite source data."""
    for budget in (memory_queries, pool_tools, test_queries):
        positive_budget(budget)
    if output.exists():
        raise FileExistsError("a fresh output directory is required")
    paths = verify_raw_files(source, raw_dir)
    spec = SOURCE_SPECS[source]
    manifest = {"kind": "dataset", "public_id": spec["public_id"],
                "revision": spec["revision"]}
    if source == "t2mem":
        with paths["longmemeval_s_cleaned.json"].open(encoding="utf-8-sig") as handle:
            converted = convert_memory_rows(json.load(handle), memory_queries)
        filename = f"t2mem-first{memory_queries}.jsonl"
        data = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in converted)
        prefix = "two" if memory_queries == 2 else str(memory_queries)
        manifest.update({
            "upstream_file": "longmemeval_s_cleaned.json",
            "upstream_sha256": spec["sha256"]["longmemeval_s_cleaned.json"],
            "transformation": f"first {prefix} official ordered queries, every haystack "
                              "session preserved; gold used only by external scorer",
            "rows": len(converted),
            "budgets": {"memory_queries": memory_queries},
            "gold_boundary": "answer is external-scoring data, not rollout/retrieval input",
        })
    else:
        payload = convert_rated_files(paths, pool_tools, test_queries)
        filename = f"rated-train{pool_tools}-test{test_queries}.json"
        data = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        prefix = "eight" if test_queries == 8 else str(test_queries)
        manifest.update({
            "upstream_file_sha256": dict(spec["sha256"]),
            "training_pairs": len(payload["pairs"]), "pool_tools": len(payload["tools"]),
            "test_queries": len(payload["queries"]),
            "transformation": "pool from first ordered training positives only; "
                              f"first {prefix} disjoint official test queries; "
                              "no test-label-selected tools",
            "execution_limitation": EXECUTION_LIMITATION,
            "evidence_level": "diagnostic", "tool_execution_status": "unbound_fail_closed",
            "real_tool_execution_validated": False,
            "gold_boundary": "reference_tool is external-scoring data, not retrieval input",
            "budgets": {"pool_tools": pool_tools, "test_queries": test_queries},
            "git_lfs_pointer_urls": dict(spec["git_lfs_pointer_urls"]),
        })
    raw = data.encode("utf-8")
    manifest.update({"fixed_urls": dict(spec["fixed_urls"]),
                     "source_verification": "fixed official revision and raw SHA256 before parsing",
                     "downloads_performed": False,
                     "files": {filename: hashlib.sha256(raw).hexdigest()}})
    output.mkdir(parents=True)
    (output / filename).write_bytes(raw)
    (output / "provenance.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, choices=["t2mem", "rated"])
    parser.add_argument("--raw-dir", required=True, type=Path,
                        help="offline raw directory; LongMemEval may be in its longmemeval child")
    parser.add_argument("--output", required=True, type=Path, help="fresh output directory")
    parser.add_argument("--memory-queries", type=int, default=2)
    parser.add_argument("--pool-tools", type=int, default=32)
    parser.add_argument("--test-queries", type=int, default=8)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    manifest = prepare_inputs(args.source, args.raw_dir, args.output,
                              memory_queries=args.memory_queries, pool_tools=args.pool_tools,
                              test_queries=args.test_queries)
    print(json.dumps({"source": args.source, "revision": manifest["revision"],
                      "files": manifest["files"],
                      "tool_execution_status": manifest.get("tool_execution_status")},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
