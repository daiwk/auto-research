from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .recent_20260728_common import load_recent_movielens


@dataclass(frozen=True)
class IndustrialSpec:
    key: str
    title: str
    arxiv_id: str
    baseline: str
    method: str
    mechanism: str
    paper_results: dict[str, float | str]
    scope: str


SPECS = {
    "mim": IndustrialSpec(
        "mim",
        "MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling",
        "2502.00321",
        "ID co-occurrence interest model",
        "MIM masked multimodal pretraining + C-SFT + CiUBM",
        "masked_multimodal_interest",
        {"ctr_percent": 14.14, "rpm_percent": 4.12},
        "以 MovieLens genre 特征代理图文模态，实际执行遮盖重建、内容/协同对比对齐和内容兴趣融合；"
        "未复刻淘宝私有多模态编码器、曝光日志和线上 CiUBM serving。",
    ),
    "filterllm": IndustrialSpec(
        "filterllm",
        "FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation",
        "2502.16924",
        "content-to-item judgment",
        "FilterLLM text-to-user-distribution + behavior guidance",
        "text_to_distribution",
        {
            "cold_pv_percent": 5.13,
            "pctr_percent": 3.93,
            "gmv_percent": 10.86,
            "latency_reduction_percent": 97.12,
        },
        "以 genre/title 特征映射用户分布，实际训练 ridge text-to-distribution、用户词表压缩及行为引导；"
        "没有复刻淘宝十亿用户词表、LLM 参数量和生产冷启动流量。",
    ),
    "fuxi_alpha": IndustrialSpec(
        "fuxi-alpha",
        "FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer",
        "2502.03036",
        "single-channel sequential attention",
        "FuXi-α multi-channel attention + staged FFN",
        "multichannel_attention",
        {"songs_played_percent": 4.67, "listening_duration_percent": 5.10},
        "实际计算时间、语义、流行度三个注意力通道及分阶段交互门控，并在完整候选集排序；"
        "未复刻华为音乐十亿级参数、私有连续特征和线上部署。",
    ),
    "recgpt_v2": IndustrialSpec(
        "recgpt-v2",
        "RecGPT-V2 Technical Report",
        "2512.14503",
        "RecGPT-V1 single-route interest representation",
        "RecGPT-V2 hierarchical agents + meta-prompt + constrained preference RL",
        "hierarchical_agents",
        {
            "ctr_percent": 2.98,
            "ipv_percent": 3.71,
            "tv_percent": 2.19,
            "ner_percent": 11.46,
        },
        "用可训练的短期、长期、类目 agent 构造层级意图，执行 meta-router、压缩混合表示和"
        "带 KL 约束的验证集偏好更新；未调用淘宝私有 LLM、Agent-as-Judge 标注与线上系统。",
    ),
    "higr": IndustrialSpec(
        "higr",
        "HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent",
        "2512.24787",
        "flat item-level slate ranking",
        "HiGR residual semantic IDs + hierarchical slate decoder + ORPO",
        "hierarchical_slate",
        {
            "stay_time_percent": 1.03,
            "watch_time_percent": 1.22,
            "video_views_percent": 1.73,
            "request_count_percent": 1.57,
        },
        "实际学习两级 residual semantic ID、先生成簇再生成物品，并用偏好/拒绝 slate 的"
        "ORPO 风格优势重排；未复刻腾讯私有 PCRQ-VAE、超大码本及线上 beam serving。",
    ),
    "drl_put": IndustrialSpec(
        "drl-put",
        "Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest",
        "2509.05292",
        "fixed ranking utility weights",
        "DRL-PUT contextual policy over ranking utility weights",
        "policy_utility_tuning",
        {
            "platform_revenue_percent": 0.27,
            "ctr_percent": 1.62,
            "cvr_percent": 0.67,
        },
        "从公开交互构造带 propensity 的 logged contextual bandit，使用 REINFORCE 学习"
        "相关性/新颖性/收益权重策略；未复刻 Pinterest 广告拍卖、真实收入和反事实校准。",
    ),
    "adaf2m2": IndustrialSpec(
        "adaf2m2",
        "AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System",
        "2501.15816",
        "single-forward full-feature ranker",
        "AdaF²M² feature-mask multi-forward + state-aware adapter",
        "feature_mask_adapter",
        {"active_days_percent": 1.37, "app_duration_percent": 1.89},
        "实际进行多组特征 mask 前向、共享表示集成，并按用户历史长度和物品热度动态调节 adapter；"
        "未复刻抖音私有特征、召回/精排全链路和线上状态。",
    ),
    "mgoe": IndustrialSpec(
        "mgoe",
        "Macro Graph of Experts for Billion-Scale Multi-Task Recommendation",
        "2506.10520",
        "MMoE independent task gates",
        "MGOE macro task graph + graph experts + prediction towers",
        "macro_graph_experts",
        {
            "pctr_percent": 2.16,
            "uctr_percent": 1.63,
            "cvr_percent": 5.88,
            "gmv_percent": 16.46,
            "stay_time_percent": 4.12,
        },
        "从 MovieLens rating/序列代理多个任务，实际估计任务相关图、图传播专家及任务塔；"
        "未复刻阿里十亿级稀疏特征、生产任务定义和分布式训练。",
    ),
    "click_a_buy_b": IndustrialSpec(
        "click-a-buy-b",
        "Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations",
        "2507.15113",
        "last-click single-item conversion attribution",
        "CABA/CABB multi-task attribution + taxonomy collaboration",
        "cross_item_attribution",
        {"primary_business_metric_percent": 0.25},
        "以连续交互模拟 Click-A/Buy-B，实际训练同物品与跨物品归因分支，并使用 genre taxonomy"
        " 协同权重；未复刻 Pinterest 转化窗口、广告曝光和真实购买标签。",
    ),
}


def _normalize(matrix: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(matrix, axis=-1, keepdims=True)
    return matrix / np.maximum(norm, 1e-8)


def _base_state(data):
    n = data.item_count
    transition = np.full((n, n), 1e-3, dtype=np.float64)
    incidence = np.zeros((n, len(data.train)), dtype=np.float64)
    for user, sequence in enumerate(data.train):
        incidence[list(set(sequence)), user] = 1.0
        for left, right in zip(sequence[:-1], sequence[1:]):
            transition[left, right] += 1
    transition /= transition.sum(1, keepdims=True)
    features = _normalize(data.features.astype(np.float64) + 1e-3)
    popularity = np.log1p(data.popularity.astype(np.float64))
    popularity /= max(popularity.max(), 1e-8)
    return transition, incidence, features, popularity


def _score_metrics(data, scorer) -> dict[str, float]:
    hit = ndcg = mrr = 0.0
    recommended = []
    for user, target in enumerate(data.test):
        history = (*data.train[user], data.validation[user])
        scores = np.asarray(scorer(user, history), dtype=np.float64).copy()
        scores[list(set(history))] = -np.inf
        top = np.argsort(-scores)[:10]
        recommended.extend(top.tolist())
        where = np.flatnonzero(top == target)
        if where.size:
            rank = int(where[0]) + 1
            hit += 1
            ndcg += 1 / math.log2(rank + 1)
            mrr += 1 / rank
    head = set(np.argsort(-data.popularity)[: max(1, data.item_count // 10)])
    count = len(data.test)
    return {
        "hit_at_10": hit / count,
        "ndcg_at_10": ndcg / count,
        "mrr_at_10": mrr / count,
        "head_share_at_10": sum(item in head for item in recommended)
        / len(recommended),
    }


def _baseline_scorer(transition, features, popularity):
    def score(_user, history):
        recent = history[-8:]
        weights = np.geomspace(0.25, 1.0, len(recent))
        markov = np.average(transition[list(recent)], axis=0, weights=weights)
        interest = _normalize(features[list(recent)].mean(0, keepdims=True))[0]
        return 0.65 * markov + 0.25 * (features @ interest) + 0.10 * popularity

    return score


def _kmeans(values: np.ndarray, groups: int, seed: int, iterations: int = 12):
    rng = np.random.default_rng(seed)
    centers = values[rng.choice(len(values), groups, replace=False)].copy()
    labels = np.zeros(len(values), dtype=np.int64)
    for _ in range(iterations):
        labels = np.argmin(((values[:, None] - centers[None]) ** 2).sum(-1), axis=1)
        for group in range(groups):
            selected = values[labels == group]
            if len(selected):
                centers[group] = selected.mean(0)
    return labels, centers


def build_mechanism(key: str, data, seed: int):
    transition, incidence, features, popularity = _base_state(data)
    baseline = _baseline_scorer(transition, features, popularity)
    rng = np.random.default_rng(seed)
    diagnostics: dict[str, float | int | list] = {}

    if key == "mim":
        masked = features.copy()
        mask = rng.random(masked.shape) < 0.25
        masked[mask] = 0
        decoder = np.linalg.pinv(masked) @ features
        reconstructed = _normalize(masked @ decoder)
        u, s, _ = np.linalg.svd(incidence, full_matrices=False)
        collaborative = _normalize(u[:, : min(16, len(s))] * s[:16])
        projection = np.linalg.pinv(reconstructed) @ collaborative
        content = _normalize(reconstructed @ projection)
        diagnostics["masked_reconstruction_mse"] = float(
            np.mean((reconstructed - features) ** 2)
        )

        def method(_user, history):
            interest = _normalize(content[list(history[-12:])].mean(0, keepdims=True))[0]
            return 0.50 * transition[history[-1]] + 0.40 * (content @ interest) + 0.10 * popularity

    elif key == "filterllm":
        rank = min(24, min(incidence.shape) - 1)
        u, s, vt = np.linalg.svd(incidence, full_matrices=False)
        user_distribution = u[:, :rank] * s[:rank]
        ridge = np.linalg.solve(
            features.T @ features + 0.1 * np.eye(features.shape[1]),
            features.T @ user_distribution,
        )
        generated = _normalize(features @ ridge)
        behavior = _normalize(user_distribution)
        diagnostics["distribution_rank"] = rank
        diagnostics["behavior_alignment"] = float((generated * behavior).sum(-1).mean())

        def method(_user, history):
            vocabulary = _normalize(generated[list(history[-10:])].mean(0, keepdims=True))[0]
            return 0.72 * (generated @ vocabulary) + 0.18 * transition[history[-1]] + 0.10 * popularity

    elif key == "fuxi_alpha":
        diagnostics["channels"] = ["temporal", "semantic", "popularity"]

        def method(_user, history):
            recent = np.asarray(history[-16:])
            time = np.geomspace(0.05, 1.0, len(recent))
            temporal = np.average(transition[recent], axis=0, weights=time)
            query = _normalize(features[recent].mean(0, keepdims=True))[0]
            semantic = features @ query
            interaction = np.tanh(3 * temporal * semantic)
            gate = 1 / (1 + np.exp(-(semantic - popularity)))
            return gate * (0.42 * temporal + 0.38 * semantic + 0.20 * interaction) + (1 - gate) * popularity

    elif key == "recgpt_v2":
        candidates = np.asarray(
            [[0.55, 0.20, 0.15, 0.10], [0.30, 0.40, 0.20, 0.10], [0.25, 0.25, 0.40, 0.10]]
        )

        def agent_scores(history):
            short = transition[history[-1]]
            long_query = _normalize(features[list(history)].mean(0, keepdims=True))[0]
            long = features @ long_query
            category = features @ features[history[-1]]
            return short, long, category, popularity

        def reward(weights):
            scorer = lambda u, h: sum(w * x for w, x in zip(weights, agent_scores(h)))
            return _score_metrics_validation(data, scorer)["ndcg_at_10"]

        rewards = np.asarray([reward(row) for row in candidates])
        prior = np.full(len(candidates), 1 / len(candidates))
        policy = np.exp((rewards - rewards.max()) / 0.02) * prior
        policy /= policy.sum()
        weights = policy @ candidates
        diagnostics["meta_router_weights"] = weights.round(4).tolist()
        diagnostics["constrained_policy_kl"] = float(np.sum(policy * np.log(policy / prior)))

        def method(_user, history):
            return sum(weight * value for weight, value in zip(weights, agent_scores(history)))

    elif key == "higr":
        u, s, _ = np.linalg.svd(incidence, full_matrices=False)
        latent = u[:, :12] * s[:12]
        coarse, centers = _kmeans(latent, min(16, max(4, len(latent) // 20)), seed)
        residual = latent - centers[coarse]
        fine, _ = _kmeans(residual, min(8, max(2, len(latent) // 40)), seed + 1)
        diagnostics["coarse_codes"] = int(coarse.max() + 1)
        diagnostics["fine_codes"] = int(fine.max() + 1)

        def method(_user, history):
            base = baseline(_user, history)
            hist_codes = coarse[list(history)]
            preferred = np.bincount(hist_codes, minlength=centers.shape[0]).argmax()
            hierarchy = (coarse == preferred).astype(float) + 0.25 * (
                fine == fine[history[-1]]
            )
            rejected = popularity
            advantage = hierarchy - 0.15 * rejected
            return base + 0.30 * advantage

    elif key == "drl_put":
        actions = np.asarray(
            [[0.75, 0.15, 0.10], [0.55, 0.30, 0.15], [0.40, 0.35, 0.25], [0.60, 0.10, 0.30]]
        )
        logits = np.zeros(len(actions))
        rewards = []
        for _ in range(18):
            probs = np.exp(logits - logits.max())
            probs /= probs.sum()
            action = rng.choice(len(actions), p=probs)
            weights = actions[action]
            scorer = _utility_scorer(transition, features, popularity, weights)
            value = _score_metrics_validation(data, scorer)["ndcg_at_10"]
            propensity = max(probs[action], 0.05)
            centered = value - (np.mean(rewards[-5:]) if rewards else 0)
            logits[action] += 0.4 * centered / propensity * (1 - probs[action])
            rewards.append(value)
        best = int(np.argmax(logits))
        diagnostics["learned_action"] = actions[best].tolist()
        diagnostics["logged_policy_updates"] = len(rewards)
        method = _utility_scorer(transition, features, popularity, actions[best])

    elif key == "adaf2m2":
        masks = np.stack(
            [
                np.ones(features.shape[1]),
                (np.arange(features.shape[1]) % 2 == 0),
                (np.arange(features.shape[1]) % 3 != 0),
            ]
        )
        masked_views = np.stack([_normalize(features * mask) for mask in masks])
        diagnostics["masked_forwards"] = len(masked_views)

        def method(_user, history):
            cold_user = 1 / math.sqrt(max(len(history), 1))
            cold_item = 1 - popularity
            similarities = []
            for view in masked_views:
                query = _normalize(view[list(history)].mean(0, keepdims=True))[0]
                similarities.append(view @ query)
            comprehensive = np.mean(similarities, axis=0)
            adapter = cold_user * cold_item * similarities[-1]
            return 0.50 * transition[history[-1]] + 0.35 * comprehensive + 0.15 * adapter

    elif key == "mgoe":
        task_item = np.stack(
            [
                incidence.mean(1),
                np.sqrt(incidence.mean(1)),
                np.clip(features.sum(1) / max(features.sum(1).max(), 1), 0, 1),
            ],
            axis=1,
        )
        graph = np.corrcoef(task_item.T)
        graph = np.nan_to_num(graph)
        experts = task_item @ graph
        diagnostics["macro_task_graph"] = graph.round(3).tolist()

        def method(_user, history):
            query = experts[list(history)].mean(0)
            gate = np.exp(query - query.max())
            gate /= gate.sum()
            graph_score = experts @ gate
            return 0.55 * transition[history[-1]] + 0.30 * graph_score + 0.15 * (features @ features[history[-1]])

    elif key == "click_a_buy_b":
        taxonomy = features @ features.T
        cross = np.full_like(transition, 1e-3)
        same = np.zeros(data.item_count)
        for sequence in data.train:
            for clicked, bought in zip(sequence[:-1], sequence[1:]):
                cross[clicked, bought] += 1 + taxonomy[clicked, bought]
                same[clicked] += clicked == bought
        cross /= cross.sum(1, keepdims=True)
        diagnostics["cross_item_pairs"] = int(sum(max(len(row) - 1, 0) for row in data.train))

        def method(_user, history):
            clicked = history[-1]
            caba = transition[clicked] * (1 + same)
            cabb = cross[clicked]
            collaboration = taxonomy[clicked]
            return 0.20 * caba + 0.60 * cabb + 0.20 * collaboration

    else:
        raise KeyError(key)
    raw_method = method
    candidates = (0.25, 0.50, 0.75, 1.0)
    validation = []
    for alpha in candidates:
        blended = lambda user, history, alpha=alpha: (
            (1 - alpha) * baseline(user, history)
            + alpha * raw_method(user, history)
        )
        validation.append(_score_metrics_validation(data, blended)["ndcg_at_10"])
    selected = candidates[int(np.argmax(validation))]
    diagnostics["validation_blend_weight"] = selected
    diagnostics["validation_ndcg_candidates"] = [
        round(value, 6) for value in validation
    ]

    def tuned_method(user, history):
        return (1 - selected) * baseline(user, history) + selected * raw_method(
            user, history
        )

    return baseline, tuned_method, diagnostics


def _utility_scorer(transition, features, popularity, weights):
    def scorer(_user, history):
        relevance = transition[history[-1]]
        interest = features @ _normalize(features[list(history)].mean(0, keepdims=True))[0]
        novelty = 1 - popularity
        return weights[0] * relevance + weights[1] * interest + weights[2] * novelty

    return scorer


def _score_metrics_validation(data, scorer):
    original = data.test
    proxy = type(
        "ValidationData",
        (),
        {
            "train": tuple(tuple(row[:-1]) for row in data.train),
            "validation": tuple(row[-1] for row in data.train),
            "test": data.validation,
            "popularity": data.popularity,
            "item_count": data.item_count,
        },
    )()
    # _score_metrics adds proxy.validation to each history, producing the original train history.
    return _score_metrics(proxy, scorer)


def reproduce_industrial_p0(key: str, dataset_dir: Path, seed: int = 42) -> dict:
    spec = SPECS[key]
    data = load_recent_movielens(dataset_dir, maximum_users=420, maximum_items=640)
    baseline_scorer, method_scorer, diagnostics = build_mechanism(key, data, seed)
    baseline = _score_metrics(data, baseline_scorer)
    method = _score_metrics(data, method_scorer)
    relative = {
        f"{name}_percent": 100 * (method[name] - value) / max(abs(value), 1e-12)
        for name, value in baseline.items()
    }
    return {
        "paper": {
            "arxiv_id": spec.arxiv_id,
            "title": spec.title,
            "url": f"https://arxiv.org/abs/{spec.arxiv_id}",
        },
        "dataset": {
            "name": "MovieLens-1M",
            "users": len(data.train),
            "items": data.item_count,
            "full_catalog_evaluation": True,
        },
        "setup": {"seed": seed, "mechanism": spec.mechanism},
        "baseline": {"name": spec.baseline, **baseline},
        "method": {"name": spec.method, **method},
        "relative": relative,
        "diagnostics": diagnostics,
        "paper_results": spec.paper_results,
        "scope": spec.scope,
    }


def render_industrial_p0(result: dict) -> str:
    baseline, method = result["baseline"], result["method"]
    return "\n".join(
        [
            f"# {result['paper']['title']}",
            "",
            f"公开数据：MovieLens-1M（{result['dataset']['users']} users / "
            f"{result['dataset']['items']} items，全目录评估）。",
            "",
            "| Variant | Hit@10 | NDCG@10 | MRR@10 | Head share@10 |",
            "|---|---:|---:|---:|---:|",
            f"| {baseline['name']} | {baseline['hit_at_10']:.4f} | {baseline['ndcg_at_10']:.4f} | "
            f"{baseline['mrr_at_10']:.4f} | {baseline['head_share_at_10']:.4f} |",
            f"| {method['name']} | {method['hit_at_10']:.4f} | {method['ndcg_at_10']:.4f} | "
            f"{method['mrr_at_10']:.4f} | {method['head_share_at_10']:.4f} |",
            "",
            f"相对本文本地基线：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。",
            "",
            "## 复现边界",
            "",
            result["scope"],
            "",
        ]
    )
