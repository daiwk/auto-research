"""Bounded PIVOT: shared teacher SFT/OPD warmup, then three resettable arms.

Gold intents are read only by external training rewards/evaluation. Generation
receives a question and the complete domain label list, never its gold intent.
The local prompt uses label names, not unavailable author Banking77 definitions.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json

import torch
from torch.nn import functional as F

from .oct10_checkpoint import _prompt, install_lora, load_public_rows
from .oct11_objectives import pivot_loss
from .pivot_intent import intent_prediction, intent_prompt, intent_reward
from auto_research.public_holdout import validate_holdout


@contextmanager
def frozen_adapter_state(model, state):
    params = dict(model.named_parameters())
    saved = {name: params[name].detach().clone() for name in state}
    try:
        with torch.no_grad():
            for name, value in state.items():
                params[name].copy_(value)
        yield
    finally:
        with torch.no_grad():
            for name, value in saved.items():
                params[name].copy_(value)


def sample(model, tokenizer, prompt, *, group, max_tokens, device, stochastic=True):
    prefix = _prompt(tokenizer, prompt, device)
    kwargs = {"do_sample": stochastic}
    vocabulary = getattr(model, "pivot_vocabulary_size", model.config.vocab_size)
    if vocabulary < model.config.vocab_size:
        kwargs["suppress_tokens"] = list(range(vocabulary, model.config.vocab_size))
    if stochastic:
        kwargs.update(temperature=1., top_p=.9, top_k=50)
    with torch.no_grad():
        ids = model.generate(prefix, attention_mask=torch.ones_like(prefix), num_return_sequences=group,
                             max_new_tokens=max_tokens, pad_token_id=tokenizer.pad_token_id, use_cache=True, **kwargs)
    response = ids[:, prefix.shape[1]:]
    mask = torch.ones_like(response, dtype=torch.bool)
    complete = []
    for row in range(len(ids)):
        eos = torch.where(response[row] == tokenizer.eos_token_id)[0]
        complete.append(bool(len(eos)))
        if len(eos):
            mask[row, int(eos[0]) + 1:] = False
    texts = tokenizer.batch_decode(response, skip_special_tokens=True)
    return {"ids": ids, "start": prefix.shape[1] - 1, "actions": response,
            "mask": mask, "texts": texts, "ended_with_eos": complete}


def response_logits(model, bank):
    # Slice before FP32 conversion: do not retain full-vocabulary prompt logits.
    output = model(bank["ids"], use_cache=False).logits
    # Qwen2.5 sizes pad projection rows differently. Use every token in the
    # verified IDENTICAL tokenizer vocabulary; discard only unnamed pad rows.
    vocabulary = getattr(model, "pivot_vocabulary_size", output.shape[-1])
    return output[:, bank["start"]:-1, :vocabulary].float()


def padded_stack(banks, values, *, is_logits=False):
    length = max(bank["mask"].shape[1] for bank in banks)
    return torch.stack([F.pad(value, (0, 0, 0, length - value.shape[-2])) if is_logits
                        else F.pad(value, (0, length - value.shape[-1]))
                        for value in values])


def optimization_step(student, teacher, tokenizer, batch, labels, optimizer, reference,
                      *, step, total_steps, group, max_tokens, device, recipe):
    banks = [sample(student, tokenizer, intent_prompt(row["question"], labels), group=group,
                    max_tokens=max_tokens, device=device) for row in batch]
    with torch.no_grad():
        old = [response_logits(student, b).log_softmax(-1).gather(-1, b["actions"][..., None]).squeeze(-1)
               for b in banks]
        teacher_values = [response_logits(teacher, b) for b in banks]
        with frozen_adapter_state(student, reference):
            refs = [response_logits(student, b) for b in banks]
    current = [response_logits(student, b) for b in banks]
    rewards = torch.tensor([[intent_reward(text, row["answer"], labels)[0] for text in b["texts"]]
                            for row, b in zip(batch, banks)], device=device)
    mask = padded_stack(banks, [b["mask"] for b in banks])
    route_step = 0 if recipe == "opd" else total_steps if recipe == "global" and step > total_steps // 2 else 0
    if recipe == "pivot":
        route_step = step
    loss, stats = pivot_loss(padded_stack(banks, current, is_logits=True),
                            padded_stack(banks, teacher_values, is_logits=True),
                            padded_stack(banks, [b["actions"] for b in banks]), padded_stack(banks, old), rewards, mask,
                            step=route_step, total_steps=total_steps,
                            reference_logits=padded_stack(banks, refs, is_logits=True), kl_beta=.001)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    norm = float(torch.nn.utils.clip_grad_norm_([p for p in student.parameters() if p.requires_grad], 1.))
    # A pure GRPO batch with identical rewards and no KL displacement may be
    # inactive. No reward editing is allowed to manufacture an update.
    active = norm > 0
    if active:
        optimizer.step()
    record = {"step": step, "recipe": recipe, "loss": float(loss.detach()), "gradient_l2": norm,
              "active": active, "rewards": rewards.tolist(), "response_tokens": int(mask.sum()),
              "routed_grpo": stats["routed_grpo"].tolist(), "cosine_ratio": stats["cosine_ratio"],
              "acquisition_scores": stats["acquisition_scores"].tolist(),
              "truncated_rollouts": sum(not eos for b in banks for eos in b["ended_with_eos"])}
    print(json.dumps(record), flush=True)
    return record


def evaluate(model, tokenizer, rows, labels, *, max_tokens, device):
    outcomes = []
    for row in rows:
        bank = sample(model, tokenizer, intent_prompt(row["question"], labels), group=1,
                      max_tokens=max_tokens, device=device, stochastic=False)
        prediction = intent_prediction(bank["texts"][0], labels)
        outcomes.append({"correct": prediction == row["answer"], "valid_prediction": prediction is not None,
                         "ended_with_eos": bank["ended_with_eos"][0], "tokens": int(bank["mask"].sum())})
    return {"accuracy": sum(r["correct"] for r in outcomes) / len(rows),
            "parse_rate": sum(r["valid_prediction"] for r in outcomes) / len(rows), "examples": len(rows),
            "eos_completion_fraction": sum(r["ended_with_eos"] for r in outcomes) / len(rows), "rows": outcomes}


def run(*, student_path, teacher_path, student_id, student_revision, teacher_id, teacher_revision,
        train_path, validation_path, split_manifest, dataset_revision, output, seed=42,
        training_examples=8, validation_examples=8, steps=8, warmup_steps=2, sft_epochs=2,
        batch_size=2, group=2, max_tokens=256, device="cuda"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if min(training_examples, validation_examples, steps, warmup_steps, sft_epochs, max_tokens) < 1 or min(batch_size, group) < 2:
        raise ValueError("positive warmup/training budgets and multiple prompts/rollouts required")
    split = validate_holdout(split_manifest, train_path, validation_path, dataset_revision=dataset_revision)
    if not split["verified"]:
        raise ValueError("verified train-only intent split required")
    record = json.loads(split_manifest.read_text())
    labels = record["partition"]["labels"]
    train = load_public_rows(train_path)[:training_examples]
    valid = load_public_rows(validation_path)[:validation_examples]
    if len(train) < batch_size or any(r["answer"] not in labels for r in train + valid):
        raise ValueError("valid full-domain labels and sufficient training examples required")
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(student_path, local_files_only=True)
    teacher_tokenizer = AutoTokenizer.from_pretrained(teacher_path, local_files_only=True)
    if tokenizer.get_vocab() != teacher_tokenizer.get_vocab():
        raise ValueError("teacher/student token identity must match")
    token_ids = set(tokenizer.get_vocab().values())
    vocabulary = max(token_ids) + 1
    if token_ids != set(range(vocabulary)):
        raise ValueError("noncontiguous token identity needs explicit mapping; not silently cropped")
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
    models = [AutoModelForCausalLM.from_pretrained(path, local_files_only=True, dtype=dtype,
              attn_implementation="eager").to(device).eval() for path in (student_path, teacher_path)]
    student, teacher = models
    for model in models:
        if model.config.vocab_size < vocabulary:
            raise ValueError("model projection omits a tokenizer-defined token")
        model.pivot_vocabulary_size = vocabulary
    teacher.requires_grad_(False)
    install_lora(student)
    parameters = {name: p for name, p in student.named_parameters() if p.requires_grad}
    optimizer = torch.optim.AdamW(parameters.values(), lr=1e-5, weight_decay=0.)
    initial = {name: p.detach().clone() for name, p in parameters.items()}
    base_metrics = evaluate(student, tokenizer, valid, labels, max_tokens=max_tokens, device=device)
    # Teacher responses on TRAIN questions only; same targets for all arms.
    targets = [sample(teacher, tokenizer, intent_prompt(row["question"], labels), group=1,
                      max_tokens=max_tokens, device=device, stochastic=False) for row in train]
    sft = []
    for epoch in range(sft_epochs):
        for index, bank in enumerate(targets):
            logits = response_logits(student, bank)
            loss = F.cross_entropy(logits[bank["mask"]], bank["actions"][bank["mask"]])
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            norm = float(torch.nn.utils.clip_grad_norm_(parameters.values(), 1.))
            optimizer.step()
            sft.append({"epoch": epoch, "example": index, "loss": float(loss.detach()), "gradient_l2": norm,
                        "teacher_ended_with_eos": bank["ended_with_eos"][0]})
    warmup = [optimization_step(student, teacher, tokenizer,
              [train[(step * batch_size + i) % len(train)] for i in range(batch_size)], labels, optimizer, initial,
              step=step, total_steps=warmup_steps, group=group, max_tokens=max_tokens, device=device, recipe="opd")
              for step in range(warmup_steps)]
    shared = {name: p.detach().clone() for name, p in parameters.items()}
    shared_metrics = evaluate(student, tokenizer, valid, labels, max_tokens=max_tokens, device=device)
    arms = []
    for recipe in ("opd", "global", "pivot"):
        with torch.no_grad():
            for name, p in parameters.items():
                p.copy_(shared[name])
        torch.manual_seed(seed)
        optimizer = torch.optim.AdamW(parameters.values(), lr=1e-6, weight_decay=0.)
        history = [optimization_step(student, teacher, tokenizer,
                   [train[((step - 1) * batch_size + i) % len(train)] for i in range(batch_size)],
                   labels, optimizer, shared, step=step, total_steps=steps, group=group,
                   max_tokens=max_tokens, device=device, recipe=recipe) for step in range(1, steps + 1)]
        delta = sum(float((p.detach() - shared[name]).square().sum()) for name, p in parameters.items()) ** .5
        arms.append({"recipe": recipe, "history": history, "adapter_delta_l2": delta,
                     "validation": evaluate(student, tokenizer, valid, labels, max_tokens=max_tokens, device=device)})
    report = {"schema_version": 1, "adapter_key": "pivot", "diagnostic_only": True,
              "evaluation_tier": "l1_mechanism", "seed": seed, "student": {"id": student_id, "revision": student_revision},
              "teacher": {"id": teacher_id, "revision": teacher_revision}, "split_provenance": split, "test_read": False,
              "dataset": {"id": split["source_id"], "revision": dataset_revision,
                          "train_sha256": hashlib.sha256(train_path.read_bytes()).hexdigest(),
                          "validation_sha256": hashlib.sha256(validation_path.read_bytes()).hexdigest()},
              "budgets": {"training_examples": len(train), "validation_examples": len(valid), "steps": steps,
                          "warmup_steps": warmup_steps, "sft_epochs": sft_epochs, "group": group,
                          "batch_size": batch_size, "max_tokens": max_tokens},
              "baseline": base_metrics, "shared_warmup_validation": shared_metrics,
              "sft_history": sft, "opd_warmup_history": warmup, "arms": arms,
              "protocol": {"shared_warmup_and_reset": True, "full_vocabulary_kl": True, "kl_beta": .001,
                           "vocabulary": "entire identical tokenizer vocabulary; unnamed projection padding suppressed",
                           "reference": "frozen shared warmup adapters", "finetuning": "q/v LoRA, not full",
                           "prompt": "77-label-only, no unavailable author intent definitions",
                           "global_switch": "fixed half-budget, never selected on test",
                           "learning_rate": "all post-warmup arms 1e-6", "validation_selection": False}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return report
