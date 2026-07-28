from __future__ import annotations

import random
from pathlib import Path

import numpy as np

from auto_research.runtime import device_for

from ..llm_training import require_torch, seed_everything
from ..recent_20260728_common import (
    full_catalog_metrics,
    load_recent_movielens,
    padded_histories,
    relative,
    training_rows,
)
from .model import MosaicConfig, build_model, cosine_redundancy


def _mrm_labels(data, targets):
    features = data.features[targets]
    columns = np.argsort(-data.features.sum(0))[:2]
    return (
        (features[:, columns[0]] > 0).astype(np.int64)
        + 2 * (features[:, columns[1]] > 0).astype(np.int64)
    )


def _train(model, data, config, seed, *, fleet):
    torch = require_torch()
    seed_everything(seed, torch)
    device = device_for(torch)
    model.to(device).train()
    rows = training_rows(data, config.maximum_history)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=config.learning_rate, weight_decay=1e-4
    )
    losses, redundancies, mrm_losses = [], [], []
    for step in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories(
            [row[0] for row in batch], config.maximum_history, torch, device
        )
        targets_np = np.asarray([row[1] for row in batch])
        targets = torch.tensor(targets_np, dtype=torch.long, device=device)
        if fleet:
            logits, specialists, mrm = model(histories, return_specialists=True)
            main = torch.nn.functional.cross_entropy(logits, targets)
            mrm_loss = torch.nn.functional.cross_entropy(
                mrm,
                torch.tensor(
                    _mrm_labels(data, targets_np), dtype=torch.long, device=device
                ),
            )
            redundancy = cosine_redundancy(specialists, torch)
            warmup = min(1.0, step / max(config.steps // 3, 1))
            loss = (
                main
                + 0.15 * mrm_loss
                + warmup * config.redundancy_weight * redundancy
            )
            redundancies.append(float(redundancy.detach().cpu()))
            mrm_losses.append(float(mrm_loss.detach().cpu()))
        else:
            loss = torch.nn.functional.cross_entropy(model(histories), targets)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
        "final_cosine_redundancy": float(np.mean(redundancies[-10:]))
        if redundancies
        else None,
        "final_mrm_loss": float(np.mean(mrm_losses[-10:])) if mrm_losses else None,
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }

def _scores(model, history, config, torch):
    device = next(model.parameters()).device
    values = padded_histories([history], config.maximum_history, torch, device)
    model.eval()
    with torch.inference_mode():
        return model(values).squeeze(0).cpu().numpy()


def reproduce_mosaic(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_recent_movielens(dataset_dir)
    config = MosaicConfig()
    seed_everything(seed, torch)
    baseline = build_model(data, config, fleet=False)
    baseline_training = _train(baseline, data, config, seed, fleet=False)
    baseline_metrics = full_catalog_metrics(
        data, lambda history: _scores(baseline, history, config, torch)
    )
    seed_everything(seed, torch)
    method = build_model(data, config, fleet=True)
    method_training = _train(method, data, config, seed, fleet=True)
    method_metrics = full_catalog_metrics(
        data, lambda history: _scores(method, history, config, torch)
    )
    return {
        "paper": {
            "arxiv_id": "2607.24015",
            "title": "Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta",
            "url": "https://arxiv.org/abs/2607.24015",
            "organization": "Meta",
        },
        "dataset": {
            "name": "MovieLens-1M",
            "users": len(data.train),
            "items": data.item_count,
        },
        "setup": {
            "seed": seed,
            "steps_per_model": config.steps,
            "specialists": [
                "memorization",
                "dense-heavy",
                "sequential",
                "CoTrain-MoE",
            ],
            "same_split_and_full_catalog": True,
        },
        "baseline": {
            "name": "single sequential user embedding",
            **baseline_metrics,
        },
        "method": {"name": "Mosaic fleet + MRM + CRL", **method_metrics},
        "relative": relative(method_metrics, baseline_metrics),
        "training": {
            "baseline": baseline_training,
            "mosaic": method_training,
        },
        "paper_results": {
            "surface_1_percent": 0.10,
            "surface_2_percent": 0.15,
            "surface_3_percent": 0.28,
            "gpu_serving_reduction_percent": 79,
            "coevaluation_speedup": "3-5x",
        },
        "scope": (
            "实际训练 memorization、dense-heavy、GRU sequential 与 routed CoTrain-MoE "
            "四种 specialist，执行二任务笛卡尔积 MRM 辅助分类、warm-up cosine "
            "redundancy loss 和下游全目录排序。MovieLens genre/popularity 代理 Meta "
            "私有多表面行为标签；未复刻 HSTU 2048、跨产品特征、CoEval 与线上混合 serving。"
        ),
    }
