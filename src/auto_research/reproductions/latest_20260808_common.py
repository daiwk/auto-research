from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random

import numpy as np

from auto_research.runtime import device_for

from .llm_training import require_torch, seed_everything
from .recent_20260728_common import (
    full_catalog_metrics,
    load_recent_movielens,
    padded_histories,
    relative,
    training_rows,
)


@dataclass(frozen=True)
class Config:
    dimensions: int = 32
    maximum_history: int = 24
    steps: int = 50
    batch_size: int = 48
    learning_rate: float = 8e-4
    rollout_candidates: int = 24


def _model(data, config: Config, *, ranker: bool):
    torch = require_torch()
    nn = torch.nn

    class GenerateRank(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.encoder = nn.GRU(
                config.dimensions, config.dimensions, batch_first=True
            )
            self.norm = nn.LayerNorm(config.dimensions)
            self.ranker = (
                nn.Sequential(
                    nn.Linear(3 * config.dimensions, 2 * config.dimensions),
                    nn.SiLU(),
                    nn.Linear(2 * config.dimensions, 1),
                )
                if ranker
                else None
            )

        def encode(self, histories):
            values, _ = self.encoder(self.item(histories))
            return self.norm(values[:, -1])

        def generation_scores(self, context):
            return context @ self.item.weight.T

        def ranking_scores(self, context, candidates=None):
            if self.ranker is None:
                return self.generation_scores(context)
            items = self.item.weight if candidates is None else self.item(candidates)
            if candidates is None:
                items = items.unsqueeze(0).expand(context.shape[0], -1, -1)
            context = context.unsqueeze(1).expand(-1, items.shape[1], -1)
            return self.ranker(
                torch.cat((context, items, context * items), dim=-1)
            ).squeeze(-1)

        def forward(self, histories):
            context = self.encode(histories)
            return self.generation_scores(context), self.ranking_scores(context)

    return GenerateRank()


def _train_teacher(data, config, seed):
    torch = require_torch()
    device = device_for(torch)
    seed_everything(seed + 101, torch)
    teacher = _model(data, config, ranker=True).to(device).train()
    rows = training_rows(data, config.maximum_history)
    rng = random.Random(seed + 101)
    optimizer = torch.optim.AdamW(teacher.parameters(), lr=config.learning_rate)
    for _ in range(config.steps * 2):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories(
            [row[0] for row in batch], config.maximum_history, torch, device
        )
        targets = torch.tensor([row[1] for row in batch], device=device)
        _, scores = teacher(histories)
        loss = torch.nn.functional.cross_entropy(scores, targets)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(teacher.parameters(), 1.0)
        optimizer.step()
    return teacher.eval()


def _train_gryphon(model, teacher, data, config, seed, *, distill):
    torch = require_torch()
    device = next(model.parameters()).device
    rows = training_rows(data, config.maximum_history)
    rng = random.Random(seed)
    generator = torch.Generator(device=device).manual_seed(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses, rollout_updates, impression_updates = [], 0, 0
    model.train()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories(
            [row[0] for row in batch], config.maximum_history, torch, device
        )
        targets = torch.tensor([row[1] for row in batch], device=device)
        generation, ranking = model(histories)
        loss = torch.nn.functional.cross_entropy(generation, targets)
        if distill:
            with torch.no_grad():
                teacher_context = teacher.encode(histories)
                teacher_all = teacher.ranking_scores(teacher_context)
                rollout = generation.topk(config.rollout_candidates, dim=-1).indices
                random_items = torch.randint(
                    data.item_count,
                    (len(batch), config.rollout_candidates - 1),
                    generator=generator,
                    device=device,
                )
                impressions = torch.cat((targets[:, None], random_items), dim=1)
            rollout_student = ranking.gather(1, rollout)
            rollout_teacher = teacher_all.gather(1, rollout)
            impression_student = ranking.gather(1, impressions)
            impression_teacher = teacher_all.gather(1, impressions)
            loss = loss + torch.nn.functional.l1_loss(
                rollout_student, rollout_teacher
            ) + torch.nn.functional.l1_loss(
                impression_student, impression_teacher
            )
            rollout_updates += int(rollout.numel())
            impression_updates += int(impressions.numel())
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:8])),
        "final_loss": float(np.mean(losses[-8:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "rollout_distillation_targets": rollout_updates,
        "impression_distillation_targets": impression_updates,
        "device": device.type,
    }


def _score(model, history, config, *, ranking, rerank_diversity=False):
    torch = require_torch()
    device = next(model.parameters()).device
    histories = padded_histories([history], config.maximum_history, torch, device)
    model.eval()
    with torch.inference_mode():
        generation, ranked = model(histories)
        scores = (ranked if ranking else generation)[0].cpu().numpy()
        if not rerank_diversity:
            return scores
        embeddings = model.item.weight.detach().cpu().numpy()
    candidates = np.argsort(-scores)[: min(80, len(scores))]
    normalized = embeddings / np.maximum(
        np.linalg.norm(embeddings, axis=1, keepdims=True), 1e-8
    )
    selected: list[int] = []
    remaining = candidates.tolist()
    adjusted = np.full_like(scores, -np.inf, dtype=np.float64)
    while remaining:
        best = max(
            remaining,
            key=lambda item: scores[item]
            - 0.12 * max(
                (float(normalized[item] @ normalized[old]) for old in selected),
                default=0.0,
            ),
        )
        adjusted[best] = len(remaining)
        selected.append(best)
        remaining.remove(best)
    return adjusted


def reproduce_gryphon_v2(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_recent_movielens(dataset_dir, maximum_users=260, maximum_items=420)
    config = Config()
    teacher = _train_teacher(data, config, seed)
    variants = {}
    for name, use_ranker in (
        ("generative retrieval", False),
        ("gryphon-v2 rollout distillation", True),
    ):
        seed_everything(seed, torch)
        model = _model(data, config, ranker=use_ranker).to(device_for(torch))
        training = _train_gryphon(
            model, teacher, data, config, seed, distill=use_ranker
        )
        variants[name] = {
            **training,
            **full_catalog_metrics(
                data,
                lambda history, model=model, rank=use_ranker: _score(
                    model, history, config, ranking=rank
                ),
            ),
        }
    baseline, method = variants.values()
    return {
        "paper": {
            "arxiv_id": "2608.06213",
            "title": "Gryphon-v2",
            "url": "https://arxiv.org/abs/2608.06213",
            "organization": "Yandex",
        },
        "dataset": {
            "name": "MovieLens-1M",
            "users": len(data.train),
            "items": data.item_count,
        },
        "setup": {"seed": seed, "steps_per_student": config.steps},
        "variants": variants,
        "relative": relative(
            {key: method[key] for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10")},
            {key: baseline[key] for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10")},
        ),
        "paper_results": {
            "active_users_percent": 1.41,
            "teacher_recall_at_10": 0.5654,
            "weighted_pair_accuracy": 0.5892,
        },
        "scope": "实际训练共享 history encoder、生成头、训练期高容量 teacher、当前生成器 rollout 与 logged-impression 双来源 MAE 蒸馏，并由 item-level ranker 给出最终顺序；未复刻 Yandex 私有音频/文本 SID、8000 长历史、在线十分钟更新和生产 Triton 服务。",
    }


def _train_degr(model, data, config, seed, *, adaptive):
    torch = require_torch()
    device = next(model.parameters()).device
    rows = training_rows(data, config.maximum_history)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses, preference_updates, diversity_updates = [], 0, 0
    model.train()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories(
            [row[0] for row in batch], config.maximum_history, torch, device
        )
        targets = torch.tensor([row[1] for row in batch], device=device)
        generation, _ = model(histories)
        ce = torch.nn.functional.cross_entropy(generation, targets)
        loss = ce
        if adaptive:
            cohort = generation.topk(8, dim=-1).indices
            cohort_embeddings = model.item(cohort)
            normalized = torch.nn.functional.normalize(cohort_embeddings, dim=-1)
            similarity = normalized @ normalized.transpose(1, 2)
            mask = torch.triu(torch.ones_like(similarity), diagonal=1)
            diversity = ((similarity.square() * mask).sum() / mask.sum().clamp_min(1))
            negative = cohort[:, 0]
            positive_score = generation.gather(1, targets[:, None]).squeeze(1)
            negative_score = generation.gather(1, negative[:, None]).squeeze(1)
            reward_gap = 1.0 + 0.2 * (
                data.popularity[targets.detach().cpu().numpy()]
                < data.popularity[negative.detach().cpu().numpy()]
            )
            reward_weight = torch.tensor(
                reward_gap, dtype=generation.dtype, device=device
            )
            log_odds = positive_score - negative_score
            ar_orpo = (
                reward_weight * torch.nn.functional.softplus(-log_odds)
            ).mean()
            loss = ce + 0.08 * diversity + 0.25 * ar_orpo
            preference_updates += len(batch)
            diversity_updates += int(mask.sum().item())
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:8])),
        "final_loss": float(np.mean(losses[-8:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "adaptive_reward_orpo_updates": preference_updates,
        "diversity_pair_updates": diversity_updates,
        "device": device.type,
    }


def reproduce_degr(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_recent_movielens(dataset_dir, maximum_users=260, maximum_items=420)
    config = Config()
    variants = {}
    for name, adaptive in (
        ("cross-entropy generator", False),
        ("degr ce + diversity + ar-orpo", True),
    ):
        seed_everything(seed, torch)
        model = _model(data, config, ranker=False).to(device_for(torch))
        training = _train_degr(model, data, config, seed, adaptive=adaptive)
        variants[name] = {
            **training,
            **full_catalog_metrics(
                data,
                lambda history, model=model, adaptive=adaptive: _score(
                    model,
                    history,
                    config,
                    ranking=False,
                    rerank_diversity=adaptive,
                ),
            ),
        }
    baseline, method = variants.values()
    return {
        "paper": {
            "arxiv_id": "2608.04809",
            "title": "DEGR",
            "url": "https://arxiv.org/abs/2608.04809",
            "organization": "JD.com",
        },
        "dataset": {
            "name": "MovieLens-1M",
            "users": len(data.train),
            "items": data.item_count,
        },
        "setup": {"seed": seed, "steps_per_model": config.steps},
        "variants": variants,
        "relative": relative(
            {key: method[key] for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10")},
            {key: baseline[key] for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10")},
        ),
        "paper_results": {"uctr_percent": 1.22, "pv_percent": 0.20},
        "scope": "实际联合训练 next-item CE、cohort 内 embedding 相似度平方约束与 reward-weighted ORPO，并执行多样性感知 greedy 重排；公开 MovieLens 没有跨 request 页面曝光与京东探索 reward，故以流行度逆向权重代理探索价值，未复刻私有十亿请求 reward model。",
    }


def render_latest(result: dict) -> str:
    lines = [
        f"# {result['paper']['title']}",
        "",
        f"公开数据：{result['dataset']['name']}（{result['dataset']['users']} users / {result['dataset']['items']} items）。",
        "",
        "| Variant | Hit@10 | NDCG@10 | Head share@10 | Params |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        lines.append(
            f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} | "
            f"{row['head_share_at_10']:.4f} | {row['parameters']} |"
        )
    lines += [
        "",
        f"相对同预算基线：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。",
        "",
        "## 复现边界",
        "",
        result["scope"],
        "",
    ]
    return "\n".join(lines)
