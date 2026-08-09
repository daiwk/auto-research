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
from .model import TokenMindsConfig, build_model, build_semantic_codes


def _train(model, data, codes, config, seed, *, dual_output):
    torch = require_torch()
    seed_everything(seed, torch)
    device = device_for(torch)
    model.to(device).train()
    rows = training_rows(data, config.maximum_history)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=config.learning_rate, weight_decay=1e-4
    )
    rank_losses, sid_losses = [], []
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories(
            [row[0] for row in batch], config.maximum_history, torch, device
        )
        target_values = np.asarray([row[1] for row in batch], dtype=np.int64)
        targets = torch.tensor(target_values, dtype=torch.long, device=device)
        ranking_logits, sid_logits = model(histories)
        rank_loss = torch.nn.functional.cross_entropy(ranking_logits, targets)
        sid_loss = torch.zeros((), device=device)
        if dual_output:
            target_codes = torch.tensor(codes[target_values], dtype=torch.long, device=device)
            sid_loss = sum(
                torch.nn.functional.cross_entropy(logits, target_codes[:, level])
                for level, logits in enumerate(sid_logits)
            ) / len(sid_logits)
        loss = rank_loss + config.sid_loss_weight * sid_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        rank_losses.append(float(rank_loss.detach().cpu()))
        if dual_output:
            sid_losses.append(float(sid_loss.detach().cpu()))
    return {
        "initial_ranking_loss": float(np.mean(rank_losses[:10])),
        "final_ranking_loss": float(np.mean(rank_losses[-10:])),
        "final_sid_loss": float(np.mean(sid_losses[-10:])) if sid_losses else None,
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def _scores(model, history, config, torch):
    device = next(model.parameters()).device
    values = padded_histories([history], config.maximum_history, torch, device)
    model.eval()
    with torch.inference_mode():
        return model(values)[0].squeeze(0).cpu().numpy()


def reproduce_tokenminds(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_recent_movielens(dataset_dir)
    config = TokenMindsConfig()
    codes = build_semantic_codes(data.features, config)

    seed_everything(seed, torch)
    baseline = build_model(data, codes, config, dual_output=False)
    baseline_training = _train(
        baseline, data, codes, config, seed, dual_output=False
    )
    baseline_metrics = full_catalog_metrics(
        data, lambda history: _scores(baseline, history, config, torch)
    )

    seed_everything(seed, torch)
    method = build_model(data, codes, config, dual_output=True)
    method_training = _train(method, data, codes, config, seed, dual_output=True)
    method_metrics = full_catalog_metrics(
        data, lambda history: _scores(method, history, config, torch)
    )

    return {
        "paper": {
            "arxiv_id": "2606.25147",
            "title": "TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems",
            "url": "https://arxiv.org/abs/2606.25147",
            "organization": "Google DeepMind / YouTube",
        },
        "dataset": {
            "name": "MovieLens-1M",
            "users": len(data.train),
            "items": data.item_count,
        },
        "setup": {
            "seed": seed,
            "steps_per_model": config.steps,
            "maximum_history": config.maximum_history,
            "sid_levels": config.sid_levels,
            "sid_cardinality": config.sid_cardinality,
            "same_split_optimizer_and_full_catalog": True,
        },
        "baseline": {"name": "dense-only sequential user encoder", **baseline_metrics},
        "method": {
            "name": "TokenMinds dense embedding + generated SID user tokens",
            **method_metrics,
        },
        "relative": relative(method_metrics, baseline_metrics),
        "training": {"baseline": baseline_training, "tokenminds": method_training},
        "paper_results": {
            "sfv_engaged_users_percent": 0.11,
            "sfv_satisfied_engagement_percent": 0.62,
            "training_compute_reduction_percent": 50,
            "serving_compute_reduction_percent": 31,
            "full_user_traffic": True,
        },
        "scope": (
            "实际训练共享序列编码器、dense 用户向量、逐层 SID 用户 token 预测头、"
            "可学习 token embedding 与下游融合排序。MovieLens genre 代理 YouTube 多模态"
            "视频内容，短序列代理 1,200 条行为；未复刻 Gemini 370M MoE encoder/decoder、"
            "CPT、LFV/SFV 私有日志、多 context beam decoding 和异步全流量服务。"
        ),
    }
