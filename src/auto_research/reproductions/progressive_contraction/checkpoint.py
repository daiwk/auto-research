"""Verified teacher trajectories -> true prefix continuations -> learner NLL routing."""
from __future__ import annotations

import torch

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.post_training.oct13_common import (CostLedger, ExecutionFailure, evaluate, load_policy,
    load_split, result_payload, sample_prefix, sft_step)
from .algorithm import (contract_teacher_pool, monte_carlo_uncertainty, normalized_response_nll,
                        paragraph_prefixes, route_student)


def run(config, *, seed=42):
    train, validation, split = load_split(config)
    ledger, student = CostLedger(), load_policy(config, seed=seed)
    teacher = load_policy(config, role="teacher", seed=seed)
    if student.vocabulary_sha256 != teacher.vocabulary_sha256:
        raise ValueError("same exact vocabulary required for unmodified teacher-token SFT")
    max_tokens = int(config.get("max_tokens", 512))
    attempts = int(config.get("teacher_attempts", 2))
    branches = int(config.get("branches", 4))
    prefix_states = int(config.get("prefix_states", 3))
    epochs = int(config.get("epochs", 3))
    if min(attempts, branches-1, prefix_states, epochs-1) < 1:
        raise ValueError("positive verified-backbone/MCRT budget and >=2 SFT epochs required")
    baseline = evaluate(student, validation, ledger, max_tokens=max_tokens, seed=seed+10000)
    demonstrations, profiles, audits = [], [], []
    delimiter = teacher.tokenizer("\n\n", add_special_tokens=False).input_ids
    for row in train:
        messages = problem_messages("Write reasoning steps separated by blank lines.\n"+row["question"])
        accepted = None
        for _ in range(attempts):
            response = ledger.sample(teacher, messages, role="teacher_backbone", max_tokens=max_tokens)[0]
            if not response.truncated and verified_reward(response.text, row["answer"]):
                accepted = response
                break
        if accepted is None:
            audits.append({"verified_backbone": False})
            continue
        cuts = paragraph_prefixes(accepted.tokens, delimiter, limit=prefix_states)
        if not cuts:
            audits.append({"verified_backbone": True, "profiled": False, "reason": "no reasoning paragraph prefix"})
            continue
        profile = []
        for cut in cuts:
            continuations = sample_prefix(teacher, messages, accepted.tokens[:cut], ledger,
                samples=branches, max_tokens=max_tokens-cut)
            outcomes = [0. if c.truncated else verified_reward(c.text, row["answer"]) for c in continuations]
            profile.append({"prefix_tokens": cut, **monte_carlo_uncertainty(outcomes)})
        demonstrations.append((row["question"], accepted.tokens))
        profiles.append(profile)
        audits.append({"verified_backbone": True, "profiled": True, "profile": profile,
                       "response_tokens": len(accepted.tokens)})
    if not demonstrations:
        raise ExecutionFailure("no verified, paragraph-structured teacher backbone survived",
                               {"teacher_audits": audits, "cost": ledger.to_dict()})
    try:
        pool, teacher_scores = contract_teacher_pool(profiles, float(config.get("pool_ratio", .5)))
    except ValueError as exc:
        raise ExecutionFailure(str(exc), {"teacher_audits": audits, "cost": ledger.to_dict()}) from exc
    active_count = int(config.get("active_size", 1))
    if active_count > len(pool):
        raise ExecutionFailure("requested learner active set exceeds actual teacher pool", {"pool_size": len(pool)})
    torch.manual_seed(seed)
    student.prepare_lora(learning_rate=float(config.get("learning_rate", 1e-5)))
    before = student.trainable_digest()
    pool_demos = [demonstrations[i] for i in pool]
    training = [{"phase": "probing-epoch", **sft_step(student, pool_demos, ledger)}]
    routes = []
    for epoch in range(1, epochs):
        with torch.no_grad():
            losses = [float(normalized_response_nll(ledger.score(student, problem_messages(q), tokens,
                            role="student_routing"))) for q,tokens in pool_demos]
        active = route_student(losses, active_count)
        routes.append({"epoch": epoch+1, "normalized_response_nll": losses, "active_indices": [pool[i] for i in active]})
        training.append({"phase": "routed-epoch", **sft_step(student, [pool_demos[i] for i in active], ledger)})
    after = evaluate(student, validation, ledger, max_tokens=max_tokens, seed=seed+10000)
    control = load_policy(config, seed=seed)
    torch.manual_seed(seed)
    control.prepare_lora(learning_rate=float(config.get("learning_rate", 1e-5)))
    control_training = [sft_step(control, demonstrations, ledger) for _ in range(epochs)]
    control_metrics = evaluate(control, validation, ledger, max_tokens=max_tokens, seed=seed+10000)
    exposures = len(pool)+(epochs-1)*active_count
    return result_payload("progressive-contraction", config, seed, split, student, ledger,
        baseline, after, training, parameters_changed=before != student.trainable_digest(),
        teacher=teacher.provenance, teacher_audits=audits, teacher_uncertainty_scores=teacher_scores,
        teacher_pool_indices=pool, learner_routes=routes,
        exposure={"method": exposures, "full_sft_control": epochs*len(demonstrations),
                  "relative_to_verified_full_sft": exposures/(epochs*len(demonstrations)),
                  "teacher_profiling_cost_excluded_from_ratio_but_reported": True},
        control={"method": "verified-full-sft", "training": control_training, "metrics": control_metrics},
        limitations=["Qwen2.5 and tiny GSM8K train-only public holdout replace the original scale and Qwen3.5 models.",
                     "Actual MCRT sampled continuation costs are reported separately; exposure reduction is not total compute saving.",
                     "Published v1 HTML has missing appendix labels and no retrievable appendix algorithm; main Eqs1-8 are implemented.",
                     "Finite samples and single-seed runtime validation cannot establish original 135x or downstream gains."])
