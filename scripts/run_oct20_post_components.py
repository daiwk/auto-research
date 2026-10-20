#!/usr/bin/env python3
"""Actual tiny causal-policy SPOD/APSD/TAR diagnostics; no pretrained capability.

No downloads, external APIs, benchmark, semantic-encoder or Evolve claim.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import time

import torch
from torch import nn

from auto_research.post_training import apsd, spod, tar

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("spod", "apsd", "tar-adaptive-replay")
SOURCES = ("scripts/run_oct20_post_components.py", "src/auto_research/post_training/spod.py",
           "src/auto_research/post_training/apsd.py", "src/auto_research/post_training/tar.py")


class TinyCausalPolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(16, 8)
        self.recurrent = nn.GRU(8, 8, batch_first=True)
        self.head = nn.Linear(8, 16)

    def forward(self, ids):
        hidden, _ = self.recurrent(self.embedding(ids))
        return self.head(hidden), hidden


@torch.no_grad()
def sample(model, public_history, device, length=2):
    response = ()
    for _ in range(length):
        ids = torch.tensor([public_history + response], dtype=torch.long, device=device)
        logits, _ = model(ids)
        response += (int(torch.multinomial(logits[0, -1].softmax(-1), 1)),)
    return response


def score(model, history, response, device):
    ids = torch.tensor([history + response[:-1]], dtype=torch.long, device=device)
    logits, _ = model(ids)
    return logits[0, -len(response):]


def selected(logits, responses, device):
    labels = nn.utils.rnn.pad_sequence([torch.tensor(r, device=device) for r in responses], batch_first=True)
    return logits.log_softmax(-1).gather(-1, labels[..., None]).squeeze(-1)


def pad(rows):
    return nn.utils.rnn.pad_sequence(rows, batch_first=True, padding_value=0.)


def mask_for(responses, device):
    return torch.tensor([[j < len(r) for j in range(max(map(len, responses)))] for r in responses], device=device)


def snapshot(model):
    return [p.detach().clone() for p in model.parameters()]


def delta(model, initial):
    return math.sqrt(sum(float((p.detach() - q).square().sum()) for p, q in zip(model.parameters(), initial, strict=True)))


def update(model, optimizer, loss):
    optimizer.zero_grad()
    loss.backward()
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 10., error_if_nonfinite=True)
    if not torch.isfinite(loss) or not math.isfinite(float(norm)) or float(norm) <= 0:
        raise RuntimeError("actual finite nonzero policy gradient required")
    optimizer.step()
    return float(norm)


def log_softmax_reference(values):
    maximum = max(values)
    normalizer = maximum + math.log(sum(math.exp(x - maximum) for x in values))
    return [x - normalizer for x in values]


def spod_reference(student, teacher, responses, episodes, success, *, retain_kl_on_protected=False):
    actions, gates = [], []
    for s, t, response, episode in zip(student, teacher, responses, episodes, strict=True):
        ps = [log_softmax_reference(row) for row in s[:len(response)]]
        pt = [log_softmax_reference(row) for row in t[:len(response)]]
        lp = sum(row[token] for row, token in zip(ps, response, strict=True))
        lq = sum(row[token] for row, token in zip(pt, response, strict=True))
        kl = statistics.mean(sum(math.exp(b) * (b - a) for a, b in zip(x, y, strict=True)) for x, y in zip(ps, pt, strict=True))
        gate = success[episode] and lq < lp
        floor = max(0., math.log(.5) - lp) / len(response)
        actions.append((kl if retain_kl_on_protected else 0.) + floor if gate else kl)
        gates.append(gate)
    value = statistics.mean(statistics.mean(v for v, e in zip(actions, episodes, strict=True) if e == episode) for episode in dict.fromkeys(episodes))
    return value, gates


def run_spod(device, steps):
    model = TinyCausalPolicy().to(device=device, dtype=torch.float64)
    teacher = TinyCausalPolicy().to(device=device, dtype=torch.float64).eval().requires_grad_(False)
    initial, teacher_initial = snapshot(model), snapshot(teacher)
    optimizer = torch.optim.SGD(model.parameters(), lr=.05)
    errors, norms, protections, control_differences, records = [], [], [], [], []
    for iteration in range(steps):
        current, targets, responses, episodes, success, histories = [], [], [], [], {}, []
        for episode, states in enumerate((1, 2, 3, 2)):
            history = (1, 2 + episode)
            episode_id = f"episode-{episode}"
            for state in range(states):
                response = sample(model, history, device, length=1 + state % 3)
                current.append(score(model, history, response, device))
                with torch.no_grad():
                    targets.append(score(teacher, history, response, device))
                histories.append(history)
                responses.append(response)
                episodes.append(episode_id)
                history += response + (8 + response[-1] % 4,)
            # Explicit synthetic training outcome is computed outside actor.
            success[episode_id] = response[-1] % 2 == episode % 2
        current, targets = pad(current), pad(targets)
        mask = mask_for(responses, device)
        labels = pad([torch.tensor(r, dtype=torch.long, device=device) for r in responses])
        loss, audit = spod.success_preserving_loss(current, targets, labels, mask, episodes, success)
        expected, expected_gate = spod_reference(current.detach().tolist(), targets.tolist(), responses, episodes, success)
        wrong, _ = spod_reference(current.detach().tolist(), targets.tolist(), responses, episodes, success, retain_kl_on_protected=True)
        errors.append(abs(float(loss.detach()) - expected))
        if audit["gate"].tolist() != expected_gate:
            raise RuntimeError("action-level success/conflict gate differs from independent reference")
        protections.append(int(audit["gate"].sum()))
        control_differences.append(abs(float(loss.detach()) - wrong))
        norms.append(update(model, optimizer, loss))
        records.append({"update": iteration, "public_histories": histories, "sampled_actions": responses,
                        "episode_ids": episodes, "explicit_training_episode_successes": success,
                        "protected_decisions": audit["gate"].tolist(), "student_action_logp": audit["student_sequence_logp"].tolist(),
                        "teacher_action_logp": audit["teacher_sequence_logp"].tolist()})
    return {"metrics": {"parameter_delta_l2": delta(model, initial), "gradient_norm_min": min(norms),
        "optimizer_updates": steps, "loss_reference_max_abs_error": max(errors),
        "protected_decisions_total": sum(protections), "floor_without_mask_negative_control_difference_max": max(control_differences),
        "teacher_parameter_delta_l2": delta(teacher, teacher_initial),
        "teacher_gradient_count": sum(p.grad is not None for p in teacher.parameters()),
        "raw_model_logits_used": True, "evaluation_outcomes_used_by_gate": False,
        "agent_benchmark_evaluated": False}, "action_audit": records}


def apsd_reference(student, teacher, correctness, *, gradient=False):
    total, gradients = 0., []
    for srow, trow, correct in zip(student, teacher, correctness, strict=True):
        alpha, row_gradients = (.5 if correct else 1.5), []
        for s, t in zip(srow, trow, strict=True):
            lp, lq = log_softmax_reference(s), log_softmax_reference(t)
            lt = log_softmax_reference([(1 - alpha) * a + alpha * b for a, b in zip(lp, lq, strict=True)])
            p, target = [math.exp(v) for v in lp], [math.exp(v) for v in lt]
            discrepancy = [a - b for a, b in zip(lp, lq, strict=True)]
            expectation = sum(a * b for a, b in zip(p, discrepancy, strict=True))
            total += sum(prob * (a - b) for prob, a, b in zip(p, lp, lt, strict=True))
            row_gradients.append([(alpha * prob * (difference - expectation) + (1 - alpha) * (q - prob)) / len(student)
                                  for prob, difference, q in zip(p, discrepancy, target, strict=True)])
        gradients.append(row_gradients)
    return gradients if gradient else total / len(student)


def run_apsd(device, steps):
    model = TinyCausalPolicy().to(device=device, dtype=torch.float64)
    initial, optimizer = snapshot(model), torch.optim.SGD(model.parameters(), lr=.05)
    errors, derivative_errors, finite_errors, differences, norms, frozen_deltas, records = [], [], [], [], [], [], []
    for iteration in range(steps):
        # Same current underlying policy, not a separately initialized teacher.
        self_teacher = deepcopy(model).eval().requires_grad_(False)
        teacher_initial = snapshot(self_teacher)
        histories, responses, correctness, student_rows, teacher_rows = [], [], [], [], []
        for instance in range(4):
            history = (1, 2 + instance % 2)
            response = sample(model, history, device, length=2)
            correct = response[-1] % 2 == instance % 2
            feedback = (14 if correct else 15,)
            student_rows.append(score(model, history, response, device))
            with torch.no_grad():
                teacher_rows.append(score(self_teacher, history + feedback, response, device))
            histories.append(history)
            responses.append(response)
            correctness.append(correct)
        student, target = torch.stack(student_rows), torch.stack(teacher_rows)
        mask = torch.ones(student.shape[:2], device=device, dtype=torch.bool)
        loss, audit = apsd.asymmetric_self_distillation_loss(student, target, torch.tensor(correctness, device=device), mask)
        raw_s, raw_t = student.detach().tolist(), target.tolist()
        errors.append(abs(float(loss.detach()) - apsd_reference(raw_s, raw_t, correctness)))
        actual = torch.autograd.grad(loss, student, retain_graph=True)[0]
        reference = torch.tensor(apsd_reference(raw_s, raw_t, correctness, gradient=True), device=device, dtype=torch.float64)
        derivative_errors.append(float((actual - reference).abs().max()))
        for token in (0, 7, 15):
            plus, minus = deepcopy(raw_s), deepcopy(raw_s)
            plus[0][0][token] += 1e-5
            minus[0][0][token] -= 1e-5
            difference = (apsd_reference(plus, raw_t, correctness) - apsd_reference(minus, raw_t, correctness)) / 2e-5
            finite_errors.append(abs(float(actual[0, 0, token]) - difference))
        log_student = student.log_softmax(-1)
        detached_loss = (log_student.exp() * (log_student - audit["target_log_probs"].detach())).sum(-1).sum(1).mean()
        detached_gradient = torch.autograd.grad(detached_loss, student, retain_graph=True)[0]
        differences.append(float((actual - detached_gradient).norm()))
        norms.append(update(model, optimizer, loss))
        frozen_deltas.append(delta(self_teacher, teacher_initial))
        if any(p.grad is not None for p in self_teacher.parameters()):
            raise RuntimeError("feedback-conditioned self-teacher must remain detached")
        records.append({"update": iteration, "public_actor_histories": histories,
                        "student_generated_responses": responses, "explicit_training_correctness": correctness,
                        "feedback_condition_only_on_self_teacher": True, "alphas": audit["alpha"].tolist()})
    return {"metrics": {"parameter_delta_l2": delta(model, initial), "gradient_norm_min": min(norms),
        "optimizer_updates": steps, "loss_reference_max_abs_error": max(errors),
        "logit_gradient_reference_max_abs_error": max(derivative_errors), "finite_difference_max_abs_error": max(finite_errors),
        "detached_target_negative_control_gradient_difference_min": min(differences),
        "self_teacher_parameter_delta_during_update_max": max(frozen_deltas), "self_teacher_gradient_count": 0,
        "self_teacher_is_current_policy_copy": True, "feedback_in_actor_condition": False,
        "formal_reasoning_or_code_benchmark_evaluated": False}, "self_teacher_audit": records}


def replay_reference(current, base):
    total, gradients, gates = 0., [], []
    for lp, lb in zip(current, base, strict=True):
        differences = [b - p for p, b in zip(lp, lb, strict=True)]
        phi = lambda x: -math.expm1(-max(x, 0.))
        gate = phi(statistics.mean(differences))
        weights = [phi(x) for x in differences]
        denominator = 1e-8 + sum(weights)
        total += gate * sum(w * -p for w, p in zip(weights, lp, strict=True)) / denominator
        gradients.append([-gate * w / denominator / len(current) for w in weights])
        gates.append(gate)
    return total / len(current), gradients, gates


def run_tar(device, steps):
    model = TinyCausalPolicy().to(device=device, dtype=torch.float64)
    base = deepcopy(model).eval().requires_grad_(False)
    initial, base_initial = snapshot(model), snapshot(base)
    optimizer = torch.optim.SGD(model.parameters(), lr=.15)
    memory, bank_audit = [], []
    for query in range(2):
        history = (1, 2 + query)
        responses = [sample(base, history, device, length=2) for _ in range(8)]
        correct = torch.tensor([r[-1] % 2 == query for r in responses], device=device)
        with torch.no_grad():
            embeddings = torch.cat([base(torch.tensor([history + r], device=device))[1][:, -1] for r in responses])
        retained = tar.farthest_point_prototypes(embeddings, correct)
        memory.extend((history, responses[i]) for i in retained)
        bank_audit.append({"query": query, "actual_base_sampled_candidates": responses,
                           "explicit_training_verifier_correct": correct.tolist(), "retained_original_indices": retained,
                           "embedding_source": "random-initialized-causal-GRU-hidden-state-not-semantic-encoder"})
    if not memory:
        raise RuntimeError("this bounded fixture produced no correct base trajectories; do not substitute gold")
    memory_responses = [r for _, r in memory]
    with torch.no_grad():
        base_memory = torch.stack([score(base, h, r, device).log_softmax(-1).gather(-1, torch.tensor(r, device=device)[:, None]).squeeze(-1) for h, r in memory])
    norms, errors, gradient_errors, replay_norms, ungated_differences, records = [], [], [], [], [], []
    for iteration in range(steps):
        behavior = deepcopy(model).eval().requires_grad_(False)
        responses, histories, outcomes = [], [], []
        for query in range(2):
            for _ in range(6):
                history = (1, 2 + query)
                response = sample(behavior, history, device, length=2)
                histories.append(history)
                responses.append(response)
                outcomes.append(float(response[-1] % 2 == query))
        current_logits = torch.stack([score(model, h, r, device) for h, r in zip(histories, responses, strict=True)])
        with torch.no_grad():
            old_logits = torch.stack([score(behavior, h, r, device) for h, r in zip(histories, responses, strict=True)])
            reference_logits = torch.stack([score(base, h, r, device) for h, r in zip(histories, responses, strict=True)])
        current_lp, old_lp = selected(current_logits, responses, device), selected(old_logits, responses, device)
        reward = torch.tensor(outcomes, device=device, dtype=torch.float64).reshape(2, 6)
        advantage = ((reward - reward.mean(1, keepdim=True)) / (reward.std(1, correction=0, keepdim=True) + 1e-6)).flatten().detach()
        a, difference = advantage[:, None], current_lp - old_lp
        chosen = torch.where(a >= 0, difference.clamp_max(math.log(1.2)), difference.clamp_min(math.log(.8)))
        policy_loss = -(chosen.exp() * a).mean()
        log_p, log_ref = current_logits.log_softmax(-1), reference_logits.log_softmax(-1)
        reference_kl = (log_p.exp() * (log_p - log_ref)).sum(-1).mean()
        replay_lp = torch.stack([score(model, h, r, device).log_softmax(-1).gather(-1, torch.tensor(r, device=device)[:, None]).squeeze(-1) for h, r in memory])
        replay_loss, audit = tar.adaptive_replay_loss(replay_lp, base_memory, torch.ones_like(replay_lp, dtype=torch.bool))
        expected, expected_gradient, _ = replay_reference(replay_lp.detach().tolist(), base_memory.tolist())
        errors.append(abs(float(replay_loss.detach()) - expected))
        actual_gradient = torch.autograd.grad(replay_loss, replay_lp, retain_graph=True)[0]
        reference_gradient = torch.tensor(expected_gradient, device=device, dtype=torch.float64)
        gradient_errors.append(float((actual_gradient - reference_gradient).abs().max()))
        replay_norms.append(float(actual_gradient.norm()))
        ungated_differences.append(abs(float(replay_loss.detach() + replay_lp.detach().mean())))
        norms.append(update(model, optimizer, policy_loss + .001 * reference_kl + replay_loss))
        records.append({"update": iteration, "actual_on_policy_responses": responses,
                        "explicit_training_verifier_rewards": outcomes, "memory_actor_responses": memory_responses,
                        "trajectory_gap": audit["trajectory_gap"].tolist(), "trajectory_gate": audit["trajectory_gate"].tolist(),
                        "token_weights": audit["token_weights"].tolist()})
    return {"metrics": {"parameter_delta_l2": delta(model, initial), "gradient_norm_min": min(norms),
        "optimizer_updates": steps, "loss_reference_max_abs_error": max(errors),
        "replay_gradient_reference_max_abs_error": max(gradient_errors), "replay_gradient_norm_max": max(replay_norms),
        "nonzero_replay_updates": sum(value > 0 for value in replay_norms), "bank_trajectory_count": len(memory),
        "ungated_sft_negative_control_difference_max": max(ungated_differences),
        "base_parameter_delta_l2": delta(base, base_initial), "base_gradient_count": sum(p.grad is not None for p in base.parameters()),
        "base_trajectories_replaced_with_gold": False, "semantic_encoder_used": False,
        "reasoning_diversity_benchmark_evaluated": False}, "bank_audit": bank_audit, "replay_audit": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--steps", type=int, default=3)
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        methods, seeds = args.methods.split(","), [int(v) for v in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not methods or len(set(methods)) != len(methods) or set(methods) - set(METHODS):
        parser.error("distinct known methods required")
    if not seeds or len(set(seeds)) != len(seeds) or any(s < 0 or s >= 2 ** 32 for s in seeds) or not 1 <= args.steps <= 8:
        parser.error("distinct bounded seeds and 1--8 updates required")
    if args.output.exists():
        parser.error("immutable output exists")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("requested CUDA unavailable; no silent CPU fallback")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        parser.error("full lowercase code commit required")
    torch.set_num_threads(1)
    started = time.monotonic()
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCES}
    common = {"diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
              "formal_comparison_eligible": False, "full_experiment_status": "not_reproduced_high_cost"}
    result = {"schema_version": 2, "code_commit": commit, "executed_source_sha256": hashes,
        "device": args.device, "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
        "seeds": seeds, "limits": {"steps": args.steps, "no_downloads": True, "pretrained_checkpoint": None,
            "synthetic_protocol_revision": "oct20-spod-apsd-tar-defining-components-v1"}, "components": {}, **common}
    methods_to_run = {"spod": run_spod, "apsd": run_apsd, "tar-adaptive-replay": run_tar}
    for key in methods:
        rows = []
        for seed in seeds:
            torch.manual_seed(seed)
            value = methods_to_run[key](args.device, args.steps)
            if not all(math.isfinite(float(v)) for v in value["metrics"].values()):
                raise RuntimeError("nonfinite diagnostic metrics")
            rows.append({"seed": seed, "status": "completed", **value})
        summary = {}
        for name in rows[0]["metrics"]:
            values = [row["metrics"][name] for row in rows]
            summary[name] = all(values) if all(isinstance(v, bool) for v in values) else {
                "mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
        result["components"][key] = {"per_seed": rows, "metrics": summary,
            "dataset": {"id": f"synthetic:oct20-{key}-v1", "revision": "sha256:" + hashes[SOURCES[0]],
                        "capability_benchmark": False}, **common}
    result["elapsed_seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "methods": methods, "device": args.device,
                      "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
