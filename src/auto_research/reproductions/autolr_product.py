"""Checkpoint-proposed, verified, resumable AutoLR product experiments.

The executable search space is deliberately bounded to two-tower dimensions,
learning rate and a category adapter. It does not execute model-written code,
claim autonomous novel architectures, or authorize an online launch.
"""
import argparse
import hashlib
import json
from pathlib import Path
from statistics import mean

import numpy as np
import torch

from .industrial_2026 import evaluate
from .product_data import load_product_data
from .sep7_models import EvidenceController, train_two_tower


EVIDENCE = {"url": "https://arxiv.org/abs/2609.05063",
            "mechanism": "shared two-tower content encoder; optional category-conditioned query adapter and reconstruction loss",
            "scope": "local next-product transfer experiment; not labelled complementarity"}


def parse_parameters(value):
    if not isinstance(value, dict) or set(value) != {"dimensions", "learning_rate", "adapter"}:
        raise ValueError("proposal must specify exactly the three executable parameters")
    if value["dimensions"] not in (16, 32, 64) or type(value["adapter"]) is not bool:
        raise ValueError("unsupported dimensions/adapter")
    if not isinstance(value["learning_rate"], (float, int)) or not 1e-5 <= value["learning_rate"] <= .01:
        raise ValueError("learning rate outside verified search bounds")
    return value


def response_json(generate, prompt):
    text = generate(prompt)
    if text.strip().startswith("```json") and text.strip().endswith("```"):
        text = text.strip()[7:-3]
    return json.loads(text)


def research(data, dataset_evidence, generate, directory, rounds=3, steps=100, seeds=(42, 43, 44)):
    directory.mkdir(parents=True, exist_ok=True)
    contract = {"dataset": dataset_evidence, "steps": steps, "rounds": rounds, "seeds": list(seeds),
                "parameters": {"dimensions": [16, 32, 64], "learning_rate": [1e-5, .01], "adapter": [False, True]}}
    contract_path = directory / "contract.json"
    if contract_path.exists() and json.loads(contract_path.read_text()) != contract:
        raise ValueError("resume contract changed")
    contract_path.write_text(json.dumps(contract, indent=2) + "\n")

    def execute_parameters(parameters, split="validation", budget=steps):
        rows = []
        for seed in seeds:
            table, training = train_two_tower(data, seed, steps=budget, **parameters)
            if not np.isfinite(table).all() or not np.isfinite(training["last_loss"]):
                raise ValueError("nonfinite actual training output")
            rows.append(evaluate(data, lambda history: table[history[-1]], target_split=split))
        return {key: mean(row[key] for row in rows) for key in rows[0]}

    baseline = {"dimensions": 32, "learning_rate": .003, "adapter": False}
    baseline_path = directory / "baseline-validation.json"
    if baseline_path.exists():
        reference = json.loads(baseline_path.read_text())
    else:
        reference = execute_parameters(baseline)
        baseline_path.write_text(json.dumps(reference, indent=2) + "\n")
    controller = EvidenceController(reference, directory / "ledger.json")

    def propose(context):
        proposals = response_json(generate,
            'Propose two runnable next-product experiments from the research evidence and observed validation ledger. '
            'Return only JSON {"proposals":[{"dimensions":16|32|64,"learning_rate":number,"adapter":boolean}, ...]}. '
            'Learning rate must lie in [0.00001,0.01]. Do not repeat prior parameter combinations. '
            'No test observations are available.\n' + json.dumps({"evidence": EVIDENCE, "validation_context": context}))
        rows = []
        for value in proposals["proposals"]:
            parameters = parse_parameters(value)
            digest = hashlib.sha256(json.dumps(parameters, sort_keys=True).encode()).hexdigest()[:16]
            rows.append({"key": digest, "parameters": parameters, "evidence": EVIDENCE,
                         "selection_split": "validation"})
        return rows

    def reviewer(role):
        def review(candidate, context):
            result = response_json(generate,
                f'Act as an independent {role} reviewer. Inspect only this proposal, evidence and validation ledger. '
                'Return only JSON {"feasible":boolean,"score":number,"reason":"brief justification"}. '
                'Score from 0 to 1. Do not predict measured results as facts.\n'
                + json.dumps({"proposal": candidate, "context": context}))
            if type(result.get("feasible")) is not bool or not 0 <= float(result["score"]) <= 1:
                raise ValueError("invalid council response")
            return result
        return review

    def verify(candidate):
        parameters = parse_parameters(candidate["parameters"])
        # Real optimizer/backprop and held-out metric computation, not a
        # counter or a reviewer asserting that code would run.
        metrics = execute_parameters(parameters, budget=1)
        return {"passed": True, "checks": ["one-step-backprop", "finite-scores", "validation-evaluation"],
                "metrics": metrics}

    # Restore from disk between rounds, exercising the same resume path users
    # use after interruption. All proposals see the accumulated actual ledger.
    for _ in range(max(0, rounds - len(controller.records))):
        before = len(controller.records)
        controller.research(propose, [reviewer("method fidelity"), reviewer("budget and evaluation")],
                            verify, lambda candidate: execute_parameters(candidate["parameters"]),
                            {"hit_at_10": reference["hit_at_10"] * .9}, rounds=1)
        controller = EvidenceController(reference, directory / "ledger.json")
        if len(controller.records) == before:
            break
    selected = next((row["proposal"]["parameters"] for row in controller.records
                     if row["candidate"] == controller.incumbent), baseline)
    # No test metrics enter the proposal or controller ledger. A final receipt
    # is idempotent across resume; a changed selection requires a new receipt.
    final_path = directory / "final-test.json"
    if final_path.exists():
        final = json.loads(final_path.read_text())
        if final["incumbent"] != controller.incumbent:
            raise ValueError("selection changed after final test; start a separate experiment")
    else:
        final = {"incumbent": controller.incumbent, "parameters": selected,
                 "test": execute_parameters(selected, split="test")}
        final_path.write_text(json.dumps(final, indent=2) + "\n")
    return {"reference_validation": reference, "records": controller.records, "final": final,
            "scope": "real checkpoint proposals and separate council calls; bounded operator space, offline only"}


if __name__ == "__main__":
    from ..agent_research.atomrec_checkpoint import FrozenMemoryCheckpoint

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()
    torch.set_num_threads(4)
    data, evidence = load_product_data(args.dataset_dir)
    checkpoint = FrozenMemoryCheckpoint()
    result = research(data, evidence, checkpoint.generate, args.output_dir, args.rounds, args.steps)
    (args.output_dir / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
