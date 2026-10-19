#!/usr/bin/env python3
"""Bounded TreeOPSD, SimOPD and GR-OPD actual tiny-policy diagnostics.

Random initialization and explicit synthetic protocols only: no downloads,
pretrained competence, external API judges, formal benchmark, or Evolve claim.
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

from auto_research.post_training import gr_opd, sim_opd, tree_opsd

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("treeopsd", "simopd", "gr-opd")
SOURCES = ("scripts/run_oct19_evening_post_components.py",
           "src/auto_research/post_training/tree_opsd.py",
           "src/auto_research/post_training/sim_opd.py",
           "src/auto_research/post_training/gr_opd.py")


class TinyCausalPolicy(nn.Module):
    """Public tokens in, causal logits/states out; no reward/verifier inputs."""
    def __init__(self, hidden=8):
        super().__init__()
        self.embedding = nn.Embedding(16, hidden)
        self.recurrent = nn.GRU(hidden, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 16)

    def forward(self, ids):
        embedded = self.embedding(ids)
        recurrent, _ = self.recurrent(embedded)
        return self.head(recurrent), torch.stack((embedded, recurrent))


@torch.no_grad()
def sample(model, public_history, device, length=3):
    result = ()
    for _ in range(length):
        ids = torch.tensor([public_history + result], device=device, dtype=torch.long)
        logits, _ = model(ids)
        result += (int(torch.multinomial(logits[0, -1].softmax(-1), 1)),)
    return result


def score(model, history, response, device):
    ids = torch.tensor([history + response[:-1]], device=device, dtype=torch.long)
    logits, _ = model(ids)
    labels = torch.tensor(response, device=device)
    return logits[0, -len(response):].log_softmax(-1).gather(-1, labels[:, None]).squeeze(-1)


def representation(model, history, response, device):
    ids = torch.tensor([history + response], device=device, dtype=torch.long)
    _, states = model(ids)
    selected = states[:, :, -len(response):]
    return sim_opd.pool_response_states(selected, torch.ones(1, len(response), device=device, dtype=torch.bool))


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


def tree_reference(parents, old_span, leaves, rewards):
    mean, std = statistics.mean(rewards), statistics.stdev(rewards)
    advantages = [0. if std == 0 else (r - mean) / std for r in rewards]
    values = dict(zip(leaves, advantages, strict=True))
    for node in reversed(range(len(parents))):
        children = [i for i, parent in enumerate(parents) if parent == node]
        if children:
            maximum = max(old_span[i] for i in children)
            weights = [math.exp(old_span[i] - maximum) for i in children]
            values[node] = sum(w * values[i] for w, i in zip(weights, children, strict=True)) / sum(weights)
    return [values[i] for i in range(len(parents))]


def tree_loss_reference(current, old, credit, terminal_count, rho=.25):
    tau = (terminal_count - 1) / (rho * math.sqrt(terminal_count))
    total, tokens = 0., 0
    for new_row, old_row, value in zip(current, old, credit, strict=True):
        s = statistics.mean(a - b for a, b in zip(new_row, old_row, strict=True))
        p, q = 1 / (1 + math.exp(-s)), .5 + value / tau
        total += len(new_row) * (q * math.log(q / p) + (1 - q) * math.log((1 - q) / (1 - p)))
        tokens += len(new_row)
    return tau * total / tokens


def run_treeopsd(device, steps):
    model = TinyCausalPolicy().to(device=device, dtype=torch.float64)
    initial, optimizer = snapshot(model), torch.optim.SGD(model.parameters(), lr=.08)
    norms, errors, loss_errors, records, savings = [], [], [], [], []
    for iteration in range(steps):
        behavior = deepcopy(model).eval().requires_grad_(False)
        before_behavior = snapshot(behavior)
        prompt, trajectories = (1, 2), []

        def continue_rollout(prefix):
            turns = list(prefix)
            history = prompt + tuple(token for turn in turns for token in turn.actor + turn.observation)
            for turn in range(len(turns), 3):
                response = sample(behavior, history, device, length=2)
                observation = (8 + response[-1] % 4,) if turn < 2 else ()
                turns.append(tree_opsd.Turn(response, observation))
                history += response + observation
            return turns

        for _ in range(3):
            original = continue_rollout(())
            trajectories.append(original)
            anchor = int(torch.randint(1, 3, (1,), device=device))
            trajectories.append(continue_rollout(original[:anchor]))
        tree = tree_opsd.merge_rollout_prefixes(prompt, trajectories)
        nodes, leaves = tree["nodes"], tree["leaf_indices"]
        current, old = [], []
        for node in nodes:
            current.append(score(model, node["history"], node["actor"], device))
            with torch.no_grad():
                old.append(score(behavior, node["history"], node["actor"], device))
        current, old = torch.stack(current), torch.stack(old)
        rewards = [(sum(trajectory[-1].actor) % 16) / 15 for trajectory in trajectories]
        parents = [node["parent"] for node in nodes]
        credit = tree_opsd.tree_credit(parents, old.sum(1), leaves, torch.tensor(rewards, device=device, dtype=torch.float64))
        reference = tree_reference(parents, old.sum(1).tolist(), leaves, rewards)
        errors.append(max(abs(float(a) - b) for a, b in zip(credit, reference, strict=True)))
        mask = torch.ones_like(current, dtype=torch.bool)
        loss, audit = tree_opsd.posterior_loss(current, old, mask, credit, terminal_count=len(leaves))
        loss_errors.append(abs(float(loss.detach()) - tree_loss_reference(current.detach().tolist(), old.tolist(), reference, len(leaves))))
        norms.append(update(model, optimizer, loss))
        if delta(behavior, before_behavior) != 0 or any(p.grad is not None for p in behavior.parameters()):
            raise RuntimeError("behavior policy must remain frozen")
        savings.append(sum(len(t) for t in trajectories) - len(nodes))
        records.append({"update": iteration, "public_prompt": prompt, "nodes": nodes,
                        "leaf_indices": leaves, "explicit_synthetic_terminal_rewards": rewards,
                        "backed_up_credit": credit.tolist(), "frozen_targets": audit["target"].tolist()})
    # Scalar target/overshoot control, distinct from a measured task improvement.
    q = .7
    score_at_target = math.log(q / (1 - q))
    probe = torch.tensor([[score_at_target], [score_at_target + 1]], device=device, dtype=torch.float64, requires_grad=True)
    tau = 1 / (.25 * math.sqrt(2))
    probe_loss, _ = tree_opsd.posterior_loss(probe, torch.zeros_like(probe), torch.ones_like(probe, dtype=torch.bool),
        torch.full((2,), (q - .5) * tau, device=device, dtype=torch.float64), terminal_count=2)
    gradient = torch.autograd.grad(probe_loss, probe)[0]
    return {"metrics": {"parameter_delta_l2": delta(model, initial), "gradient_norm_min": min(norms),
        "optimizer_updates": steps, "credit_reference_max_abs_error": max(errors),
        "loss_reference_max_abs_error": max(loss_errors), "shared_prefix_turn_savings_min": min(savings),
        "target_gradient_max_abs_error": abs(float(gradient[0])), "overshoot_loss_gradient": float(gradient[1]),
        "behavior_parameter_delta_l2": 0., "behavior_gradient_count": 0,
        "real_search_or_task_capability_evaluated": False}, "tree_audit": records}


def cosine_reference(a, b):
    denominator = math.sqrt(sum(v * v for v in a) * sum(v * v for v in b))
    return sum(x * y for x, y in zip(a, b, strict=True)) / denominator if denominator else 0.


def relation_reference(student, teacher, student_bank, teacher_bank, temperature=.1):
    result = []
    for sq, tq in zip(student, teacher, strict=True):
        distributions = []
        for query, bank in ((sq, student_bank), (tq, teacher_bank)):
            logits = [cosine_reference(query, row) / temperature for row in bank]
            maximum = max(logits)
            normalizer = sum(math.exp(value - maximum) for value in logits)
            distributions.append([value - maximum - math.log(normalizer) for value in logits])
        ls, lt = distributions
        result.append(sum(math.exp(b) * (b - a) for a, b in zip(ls, lt, strict=True)))
    return statistics.mean(result)


def run_simopd(device, steps):
    model = TinyCausalPolicy(8).to(device=device, dtype=torch.float64)
    teacher = TinyCausalPolicy(12).to(device=device, dtype=torch.float64).eval().requires_grad_(False)
    initial, teacher_initial = snapshot(model), snapshot(teacher)
    optimizer, bank = torch.optim.SGD(model.parameters(), lr=.02), sim_opd.PairedMemoryBank(capacity=6)
    norms, errors, changes, pairing_controls, records = [], [], [], [], []
    for iteration in range(steps + 1):
        histories = [(1, 2 + i % 2) for i in range(4)]
        responses = [sample(model, history, device) for history in histories]
        student = torch.cat([representation(model, h, r, device) for h, r in zip(histories, responses, strict=True)])
        with torch.no_grad():
            target = torch.cat([representation(teacher, h, r, device) for h, r in zip(histories, responses, strict=True)])
        pre_update = student.detach().clone()
        ids = tuple(f"batch-{iteration}-response-{i}" for i in range(4))
        if iteration:
            loss, _ = bank.loss(student, target)
            expected = relation_reference(student.detach().tolist(), target.tolist(), bank.student.tolist(), bank.teacher.tolist())
            errors.append(abs(float(loss.detach()) - expected))
            wrong_bank = sim_opd.PairedMemoryBank(6)
            wrong_bank.append(bank.student, bank.teacher.roll(1, 0), bank.ids)
            wrong_loss, _ = wrong_bank.loss(student.detach(), target)
            pairing_controls.append(abs(float(loss.detach()) - float(wrong_loss)))
            norms.append(update(model, optimizer, loss))
            with torch.no_grad():
                after_update = torch.cat([representation(model, h, r, device) for h, r in zip(histories, responses, strict=True)])
            changes.append(float((after_update - pre_update).abs().max()))
        else:
            if delta(model, initial) != 0:
                raise RuntimeError("warmup batch must not update student")
        prior_ids = bank.ids
        bank.append(pre_update, target, ids)
        if not torch.equal(bank.student[-4:], pre_update) or bank.student.requires_grad or bank.teacher.requires_grad:
            raise RuntimeError("bank must contain detached paired pre-update states")
        records.append({"batch": iteration, "warmup_only": iteration == 0, "public_histories": histories,
                        "student_generated_responses": responses, "previous_bank_ids": prior_ids,
                        "new_bank_ids": bank.ids, "student_dim": 8, "teacher_dim": 12})
    return {"metrics": {"parameter_delta_l2": delta(model, initial), "gradient_norm_min": min(norms),
        "optimizer_updates": steps, "loss_reference_max_abs_error": max(errors),
        "mispaired_bank_negative_control_abs_difference_min": min(pairing_controls),
        "post_update_representation_change_min": min(changes), "bank_size_final": len(bank),
        "teacher_parameter_delta_l2": delta(teacher, teacher_initial),
        "teacher_gradient_count": sum(p.grad is not None for p in teacher.parameters()),
        "warmup_optimizer_updates": 0, "paired_preupdate_fifo_verified": True,
        "pretrained_teacher_capability_evaluated": False}, "paired_bank_audit": records}


def gr_reference(teacher, old, groups, gamma=.99, pressure=.25):
    scores = []
    for t, b in zip(teacher, old, strict=True):
        feedback = [max(-5., min(5., a - c)) for a, c in zip(t, b, strict=True)]
        weights = [gamma ** i for i in range(len(feedback))]
        scores.append(sum(w * v for w, v in zip(weights, feedback, strict=True)) / sum(weights))
    advantages = []
    for value, group in zip(scores, groups, strict=True):
        values = [s for s, g in zip(scores, groups, strict=True) if g == group]
        mean, std = statistics.mean(values), statistics.pstdev(values)
        advantages.append(max(-5., min(5., (value - mean + pressure * mean) / (std + 1e-6))))
    return scores, advantages


def ppo_reference(current, old, advantages):
    values = []
    for c, b, a in zip(current, old, advantages, strict=True):
        ratios = [math.exp(x - y) for x, y in zip(c, b, strict=True)]
        values.append(-statistics.mean(min(r * a, min(1.2, max(.8, r)) * a) for r in ratios))
    return statistics.mean(values)


def run_gr_opd(device, steps):
    model = TinyCausalPolicy().to(device=device, dtype=torch.float64)
    teacher = TinyCausalPolicy().to(device=device, dtype=torch.float64).eval().requires_grad_(False)
    initial, teacher_initial = snapshot(model), snapshot(teacher)
    optimizer = torch.optim.SGD(model.parameters(), lr=.04)
    norms, errors, loss_errors, weighting_controls, records = [], [], [], [], []
    for iteration in range(steps):
        behavior = deepcopy(model).eval().requires_grad_(False)
        current, old, targets, responses, groups = [], [], [], [], []
        for query in range(2):
            history = (1, 2 + query)
            for length in (2, 3, 4):
                response = sample(behavior, history, device, length=length)
                current.append(score(model, history, response, device))
                with torch.no_grad():
                    old.append(score(behavior, history, response, device))
                    targets.append(score(teacher, history, response, device))
                groups.append(f"query-{query}")
                responses.append(response)
        pad = lambda rows: nn.utils.rnn.pad_sequence(rows, batch_first=True, padding_value=0.)
        c, o, t = pad(current), pad(old), pad(targets)
        mask = torch.tensor([[i < len(r) for i in range(4)] for r in responses], device=device)
        advantage, audit = gr_opd.sequence_credit(t, o, mask, groups)
        reference_scores, reference_advantage = gr_reference([v.tolist() for v in targets], [v.tolist() for v in old], groups)
        errors.append(max(abs(float(a) - b) for a, b in zip(advantage, reference_advantage, strict=True)))
        errors.append(max(abs(float(a) - b) for a, b in zip(audit["sequence_scores"], reference_scores, strict=True)))
        loss = gr_opd.clipped_policy_loss(c, o, mask, advantage)
        loss_errors.append(abs(float(loss.detach()) - ppo_reference([v.detach().tolist() for v in current], [v.tolist() for v in old], reference_advantage)))
        # Unequal response lengths must not turn this into a global-token mean.
        global_token_mean = -sum(float(a) * len(r) for a, r in zip(advantage, responses, strict=True)) / sum(map(len, responses))
        weighting_controls.append(abs(float(loss.detach()) - global_token_mean))
        norms.append(update(model, optimizer, loss))
        records.append({"update": iteration, "query_ids": groups, "student_generated_responses": responses,
                        "sequence_scores": audit["sequence_scores"].tolist(), "groups": audit["groups"],
                        "broadcast_sequence_advantages": advantage.tolist()})
    return {"metrics": {"parameter_delta_l2": delta(model, initial), "gradient_norm_min": min(norms),
        "optimizer_updates": steps, "credit_reference_max_abs_error": max(errors),
        "loss_reference_max_abs_error": max(loss_errors),
        "global_token_weighting_negative_control_abs_difference_max": max(weighting_controls),
        "teacher_parameter_delta_l2": delta(teacher, teacher_initial),
        "teacher_gradient_count": sum(p.grad is not None for p in teacher.parameters()),
        "raw_sum_unbiasedness_claimed_for_practical_estimator": False,
        "formal_math_benchmark_evaluated": False}, "sequence_credit_audit": records}


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
            "synthetic_protocol_revision": "oct19-evening-posttraining-defining-components-v1"},
        "components": {}, **common}
    functions = {"treeopsd": run_treeopsd, "simopd": run_simopd, "gr-opd": run_gr_opd}
    for key in methods:
        rows = []
        for seed in seeds:
            torch.manual_seed(seed)
            value = functions[key](args.device, args.steps)
            if not all(math.isfinite(float(v)) for v in value["metrics"].values()):
                raise RuntimeError("nonfinite diagnostic metrics")
            rows.append({"seed": seed, "status": "completed", **value})
        summary = {}
        for name in rows[0]["metrics"]:
            values = [row["metrics"][name] for row in rows]
            summary[name] = all(values) if all(isinstance(v, bool) for v in values) else {
                "mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
        result["components"][key] = {"per_seed": rows, "metrics": summary,
            "dataset": {"id": f"synthetic:oct19-evening-{key}-v1", "revision": "sha256:" + hashes[SOURCES[0]]}, **common}
    result["elapsed_seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "methods": methods, "device": args.device,
                      "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
