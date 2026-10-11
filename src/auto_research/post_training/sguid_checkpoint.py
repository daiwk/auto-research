"""Bounded, real checkpoint SGUID with a live self-distillation teacher.

Skills come from the current student's verified training rollouts. Neither skill
retrieval nor student/evaluation prompts receive reference answers. The same
model scores privileged skill prompts under no_grad, so teacher weights remain
synchronized without a separate optimizer or checkpoint.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path

import torch

from auto_research.public_holdout import validate_holdout
from .oct10_checkpoint import install_lora, load_public_rows, verified_reward
from .oct11_objectives import SkillActivity, select_sguid_skills, sguid_coefficient

EXECUTED_SOURCES = (
    "src/auto_research/post_training/sguid_checkpoint.py", "scripts/run_sguid_checkpoint.py",
    "src/auto_research/post_training/oct11_objectives.py",
    "src/auto_research/post_training/oct10_checkpoint.py", "src/auto_research/public_holdout.py",
)


def curation_prompt(question, response, reference, correct):
    return (
        "Extract one reusable mathematical skill from this VERIFIED TRAINING example. "
        "This is offline skill curation, not evaluation. Return only a JSON object "
        'with string keys "title" and "principle". Describe a general procedure or '
        "failure mode; do not copy the example's names, numbers or final answer.\n"
        f"Question: {question}\nStudent rollout: {response}\n"
        f"Verifier correct: {bool(correct)}\nTraining reference: {reference}\n"
    )


def parse_skill(text):
    """Accept generated JSON only; never manufacture a skill on parse failure."""
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            item, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if (isinstance(item, dict) and all(isinstance(item.get(k), str)
                and item[k].strip() for k in ("title", "principle"))):
            if len(item["title"]) <= 160 and 20 <= len(item["principle"]) <= 2000:
                return {k: item[k].strip() for k in ("title", "principle")}
    raise ValueError("generated response contains no valid skill JSON")


def skill_teacher_prompt(question, skill):
    """Privileged training context contains a skill, never a gold solution."""
    return (f"Use this reusable mathematical guidance when relevant:\n"
            f"{skill['title']}: {skill['principle']}\n\nQuestion: {question}")


def snapshot_adapters(model):
    return {name: p.detach().clone() for name, p in model.named_parameters() if p.requires_grad}


def restore_adapters(model, snapshot):
    parameters = dict(model.named_parameters())
    with torch.no_grad():
        for name, value in snapshot.items():
            parameters[name].copy_(value)


def adapter_digest(snapshot):
    digest = hashlib.sha256()
    for name, value in sorted(snapshot.items()):
        digest.update(name.encode())
        digest.update(value.detach().float().cpu().numpy().tobytes())
    return digest.hexdigest()


def adapter_distance(model, snapshot):
    return sum(float((p.detach() - snapshot[name]).square().sum())
               for name, p in model.named_parameters() if name in snapshot) ** .5


def step_if_finite_nonzero_gradient(parameters, optimizer, *, max_norm=.1):
    """A nonzero gate is not proof of an actual parameter update.

    Check the measured gradient before advancing AdamW moments. A nonfinite
    gradient is a hard failure, not a silently skipped or successful update.
    """
    norm = torch.nn.utils.clip_grad_norm_(parameters, max_norm, error_if_nonfinite=True)
    gradient = float(norm)
    active = gradient > 0
    if active:
        optimizer.step()
    return gradient, active


def co_evolve(model, training_rows, *, curate, distill, rounds=2, counts=(6, 3),
              late_minimum=2, tau=5.0, journal=None):
    """Restart adapters AND fresh optimizer after each probe; re-curate next round.

    Curate and distill receive training rows only. Failures retain the generated
    bank/activity log and restore the round base; no fallback or padded counts.
    """
    if rounds < 1 or len(counts) < rounds:
        raise ValueError("positive rounds and one compact-bank size per round required")
    records = []
    for r in range(rounds):
        initial = snapshot_adapters(model)
        record = {"round": r, "round_base_sha256": adapter_digest(initial)}
        records.append(record)
        bank, curation = curate(model, training_rows, r)
        record.update(candidate_bank=bank, curation=curation)
        if not bank:
            record.update(status="failed", failure="student-generated skill bank is empty")
            if journal:
                journal(records)
            return records
        try:
            activities, probe = distill(model, training_rows, bank, True, r)
            record.update(probe=probe, activities={k: asdict(v) for k, v in activities.items()},
                          probe_parameter_delta_l2=adapter_distance(model, initial))
            selected = select_sguid_skills(activities, count=counts[r],
                                          late_minimum=late_minimum, tau=tau)
            if any(key not in bank for key in activities):
                raise ValueError("activity refers to a skill outside the generated candidate bank")
        except Exception as exc:
            record.update(status="failed", failure=f"probe error: {type(exc).__name__}: {exc}")
            raise
        finally:
            restore_adapters(model, initial)
            record["restored_sha256"] = adapter_digest(snapshot_adapters(model))
            if journal:
                journal(records)
        record.update(restored_sha256=adapter_digest(snapshot_adapters(model)),
                      selected_skills=list(selected))
        if not selected:
            record.update(status="failed", failure="no skills passed the persistence criterion")
            if journal:
                journal(records)
            return records
        compact = {key: bank[key] for key in selected}
        _, internalization = distill(model, training_rows, compact, False, r)
        record.update(internalization=internalization, status="completed",
                      internalization_parameter_delta_l2=adapter_distance(model, initial),
                      next_policy_sha256=adapter_digest(snapshot_adapters(model)))
        if journal:
            journal(records)
    return records


def signed_forward_kl(student_logits, teacher_logits, actions, relevant_mask, correct,
                      *, kappa=.05, gap_clip=3.):
    """Eq. 9's generalized full-vocabulary forward KL with frozen signed gate."""
    if student_logits.shape != teacher_logits.shape or actions.shape != relevant_mask.shape:
        raise ValueError("aligned response distributions/actions/masks required")
    s = student_logits.float().log_softmax(-1)
    t = teacher_logits.detach().float().log_softmax(-1)
    slp = s.gather(-1, actions[..., None]).squeeze(-1)
    tlp = t.gather(-1, actions[..., None]).squeeze(-1)
    c, support = sguid_coefficient(tlp, slp, relevant_mask, correct,
                                  kappa=kappa, gap_clip=gap_clip)
    kl = (t.exp() * (t - s)).sum(-1).masked_fill(~relevant_mask, 0)
    per_response = kl.sum(-1) / relevant_mask.sum(-1)
    return (c.detach() * per_response).mean(), c, support


def thinking_template_audit(tokenizer):
    """Inspect the rendered protocol, not whether a tokenizer accepts a kwarg.

    Non-thinking-only Instruct templates may silently ignore enable_thinking.
    Fail closed unless the actual prefixes switch from an explicitly closed
    thinking block to an open block. This is a prompt-protocol check, not proof
    that generated reasoning is correct or that a response avoids truncation.
    """
    prefixes = {}
    for enabled in (False, True):
        text = tokenizer.apply_chat_template(
            [{"role": "user", "content": "Solve 2 plus 3."}], tokenize=False,
            add_generation_prompt=True, enable_thinking=enabled)
        prefixes["enabled" if enabled else "disabled"] = text
    supported = (prefixes["enabled"] != prefixes["disabled"]
                 and prefixes["enabled"].rstrip().endswith("<think>")
                 and prefixes["disabled"].rstrip().endswith("</think>"))
    return {"probe_question": "Solve 2 plus 3.", "supported": supported,
            "rendered_prefixes": prefixes,
            "rendered_prefix_sha256": {key: hashlib.sha256(text.encode()).hexdigest()
                                       for key, text in prefixes.items()},
            "requested": {"student": False, "teacher": True, "evaluation": True},
            "effective": {"student": False, "teacher": True, "evaluation": True}
                         if supported else None}


def _load_checkpoint(checkpoint_path, dtype, device):
    from transformers import AutoConfig, AutoModelForCausalLM

    config = AutoConfig.from_pretrained(checkpoint_path, local_files_only=True)
    if config.model_type == "qwen3_5":
        from transformers import Qwen3_5ForConditionalGeneration
        cls = Qwen3_5ForConditionalGeneration
    elif config.model_type == "qwen3":
        cls = AutoModelForCausalLM
    else:
        raise ValueError("SGUID supports audited Qwen3 or Qwen3.5 text-only checkpoints")
    model = cls.from_pretrained(checkpoint_path, local_files_only=True,
                               dtype=dtype, attn_implementation="eager").to(device).eval()
    return model, {"model_type": config.model_type, "loaded_class": type(model).__name__,
                   "input_modality": "text only; vision weights frozen and unused"}


def _language_backbone(model):
    # Qwen3.5 is a multimodal wrapper with a hybrid text decoder. Do not run
    # the vision branch or replace hybrid layers with a Qwen3 approximation.
    return getattr(model.model, "language_model", model.model)


def _prefix(tokenizer, text, device, *, thinking=False):
    rendered = tokenizer.apply_chat_template(
        [{"role": "user", "content": text}], tokenize=False,
        add_generation_prompt=True, enable_thinking=thinking)
    return tokenizer(rendered, return_tensors="pt").input_ids.to(device)


def _generate(model, tokenizer, text, device, max_tokens, *, sample=True, thinking=False):
    prefix = _prefix(tokenizer, text, device, thinking=thinking)
    kwargs = {"temperature": 1.1, "top_p": .95, "top_k": 20} if sample else {}
    with torch.no_grad():
        ids = model.generate(prefix, attention_mask=torch.ones_like(prefix),
                             max_new_tokens=max_tokens, do_sample=sample,
                             pad_token_id=tokenizer.pad_token_id, **kwargs)
    response = ids[:, prefix.shape[1]:]
    eos = torch.where(response[0] == tokenizer.eos_token_id)[0]
    if len(eos):
        response = response[:, :int(eos[0]) + 1]
    return prefix, response, tokenizer.decode(response[0], skip_special_tokens=True), bool(len(eos))


def _response_logits(model, prefix, response):
    ids = torch.cat((prefix, response), dim=-1)
    # Exclude prefix distributions, preserving the first response prediction.
    return model(input_ids=ids, use_cache=False).logits[:, prefix.shape[1] - 1:-1]


def _embedding(model, tokenizer, text, device):
    tokens = tokenizer(text, return_tensors="pt").input_ids.to(device)
    with torch.no_grad():
        hidden = _language_backbone(model)(input_ids=tokens, use_cache=False).last_hidden_state
        vector = hidden.float().mean(1)[0]
    return torch.nn.functional.normalize(vector, dim=0)


def run(*, checkpoint_path, checkpoint_id, checkpoint_revision, train_path,
        validation_path, dataset_revision, split_manifest, output, seed=42,
        training_examples=8, validation_examples=8, rounds=2, probe_steps=8,
        internalization_steps=8, max_tokens=512, skill_tokens=256,
        candidate_count=8, retrieve_count=6, late_minimum=2, device="cuda"):
    from transformers import AutoTokenizer

    if (rounds != 2 or min(training_examples, validation_examples, probe_steps,
            internalization_steps, max_tokens, skill_tokens, candidate_count,
            retrieve_count, late_minimum) < 1 or probe_steps < 4):
        raise ValueError("two rounds, nonzero budgets and at least four probe steps required")
    split = validate_holdout(split_manifest, train_path, validation_path,
                             dataset_revision=dataset_revision)
    if not split["verified"] or not checkpoint_revision:
        raise ValueError("immutable checkpoint and verified train-only holdout required")
    train = load_public_rows(train_path)[:training_examples]
    valid = load_public_rows(validation_path)[:validation_examples]
    torch.manual_seed(seed)
    dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_path, local_files_only=True)
    if not tokenizer.chat_template:
        raise ValueError("SGUID runner requires a thinking-aware public chat tokenizer")
    thinking_audit = thinking_template_audit(tokenizer)
    if not thinking_audit["supported"]:
        raise ValueError("actual chat template does not switch thinking mode; "
                         "enable_thinking kwargs alone are not evidence")
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    model, backbone = _load_checkpoint(checkpoint_path, dtype, device)
    model.requires_grad_(False)
    lora_modules = install_lora(_language_backbone(model), rank=8)
    initial = snapshot_adapters(model)
    parameters = [p for p in model.parameters() if p.requires_grad]

    def evaluate():
        correct, eos = 0, 0
        for row in valid:
            _, _, text, finished = _generate(model, tokenizer, row["question"], device,
                                             max_tokens, sample=False, thinking=True)
            correct += verified_reward(text, row["answer"])
            eos += finished
        return {"examples": len(valid), "exact_match": correct / len(valid),
                "eos_completed": eos, "truncated": len(valid) - eos}

    baseline = evaluate()

    def curate(current, rows, round_index):
        bank, records, seen = {}, [], set()
        policy_sha = adapter_digest(snapshot_adapters(current))
        for index, row in enumerate(rows[:candidate_count]):
            _, _, response, finished = _generate(current, tokenizer, row["question"],
                                                 device, max_tokens)
            correct = verified_reward(response, row["answer"])
            prompt = curation_prompt(row["question"], response, row["answer"], correct)
            _, _, text, skill_finished = _generate(current, tokenizer, prompt, device,
                                                  skill_tokens, sample=False)
            item = {"training_index": index, "rollout_correct": bool(correct),
                    "student_policy_sha256": policy_sha,
                    "rollout_eos": finished, "skill_eos": skill_finished,
                    "student_rollout": response, "generated_skill_response": text,
                    "student_rollout_sha256": hashlib.sha256(response.encode()).hexdigest(),
                    "generated_skill_sha256": hashlib.sha256(text.encode()).hexdigest()}
            try:
                skill = parse_skill(text)
                key = f"r{round_index}-s{index}"
                canonical = json.dumps(skill, sort_keys=True)
                if canonical not in seen:
                    bank[key] = skill
                    seen.add(canonical)
                    item["accepted_skill"] = key
                else:
                    item["rejection"] = "duplicate generated skill"
            except ValueError as exc:
                item["rejection"] = str(exc)
            records.append(item)
        return bank, records

    def distill(current, rows, bank, collect_activity, round_index):
        # Fresh optimizer: no probe momentum leaks into compact-bank restart.
        optimizer = torch.optim.AdamW(parameters, lr=5e-6, weight_decay=0)
        activities = {key: SkillActivity() for key in bank}
        vectors = {key: _embedding(current, tokenizer, f"{s['title']}: {s['principle']}", device)
                   for key, s in bank.items()}
        steps = probe_steps if collect_activity else internalization_steps
        history = []
        for step in range(steps):
            policy_before = adapter_digest(snapshot_adapters(current))
            row = rows[step % len(rows)]
            query = _embedding(current, tokenizer, row["question"], device)
            keys = sorted(bank, key=lambda key: (-float(query @ vectors[key]), key))[:retrieve_count]
            prefix, response, text, finished = _generate(current, tokenizer, row["question"],
                                                       device, max_tokens)
            correct = torch.tensor([bool(verified_reward(text, row["answer"]))], device=device)
            mask = torch.ones_like(response, dtype=torch.bool)
            for special in tokenizer.all_special_ids:
                mask &= response != special
            if not bool(mask.any()):
                raise ValueError("rollout has no relevant nonspecial response tokens")
            optimizer.zero_grad(set_to_none=True)
            events, loss_value = [], 0.
            for key in keys:
                teacher_prefix = _prefix(tokenizer, skill_teacher_prompt(row["question"], bank[key]),
                                          device, thinking=True)
                # Same current theta, privileged context, no teacher gradient.
                with torch.no_grad():
                    teacher_logits = _response_logits(current, teacher_prefix, response)
                student_logits = _response_logits(current, prefix, response)
                loss, coefficient, support = signed_forward_kl(student_logits, teacher_logits,
                                                               response, mask, correct)
                signed = float(coefficient[0])
                if collect_activity:
                    activities[key].record(early=step < steps // 2, coefficient=signed)
                if signed:
                    (loss / len(keys)).backward()
                loss_value += float(loss.detach()) / len(keys)
                events.append({"skill": key, "coefficient": signed, "support": float(support[0]),
                               "full_vocabulary_size": student_logits.shape[-1],
                               "teacher_requires_grad": teacher_logits.requires_grad,
                               "student_requires_grad": student_logits.requires_grad})
                del teacher_logits, student_logits, loss
            nonzero_gates = sum(e["coefficient"] != 0 for e in events)
            gradient, active = step_if_finite_nonzero_gradient(parameters, optimizer)
            item = {"step": step, "training_index": step % len(rows), "early": step < steps // 2,
                    "policy_sha256_before": policy_before,
                    "policy_sha256_after": adapter_digest(snapshot_adapters(current)),
                    "correct": bool(correct[0]), "eos_completed": finished,
                    "response_tokens": response.numel(), "active_update": active,
                    "gate_nonzero_skills": nonzero_gates,
                    "loss": loss_value, "gradient_l2": gradient, "events": events}
            history.append(item)
            print(json.dumps({"round": round_index, "probe": collect_activity, **item},
                             allow_nan=False), flush=True)
        return activities, history

    payload = {"schema_version": 1, "adapter_key": "sguid", "seed": seed,
               "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
               "checkpoint": {"id": checkpoint_id, "revision": checkpoint_revision},
               "dataset": {"id": split["source_id"], "revision": dataset_revision},
               "split_provenance": split, "test_read": False,
               "validation_used_for_selection": False, "baseline": baseline,
               "accelerator": {"vendor": "NVIDIA" if device.startswith("cuda") else "CPU",
                   "model": torch.cuda.get_device_name(device) if device.startswith("cuda") else "CPU"},
               "executed_source_sha256": {relative: hashlib.sha256(
                   (Path(__file__).resolve().parents[3] / relative).read_bytes()).hexdigest()
                   for relative in EXECUTED_SOURCES},
               "protocol": {"rounds": rounds, "training_examples": len(train),
                   "probe_steps": probe_steps, "internalization_steps": internalization_steps,
                   "max_tokens": max_tokens, "skill_tokens": skill_tokens,
                   "candidate_count": candidate_count, "retrieve_count": retrieve_count,
                   "kappa": .05, "gap_clip": 3., "tau": 5., "late_minimum": late_minimum,
                   "compact_counts": [6, 3], "teacher": "live synchronized same-model no_grad",
                   "full_vocabulary_size": model.get_output_embeddings().out_features,
                   "logits_projection": "full model output vocabulary; no top-k approximation",
                   "retriever": "current LM mean last hidden-state cosine; not Qwen3-Embedding-0.6B",
                   "loss": "signed generalized full-vocabulary forward KL",
                   "adapter": "q/v rank-8 FP32 LoRA; not original all-linear rank-64 LoRA",
                   "adapter_module_count": lora_modules, "backbone": backbone,
                   "thinking_template_audit": thinking_audit,
                   "gold_role": "training verifier/curation only; absent from student and retrieval",
                   "student_thinking": thinking_audit["effective"]["student"],
                   "teacher_thinking": thinking_audit["effective"]["teacher"],
                   "evaluation_thinking": thinking_audit["effective"]["evaluation"]}}

    def write(records):
        payload["rounds"] = records
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")

    records = co_evolve(model, train, curate=curate, distill=distill, rounds=rounds,
                        late_minimum=late_minimum, journal=write)
    payload.update(status="completed" if all(r["status"] == "completed" for r in records) else "failed",
                   final_validation=evaluate(),
                   adapter_parameter_delta_l2=adapter_distance(model, initial))
    write(records)
    return payload
