"""Audit paired Qwen/GSM8K DCE and OPSD diagnostics without test-based selection.

Inputs are independently executed outputs of ``recursive_opsd_public_math.py``.
The ``generated_tokens`` field in the shared comparison contract denotes the
*per-generation cap*, not the realized output length (which may differ).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.post_training.paired_public_comparison import PublicRun, compare_runs


def summarize(directory: Path, *, arms: tuple[str, ...], seeds: tuple[int, ...],
              baseline: str = "frozen") -> dict:
    if baseline not in arms or len(set(arms)) != len(arms) or len(set(seeds)) != len(seeds):
        raise ValueError("baseline, arms and seeds must identify distinct runs")
    runs = []
    for arm in arms:
        for seed in seeds:
            record = json.loads((directory / f"{arm}-{seed}.json").read_text(encoding="utf-8"))
            protocol = record["protocol"]
            if (not record["diagnostic_only"] or record["paper_result_reproduced"] or
                    protocol["seed"] != seed or protocol["test_used_for_selection"]):
                raise ValueError(f"invalid diagnostic provenance for {arm}-{seed}")
            expected_method = "DCE" if arm == "dce" else "DCE+SRCL"
            expected_teacher = "frozen" if arm == "frozen" else "dynamic"
            if record["method"] != expected_method or record["teacher_mode"] != expected_teacher:
                raise ValueError(f"method mismatch for {arm}-{seed}")
            if min(protocol["train_examples"], protocol["validation_examples"],
                   protocol["test_examples"]) < 1:
                raise ValueError("all public splits must be nonempty")
            runs.append(PublicRun(
                method=arm, seed=seed,
                validation_score=float(record["final_validation"]["accuracy"]),
                test_score=float(record["final_test"]["accuracy"]),
                update_steps=int(protocol["steps"]),
                generated_tokens=int(protocol["max_new_tokens"]),
                dataset_revision=record["public_dataset"]["revision"],
                checkpoint_revision=record["public_model"]["revision"],
            ))
    summary = compare_runs(tuple(runs), baseline=baseline)
    summary.update({
        "evidence_tier": "bounded_public_task_diagnostic",
        "paper_result_reproduced": False,
        "official_test_is_held_out": True,
        "arms": list(arms),
        "seed_validation_accuracy": {
            arm: {str(seed): next(row.validation_score for row in runs if row.method == arm and row.seed == seed)
                  for seed in seeds}
            for arm in arms
        },
        "seed_test_accuracy": {
            arm: {str(seed): next(row.test_score for row in runs if row.method == arm and row.seed == seed)
                  for seed in seeds}
            for arm in arms
        },
    })
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", default="42,43,44")
    args = parser.parse_args()
    result = summarize(
        args.directory, arms=("dynamic", "frozen", "dce"),
        seeds=tuple(int(value) for value in args.seeds.split(",")),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
