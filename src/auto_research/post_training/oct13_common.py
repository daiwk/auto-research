"""Shared execution plumbing, not paper algorithms, for verified checkpoint runs.

The dataset verifier owns reference labels. Model generation accepts messages
only. Every generated token, including rejection/profiling tokens, is charged.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

import torch

from auto_research.public_holdout import validate_holdout
from .oct10_checkpoint import load_public_rows, verified_reward
from .proximal_checkpoint import problem_messages
from .response_policy import GeneratedResponse, ResponsePolicy


class ExecutionFailure(RuntimeError):
    def __init__(self, message, evidence=None):
        super().__init__(message)
        self.evidence = {"status": "failed", "diagnostic_only": True,
                         "error": message, **(evidence or {})}


@dataclass
class CostLedger:
    calls: dict[str, int] = field(default_factory=dict)
    generated_tokens: dict[str, int] = field(default_factory=dict)
    scored_tokens: dict[str, int] = field(default_factory=dict)
    encoder_calls: int = 0
    encoded_input_tokens: int = 0

    def sample(self, policy, messages, *, role="student", samples=1, max_tokens=512, sample=True, json_schema=None):
        if json_schema is None:
            responses = policy.generate(messages, samples=samples, max_tokens=max_tokens, sample=sample)
        else:
            responses = policy.generate(messages, samples=samples, max_tokens=max_tokens, sample=sample, json_schema=json_schema)
        self.calls[role] = self.calls.get(role, 0) + 1
        self.generated_tokens[role] = self.generated_tokens.get(role, 0) + sum(len(r.tokens) for r in responses)
        return responses

    def score(self, policy, messages, tokens, *, role="student"):
        self.scored_tokens[role] = self.scored_tokens.get(role, 0) + len(tokens)
        return policy.token_statistics(messages, tokens)[0]

    def to_dict(self):
        return {"generation_calls": dict(self.calls), "generated_tokens": dict(self.generated_tokens),
                "scored_response_tokens": dict(self.scored_tokens),
                "frozen_encoder_forward_calls": self.encoder_calls,
                "frozen_encoder_input_tokens_including_prompt": self.encoded_input_tokens,
                "scope": "entire invocation, including training controls, profiling and evaluation",
                "includes_rejected_and_profiling_generations": True}


def load_split(config):
    split = validate_holdout(Path(config["split_manifest"]), Path(config["train_path"]),
                             Path(config["validation_path"]), dataset_revision=config["dataset_revision"])
    if not split["verified"]:
        raise ValueError("verified public train-only holdout required")
    train = load_public_rows(Path(config["train_path"]))
    validation = load_public_rows(Path(config["validation_path"]))
    train_count, validation_count = int(config.get("train_examples", 8)), int(config.get("validation_examples", 4))
    if min(train_count, validation_count) < 1:
        raise ValueError("positive train and validation example budgets required")
    train = train[:train_count]
    validation = validation[:validation_count]
    if not train or not validation:
        raise ValueError("nonempty train and validation are required")
    return train, validation, split


def load_policy(config, *, role="student", seed=42):
    return ResponsePolicy(public_id=config[f"{role}_id"], revision=config[f"{role}_revision"],
                          checkpoint_path=Path(config[f"{role}_path"]),
                          device=config.get("device", "cuda"), seed=seed,
                          context_limit=int(config.get("context_limit", 4096)))


def evaluate(policy, rows, ledger, *, max_tokens=512, seed=10042, role="evaluation"):
    results = []
    devices = [torch.cuda.current_device()] if str(policy.device).startswith("cuda") else []
    with torch.random.fork_rng(devices=devices):
        torch.manual_seed(seed)
        for row in rows:
            response = ledger.sample(policy, problem_messages(row["question"]), role=role,
                                     max_tokens=max_tokens, sample=False)[0]
            results.append({"correct": 0. if response.truncated else verified_reward(response.text, row["answer"]),
                            "tokens": len(response.tokens), "truncated": response.truncated})
    return {"accuracy": sum(r["correct"] for r in results) / len(results), "examples": len(results),
            "generated_tokens": sum(r["tokens"] for r in results),
            "truncated_responses": sum(r["truncated"] for r in results)}


def optimizer_step(policy, losses, *, denominator):
    if policy.optimizer is None or denominator < 1 or not losses:
        raise ValueError("actual supervised tokens and initialized trainable policy required")
    policy.model.train()
    policy.optimizer.zero_grad(set_to_none=True)
    total = 0.
    for loss in losses:
        (loss / denominator).backward()
        total += float(loss.detach()) / denominator
    norm = torch.nn.utils.clip_grad_norm_([p for p in policy.model.parameters() if p.requires_grad],
                                          1., error_if_nonfinite=True)
    if not float(norm) > 0:
        raise ExecutionFailure("zero actual gradient; no parameter update fabricated")
    policy.optimizer.step()
    policy.model.eval()
    return {"loss": total, "gradient_l2_norm": float(norm), "optimizer_update_executed": True}


def sft_step(policy, demonstrations, ledger):
    """Response-only NLL. Demonstrations are training targets, never prompt gold."""
    policy.model.train()
    losses, count = [], 0
    for question, tokens in demonstrations:
        likelihood = ledger.score(policy, problem_messages(question), tokens, role="student_sft")
        losses.append(-likelihood.sum())
        count += len(tokens)
    audit = optimizer_step(policy, losses, denominator=count)
    return {**audit, "supervised_tokens": count, "supervised_instances": len(demonstrations)}


def centered_advantages(rewards, *, normalize_std=False):
    values = torch.as_tensor(rewards, dtype=torch.float64, device="cpu")
    if values.ndim != 1 or values.numel() < 2 or not torch.isfinite(values).all():
        raise ValueError("at least two finite rewards required")
    # Translation leaves group advantages unchanged. Subtracting one actual
    # reward first makes a constant group exactly zero, instead of amplifying
    # float32 reduction residue through the subsequent std + epsilon division.
    offsets = values - values.flatten()[0]
    centered = offsets - offsets.mean()
    if normalize_std:
        # Scalar reductions stay on CPU: CUDA/MPS receive only policy precision.
        scale = offsets.std(unbiased=False)
        if not torch.isfinite(scale):
            raise ValueError("finite reward dispersion required")
        centered = centered / (scale + 1e-6)
    if not torch.isfinite(centered).all():
        raise ValueError("finite centered rewards required")
    result = centered.to(dtype=torch.float32)
    if not torch.isfinite(result).all():
        raise ValueError("centered rewards must fit policy precision")
    return result


def policy_gradient_step(policy, group, rewards, ledger, *, reference=None, kl_beta=0., epsilon=.2,
                         behavior_log_probs=None, normalize_std=False):
    """One actual clipped group update with fixed behavior and optional frozen KL."""
    advantages = centered_advantages(rewards, normalize_std=normalize_std).to(policy.device)
    if not bool(advantages.abs().sum()):
        return {"optimizer_update_executed": False, "zero_advantage_group": True,
                "rewards": list(map(float, rewards))}
    old = behavior_log_probs
    if old is None:
        old = []
        with torch.no_grad():
            for messages, response in group:
                old.append(ledger.score(policy, messages, response.tokens, role="behavior").detach())
    if len(old) != len(group):
        raise ValueError("behavior likelihoods must align with the actual generated group")
    policy.model.train()
    losses = []
    for index, (messages, response) in enumerate(group):
        current = ledger.score(policy, messages, response.tokens, role="student_rl")
        ratio = (current - old[index]).exp()
        surrogate = torch.minimum(ratio * advantages[index], ratio.clamp(1-epsilon, 1+epsilon) * advantages[index])
        loss = -surrogate.mean()
        if reference is not None and kl_beta:
            with torch.no_grad():
                ref = ledger.score(reference, messages, response.tokens, role="reference")
            # Nonnegative k3 estimator on the sampled response, fixed reference.
            log_ratio = ref - current
            loss = loss + kl_beta * (log_ratio.exp() - log_ratio - 1).mean()
        losses.append(loss)
    audit = optimizer_step(policy, losses, denominator=len(group))
    return {**audit, "zero_advantage_group": False, "rewards": list(map(float, rewards)),
            "advantages": advantages.tolist()}


def sample_prefix(policy, messages, prefix_tokens, ledger, *, samples=2, max_tokens=512, role="teacher_profile"):
    """Continue the SAME open assistant response, not a new user-turn approximation."""
    prompt = policy.prompt_ids(messages)
    prefix = torch.tensor(prefix_tokens, device=policy.device, dtype=torch.long)[None]
    inputs = torch.cat((prompt, prefix), dim=-1)
    remaining = min(max_tokens, policy.context_limit-inputs.shape[1])
    if remaining < 1 or samples < 1:
        raise ValueError("prefix continuation needs a positive remaining context budget")
    policy.model.eval()
    with torch.no_grad():
        output = policy.model.generate(inputs, attention_mask=torch.ones_like(inputs),
            max_new_tokens=remaining, num_return_sequences=samples, do_sample=True,
            temperature=1., top_p=1., top_k=0, use_cache=True,
            pad_token_id=policy.tokenizer.pad_token_id)
    responses = []
    for row in output:
        suffix = row[inputs.shape[1]:]
        eos = torch.where(suffix == policy.tokenizer.eos_token_id)[0]
        if len(eos):
            suffix = suffix[:int(eos[0])+1]
        tokens = tuple(map(int, suffix.cpu().tolist()))
        responses.append(GeneratedResponse(tokens, policy.tokenizer.decode(tokens, skip_special_tokens=True),
                                            not len(eos) and len(tokens) >= remaining))
    ledger.calls[role] = ledger.calls.get(role, 0)+1
    ledger.generated_tokens[role] = ledger.generated_tokens.get(role, 0)+sum(len(r.tokens) for r in responses)
    return responses


def causal_response_features(encoder, messages, tokens, *, prompt_token_ids=None):
    """Frozen last-layer CAUSAL features at exact generated-token positions."""
    prompt = encoder.prompt_ids(messages) if prompt_token_ids is None else prompt_token_ids.to(encoder.device)
    response = torch.tensor(tokens, dtype=torch.long, device=encoder.device)[None]
    inputs = torch.cat((prompt, response), dim=-1)
    if inputs.shape[1] > encoder.context_limit:
        raise ValueError("complete encoder history exceeds context budget")
    encoder.model.eval()
    with torch.no_grad():
        hidden = encoder.model.model(inputs, attention_mask=torch.ones_like(inputs), use_cache=False).last_hidden_state
    return hidden[0, prompt.shape[1]:].detach().float()


def result_payload(method, config, seed, split, policy, ledger, baseline, after, training, **extra):
    return {"method": method, "seed": seed, "device": config.get("device", "cuda"),
            "diagnostic_only": True, "promotion_eligible": False, "evaluation_tier": "l1_mechanism",
            "dataset": split, "checkpoint": policy.provenance, "baseline": baseline,
            "method_metrics": after, "training": training, "cost": ledger.to_dict(),
            "protocol": {"test_opened": False, "gold_in_student_generation": False,
                         "gold_in_student_generation_scope": "evaluated_student_inference_only",
                         "training_construction_roles_with_gold":
                             ["offline_aligner", "construction_self_rewrite"] if method == "synthself" else [],
                         "comparison_kind": "matched_budget_control" if method == "upturn" else "before_after_training",
                         "train_examples": config.get("train_examples", 8),
                         "validation_examples": config.get("validation_examples", 4),
                         "max_tokens": config.get("max_tokens", 512)}, **extra}


def execute(method, config, *, seed=42):
    config={k:(Path(v) if k.endswith("_path") or k=="split_manifest" else v)
            for k,v in config.items() if k not in {"seed","method"}}
    if method == "state-opd":
        from auto_research.reproductions.state_opd.checkpoint import run_state_opd
        import inspect
        fields=inspect.signature(run_state_opd).parameters
        return run_state_opd(**{k:v for k,v in config.items() if k in fields},seed=seed)
    if method in {"gppo-framework","tapo-trajectory"}:
        from .proximal_checkpoint import run_proximal_checkpoint
        import inspect
        fields=inspect.signature(run_proximal_checkpoint).parameters
        return run_proximal_checkpoint(method=method,**{k:v for k,v in config.items() if k in fields and k not in {"method","seed"}},seed=seed)
    from importlib import import_module
    module = import_module("auto_research.reproductions." + method.replace("-", "_") + ".checkpoint")
    return module.run(config, seed=seed)


def adapter_run(method, dataset_dir, seed):
    """Real adapter entry; a missing resource configuration is never a fixture."""
    config_path = Path(dataset_dir) / "oct13_execution.json"
    if not config_path.is_file():
        raise FileNotFoundError("prepare oct13_execution.json with verified checkpoint and holdout resources")
    config = json.loads(config_path.read_text())
    config = {**config.get("shared", config), **config.get("methods", {}).get(method, {})}
    return execute(method,config,seed=seed)


def render_result(result):
    baseline_label, method_label = ("匹配预算对照 validation", "训练后干预策略 validation") if result["method"] == "upturn" else ("训练前 validation", "训练后 validation")
    return (f"# {result['method']} 本地执行\n\n"
            "公开checkpoint上的小预算机制诊断；不是原benchmark复现或正式能力比较。\n\n"
            f"Seed：{result['seed']}；权重/头部更新：{result.get('parameters_changed', False)}。\n\n"
            f"{baseline_label}：{result['baseline']}\n\n{method_label}：{result['method_metrics']}\n\n"
            f"真实预算：{result.get('cost',result.get('sampling',result.get('protocol')))}\n\n不读取官方test，失败和零优势组保留。\n")
