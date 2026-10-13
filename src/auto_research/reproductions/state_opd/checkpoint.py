"""Actual State-OPD updates over executed public calculator episodes."""
from __future__ import annotations

import hashlib
from pathlib import Path

import torch

from auto_research.post_training.response_policy import ResponsePolicy
from auto_research.post_training.oct10_checkpoint import load_public_rows, verified_reward
from auto_research.public_holdout import validate_holdout
from .algorithm import Sample, collect_response_pool, sampled_k1_dual_clip
from .environment import ArithmeticEnvironment, SYSTEM_PROMPT


class SamplingPolicy:
    def __init__(self, policy, max_tokens):
        self.policy, self.max_tokens = policy, max_tokens

    def sample(self, history):
        response = self.policy.generate(history, max_tokens=self.max_tokens)[0]
        with torch.no_grad():
            likelihood, entropy = self.policy.token_statistics(history, response.tokens, entropy=True)
        return Sample(response.tokens, response.text, likelihood.detach(), float(entropy.mean()))


def run_state_opd(*, student_path, teacher_path, student_id, student_revision, teacher_id, teacher_revision,
                  train_path, validation_path, split_manifest, dataset_revision,
                  device="cuda", seed=42, steps=2, max_turns=4, max_tokens=256,
                  multiplicity=4, concentration=2, validation_examples=4, context_limit=4096):
    if min(steps, validation_examples) < 1:
        raise ValueError("positive train/evaluation budget required")
    split = validate_holdout(split_manifest, train_path, validation_path, dataset_revision=dataset_revision)
    if not split["verified"]:
        raise ValueError("verified train-only public holdout required")
    train = load_public_rows(train_path)
    validation = load_public_rows(validation_path)[:validation_examples]
    student = ResponsePolicy(public_id=student_id, revision=student_revision, checkpoint_path=Path(student_path),
                             device=device, seed=seed, context_limit=context_limit)
    teacher = ResponsePolicy(public_id=teacher_id, revision=teacher_revision, checkpoint_path=Path(teacher_path),
                             device=device, seed=seed, context_limit=context_limit)
    if student.vocabulary_sha256 != teacher.vocabulary_sha256:
        raise ValueError("State-OPD same-prefix token supervision requires matching vocabularies")
    student.prepare_lora(learning_rate=1e-6)
    before = student.trainable_digest()

    def evaluate():
        predictions = []
        for row in validation:
            environment = ArithmeticEnvironment(row["question"])
            # Evaluation executes only one root, no training response expansion.
            _, audit = collect_response_pool(SamplingPolicy(student, max_tokens), environment,
                                             system_prompt=SYSTEM_PROMPT, max_turns=max_turns,
                                             multiplicity=1, concentration=1)
            prediction = environment.finished_answer or ""
            predictions.append({"correct": verified_reward(prediction, row["answer"]),
                                "executed_actions": audit["root_actions_executed"],
                                "submitted": environment.finished_answer is not None})
        return {"accuracy": sum(p["correct"] for p in predictions) / len(predictions),
                "submission_rate": sum(p["submitted"] for p in predictions) / len(predictions),
                "mean_executed_actions": sum(p["executed_actions"] for p in predictions) / len(predictions),
                "examples": len(predictions)}

    baseline = evaluate()
    trajectory_audits = []
    training = []
    for step in range(steps):
        row = train[step % len(train)]
        environment = ArithmeticEnvironment(row["question"])
        pool, audit = collect_response_pool(SamplingPolicy(student, max_tokens), environment,
                                            system_prompt=SYSTEM_PROMPT, max_turns=max_turns,
                                            multiplicity=multiplicity, concentration=concentration)
        denominator = sum(len(record.sample.tokens) for record in pool)
        student.optimizer.zero_grad(set_to_none=True)
        total_loss, teacher_context_digests = 0., []
        prior_reasoning_removed = 0
        for record in pool:
            teacher_messages = record.state.teacher_messages(SYSTEM_PROMPT)
            with torch.no_grad():
                teacher_likelihood, _ = teacher.token_statistics(teacher_messages, record.sample.tokens)
            # Scoring the same realized response-prefix tokens under different
            # preceding contexts, not generating a teacher replacement answer.
            student.model.train()
            current, _ = student.token_statistics(record.history, record.sample.tokens)
            token_losses = sampled_k1_dual_clip(current, teacher_likelihood,
                                               record.sample.log_probabilities)
            normalized = token_losses.sum() / denominator
            normalized.backward()
            total_loss += float(normalized.detach())
            prior_reasoning_removed += int(any(m["role"] == "assistant" for m in record.history))
            teacher_context_digests.append(hashlib.sha256(str(teacher_messages).encode()).hexdigest())
        gradient_norm = torch.nn.utils.clip_grad_norm_([p for p in student.model.parameters() if p.requires_grad],
                                                       1., error_if_nonfinite=True)
        # A zero-gradient step must not be disguised by AdamW weight decay.
        if float(gradient_norm) > 0:
            student.optimizer.step()
        student.model.eval()
        trajectory_audits.append({**audit, "teacher_prior_reasoning_removed_responses": prior_reasoning_removed,
                                  "teacher_context_sha256": teacher_context_digests,
                                  "same_current_response_prefix": True,
                                  "environment_reward_in_loss": False})
        training.append({"step": step + 1, "token_mean_sampled_k1_loss": total_loss,
                         "gradient_l2_norm": float(gradient_norm),
                         "optimizer_update_executed": float(gradient_norm) > 0,
                         "supervised_tokens": denominator})
    return {"method": "state-opd", "seed": seed, "device": device, "diagnostic_only": True,
            "evaluation_tier": "l1_mechanism", "dataset": split,
            "student": student.provenance, "teacher": teacher.provenance,
            "baseline": baseline, "method_metrics": evaluate(), "training": training,
            "parameters_changed": before != student.trainable_digest(), "trajectory_audits": trajectory_audits,
            "execution_status": "passed" if any(row["optimizer_update_executed"] for row in training) else "failed-no-gradient",
            "protocol": {"steps": steps, "max_turns": max_turns, "response_cap": max_tokens,
                         "transcript_cap": context_limit, "multiplicity": multiplicity,
                         "concentration": concentration, "test_opened": False,
                         "teacher_and_policy_receive_gold": False},
            "limitations": ["Public calculator interaction diagnostic, not ALFWorld/ScienceWorld/WebShop.",
                            "Small Qwen2.5 checkpoints replace original Qwen3 configurations.",
                            "Bounded response/transcript/step budget differs from the original scale.",
                            "A single seed and few tasks do not establish agent capability gains."]}
