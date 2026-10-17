#!/usr/bin/env python3
"""Bounded OPRD/OpCredit numerical diagnostics; no paper capability claims.

Uses randomly initialized tiny causal/linear policies, sampled token/action
trajectories, and real optimizer updates. No downloads or external services.
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

from auto_research.post_training import operation_credit as oc
from auto_research.post_training import reminder_distillation as rd

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("oprd", "opcredit")
SOURCES = ("src/auto_research/post_training/reminder_distillation.py",
           "src/auto_research/post_training/operation_credit.py",
           "scripts/run_oct17_supplement_post.py")


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
        raise RuntimeError("diagnostic must perform a nonzero finite-gradient update")
    optimizer.step()
    return float(norm)


class TinyCausalPolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(128, 12)
        self.head = nn.Linear(12, 128)

    def forward(self, ids):
        hidden = self.embedding(ids)
        length = torch.arange(1, ids.shape[1] + 1, device=ids.device, dtype=hidden.dtype)
        return self.head(hidden.cumsum(1) / length[None, :, None])


@torch.no_grad()
def sample_turn(model, history, device):
    response = ()
    for _ in range(2):
        ids = torch.tensor([history + response], device=device)
        token = int(torch.multinomial(model(ids)[0, -1].softmax(-1), 1))
        response += (token,)
    return rd.AssistantTurn(history, response)


def oprd_reference(student, teacher, labels, success, *, top_k=100):
    """Separate per-trajectory scalar-loop implementation, not loss API reuse."""
    passed, failed = [], []
    for row in range(student.shape[0]):
        values = []
        for column in range(student.shape[1]):
            log_s = student[row, column].detach().log_softmax(-1)
            log_t = teacher[row, column].detach().log_softmax(-1)
            if bool(success[row]):
                values.append(-float(log_s[int(labels[row, column])]))
            else:
                support = sorted(range(len(log_s)), key=lambda v: max(float(log_s[v]), float(log_t[v])), reverse=True)[:top_k]
                s = log_s[support] - torch.logsumexp(log_s[support], 0)
                t = log_t[support] - torch.logsumexp(log_t[support], 0)
                values.append(sum(math.exp(float(s[v])) * float(s[v] - t[v]) for v in range(top_k)))
        (passed if bool(success[row]) else failed).append(sum(values) / len(values))
    return (sum(passed) / len(passed) if passed else 0.) + (sum(failed) / len(failed) if failed else 0.)


def run_oprd(device, steps):
    student = TinyCausalPolicy().to(device=device, dtype=torch.float64)
    initial = snapshot(student)
    teacher = rd.RefreshingTeacher(student, steps)
    optimizer = torch.optim.SGD(student.parameters(), lr=.08)
    reminders = rd.ScopedReminders((111, 112), ((0, (113,)),))
    norms, errors, frozen_errors, successes, failures = [], [], [], 0, 0
    for step in range(steps):
        current, privileged, targets, outcomes = [], [], [], []
        for row in range(8):
            history, turns = (1 + row % 2, 4), []
            for turn_index in range(3):
                turn = sample_turn(student, history, device)
                turns.append(turn)
                history += turn.response + (7 + turn_index,)
            logits, teacher_logits, labels = rd.score_trajectory(
                student, teacher.model, tuple(turns), reminders, device=device)
            current.append(logits)
            privileged.append(teacher_logits)
            targets.append(labels)
            # A deliberately nonsemantic tiny verifier, not SWE-bench success.
            outcomes.append(sum(token for turn in turns for token in turn.response) % 2 == 0)
        current, privileged, targets = torch.stack(current), torch.stack(privileged), torch.stack(targets)
        success = torch.tensor(outcomes, device=device)
        successes += sum(outcomes)
        failures += len(outcomes) - sum(outcomes)
        mask = torch.ones_like(targets, dtype=torch.bool)
        loss, _ = rd.outcome_routed_loss(current, privileged, targets, mask, success)
        errors.append(abs(float(loss.detach()) - oprd_reference(current, privileged, targets, success)))
        frozen = snapshot(teacher.model)
        norms.append(update(student, optimizer, loss))
        frozen_errors.append(delta(teacher.model, frozen))
        if any(p.grad is not None for p in teacher.model.parameters()):
            raise RuntimeError("teacher gradient leaked")
        teacher.after_update(student, step + 1)
    zero, _ = rd.shared_support_reverse_kl(current, current.detach(), mask)
    plain = rd.AssistantTurn((1, 2), (3, 4))
    scope = [rd.contexts_for_turn(plain, reminders, i) for i in range(3)]
    return {"parameter_delta_l2": delta(student, initial), "gradient_norm_min": min(norms),
            "optimizer_updates": steps, "reference_max_abs_error": max(errors),
            "teacher_delta_between_refresh_l2": max(frozen_errors),
            "teacher_gradient_count": sum(p.grad is not None for p in teacher.model.parameters()),
            "teacher_refresh_count": teacher.refresh_count, "sampled_success_trajectories": successes,
            "sampled_failure_trajectories": failures,
            "identical_teacher_negative_control_max_abs_kl": float(zero.detach().abs().max()),
            "student_context_unchanged": all(s == plain.history for s, _ in scope),
            "local_reminder_only_next_turn": all((113 in t) == (i == 1) for i, (_, t) in enumerate(scope)),
            "top_k": 100, "vocabulary_size": 128}


def boc_reference(records, rewards):
    values = []
    for record in records:
        same_question = [v for (question, _), v in rewards.items() if question == record.state.question]
        mean = sum(same_question) / len(same_question)
        sigma = math.sqrt(sum((v - mean) ** 2 for v in same_question) / len(same_question))
        relevant = [other for other in records if other.context_key == record.context_key]
        context = {other.rollout_key for other in relevant}
        operation = {other.rollout_key for other in relevant if other.operation == record.operation}
        contrast = sum(rewards[k] for k in operation) / len(operation) - sum(rewards[k] for k in context) / len(context)
        values.append((contrast if contrast != 0 else rewards[record.rollout_key] - mean) / (sigma + 1e-6))
    return values


def opcredit_reference(current, old, reference, labels, mask, boc, ftc):
    rows = []
    for i in range(current.shape[0]):
        tokens = []
        for j in range(current.shape[1]):
            if not bool(mask[i, j]):
                continue
            logp = current[i, j].detach().log_softmax(-1)
            oldp = old[i, j].detach().log_softmax(-1)
            refp = reference[i, j].detach().log_softmax(-1)
            chosen, advantage = int(labels[i, j]), float(boc[i, j])
            ratio = math.exp(float(logp[chosen] - oldp[chosen]))
            surrogate = min(ratio * advantage, min(1.2, max(.8, ratio)) * advantage)
            if advantage < 0:
                surrogate = max(surrogate, 3. * advantage)
            kl = sum(math.exp(float(logp[v])) * float(logp[v] - refp[v]) for v in range(len(logp)))
            entropy = -sum(math.exp(float(logp[v])) * float(logp[v]) for v in range(len(logp)))
            tokens.append(-surrogate - .1 * float(ftc[i, j]) * float(logp[chosen]) + .002 * kl - .001 * entropy)
        rows.append(sum(tokens) / len(tokens))
    return sum(rows) / len(rows)


def run_opcredit(device, steps):
    student = nn.Linear(4, 3).to(device=device, dtype=torch.float64)
    initial = snapshot(student)
    reference = deepcopy(student).eval().requires_grad_(False)
    frozen = snapshot(reference)
    optimizer = torch.optim.SGD(student.parameters(), lr=.1)
    norms, boc_errors, ftc_errors, loss_errors, duplicate_errors = [], [], [], [], []
    changed_credit = False
    for _ in range(steps):
        old = deepcopy(student).eval().requires_grad_(False)
        rows, token_rows, records, rewards, keys, neighborhoods = [], [], [], {}, [], {}
        for question in range(2):
            q = f"question-{question}"
            entities = tuple(f"q{question}-entity-{index}" for index in range(3))
            root = f"q{question}-root"
            # Public edges root -> each candidate; the gold tag exists only here,
            # outside actor-visible features/observations, for post-rollout credit.
            neighborhoods[q] = oc.TrainingNeighborhood(frozenset((entities[question],)), frozenset((root,)))
            for trajectory in range(6):
                identifier = str(trajectory)
                key = q, identifier
                keys.append(key)
                first = torch.tensor([question, 0., 0., 1.], device=device, dtype=torch.float64)
                with torch.no_grad():
                    selected = int(torch.multinomial(old(first).softmax(-1), 1))
                active = entities[selected]
                second = torch.tensor([question, 1., selected / 2., 1.], device=device, dtype=torch.float64)
                with torch.no_grad():
                    answer = int(torch.multinomial(old(second).softmax(-1), 1))
                rows.append(torch.stack((first, torch.zeros_like(first), second, torch.zeros_like(first))))
                token_rows.append((selected, -1, answer, -1))
                start_state = oc.VisibleKGState(q, root, frozenset((root,)), 2, "relation", entities)
                answer_state = oc.VisibleKGState(q, active, frozenset((root, active)), 1, "answer", entities)
                records.extend((oc.OperationRecord(identifier, start_state, f"relation-{selected}", (0,), (root,), (active,)),
                                oc.OperationRecord(identifier, answer_state, f"answer-{answer}", (2,), (active,), (entities[answer],))))
                # This deterministic verifier is training-only. It never chooses actions.
                rewards[key] = float(entities[answer] in neighborhoods[q].gold_answers)
                if set(start_state.policy_observation()) != {"question", "active_entity", "visited_entities", "remaining_budget", "phase", "visible_entities"}:
                    raise RuntimeError("training-only data leaked to policy observation")
        features = torch.stack(rows)
        labels = torch.tensor(token_rows, device=device, dtype=torch.long)
        mask = labels >= 0
        current = student(features)
        with torch.no_grad():
            old_logits, reference_logits = old(features), reference(features)
        boc, audit = oc.branch_outcome_credit(records, rewards, device=device)
        expected_boc = torch.tensor(boc_reference(records, rewards), device=device, dtype=torch.float64)
        boc_errors.append(float((boc - expected_boc).abs().max()))
        duplicates, _ = oc.branch_outcome_credit(records + [records[0]], rewards, device=device)
        duplicate_errors.append(float((duplicates[:-1] - boc).abs().max()))
        ftc_values = [oc.frontier_transition_credit(record, neighborhoods[record.state.question])[0] for record in records]
        ftc = torch.tensor(ftc_values, device=device, dtype=torch.float64)
        expected_ftc = []
        for record in records:
            neighborhood = neighborhoods[record.state.question]
            distance = lambda entity: 0 if entity in neighborhood.gold_answers else 1 if entity in neighborhood.one_hop_neighbors else 2
            expected_ftc.append(min(map(distance, record.before_frontier)) - min(map(distance, record.after_frontier)))
        ftc_errors.append(float((ftc - torch.tensor(expected_ftc, device=device)).abs().max()))
        changed_credit |= bool(ftc.abs().sum() > 0)
        aligned_boc, aligned_ftc = oc.align_decision_credits(records, keys, mask, boc, ftc)
        loss, _ = oc.operation_policy_loss(current, old_logits, reference_logits, labels, mask, aligned_boc, aligned_ftc)
        loss_errors.append(abs(float(loss.detach()) - opcredit_reference(current, old_logits, reference_logits, labels, mask, aligned_boc, aligned_ftc)))
        norms.append(update(student, optimizer, loss))
    blank = oc.OperationRecord("x", oc.VisibleKGState("q", "root", frozenset(("root",)), 1, "answer"), "answer", (0,), (), ("gold",))
    no_signal, eligible = oc.frontier_transition_credit(blank, oc.TrainingNeighborhood(frozenset(("gold",)), frozenset()))
    return {"parameter_delta_l2": delta(student, initial), "gradient_norm_min": min(norms),
            "optimizer_updates": steps, "frozen_reference_delta_l2": delta(reference, frozen),
            "boc_reference_max_abs_error": max(boc_errors), "ftc_reference_max_abs_error": max(ftc_errors),
            "loss_reference_max_abs_error": max(loss_errors), "duplicate_support_negative_control_max_abs_error": max(duplicate_errors),
            "unavailable_frontier_negative_control_credit": no_signal,
            "unavailable_frontier_is_ineligible": not eligible, "nonzero_signed_ftc_observed": changed_credit,
            "observation_tokens_per_trajectory_excluded": 2, "rollouts_per_question": 6,
            "last_fallback_decisions": audit["fallback_decisions"], "gold_is_training_credit_only": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    methods, seeds = args.methods.split(","), [int(v) for v in args.seeds.split(",")]
    if not methods or len(set(methods)) != len(methods) or set(methods) - set(METHODS):
        parser.error("unknown or duplicate method")
    if not seeds or len(set(seeds)) != len(seeds) or not 1 <= args.steps <= 12:
        parser.error("distinct seeds and 1--12 updates required")
    if args.output.exists():
        parser.error("preserve prior evidence: output already exists")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA unavailable; no silent CPU fallback")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        parser.error("a full lowercase Git commit is required")
    torch.set_num_threads(1)
    started = time.monotonic()
    source_hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCES}
    result = {"schema_version": 2, "code_commit": commit, "executed_source_sha256": source_hashes,
              "device": args.device, "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
              "diagnostic_only": True, "promotion_eligible": False, "formal_comparison_eligible": False,
              "full_experiment_status": "not_reproduced_high_cost", "seeds": seeds, "components": {},
              "limits": {"steps": args.steps, "no_downloads": True, "pretrained_checkpoint": None,
                         "fixture": "sampled tiny token/parity and three-entity KG; not paper benchmarks"}}
    functions = {"oprd": run_oprd, "opcredit": run_opcredit}
    for method in methods:
        per_seed = []
        for seed in seeds:
            torch.manual_seed(seed)
            metrics = functions[method](args.device, args.steps)
            if not all(math.isfinite(float(value)) for value in metrics.values()):
                raise RuntimeError("nonfinite diagnostic metric")
            per_seed.append({"seed": seed, "metrics": metrics})
        aggregate = {}
        for name in per_seed[0]["metrics"]:
            values = [float(row["metrics"][name]) for row in per_seed]
            aggregate[name + "_mean"] = statistics.mean(values)
            aggregate[name + "_std"] = statistics.stdev(values) if len(values) > 1 else 0.
        result["components"][method] = {"dataset": {"id": "fixture:oct17-supplement-post-v1",
            "revision": "sha256:" + source_hashes["scripts/run_oct17_supplement_post.py"]},
            "per_seed": per_seed, "metrics": aggregate, "diagnostic_only": True, "promotion_eligible": False}
    result["elapsed_seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "methods": methods, "seeds": seeds,
                      "device": args.device, "elapsed_seconds": result["elapsed_seconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
