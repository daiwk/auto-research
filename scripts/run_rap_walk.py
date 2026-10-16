#!/usr/bin/env python3
"""Run RAP-Walk on supplied comparison graphs, or explicit mechanism fixtures."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def run(*, input_path=None, device="cpu", seeds=(42, 43, 44)):
    import torch
    from auto_research.post_training.rap_walk import rap_walk_advantages, rap_walk_grpo_loss

    records = json.loads(input_path.read_text()) if input_path else [
        {"id": "transitive-mechanism-fixture", "pairwise": [[.5, .8, .9], [.2, .5, .8], [.1, .2, .5]]},
        {"id": "cyclic-mechanism-fixture", "pairwise": [[.5, .9, .2, .7], [.1, .5, .8, .7],
                                                                 [.8, .2, .5, .6], [.3, .3, .4, .5]]},
    ]
    if not isinstance(records, list) or not records or len(records) > 64:
        raise ValueError("provide 1..64 observed comparison graph records")
    results = []
    for seed in seeds:
        torch.manual_seed(seed)
        graphs = []
        for record in records:
            graph = torch.tensor(record["pairwise"], dtype=torch.float64, device=device)
            if len(graph) > 32:
                raise ValueError("bounded mechanism runner supports at most 32 rollouts per graph")
            advantage, audit = rap_walk_advantages(graph)
            # An actual differentiable categorical policy validates the GRPO
            # interface, not video generation or an invented judge capability.
            logits = torch.nn.Parameter(torch.randn(len(graph), 4, device=device))
            actions = torch.zeros(len(graph), 2, dtype=torch.long, device=device)
            old = logits.detach().log_softmax(-1).gather(-1, actions)
            optimizer = torch.optim.SGD([logits], lr=.01)
            before = logits.detach().clone()
            current = logits.log_softmax(-1).gather(-1, actions)
            mask = torch.ones_like(current, dtype=torch.bool)
            loss, _ = rap_walk_grpo_loss(current, old, mask, graph)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            graphs.append({"id": record["id"], "advantages": advantage.tolist(),
                           "stationary_residual": audit["stationary_residual"],
                           "normalized_entropy": audit["normalized_entropy"],
                           "mixing_coefficient": audit["mixing_coefficient"],
                           "parameter_delta_l2": float((logits.detach() - before).norm()),
                           "loss": float(loss.detach())})
        results.append({"seed": seed, "graphs": graphs})
    return {"method": "rap-walk", "paper": "2610.20089v1", "seeds": list(seeds),
            "diagnostic_only": True, "promotion_eligible": False, "evaluation_tier": "L1",
            "input_kind": "observed_comparison_graphs" if input_path else "explicit_mechanism_fixtures",
            "scope": "preference aggregation and GRPO loss interface, no video experiment",
            "full_reproduction": "not_reproduced_high_cost", "results": results,
            "accelerator": torch.cuda.get_device_name() if device.startswith("cuda") else device}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-path", type=Path)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("choose a fresh output; do not overwrite evidence")
    seeds = tuple(int(seed) for seed in args.seeds.split(","))
    if not seeds or len(seeds) != len(set(seeds)):
        parser.error("unique nonempty seeds required")
    result = run(input_path=args.input_path, device=args.device, seeds=seeds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"method": result["method"], "input_kind": result["input_kind"],
                      "seeds": result["seeds"]}))


if __name__ == "__main__":
    main()
