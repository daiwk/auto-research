from __future__ import annotations

import copy
from pathlib import Path

import numpy as np

from auto_research.runtime import device_for

from ..llm_training import require_torch, seed_everything
from ..recent_20260728_common import load_recent_movielens
from .model import (
    COREConfig,
    build_model,
    cascaded_supervised_loss,
    step_rewards,
    teacher_binary_logits,
)


def build_ordinal_data(data, seed):
    rng = np.random.default_rng(seed)
    queries, items, labels, groups = [], [], [], []
    for user, history in enumerate(data.train):
        query = data.features[list(history)].mean(0)
        excluded = set((*history, data.validation[user], data.test[user]))
        candidates = np.asarray(
            [item for item in range(data.item_count) if item not in excluded]
        )
        overlap = data.features[candidates] @ query
        middle_pool = candidates[(overlap > 0) & (overlap < np.quantile(overlap, 0.8))]
        low_pool = candidates[overlap <= np.quantile(overlap, 0.2)]
        if not len(middle_pool) or not len(low_pool):
            continue
        selected = (
            data.test[user],
            int(rng.choice(middle_pool)),
            int(rng.choice(low_pool)),
        )
        for label, item in zip((2, 1, 0), selected):
            queries.append(query)
            items.append(data.features[item])
            labels.append(label)
            groups.append(user)
    order = np.arange(len(labels))
    train = order[np.asarray(groups) % 5 != 0]
    test = order[np.asarray(groups) % 5 == 0]
    return {
        "query": np.asarray(queries, dtype=np.float32),
        "item": np.asarray(items, dtype=np.float32),
        "label": np.asarray(labels, dtype=np.int64),
        "group": np.asarray(groups, dtype=np.int64),
        "train": train,
        "test": test,
    }

def _batch(values, indices, device, torch):
    return torch.tensor(values[indices], device=device)


def _supervised_train(model, rows, config, seed, steps, *, cascaded, teacher=None):
    torch = require_torch()
    seed_everything(seed, torch)
    device = device_for(torch)
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(steps):
        indices = rng.choice(rows["train"], config.batch_size, replace=True)
        query = _batch(rows["query"], indices, device, torch)
        item = _batch(rows["item"], indices, device, torch)
        labels = _batch(rows["label"], indices, device, torch).long()
        logits = model(query, item)
        if not cascaded:
            loss = torch.nn.functional.cross_entropy(logits, labels)
        else:
            loss = cascaded_supervised_loss(logits, labels, torch)
            if teacher is not None:
                with torch.no_grad():
                    class_logits = teacher.class_log_probs(query, item)
                    targets = teacher_binary_logits(class_logits, torch)
                active = labels != 2
                distill = torch.nn.functional.binary_cross_entropy_with_logits(
                    logits[:, 0] / config.temperature,
                    torch.sigmoid(targets[:, 0] / config.temperature),
                )
                distill += torch.nn.functional.binary_cross_entropy_with_logits(
                    logits[active, 1] / config.temperature,
                    torch.sigmoid(targets[active, 1] / config.temperature),
                )
                loss = loss + 0.7 * config.temperature**2 * distill
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
    }


def _step_grpo(model, rows, config, seed):
    torch = require_torch()
    device = next(model.parameters()).device
    reference = copy.deepcopy(model).eval()
    optimizer = torch.optim.AdamW(model.parameters(), lr=4e-4)
    rng = np.random.default_rng(seed + 7)
    losses, reward_means = [], []
    model.train()
    for _ in range(config.grpo_steps):
        indices = rng.choice(rows["train"], config.batch_size, replace=True)
        query = _batch(rows["query"], indices, device, torch)
        item = _batch(rows["item"], indices, device, torch)
        labels = _batch(rows["label"], indices, device, torch).long()
        with torch.no_grad():
            old_logits = reference(query, item)
        logits = model(query, item)
        probabilities = torch.sigmoid(logits)
        distribution = torch.distributions.Bernoulli(
            probabilities[:, None].expand(-1, config.group_size, -1)
        )
        actions = distribution.sample()
        rewards, active = step_rewards(actions, labels, torch)
        mean = rewards.mean(1, keepdim=True)
        std = rewards.std(1, keepdim=True).clamp_min(1e-4)
        advantages = (rewards - mean) / std
        log_probability = distribution.log_prob(actions)
        with torch.no_grad():
            old_distribution = torch.distributions.Bernoulli(
                torch.sigmoid(old_logits)[:, None].expand_as(actions)
            )
            old_log_probability = old_distribution.log_prob(actions)
        ratio = torch.exp(log_probability - old_log_probability)
        clipped = ratio.clamp(0.8, 1.2)
        policy = -torch.minimum(ratio * advantages, clipped * advantages)
        policy = (policy * active).sum() / active.sum().clamp_min(1)
        kl = torch.nn.functional.binary_cross_entropy_with_logits(
            logits, torch.sigmoid(old_logits)
        )
        loss = policy + 0.02 * kl
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        reward_means.append(float((rewards * active).sum().cpu() / active.sum().cpu()))
    return {
        "final_policy_loss": float(np.mean(losses[-10:])),
        "mean_step_reward": float(np.mean(reward_means[-10:])),
        "group_size": config.group_size,
    }


def _evaluate(model, rows, torch):
    device = next(model.parameters()).device
    indices = rows["test"]
    query = _batch(rows["query"], indices, device, torch)
    item = _batch(rows["item"], indices, device, torch)
    labels = rows["label"][indices]
    model.eval()
    with torch.inference_mode():
        scores = model.class_log_probs(query, item).exp().cpu().numpy()
    predictions = scores.argmax(-1)
    f1 = []
    for label in range(3):
        true = labels == label
        predicted = predictions == label
        precision = (true & predicted).sum() / max(predicted.sum(), 1)
        recall = (true & predicted).sum() / max(true.sum(), 1)
        f1.append(2 * precision * recall / max(precision + recall, 1e-12))
    ndcg = badcase = groups = 0.0
    for group in np.unique(rows["group"][indices]):
        selected = rows["group"][indices] == group
        ranking = np.argsort(-scores[selected, 2])
        ordered = labels[selected][ranking]
        gains = (2**ordered - 1).astype(np.float64)
        discounts = 1 / np.log2(np.arange(len(gains)) + 2)
        ideal = np.sort(gains)[::-1]
        ndcg += float((gains * discounts).sum() / max((ideal * discounts).sum(), 1e-12))
        badcase += float(ordered[0] == 0)
        groups += 1
    return {
        "accuracy": float((predictions == labels).mean()),
        "macro_f1": float(np.mean(f1)),
        "ndcg_at_5": ndcg / groups,
        "badcase_at_5": badcase / groups,
    }


def reproduce_core_relevance(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_recent_movielens(dataset_dir)
    rows = build_ordinal_data(data, seed)
    config = COREConfig()
    variants, training = {}, {}

    seed_everything(seed, torch)
    flat = build_model(data.features.shape[1], config, cascaded=False)
    training["flat"] = _supervised_train(
        flat, rows, config, seed, config.sft_steps, cascaded=False
    )
    variants["Flat classifier"] = _evaluate(flat, rows, torch)

    seed_everything(seed, torch)
    cascade = build_model(data.features.shape[1], config, cascaded=True)
    training["cascade_sft"] = _supervised_train(
        cascade, rows, config, seed, config.sft_steps, cascaded=True
    )
    variants["Cascaded classifier"] = _evaluate(cascade, rows, torch)
    training["step_grpo"] = _step_grpo(cascade, rows, config, seed)
    variants["Cascaded + step-GRPO"] = _evaluate(cascade, rows, torch)

    seed_everything(seed + 1, torch)
    distilled = build_model(data.features.shape[1], config, cascaded=True)
    training["postcot_distillation"] = _supervised_train(
        distilled,
        rows,
        config,
        seed + 1,
        config.distill_steps,
        cascaded=True,
        teacher=cascade,
    )
    variants["PostCoT distilled cascade"] = _evaluate(distilled, rows, torch)
    baseline, method = variants["Flat classifier"], variants["PostCoT distilled cascade"]
    return {
        "paper": {
            "arxiv_id": "2607.24417",
            "title": "CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search",
            "url": "https://arxiv.org/abs/2607.24417",
            "organization": "Meituan / Beijing Institute of Technology",
        },
        "dataset": {
            "name": "MovieLens-1M ordinal relevance",
            "train_pairs": len(rows["train"]),
            "test_pairs": len(rows["test"]),
            "labels": ["Low", "Mid", "High"],
        },
        "setup": {
            "seed": seed,
            "sft_steps": config.sft_steps,
            "step_grpo_steps": config.grpo_steps,
            "group_size": config.group_size,
        },
        "variants": variants,
        "training": training,
        "relative": {
            "accuracy_points": 100 * (method["accuracy"] - baseline["accuracy"]),
            "ndcg_at_5_percent": 100
            * (method["ndcg_at_5"] - baseline["ndcg_at_5"])
            / max(baseline["ndcg_at_5"], 1e-12),
            "badcase_reduction_percent": 100
            * (baseline["badcase_at_5"] - method["badcase_at_5"])
            / max(baseline["badcase_at_5"], 1e-12),
        },
        "paper_results": {
            "direct_bert_accuracy": 0.7441,
            "cascaded_bert_accuracy": 0.7558,
            "distilled_accuracy": 0.7622,
            "step_grpo_accuracy": 0.7648,
            "postcot_core_accuracy": 0.7706,
            "online_ndcg_at_5_percent": 0.20,
            "online_badcase_reduction_percent": 15.9,
        },
        "scope": (
            "实际训练 flat 三分类、High→(Mid/Low) 条件双头、SFT 后的逐 step "
            "group-normalized clipped GRPO，以及按 logsumexp 聚合三类 teacher logits "
            "的 PostCoT 双头蒸馏。MovieLens 用户画像/genre 构造可审计的三级序数相关性，"
            "替代美团 9 万私有 query-item 标注；未使用 Qwen3-14B 或生产 BERT。"
        ),
    }
