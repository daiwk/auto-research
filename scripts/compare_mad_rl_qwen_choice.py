"""Validation-selected, paired comparison of bounded Qwen MaD-RL diagnostics.

This audits real checkpoint updates on a synthetic five-choice suite; it must
not be interpreted as the paper's multilingual math/code reproduction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from auto_research.post_training.paired_public_comparison import PublicRun, compare_runs


def summarize(directory: Path, *, arms: tuple[str, ...], seeds: tuple[int, ...],
              baseline: str = "l2") -> dict:
    if baseline not in arms or len(set(arms)) != len(arms) or len(set(seeds)) != len(seeds):
        raise ValueError("baseline, arms and seeds must identify distinct runs")
    records = {}
    runs = []
    reference_protocol = None
    for arm in arms:
        for seed in seeds:
            record = json.loads((directory / f"{arm}-{seed}.json").read_text(encoding="utf-8"))
            if (not record["diagnostic_only"] or record["paper_result_reproduced"] or
                    record["test_used_for_selection"] or record["seed"] != seed or
                    record["divergence"] != arm):
                raise ValueError(f"invalid diagnostic provenance for {arm}-{seed}")
            protocol = tuple(json.dumps(record[key], sort_keys=True) for key in (
                "target", "train_topics", "validation_topics", "test_topics",
                "steps", "warmup_steps", "group_size", "model_revision",
            ))
            if reference_protocol is None:
                reference_protocol = protocol
            elif protocol != reference_protocol:
                raise ValueError("public-task data, model or training budgets differ")
            validation = record["final_validation"]["jsd_to_target_valid_only"]
            test = record["final_test"]["jsd_to_target_valid_only"]
            if validation is None or test is None:
                raise ValueError("cannot compare runs without valid sampled choices")
            records[(arm, seed)] = record
            data_fingerprint = hashlib.sha256("|".join(protocol[:4]).encode()).hexdigest()
            runs.append(PublicRun(
                method=arm, seed=seed,
                validation_score=float(validation), test_score=float(test),
                update_steps=int(record["steps"]) + int(record["warmup_steps"]),
                generated_tokens=int(record["group_size"]),
                dataset_revision=data_fingerprint,
                checkpoint_revision=record["model_revision"],
            ))
    summary = compare_runs(tuple(runs), baseline=baseline, maximize=False)
    summary.update({
        "evidence_tier": "bounded_synthetic_choice_diagnostic",
        "paper_result_reproduced": False,
        "metric": "valid_choice_conditional_jsd_to_target_lower_is_better",
        "arms": list(arms),
        "warmup_updates": records[(baseline, seeds[0])]["warmup_steps"],
        "rl_updates": records[(baseline, seeds[0])]["steps"],
        "group_size": records[(baseline, seeds[0])]["group_size"],
        "validation_jsd_by_seed": {
            arm: [records[(arm, seed)]["final_validation"]["jsd_to_target_valid_only"] for seed in seeds]
            for arm in arms
        },
        "test_jsd_by_seed": {
            arm: [records[(arm, seed)]["final_test"]["jsd_to_target_valid_only"] for seed in seeds]
            for arm in arms
        },
        "validation_off_support_rate_by_seed": {
            arm: [records[(arm, seed)]["final_validation"]["off_support_rate"] for seed in seeds]
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
        args.directory, arms=("l2", "forward-kl", "jsd"),
        seeds=tuple(int(value) for value in args.seeds.split(",")),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
