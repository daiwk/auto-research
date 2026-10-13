"""Current-policy re-estimation controls actual GRPO sample eligibility."""
from __future__ import annotations

import torch

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.post_training.oct13_common import (CostLedger, evaluate, load_policy, load_split,
    policy_gradient_step, result_payload)
from .algorithm import BANDS, PlateauSchedule, band_gate, difficulty_dynamics, success_rate


def run(config, *, seed=42):
    train, validation, split = load_split(config)
    ledger, policy = CostLedger(), load_policy(config, seed=seed)
    max_tokens = int(config.get("max_tokens", 512))
    group = int(config.get("group", 8))
    steps = int(config.get("steps", 3))
    variant = config.get("variant", "fixed-medium")
    if variant not in {"fixed-medium", "staged", "too-hard", "unfiltered", "static"} or min(steps, group-1) < 1:
        raise ValueError("invalid curriculum variant/budget")
    baseline = evaluate(policy, validation, ledger, max_tokens=max_tokens, seed=seed+10000)
    policy.prepare_lora(learning_rate=float(config.get("learning_rate", 1e-5)))
    before = policy.trainable_digest()
    schedule, training, difficulty, initial = PlateauSchedule(), [], [], None
    static_order = None
    best_parameters = None
    for step in range(steps):
        current_rates, groups = [], []
        # Every step re-rolls with the CURRENT policy, including after updates.
        for row in train:
            messages = problem_messages(row["question"])
            responses = ledger.sample(policy, messages, samples=group, max_tokens=max_tokens)
            correctness = [0. if r.truncated else verified_reward(r.text, row["answer"]) for r in responses]
            current_rates.append(success_rate(correctness))
            with torch.no_grad():
                old = [ledger.score(policy, messages, r.tokens, role="behavior").detach() for r in responses]
            groups.append((messages, responses, correctness, old))
        difficulty.append(current_rates)
        if initial is None:
            initial = list(current_rates)
            static_order = sorted(range(len(initial)),key=lambda i:(-initial[i],i))
        band = (BANDS[schedule.stage] if variant == "staged" else
                BANDS[4] if variant == "too-hard" else BANDS[2])
        static_indices = set(static_order[step*len(train)//steps:(step+1)*len(train)//steps])
        audits = []
        for index, (messages, responses, correctness, old) in enumerate(groups):
            eligible = (variant == "unfiltered" or
                        (index in static_indices if variant == "static" else band_gate(correctness, band)))
            if not eligible:
                audits.append({"training_row": index, "eligible": False, "current_success": current_rates[index]})
                continue
            # Auxiliary length reward never affects correctness difficulty/gate.
            shaped = [r + .2 * float(60 <= len(o.tokens) <= 650) for r,o in zip(correctness,responses)]
            update = policy_gradient_step(policy, list(zip([messages]*group, responses)), shaped, ledger,
                                          behavior_log_probs=old, normalize_std=True)
            audits.append({"training_row": index, "eligible": True, "current_success": current_rates[index],
                           "correctness_rewards": correctness, **update})
        diagnostics = evaluate(policy, validation, ledger, max_tokens=max_tokens, seed=seed+10000)
        transition = "not-staged"
        effective_updates=sum(bool(a.get("optimizer_update_executed")) for a in audits)
        if variant == "staged" and effective_updates:
            transition = schedule.observe(diagnostics["accuracy"])
            if transition == "new-best":
                best_parameters = {n:p.detach().clone() for n,p in policy.model.named_parameters() if p.requires_grad}
            elif transition == "advance" and best_parameters is not None:
                with torch.no_grad():
                    for name, parameter in policy.model.named_parameters():
                        if name in best_parameters:
                            parameter.copy_(best_parameters[name])
                # The next stage starts from its selected diagnostic checkpoint.
                policy.optimizer.state.clear()
                best_parameters = None
        elif variant == "staged":
            transition = "no-effective-updates"
        training.append({"step": step+1, "band": band, "groups": audits,
                         "validation_diagnostic": diagnostics, "transition": transition,
                         "effective_updates": effective_updates})
    after = evaluate(policy, validation, ledger, max_tokens=max_tokens, seed=seed+10000)
    return result_payload("grpo-difficulty-curriculum", config, seed, split, policy, ledger,
        baseline, after, training, parameters_changed=before != policy.trainable_digest(),
        variant=variant, difficulty_history=difficulty, difficulty_dynamics=difficulty_dynamics(difficulty),
        initial_static_easy_to_hard_order=static_order if variant=="static" else None,
        execution_status=("passed" if before != policy.trainable_digest() else
                          "passed-negative-control" if variant=="too-hard" else "failed-no-effective-updates"),
        limitations=["Small public train-only GSM8K holdout diagnostic; no official test is read.",
                     "Qwen2.5-0.5B replaces 1.5B and diagnostic cadence is scaled to each bounded step.",
                     "Run fixed-medium/staged/too-hard/unfiltered/static separately with matched configured budgets.",
                     "All rejected groups and calibration generations are charged; no invented nonzero advantage.",
                     "Staged diagnostic uses the validation split, not original 128-per-band training-heldout pools."])
