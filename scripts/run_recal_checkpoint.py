#!/usr/bin/env python3
"""Bounded paired Qwen ReCal runtime: physical FFN pruning -> SFT -> OPD.

LoRA recovery and a math-only small prompt pool differ from the paper's full
training recipe. Outputs are diagnostics, never original benchmark gains.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import torch
from auto_research.public_holdout import validate_holdout

from auto_research.post_training.oct10_checkpoint import (
    _logits, _prompt, _sample, install_lora, load_public_rows, verified_reward,
)
from auto_research.post_training.recal import (
    coarsened_forward_kl, damage_weights, prune_gated_ffn, restricted_opd_loss,
)


def mlps(model):
    return [layer.mlp for layer in model.model.layers]


def calibration_scores(model, sequences, masks, damages=None):
    layers = mlps(model)
    sums = [torch.zeros(m.down_proj.in_features, device=model.device) for m in layers]
    for row, (ids, mask) in enumerate(zip(sequences, masks)):
        weights = (damage_weights(damages[row], mask) if damages is not None
                   else mask.float() / mask.sum(-1, keepdim=True))
        hooks = []
        for index, mlp in enumerate(layers):
            def capture(_, inputs, index=index):
                activation = inputs[0][:, :-1].detach().float()
                sums[index].add_((activation.square() * weights[..., None]).sum(-2).mean(0))
            hooks.append(mlp.down_proj.register_forward_pre_hook(capture))
        try:
            with torch.no_grad():
                model(ids, use_cache=False)
        finally:
            for handle in hooks:
                handle.remove()
    return [(s / len(sequences)).sqrt() * m.down_proj.weight.detach().float().norm(dim=0)
            for s, m in zip(sums, layers)]


def prune_copy(teacher, scores, width):
    model = deepcopy(teacher)
    for mlp, score in zip(mlps(model), scores):
        indices = score.argsort(descending=True, stable=True)[:width].sort().values
        prune_gated_ffn(mlp, indices)
    model.config.intermediate_size = width
    return model


def evaluate(model, tokenizer, rows, *, device, max_tokens, examples):
    correct = 0
    for row in rows[:examples]:
        ids = _prompt(tokenizer, row["question"], device)
        with torch.no_grad():
            result = model.generate(ids, attention_mask=torch.ones_like(ids), do_sample=False,
                                    max_new_tokens=max_tokens, pad_token_id=tokenizer.pad_token_id)
        text = tokenizer.decode(result[0, ids.shape[1]:], skip_special_tokens=True)
        correct += verified_reward(text, row["answer"])
    count = min(examples, len(rows))
    return {"examples": count, "exact_match": correct / count}


def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    p = argparse.ArgumentParser(description=__doc__)
    for name in ("checkpoint-path", "train-path", "validation-path", "output"):
        p.add_argument("--" + name, required=True, type=Path)
    for name in ("checkpoint-id", "checkpoint-revision", "dataset-revision"):
        p.add_argument("--" + name, required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--calibration-examples", type=int, default=4)
    p.add_argument("--opd-steps", type=int, default=4)
    p.add_argument("--max-tokens", type=int, default=256)
    p.add_argument("--validation-examples", type=int, default=4)
    p.add_argument("--keep-ratio", type=float, default=.75)
    p.add_argument("--device", default="cuda")
    p.add_argument("--split-manifest", type=Path)
    a = p.parse_args()
    if not 0 < a.keep_ratio < 1 or min(a.calibration_examples, a.opd_steps, a.validation_examples) < 1:
        raise ValueError("valid ratio and positive budgets required")
    split = validate_holdout(a.split_manifest, a.train_path, a.validation_path,
                             dataset_revision=a.dataset_revision)
    train, valid = load_public_rows(a.train_path), load_public_rows(a.validation_path)
    if {r["question"] for r in train} & {r["question"] for r in valid}:
        raise ValueError("train/validation overlap")
    if len(train) < a.calibration_examples + a.opd_steps:
        raise ValueError("disjoint SFT and OPD training prompt pools required")
    torch.manual_seed(a.seed)
    tokenizer = AutoTokenizer.from_pretrained(a.checkpoint_path, local_files_only=True)
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    dtype = torch.bfloat16 if a.device.startswith("cuda") else torch.float32
    teacher = AutoModelForCausalLM.from_pretrained(a.checkpoint_path, local_files_only=True,
                  dtype=dtype, attn_implementation="eager").to(a.device).eval()
    teacher.requires_grad_(False)
    original_width = mlps(teacher)[0].gate_proj.out_features
    width = int(original_width * a.keep_ratio) // 128 * 128
    prompts = [_prompt(tokenizer, r["question"], a.device) for r in train[:a.calibration_examples]]
    prompt_masks = [torch.ones_like(ids[:, 1:], dtype=torch.bool) for ids in prompts]
    base_scores = calibration_scores(teacher, prompts, prompt_masks)
    sequences, masks = [], []
    for ids in prompts:
        with torch.no_grad():
            target = teacher.generate(ids, attention_mask=torch.ones_like(ids), do_sample=False,
                                      max_new_tokens=a.max_tokens, pad_token_id=tokenizer.pad_token_id)
        response = target[0, ids.shape[1]:]
        if not bool((response == tokenizer.eos_token_id).any()):
            raise ValueError("teacher SFT response truncated; increase max-tokens instead of silently accepting")
        mask = torch.zeros_like(target[:, 1:], dtype=torch.bool)
        mask[:, ids.shape[1] - 1:] = True
        sequences.append(target)
        masks.append(mask)
    probe = prune_copy(teacher, base_scores, width)
    damages = []
    for ids in sequences:
        with torch.no_grad():
            damages.append(coarsened_forward_kl(_logits(teacher, ids), _logits(probe, ids)))
    del probe
    if a.device.startswith("cuda"):
        torch.cuda.empty_cache()
    # Final scores always recomputed on the original teacher, not the probe.
    recal_scores = calibration_scores(teacher, sequences, masks, damages)
    rows = []
    for recipe, scores in (("base-wanda", base_scores), ("recal-wanda", recal_scores)):
        torch.manual_seed(a.seed)
        model = prune_copy(teacher, scores, width)
        parameter_count = sum(x.numel() for x in model.parameters())
        install_lora(model)
        params = [x for x in model.parameters() if x.requires_grad]
        optimizer = torch.optim.AdamW(params, lr=1e-5, weight_decay=0)
        before = {name: x.detach().clone() for name, x in model.named_parameters() if x.requires_grad}
        stages = {"pruned": evaluate(model, tokenizer, valid, device=a.device,
                                     max_tokens=a.max_tokens, examples=a.validation_examples)}
        for _ in range(2):
            for ids, mask in zip(sequences, masks):
                logits = _logits(model, ids)
                losses = torch.nn.functional.cross_entropy(logits.flatten(0, 1), ids[:, 1:].flatten(),
                                                            reduction="none").reshape_as(mask)
                loss = losses[mask].mean()
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(params, 1.)
                optimizer.step()
        stages["sft"] = evaluate(model, tokenizer, valid, device=a.device,
                                  max_tokens=a.max_tokens, examples=a.validation_examples)
        for group in optimizer.param_groups:
            group["lr"] = 1e-6
        history = []
        for step, example in enumerate(train[a.calibration_examples:a.calibration_examples + a.opd_steps]):
            ids, mask, _ = _sample(model, tokenizer, example["question"], a.device, 2, a.max_tokens)
            with torch.no_grad():
                old, target = _logits(model, ids), _logits(teacher, ids)
            loss = restricted_opd_loss(_logits(model, ids), target, old, mask)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            gradient = float(torch.nn.utils.clip_grad_norm_(params, 1.))
            optimizer.step()
            history.append({"step": step, "loss": float(loss.detach()), "gradient_l2": gradient})
        stages["opd"] = evaluate(model, tokenizer, valid, device=a.device,
                                  max_tokens=a.max_tokens, examples=a.validation_examples)
        delta = sum(float((x.detach() - before[name]).square().sum())
                    for name, x in model.named_parameters() if name in before)**.5
        row = {"recipe": recipe, "parameters_after_pruning": parameter_count,
               "retained_width": width, "stages": stages, "adapter_delta_l2": delta,
               "opd_history": history, "sft_updates": 2 * len(sequences)}
        rows.append(row)
        print(json.dumps(row), flush=True)
        del model, optimizer, params, before, logits, losses, loss, old, target
        if a.device.startswith("cuda"):
            torch.cuda.empty_cache()
    payload = {"adapter_key": "recal", "seed": a.seed, "diagnostic_only": True,
               "evaluation_tier": "l1_mechanism", "rows": rows,
               "checkpoint": {"id": a.checkpoint_id, "revision": a.checkpoint_revision},
               "dataset": {"id": "openai/grade-school-math", "revision": a.dataset_revision,
                           "train_sha256": hashlib.sha256(a.train_path.read_bytes()).hexdigest(),
                           "validation_sha256": hashlib.sha256(a.validation_path.read_bytes()).hexdigest()},
               "original_width": original_width, "calibration_examples": len(sequences),
               "fidelity": "core_mechanism", "test_read": split["test_read"], "split_provenance": split,
               "limitations": ["LoRA recovery instead of original full-parameter FSDP",
                               "math-only small public pool; not four-domain benchmark reproduction",
                               "Same retained width and SFT targets; wall-clock budgets not claimed equal"]}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
