#!/usr/bin/env python3
"""Four bounded numerical/gradient diagnostics, not paper capability results.

No downloads, API calls, gold benchmarks or pretrained checkpoints. Fixed tiny
fixtures test the defining operators; all real updates stay within seconds.
"""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

import torch
from torch import nn

from auto_research.post_training import clean_rm, elite_replay, progress_reward
from auto_research.post_training import shared_residual_distillation as srd

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("shared-residual-distillation", "progress-reward", "elite-replay", "clean-rm")
SOURCES = ("src/auto_research/post_training/shared_residual_distillation.py",
    "src/auto_research/post_training/progress_reward.py", "src/auto_research/post_training/elite_replay.py",
    "src/auto_research/post_training/clean_rm.py", "scripts/run_oct17_post_components.py")


def delta(model, initial):
    return sum(float((p.detach() - q).square().sum()) for p, q in zip(model.parameters(), initial, strict=True)) ** .5


def snapshot(model):
    return [p.detach().clone() for p in model.parameters()]


def update(model, optimizer, loss):
    if not torch.isfinite(loss):
        raise RuntimeError("nonfinite diagnostic objective")
    optimizer.zero_grad()
    loss.backward()
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 10., error_if_nonfinite=True)
    optimizer.step()
    return float(norm)


class TinyPrefixPolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(8, 12)
        self.head = nn.Linear(12, 8)

    def forward(self, tokens):
        hidden = self.embedding(tokens)
        lengths = torch.arange(1, tokens.shape[1] + 1, device=tokens.device, dtype=hidden.dtype)
        return self.head(hidden.cumsum(1) / lengths[None, :, None])


@torch.no_grad()
def rollout(model, prompt, length=4):
    sequence = prompt.clone()
    for _ in range(length):
        sampled = torch.multinomial(model(sequence[None])[:, -1].softmax(-1), 1)[0]
        sequence = torch.cat((sequence, sampled))
    return sequence[len(prompt):]


def run_srd(device, steps):
    learner = TinyPrefixPolicy().to(device=device, dtype=torch.float64)
    initial = snapshot(learner)
    teacher = deepcopy(learner).eval().requires_grad_(False)
    frozen = snapshot(teacher)
    optimizer = torch.optim.SGD(learner.parameters(), lr=.1)
    prompts = [torch.tensor([1, 2], device=device), torch.tensor([3, 4], device=device)]
    errors, shared, norms = [], [], []
    for step in range(steps):
        trajectories = [rollout(learner, prompt) for prompt in prompts for _ in range(4)]
        groups = srd.split_peers(["a"] * 4 + ["b"] * 4, seed=42 + step)
        losses = []
        for group in groups:
            prompt = prompts[group.target // 4]
            trajectory = trajectories[group.target]
            sequence = torch.cat((prompt, trajectory))
            current = learner(sequence[None])[:, len(prompt) - 1:-1]
            base_views, control_views, peer_views = [], [], []
            for position in range(len(trajectory)):
                prefix = torch.cat((prompt, trajectory[:position]))
                with torch.no_grad():
                    base_views.append(teacher(prefix[None])[:, -1])
                    control_context = torch.cat((trajectories[group.control], torch.tensor([7], device=device), prefix))
                    control_views.append(teacher(control_context[None])[:, -1])
                    peer_views.append(torch.stack([teacher(torch.cat((trajectories[p], torch.tensor([7], device=device), prefix))[None])[:, -1]
                                                  for p in group.peers]))
            base = torch.stack(base_views, 1)
            control = torch.stack(control_views, 1)
            peers = torch.stack(peer_views, 2)
            mask = torch.ones(base.shape[:-1], device=device, dtype=torch.bool)
            target, info = srd.shared_residual_target(base, control, peers, mask)
            # Independent scalar-loop construction, not the implementation's
            # tensor reductions, checks q0-centering and minmod at every token.
            expected = torch.zeros_like(target)
            for t in range(base.shape[1]):
                q0 = base[0, t].softmax(-1)
                qc = control[0, t].softmax(-1)
                residuals = []
                for j in range(len(peers)):
                    d = peers[j, 0, t].log_softmax(-1) - qc.log()
                    residuals.append(d - sum(q0[v] * d[v] for v in range(len(q0))))
                retained = []
                for v in range(len(q0)):
                    values = [float(r[v]) for r in residuals]
                    retained.append(min(values) if min(values) > 0 else max(values) if max(values) < 0 else 0.)
                expected[0, t] = (q0.log() + torch.tensor(retained, device=device, dtype=q0.dtype)).softmax(-1)
            errors.append(float((expected - target).abs().max()))
            shared.append(float(info["shared_residual"].abs().mean()))
            losses.append(srd.clipped_distillation_loss(current, target, mask, coordinate_cap=1e-6))
        norms.append(update(learner, optimizer, torch.stack(losses).mean()))
    zero = torch.zeros(1, 2, 8, device=device, dtype=torch.float64)
    control_target, _ = srd.shared_residual_target(zero, zero, torch.stack((zero, zero)))
    return {"parameter_delta_l2": delta(learner, initial), "teacher_delta_l2": delta(teacher, frozen),
        "reference_max_abs_error": max(errors), "shared_residual_mean_abs": sum(shared) / len(shared),
        "identical_peer_negative_control_error": float((control_target - 1 / 8).abs().max()),
        "gradient_norm_min": min(norms), "optimizer_updates": steps,
        "coordinate_cap": 1e-6, "training_target_count": steps * 4,
        "final_signed_clipped_loss": float(torch.stack(losses).mean().detach())}


def run_progress(device, steps):
    plan = progress_reward.ProgressPlan(("Move to first", "Move to second", "Reach goal"),
        (lambda s: s[:, 0] >= 1 / 3, lambda s: s[:, 0] >= 2 / 3, lambda s: s[:, 0] >= 1),
        lambda s: s[:, 0])
    embedding = torch.eye(3, device=device, dtype=torch.float64)
    policy = nn.Linear(4, 2).to(device=device, dtype=torch.float64)
    initial = snapshot(policy)
    optimizer = torch.optim.SGD(policy.parameters(), lr=.1)
    norms = []
    for _ in range(steps):
        states = torch.rand(64, 1, device=device, dtype=torch.float64)
        augmented = progress_reward.augment_state(states, plan, embedding)
        logits = policy(augmented)
        actions = torch.multinomial(logits.softmax(-1), 1).squeeze(-1)
        next_states = (states + (2 * actions[:, None] - 1) / 3).clamp(0, 1)
        success = next_states[:, 0] >= 1
        rewards = progress_reward.progress_reward(plan.progress(states), plan.progress(next_states), success,
            gamma=.99, bonus=1., terminated=success)
        logp = logits.log_softmax(-1).gather(-1, actions[:, None]).squeeze(-1)
        norms.append(update(policy, optimizer, -(logp * (rewards - rewards.mean()).detach()).mean()))
    phi = torch.tensor([.2, .5, .8, 1.], device=device, dtype=torch.float64)
    terms = progress_reward.progress_reward(phi[:-1], phi[1:], torch.tensor([False, False, True], device=device),
        gamma=.9, bonus=0., terminated=torch.tensor([False, False, True], device=device))
    telescoped = sum(.9 ** i * terms[i] for i in range(3))
    direct = .99 * phi[1:] - phi[:-1] + torch.tensor([0., 0., 1.], device=device)
    literal = progress_reward.progress_reward(phi[:-1], phi[1:], torch.tensor([False, False, True], device=device))
    states = torch.tensor([[.1], [.4], [.9]], device=device, dtype=torch.float64)
    augmented = progress_reward.augment_state(states, plan, embedding)
    return {"parameter_delta_l2": delta(policy, initial), "gradient_norm_min": min(norms),
        "optimizer_updates": steps, "literal_equation_max_abs_error": float((literal - direct).abs().max()),
        "terminal_telescoping_abs_error": float((telescoped + phi[0]).abs()),
        "nonterminal_boundary_negative_control_gap": float(.9 ** 3 * phi[-1]),
        "subtask_embedding_max_abs_error": float((augmented[:, 1:] - embedding).abs().max())}


class ChoicePolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.head = nn.Linear(4, 4)

    def forward(self, features):
        return self.head(features)


def _arithmetic(expression):
    node = ast.parse(expression, mode="eval").body
    def visit(part):
        if isinstance(part, ast.Constant) and type(part.value) is int:
            return part.value
        if isinstance(part, ast.UnaryOp) and isinstance(part.op, ast.USub):
            return -visit(part.operand)
        if isinstance(part, ast.BinOp):
            left, right = visit(part.left), visit(part.right)
            if isinstance(part.op, ast.Add):
                return left + right
            if isinstance(part.op, ast.Sub):
                return left - right
            if isinstance(part.op, ast.Mult):
                return left * right
        raise ValueError("outside reviewed arithmetic grammar")
    return visit(node)


def run_elite(device, steps):
    operands = {"q0": (2, 3), "q1": (3, 5), "q2": (4, 6)}
    options = {q: (f"{a}+{b}", f"{a}-(-{b})", f"{a}*{b}", f"{a}+{b}+0") for q, (a, b) in operands.items()}
    approaches = ("add", "subtract", "multiply", "add")
    base = ChoicePolicy().to(device=device, dtype=torch.float64).eval().requires_grad_(False)
    frozen = snapshot(base)
    archive = elite_replay.EliteArchive({q: ("add", "subtract", "multiply") for q in operands})
    def candidate(q, index):
        text = options[q][index]
        return elite_replay.Elite(q, text, tuple(text.encode()), approaches[index], (index == 3,))
    def verify(q, solution):
        return _arithmetic(solution) == sum(operands[q])
    for q in operands:
        archive.insert(candidate(q, 0), verify)
    def features(q, target=0., parent=0.):
        a, b = operands[q]
        return torch.tensor([a / 6, b / 6, target, parent], device=device, dtype=torch.float64)
    def generate(model, q, target, parent):
        target_index = archive.applicable[q].index(target)
        logits = model(features(q, target_index, float(parent is not None)))
        index = int(torch.multinomial(logits.softmax(-1), 1))
        return candidate(q, index)
    audit = elite_replay.map_elites_search(base, archive, generate=generate, verify=verify,
        mutations_per_question=24, seed=42)
    archive.freeze()
    learner = deepcopy(base).train().requires_grad_(True)
    initial = snapshot(learner)
    optimizer = torch.optim.SGD(learner.parameters(), lr=.1)
    norms, reference_errors = [], []
    rows = torch.stack([features(q) for q in operands])
    max_length = max(len(text) for values in options.values() for text in values)
    for _ in range(steps):
        distribution = learner(rows).log_softmax(-1)
        sampled = torch.multinomial(distribution.detach().exp(), 8, replacement=True)
        # A controlled grammar's stochastic first decision chooses the entire
        # expression; its remaining deterministic tokens have log p = 0.
        selected = distribution.gather(-1, sampled)
        current = torch.cat((selected[..., None], torch.zeros(3, 8, max_length - 1, device=device)), -1)
        mask = torch.zeros_like(current, dtype=torch.bool)
        rewards = torch.zeros(3, 8, device=device, dtype=torch.float64)
        for qi, q in enumerate(operands):
            for j, index in enumerate(sampled[qi].tolist()):
                mask[qi, j, :len(options[q][index])] = True
                rewards[qi, j] = verify(q, options[q][index])
        elites = archive.sample_balanced(12)
        replay_values, replay_masks = [], []
        for item in elites:
            logp = learner(features(item.question)).log_softmax(-1)[options[item.question].index(item.solution)]
            replay_values.append(torch.cat((logp[None], torch.zeros(max_length - 1, device=device))))
            replay_masks.append(torch.arange(max_length, device=device) < len(item.tokens))
        replay, replay_mask = torch.stack(replay_values), torch.stack(replay_masks)
        loss, parts = elite_replay.grpo_replay_loss(current, current.detach(), rewards, mask, replay, replay_mask)
        expected_replay = sum(-replay[i, :int(replay_mask[i].sum())].sum() / replay_mask[i].sum() for i in range(len(elites))) / len(elites)
        reference_errors.append(float((expected_replay.detach() - parts["replay_loss"]).abs()))
        norms.append(update(learner, optimizer, loss))
    balanced = archive.sample_balanced(60)
    counts = [sum(e.question == q for e in balanced) for q in operands]
    ratio_guard = False
    try:
        elite_replay.grpo_replay_loss(
            torch.full((1, 2, 1), -1., dtype=torch.float64, device=device, requires_grad=True),
            torch.tensor([[[-1000.], [-1.]]], dtype=torch.float64, device=device),
            torch.tensor([[1., 0.]], dtype=torch.float64, device=device),
            torch.ones(1, 2, 1, dtype=torch.bool, device=device),
            torch.zeros(1, 1, dtype=torch.float64, device=device),
            torch.ones(1, 1, dtype=torch.bool, device=device))
    except ValueError:
        ratio_guard = True
    assert ratio_guard
    return {**audit, "parameter_delta_l2": delta(learner, initial), "frozen_base_delta_l2": delta(base, frozen),
        "unrepresentable_ratio_rejected": ratio_guard,
        "gradient_norm_min": min(norms), "optimizer_updates": steps,
        "replay_reference_max_abs_error": max(reference_errors), "question_sampling_count_gap": max(counts) - min(counts),
        "verified_archive_fraction": sum(verify(e.question, e.solution) for e in balanced) / len(balanced),
        "rejected_mutation_candidates": audit["mutation_attempts"] - audit["verified_candidates"],
        "seed_cells": 3, "new_cells_from_directed_search": audit["occupied_cells"] - 3,
        "replay_mixture_weight": .05}


def run_clean(device, steps):
    features = torch.randn(6, 3, device=device, dtype=torch.float64)
    clean_features = features + .1 * torch.randn_like(features)
    observed = torch.tensor([0., 1., 1., 0., 1., 0.], device=device, dtype=torch.float64)
    # These are a distinct clean calibration subset, not oracle noise rates or
    # hidden clean labels attached to the noisy training rows.
    clean_labels = torch.tensor([0., 1., 0., 1., 1., 0.], device=device, dtype=torch.float64)
    estimator = clean_rm.NoiseEstimator(3).to(device=device, dtype=torch.float64)
    initial = snapshot(estimator)
    optimizer = torch.optim.Adam(estimator.parameters(), lr=.01)
    norms, losses = [], []
    for _ in range(steps):
        loss, info = clean_rm.noise_estimation_loss(estimator, features, observed, clean_features, clean_labels)
        losses.append(float(loss.detach()))
        norms.append(update(estimator, optimizer, loss))
    with torch.no_grad():
        mu, nu = estimator(features)
    estimator_frozen = snapshot(estimator)
    reward_model = nn.Linear(3, 1).to(device=device, dtype=torch.float64)
    naive = deepcopy(reward_model)
    reward_initial = snapshot(reward_model)
    reward_optimizer = torch.optim.SGD(reward_model.parameters(), lr=.03)
    naive_optimizer = torch.optim.SGD(naive.parameters(), lr=.03)
    reward_norms = []
    for _ in range(steps):
        prediction = reward_model(features).squeeze(-1)
        loss = clean_rm.corrected_reward_loss(prediction, observed, mu, nu)
        reward_norms.append(update(reward_model, reward_optimizer, loss))
        naive_loss = (naive(features).squeeze(-1) - observed).square().mean()
        update(naive, naive_optimizer, naive_loss)
    cost = torch.tensor([[3., 1., 2.], [2., 4., .5], [.1, 2., 3.]], device=device, dtype=torch.float64)
    value, plan = clean_rm.exact_uniform_transport(cost)
    brute = min(sum(float(cost[i, p[i]]) for i in range(3)) / 3 for p in itertools.permutations(range(3)))
    zero = torch.zeros_like(mu)
    probe = reward_model(features).squeeze(-1)
    uncorrected = clean_rm.corrected_reward_loss(probe, observed, zero, zero)
    return {"noise_estimator_delta_l2": delta(estimator, initial),
        "reward_parameter_delta_l2": delta(reward_model, reward_initial),
        "noise_estimator_delta_during_reward_phase_l2": delta(estimator, estimator_frozen),
        "noise_gradient_norm_min": min(norms), "reward_gradient_norm_min": min(reward_norms),
        "noise_optimizer_updates": steps, "reward_optimizer_updates": steps,
        "initial_joint_ot_loss": losses[0], "final_preupdate_joint_ot_loss": losses[-1],
        "exact_ot_reference_abs_error": abs(float(value) - brute),
        "transport_marginal_max_abs_error": float((plan.sum(0) - 1 / 3).abs().max()),
        "nondegenerate_margin_min": float((1 - mu - nu).min()),
        "zero_noise_negative_control_abs_error": float((uncorrected - (probe - observed).square().mean()).abs()),
        "corrected_vs_naive_parameter_l2": delta(reward_model, snapshot(naive)),
        "final_signed_corrected_loss": float(loss.detach())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--code-commit")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    methods, seeds = args.methods.split(","), [int(s) for s in args.seeds.split(",")]
    if not methods or len(set(methods)) != len(methods) or set(methods) - set(METHODS):
        parser.error("unknown or duplicate method")
    if not seeds or len(set(seeds)) != len(seeds) or not 1 <= args.steps <= 12:
        parser.error("distinct seeds and 1--12 optimizer steps required")
    if args.output.exists():
        parser.error("output already exists; preserve prior results")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA explicitly requested but unavailable; no CPU fallback")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        parser.error("code commit must be a full lowercase Git object ID")
    torch.set_num_threads(1)
    start = time.monotonic()
    functions = dict(zip(METHODS, (run_srd, run_progress, run_elite, run_clean), strict=True))
    result = {"schema_version": 2, "code_commit": commit, "device": args.device,
        "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
        "diagnostic_only": True, "promotion_eligible": False, "formal_comparison_eligible": False,
        "full_experiment_status": "not_reproduced_high_cost", "seeds": seeds, "components": {},
        "executed_source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES},
        "limits": {"steps": args.steps, "no_downloads": True, "pretrained_checkpoint": None,
                   "fixture": "seeded tiny tensors/arithmetic grammar; not paper benchmark"}}
    for method in methods:
        per_seed = []
        for seed in seeds:
            torch.manual_seed(seed)
            metrics = functions[method](args.device, args.steps)
            if not all(torch.isfinite(torch.tensor(v)).all() for v in metrics.values()):
                raise RuntimeError(f"{method} returned nonfinite metrics")
            per_seed.append({"seed": seed, "metrics": metrics})
        aggregate = {}
        for key in per_seed[0]["metrics"]:
            values = torch.tensor([r["metrics"][key] for r in per_seed], dtype=torch.float64)
            aggregate[key + "_mean"] = float(values.mean())
            aggregate[key + "_std"] = float(values.std(unbiased=False))
        result["components"][method] = {"dataset": {"id": "fixture:oct17-post-numeric-grammar-v1",
            "revision": "sha256:" + result["executed_source_sha256"]["scripts/run_oct17_post_components.py"]},
            "per_seed": per_seed, "metrics": aggregate, "diagnostic_only": True, "promotion_eligible": False}
    result["elapsed_seconds"] = time.monotonic() - start
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "device": args.device, "methods": methods,
                      "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
