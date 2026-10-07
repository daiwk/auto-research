"""Extracted unchanged from auto_research.reproductions.latest_20260907; stable mechanism boundary."""
from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec
from pathlib import Path
import numpy as np
from auto_research.reproductions.base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from auto_research.reproductions.industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result
from auto_research.reproductions.industrial_2026 import render_standard as render
from auto_research.reproductions.sep7_models import EvidenceController, train_two_tower

PAPERS = {
    "allecompanion": {
        "arxiv_id": "2609.05063",
        "title": "Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro",
        "organization": "Allegro.com",
        "published": "2026-09-04",
        "publication_label": "RecSys 2026",
        "topics": ("complementary-recommendation", "two-tower", "category-adapter", "e-commerce"),
        "operator": "context:complementary-category-adapter",
        "paper_results": {"web_organic_gmv_lift_percent": 8.05, "app_organic_gmv_lift_percent": 9.35, "web_cart_gmv_lift_percent": 21.25, "app_cart_gmv_lift_percent": 15.73},
        "evidence": ("Allegro product and cart placements", "attributed GMV", 21.25, "two-week tests routed over 100% platform traffic", "Section 4.4, Table 5"),
        "omitted": ("private 90-day Allegro transaction log", "production Faiss index", "ComCat expert/LLM mapping", "product complementarity benchmark; MovieLens is a structural diagnostic"),
    },
    "autolr": {
        "arxiv_id": "2609.04871",
        "title": "AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems",
        "organization": "NetEase, Inc.",
        "published": "2026-09-04",
        "publication_label": "NetEase technical report",
        "topics": ("auto-research", "experiment-controller", "launch-review", "industrial-recommendation"),
        "operator": "controller:autolr-evidence-council",
        "paper_results": {"completed_offline_evaluations": 1586, "canonical_ledger_records": 3289, "launch_reviews": 9, "content_time_lift_sum_percent": 10.83},
        "evidence": ("NetEase DASHEN feed and immersive-video feed", "content-consumption time", 10.83, "nine Launch Review records with online A/B and production decisions", "Section 5.2, Table 1"),
        "omitted": ("live LLM research and repository code generation", "multi-expert LLM debate", "private DASHEN repository", "online admission and Launch Review authority"),
    },
}

def reproduce(key: str, dataset_dir: Path, seed: int = 42, *, ledger_path=None) -> dict:
    data = load_industrial_data(dataset_dir)
    if key == "allecompanion":
        base_table, base_training = train_two_tower(data, seed, adapter=False)
        method_table, method_training = train_two_tower(data, seed, adapter=True)
        baseline_scorer = lambda history: base_table[history[-1]]
        method_scorer = lambda history: method_table[history[-1]]
        details = {"baseline_training": base_training, "method_training": method_training}
        baseline_name = "shared two-tower without category adapter"
    else:
        baseline_scorer = lambda history: base_scores(data, history)
        controller = EvidenceController(evaluate(data, baseline_scorer, target_split="validation"), ledger_path)
        candidates = [{"key": f"category-tower-{steps}", "steps": steps,
                       "evidence": "arxiv:2609.05063; bounded local candidate, not live research",
                       "reviews": [{"role": "budget", "feasible": steps <= 80, "score": 1.0},
                                   {"role": "data-contract", "feasible": True, "score": 0.5}]}
                      for steps in (20, 40, 80)]
        tables = {}
        def execute(candidate):
            table, _ = train_two_tower(data, seed, steps=candidate["steps"])
            tables[candidate["key"]] = table
            return evaluate(data, lambda history: table[history[-1]], target_split="validation")
        for _ in range(len(candidates)):
            candidate = controller.select(candidates)
            if candidate is None:
                break
            controller.evaluate(candidate, execute, {"hit_at_10": controller.reference["hit_at_10"]})
        if controller.incumbent == "baseline":
            method_scorer = baseline_scorer
        else:
            if controller.incumbent not in tables:
                execute(next(c for c in candidates if c["key"] == controller.incumbent))
            method_scorer = lambda history: tables[controller.incumbent][history[-1]]
        details = {"ledger": controller.records, "incumbent": controller.incumbent,
                   "reference": controller.reference, "online_authorized": False}
        baseline_name = "transition + content + popularity"
    baseline = evaluate(data, baseline_scorer)
    proposed = evaluate(data, method_scorer)
    row = PAPERS[key]
    result = summary_result(
        key=key,
        paper={"arxiv_id": row["arxiv_id"], "title": row["title"], "url": f"https://arxiv.org/abs/{row['arxiv_id']}", "organization": row["organization"]},
        data=data,
        baseline_name=baseline_name,
        method_name=f"{key} executable offline mechanism",
        baseline=baseline,
        proposed=proposed,
        stages={"finite_scores": int(np.isfinite(method_scorer(data.sequences.train[0])).sum()), **details},
        paper_results=row["paper_results"],
        scope="CPU 小型机制验证：MovieLens 邻接关系不等于商品互补性；AutoLR 仅执行预定义候选的离线控制，不包含 LLM 调研/代码生成或线上发布。",
    )
    result["manifest_ref"] = f"reproduction:{key}"
    result["setup"]["seed"] = seed
    return result

def make_adapter(key: str) -> ReproductionAdapter:
    row = PAPERS[key]
    product, metric, lift, traffic, location = row["evidence"]
    return adapter_from_spec(key=key, run=lambda dataset_dir, seed=42: reproduce(key, dataset_dir, seed), render=render)
