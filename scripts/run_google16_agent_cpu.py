"""Reproducible CPU mechanism artifacts; no model/agent capability benchmark."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re
import subprocess

from auto_research.agent_research.google16_dynamic_brt import Patch, review_patch, select_patch
from auto_research.agent_research.google16_hcrg import dependency_order, extract_python_graph, static_metrics
from auto_research.agent_research.google16_polca import Candidate, Polca

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = (
    "src/auto_research/agent_research/google16_dynamic_brt.py",
    "src/auto_research/agent_research/google16_polca.py",
    "src/auto_research/agent_research/google16_hcrg.py",
    "scripts/run_google16_agent_cpu.py",
)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def run_brt():
    buggy = "def increment(x):\n    return x\n"
    fixed = "def increment(x):\n    return x + 1\n"
    brt = "assert increment(2) == 3\n"
    regression = "assert increment(-1) == 0\n"
    patches = (Patch("with-test", fixed, brt), Patch("no-test-1", fixed, None),
               Patch("no-test-2", fixed, None), Patch("buggy", buggy, brt),
               Patch("trivial-test", fixed, "assert 1 == 1"))
    reviews = tuple(review_patch(p, buggy=buggy, regression=regression,
                                 bug_report="increment the integer by one") for p in patches)
    return {"method": "dynamic-brt", "diagnostic_only": True, "component_only": True,
            "fixture_generated_by_model": False, "semantic_reviewer_observed": False,
            "public_inputs": {"buggy": buggy, "fixed_fixture": fixed,
                              "brt_fixture": brt, "regression": regression},
            "reviews": [asdict(r) for r in reviews],
            "ranked_selected": select_patch(reviews, strategy="ranked").key,
            "dual_selected": select_patch(reviews, strategy="dual").key,
            "runtime_execution": "separate-real-Python-subprocess-per-source-test-pair"}


def run_polca(seed):
    controller = Polca(Candidate("base", "0", (0.,)), epsilon=.1, seed=seed,
                       max_metric_calls=16, max_memory=8)
    data = (("validation-0", 1.), ("validation-1", 2.))
    proposal_count = [0]

    def evaluator(candidate, value):
        score = -(float(candidate.parameter) - value) ** 2
        return score, f"synthetic scalar fixture reward={score}"

    def summarizer(history):
        return json.dumps({h.candidate.key: {"mean": h.mean, "count": len(h.observations)}
                           for h in history}, sort_keys=True)

    def proposer(history, summary):
        assert summary
        proposal_count[0] += 1
        parameter = float(history[0].candidate.parameter) + .5
        return [Candidate(f"proposal-{proposal_count[0]}", str(parameter), (parameter,))]

    for _ in range(3):
        controller.round(data, evaluator=evaluator, summarizer=summarizer, proposer=proposer)
    best = controller.best()
    return {"method": "polca", "diagnostic_only": True, "component_only": True,
            "callback_fixture": True, "real_llm_calls": 0,
            "embedding_kind": "synthetic-scalar-coordinate-not-semantic-embedding",
            "dataset": list(data), "history": [asdict(h) for h in controller.histories()],
            "traces": [asdict(t) for t in controller.traces], "metric_calls": controller.calls,
            "fixture_best": {"key": best.candidate.key, "mean": best.mean},
            "claim": "controller execution only, not LLM program optimization"}


def run_hcrg():
    sources = {"base": "class Base:\n    def save(self, value): return value\n",
               "mid": "from base import Base\nclass Middle(Base): pass\n",
               "child": "from mid import Middle\nclass Child(Middle): pass\n"}
    graph = extract_python_graph(sources)
    static_reference = 'class Base: pass\nclass Child(Base):\n    def f(self,x): return x\n'
    target = ('import os\nimport imaginary_package\nclass Base: pass\nclass Child:\n'
              '    def f(self,x:int)->int: return x\n')
    return {"method": "hcrg", "diagnostic_only": True, "component_only": True,
            "parser": graph.parser, "sources": sources, "source_sha256": graph.source_sha256,
            "graph": json.loads(graph.skeleton()),
            "dependency_order": dependency_order(graph),
            "three_hop_keys": [n.key for n in graph.retrieve("child.Child")],
            "static_reference": static_reference, "static_target": target,
            "partial_static_metrics": static_metrics(static_reference, target),
            "llm_migration_calls": 0, "java_ingestion_observed": False,
            "claim": "Python AST-supported graph subsystem, not Java-to-Python migration"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--source-commit")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("immutable output already exists")
    commit = args.source_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("exact source commit required")
    result = {"schema_version": 1, "protocol": "google16-agent-cpu-components-v1",
              "source_commit": commit, "seed": args.seed, "device": "cpu",
              "diagnostic_only": True, "component_only": True,
              "full_experiment_status": "not_reproduced_high_cost",
              "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                                for p in SOURCE_FILES},
              "components": [run_brt(), run_polca(args.seed), run_hcrg()]}
    result["content_sha256"] = fingerprint(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": str(args.output), "content_sha256": result["content_sha256"]}))


if __name__ == "__main__":
    main()
