from __future__ import annotations

import os
from pathlib import Path

from .data import creative, load_retrieval_data
from .model import (
    collaborative_matrix,
    evaluate,
    generate_representations,
    graph_stability,
    lexical_representation,
    similarity_matrix,
)


def reproduce_llm_ad_retrieval(dataset_dir: Path, seed: int = 42) -> dict:
    maximum_users = int(os.environ.get("AUTO_RESEARCH_LLM_AD_USERS", "180"))
    maximum_items = int(os.environ.get("AUTO_RESEARCH_LLM_AD_ITEMS", "240"))
    k = int(os.environ.get("AUTO_RESEARCH_LLM_AD_K", "20"))
    model_name = os.environ.get(
        "AUTO_RESEARCH_LLM_AD_MODEL", "HuggingFaceTB/SmolLM2-135M-Instruct"
    )
    tuning_steps = int(os.environ.get("AUTO_RESEARCH_LLM_AD_TUNING_STEPS", "80"))
    data = load_retrieval_data(dataset_dir, maximum_users, maximum_items)
    primary, shadow, generation = generate_representations(
        data, dataset_dir, model_name, tuning_steps=tuning_steps, seed=seed
    )
    semantic = similarity_matrix(primary)
    collaborative = collaborative_matrix(data)
    candidates = (0.0, 0.25, 0.5, 1.0, 2.0)
    validation = {
        str(alpha): evaluate(
            data, collaborative, semantic, alpha, "validation", k, seed
        )
        for alpha in candidates
    }
    best_alpha = max(
        candidates,
        key=lambda alpha: (
            validation[str(alpha)]["recall_at_k"],
            validation[str(alpha)]["ndcg_at_k"],
            -alpha,
        ),
    )
    baseline = evaluate(data, collaborative, semantic, 0.0, "test", k, seed)
    treatment = evaluate(
        data, collaborative, semantic, best_alpha, "test", k, seed
    )
    lexical_primary = [
        lexical_representation(creative(title, genres))
        for title, genres in zip(data.titles, data.genres)
    ]
    lexical_shadow = [
        lexical_representation(creative(title, genres, shadow=True))
        for title, genres in zip(data.titles, data.genres)
    ]
    return {
        "paper": {
            "arxiv_id": "2605.21969",
            "title": "LLM Retrieval for Stable and Predictable Ad Recommendations",
            "url": "https://arxiv.org/abs/2605.21969",
            "track": "recommendation",
        },
        "dataset": "MovieLens-100K titles, genres, and chronological positive feedback",
        "setup": {
            "seed": seed,
            "users": len(data.train),
            "items": data.items,
            "k": k,
            "model": model_name,
            "selected_alpha": best_alpha,
            **generation,
        },
        "validation": validation,
        "results": {
            "collaborative_graph": baseline,
            "collaborative_plus_llm_graph": treatment,
        },
        "stability": {
            "lexical_graph": graph_stability(lexical_primary, lexical_shadow, k),
            "llm_semantic_graph": graph_stability(primary, shadow, k),
        },
        "paper_online_ab": {
            "topline_lift_percent": 0.45,
            "final_stage_recall_lift_percent": 1.2,
            "aa_difference_reduction_percent": 8.62,
            "mad_improvement_percent": 45.0,
        },
        "scope": (
            "Runs real domain instruction tuning and an LLM hidden-state attribute head for "
            "paired primary and perturbed creatives, hierarchical phrase/token fuzzy matching, semantic graph "
            "expansion, validation-only route weighting, held-out retrieval, and stability "
            "evaluation. A domain-tuned SmolLM2-135M and MovieLens text/feedback replace "
            "Llama-3-8B, tens of "
            "millions of private ads, Meta's serving stack, conversions, and live A/A' traffic."
        ),
    }
