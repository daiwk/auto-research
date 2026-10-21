"""CPU typed retrieval-program diagnostic; no policy, embedding or RL training."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import statistics
import subprocess

from auto_research.agent_research.retrieval_program import (
    Document, RetrievalProgram, RetrievalSDK, continuation_context, execute,
    supervision_spans, verified_mutation,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = ("scripts/run_oct21_rpl.py", "src/auto_research/agent_research/retrieval_program.py")


def diagnostic(seed):
    rng = random.Random(seed)
    docs = tuple(Document(f"doc-{index}", f"public document value {rng.randrange(10**9)}") for index in range(20))
    # Fixed ranking callbacks are SDK fixtures, explicitly not BM25/E5/Qwen.
    sdk = RetrievalSDK(dense=lambda query, top_k: docs[:top_k],
        sparse=lambda query, top_k: tuple(reversed(docs))[:top_k],
        rerank=lambda query, candidates, top_k: tuple(reversed(candidates))[:top_k])
    program = RetrievalProgram(("public query",), "dense", 3, 0, 5)
    baseline = execute(program, sdk)
    verifier = lambda execution: any(doc.identifier == "doc-4" for doc in execution.printed)
    selected, trials = verified_mutation(program, sdk, verifier=verifier)
    assert selected is not None and not verifier(baseline)
    assert selected.program.breadth == 5 and selected.program.queries == program.queries
    context = asdict(continuation_context("public question", selected))
    narrow = execute(RetrievalProgram(("public query",), "fuse", 10, 3, 3), sdk)
    bad_answer = supervision_spans(retrieval_verified=True, answer_verified=False)
    good_answer = supervision_spans(retrieval_verified=True, answer_verified=True)
    assert len(narrow.printed) == 3 and narrow.retrieved_candidates == 20
    assert bad_answer == {"program": True, "environment_observation": False, "answer": False}
    assert good_answer["answer"] and not good_answer["environment_observation"]
    return {"seed": seed, "fixture_sha256": hashlib.sha256(
        json.dumps([asdict(doc) for doc in docs], sort_keys=True).encode()).hexdigest(), "metrics": {
        "baseline_fixture_support_covered": int(verifier(baseline)),
        "selected_fixture_support_covered": int(verifier(selected.execution)),
        "mutation_programs_executed": len(trials), "selected_breadth": selected.program.breadth,
        "wide_program_retrieved_candidates": narrow.retrieved_candidates,
        "wide_program_printed_documents": len(narrow.printed),
        "continuation_private_top_level_fields": len(set(context) & {"gold", "answer", "verifier", "score"}),
        "incorrect_answer_supervised": int(bad_answer["answer"]),
        "verified_program_supervised": int(bad_answer["program"]), "actual_llm_calls": 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not 1 <= len(seeds) <= 5 or len(set(seeds)) != len(seeds) or any(not 0 <= seed < 2**32 for seed in seeds):
        parser.error("one to five distinct uint32 seeds required")
    if args.output.exists():
        parser.error("immutable output already exists")
    rows = [diagnostic(seed) for seed in seeds]
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    source_hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCE_PATHS}
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--", *SOURCE_PATHS], cwd=ROOT, text=True).strip())
    payload = {"schema_version": 2, "method": "rpl", "manifest_ref": "agent-research:rpl", "seeds": seeds,
        "device": "cpu", "evaluation_tier": "l1_mechanism",
        "dataset": {"id": "synthetic-rpl-sdk-rankings", "revision": "oct21-contract-v1", "capability_benchmark": False},
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": seeds, "formal_comparison": False,
            "claim_policy": "typed grammar and execution diagnostic; not neural retrieval or RL capability evidence"},
        "per_seed": rows, "metrics": {key: {"mean": statistics.mean(row["metrics"][key] for row in rows),
            "std": statistics.stdev(row["metrics"][key] for row in rows) if len(rows) > 1 else 0., "n": len(rows)}
            for key in rows[0]["metrics"]},
        "provenance": {"commit": commit, "artifact_path": args.output.as_posix(),
            "dataset_fingerprint": "sha256:" + hashlib.sha256("".join(row["fixture_sha256"] for row in rows).encode()).hexdigest(),
            "executed_source_uncommitted": dirty, "executed_source_sha256": source_hashes, "accelerator": "CPU"},
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "formal_comparison": False, "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"method": "rpl", "seeds": seeds, "output": str(args.output)}))


if __name__ == "__main__":
    main()
