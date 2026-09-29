#!/usr/bin/env python3
"""Run the auditable 2026-09-30 mechanism suite on CPU or CUDA.

CUDA mode can optionally use a locally cached public causal-LM checkpoint for
ROFT/LSPD, while MS-GLA always executes its own architecture layer.  The two
Agent kernels intentionally consume only execution reports or sampled rollout
graphs: there is no gold-answer or gold-plan input.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.latest_20260930 import (  # noqa: E402
    HarnessProposer,
    Transition,
    adapt_harness,
    graphhca_credit,
)
from auto_research.foundation_latest_20260930 import MultiScaleGLA  # noqa: E402
from auto_research.post_training.latest_20260930 import (  # noqa: E402
    lspd_objective,
    roft_retrospection_loss,
)


SEEDS = (42, 43, 44)
DOMAINS = {
    "roft": "post-training/2609.35741-roft",
    "lspd": "post-training/2609.35505-lspd",
    "harness-learning": "agent-research/2609.35738-harness-learning",
    "ms-gla": "foundation-models/2609.35664-ms-gla",
    "graphhca": "agent-research/2609.35084-graphhca",
}


def _language_model_logits(model_id: str, revision: str, device: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    load_target = model_id
    cached_snapshot = (
        Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface"))
        / "hub"
        / f"models--{model_id.replace('/', '--')}"
        / "snapshots"
        / revision
    )
    if cached_snapshot.is_dir():
        # Passing the concrete cached snapshot avoids transformers metadata
        # requests while the public id/revision remain the command contract.
        load_target = str(cached_snapshot)
    tokenizer = AutoTokenizer.from_pretrained(load_target, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        load_target,
        local_files_only=True,
        torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
    ).to(device)
    model.train()
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    model.get_output_embeddings().weight.requires_grad_(True)
    batch = tokenizer(
        ["Question: 2+3? Action: calculate. Feedback: 5. Retrospection: verify arithmetic."],
        return_tensors="pt",
    ).to(device)
    return model, model(**batch).logits[:, :-1], batch.input_ids[:, 1:]


def run(device: str, model_id: str | None, revision: str | None):
    import torch

    results = {key: [] for key in DOMAINS}
    for seed in SEEDS:
        torch.manual_seed(seed)
        np.random.seed(seed)
        if model_id:
            model, logits, targets = _language_model_logits(model_id, revision or "main", device)
        else:
            model = None
            logits = torch.randn(1, 12, 97, device=device, requires_grad=True)
            targets = torch.randint(0, 97, (1, 12), device=device)

        target_mask = torch.zeros_like(targets)
        target_mask[:, -max(2, targets.shape[1] // 4):] = 1
        roft_loss = roft_retrospection_loss(logits, targets, target_mask)
        roft_loss.backward(retain_graph=True)
        results["roft"].append({
            "seed": seed,
            "masked_ce": float(roft_loss.detach().float().cpu()),
            "retrospection_tokens": int(target_mask.sum()),
            "context_target_tokens": 0,
        })

        student_log_prob = torch.log_softmax(logits.float(), dim=-1).gather(
            -1, targets.unsqueeze(-1)
        ).squeeze(-1)
        teacher_log_prob = (student_log_prob.detach() - 0.15).clone()
        entropy = -(torch.softmax(logits.float(), -1) * torch.log_softmax(logits.float(), -1)).sum(-1)
        response_mask = torch.ones_like(student_log_prob)
        lspd_loss, diagnostics = lspd_objective(
            student_log_prob, teacher_log_prob, entropy, response_mask
        )
        lspd_loss.backward()
        results["lspd"].append({"seed": seed, "loss": float(lspd_loss.detach().cpu()), **diagnostics})
        del model, logits, targets
        if device == "cuda":
            torch.cuda.empty_cache()

        layer = MultiScaleGLA(32, scales=(1, 2, 4)).to(device)
        hidden = torch.randn(2, 31, 32, device=device, requires_grad=True)
        output, audit = layer(hidden)
        architecture_loss = output.square().mean()
        architecture_loss.backward()
        routing = audit["routing_weights"].detach().float().cpu()
        results["ms-gla"].append({
            "seed": seed,
            "loss": float(architecture_loss.detach().cpu()),
            "routing_sum_error": float((routing.sum(-1) - 1).abs().max()),
            "finite_gradient": bool(torch.isfinite(hidden.grad).all()),
        })

        rollouts = [
            ([Transition("s0", "short", "goal")], True),
            ([Transition("s0", "detour", "s1"), Transition("s1", "finish", "goal")], True),
            ([Transition("s0", "bad", "fail")], False),
        ]
        graph = graphhca_credit(rollouts, discount=0.9)
        results["graphhca"].append({
            "seed": seed,
            "start_value": graph["values"]["s0"],
            "iterations": graph["iterations"],
            "successful_credit_above_failure": bool(graph["step_advantages"][0] > graph["step_advantages"][2]),
            "gold_fields_exposed": False,
        })

        proposer = HarnessProposer()
        for _ in range(8):
            proposer.train_step([0.1, 0.2, 0.9, 0.3], learning_rate=0.2)

        def execute(harness):
            missing = "retrieve" not in harness
            return {"score": len(harness) / 4, "failure": "missing_evidence" if missing else ""}

        harness, trace = adapt_harness(proposer, ("retry",), execute, rounds=3)
        results["harness-learning"].append({
            "seed": seed,
            "rounds": len(trace),
            "final_harness_size": len(harness),
            "uses_execution_reports": True,
            "gold_fields_exposed": False,
        })
    return results


def write_metrics(results, output_root: Path):
    aggregate = {}
    for method, seed_results in results.items():
        numeric = {}
        for row in seed_results:
            for key, value in row.items():
                if key != "seed" and isinstance(value, (int, float)) and not isinstance(value, bool):
                    numeric.setdefault(key, []).append(float(value))
        metrics = {
            key: {"mean": float(np.mean(values)), "std": float(np.std(values))}
            for key, values in numeric.items()
        }
        target = output_root / DOMAINS[method] / "metrics" / "mechanism-seeds42-44.json"
        payload = {
            "schema_version": 2,
            "manifest_ref": f"{DOMAINS[method].split('/')[0]}:{method}",
            "method": method,
            "seeds": list(SEEDS),
            "metrics": metrics,
            "seed_results": seed_results,
            "evaluation_protocol": {
                "tier": "l1_mechanism",
                "seeds": list(SEEDS),
                "formal_comparison": False,
                "diagnostic_only": True,
                "claim_policy": "executable mechanism and invariant checks only",
            },
            "provenance": {
                "artifact_path": str(target.relative_to(output_root.parent)),
                "dataset_fingerprint": "deterministic public mechanism suite sep30-v1",
                "original_code_commit": "working tree",
            },
        }
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        aggregate[method] = payload
    aggregate.update({
        "schema_version": 2,
        "manifest_ref": "experiments:sep30-p0-p1-mechanisms-seeds42-44",
        "evaluation_protocol": {
            "tier": "l1_mechanism",
            "seeds": list(SEEDS),
            "formal_comparison": False,
            "diagnostic_only": True,
            "claim_policy": "cross-paper mechanism summary; not a capability comparison",
        },
        "provenance": {
            "artifact_path": "docs/experiments/sep30-p0-p1-mechanisms-seeds42-44.json",
            "dataset_fingerprint": "deterministic public mechanism suite sep30-v1",
            "original_code_commit": "working tree",
        },
    })
    experiment = output_root / "experiments" / "sep30-p0-p1-mechanisms-seeds42-44.json"
    experiment.parent.mkdir(parents=True, exist_ok=True)
    experiment.write_text(json.dumps(aggregate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--model-id")
    parser.add_argument("--revision")
    parser.add_argument("--output-root", type=Path, default=ROOT / "docs")
    args = parser.parse_args()
    results = run(args.device, args.model_id, args.revision)
    write_metrics(results, args.output_root)
    print(json.dumps(results, ensure_ascii=False))


if __name__ == "__main__":
    main()
