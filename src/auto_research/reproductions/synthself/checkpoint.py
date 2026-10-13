"""Actual greedy aligner rewrite, external rejection and student LoRA SFT."""
from __future__ import annotations

from pathlib import Path
import torch

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.post_training.oct13_common import (CostLedger, ExecutionFailure, evaluate, load_policy,
    load_split, result_payload, sft_step)
from .algorithm import rewrite_messages, select_aligner, validate_aligner


def run(config, *, seed=42):
    train, validation, split = load_split(config)
    ledger = CostLedger()
    student = load_policy(config, seed=seed)
    aligner = load_policy(config, role="teacher", seed=seed)
    self_builder = load_policy(config, seed=seed)
    if student.vocabulary_sha256 != aligner.vocabulary_sha256:
        raise ValueError("offline rewrite tokens must match the student's exact vocabulary")
    validate_aligner(config["student_id"], config["teacher_id"],
                     sum(p.numel() for p in student.model.parameters()),
                     sum(p.numel() for p in aligner.model.parameters()))
    # Acquisition and retention are two predeclared, disjoint validation slices.
    # This default is math-only retention, explicitly NOT 14-task cross-domain retention.
    if len(validation) < 2:
        raise ValueError("SynthSelf needs disjoint acquisition and retention validation cases")
    cut = max(1, len(validation)//2)
    acquisition, retention = validation[:cut], validation[cut:]
    max_tokens = int(config.get("max_tokens", 512))
    def assess():
        return {"acquisition": evaluate(student, acquisition, ledger, max_tokens=max_tokens, seed=seed+10000),
                "retention": evaluate(student, retention, ledger, max_tokens=max_tokens, seed=seed+20000)}
    baseline = assess()
    accepted, all_rewrites, measurements = [], [], []
    gold_nll, aligner_nll, self_correct = [], [], []
    for row in train:
        response = ledger.sample(aligner, rewrite_messages(row["question"], row["answer"]),
                                 role="offline_aligner", max_tokens=max_tokens, sample=False)[0]
        own = ledger.sample(self_builder, rewrite_messages(row["question"], row["answer"]),
                            role="construction_self_rewrite", max_tokens=max_tokens, sample=False)[0]
        reward = 0. if response.truncated else verified_reward(response.text, row["answer"])
        self_correct.append(0. if own.truncated else verified_reward(own.text, row["answer"]))
        gold_tokens = tuple(student.tokenizer(row["answer"], add_special_tokens=False).input_ids)
        with torch.no_grad():
            # Eq4/5 sequence NLL, not a full-distribution KL claim.
            gold_nll.append(float(-ledger.score(student, problem_messages(row["question"]), gold_tokens).sum()))
            aligner_nll.append(float(-ledger.score(student, problem_messages(row["question"]), response.tokens).sum()))
        all_rewrites.append((row["question"], response.tokens))
        if reward:
            accepted.append((row["question"], response.tokens))
        measurements.append({"verified": bool(reward), "truncated": response.truncated,
                             "tokens": len(response.tokens)})
    if not accepted:
        raise ExecutionFailure("no verified aligner rewrite; no SFT targets fabricated",
                               {"rewrites": measurements, "cost": ledger.to_dict()})
    selection = select_aligner([{"id": config["teacher_id"], "nll": sum(aligner_nll)/len(aligner_nll),
                                "quality": len(accepted)/len(train)}],
                               gold_nll=sum(gold_nll)/len(gold_nll),
                               self_quality=sum(self_correct)/len(self_correct))
    # Algorithm 1 starts after aligner selection; a fixed same-family choice may
    # fail finite-sample Eq6. Record that fact, never relabel it as measured alignment.
    torch.manual_seed(seed)
    student.prepare_lora(learning_rate=float(config.get("learning_rate", 1e-5)))
    before = student.trainable_digest()
    epochs = int(config.get("epochs", 2))
    if epochs < 1:
        raise ValueError("positive offline training epochs required")
    training = [sft_step(student, accepted, ledger) for _ in range(epochs)]
    after = assess()
    control = load_policy(config, seed=seed)
    torch.manual_seed(seed)
    control.prepare_lora(learning_rate=float(config.get("learning_rate", 1e-5)))
    variant = config.get("control", "gold-sft")
    if variant not in {"gold-sft", "unfiltered-rewrite"}:
        raise ValueError("unknown SynthSelf control")
    targets = ([(r["question"], tuple(control.tokenizer(r["answer"], add_special_tokens=False).input_ids))
                for r in train] if variant == "gold-sft" else all_rewrites)
    control_training = [sft_step(control, targets, ledger) for _ in range(epochs)]
    control_metrics = {"acquisition": evaluate(control, acquisition, ledger, max_tokens=max_tokens, seed=seed+10000),
                       "retention": evaluate(control, retention, ledger, max_tokens=max_tokens, seed=seed+20000)}
    return result_payload("synthself", config, seed, split, student, ledger, baseline, after, training,
        parameters_changed=before != student.trainable_digest(), teacher=aligner.provenance,
        execution_status="passed" if selection is not None else "failed-aligner-constraints",
        rewrites=measurements, empirical_aligner_constraints={"satisfied": selection is not None,
            "gold_sequence_nll": sum(gold_nll)/len(gold_nll),
            "rewrite_sequence_nll": sum(aligner_nll)/len(aligner_nll),
            "aligner_quality": len(accepted)/len(train), "self_quality": sum(self_correct)/len(self_correct)},
        control={"method": variant, "training": control_training, "metrics": control_metrics},
        limitations=["Qwen2.5-0.5B/7B and GSM8K replace the original multi-domain protocol.",
                     "Retention is a predeclared disjoint math validation slice, not cross-domain capability retention.",
                     "Frozen aligner is configured a priori; finite-sample Eq6 failure is retained.",
                     "LoRA replaces original full fine-tuning; no benchmark gain is claimed."])
