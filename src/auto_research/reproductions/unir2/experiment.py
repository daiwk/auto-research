from __future__ import annotations

import random
from pathlib import Path

import numpy as np

from auto_research.runtime import device_for

from ..industrial_2026 import hierarchical_codes
from ..llm_training import require_torch, seed_everything
from ..recent_20260728_common import (
    full_catalog_metrics,
    load_recent_movielens,
    padded_histories,
    relative,
    training_rows,
)
from .model import UniR2Config, build_model


def _objective_labels(data, histories, candidates, positives):
    history_features = np.stack(
        [data.features[list(history)].mean(0) for history in histories]
    )
    candidate_features = data.features[candidates]
    affinity = (history_features * candidate_features).sum(-1)
    return np.stack((positives, (affinity > np.median(affinity)).astype(np.float32)), -1)


def _train(model, data, ids, config, seed):
    torch = require_torch()
    seed_everything(seed, torch)
    device = device_for(torch)
    model.to(device).train()
    rows = training_rows(data, config.maximum_history)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    for _ in range(config.steps):
        positives = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size // 2)]
        histories = [row[0] for row in positives] * 2
        candidates_np = np.asarray(
            [row[1] for row in positives]
            + [rng.randrange(data.item_count) for _ in positives]
        )
        positive_mask = np.asarray(
            [1.0] * len(positives) + [0.0] * len(positives), dtype=np.float32
        )
        history_tensor = padded_histories(
            histories, config.maximum_history, torch, device
        )
        candidates = torch.tensor(candidates_np, dtype=torch.long, device=device)
        generation, ranking = model(history_tensor, candidates)
        generation_loss = sum(
            torch.nn.functional.cross_entropy(
                logits[: len(positives)],
                torch.tensor(
                    ids[candidates_np[: len(positives)], level],
                    dtype=torch.long,
                    device=device,
                ),
            )
            for level, logits in enumerate(generation)
        )
        labels = torch.tensor(
            _objective_labels(data, histories, candidates_np, positive_mask),
            dtype=torch.float32,
            device=device,
        )
        ranking_loss = torch.nn.functional.binary_cross_entropy_with_logits(
            ranking, labels
        )
        loss = generation_loss + ranking_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def _catalog_scores(model, history, data, ids, config, torch):
    device = next(model.parameters()).device
    histories = padded_histories(
        [history] * data.item_count, config.maximum_history, torch, device
    )
    candidates = torch.arange(data.item_count, device=device)
    model.eval()
    with torch.inference_mode():
        generation, ranking = model(histories, candidates)
        sid_score = torch.zeros(data.item_count, device=device)
        for level, logits in enumerate(generation):
            sid_score += torch.log_softmax(logits, -1).gather(
                1,
                torch.tensor(ids[:, level], dtype=torch.long, device=device)[:, None],
            ).squeeze(1)
        score = torch.sigmoid(ranking[:, 0]) + 0.15 * sid_score
        return score.cpu().numpy()


def _recall_code_accuracy(model, data, ids, config, torch):
    device = next(model.parameters()).device
    correct = total = 0
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(data.train), 64):
            histories = padded_histories(
                data.train[start : start + 64],
                config.maximum_history,
                torch,
                device,
            )
            targets = np.asarray(data.validation[start : start + 64])
            candidates = torch.tensor(targets, dtype=torch.long, device=device)
            generation, _ = model(histories, candidates)
            for level, logits in enumerate(generation):
                correct += int(
                    (
                        logits.argmax(-1).cpu().numpy() == ids[targets, level]
                    ).sum()
                )
                total += len(targets)
    return correct / total


def reproduce_unir2(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_recent_movielens(dataset_dir)
    config = UniR2Config()
    ids = hierarchical_codes(
        data.features,
        levels=config.sid_levels,
        width=config.codebook_size,
        seed=seed,
    )
    rows = {}
    models = {}
    for name, unified in (("separate cascade", False), ("UniR2", True)):
        seed_everything(seed, torch)
        model = build_model(data, ids, config, unified=unified)
        training = _train(model, data, ids, config, seed)
        metrics = full_catalog_metrics(
            data,
            lambda history, model=model: _catalog_scores(
                model, history, data, ids, config, torch
            ),
        )
        rows[name] = {
            **training,
            **metrics,
            "sid_code_accuracy": _recall_code_accuracy(
                model, data, ids, config, torch
            ),
        }
        models[name] = model
    baseline, method = rows["separate cascade"], rows["UniR2"]
    return {
        "paper": {
            "arxiv_id": "2607.24439",
            "title": "Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence",
            "url": "https://arxiv.org/abs/2607.24439",
            "organization": "Kuaishou / IIE, CAS / UCAS",
        },
        "dataset": {
            "name": "MovieLens-1M",
            "users": len(data.train),
            "items": data.item_count,
        },
        "setup": {
            "seed": seed,
            "steps_per_model": config.steps,
            "sid_levels": config.sid_levels,
            "codebook_size": config.codebook_size,
            "ranking_objectives": ["next-item", "genre-affinity"],
        },
        "variants": rows,
        "relative": relative(
            {
                key: method[key]
                for key in ("hit_at_10", "ndcg_at_10", "sid_code_accuracy")
            },
            {
                key: baseline[key]
                for key in ("hit_at_10", "ndcg_at_10", "sid_code_accuracy")
            },
        ),
        "paper_results": {
            "kuaishou_play_volume_percent": 1.177,
            "kuaishou_follow_rate_percent": 0.655,
            "kuaishou_like_rate_percent": 2.560,
            "lite_gifting_users_percent": 0.717,
            "lite_gifting_intention_percent": 1.567,
            "lite_gifting_amount_percent": 2.569,
        },
        "scope": (
            "实际训练 Res-KMeans 两级 SID、统一异构序列、generation prefix-causal "
            "query、ranking mutual-visible query、共享 Q/K/V、ranking-only LoRA 与 "
            "stop-gradient，并和独立 recall/ranker cascade 做同数据全目录对照。"
            "MovieLens genre-affinity 代理快手 long-view/gift 等私有多目标，未复刻 "
            "8129 codebook、beam service、3×640 线上模型和 5% 流量实验。"
        ),
    }
