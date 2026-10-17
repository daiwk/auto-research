#!/usr/bin/env python3
"""CPU-only SSR and paired-budget protocol diagnostics on explicit synthetic inputs."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
import re
import statistics
import subprocess
import time

from auto_research.agent_research.structural_signal_retriever import (
    AgentCard, StructuralSignalIndex, outcome_counts, structural_signals,
    validate_orchestrator_selection,
)
from auto_research.foundation_models.muon_paired_budget import (
    ValidationTrajectory, frozen_pool_regret, normalized_validation_auc,
    paired_budget_comparison, paired_relative_gain_interval, select_by_validation_data_auc,
    stable_data_crossover,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {"structural-signal-retriever": "src/auto_research/agent_research/structural_signal_retriever.py",
           "muon-paired-budget": "src/auto_research/foundation_models/muon_paired_budget.py"}


def ssr_diagnostic(seed: int) -> dict:
    rng = random.Random(seed)
    vocabulary = ["database", "search", "visual", "speech", "classify", "extract", "language", "sql",
                  "remote", "local", "python", "finance", "medical", "policy", "image", "summarize"]
    cards = [AgentCard(f"card-{i:03d}", description=" ".join(rng.sample(vocabulary, 5))) for i in range(64)]
    index = StructuralSignalIndex(cards)
    signals = {card.identifier: structural_signals(card.capability_text()) for card in cards}
    df = Counter(signal for doc in signals.values() for signal in doc)
    max_error, equivalence_cases = 0., 0
    for _ in range(12):
        query = " ".join(rng.sample(vocabulary, 3))
        query_signals = structural_signals(query)
        expected = []
        for identifier, doc in signals.items():
            overlap = tuple(sorted(query_signals.intersection(doc)))
            if overlap:
                score = sum(math.log(65 / (df[signal] + 1)) + 1 for signal in overlap)
                expected.append((identifier, score, overlap))
        expected.sort(key=lambda row: (-row[1], -len(row[2]), row[0]))
        result = index.query(query, top_k=20)
        assert [hit.identifier for hit in result] == [row[0] for row in expected[:20]]
        max_error = max(max_error, *(abs(hit.score - row[1]) for hit, row in zip(result, expected)))
        equivalence_cases += 1
    assert not index.query("unmatchedxyz") and not index.query("the is of")
    pool = index.query("database")
    assert pool
    outcomes = outcome_counts([
        validate_orchestrator_selection(pool, 1), validate_orchestrator_selection(pool, 0),
        validate_orchestrator_selection(pool, 1, api_failed=True), validate_orchestrator_selection([]),
    ])
    assert outcomes["total_attempts"] == 4 and all(outcomes[key] == 1 for key in outcomes if key != "total_attempts")
    assert max_error < 1e-12
    return {"fullscan_ranking_equivalence_queries": equivalence_cases, "fullscan_score_max_error": max_error,
            "registry_cards": len(cards), "signal_limit": 64, "no_match_returns_empty": True,
            **{f"fixture_{key}": value for key, value in outcomes.items()},
            "orchestrator_model_calls": 0}


def muon_diagnostic(seed: int) -> dict:
    rng = random.Random(seed)
    offset = rng.uniform(0, .03)
    data = (0., 1., 2., 3., 4.)
    ref = ValidationTrajectory("reference", seed, data, data, tuple(v + offset for v in (4., 3., 2., 1.5, 1.)))
    alt = ValidationTrajectory("alternative", seed, data, (0., 2., 4., 6., 8.),
                               tuple(v + offset for v in (4., 2.6, 1.5, 1.1, .7)))
    data_result = paired_budget_comparison(ref, alt, axis="data")
    time_result = paired_budget_comparison(ref, alt, axis="time")
    error = max(abs(data_result["reference_auc"] - (2.25 + offset)),
                abs(data_result["alternative_auc"] - (1.8875 + offset)),
                abs(time_result["alternative_auc"] - (2.675 + offset)))
    short_partial_auc = normalized_validation_auc((0., 2., 5.), (6., 4., 1.), 3.)
    assert abs(short_partial_auc - 4.5) < 1e-12
    assert data_result["relative_auc_gain"] > 0 and time_result["relative_auc_gain"] < 0 and error < 1e-12
    better_auc = ValidationTrajectory("better-data-auc", seed, data, data, (4., 1., 1., 1., 2.))
    selected = select_by_validation_data_auc([ref, better_auc])
    assert selected.run_id == "better-data-auc" and selected.validation_loss[-1] > ref.validation_loss[-1]
    flat = ValidationTrajectory("flat", seed, data, data, (4., 4., 4., 4., 4.))
    recovers = ValidationTrajectory("recover", seed, data, data, (4., 3., 4.1, 3., 3.))
    crossover = stable_data_crossover(flat, recovers)
    assert crossover == 3
    # Three synthetic paired replication IDs, not trained models or paper results.
    references = {101: 1. + offset, 102: 10. + offset, 103: 100. + offset}
    alternatives = {key: .8 * value for key, value in references.items()}
    interval = paired_relative_gain_interval(references, alternatives, seed=seed)
    bootstrap_error = max(abs(interval[key] - .2) for key in ("relative_gain", "lower", "upper"))
    assert bootstrap_error < 1e-12
    pool = [1.] + [1 + rng.random() for _ in range(22)]
    regret = frozen_pool_regret(pool, seed=seed)
    budget_one_expected = statistics.mean(pool) - 1
    regret_error = abs(regret[0] - budget_one_expected)
    assert regret[-1] == 0 and all(a >= b for a, b in zip(regret, regret[1:])) and regret_error < .03
    invalid_rejected = 0
    for bad_x, bad_loss, horizon in [((0., 1.), (1., float("nan")), 1.),
                                   ((0., 1.), (2., 1.), 2.), ((0., 0.), (2., 1.), 1.)]:
        try:
            normalized_validation_auc(bad_x, bad_loss, horizon)
        except ValueError:
            invalid_rejected += 1
    try:
        paired_relative_gain_interval(references, {102: .8, 103: 8., 104: 80.}, seed=seed)
    except ValueError:
        invalid_rejected += 1
    assert invalid_rejected == 4
    return {"analytic_piecewise_auc_max_error": error, "synthetic_data_auc_gain": data_result["relative_auc_gain"],
            "synthetic_time_auc_gain": time_result["relative_auc_gain"], "common_time_horizon": time_result["common_horizon"],
            "data_time_ranking_reversal_preserved": True, "selection_uses_auc_not_final_loss": True,
            "stable_crossover_budget": crossover, "paired_bootstrap_analytic_ratio_max_error": bootstrap_error,
            "frozen_pool_candidates": len(pool), "permutations": 10000,
            "one_candidate_monte_carlo_expected_regret_error": regret_error,
            "full_budget_regret": regret[-1], "invalid_input_rejection_cases": invalid_rejected,
            "actual_model_training_runs": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--papers", default=",".join(SOURCES))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    papers = args.papers.split(",")
    try:
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not papers or set(papers) - set(SOURCES) or len(set(papers)) != len(papers):
        parser.error("select unique supported protocols")
    if not seeds or len(seeds) > 8 or len(set(seeds)) != len(seeds):
        parser.error("1..8 unique seeds required")
    if args.output.exists():
        parser.error("immutable output already exists")
    if args.code_commit and not re.fullmatch(r"[0-9a-fA-F]{40}", args.code_commit):
        parser.error("full hexadecimal code commit required")
    start = time.monotonic()
    operations = {"structural-signal-retriever": ssr_diagnostic, "muon-paired-budget": muon_diagnostic}
    components = {}
    for paper in papers:
        rows = [{"seed": seed, "metrics": operations[paper](seed)} for seed in seeds]
        metrics = {}
        for key in rows[0]["metrics"]:
            values = [row["metrics"][key] for row in rows]
            metrics[key] = all(values) if isinstance(values[0], bool) else {
                "mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0.,
                "n": len(values)}
        components[paper] = {
            "dataset": {"id": "synthetic-agent-cards-and-validation-trajectories",
                        "revision": "oct17-supplement-protocols-v1", "checkpoint": None,
                        "capability_benchmark": False},
            "per_seed": rows, "metrics": metrics, "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost"}
    sources = [Path(__file__).resolve()] + [ROOT / path for path in SOURCES.values()]
    commit = args.code_commit.lower() if args.code_commit else subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    payload = {"schema_version": 1, "code_commit": commit, "device": "cpu", "accelerator": "CPU",
               "seeds": seeds, "diagnostic_only": True, "promotion_eligible": False, "components": components,
               "elapsed_seconds": time.monotonic() - start,
               "executed_source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                          for path in sources}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "components": list(components),
                      "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
