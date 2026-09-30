#!/usr/bin/env python3
"""Generate deterministic L1 receipts for the Sep-29 follow-up batch."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.latest_20260930_followup import gaussian_evsi, set_level_uplift, user_fidelity_score
from auto_research.foundation_latest_20260930_followup import lift_loss, lift_topk_state, triadic_linear_attention
from auto_research.post_training.latest_20260930_followup import graft_peer_objective, oasis_forward_kl, oasis_select_scaffold, pr_opd_alignment, ride_loss
from auto_research.reproductions.grp.experiment import reproduce as reproduce_grp

SEEDS = (42, 43, 44)
PATHS = {
    "grp": "reproductions/2609.36688-grp",
    "lift-feedback": "foundation-models/2609.38149-lift-feedback",
    "triadic-linear-attention": "foundation-models/2609.36529-triadic-linear-attention",
    "oasis-opsd": "post-training/2609.37915-oasis",
    "graft": "post-training/2609.37868-graft",
    "ride-opd": "post-training/2609.36484-ride",
    "pr-opd": "post-training/2609.36642-pr-opd",
    "user-proxy-bench": "agent-research/2609.38043-userproxybench",
    "upliftmem": "agent-research/2609.36805-upliftmem",
}


def run():
    import torch

    results = {key: [] for key in PATHS}
    for seed in SEEDS:
        torch.manual_seed(seed)
        np.random.seed(seed)
        results["grp"].append({"seed": seed, **reproduce_grp(None, seed)["metrics"]})

        student = torch.randn(2, 4, 13, requires_grad=True)
        teacher = torch.randn(2, 4, 13, requires_grad=True)
        state = lift_topk_state(teacher, k=4)
        loss, audit = lift_loss(student, teacher, torch.randint(0, 13, (2, 4)), k=4)
        loss.backward()
        results["lift-feedback"].append({"seed": seed, "loss": float(loss.detach()), "state_nonzero": int((state > 0).sum()), **audit, "teacher_detached": teacher.grad is None})

        q, k = torch.randn(1, 6, 3), torch.randn(1, 6, 3)
        q2, k2 = torch.randn(1, 6, 2), torch.randn(1, 6, 2)
        value = torch.randn(1, 6, 4)
        output, state3 = triadic_linear_attention(q, q2, k, k2, value)
        results["triadic-linear-attention"].append({"seed": seed, "output_norm": float(output.norm()), "state_entries": state3.numel(), "finite": bool(torch.isfinite(output).all())})

        rollouts = [{"id": "ok", "tokens": [1, 2], "verified": True}, {"id": "bad", "tokens": [3], "verified": False}]
        scaffold, context = oasis_select_scaffold(rollouts)
        logp = torch.log_softmax(torch.randn(1, 2, 7), -1)
        prob = torch.softmax(torch.randn(1, 2, 7), -1)
        oasis = oasis_forward_kl(logp, prob, torch.ones(1, 2))
        results["oasis-opsd"].append({"seed": seed, "loss": float(oasis), "verified_scaffold": scaffold["verified"], "distinct_context": scaffold["id"] != context["id"]})

        current = torch.tensor([[-0.2, -0.4], [-1.5, -1.7]], requires_grad=True)
        graft, graft_audit = graft_peer_objective(current, current.detach() - .05, torch.tensor([1., -1.]), torch.tensor([-.2, -2.]), torch.ones_like(current))
        graft.backward()
        results["graft"].append({"seed": seed, "loss": float(graft.detach()), **graft_audit, "finite_gradient": bool(torch.isfinite(current.grad).all())})

        base, teacher_hidden = torch.zeros(1, 3, 4), torch.ones(1, 3, 4)
        learner = torch.zeros(1, 3, 4, requires_grad=True)
        ride = ride_loss(learner, base, teacher_hidden, extrapolation=1.5, token_mask=torch.tensor([[1, 1, 0]]))
        ride.backward()
        results["ride-opd"].append({"seed": seed, "loss": float(ride.detach()), "masked_gradient_zero": bool(learner.grad[:, 2].abs().sum() == 0), "target_multiplier": 1.5})

        privileged = [torch.randn(1, 3, 4) for _ in range(2)]
        learners = [(item + .1 * torch.randn_like(item)).requires_grad_() for item in privileged]
        alignment = pr_opd_alignment(learners, privileged, torch.tensor([[1, 1, 0]]))
        alignment.backward()
        results["pr-opd"].append({"seed": seed, "alignment_loss": float(alignment.detach()), "layers": 2, "privileged_detached": all(item.grad is None for item in privileged)})

        rubric = np.asarray([[1, 1, 1], [1, seed % 2, 1]], dtype=float)
        fidelity = user_fidelity_score(rubric)
        results["user-proxy-bench"].append({"seed": seed, "user_fidelity_score": fidelity["user_fidelity_score"], "episodes": 2, "agent_reward_used": False})

        uplift, uplift_audit = set_level_uplift([1, 0, 1], [0, 1, 1])
        selected, scores = gaussian_evsi([.2, .1], [[.1, 0], [0, 1]], [0, 1])
        results["upliftmem"].append({"seed": seed, **uplift_audit, "selected_probe": selected, "maximum_evsi": float(scores.max()), "paired_outcomes": len(uplift)})
    return results


def _numeric_summary(rows):
    summary = {}
    for key in rows[0]:
        values = [row[key] for row in rows]
        if key != "seed" and all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            summary[key] = {"mean": float(np.mean(values)), "std": float(np.std(values))}
    return summary


def main():
    for method, rows in run().items():
        destination = ROOT / "docs" / PATHS[method] / "metrics" / "mechanism-seeds42-44.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 2, "manifest_ref": f"{PATHS[method].split('/')[0]}:{method}",
            "method": method, "dataset": "deterministic public mechanism mini-suite", "seeds": list(SEEDS),
            "diagnostic_only": True,
            "metrics": _numeric_summary(rows), "seed_results": rows,
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": list(SEEDS), "formal_comparison": False, "diagnostic_only": True, "claim_policy": "executable mechanism and invariant checks only"},
            "provenance": {"artifact_path": str(destination.relative_to(ROOT)), "dataset_fingerprint": "deterministic public mechanism suite sep30-followup-v1", "original_code_commit": "working tree"},
        }
        destination.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(destination.relative_to(ROOT))


if __name__ == "__main__":
    main()
