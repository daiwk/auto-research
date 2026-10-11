"""Bounded real-checkpoint ZCPO runtime validation, with external numeric reward.

There is no reward fabrication to force a nonzero update. Equal-reward groups
can legitimately skip every update; the report then records no active evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import torch

from .oct10_checkpoint import _logits, _prompt, _sample, install_lora, load_public_rows, verified_reward
from .oct11_objectives import zcpo_loss
from auto_research.public_holdout import validate_holdout


def run_zcpo(*, checkpoint_path, checkpoint_id, checkpoint_revision, train_path,
             validation_path, dataset_revision, output, steps=8, seed=42,
             max_tokens=128, group=4, validation_examples=8, device="cuda", split_manifest=None):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if min(steps, max_tokens, validation_examples) < 1 or group < 2:
        raise ValueError("positive budget and multiple rollouts required")
    if not checkpoint_revision or not dataset_revision:
        raise ValueError("immutable public model/data revisions required")
    split = validate_holdout(split_manifest, train_path, validation_path, dataset_revision=dataset_revision)
    train, valid = load_public_rows(train_path), load_public_rows(validation_path)
    if {r["question"] for r in train} & {r["question"] for r in valid}:
        raise ValueError("train/validation overlap")
    torch.manual_seed(seed)
    dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_path, local_files_only=True)
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(checkpoint_path, local_files_only=True,
                dtype=dtype, attn_implementation="eager").to(device).eval()
    install_lora(model)
    params = [p for p in model.parameters() if p.requires_grad]
    initial = {n: p.detach().clone() for n, p in model.named_parameters() if p.requires_grad}
    optimizer = torch.optim.AdamW(params, lr=1e-5, weight_decay=0)
    history = []
    for step in range(steps):
        row = train[step % len(train)]
        ids, mask, texts = _sample(model, tokenizer, row["question"], device, group, max_tokens)
        with torch.no_grad():
            old_logits = _logits(model, ids)
            old = old_logits.log_softmax(-1).gather(-1, ids[:, 1:, None]).squeeze(-1)
            # Disabling only LoRA B matrices recovers the exact frozen initial
            # reference without loading a second copy or sharing mutable adapters.
            saved_b = {n: p.detach().clone() for n, p in model.named_parameters()
                       if n.endswith(".b") and p.requires_grad}
            try:
                for n, p in model.named_parameters():
                    if n in saved_b:
                        p.zero_()
                reference = _logits(model, ids)
            finally:
                for n, p in model.named_parameters():
                    if n in saved_b:
                        p.copy_(saved_b[n])
        rewards = torch.tensor([verified_reward(t, row["answer"]) for t in texts], device=device)
        logits = _logits(model, ids)
        logp = logits.log_softmax(-1).gather(-1, ids[:, 1:, None]).squeeze(-1)
        loss, stats = zcpo_loss(logp, old, logits, reference, rewards, mask)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        gradient = float(torch.nn.utils.clip_grad_norm_(params, 1.))
        # An inactive group must not advance AdamW's moments or weight decay.
        if stats["active"]:
            optimizer.step()
        item = {"step": step, "rewards": rewards.tolist(), "loss": float(loss.detach()),
                "gradient_l2": gradient, "response_tokens": int(mask.sum()), **stats}
        history.append(item)
        print(json.dumps(item), flush=True)
        del logits, logp, reference, old_logits, old, loss
    correct = 0
    for row in valid[:validation_examples]:
        prompt = _prompt(tokenizer, row["question"], device)
        with torch.no_grad():
            ids = model.generate(prompt, attention_mask=torch.ones_like(prompt), max_new_tokens=max_tokens,
                                 do_sample=False, pad_token_id=tokenizer.pad_token_id)
        text = tokenizer.decode(ids[0, prompt.shape[1]:], skip_special_tokens=True)
        correct += verified_reward(text, row["answer"])
    n = min(len(valid), validation_examples)
    delta = sum(float((p.detach() - initial[name]).square().sum())
                for name, p in model.named_parameters() if name in initial)**.5
    payload = {"schema_version": 1, "adapter_key": "zcpo", "seed": seed,
               "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
               "claim_scope": "bounded real checkpoint runtime validation, not benchmark gains",
               "checkpoint": {"id": checkpoint_id, "revision": checkpoint_revision},
               "dataset": {"id": "openai/grade-school-math", "revision": dataset_revision,
                           "train_sha256": hashlib.sha256(train_path.read_bytes()).hexdigest(),
                           "validation_sha256": hashlib.sha256(validation_path.read_bytes()).hexdigest()},
               "metrics": {"active_groups": sum(r["active"] for r in history),
                           "adapter_parameter_delta_l2": delta,
                           "validation_examples": n, "validation_exact_match": correct / n},
               "history": history, "split_provenance": split, "test_read": split["test_read"],
               "validation_used_for_selection": False}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")
    return payload
