"""Public-data core-mechanism reproductions for historical batches B04--B06."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .industrial_2026 import (
    base_scores,
    evaluate,
    hierarchical_codes,
    load_industrial_data,
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
        MechanismSpec("prl-puts", "PRL-PUTS", "pareto_rl", {"repin_percent": .66, "p2p_impression_percent": .30, "successful_session_percent": .13}),
        MechanismSpec("ektm", "Effective Knowledge Transfer for Multi-Task Recommendation Models", "ektm", {"ecpm_percent": 3.93, "final_traffic_percent": 100.0}),
        MechanismSpec("adasid", "AdaSID", "adasid", {"gmv_percent": .98, "orders_percent": .91, "gpm_percent": 1.16}),
        MechanismSpec("unirec-coa", "UniRec", "unirec", {"pvctr_percent": 5.37, "orders_percent": 4.76, "gmv_percent": 5.60}),
        MechanismSpec("uniscale", "UniScale", "uniscale", {"purchase_percent": 1.70, "gmv_percent": 2.04, "gpu_cost_percent": -55.0}),
        MechanismSpec("gatesid", "GateSID", "gatesid", {"gmv_percent": 2.6, "ctr_percent": 1.1, "orders_percent": 1.6}),
        MechanismSpec("aigq", "AIGQ", "aigq", {"attributed_orders_percent": 10.31, "gmv_percent": 10.68, "retention_7d_percent": 3.73}),
        MechanismSpec("safro", "SaFRO", "safro", {"watch_time_percent": .611, "lpr_percent": .495, "qrr_percent": -.319}),
        MechanismSpec("sort-ranking", "SORT", "sort", {"orders_percent": 6.35, "buyers_percent": 5.97, "gmv_percent": 5.47}),
        MechanismSpec("quasid", "QuaSID", "quasid", {"gmv_s2_percent": 2.38, "gmv_s1_percent": 1.44, "co_percent": .20}),
        MechanismSpec("gpl-prerank", "Generative Pseudo-Labeling", "gpl", {"ctr_percent": 3.07, "ipv_percent": 3.53, "ctcvr_percent": 2.51}),
        MechanismSpec("ltv-video-ranking", "Long-term Value Prediction", "ltv", {"vv_percent": 2.49, "retention_percent": .21, "qa_vv_percent": 4.03}),
        MechanismSpec("rgalign-rec", "RGAlign-Rec", "rgalign", {"ctr_at_3_increment_percent": .13, "qe_rec_ctr_at_3_percent": .98, "csat_percent": -.21}),
        MechanismSpec("linkedin-feed-sr", "LinkedIn Feed SR", "feed_sr", {"time_spent_percent": 2.10}),
        MechanismSpec("cadet", "CADET", "cadet", {"ctr_percent": 11.04, "revenue_percent": .14}),
        MechanismSpec("diffureason", "DiffuReason", "diffureason", {"gmv_percent": .7902, "ad_consumption_percent": 1.1462}),
        MechanismSpec("sarm", "SARM", "sarm", {"watch_count_percent": 1.190, "watch_time_percent": .397, "served_users_million": 400.0}),
        MechanismSpec("ml-dcn", "ML-DCN", "ml_dcn", {"ctr_percent": 1.89, "gctr_percent": 2.17, "cpc_percent": -.93}),
        MechanismSpec("rag-qac", "RAG-QAC", "rag_qac", {"suggestions_taken_percent": 3.46, "characters_typed_percent": -5.44}),
    )
}


class HistoricalMechanism:
    """A fitted mechanism; every mode owns distinct state and scoring logic."""

    def __init__(self, mode: str, seed: int = 42):
        self.mode = mode
        self.seed = seed
        self.state: dict[str, object] = {}

    def fit(self, data) -> "HistoricalMechanism":
        rng = np.random.default_rng(self.seed)
        features = data.sequences.features.astype(np.float64)
        semantic = features / np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-9)
        self.state["semantic"] = semantic
        if self.mode in {"adasid", "unirec", "gatesid", "quasid", "aigq", "rgalign"}:
            self.state["codes"] = hierarchical_codes(features, 3, 8, self.seed)
        if self.mode in {"adasid", "unirec", "quasid"}:
            codes = np.asarray(self.state["codes"])
            occupancy = np.stack([np.bincount(codes[:, level], minlength=8) for level in range(3)])
            self.state["occupancy"] = occupancy / max(len(codes), 1)
        if self.mode == "pareto_rl":
            self.state["alphas"] = np.linspace(.1, .9, 9)
            self.state["q_scale"] = np.array([1.0, .8])
        elif self.mode == "ektm":
            self.state["task_affinity"] = softmax(np.corrcoef(np.stack([data.popularity, data.transition.mean(0), semantic.mean(1)])))
        elif self.mode == "uniscale":
            self.state["scale_gates"] = softmax(np.array([.8, .6, .4, .2]))
        elif self.mode == "gatesid":
            self.state["cold_gate"] = 1.0 / (1.0 + np.exp(8.0 * (data.popularity - .35)))
        elif self.mode == "safro":
            self.state["reward_center"] = np.array([data.popularity.mean(), data.transition.mean(), data.cosine.mean()])
        elif self.mode == "sort":
            self.state["token_projection"] = rng.normal(0, 1 / np.sqrt(features.shape[1]), (features.shape[1], features.shape[1]))
        elif self.mode == "gpl":
            anchors = semantic @ semantic.T
            self.state["pseudo_labels"] = .6 * anchors.mean(0) + .4 * (1.0 - data.popularity)
        elif self.mode == "ltv":
            self.state["quantile"] = np.searchsorted(np.sort(data.popularity), data.popularity) / len(data.popularity)
        elif self.mode == "feed_sr":
            self.state["time_decay"] = np.geomspace(.15, 1.0, 16)
        elif self.mode == "cadet":
            self.state["context_delay"] = 2
        elif self.mode == "diffureason":
            self.state["noise_schedule"] = np.linspace(.35, .05, 4)
        elif self.mode == "sarm":
            domain_count = int(data.domains.max()) + 1
            anchors = np.stack([
                semantic[data.domains == d].mean(0)
                if np.any(data.domains == d) else np.zeros(semantic.shape[1])
                for d in range(domain_count)
            ])
            self.state["anchors"] = anchors
        elif self.mode == "ml_dcn":
            rank = min(8, features.shape[1])
            self.state["low_rank"] = (rng.normal(0, .2, (features.shape[1], rank)), rng.normal(0, .2, (rank, features.shape[1])))
            self.state["mask"] = (rng.random(features.shape[1]) > .5).astype(float)
        elif self.mode == "rag_qac":
            self.state["objective_weights"] = np.array([.42, .23, .15, .12, .08])
        self.state["fitted"] = True
        return self

    def score(self, data, history) -> np.ndarray:
        if not self.state.get("fitted"):
            raise RuntimeError("fit must be called before score")
        recent = list(history[-8:])
        semantic = np.asarray(self.state["semantic"])
        base = base_scores(data, history)
        transition = data.transition[history[-1]]
        content = data.cosine[recent].mean(0)
        fresh = 1.0 - data.popularity
        domain_match = (data.domains == data.domains[history[-1]]).astype(float)
        query = semantic[recent].mean(0)
        semantic_score = semantic @ query
        if self.mode == "pareto_rl":
            cohort = min(8, len(set(history)) // 2)
            alpha = np.asarray(self.state["alphas"])[cohort]
            return alpha * transition + (1.0 - alpha) * (.65 * content + .35 * fresh)
        if self.mode == "ektm":
            affinity = np.asarray(self.state["task_affinity"])
            tasks = np.stack([transition, content, data.popularity])
            transferred = affinity @ tasks
            return transferred[0] + .5 * transferred[1] - .15 * transferred[2]
        if self.mode == "adasid":
            codes = np.asarray(self.state["codes"]); occ = np.asarray(self.state["occupancy"])
            overlap = (codes[:, None, :] == codes[recent][None, :, :]).mean(1)
            load = occ[np.arange(3), codes].mean(1)
            compatibility = np.maximum(semantic_score, 0)
            return (overlap * (1.0 + compatibility[:, None])).mean(1) - .4 * load
        if self.mode == "unirec":
            codes = np.asarray(self.state["codes"]); occ = np.asarray(self.state["occupancy"])
            coa = .45 * domain_match + .35 * semantic_score + .20 * (codes[:, 0] == codes[history[-1], 0])
            return coa - .25 * occ[np.arange(3), codes].mean(1) + .15 * transition
        if self.mode == "uniscale":
            gates = np.asarray(self.state["scale_gates"])
            return gates @ np.stack([transition, content, domain_match, fresh])
        if self.mode == "gatesid":
            gate = np.asarray(self.state["cold_gate"])
            codes = np.asarray(self.state["codes"])
            sid = (codes[:, 0] == codes[history[-1], 0]).astype(float)
            return gate * (.7 * semantic_score + .3 * sid) + (1.0 - gate) * transition
        if self.mode == "aigq":
            codes = np.asarray(self.state["codes"])
            direct = .6 * transition + .4 * content
            reasoned = .5 * semantic_score + .3 * domain_match + .2 * (codes[:, 0] == codes[history[-1], 0])
            return .55 * direct + .45 * reasoned + .12 * fresh
        if self.mode == "safro":
            rewards = np.stack([transition, content, fresh])
            relative = (rewards - rewards.mean(1, keepdims=True)) / np.maximum(rewards.std(1, keepdims=True), 1e-6)
            return .45 * relative[0] + .35 * relative[1] + .20 * relative[2]
        if self.mode == "sort":
            projection = np.asarray(self.state["token_projection"])
            weights = softmax(np.linspace(-1.2, .4, len(recent)))
            token_query = weights @ (semantic[recent] @ projection)
            return semantic @ token_query + .25 * transition + .12 * domain_match
        if self.mode == "quasid":
            codes = np.asarray(self.state["codes"]); occ = np.asarray(self.state["occupancy"])
            collision = (codes[:, None, :] == codes[recent][None, :, :]).mean((1, 2))
            qualification = .55 * semantic_score + .45 * transition
            margin = 1.0 / (1.0 + 4.0 * occ[np.arange(3), codes].mean(1))
            return qualification + collision * margin
        if self.mode == "gpl":
            return .55 * transition + .30 * np.asarray(self.state["pseudo_labels"]) + .15 * semantic_score
        if self.mode == "ltv":
            position_debiased = transition / np.maximum(.3 + data.popularity, 1e-6)
            author_value = .6 * domain_match + .4 * np.asarray(self.state["quantile"])
            return .55 * position_debiased + .45 * author_value
        if self.mode == "rgalign":
            codes = np.asarray(self.state["codes"])
            latent_query = .6 * semantic_score + .4 * domain_match
            guide = .7 * transition + .3 * (codes[:, 0] == codes[history[-1], 0])
            return latent_query + .35 * (guide - latent_query)
        if self.mode == "feed_sr":
            length = min(len(history), len(np.asarray(self.state["time_decay"])))
            weights = np.asarray(self.state["time_decay"])[-length:]
            long_sequence = (data.cosine[list(history[-length:])] * weights[:, None]).sum(0) / weights.sum()
            return .58 * long_sequence + .30 * transition + .12 * domain_match
        if self.mode == "cadet":
            delayed = list(history[:-int(self.state["context_delay"])])[-6:] or recent
            early = data.cosine[delayed].mean(0)
            post_context = .6 * domain_match + .4 * transition
            return early + .35 * post_context * (1.0 + early)
        if self.mode == "diffureason":
            latent = .55 * semantic_score + .30 * transition + .15 * domain_match
            for noise in np.asarray(self.state["noise_schedule"]):
                latent = (1.0 - noise) * latent + noise * (data.cosine @ softmax(latent))
            return latent
        if self.mode == "sarm":
            anchor = np.asarray(self.state["anchors"])[data.domains]
            anchor_score = np.sum(anchor * query, axis=1)
            return .55 * anchor_score + .30 * transition + .15 * domain_match
        if self.mode == "ml_dcn":
            left, right = self.state["low_rank"]
            context = semantic[recent].mean(0) * np.asarray(self.state["mask"])
            crossed = (context @ np.asarray(left)) @ np.asarray(right)
            return semantic @ (context + crossed + context * crossed) + .2 * transition
        if self.mode == "rag_qac":
            retrieved = .55 * transition + .45 * content
            grounded = semantic_score
            safe = 1.0 - data.popularity * (1.0 - domain_match)
            diversity = fresh
            context = domain_match
            return np.asarray(self.state["objective_weights"]) @ np.stack([retrieved, grounded, safe, diversity, context])
        raise ValueError(f"unknown historical mechanism: {self.mode}")

    def diagnostics(self) -> dict[str, object]:
        return {"mode": self.mode, "fitted": bool(self.state.get("fitted")), "state_keys": sorted(self.state)}


def reproduce(key: str, dataset_dir: Path, seed: int = 42, model_class=HistoricalMechanism) -> dict:
    spec = SPECS[key]
    data = load_industrial_data(dataset_dir, maximum_users=220, maximum_items=360)
    model = model_class(seed).fit(data) if model_class is not HistoricalMechanism else HistoricalMechanism(spec.mode, seed).fit(data)
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
        stages={"mechanism": model.diagnostics(), "validation_selected_alpha": alpha, "validation": validation},
        paper_results=spec.paper_results,
        scope=("在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；"
               "私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。"),
    )
