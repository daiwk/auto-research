"""Four CPU-only equation diagnostics; synthetic fixtures, not capability scores."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

from auto_research.reproductions.attribution_sets_components import binomial_tail, unbiased_cell
from auto_research.reproductions.spatial_ads_components import Disk, feasible_ii, round_solution, solve_relaxation
from auto_research.foundation_models.google16_mild import fit_router, margin_schedule, route
from auto_research.foundation_models.google16_proeval import EmpiricalGP

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ["scripts/run_google16_statistics.py", "src/auto_research/reproductions/attribution_sets_components.py",
    "src/auto_research/reproductions/spatial_ads_components.py",
    "src/auto_research/foundation_models/google16_mild.py", "src/auto_research/foundation_models/google16_proeval.py"]


def diagnose(seed=42):
    b = binomial_tail(10, .3, 4)
    printed = unbiased_cell(.6, n=10, p=.3, j=2, prior=[.6, .4], position=1,
                           mean_f1=.04, mean_f2=.6)
    attribution = {"printed_formula_expectation_constant_h": printed*b,
        "known_population_risk_constant_h": .22,
        "finite_n_absolute_discrepancy": abs(printed*b-.22),
        "unbiasedness_confirmed": False}
    d = [[0, .4, 1], [.4, 0, .6], [1, .6, 0]]
    disks = [Disk(0, .5, 2, 0), Disk(1, .5, 1, 1), Disk(2, .7, 3, 2)]
    x, upper = solve_relaxation(d, disks)
    selections = [round_solution(d, disks, x, seed=seed+i) for i in range(256)]
    spatial = {"lp_upper_bound": upper, "rounding_trials": len(selections),
        "infeasible_selections": sum(not feasible_ii(d, disks, s) for s in selections),
        "mean_selected_disk_weight": float(np.mean([sum(disks[i].weight for i in s) for s in selections])),
        "ad_matching_or_payments_validated": False}
    historical = np.array([[.1, .2, .8, .4], [.3, .3, .2, .8], [.6, .1, .7, .1], [.8, .7, .3, .4]])
    gp = EmpiricalGP(historical, historical_ids=['a', 'b', 'c', 'd'], target_id='target')
    initial = gp.quadrature()
    # The separate fixture oracle supplies ONLY the newly queried value.
    fixture_oracle = [.4, .2, .9, .1]
    queries = []
    for _ in range(2):
        index = gp.select()
        queries.append(index)
        gp.observe(index, fixture_oracle[index])
    proeval = {"initial_bq_variance": initial['variance'], "final_bq_variance": gp.quadrature()['variance'],
        "queried_examples": len(queries), "unique_queries": len(set(queries)),
        "prior_models": 4, "real_model_evaluation": False}
    features = np.array([[1, -1], [1, -.5], [1, .5], [1, 1.]])
    costs = [[0, 1], [0, 1], [1, 0], [1, 0]]
    margins = margin_schedule([2, 2])
    weights, losses = fit_router(features, costs, margins, steps=100)
    mild = {"training_initial_surrogate": losses[0], "training_final_surrogate": losses[-1],
            "inference_examples": len(route(features, weights)), "real_experts_evaluated": False,
            "inference_reads_labels_or_costs": False}
    return {"attribution-sets": attribution, "spatial-ads": spatial, "proeval": proeval, "mild": mild}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("immutable evidence already exists")
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    payload = {"schema_version": 2, "seed": args.seed, "device": "cpu", "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism", "promotion_eligible": False, "evolve_integrated": False,
        "created_at_utc": datetime.now(timezone.utc).isoformat(), "code_commit": commit,
        "source_sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in SOURCES},
        "dataset": {"id": "repository-authored-equation-fixtures", "public_benchmark": False},
        "components": diagnose(args.seed), "full_experiments_reproduced": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(payload['components'], allow_nan=False))


if __name__ == '__main__':
    main()
