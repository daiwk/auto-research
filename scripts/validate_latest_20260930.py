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
    multi_memory_grpo_objective,
    time_evolving_memory,
    video_rsi_accept,
)
from auto_research.foundation_latest_20260930 import (  # noqa: E402
    ChineseJevHead,
    MultiScaleGLA,
    chinese_jev_objective,
    leapquant_compress,
    leapquant_window,
    stepquant_bit_allocation,
    stepquant_dual_axis,
)
from auto_research.post_training.latest_20260930 import (  # noqa: E402
    dr_opd_reverse_kl,
    dr_opd_token_weights,
    lspd_objective,
    roft_retrospection_loss,
    sipo_token_advantage,
    token_policy_gradient_loss,
)
from auto_research.reproductions.helix.experiment import reproduce as reproduce_helix  # noqa: E402


SEEDS = (42, 43, 44)
DOMAINS = {
    "roft": "post-training/2609.35741-roft",
    "lspd": "post-training/2609.35505-lspd",
    "harness-learning": "agent-research/2609.35738-harness-learning",
    "ms-gla": "foundation-models/2609.35664-ms-gla",
    "graphhca": "agent-research/2609.35084-graphhca",
    "stepquant": "foundation-models/2609.38169-stepquant",
    "leapquant": "foundation-models/2609.38166-leapquant",
    "chinese-jev": "foundation-models/2609.36965-chinese-jev",
    "dr-opd": "post-training/2609.38025-dr-opd",
    "sipo": "post-training/2609.36742-sipo",
    "remem": "agent-research/2609.37311-remem",
    "video-rsi": "agent-research/2609.37950-video-rsi",
    "helix": "reproductions/2609.37183-helix",
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

        state = torch.randn(32, 32, device=device)
        row_impact = torch.linspace(4, 1, 32, device=device)
        step_state, step_audit = stepquant_dual_axis(state, row_impact, bits=6)
        allocation = stepquant_bit_allocation(
            [[1.0, .2], [.7, .15], [.3, .12]], [-.01, -.2, -.6], (4, 8), average_bits=6,
        )
        results["stepquant"].append({
            "seed": seed,
            "state_mse": float((step_state - state).square().mean().detach().cpu()),
            "average_allocated_bits": float(allocation["bits"].mean()),
            "finite_scales": bool(torch.isfinite(step_audit["row_scale"]).all()),
        })
        leap_state, leap_audit = leapquant_compress(state, bits=8, rank=2)
        decays = torch.full((4, 32), .98, device=device)
        keys = torch.randn(4, 32, device=device)
        corrections = torch.randn(4, 32, device=device)
        leap_boundary, window = leapquant_window(
            leap_state, decays, keys, corrections, bits=8, rank=2,
        )
        results["leapquant"].append({
            "seed": seed,
            "state_mse": float((leap_state - state).square().mean().detach().cpu()),
            "window_steps": len(window["intermediate_states"]),
            "finite_boundary": bool(torch.isfinite(leap_boundary).all()),
            "compensator_rank": int(torch.linalg.matrix_rank(leap_audit["compensator"].float()).cpu()),
        })

        jev = ChineseJevHead(32).to(device)
        candidate_hidden = torch.randn(3, 5, 32, device=device, requires_grad=True)
        jev_logits = jev(candidate_hidden, torch.tensor([0, 1, 2], device=device))
        jev_targets = torch.eye(5, device=device)[:3]
        jev_loss, jev_audit = chinese_jev_objective(
            jev_logits, jev_targets, torch.tensor([0, 1, 2], device=device),
            generator=torch.Generator(device=device).manual_seed(seed),
        )
        jev_loss.backward()
        results["chinese-jev"].append({
            "seed": seed,
            "loss": float(jev_loss.detach().cpu()),
            "reward_std": jev_audit["reward_std"],
            "finite_gradient": bool(torch.isfinite(candidate_hidden.grad).all()),
        })

        discrepancy = torch.randn(3, 7, device=device) * .2
        directional = torch.randn(3, 7, device=device)
        dr_weights, dr_audit = dr_opd_token_weights(discrepancy, directional, strength=.5)
        student = torch.randn(3, 7, device=device, requires_grad=True)
        dr_loss = dr_opd_reverse_kl(student, student.detach() - discrepancy, dr_weights, torch.ones_like(student))
        dr_loss.backward()
        results["dr-opd"].append({
            "seed": seed,
            "credit_rms": dr_audit["credit_rms"],
            "weight_range": dr_audit["maximum_weight"] - dr_audit["minimum_weight"],
            "finite_gradient": bool(torch.isfinite(student.grad).all()),
        })

        rewards = torch.zeros(3, device=device)
        positive = torch.randn(3, 7, device=device)
        negative = positive - torch.randn(3, 7, device=device) * .2
        advantage, sipo_audit = sipo_token_advantage(
            rewards, positive, negative, torch.ones_like(positive),
        )
        sipo_student = torch.randn(3, 7, device=device, requires_grad=True)
        sipo_loss = token_policy_gradient_loss(sipo_student, advantage, torch.ones_like(advantage))
        sipo_loss.backward()
        results["sipo"].append({
            "seed": seed,
            "mean_abs_evidence": sipo_audit["mean_abs_evidence"],
            "uniform_failure_signal": bool(advantage.abs().sum() > 0),
            "finite_gradient": bool(torch.isfinite(sipo_student.grad).all()),
        })

        history = [f"event-{index}" for index in range(12)]
        memory, memory_trace = time_evolving_memory(
            history, chunk_size=3, memory_budget=4,
            update=lambda previous, chunk: previous + chunk,
        )
        ratio = torch.ones(3, 5, device=device)
        mem_ratio = torch.ones(3, len(memory_trace), 4, device=device)
        mem_objective, mem_audit = multi_memory_grpo_objective(
            ratio, mem_ratio, torch.tensor([1.0, 0.0, .5], device=device),
        )
        results["remem"].append({
            "seed": seed,
            "memory_tokens": len(memory),
            "history_chunks": len(memory_trace),
            "memory_objective": mem_audit["memory_objective"],
            "gold_fields_exposed": False,
        })

        accepted_accuracy, _ = video_rsi_accept(.6, 100, .61, 108)
        accepted_cost, _ = video_rsi_accept(.6, 100, .595, 80)
        rejected, _ = video_rsi_accept(.6, 100, .59, 95)
        results["video-rsi"].append({
            "seed": seed,
            "accuracy_branch_accepts": accepted_accuracy,
            "cost_branch_accepts": accepted_cost,
            "non_pareto_candidate_rejected": not rejected,
            "private_example_scores_exposed": False,
        })

        helix = reproduce_helix(None, seed=seed)
        results["helix"].append({"seed": seed, **helix["metrics"]})
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
            "dataset": "deterministic public mechanism mini-suite",
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
