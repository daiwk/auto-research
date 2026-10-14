"""Actual on-policy group rollouts and LoRA updates for GPPO/TAPO.

Zero-advantage groups are counted, never turned into invented signal. A run
without an actual parameter update fails its execution gate. This bounded
GSM8K diagnostic is not a reproduction of the original competition benchmarks.
"""
from __future__ import annotations

from pathlib import Path

import torch

from auto_research.public_holdout import validate_holdout
from auto_research.reproductions.gppo_framework.objective import gppo_loss
from auto_research.reproductions.tapo_trajectory.objective import tapo_loss
from .response_policy import ResponsePolicy
from .oct10_checkpoint import load_public_rows, verified_reward


class ProximalExecutionFailure(RuntimeError):
    def __init__(self, message, evidence):
        super().__init__(message)
        self.evidence = {"status": "failed", "diagnostic_only": True, **evidence, "error": message}


def problem_messages(question):
    return ({"role": "user", "content": "Solve the problem carefully and end with the numerical answer in \\boxed{...}.\n" + question},)


def run_proximal_checkpoint(*, method, student_path, student_id, student_revision,
                            train_path, validation_path, split_manifest, dataset_revision,
                            device="cuda", seed=42, steps=3, group=4, max_tokens=512,
                            inner_updates=2, validation_examples=8, max_task_attempts=16,
                            context_limit=4096, learning_rate=1e-5,
                            geometry="chi2", topology="atomic", delta=.04):
    if method not in {"gppo-framework", "tapo-trajectory", "grpo-control"}:
        raise ValueError("unknown proximal paper")
    if min(steps, group - 1, max_tokens, inner_updates, validation_examples, max_task_attempts) < 1:
        raise ValueError("positive training budget and at least two on-policy responses required")
    split = validate_holdout(split_manifest, train_path, validation_path, dataset_revision=dataset_revision)
    if not split["verified"]:
        raise ValueError("verified train-only public holdout required")
    train = load_public_rows(train_path)
    validation = load_public_rows(validation_path)[:validation_examples]
    policy = ResponsePolicy(public_id=student_id, revision=student_revision, checkpoint_path=Path(student_path),
                            device=device, seed=seed, context_limit=context_limit)
    policy.prepare_lora(learning_rate=learning_rate)
    before = policy.trainable_digest()

    def evaluate():
        results = []
        with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device.startswith("cuda") else []):
            torch.manual_seed(seed + 10000)
            for row in validation:
                response = policy.generate(problem_messages(row["question"]), max_tokens=max_tokens, sample=False)[0]
                results.append((0. if response.truncated else verified_reward(response.text, row["answer"]),
                                len(response.tokens), response.truncated))
        return {"accuracy": sum(r[0] for r in results) / len(results), "examples": len(results),
                "generated_tokens": sum(r[1] for r in results), "truncated_responses": sum(r[2] for r in results)}

    baseline = evaluate()
    torch.manual_seed(seed)
    cursor, zero_groups, sampled_tokens = 0, 0, 0
    history = []
    for step in range(steps):
        accepted = None
        for _ in range(max_task_attempts):
            row = train[cursor % len(train)]
            row_index = cursor % len(train)
            cursor += 1
            messages = problem_messages(row["question"])
            responses = policy.generate(messages, samples=group, max_tokens=max_tokens)
            sampled_tokens += sum(len(r.tokens) for r in responses)
            rewards = torch.tensor([0. if r.truncated else verified_reward(r.text, row["answer"])
                                    for r in responses], device=device)
            if rewards.std(unbiased=False) == 0:
                zero_groups += 1
                continue
            with torch.no_grad():
                old_likelihoods = [policy.token_statistics(messages, r.tokens)[0].detach() for r in responses]
            advantages = (rewards - rewards.mean()) / (rewards.std(unbiased=False) + 1e-6)
            accepted = messages, responses, old_likelihoods, advantages, rewards, row_index
            break
        if accepted is None:
            raise ProximalExecutionFailure(
                f"step {step + 1}: no nonzero-advantage group in {max_task_attempts} real attempts; no update fabricated",
                {"method": method, "seed": seed, "failed_step": step + 1,
                 "zero_advantage_groups": zero_groups, "tasks_attempted": cursor,
                 "generated_training_tokens": sampled_tokens, "completed_training": history,
                 "dataset": split, "checkpoint": policy.provenance},
            )
        messages, responses, old_likelihoods, advantages, rewards, row_index = accepted
        updates = []
        for update in range(inner_updates):
            policy.model.train()
            policy.optimizer.zero_grad(set_to_none=True)
            loss_sum, audits = 0., []
            for index, response in enumerate(responses):
                current, _ = policy.token_statistics(messages, response.tokens)
                old = old_likelihoods[index]
                mask = torch.ones_like(current, dtype=torch.bool)
                if method == "tapo-trajectory":
                    loss, audit = tapo_loss(current, old, advantages[index], mask, horizon=max_tokens)
                else:
                    parameters = {"geometry": geometry, "topology": topology, "delta": delta}
                    if method == "grpo-control":
                        parameters = {"geometry": "tv", "topology": "mc", "delta": .1}
                    loss, audit = gppo_loss(current, old, advantages[index], mask, **parameters)
                (loss / group).backward()
                loss_sum += float(loss.detach()) / group
                audits.append({**audit, "max_abs_log_ratio": float((current.detach() - old).abs().max())})
            gradient_norm = torch.nn.utils.clip_grad_norm_([p for p in policy.model.parameters() if p.requires_grad],
                                                          1., error_if_nonfinite=True)
            if not float(gradient_norm) > 0:
                raise ProximalExecutionFailure("zero actual gradient; weight decay is not evidence of learning",
                                                {"method": method, "seed": seed, "failed_step": step + 1,
                                                 "completed_training": history})
            policy.optimizer.step()
            updates.append({"inner_update": update + 1, "loss": loss_sum,
                            "gradient_l2_norm": float(gradient_norm), "response_audits": audits})
        policy.model.eval()
        history.append({"step": step + 1, "training_row": row_index, "rewards": rewards.tolist(),
                        "advantages": advantages.tolist(), "updates": updates})
    changed = before != policy.trainable_digest()
    if not changed:
        raise RuntimeError("no actual LoRA parameter update; execution gate failed")
    return {"method": method, "seed": seed, "device": device, "diagnostic_only": True,
            "evaluation_tier": "l1_mechanism", "dataset": split, "checkpoint": policy.provenance,
            "baseline": baseline, "method_metrics": evaluate(), "training": history,
            "parameters_changed": changed,
            "sampling": {"zero_advantage_groups_retained": zero_groups, "tasks_attempted": cursor,
                         "generated_training_tokens_including_rejected_groups": sampled_tokens},
            "protocol": {"steps": steps, "group": group, "max_tokens": max_tokens,
                         "inner_updates": inner_updates, "learning_rate": learning_rate,
                         "geometry": geometry if method == "gppo-framework" else None,
                         "topology": topology if method == "gppo-framework" else None,
                         "delta": delta if method == "gppo-framework" else None,
                         "gold_in_generation": False, "test_opened": False},
            "limitations": ["Few-step GSM8K runtime diagnostic, not original AIME/coding Avg@8 results.",
                            "Training-only difficulty calibration is charged as sampling cost.",
                            "Current-policy rejected-group counts may differ: no equal-total-compute superiority claim.",
                            "GPPO default chi2/atomic avoids equating literal KL with the paper's separate two-sided mapping."]}
