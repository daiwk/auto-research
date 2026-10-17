#!/usr/bin/env python3
"""Bounded TAG/MRTPO/teacher-routing/IG-OPD/RSHD gradient diagnostics.

Randomly initialized 32-token causal models sample real continuations. Verifiers
are explicitly artificial; these runs measure equations/isolation, not LLM skill.
No downloads, API calls, pretrained checkpoints, semantic scores, or evolve use.
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

from auto_research.post_training import reviewed_oct18 as ops

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("tag-reward-gating", "mrtpo", "token-teacher-selection", "ig-opd", "rshd")
SOURCES = ("src/auto_research/post_training/reviewed_oct18.py", "scripts/run_oct18_post_components.py")


class TinyCausalPolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(32, 8)
        self.head = nn.Linear(8, 32)

    def features(self, ids):
        values = self.embedding(ids)
        counts = torch.arange(1, ids.shape[1] + 1, dtype=values.dtype, device=ids.device)
        return values.cumsum(1) / counts[None, :, None]

    def forward(self, ids):
        return self.head(self.features(ids))


def snapshot(model):
    return [p.detach().clone() for p in model.parameters()]


def delta(model, initial):
    return math.sqrt(sum(float((p.detach() - q).square().sum())
                         for p, q in zip(model.parameters(), initial, strict=True)))


def update(model, optimizer, loss):
    if not torch.isfinite(loss):
        raise RuntimeError("nonfinite objective")
    optimizer.zero_grad()
    loss.backward()
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 10., error_if_nonfinite=True)
    if norm <= 0:
        raise RuntimeError("nonzero gradient required for this diagnostic update")
    optimizer.step()
    return float(norm)


def policy(device):
    return TinyCausalPolicy().to(device=device, dtype=torch.float64)


@torch.no_grad()
def sample(model, prompt, length, device):
    output = ()
    for _ in range(length):
        ids = torch.tensor([prompt + output], dtype=torch.long, device=device)
        output += (int(torch.multinomial(model(ids)[0, -1].softmax(-1), 1)),)
    return output


def score(model, prompt, response, device):
    ids = torch.tensor([prompt + response[:-1]], dtype=torch.long, device=device)
    return model(ids)[0, -len(response):]


def score_batch(model, prompts, responses, device):
    return torch.stack([score(model, p, y, device) for p, y in zip(prompts, responses, strict=True)])


def label_mask(responses, device):
    labels = torch.tensor(responses, dtype=torch.long, device=device)
    return labels, torch.ones_like(labels, dtype=torch.bool)


def common(model, initial, norms, steps):
    return {"parameter_delta_l2": delta(model, initial), "gradient_norm_min": min(norms),
            "optimizer_updates": steps}


def scalar_policy_reference(current, old, advantage, mask):
    rows = []
    for i in range(len(current)):
        tokens = []
        for j in range(len(current[i])):
            if bool(mask[i, j]):
                ratio, a = math.exp(float(current[i, j].detach() - old[i, j])), float(advantage[i, j])
                tokens.append(-min(ratio * a, min(1.2, max(.8, ratio)) * a))
        rows.append(sum(tokens) / len(tokens))
    return sum(rows) / len(rows)


def run_tag(device, steps):
    base = policy(device)
    initial = snapshot(base)
    prompts = [(1, 2)] * 12
    probes, probe_scores, base_scores, probe_norms = [], [], [], []
    # Every channel starts from EXACTLY the same base; no joint-training reuse.
    for channel in range(2):
        probe = deepcopy(base)
        optimizer = torch.optim.SGD(probe.parameters(), lr=.06)
        for _ in range(steps):
            responses = [sample(probe, p, 3, device) for p in prompts]
            labels, mask = label_mask(responses, device)
            values = ops.token_log_probs(score_batch(probe, prompts, responses, device), labels, mask)
            rewards = torch.tensor([[float(y[channel] % 2 == 0) for y in responses]], device=device, dtype=values.dtype)
            advantages = ops.group_advantages(rewards).flatten()[:, None].expand_as(values)
            probe_norms.append(update(probe, optimizer, ops.policy_surrogate(values, values.detach(), mask, advantages)))
        probes.append(probe)
        # Separate held-out prompts and probe-generated response distributions.
        heldout = [(3, 4)] * 12
        responses = [sample(probe, p, 3, device) for p in heldout]
        labels, mask = label_mask(responses, device)
        with torch.no_grad():
            probe_scores.append(ops.token_log_probs(score_batch(probe, heldout, responses, device), labels, mask))
            base_scores.append(ops.token_log_probs(score_batch(base, heldout, responses, device), labels, mask))
    probe_scores, base_scores = torch.stack(probe_scores), torch.stack(base_scores)
    anchor, estimates = ops.elect_anchor(probe_scores, base_scores, mask[None].expand_as(probe_scores))
    reference = [sum(float((probe_scores[k] - base_scores[k])[i, j]) for i in range(12) for j in range(3)) / 36 for k in range(2)]
    restart_error = delta(base, initial)
    optimizer, norms, errors, gate_errors = torch.optim.SGD(base.parameters(), lr=.06), [], [], []
    for _ in range(steps):
        responses = [sample(base, p, 3, device) for p in prompts]
        labels, mask = label_mask(responses, device)
        rewards = torch.tensor([[[float(y[0] % 2 == 0), float(y[1] % 2 == 0)] for y in responses]], device=device, dtype=torch.float64)
        assigned = ops.tag_reward(rewards, anchor)
        expected = [float(row[anchor]) * (1 + float(row[1 - anchor])) / 2 for row in rewards[0]]
        gate_errors.append(max(abs(float(assigned[0, i]) - expected[i]) for i in range(12)))
        adv = ops.group_advantages(assigned).flatten()[:, None].expand_as(mask)
        current = ops.token_log_probs(score_batch(base, prompts, responses, device), labels, mask)
        loss = ops.policy_surrogate(current, current.detach(), mask, adv)
        errors.append(abs(float(loss.detach()) - scalar_policy_reference(current, current.detach(), adv, mask)))
        norms.append(update(base, optimizer, loss))
    controls = torch.tensor([[0., 1.], [1., 0.], [1., 1.]], device=device, dtype=torch.float64)
    return {**common(base, initial, norms, steps), "probe_gradient_norm_min": min(probe_norms),
            "probe_optimizer_updates": 2 * steps, "joint_restart_delta_l2": restart_error,
            "anchor_reference_max_abs_error": max(abs(float(estimates[k]) - reference[k]) for k in range(2)),
            "gate_reference_max_abs_error": max(gate_errors), "loss_reference_max_abs_error": max(errors),
            "auxiliary_only_negative_control_credit": float(ops.tag_reward(controls, 0)[0]),
            "anchor_channel": anchor, "probe_parameters_are_not_joint_initialization": True}


def mrtpo_reference(advantages, all_logits, omitted, beta):
    # Scalar probability calculations, independent of the tensor implementation.
    batch, channels, tokens = omitted.shape[:3]
    weights = []
    for b in range(batch):
        reward_weights = []
        for k in range(channels):
            q = []
            for t in range(tokens):
                p = all_logits[b, t].softmax(-1).tolist()
                o = omitted[b, k, t].softmax(-1).tolist()
                js = sum(.5 * (p[v] * math.log(p[v] / ((p[v] + o[v]) / 2)) + o[v] * math.log(o[v] / ((p[v] + o[v]) / 2))) for v in range(len(p)))
                q.append(math.sqrt(max(js, 0) / math.log(2)))
            mean = sum(q) / tokens
            reward_weights.append([(1 - beta) + beta * (v / mean if mean > 1e-8 else 1) for v in q])
        weights.append(reward_weights)
    uniform = [sum(float(v) for v in advantages[b]) for b in range(batch)]
    remainder = [[sum(float(advantages[b, k]) * weights[b][k][t] for k in range(channels)) - uniform[b] for t in range(tokens)] for b in range(batch)]
    denominator = sum(v * v for row in remainder for v in row)
    scale = min(1., math.sqrt(sum(tokens * v * v for v in uniform) / max(denominator, 1e-8)))
    bounded = [[uniform[b] + scale * remainder[b][t] for t in range(tokens)] for b in range(batch)]
    flat = [v for row in bounded for v in row]
    std = statistics.pstdev(flat)
    return torch.tensor([[v / (std + 1e-8) for v in row] for row in bounded], dtype=all_logits.dtype, device=all_logits.device)


def run_mrtpo(device, steps):
    student, norms, errors, loss_errors, mean_errors, no_info_errors = policy(device), [], [], [], [], []
    initial, optimizer = snapshot(student), torch.optim.SGD(student.parameters(), lr=.06)
    frozen_error = 0.
    for _ in range(steps):
        behavior = deepcopy(student).eval().requires_grad_(False)
        frozen = snapshot(behavior)
        prompts = [(1, 2)] * 12
        responses = [sample(behavior, p, 4, device) for p in prompts]
        labels, mask = label_mask(responses, device)
        rewards = torch.tensor([[[float(y[0] % 2 == 0), float(y[-1] % 2 == 0)] for y in responses]], device=device, dtype=torch.float64)
        advantages = ops.group_advantages(rewards)[0]
        all_prompts = [p + (20, 5, 21, y[-1]) for p, y in zip(prompts, responses, strict=True)]
        omitted_prompts = [[p + (21, y[-1]), p + (20, 5)] for p, y in zip(prompts, responses, strict=True)]
        with torch.no_grad():
            all_values = score_batch(behavior, all_prompts, responses, device)
            omitted = torch.stack([score_batch(behavior, [row[k] for row in omitted_prompts], responses, device) for k in range(2)], 1)
        adv, audit = ops.mrtpo_advantages(advantages, all_values, omitted, mask)
        reference = mrtpo_reference(advantages, all_values, omitted, .5)
        errors.append(float((adv - reference).abs().max()))
        mean_errors.append(float((audit["bounded"].mean(1) - advantages.sum(1)).abs().max()))
        _, zero = ops.mrtpo_advantages(advantages, all_values, all_values[:, None].expand_as(omitted), mask)
        no_info_errors.append(float((zero["weights"] - 1).abs().max()))
        current = ops.token_log_probs(score_batch(student, prompts, responses, device), labels, mask)
        with torch.no_grad():
            old = ops.token_log_probs(score_batch(behavior, prompts, responses, device), labels, mask)
        loss = ops.policy_surrogate(current, old, mask, adv)
        loss_errors.append(abs(float(loss.detach()) - scalar_policy_reference(current, old, adv, mask)))
        norms.append(update(student, optimizer, loss))
        frozen_error = max(frozen_error, delta(behavior, frozen))
    return {**common(student, initial, norms, steps), "advantage_reference_max_abs_error": max(errors),
            "loss_reference_max_abs_error": max(loss_errors), "credit_mean_preservation_max_abs_error": max(mean_errors),
            "empty_block_negative_control_max_abs_error": max(no_info_errors),
            "frozen_behavior_delta_l2": frozen_error, "actor_receives_verifier_blocks": False,
            "replay_contexts_per_response": 3}


def run_routing(device, steps):
    student = policy(device)
    teachers = [policy(device).eval().requires_grad_(False) for _ in range(2)]
    initial, frozen = snapshot(student), [snapshot(t) for t in teachers]
    optimizer, norms, errors, losses, negative = torch.optim.SGD(student.parameters(), lr=.06), [], [], [], []
    for index in range(steps):
        prompts = [(1, 2 + i % 2) for i in range(8)]
        responses = [sample(student, p, 4, device) for p in prompts]
        labels, mask = label_mask(responses, device)
        current = score_batch(student, prompts, responses, device)
        teacher_values = torch.stack([score_batch(t, prompts, responses, device) for t in teachers])
        criterion = ("entropy", "hellinger", "features")[index % 3]
        ids = [torch.tensor([p + y[:-1]], device=device) for p, y in zip(prompts, responses, strict=True)]
        features = torch.stack([student.features(x)[0, -4:] for x in ids])
        teacher_features = torch.stack([torch.stack([t.features(x)[0, -4:] for x in ids]) for t in teachers])
        target, weights = ops.route_teachers(current, teacher_values, mask, criterion=criterion,
            student_features=features, teacher_features=teacher_features)
        mixture = (weights[..., None] * teacher_values.detach().softmax(-1)).sum(0)
        errors.append(float((target.exp() - mixture).abs().max()))
        loss = ops.routed_opd_loss(current, target, labels, mask)
        rows = []
        for b in range(8):
            terms = []
            for t in range(4):
                lp = float(current[b, t].detach().log_softmax(-1)[labels[b, t]])
                terms.append(-(float(target[b, t, labels[b, t]]) - lp) * lp)
            rows.append(sum(terms) / 4)
        losses.append(abs(float(loss.detach()) - sum(rows) / 8))
        same, _ = ops.route_teachers(current, current.detach()[None], mask)
        negative.append(abs(float(ops.routed_opd_loss(current, same, labels, mask).detach())))
        norms.append(update(student, optimizer, loss))
    return {**common(student, initial, norms, steps), "mixture_reference_max_abs_error": max(errors),
            "loss_reference_max_abs_error": max(losses), "identical_teacher_negative_control_abs_loss": max(negative),
            "teacher_delta_l2": max(delta(t, f) for t, f in zip(teachers, frozen, strict=True)),
            "teacher_gradient_count": sum(p.grad is not None for t in teachers for p in t.parameters()),
            "routing_criteria_executed": min(steps, 3), "teachers_per_prefix": 2}


def run_ig(device, steps):
    student, teacher = policy(device), policy(device).eval().requires_grad_(False)
    initial, frozen = snapshot(student), snapshot(teacher)
    optimizer, norms, errors, credit_errors, gain_errors = torch.optim.SGD(student.parameters(), lr=.06), [], [], [], []
    for index in range(steps):
        current_rows, teacher_rows, labels_rows, probe_rows = [], [], [], []
        for row in range(8):
            history = (1, 2 + row % 2)
            # Training-only answer; never passed to sample/student score.
            reference = (5 + row % 2,)
            probes = [score(teacher, history, reference, device)[0].log_softmax(-1)[reference[0]]]
            current_turns, teacher_turns, labels = [], [], []
            for turn in range(3):
                response = sample(student, history, 2, device)
                current_turns.append(score(student, history, response, device))
                teacher_turns.append(score(teacher, history, response, device))
                labels.extend(response)
                if turn < 2:
                    observation = (10 + response[0] % 3,)
                    history += response + observation
                    probes.append(score(teacher, history, reference, device)[0].log_softmax(-1)[reference[0]])
            current_rows.append(torch.cat(current_turns))
            teacher_rows.append(torch.cat(teacher_turns))
            labels_rows.append(labels)
            probe_rows.append(torch.stack(probes))
        current_logits, teacher_logits = torch.stack(current_rows), torch.stack(teacher_rows)
        labels, mask = label_mask(labels_rows, device)
        current = ops.token_log_probs(current_logits, labels, mask)
        old = current.detach().clone()
        teacher_chosen = ops.token_log_probs(teacher_logits, labels, mask)
        probes = torch.stack(probe_rows)[..., None]
        gained = ops.information_gains(probes, torch.ones_like(probes, dtype=torch.bool))
        gains = torch.cat((gained, torch.zeros(8, 1, device=device, dtype=gained.dtype)), 1)
        turns = torch.tensor([[0, 0, 1, 1, 2, 2]] * 8, device=device)
        decisions = torch.tensor([[False, True, False, True, False, False]] * 8, device=device)
        adv, audit = ops.ig_calibrated_advantages(current, teacher_chosen, mask, turns, gains, decisions,
            step=index + 1, ramp_steps=steps)
        rms = math.sqrt(sum(float(v) ** 2 for row in gains for v in row) / gains.numel())
        expected = []
        for b in range(8):
            scores = [1 + .1 * math.tanh(abs(float(v)) / max(rms, 1e-6)) for v in gains[b]]
            q = [v / sum(scores) for v in scores]
            row = []
            for t in range(6):
                turn = t // 2
                value = 3 * q[turn] * float((teacher_chosen - old)[b, t])
                if bool(decisions[b, t]):
                    value += float(audit["alpha"]) * float(gains[b, turn])
                row.append(value)
            expected.append(row)
            gain_errors.append(abs(float(gained[b].sum()) - math.log(math.exp(float(probes[b, -1, 0])) + .001)
                                   + math.log(math.exp(float(probes[b, 0, 0])) + .001)))
        errors.append(float((adv - torch.tensor(expected, device=device, dtype=current.dtype)).abs().max()))
        for turn in range(3):
            credit_errors.append(float((audit["iqc"][:, turns[0] == turn].sum(1) - audit["alpha"] * gains[:, turn]).abs().max()))
        loss = ops.policy_surrogate(current, old, mask, adv)
        norms.append(update(student, optimizer, loss))
    zero_adv, zero_audit = ops.ig_calibrated_advantages(old, old, mask, turns, gains * 0, decisions)
    return {**common(student, initial, norms, steps), "advantage_reference_max_abs_error": max(errors),
            "macro_action_credit_max_abs_error": max(credit_errors), "gain_telescoping_max_abs_error": max(gain_errors),
            "no_gain_equal_teacher_negative_control_max_abs_advantage": float(zero_adv.abs().max()),
            "no_gain_turn_share_max_abs_error": float((zero_audit["turn_shares"] - 1 / 3).abs().max()),
            "formatting_iqc_max_abs_credit": float(audit["iqc"][~decisions].abs().max()),
            "teacher_delta_l2": delta(teacher, frozen), "actor_receives_reference_answer": False,
            "external_observation_tokens_excluded": 2}


def run_rshd(device, steps):
    student = policy(device)
    initial, optimizer = snapshot(student), torch.optim.SGD(student.parameters(), lr=.06)
    norms, errors, accepted, rejected, leaks, positive_weights = [], [], 0, 0, 0, 0
    teacher_gradients, frozen_error = 0, 0.
    for _ in range(steps):
        old = deepcopy(student).eval().requires_grad_(False)
        frozen = snapshot(old)
        plain_values, privileged_values, replay_labels = [], [], []
        original_logits, original_labels, original_adv = [], [], []
        for problem in range(5):
            prompt, gold = (1, 2 + problem % 2), (5 + problem % 2,)
            # Artificial outcome: last token has the reference residue. Neither
            # gold token nor its residue is handed to the note writer or sampler.
            verify = lambda y: int(y[-1] % 4 == gold[0] % 4)
            originals = [sample(old, prompt, 3, device) for _ in range(8)]
            rewards = [verify(y) for y in originals]
            group = ops.group_advantages(torch.tensor([rewards], device=device, dtype=torch.float64))[0]
            for response, advantage, reward in zip(originals, group, rewards, strict=True):
                original_logits.append(score(student, prompt, response, device))
                original_labels.append(response)
                original_adv.append(advantage)
                if reward:
                    continue
                writer_prompt = prompt + response + (27,)  # only failure marker
                note = sample(old, writer_prompt, 2, device)
                leaking = ops.note_has_answer(note, gold)
                replays = [sample(old, prompt + note, 3, device) for _ in range(2)]
                outcomes = [verify(y) for y in replays]
                leaks += int(leaking)
                if not ops.admit_note(rewards, outcomes, valid=True, leaks_answer=leaking):
                    rejected += 1
                    continue
                accepted += 1
                # Uniform replay selection, not cherry-picking successes.
                replay = replays[int(torch.randint(2, (1,), device=device))]
                plain_values.append(score(student, prompt, replay, device))
                privileged_values.append(score(old, prompt + note, replay, device))
                replay_labels.append(replay)
        logits = torch.stack(original_logits)
        labels, mask = label_mask(original_labels, device)
        current = ops.token_log_probs(logits, labels, mask)
        advantage = torch.stack(original_adv)[:, None].expand_as(current)
        loss = ops.policy_surrogate(current, current.detach(), mask, advantage)
        if replay_labels:
            plain, privileged = torch.stack(plain_values), torch.stack(privileged_values)
            labels, replay_mask = label_mask(replay_labels, device)
            aux, weights = ops.rshd_aux_loss(plain, privileged, labels, replay_mask,
                torch.ones(len(replay_labels), device=device, dtype=torch.bool))
            terms = []
            for i in range(len(replay_labels)):
                for j in range(3):
                    lp = float(plain[i, j].detach().log_softmax(-1)[labels[i, j]])
                    lt = float(privileged[i, j].detach().log_softmax(-1)[labels[i, j]])
                    terms.append(-min(2., max(0., lt - lp)) * lp)
            errors.append(abs(float(aux.detach()) - sum(terms) / len(terms)))
            positive_weights += int((weights > 0).sum())
            loss = loss + .2 * aux
        norms.append(update(student, optimizer, loss))
        teacher_gradients += sum(p.grad is not None for p in old.parameters())
        frozen_error = max(frozen_error, delta(old, frozen))
    # Empty admission must reduce EXACTLY to GRPO, not self-imitation.
    controls = torch.randn(1, 2, 4, device=device, dtype=torch.float64, requires_grad=True)
    no_aux, _ = ops.rshd_aux_loss(controls, controls.detach() + .2, torch.zeros(1, 2, device=device, dtype=torch.long),
        torch.ones(1, 2, device=device, dtype=torch.bool), torch.zeros(1, device=device, dtype=torch.bool))
    return {**common(student, initial, norms, steps), "aux_loss_reference_max_abs_error": max(errors, default=0.),
            "accepted_notes": accepted, "rejected_notes": rejected, "answer_leaking_notes_rejected": leaks,
            "positive_lift_tokens": positive_weights, "empty_admission_negative_control_abs_loss": float(no_aux.detach().abs()),
            "equal_replay_rate_is_rejected": not ops.admit_note([1, 0], [1, 0], valid=True, leaks_answer=False),
            "leaking_note_is_rejected": not ops.admit_note([0, 0], [1, 1], valid=True, leaks_answer=True),
            "frozen_behavior_delta_l2": frozen_error, "teacher_gradient_count": teacher_gradients,
            "note_writer_receives_reference_answer": False, "semantic_note_screen_implemented": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--steps", type=int, default=3)
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    methods, seeds = args.methods.split(","), [int(value) for value in args.seeds.split(",")]
    if not methods or len(methods) != len(set(methods)) or set(methods) - set(METHODS):
        parser.error("distinct known methods required")
    if not seeds or len(seeds) != len(set(seeds)) or not 1 <= args.steps <= 8:
        parser.error("distinct seeds and 1--8 steps required")
    if args.output.exists():
        parser.error("immutable output already exists")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA unavailable; no silent CPU fallback")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if len(commit) != 40 or any(value not in "0123456789abcdef" for value in commit):
        parser.error("full lowercase Git commit required")
    torch.set_num_threads(1)
    started = time.monotonic()
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCES}
    result = {"schema_version": 2, "code_commit": commit, "executed_source_sha256": hashes,
        "device": args.device, "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
        "diagnostic_only": True, "promotion_eligible": False, "formal_comparison_eligible": False,
        "evolve_integrated": False, "full_experiment_status": "not_reproduced_high_cost", "seeds": seeds,
        "limits": {"steps": args.steps, "no_downloads": True, "pretrained_checkpoint": None,
            "fixture": "random 32-token causal policies and artificial residue verifiers; not paper benchmarks"},
        "components": {}}
    functions = dict(zip(METHODS, (run_tag, run_mrtpo, run_routing, run_ig, run_rshd), strict=True))
    for method in methods:
        per_seed = []
        for seed in seeds:
            torch.manual_seed(seed)
            metrics = functions[method](args.device, args.steps)
            if not all(math.isfinite(float(value)) for value in metrics.values()):
                raise RuntimeError("nonfinite metric")
            per_seed.append({"seed": seed, "status": "completed", "metrics": metrics})
        aggregate = {}
        for field in per_seed[0]["metrics"]:
            values = [row["metrics"][field] for row in per_seed]
            if all(isinstance(value, bool) for value in values):
                aggregate[field] = all(values)
            else:
                aggregate[field] = {"mean": statistics.mean(values),
                    "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
        result["components"][method] = {"dataset": {"id": "fixture:oct18-post-components-v1",
            "revision": "sha256:" + hashes[SOURCES[-1]]}, "per_seed": per_seed, "metrics": aggregate,
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost"}
    result["elapsed_seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "methods": methods, "seeds": seeds,
        "device": args.device, "elapsed_seconds": result["elapsed_seconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
