"""Fixed-K versus Elastic Expert Routing, causal scratch LM on public text."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch
from torch.nn import functional as F

from auto_research.foundation_models.elastic_expert_routing import ElasticMoELanguageModel


def run(text, seed, device, steps=100, context=64, batch=8):
    alphabet = sorted(set(text))
    encoding = {char: i for i, char in enumerate(alphabet)}
    ids = torch.tensor([encoding[c] for c in text], device=device)
    cut1, cut2 = int(len(ids) * .9), int(len(ids) * .95)
    splits = ids[:cut1], ids[cut1:cut2], ids[cut2:]
    if any(len(split) < context + 1 for split in splits):
        raise ValueError("public corpus too short for isolated train/validation/test")
    generator = torch.Generator().manual_seed(seed)
    starts = torch.randint(0, len(splits[0]) - context - 1, (steps, batch), generator=generator)
    results = {}
    for radius in (0, 1):
        torch.manual_seed(seed)
        model = ElasticMoELanguageModel(len(alphabet), radius=radius, context=context).to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
        initial = next(model.parameters()).detach().clone()
        budgets = []
        model.train()
        for offsets in starts:
            x = torch.stack([splits[0][i:i + context] for i in offsets])
            y = torch.stack([splits[0][i + 1:i + context + 1] for i in offsets])
            logits, aux, mean_budget = model(x)
            loss = F.cross_entropy(logits.flatten(0, 1), y.flatten()) + .01 * aux
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
            optimizer.step()
            budgets.append(float(mean_budget.detach()))
        model.eval()
        metrics = {}
        with torch.no_grad():
            for name, split in zip(("validation", "test"), splits[1:], strict=True):
                losses = []
                for start in range(0, min(len(split) - context, context * 16), context):
                    logits, _, realized = model(split[start:start + context][None])
                    assert float(realized) == 3.
                    losses.append(float(F.cross_entropy(logits[0], split[start + 1:start + context + 1])))
                metrics[f"{name}_character_nll"] = sum(losses) / len(losses)
                metrics[f"{name}_character_perplexity"] = math.exp(sum(losses) / len(losses))
        metrics["training_realized_experts_mean"] = sum(budgets) / len(budgets)
        metrics["parameter_delta_norm"] = float((next(model.parameters()).detach() - initial).norm())
        results["fixed_k" if radius == 0 else "elastic_k"] = metrics
    return {"seed": seed, "steps": steps, "context": context, "batch": batch,
            "split": "chronological 90/5/5, vocabulary shared but targets isolated",
            "fidelity": "core_mechanism", "evaluation_tier": "L2",
            "diagnostic_only": True, "results": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-file", type=Path, required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--dataset-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("positive training steps required")
    report = run(args.text_file.read_text(), args.seed, args.device, args.steps)
    report["dataset"] = {"id": args.dataset_id, "revision": args.dataset_revision}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
