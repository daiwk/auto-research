"""CPU-only Harness² controller diagnostic with actual trusted Python rollouts.

No model/API calls, no benchmark answer/rubric, no CUDA dependency. The scripted
editor and selector are test doubles, so this is L1 mechanics, not agent ability.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import time

from auto_research.agent_research.harness2 import (
    Edit, EvidenceLibrary, Execution, ExecutionConfig, Harness, Harness2, Lesson,
    PROTOCOL, PublicTask, UPSTREAM_COMMIT, fingerprint,
)

ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = """import csv
import sys
from decimal import Decimal
with open(sys.argv[1], encoding='utf-8') as stream:
    values = [Decimal(row['amount']) for row in csv.DictReader(stream)]
print(f'{sum((v for v in values if v > 0), Decimal(0)):.2f}')
"""
SOURCE_PATHS = ("scripts/run_harness2_component.py", "src/auto_research/agent_research/harness2.py")


def base_harness():
    return Harness((("systemprompt.md", "Sum signed ledger rows with scripts/summarize.py."),
                    ("scripts/summarize.py", BASE_SCRIPT)))


def executor(task, harness, config):
    """Only this diagnostic's generated helper is trusted; not an arbitrary-code service."""
    tree = harness.mapping()
    with tempfile.TemporaryDirectory(prefix="harness2-python-") as directory:
        root = Path(directory)
        (root / "summarize.py").write_text(tree["scripts/summarize.py"], encoding="utf-8")
        (root / "ledger.csv").write_text(dict(task.sources)["ledger.csv"], encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(root / "summarize.py"), str(root / "ledger.csv")],
                                cwd=root, capture_output=True, text=True, timeout=5, check=False)
        return Execution("Python helper executed on public ledger.csv.\nstdout:\n" + result.stdout,
                         result.stdout, result.returncode == 0,
                         "" if result.returncode == 0 else "Python helper failed")


def editor(context):
    """Deterministic mechanism fixture, not a substitute for a learned harness editor."""
    tree = context.current.mapping()
    supports = (context.references[0].label,)
    if context.stage == "invariant":
        tree["guardrails.md"] = "Apply the task request to every source record; do not silently filter rows."
        notes = "The base helper applies an undocumented positive-only filter."
    elif context.stage == "domain":
        tree["scripts/summarize.py"] = tree["scripts/summarize.py"].replace(" if v > 0", "")
        notes = "Signed-ledger request and the base source conflict at the positive-only filter."
    else:
        # Use executed domain proposals from the complete evidence pool, not a
        # precomputed expected total. Successful execution does not prove truth.
        domain = [e for e in context.pool if e.label.startswith("domain") and e.execution.ok]
        if domain:
            tree.update(domain[-1].harness.mapping())
            supports += (domain[-1].label,)
        invariant = [e for e in context.pool if e.label.startswith("invariant") and e.execution.ok]
        if invariant:
            tree["guardrails.md"] = invariant[-1].harness.mapping()["guardrails.md"]
            supports += (invariant[-1].label,)
        notes = "Compose executed domain helper with source-row guardrail; differing totals are behavioral evidence only."
    return Edit(Harness(tuple(sorted(tree.items()))), notes, supports)


def selector(context):
    # Outputs-only anonymized boundary is exercised without evaluating against
    # a hidden total. Choosing first is a declared fixture, not an agentic judge.
    return context.candidates[0][0]


def reflector(context):
    reference = context.evidence[0]
    changed = next((e for e in context.evidence if e.label.startswith("domain") and
                    e.execution.ok and e.harness.sha256 != reference.harness.sha256 and
                    e.execution.deliverable != reference.execution.deliverable), None)
    if changed is None:
        return None
    return Lesson("A signed ledger includes both debit and credit records.",
                  "Removing an undocumented sign filter changed actual output; inspect such filters against the current request.",
                  ((reference.label, changed.label),))


def run_seed(seed, mode, k, workers, root):
    rng = random.Random(seed)
    config = ExecutionConfig("trusted-python-ledger-script-v1-no-model", "stdlib-csv-decimal-isolated-subprocess-v1",
                             seed, "scripted-editor-selector-reflector-v1", base_harness().sha256)
    controller = Harness2(executor=executor, editor=editor, selector=selector, reflector=reflector,
                          config=config, mode=mode, k=k, workers=workers)
    library = EvidenceLibrary(root / f"{mode}-{seed}.json", controller.namespace)
    records, fixtures, checks = [], [], []
    for index in range(2):
        cents = [rng.randrange(1000, 20000), -rng.randrange(100, 900), rng.randrange(10, 1000)]
        contents = "amount\n" + "\n".join(str(Decimal(value)/100) for value in cents) + "\n"
        task = PublicTask(f"signed-ledger-{index}", "accounting",
                          "Sum every signed amount in ledger.csv; output one decimal total with two places.",
                          (("ledger.csv", contents),))
        result = controller.run(task, base_harness(), library=library, task_index=index)
        adopted = next(e for e in result.evidence if e.label == result.adopted)
        # Native post-run diagnostic checks are outside editor/selector/reflector
        # contexts. No capability benchmark or held-out inference claim follows.
        expected = f"{sum(Decimal(v)/100 for v in cents):.2f}\n"
        checks.append(adopted.execution.deliverable == expected)
        fixtures.append({"task": asdict(task), "config": asdict(config)})
        records.append({"summary": result.summary(), "evidence": [asdict(e) for e in result.evidence],
                        "stages": [{"label": s.label, "stage": s.context.stage,
                                    "current_harness_sha256": s.context.current.sha256,
                                    "pool_labels": [e.label for e in s.context.pool],
                                    "library_task_ids": [e.task_id for e in s.context.library],
                                    "edit": asdict(s.edit), "attempts": s.attempts,
                                    "fell_back": s.fell_back, "errors": list(s.errors)} for s in result.stages]})
    return {"seed": seed, "mode": mode, "fixture_sha256": fingerprint(fixtures),
            "metrics": {"tasks": 2, "actual_python_rollouts": sum(r["summary"]["rollouts"] for r in records),
                "improvement_stages": sum(r["summary"]["improvement_stages"] for r in records),
                "rollout_budget_identity_checks": sum(r["summary"]["rollouts"] == 4*k for r in records),
                "stage_budget_identity_checks": sum(r["summary"]["improvement_stages"] == 3*k for r in records),
                "script_mechanism_post_run_checks": sum(checks),
                "second_task_prior_library_entries": records[1]["summary"]["library_entries_seen"],
                "retained_evidence_lessons": sum(r["summary"]["lesson_retained"] for r in records),
                "failed_rollouts": sum(r["summary"]["failed_rollouts"] for r in records)},
            "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--mode", choices=("parallel", "sequential", "both"), default="both")
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seeds = tuple(int(v) for v in args.seeds.split(","))
    if not seeds or len(set(seeds)) != len(seeds):
        parser.error("unique integer seeds required")
    if args.output.exists():
        parser.error("refusing to overwrite previous execution evidence")
    modes = ("parallel", "sequential") if args.mode == "both" else (args.mode,)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="harness2-library-") as directory:
        rows = [run_seed(seed, mode, args.k, args.workers, Path(directory)) for seed in seeds for mode in modes]
    result = {"schema_version": 2, "method": "harness2", "protocol_id": PROTOCOL,
        "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
        "promotion_eligible": False, "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost", "device": "cpu",
        "dataset": {"id": "generated-signed-ledger", "revision": "signed-ledger-decimal-v1",
                    "public_benchmark": False},
        "upstream_commit": UPSTREAM_COMMIT,
        "source_sha256": {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in SOURCE_PATHS},
        "budget": {"k": args.k, "modes": list(modes), "workers": args.workers},
        "seeds": list(seeds), "elapsed_seconds": time.monotonic()-started, "per_seed_mode": rows,
        "boundary": "Deterministic editor/selector fixtures and trusted Python execution; no model-backed agent or benchmark ability; native numeric checks occur after adoption."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "elapsed_seconds": result["elapsed_seconds"],
                      "actual_python_rollouts": sum(r["metrics"]["actual_python_rollouts"] for r in rows),
                      "seed_modes": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
