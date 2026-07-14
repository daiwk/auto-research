import os
from pathlib import Path

from ..llm_rec_data import load_text_ctr_data
from ..rec_utils import load_movielens_sequences
from .model import LEARNConfig, build_model, content_embeddings, evaluate_learn, evaluate_semantic_mean, train_model


def reproduce_learn(dataset_dir: Path, seed: int = 42):
    config = LEARNConfig(steps=int(os.environ.get("AUTO_RESEARCH_LEARN_STEPS", "140")))
    data = load_movielens_sequences(dataset_dir)
    titles = load_text_ctr_data(dataset_dir).titles
    content = content_embeddings(titles, dataset_dir, config)
    baseline = evaluate_semantic_mean(content, data, config)
    model, training = train_model(build_model(content, config), data, config, seed)
    return {
        "paper": {"arxiv_id": "2405.03988", "title": "Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application", "url": "https://arxiv.org/abs/2405.03988", "track": "recommendation"},
        "dataset": "MovieLens 100K title/genre text",
        "setup": {"seed": seed, "steps": config.steps, "llm": config.model_name, "users": len(data.train)},
        "results": {"frozen_llm_semantic_mean": baseline, "learn_ceg_pch": evaluate_learn(model, data, config)},
        "training": training,
        "paper_online_ab": {"traffic_percent": 20, "days": 9, "cold_item_revenue_percent": 8.77, "long_tail_item_revenue_percent": 4.63, "cold_user_revenue_percent": 1.56},
        "scope": "Executes frozen pretrained-LM content embedding generation, cached item embeddings, causal Preference Comprehension Transformer, dense all-position objective, and online projection.",
    }
