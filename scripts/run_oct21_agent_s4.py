"""CPU Agent S4 control-plane diagnostic; no LLM, browser or GUI claims."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess

from auto_research.agent_research.agent_s4 import Population, PublicTask, PublicTrajectory, Repository

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = ("scripts/run_oct21_agent_s4.py", "src/auto_research/agent_research/agent_s4.py")


def diagnostic(seed):
    rng = random.Random(seed)
    tasks = tuple(PublicTask(f"task-{index}", json.dumps([rng.randrange(10) for _ in range(5)]))
                  for index in range(9))
    builder_views, grader_ids, agent_calls = [], [], []

    def actor(repository, task):
        # Fixed arithmetic actor. Repository content is an opaque version token,
        # not an automatically invented or executed interface implementation.
        agent_calls.append(task.task_id)
        numbers = json.loads(task.instruction)
        complete = any(name == "batch_reader.py" for name, _ in repository.files)
        observed = numbers if complete else numbers[:2]
        return PublicTrajectory(task.task_id, tuple(f"read cell: {n}" for n in observed), str(sum(observed)))

    def grader(task, trajectory):
        grader_ids.append(task.task_id)
        actual = int(trajectory.final_output)
        expected = sum(json.loads(task.instruction))
        return float(actual == expected)

    def builder(view):
        builder_views.append(view)
        parent = view.parents[0].repository
        if len(builder_views) == 2:
            return Repository((("cell_reader.py", "# deliberately reduced fixture variant"),))
        return Repository(tuple(dict(parent.files + (("batch_reader.py", "# fixture token, no LLM code generation"),)).items()),
            ("Synthetic public read observations only; no validation feedback.",))

    population = Population(Repository((("cell_reader.py", "# fixture token"),)),
        training_tasks=tasks[:3], validation_tasks=tasks[3:], task_agent=actor,
        validation_grader=grader, seed=seed, benchmark="scienceboard")
    for _ in range(4):
        population.advance(builder)
    before = len(agent_calls)
    denoised = population.denoise_top(3)
    removed = population.prune_lowest(1)
    winner, _ = population.selected()
    visible = [asdict(view) for view in builder_views]
    encoded = json.dumps(visible, sort_keys=True)
    summaries = {row.variant_id: row for row in population.summaries}
    checks = {"feedback_isolation": not any(task.task_id in encoded for task in tasks[3:]),
        "no_training_grader_calls": set(grader_ids) == {task.task_id for task in tasks[3:]},
        "parent_arity": all(len(item.parent_ids) == (2 if item.operator == "crossover" else 1)
               for item in population.lineage[1:]),
        "distinct_crossover_parents": all(len(set(item.parent_ids)) == len(item.parent_ids)
               for item in population.lineage),
        "lower_score_not_rejected": "v2" in summaries and summaries["v2"].mean_validation < summaries["v1"].mean_validation,
        "pruned_lineage_retained": len(population.lineage) == 5 and len(removed) == 1,
        "validation_only_denoise": len(agent_calls) - before == 3 * len(tasks[3:])}
    assert all(checks.values())
    metrics = {"evaluated_variants": len(population.summaries), "mutation_steps": 2,
        "crossover_steps": 2, "retained_reduced_fixture_variant": int(any(s.variant_id == "v2" for s in population.summaries)),
        "parent_eligibility_pruned": len(removed), "preserved_lineage_records": len(population.lineage),
        "denoised_variants": len(denoised), "denoise_validation_rollouts": len(agent_calls) - before,
        "builder_validation_task_ids_exposed": 0, "training_grader_calls": 0,
        "actual_llm_calls": 0, "actual_gui_calls": 0}
    return {"seed": seed, "metrics": metrics, "checks": checks,
        "selected_fixture_variant": winner,
        "fixture_sha256": hashlib.sha256(json.dumps([asdict(task) for task in tasks], sort_keys=True).encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--source-commit", default=None)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not 1 <= len(seeds) <= 3 or len(seeds) != len(set(seeds)) or any(not 0 <= seed < 2**32 for seed in seeds):
        parser.error("one to three distinct uint32 seeds required")
    if args.output.exists():
        parser.error("immutable output already exists")
    source_commit = args.source_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        parser.error("source commit must be full 40-character lowercase hex")
    payload = {"schema_version": 2, "device": "cpu", "seeds": seeds, "accelerator": "CPU",
        "code_commit": source_commit,
        "source_sha256": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCE_PATHS},
        "executed_source_uncommitted": bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--", *SOURCE_PATHS], cwd=ROOT, text=True).strip()),
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "evaluation_tier": "l1_mechanism", "formal_comparison": False,
        "dataset": {"id": "synthetic-agent-s4-control-plane", "revision": "oct21-followup-v1",
            "capability_benchmark": False},
        "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
        "components": {"agent-s4": {"per_seed": [diagnostic(seed) for seed in seeds]}}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"component": "agent-s4", "seeds": seeds, "output": str(args.output)}))


if __name__ == "__main__":
    main()
