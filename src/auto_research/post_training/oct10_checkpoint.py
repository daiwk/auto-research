"""Real causal-LM LoRA training for the October OPD/RL operators.

No gold references enter rollout generation. References are read by the external
verifier, or MetaOPD's separate *training* reference stream. Short executions
are explicitly runtime validations, not reproductions of paper benchmark gains.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

import torch
from torch import nn
from torch.func import functional_call

from .oct10_objectives import (
    SemiOPDCache, clipped_actor_loss, co_ra_step, dial_opd_loss, grpo_dropout,
    meta_opd_step, residual_advantage, semi_opd_loss, topk_overlap,
)

OBJECTIVES = ("opd", "dial-opd", "meta-opd", "semi-opd", "grpo-dropout", "residual-advantage", "co-ra")
PAPER_OBJECTIVES = {
    "dial-opd": ("dial-opd",), "meta-opd": ("meta-opd",),
    "semi-opd": ("semi-opd",), "grpo-dropout": ("grpo-dropout",),
    "residual-advantage": ("residual-advantage", "co-ra"),
}


class LowRankLinear(nn.Module):
    """Zero-output LoRA; base frozen, FP32 adapter for stable meta derivatives."""
    def __init__(self, base: nn.Linear, rank=8):
        super().__init__()
        self.base = base
        self.base.requires_grad_(False)
        self.a = nn.Parameter(torch.empty(rank, base.in_features, device=base.weight.device))
        self.b = nn.Parameter(torch.zeros(base.out_features, rank, device=base.weight.device))
        nn.init.kaiming_uniform_(self.a, a=5**.5)
        self.scale = 1.0

    def forward(self, x):
        adaptation = torch.nn.functional.linear(torch.nn.functional.linear(x.float(), self.a), self.b)
        return self.base(x) + (self.scale * adaptation).to(x.dtype)


def install_lora(model, rank=8):
    model.requires_grad_(False)
    replaced = 0
    for name, module in list(model.named_modules()):
        if name.rsplit(".", 1)[-1] in {"q_proj", "v_proj"} and isinstance(module, nn.Linear):
            parent_name, child = name.rsplit(".", 1)
            setattr(model.get_submodule(parent_name), child, LowRankLinear(module, rank))
            replaced += 1
    if not replaced:
        raise ValueError("checkpoint has no supported q_proj/v_proj modules")
    return replaced


def load_public_rows(path: Path):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not rows or any(not isinstance(r.get("question"), str) or
                       not isinstance(r.get("answer"), str) for r in rows):
        raise ValueError("JSONL requires nonempty public question/answer records")
    return rows


def numeric_answer(text):
    """GSM8K numeric verifier; extraction is not a model input."""
    if "####" in text:
        text = text.rsplit("####", 1)[-1]
    boxed = re.findall(r"\\boxed\{([^{}]+)\}", text)
    if boxed:
        text = boxed[-1]
    values = re.findall(r"-?\d[\d,]*(?:\.\d+)?", text)
    return values[-1].replace(",", "") if values else None


def verified_reward(response, reference):
    """Invalid references are a data error, never a None == None success."""
    target = numeric_answer(reference)
    if target is None:
        raise ValueError("GSM8K reference has no numeric answer")
    prediction = numeric_answer(response)
    return float(prediction is not None and prediction == target)


def _prompt(tokenizer, question, device):
    messages = [{"role": "user", "content": question}]
    if tokenizer.chat_template:
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                              enable_thinking=False)
    else:
        text = f"Question: {question}\nAnswer:"
    return tokenizer(text, return_tensors="pt").input_ids.to(device)


def _sample(student, tokenizer, question, device, group, max_tokens):
    prompt = _prompt(tokenizer, question, device)
    with torch.no_grad():
        ids = student.generate(prompt, attention_mask=torch.ones_like(prompt),
                               max_new_tokens=max_tokens, do_sample=True,
                               temperature=1., top_p=1., num_return_sequences=group,
                               pad_token_id=tokenizer.pad_token_id, use_cache=True)
    mask = torch.zeros_like(ids[:, 1:], dtype=torch.bool)
    mask[:, prompt.shape[1] - 1:] = True
    # Includes first EOS, excludes repeated padding after generation finishes.
    for row in range(len(ids)):
        response = ids[row, prompt.shape[1]:]
        eos = torch.where(response == tokenizer.eos_token_id)[0]
        if len(eos):
            mask[row, prompt.shape[1] + int(eos[0]):] = False
    texts = tokenizer.batch_decode(ids[:, prompt.shape[1]:], skip_special_tokens=True)
    return ids, mask, texts


def _logits(model, ids, parameters=None):
    kwargs = {"input_ids": ids, "use_cache": False}
    result = model(**kwargs) if parameters is None else functional_call(model, parameters, (), kwargs)
    return result.logits[:, :-1].float()


def run_checkpoint(*, objective, student_path, teacher_path, student_id, student_revision,
                   teacher_id, teacher_revision, train_path, validation_path, dataset_revision,
                   output_dir, seed=42, steps=3, max_tokens=32, group=4, learning_rate=1e-5,
                   validation_examples=4, device="cuda"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if objective not in OBJECTIVES or min(steps, max_tokens, group, validation_examples) < 1:
        raise ValueError("invalid objective or execution budget")
    if objective in {"grpo-dropout", "residual-advantage", "co-ra"} and group < 2:
        raise ValueError("GRPO requires multiple responses per prompt")
    if not all((student_revision, teacher_revision, dataset_revision)):
        raise ValueError("public checkpoint/data revisions are required")
    train, validation = load_public_rows(train_path), load_public_rows(validation_path)
    if {r["question"] for r in train} & {r["question"] for r in validation}:
        raise ValueError("training and validation questions overlap")
    torch.manual_seed(seed)
    dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(student_path, local_files_only=True)
    teacher_tokenizer = AutoTokenizer.from_pretrained(teacher_path, local_files_only=True)
    if tokenizer.get_vocab() != teacher_tokenizer.get_vocab():
        raise ValueError("teacher/student token identity must align; equal vocabulary size is insufficient")
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    student = AutoModelForCausalLM.from_pretrained(student_path, dtype=dtype,
                 attn_implementation="eager", local_files_only=True).to(device).eval()
    teacher = AutoModelForCausalLM.from_pretrained(teacher_path, dtype=dtype,
                 attn_implementation="eager", local_files_only=True).to(device).eval()
    teacher.requires_grad_(False)
    install_lora(student)
    optimizer = torch.optim.AdamW([p for p in student.parameters() if p.requires_grad],
                                  lr=learning_rate, weight_decay=.01)
    before = {n: p.detach().clone() for n, p in student.named_parameters() if p.requires_grad}
    network = nn.Sequential(nn.Linear(74, 64), nn.Tanh(), nn.Linear(64, 1)).to(device)
    nn.init.zeros_(network[-1].weight)
    nn.init.zeros_(network[-1].bias)
    meta_optimizer = torch.optim.AdamW(network.parameters(), lr=1e-3)
    teacher_optimizer = None
    teacher_before = {}
    if objective == "co-ra":
        install_lora(teacher)
        teacher_before = {n: p.detach().clone() for n, p in teacher.named_parameters() if p.requires_grad}
        teacher_optimizer = torch.optim.AdamW([p for p in teacher.parameters() if p.requires_grad],
                                              lr=learning_rate, weight_decay=.01)
    # Fixed pi_0 responses and one teacher pass per response, before any update.
    cache = []
    if objective == "semi-opd":
        for row in train[:steps]:
            ids, mask, texts = _sample(student, tokenizer, row["question"], device, 1, max_tokens)
            with torch.no_grad():
                teacher_lp = _logits(teacher, ids).log_softmax(-1).gather(-1, ids[:, 1:, None]).squeeze(-1)
            record = SemiOPDCache(student_revision, teacher_revision, student_revision, dataset_revision,
                                  tuple(map(tuple, ids.tolist())), tuple(map(tuple, mask.tolist())),
                                  tuple(map(tuple, teacher_lp.tolist())))
            cache.append((ids, mask, texts, teacher_lp, record))
    history = []
    for step in range(steps):
        row = train[step % len(train)]
        if objective == "semi-opd":
            ids, mask, texts, teacher_lp, _ = cache[step % len(cache)]
            teacher_logits = None
        else:
            ids, mask, texts = _sample(student, tokenizer, row["question"], device, group, max_tokens)
            with torch.no_grad():
                teacher_logits = _logits(teacher, ids)
                teacher_lp = teacher_logits.log_softmax(-1).gather(-1, ids[:, 1:, None]).squeeze(-1)
        actions = ids[:, 1:]
        with torch.no_grad():
            rollout_logits = _logits(student, ids)
            old_lp = rollout_logits.log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
        metrics = {"step": step, "response_tokens": int(mask.sum())}
        rewards = torch.tensor([verified_reward(text, row["answer"])
                                for text in texts], device=device)
        # GRPO's group estimator uses sample standard deviation (RA Table 12).
        deviation = rewards.std(unbiased=True) if len(rewards) > 1 else rewards.new_zeros(())
        advantage = (rewards - rewards.mean()) / (deviation + 1e-6)
        if objective == "meta-opd":
            reference = train[(step + len(train) // 2) % len(train)]
            prefix = _prompt(tokenizer, reference["question"], device)
            suffix = tokenizer(reference["answer"], return_tensors="pt", add_special_tokens=False).input_ids.to(device)
            ref_ids = torch.cat((prefix, suffix[:, :max_tokens]), -1)
            def reference_loss(parameters):
                logits = _logits(student, ref_ids, parameters)[:, prefix.shape[1] - 1:]
                return torch.nn.functional.cross_entropy(logits.reshape(-1, logits.shape[-1]),
                                                         ref_ids[:, prefix.shape[1]:].reshape(-1))
            metrics.update(meta_opd_step(student, network, optimizer, meta_optimizer,
                            logits_fn=lambda p: _logits(student, ids, p),
                            reference_loss_fn=reference_loss, teacher_logits=teacher_logits,
                            actions=actions, old_logp=old_lp, mask=mask))
        elif objective == "co-ra":
            metrics.update(co_ra_step(student, teacher, optimizer, teacher_optimizer,
                            student_logits_fn=lambda: _logits(student, ids),
                            teacher_logits_fn=lambda: _logits(teacher, ids),
                            actions=actions, mask=mask, verifier_advantage=advantage))
        else:
            logits = _logits(student, ids)
            current = logits.log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
            if objective == "dial-opd":
                loss, selected = dial_opd_loss(current, teacher_lp, mask)
                metrics["selected_tokens"] = int(selected.sum())
            elif objective in {"opd", "semi-opd"}:
                loss = semi_opd_loss(current, teacher_lp, mask)
            elif objective == "grpo-dropout":
                retained, centered = grpo_dropout(old_lp, mask, advantage)
                loss = clipped_actor_loss(current, old_lp, centered[:, None].expand_as(current),
                                           mask & retained[:, None])
                metrics["retained_rollouts"] = int(retained.sum())
            else:
                labels = residual_advantage(rollout_logits, teacher_logits, actions, mask,
                                             advantage, guidance_weight=10.)
                loss = clipped_actor_loss(current, old_lp, labels, mask)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(student.parameters(), 1.)
            optimizer.step()
            metrics["loss"] = float(loss.detach())
        if teacher_logits is not None:
            metrics["overlap_at_64"] = float(topk_overlap(rollout_logits, teacher_logits, mask))
        metrics["training_reward_mean"] = float(rewards.mean())
        metrics["training_reward_variance"] = float(rewards.var(unbiased=False))
        metrics["student_gradient_l2"] = sum(
            float(p.grad.detach().square().sum()) for p in student.parameters()
            if p.requires_grad and p.grad is not None
        )**.5
        if teacher_optimizer is not None:
            metrics["teacher_gradient_l2"] = sum(
                float(p.grad.detach().square().sum()) for p in teacher.parameters()
                if p.requires_grad and p.grad is not None
            )**.5
        history.append(metrics)
        print(json.dumps({"objective": objective, "seed": seed, **metrics}), flush=True)
    delta = sum(float((p.detach() - before[n]).square().sum())
                for n, p in student.named_parameters() if p.requires_grad)**.5
    # Validation is read only after optimization. No choice/early stopping uses it.
    correct = 0
    for row in validation[:validation_examples]:
        prompt = _prompt(tokenizer, row["question"], device)
        with torch.no_grad():
            result = student.generate(prompt, attention_mask=torch.ones_like(prompt),
                                       max_new_tokens=max_tokens, do_sample=False,
                                       pad_token_id=tokenizer.pad_token_id, use_cache=True)
        text = tokenizer.decode(result[0, prompt.shape[1]:], skip_special_tokens=True)
        correct += verified_reward(text, row["answer"])
    examples = min(validation_examples, len(validation))
    teacher_delta = sum(float((p.detach() - teacher_before[n]).square().sum())
                        for n, p in teacher.named_parameters() if n in teacher_before)**.5
    report = {"objective": objective, "seed": seed, "steps": steps,
              "fidelity": "core-mechanism", "diagnostic_only": True,
              "evaluation_scope": "short real-checkpoint runtime validation; not paper benchmark reproduction",
              "checkpoint": {"student": student_id, "student_revision": student_revision,
                             "teacher": teacher_id, "teacher_revision": teacher_revision},
              "dataset": {"id": "openai/grade-school-math", "revision": dataset_revision,
                          "train_sha256": hashlib.sha256(train_path.read_bytes()).hexdigest(),
                          "validation_sha256": hashlib.sha256(validation_path.read_bytes()).hexdigest()},
              "metrics": {"adapter_parameter_delta_l2": delta,
                          "teacher_adapter_parameter_delta_l2": teacher_delta,
                          "steps_with_nonzero_student_gradient": sum(
                              item["student_gradient_l2"] > 0 for item in history),
                          "validation_examples": examples, "validation_exact_match": correct / examples},
              "history": history, "validation_used_for_selection": False}
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    torch.save({n: p.detach().cpu() for n, p in student.named_parameters() if p.requires_grad},
               output_dir / "adapter.pt")
    return report
