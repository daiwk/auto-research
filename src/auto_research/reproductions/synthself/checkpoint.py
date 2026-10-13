"""Actual greedy aligner rewrite, external rejection and student LoRA SFT."""
from __future__ import annotations

from pathlib import Path
import torch

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.post_training.oct13_common import (CostLedger, ExecutionFailure, evaluate, load_policy,
    load_split, result_payload, sft_step)
from .algorithm import complete_response_tokens, naturally_complete_response, rewrite_messages, select_aligner, validate_aligner


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
    eos=student.tokenizer.eos_token_id
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
        complete=naturally_complete_response(response.tokens,truncated=response.truncated,eos_token_id=eos)
        own_complete=naturally_complete_response(own.tokens,truncated=own.truncated,eos_token_id=eos)
        reward = verified_reward(response.text, row["answer"]) if complete else 0.
        self_correct.append(verified_reward(own.text, row["answer"]) if own_complete else 0.)
        raw_gold_tokens = tuple(student.tokenizer(row["answer"], add_special_tokens=False).input_ids)
        gold_tokens = complete_response_tokens(raw_gold_tokens,eos_token_id=eos)
        # A partial output may be scored diagnostically, but EOS is NEVER
        # fabricated onto it to turn a bounded prefix into a complete rewrite.
        rewrite_tokens = (complete_response_tokens(response.tokens,eos_token_id=eos)
                          if complete else response.tokens)
        with torch.no_grad():
            # Eq4/5 sequence NLL, not a full-distribution KL claim.
            gold_nll.append(float(-ledger.score(student, problem_messages(row["question"]), gold_tokens).sum()))
            aligner_nll.append(float(-ledger.score(student, problem_messages(row["question"]), rewrite_tokens).sum()))
        if complete:
            all_rewrites.append((row["question"], rewrite_tokens))
        if reward:
            accepted.append((row["question"], rewrite_tokens))
        measurements.append({"verified": bool(reward), "truncated": response.truncated,
                             "tokens": len(response.tokens),"gold_original_tokens":len(raw_gold_tokens),
                             "gold_scored_tokens":len(gold_tokens),"rewrite_scored_tokens":len(rewrite_tokens),
                             "gold_scored_eos_count":gold_tokens.count(eos),"rewrite_scored_eos_count":rewrite_tokens.count(eos),
                             "gold_canonical_eos_appended":eos not in raw_gold_tokens,
                             "rewrite_natural_completion":complete,"rewrite_canonical_eos_appended":False,
                             "rewrite_nll_scope":"complete_sequence" if complete else "actual_partial_diagnostic_only",
                             "self_response_truncated":own.truncated,"self_natural_completion":own_complete})
    all_complete=all(row["rewrite_natural_completion"] for row in measurements)
    empirical={"satisfied":False,"all_aligner_responses_naturally_complete":all_complete,
        "selection_blocked_by_incomplete_outputs":not all_complete,
        "nll_reduction":"full-response sequence sum including exactly one EOS",
        "eos_token_id":eos,"gold_and_rewrite_eos_policy":"gold canonical EOS; rewrite requires actual single terminal EOS",
        "gold_sequence_nll":sum(gold_nll)/len(gold_nll),
        "rewrite_sequence_nll":sum(aligner_nll)/len(aligner_nll) if all_complete else None,
        "diagnostic_bounded_rewrite_sequence_or_partial_nll":sum(aligner_nll)/len(aligner_nll),
        "aligner_quality":len(accepted)/len(train),"self_quality":sum(self_correct)/len(self_correct)}
    if not accepted:
        raise ExecutionFailure("no verified aligner rewrite; no SFT targets fabricated",
                               {"rewrites": measurements,"empirical_aligner_constraints":empirical,"cost": ledger.to_dict()})
    selection = select_aligner([{"id": config["teacher_id"], "nll": sum(aligner_nll)/len(aligner_nll),
                                "quality": len(accepted)/len(train)}],
                               gold_nll=sum(gold_nll)/len(gold_nll),
                               self_quality=sum(self_correct)/len(self_correct)) if all_complete else None
    empirical["satisfied"]=selection is not None
    # Algorithm 1 starts after aligner selection; a fixed same-family choice may
    # fail finite-sample Eq6. No SFT is executed for an unselected aligner or a
    # candidate pool that includes incomplete output, regardless of its NLL.
    if selection is None:
        raise ExecutionFailure("aligner rejected by complete-response or strict Eq6 constraints; no SFT executed",
            {"rewrites":measurements,"empirical_aligner_constraints":empirical,"cost":ledger.to_dict()})
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
    targets = ([(r["question"], complete_response_tokens(
                    control.tokenizer(r["answer"], add_special_tokens=False).input_ids,eos_token_id=control.tokenizer.eos_token_id))
                for r in train] if variant == "gold-sft" else all_rewrites)
    control_training = [sft_step(control, targets, ledger) for _ in range(epochs)]
    control_metrics = {"acquisition": evaluate(control, acquisition, ledger, max_tokens=max_tokens, seed=seed+10000),
                       "retention": evaluate(control, retention, ledger, max_tokens=max_tokens, seed=seed+20000)}
    return result_payload("synthself", config, seed, split, student, ledger, baseline, after, training,
        parameters_changed=before != student.trainable_digest(), teacher=aligner.provenance,
        execution_status="passed" if selection is not None else "failed-aligner-constraints",
        rewrites=measurements, empirical_aligner_constraints=empirical,
        control={"method": variant, "training": control_training, "metrics": control_metrics},
        limitations=["Qwen2.5-0.5B/7B and GSM8K replace the original multi-domain protocol.",
                     "Retention is a predeclared disjoint math validation slice, not cross-domain capability retention.",
                     "Frozen aligner is configured a priori; finite-sample Eq6 failure is retained.",
                     "LoRA replaces original full fine-tuning; no benchmark gain is claimed."])
