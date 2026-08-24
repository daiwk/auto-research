"""Public-data core-mechanism reproductions for historical batches B01--B03.

The papers share only the MovieLens split, baseline and validation-only blend
selection.  ``HistoricalMechanism`` builds a different state and scoring path
for every paper; production A/B values are metadata and are never mixed into
the local metric.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .industrial_2026 import (
    base_scores,
    evaluate,
    hierarchical_codes,
    load_industrial_data,
    ridge,
    softmax,
    summary_result,
    tune_blend,
)


@dataclass(frozen=True)
class MechanismSpec:
    key: str
    title: str
    mode: str
    paper_results: dict[str, float | str]


SPECS = {
    row.key: row for row in (
        MechanismSpec("dynamic-codebook", "Dynamic Single-Level Large Semantic Codebook", "dynamic_codebook", {"consumption_percent": 0.792, "traffic_percent": 2.5}),
        MechanismSpec("netflix-mediafm", "Multimedia Asset Personalization", "mediafm", {"search_playthrough_percent": 0.36, "unified_clip_discovery_percent": 0.127, "mediafm_streaming_percent": 0.193}),
        MechanismSpec("ogr", "Once Generated, Ranked", "ogr", {"effective_views_percent": 1.120, "comments_percent": 2.954, "likes_percent": .505, "forwards_percent": 1.255}),
        MechanismSpec("inthq", "IntHQ", "inthq", {"uvctr_percent": 1.60, "latency_ms": 40.0}),
        MechanismSpec("pushdualgen", "PushDualGen", "pushdualgen", {"effective_play_percent": 8.50, "dissatisfaction_percent": -37.70}),
        MechanismSpec("recharness", "RecHarness", "recharness", {"advv_percent": 2.084, "revenue_percent": 0.534, "exposure_percent": .559}),
        MechanismSpec("gala", "GALA", "gala", {"order_volume_percent": .55}),
        MechanismSpec("feedback-policy", "From Understanding to Action", "feedback_policy", {"revenue_percent": 4.506, "advv_percent": 4.621}),
        MechanismSpec("real-estate-rerank", "LLM-Based Re-Ranking for Real Estate Search", "real_estate", {"ctr_percent": 5.3, "scheduled_visits_percent": 4.8}),
        MechanismSpec("adaptive-ad-load", "Adaptive Ad Load Design", "ad_load", {"revenue_percent": 36.8, "conversion_percent": -1.1}),
        MechanismSpec("guess-where-you-go", "Guess Where You Go", "next_poi", {"p_ctr_percent": 5.83, "u_ctr_percent": 6.20, "negative_feedback_percent": -11.11}),
        MechanismSpec("genpage", "GenPage", "genpage", {"engagement_percent": 0.24, "latency_percent": -20.0}),
        MechanismSpec("journeyformer", "JourneyFormer", "journeyformer", {"bookers_percent": 0.55, "booked_nights_percent": 0.82}),
        MechanismSpec("l2rec", "L2Rec", "l2rec", {"ctr_percent": 9.24, "reply_rate_percent": 3.15}),
        MechanismSpec("qgs", "Query-Conditioned Generative Search", "qgs", {"ctr_percent": 0.62, "click_search_ratio_percent": .38, "pv_duration_percent": 3.55}),
        MechanismSpec("tubifm", "TubiFM", "tubifm", {"search_tvt_percent": 3.9, "carousel_tvt_percent": 0.30, "item_tvt_percent": .14, "p99_latency_ms": 200.0}),
        MechanismSpec("pearl-percentile", "PEARL", "pearl", {"watch_duration_percent": 2.10, "consumption_percent": .80, "interaction_percent": 1.49, "report_rate_percent": -6.91}),
        MechanismSpec("dadf", "DADF", "dadf", {"time_spent_percent": 0.649, "production_mae_percent": -12.57}),
    )
}


class HistoricalMechanism:
    """Fitted, inspectable paper operator used by both adapters and evolve."""

    def __init__(self, mode: str, seed: int = 42):
        self.mode = mode
        self.seed = seed
        self.state: dict[str, object] = {}

    def fit(self, data) -> "HistoricalMechanism":
        rng = np.random.default_rng(self.seed)
        features = data.sequences.features.astype(np.float64)
        n = data.item_count
        domain_count = int(data.domains.max()) + 1
        if self.mode in {"dynamic_codebook", "ogr", "pushdualgen", "gala", "next_poi", "qgs"}:
            levels = 1 if self.mode == "dynamic_codebook" else 3
            width = min(16, max(4, int(np.sqrt(n))))
            codes = hierarchical_codes(features, levels, width, self.seed)
            self.state["codes"] = codes
            self.state["code_width"] = width
            exposure = np.zeros((levels, width))
            for sequence in data.sequences.train:
                for position, item in enumerate(sequence):
                    exposure[np.arange(levels), codes[item]] += 1.0 / (1.0 + 0.03 * position)
            self.state["code_prior"] = exposure / np.maximum(exposure.sum(1, keepdims=True), 1e-12)
        if self.mode in {"mediafm", "gala", "real_estate", "l2rec", "qgs", "tubifm"}:
            # Frozen public metadata embedding stands in for the paper's frozen
            # multimodal/text tower; a learned projection aligns it to behavior.
            semantic = np.concatenate([features, features @ rng.normal(0, .2, (features.shape[1], 8))], axis=1)
            collab = np.concatenate([data.transition, data.transition.T], axis=1)
            self.state["semantic"] = semantic / np.maximum(np.linalg.norm(semantic, axis=1, keepdims=True), 1e-9)
            self.state["align"] = ridge(self.state["semantic"], collab[:, :n])
        if self.mode == "recharness":
            self.state["arms"] = ("transition", "content", "fresh")
            self.state["counts"] = np.ones(3)
            rewards = np.zeros(3)
            for sequence in data.sequences.train:
                if len(sequence) > 1:
                    left, right = sequence[-2], sequence[-1]
                    rewards += (data.transition[left, right], data.cosine[left, right], 1.0 - data.popularity[right])
                    self.state["counts"] += 1
            self.state["arm_reward"] = rewards / self.state["counts"]
        if self.mode == "pearl":
            comparisons = np.zeros(n)
            counts = np.ones(n)
            for sequence in data.sequences.train:
                for item in sequence:
                    rivals = rng.choice(n, 50, replace=True)
                    comparisons[item] += np.mean(data.popularity[item] >= data.popularity[rivals])
                    counts[item] += 1
            self.state["percentile"] = comparisons / counts
        if self.mode == "dadf":
            # Frozen first-stage score followed by regime-specific multiplicative
            # residual estimates; no first-stage parameters are changed.
            regimes = np.stack([data.popularity, 1.0 - data.popularity, np.ones(n)], axis=1)
            target = np.maximum(data.transition.mean(0), 1e-4)
            frozen = np.maximum(0.55 * data.popularity + 0.45 * data.cosine.mean(0), 1e-4)
            self.state["correction"] = np.clip(regimes @ ridge(regimes, target / frozen), .25, 4.0)
        self.state["domain_eye"] = np.eye(domain_count)[data.domains]
        self.state["fitted"] = True
        return self

    def score(self, data, history) -> np.ndarray:
        if not self.state.get("fitted"):
            raise RuntimeError("fit must be called before score")
        recent = list(history[-8:])
        base = base_scores(data, history)
        content = data.cosine[recent].mean(0)
        transition = data.transition[history[-1]]
        fresh = 1.0 - data.popularity
        domain = np.asarray(self.state["domain_eye"])
        intent = domain[recent].mean(0)
        domain_score = domain @ intent
        if self.mode == "dynamic_codebook":
            codes = np.asarray(self.state["codes"]); prior = np.asarray(self.state["code_prior"])[0]
            match = (codes[:, 0, None] == codes[recent, 0]).mean(1)
            # Popularity-weighted moving-codebook occupancy plus stable collision token.
            collision = (np.arange(data.item_count) % 11 == history[-1] % 11).astype(float)
            return match + .35 * np.log(prior[codes[:, 0]] + 1e-8) + .08 * collision
        if self.mode == "mediafm":
            sem = np.asarray(self.state["semantic"])
            query = sem[recent].mean(0)
            return sem @ query + .25 * domain_score
        if self.mode == "ogr":
            codes = np.asarray(self.state["codes"])
            sid = (codes[:, None, :] == codes[recent][None, :, :]).mean((1, 2))
            list_advantage = .6 * content + .4 * transition - .12 * data.popularity
            return sid + .45 * list_advantage
        if self.mode == "inthq":
            short = data.cosine[list(history[-3:])].mean(0)
            long = data.cosine[recent].mean(0)
            task_queries = np.stack([short, long, transition, domain_score])
            gates = softmax(np.array([short.max(), long.max(), transition.max(), intent.max()]))
            return gates @ task_queries
        if self.mode == "pushdualgen":
            codes = np.asarray(self.state["codes"])
            sid = (codes[:, 0, None] == codes[recent, 0]).mean(1)
            copy_agreement = domain_score * (content > np.median(content))
            return sid + .30 * copy_agreement + .12 * fresh
        if self.mode == "recharness":
            values = np.stack([transition, content, fresh])
            reward = np.asarray(self.state["arm_reward"])
            confidence = np.sqrt(2.0 * np.log(1.0 + reward.sum()) / np.asarray(self.state["counts"]))
            return values[int(np.argmax(reward + confidence))]
        if self.mode == "gala":
            sem = np.asarray(self.state["semantic"])
            aligned = sem @ sem[recent].mean(0)
            reward_gate = softmax(np.stack([aligned, base]), axis=0)
            return reward_gate[0] * aligned + reward_gate[1] * base
        if self.mode == "feedback_policy":
            positive = .5 * transition + .3 * content + .2 * fresh
            conservative = np.minimum(positive - base, .25)
            return base + .65 * conservative
        if self.mode == "real_estate":
            sem = np.asarray(self.state["semantic"])
            query = .65 * sem[recent].mean(0) + .35 * sem[history[-1]]
            return sem @ query + .2 * fresh
        if self.mode == "ad_load":
            relevance = softmax(base)
            revenue = softmax(.6 * data.popularity + .4 * transition)
            load_penalty = np.maximum(np.cumsum(np.sort(revenue)[::-1]).mean() - .5, 0)
            return relevance + .35 * revenue - load_penalty * data.popularity
        if self.mode == "next_poi":
            codes = np.asarray(self.state["codes"])
            path = (codes[:, 0] == codes[history[-1], 0]).astype(float)
            return .55 * transition + .25 * path + .20 * domain_score
        if self.mode == "genpage":
            # Greedy page utility is distilled into a per-item score: relevance,
            # coverage and redundancy are optimized jointly.
            return base + .28 * fresh + .22 * (1.0 - content * data.popularity)
        if self.mode == "journeyformer":
            positions = np.geomspace(.25, 1.0, len(recent))
            journey = (data.cosine[recent] * positions[:, None]).sum(0) / positions.sum()
            return .55 * journey + .30 * transition + .15 * domain_score
        if self.mode == "l2rec":
            sem = np.asarray(self.state["semantic"])
            parameter_view = sem @ sem[recent].mean(0)
            representation_view = .55 * content + .45 * transition
            gate = 1.0 / (1.0 + np.exp(-(len(history) - 6) / 3.0))
            return gate * parameter_view + (1.0 - gate) * representation_view
        if self.mode == "qgs":
            codes = np.asarray(self.state["codes"])
            query = domain_score + .5 * transition
            sequence = (codes[:, 0] == codes[history[-1], 0]).astype(float)
            return .55 * query + .45 * sequence
        if self.mode == "tubifm":
            item = .5 * transition + .5 * content
            carousel = domain_score
            search = np.asarray(self.state["semantic"]) @ np.asarray(self.state["semantic"])[history[-1]]
            task_gate = softmax(np.array([len(history), len(set(data.domains[recent])), 1.0]))
            return task_gate @ np.stack([item, carousel, search])
        if self.mode == "pearl":
            percentile = np.asarray(self.state["percentile"])
            return base + .35 * (percentile - np.mean(percentile))
        if self.mode == "dadf":
            return base * np.asarray(self.state["correction"])
        raise ValueError(f"unknown historical mechanism: {self.mode}")

    def diagnostics(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "fitted": bool(self.state.get("fitted")),
            "state_keys": sorted(self.state),
        }


def reproduce(key: str, dataset_dir: Path, seed: int = 42, model_class=HistoricalMechanism) -> dict:
    spec = SPECS[key]
    data = load_industrial_data(dataset_dir, maximum_users=220, maximum_items=360)
    model = (
        model_class(seed).fit(data)
        if model_class is not HistoricalMechanism
        else HistoricalMechanism(spec.mode, seed).fit(data)
    )
    baseline = lambda history: base_scores(data, history)
    method = lambda history: model.score(data, history)
    alpha, blended, validation = tune_blend(data, baseline, method)
    return summary_result(
        key=key,
        paper={"title": spec.title},
        data=data,
        baseline_name="shared transition + content baseline",
        method_name=spec.title,
        baseline=evaluate(data, baseline),
        proposed=evaluate(data, blended),
        stages={
            "mechanism": model.diagnostics(),
            "validation_selected_alpha": alpha,
            "validation": validation,
        },
        paper_results=spec.paper_results,
        scope=(
            "在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；"
            "公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。"
        ),
    )
