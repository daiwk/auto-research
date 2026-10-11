#!/usr/bin/env python3
"""Real checkpoint OPD diagnostics; no claimed reproduction of 200-step plateaus."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from auto_research.post_training.learning_signals import (
    cross_fitted_occupancy, learning_signal_proxy, linear_cka, mean_pool_prompt,
    occupancy_surrogate, parameter_displacement, topk_residual,
)
from auto_research.post_training.oct10_checkpoint import _logits, _prompt, _sample, install_lora, load_public_rows
from auto_research.public_holdout import validate_holdout


def features(model, inputs):
    rows = []
    for ids in inputs:
        with torch.no_grad():
            hidden = model(ids, use_cache=False, output_hidden_states=True).hidden_states
        pooled = [mean_pool_prompt(h, torch.ones_like(ids, dtype=torch.bool))[0].cpu() for h in hidden]
        rows.append(torch.stack(pooled))
    return torch.stack(rows).transpose(0, 1)


def response_statistics(current, target, old, ids, mask):
    logp, teacher = current.log_softmax(-1), target.detach().log_softmax(-1)
    old_logp = old.detach().log_softmax(-1)
    values, selected = old_logp.topk(16, -1)
    gaps = (values - teacher.gather(-1, selected)).detach()
    weights = values.softmax(-1).detach()
    residual = (weights * gaps).sum(-1)
    # Frozen support/advantage policy surrogate, as the training actor. The
    # logged residual is separate and can be negative under truncated support.
    ratio = (logp.gather(-1, selected) - values).exp()
    surrogate = (weights * gaps * ratio).sum(-1)
    lengths = mask.sum(-1)
    per_response = residual.masked_fill(~mask, 0).sum(-1) / lengths
    policy = surrogate.masked_fill(~mask, 0).sum(-1) / lengths
    seq_logp = logp.gather(-1, ids[:, 1:, None]).squeeze(-1).masked_fill(~mask, 0).sum(-1)
    return per_response, policy, seq_logp


def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    p = argparse.ArgumentParser(description=__doc__)
    for name in ("student-path", "teacher-path", "train-path", "validation-path", "split-manifest", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    for name in ("student-id", "student-revision", "teacher-id", "teacher-revision", "dataset-revision"):
        p.add_argument("--" + name, required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=3)
    p.add_argument("--max-tokens", type=int, default=128)
    p.add_argument("--representation-prompts", type=int, default=8)
    p.add_argument("--device", default="cuda")
    a = p.parse_args()
    if min(a.steps, a.max_tokens) < 1 or a.representation_prompts < 2:
        raise ValueError("positive training and at least two representation prompts required")
    split = validate_holdout(a.split_manifest, a.train_path, a.validation_path, dataset_revision=a.dataset_revision)
    torch.manual_seed(a.seed)
    tokenizer = AutoTokenizer.from_pretrained(a.student_path, local_files_only=True)
    teacher_tokenizer = AutoTokenizer.from_pretrained(a.teacher_path, local_files_only=True)
    if tokenizer.get_vocab() != teacher_tokenizer.get_vocab():
        raise ValueError("same token identities required")
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    dtype = torch.bfloat16 if a.device.startswith("cuda") else torch.float32
    student = AutoModelForCausalLM.from_pretrained(a.student_path, local_files_only=True,
              dtype=dtype, attn_implementation="eager").to(a.device).eval()
    teacher = AutoModelForCausalLM.from_pretrained(a.teacher_path, local_files_only=True,
              dtype=dtype, attn_implementation="eager").to(a.device).eval()
    teacher.requires_grad_(False)
    install_lora(student)
    params = [x for x in student.parameters() if x.requires_grad]
    before = {n: x.detach().clone() for n, x in student.named_parameters() if x.requires_grad}
    train, valid = load_public_rows(a.train_path), load_public_rows(a.validation_path)
    prompts = [_prompt(tokenizer, r["question"], a.device) for r in valid[:a.representation_prompts]]
    initial_features = features(student, prompts)
    optimizer = torch.optim.AdamW(params, lr=1e-6, weight_decay=.01)
    rows = []
    for step in range(a.steps):
        ids, mask, _ = _sample(student, tokenizer, train[step % len(train)]["question"], a.device, 8, a.max_tokens)
        with torch.no_grad():
            old, target = _logits(student, ids), _logits(teacher, ids)
        current = _logits(student, ids)
        residuals, losses, logp = response_statistics(current, target, old, ids, mask)
        lengths = mask.sum(-1)
        h0, h1 = occupancy_surrogate(residuals[None], logp[None])
        g0 = torch.autograd.grad((losses[:4] * lengths[:4]).sum() / lengths[:4].sum(), params, retain_graph=True)
        g1 = torch.autograd.grad((losses[4:] * lengths[4:]).sum() / lengths[4:].sum(), params, retain_graph=True)
        hg0 = torch.autograd.grad(h0, params, retain_graph=True)
        hg1 = torch.autograd.grad(h1, params, retain_graph=True)
        cross = cross_fitted_occupancy(g0, g1, hg0, hg1)
        loss = (losses * lengths).sum() / lengths.sum()
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        norm = float(torch.nn.utils.clip_grad_norm_(params, 1.))
        measured = float(topk_residual(current.detach(), target, mask))
        optimizer.step()
        record = {"step": step, "top16_residual_global_token_mean": measured,
                  "actor_surrogate_global_token_mean": float(loss.detach()), "pre_clip_gradient_l2": norm,
                  "learning_signal_proxy": learning_signal_proxy(measured, norm),
                  "cross_fitted_occupancy": cross, "response_tokens": int(mask.sum())}
        rows.append(record)
        print(json.dumps(record), flush=True)
        del current, target, old, residuals, losses, logp, h0, h1, g0, g1, hg0, hg1, loss
    final = {n: x.detach() for n, x in student.named_parameters() if x.requires_grad}
    final_features = features(student, prompts)
    report = {"adapter_key": "opd-learning-signals", "seed": a.seed, "diagnostic_only": True,
              "evaluation_tier": "l1_mechanism", "student": {"id": a.student_id, "revision": a.student_revision},
              "teacher": {"id": a.teacher_id, "revision": a.teacher_revision},
              "split_provenance": split, "test_read": split["test_read"], "rows": rows,
              "parameter_statistics": parameter_displacement(before, final),
              "parameter_scope": "LoRA adapter parameters only; not original full-model displacement",
              "representation_prompts": len(prompts),
              "layerwise_prompt_cka": [linear_cka(x, y) for x, y in zip(initial_features, final_features)],
              "limitations": ["three-step small GSM8K diagnostic is not evidence of a learning plateau",
                              "one public teacher; not original larger-teacher versus self-RL comparison",
                              "minibatch proxy/cross-fit estimates are not population quantities or causal explanations"]}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
