#!/usr/bin/env python3
"""Frozen CPU mapping diagnostics, not a learned retrieval capability run."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess
import time

from auto_research.reproductions.sid_topology import (
    Item, insert_preserving, ranked_assignment, remapped_fraction, resolve_paths,
)

ROOT = Path(__file__).resolve().parents[1]


def diagnostic(seed):
    rng = random.Random(seed)
    old_items = [Item(f"old-{i}", (1, 2), 0, 0, rng.random()+1, 0) for i in range(8)]
    old = ranked_assignment(old_items, head=3, tail_buckets=8, tail_group_size=2)
    arrivals = [Item(f"new-{i}", (1, 2), 0, 0, 10+i, 0) for i in range(3)]
    items = [*old_items, *arrivals]
    frozen = insert_preserving(old, items, head=3, tail_buckets=8, tail_group_size=2)
    full = ranked_assignment(items, head=3, tail_buckets=8, tail_group_size=2)
    old_snapshot = dict(old)
    permutation = list(items)
    rng.shuffle(permutation)
    permuted = insert_preserving(old, permutation, head=3, tail_buckets=8, tail_group_size=2)
    retained = sum(key in resolve_paths(frozen, [sid]) for key, sid in old.items())
    lost = sum(key not in resolve_paths(full, [sid]) for key, sid in old.items())
    result = {"old_sid_remapped_fraction": remapped_fraction(old, frozen),
              "full_remap_negative_control_fraction": remapped_fraction(old, full),
              "frozen_old_path_address_recovery": retained / len(old),
              "full_remap_old_address_losses": lost,
              "insertion_order_mismatches": sum(permuted[k] != v for k, v in frozen.items()),
              "head_collision_members": len(resolve_paths(frozen, [old["old-0"]])),
              "input_mapping_mutated": old != old_snapshot,
              "learned_retriever_evaluated": False, "production_ab_reproduced": False}
    assert retained == len(old) and lost > 0 and result["old_sid_remapped_fraction"] == 0
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    if not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 8 or any(not 0 <= x < 2**32 for x in seeds):
        parser.error("1..8 unique uint32 seeds required")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("full lowercase frozen commit required")
    if args.output.exists():
        parser.error("immutable output; choose a fresh path")
    start = time.monotonic()
    per_seed = [{"seed": seed, "metrics": diagnostic(seed)} for seed in seeds]
    source = ("scripts/run_oct20_sid_topology.py", "src/auto_research/reproductions/sid_topology.py")
    hashes = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source}
    boundary = {"diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False}
    dataset = {"id": "synthetic-sid-topology-mapping-fixture", "revision": "oct20-sid-topology-v1", "capability_benchmark": False}
    payload = {"schema_version": 1, "code_commit": commit, "device": "cpu", "accelerator": "CPU", "seeds": seeds,
               **boundary, "executed_source_sha256": hashes, "elapsed_seconds": time.monotonic()-start,
               "components": {"sid-topology": {"dataset": dataset, "per_seed": per_seed,
                   "full_experiment_status": "not_reproduced_high_cost", **boundary}}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "elapsed_seconds": payload["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
