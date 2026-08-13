from __future__ import annotations

import math
import os
from pathlib import Path
import random

import numpy as np

from auto_research.runtime import device_for

from ..llm_training import require_torch, seed_everything
from .data import GenRecData, load_genrec_data, training_rows
from .model import GenRecConfig, GenRecRanker


def _padded(histories, width, torch, device):
    rows = []
    for history in histories:
        values = tuple(history[-width:])
        rows.append((values[0],) * (width - len(values)) + values)
    return torch.tensor(rows, dtype=torch.long, device=device)


def _train_baseline(data: GenRecData, config: GenRecConfig, seed: int):
    torch = require_torch()
    nn = torch.nn
    seed_everything(seed, torch)

    class DiscriminativeRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.items = nn.Embedding(len(data.item_texts), config.ranking_dimensions)
            self.encoder = nn.GRU(
                config.ranking_dimensions, config.ranking_dimensions, batch_first=True
            )

        def forward(self, histories):
            values, _ = self.encoder(self.items(histories))
            return values[:, -1] @ self.items.weight.T / math.sqrt(config.ranking_dimensions)

    device = device_for(torch)
    model = DiscriminativeRanker().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=8e-4)
    rows = training_rows(data, config.maximum_history)
    rng = random.Random(seed)
    losses = []
    model.train()
    # Match the GenRec number of observed examples, not its much larger parameter count.
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = _padded([row[0] for row in batch], config.maximum_history, torch, device)
        targets = torch.tensor([row[1] for row in batch], device=device)
        loss = torch.nn.functional.cross_entropy(model(histories), targets)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))

    def score(histories):
        model.eval()
        with torch.inference_mode():
            values = _padded(histories, config.maximum_history, torch, device)
            return model(values).float().cpu().numpy()

    return model, score, {
        "initial_loss": float(np.mean(losses[:6])),
        "final_loss": float(np.mean(losses[-6:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def _metrics(data: GenRecData, scorer, batch_size: int = 16):
    histories = [(*history, validation) for history, validation in zip(data.train, data.validation)]
    scores = []
    for start in range(0, len(histories), batch_size):
        scores.append(np.asarray(scorer(histories[start:start + batch_size])))
    scores = np.concatenate(scores)
    hits = ndcg = reciprocal_rank = 0.0
    recommendations = []
    for row, (history, target) in enumerate(zip(histories, data.test)):
        values = scores[row].copy()
        values[list(set(history))] = -np.inf
        order = np.argsort(-values)
        top = order[:10]
        recommendations.extend(top.tolist())
        positions = np.flatnonzero(order == target)
        if positions.size:
            rank = int(positions[0])
            reciprocal_rank += 1 / (rank + 1)
            if rank < 10:
                hits += 1
                ndcg += 1 / math.log2(rank + 2)
    head = set(np.argsort(-data.popularity)[: max(1, len(data.item_texts) // 10)].tolist())
    count = len(data.test)
    return {
        "hit_at_10": hits / count,
        "ndcg_at_10": ndcg / count,
        "mrr": reciprocal_rank / count,
        "head_share_at_10": sum(item in head for item in recommendations) / len(recommendations),
    }


def _relative(method, baseline):
    return {
        f"{key}_percent": 100 * (method[key] - baseline[key]) / max(abs(baseline[key]), 1e-12)
        for key in ("hit_at_10", "ndcg_at_10", "mrr", "head_share_at_10")
    }


def reproduce_genrec_netflix(dataset_dir: Path, seed: int = 42) -> dict:
    config = GenRecConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_GENREC_STEPS", "120")),
        batch_size=int(os.environ.get("AUTO_RESEARCH_GENREC_BATCH_SIZE", "2")),
    )
    data = load_genrec_data(
        dataset_dir,
        maximum_users=int(os.environ.get("AUTO_RESEARCH_GENREC_USERS", "240")),
        maximum_items=int(os.environ.get("AUTO_RESEARCH_GENREC_ITEMS", "500")),
    )
    _, baseline_scorer, baseline_training = _train_baseline(data, config, seed)
    baseline = {**baseline_training, **_metrics(data, baseline_scorer)}

    ranker = GenRecRanker(data, config, seed)
    genrec_training = ranker.train_phase2(seed)
    method = {**genrec_training, **_metrics(data, ranker.scores, config.evaluation_batch_size)}
    average_full_events = float(np.mean([len(history) for history in data.train]))
    average_used_events = float(
        np.mean([min(len(history), config.maximum_history) for history in data.train])
    )
    return {
        "paper": {
            "arxiv_id": "2608.10257",
            "title": "GenRec: An LLM-Backed Recommendation Ranker at Netflix",
            "url": "https://arxiv.org/abs/2608.10257",
            "organization": "Netflix",
        },
        "dataset": {
            "name": "MovieLens-1M",
            "users": len(data.train),
            "items": len(data.item_texts),
            "feedback": "chronological ratings >= 3",
        },
        "setup": {
            "seed": seed,
            "model": config.model_name,
            "steps_per_variant": config.steps,
            "examples_per_step": config.batch_size,
            "maximum_history_events": config.maximum_history,
            "average_available_history_events": average_full_events,
            "average_prefill_history_events": average_used_events,
        },
        "variants": {
            "ID-only discriminative ranker": baseline,
            "GenRec LoRA + catalog head + reward weighting": method,
        },
        "relative": _relative(method, baseline),
        "paper_results": {
            "offline_mrr_percent": 1.6,
            "phase2_data_reduction_factor": 40.0,
            "short_term_homepage_engagement_percent": 0.115,
            "short_term_p_value": 3.1e-10,
            "long_term_core_metric_percent": 0.006,
            "long_term_p_value": 0.025,
            "traffic_percent": 10.0,
            "duration_weeks": 4,
        },
        "scope": (
            "真实加载 SmolLM2-135M，向 causal LM 注入 q/v LoRA；把 MovieLens 标题、"
            "genre 与用户历史文本化，在同一 Phase-2 step 中联合优化 completion LM loss、"
            "全目录 ranking head 和 novelty/content-discovery reward-weighted loss，并以一次"
            "prefill 对全部公开目录打分。Netflix 内部 Phase-1 模型、私有 reward models、"
            "数十亿事件、vLLM 生产服务与真实长期满意度标签不可公开，未作伪造。"
        ),
    }
