"""Bounded public-data diagnostic: attributes/history replace private queries."""
from __future__ import annotations

from collections import defaultdict
import copy
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch

from auto_research.datasets import MOVIELENS_SHA256, MOVIELENS_URL, movielens_100k
from auto_research.reproductions.forte.experiment import parameter_digest
from .model import CoCoVAE, SIDPolicy, dhpo_loss, horizon, multi_positive_loss, prefix_rewards


def public_data(root: Path, max_users=64):
    events = defaultdict(list)
    for user, item, rating, stamp in movielens_100k(root):
        if rating >= 4:
            events[user].append((stamp, item, rating))
    splits = {name: [] for name in ("train", "validation", "test")}
    for user in sorted(events)[:max_users]:
        ratings = sorted(events[user])
        if len(ratings) < 8:
            continue
        training = ratings[:-2]
        for offset in range(3, len(training), 3):
            future = training[offset:offset + 3]
            splits["train"].append({"user": user, "history": [r[1] for r in training[:offset]][-24:],
                                    "positive": [r[1] for r in future],
                                    "reward": [2. if r[2] == 5 else 1. for r in future]})
        for name, index in (("validation", -2), ("test", -1)):
            splits[name].append({"user": user, "history": [r[1] for r in ratings[:index]][-24:],
                                 "positive": [ratings[index][1]]})
    if not all(splits.values()):
        raise ValueError("public temporal split has empty partitions")
    attributes = {}
    for line in (root / "ml-100k/u.item").read_text(encoding="latin-1").splitlines():
        row = line.split("|")
        # Public metadata only. No embeddings fitted on held-out interactions.
        title = np.zeros(32, dtype=np.float32)
        for character in row[1].lower():
            title[ord(character) % 32] += 1
        title /= max(1., title.sum())
        attributes[int(row[0])] = np.r_[np.array(row[5:], dtype=np.float32), title]
    items = sorted(attributes)
    features = torch.tensor(np.stack([attributes[item] for item in items]))
    metadata = {"public_id": "MovieLens-100K", "revision": MOVIELENS_SHA256, "source": MOVIELENS_URL,
                "ratings_sha256": hashlib.sha256((root / "ml-100k/u.data").read_bytes()).hexdigest(),
                "split": "per-user positive events in timestamp order, leave-last-two",
                "counts": {name: len(rows) for name, rows in splits.items()}, "max_users": max_users,
                "training_session": "three consecutive training-only positive events; prior 24 form context",
                "surrogate_reward": "rating 5 -> 2; rating 4 -> 1; not click/order labels",
                "attributes": "19 public genre flags + normalized 32-bin title character counts",
                "split_sha256": {name: hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
                                 for name, rows in splits.items()}}
    return splits, items, features, metadata


def run(root: Path, seed: int, *, device="cpu", max_users=64, tokenizer_steps=24,
        sft_steps=32, stage_steps=6, batch_size=16):
    if device not in {"cpu", "cuda"} or min(max_users, tokenizer_steps, sft_steps, stage_steps, batch_size) < 1:
        raise ValueError("positive bounded training budgets and cpu/cuda required")
    if max_users > 128 or tokenizer_steps > 100 or sft_steps > 100 or stage_steps > 20 or batch_size > 64:
        raise ValueError("budget exceeds the affordable diagnostic; review cost before expansion")
    started = time.monotonic()
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    splits, items, features, metadata = public_data(root, max_users)
    features = features.to(device)
    item_index = {item: index for index, item in enumerate(items)}
    train_items = sorted({item_index[item] for row in splits["train"]
                          for item in row["history"] + row["positive"]})
    tokenizer = CoCoVAE(features.shape[1]).to(device)
    before = parameter_digest(tokenizer)
    optimizer = torch.optim.AdamW(tokenizer.parameters(), lr=.002)
    tokenizer_trace = []
    for step in range(tokenizer_steps):
        selection = rng.choice(train_items, min(64, len(train_items)), replace=False)
        chosen = [splits["train"][int(index)] for index in rng.choice(len(splits["train"]), 32)]
        query = torch.stack([features[[item_index[item] for item in row["history"]]].mean(0) for row in chosen])
        positive = torch.stack([features[item_index[row["positive"][0]]] for row in chosen])
        neighbor = torch.stack([features[item_index[row["history"][-1]]] for row in chosen])
        optimizer.zero_grad(set_to_none=True)
        _, codes, objective, parts = tokenizer(features[selection])
        collaboration = tokenizer.collaborative_loss(query, positive, neighbor)
        loss = objective + collaboration
        loss.backward()
        torch.nn.utils.clip_grad_norm_(tokenizer.parameters(), 1.)
        optimizer.step()
        refreshed = tokenizer.refresh(codes.detach())
        tokenizer_trace.append({"step": step, "loss": float(loss.detach()),
                                **{key: float(value.detach()) for key, value in parts.items()},
                                "collaboration": float(collaboration.detach()), "refreshed_first_codes": refreshed})
    tokenizer.eval().requires_grad_(False)
    with torch.no_grad():
        representations, ids, _, _ = tokenizer(features)
    def context(row):
        return representations[[item_index[item] for item in row["history"]]].mean(0)

    def batch(rows):
        contexts = torch.stack([context(row) for row in rows])
        positive_ids = torch.zeros((len(rows), 3, 3), dtype=torch.long, device=device)
        values = torch.zeros((len(rows), 3), device=device)
        for j, row in enumerate(rows):
            count = len(row["positive"])
            positive_ids[j, :count] = ids[[item_index[item] for item in row["positive"]]]
            values[j, :count] = torch.tensor(row["reward"], device=device)
        return contexts, positive_ids, values

    def msft(model, contexts, positives, values):
        logp = model.log_prob(contexts.repeat_interleave(3, 0), positives.reshape(-1, 3))
        return multi_positive_loss(logp.reshape(len(contexts), 3, 3), values > 0)

    policy = SIDPolicy(representations.shape[1]).to(device)
    initial_digest = parameter_digest(policy)
    optimizer = torch.optim.AdamW(policy.parameters(), lr=.002)
    sft_trace = []
    for step in range(sft_steps):
        rows = [splits["train"][int(index)] for index in rng.choice(len(splits["train"]), batch_size)]
        contexts, positives, values = batch(rows)
        optimizer.zero_grad(set_to_none=True)
        loss = msft(policy, contexts, positives, values)
        loss.backward()
        optimizer.step()
        sft_trace.append(float(loss.detach()))
    initial = copy.deepcopy(policy.state_dict())
    arms = {"sft": policy}
    traces = {}
    for arm in ("exact-grpo", "dhpo"):
        torch.manual_seed(seed + 100)
        arm_rng = np.random.default_rng(seed + 100)
        model = SIDPolicy(representations.shape[1]).to(device)
        model.load_state_dict(initial)
        optimizer = torch.optim.AdamW(model.parameters(), lr=.0005)
        trace = []
        for step in range(3 * stage_steps):
            rows = [splits["train"][int(index)] for index in arm_rng.choice(len(splits["train"]), batch_size)]
            contexts, positives, values = batch(rows)
            active_horizon = horizon(step, stage_steps, 3) if arm == "dhpo" else 3
            samples, old_logp = model.sample(contexts, 4)
            rewards = prefix_rewards(samples, positives, values, horizon_length=active_horizon)
            logp = model.log_prob(contexts.repeat_interleave(4, 0), samples.reshape(-1, 3)).reshape(-1, 4, 3)
            optimizer.zero_grad(set_to_none=True)
            rl_loss = dhpo_loss(logp, old_logp, rewards, horizon_length=active_horizon)
            supervised = msft(model, contexts, positives, values)
            loss = rl_loss + .5 * supervised
            loss.backward()
            gradient = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 1.))
            optimizer.step()
            trace.append({"step": step, "horizon": active_horizon, "policy_loss": float(rl_loss.detach()),
                          "msft_loss": float(supervised.detach()), "gradient_norm": gradient,
                          "nonzero_reward_fraction": float((rewards > 0).float().mean()),
                          "nonconstant_reward_groups": int((rewards.std(-1, unbiased=False) > 0).sum())})
        traces[arm], arms[arm] = trace, model

    @torch.no_grad()
    def evaluate(model, rows):
        model.eval()
        reciprocal, hits = [], []
        for row in rows:
            scores = []
            for offset in range(0, len(ids), 256):
                sid = ids[offset:offset + 256]
                scores.append(model.log_prob(context(row)[None].expand(len(sid), -1), sid).sum(-1))
            scores = torch.cat(scores).cpu().numpy()
            scores[[item_index[item] for item in row["history"]]] = -np.inf
            # Stable item-ID tie rule: SID collisions are retained, not given
            # oracle disambiguation or favorable random tie breaks.
            order = np.argsort(-scores, kind="stable")
            rank = int(np.flatnonzero(order == item_index[row["positive"][0]])[0]) + 1
            reciprocal.append(1 / rank)
            hits.append(float(rank <= 10))
        return {"hr_at_10": float(np.mean(hits)), "mrr": float(np.mean(reciprocal)), "examples": len(rows)}

    validation = {arm: evaluate(model, splits["validation"]) for arm, model in arms.items()}
    selected = max(validation, key=lambda arm: validation[arm]["mrr"])
    # Only now read test targets for final reporting; never for selection.
    test = {arm: evaluate(model, splits["test"]) for arm, model in arms.items()}
    return {"method": "wegr", "seed": seed, "device": device, "diagnostic_only": True,
            "measured_locally": True, "evaluation_tier": "l2_public_dataset", "dataset": metadata,
            "checkpoint": {"public_id": "locally-initialized-two-layer-causal-transformer", "revision": "seeded-no-pretrained-weights"},
            "protocol": {"tokenizer_steps": tokenizer_steps, "sft_steps": sft_steps,
                         "stage_steps": stage_steps, "batch_size": batch_size, "group": 4,
                         "test_used_for_selection": False, "core_algorithms": "CoCo-VAE + DHPO + MSFT",
                         "teacher_or_reward_model": False, "tokenizer_fit": "training items and sessions only"},
            "tokenizer": {"training": tokenizer_trace, "parameters_changed": before != parameter_digest(tokenizer),
                          "unique_sids": len(ids.unique(dim=0)), "catalog_items": len(ids)},
            "sft": {"training_loss": sft_trace, "parameters_changed": initial_digest != parameter_digest(policy)},
            "arms": {arm: {"validation": validation[arm], "test": test[arm],
                            "parameters_changed_after_sft": any(not torch.equal(value, initial[key])
                                                                  for key, value in model.state_dict().items()),
                            "training": traces.get(arm, [])} for arm, model in arms.items()},
            "validation_selected_arm": selected, "elapsed_seconds": time.monotonic() - started,
            "limitations": ["MovieLens history and rating utility replace private query/click/order sessions.",
                            "Small random-initialized Transformer replaces GPT-2 Small; no pretrained language claim.",
                            "Public genre/title attributes replace private multimodal semantic features.",
                            "This is a bounded mechanism diagnostic, not stable improvement or production A/B reproduction.",
                            "SID collisions retain stable item-ID ties; no extra collision resolution learned."]}


def render(result):
    lines = ["# WeGR 公开数据核心机制诊断", "", "不代表微信线上 A/B 或论文级效果。", "",
             "| 对照 | Validation MRR | Test MRR | Test HR@10 |", "| --- | ---: | ---: | ---: |"]
    for name, arm in result["arms"].items():
        lines.append(f"| {name} | {arm['validation']['mrr']:.6f} | {arm['test']['mrr']:.6f} | {arm['test']['hr_at_10']:.6f} |")
    return "\n".join(lines + ["", f"仅按 validation 选择：{result['validation_selected_arm']}。", ""])
