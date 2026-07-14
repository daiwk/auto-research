from __future__ import annotations

import os
from pathlib import Path

from .data import load_joint_reviews
from .model import LSVCRConfig, prepare_llm_views, train_variant


def reproduce_lsvcr(dataset_dir: Path, seed: int = 42):
    config = LSVCRConfig(
        maximum_users=int(os.environ.get("AUTO_RESEARCH_LSVCR_USERS", "80")),
        lora_steps=int(os.environ.get("AUTO_RESEARCH_LSVCR_LORA_STEPS", "24")),
        alignment_steps=int(os.environ.get("AUTO_RESEARCH_LSVCR_ALIGN_STEPS", "80")),
        finetune_steps=int(os.environ.get("AUTO_RESEARCH_LSVCR_STEPS", "120")),
    )
    data = load_joint_reviews(dataset_dir, config.maximum_users)
    views, llm = prepare_llm_views(data, dataset_dir, config, seed)
    baseline = train_variant(data, views, config, seed, False)
    method = train_variant(data, views, config, seed, True)
    return {
        "paper": {"arxiv_id": "2403.13574", "title": "A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation", "url": "https://arxiv.org/abs/2403.13574", "track": "recommendation"},
        "dataset": "Amazon Beauty 5-core product interactions and real review text",
        "setup": {"seed": seed, "users": config.maximum_users, "items": len(data.item_texts), "comments": len(data.comment_texts), "train": len(data.train), "test": len(data.test), "lora_steps": config.lora_steps, "alignment_steps": config.alignment_steps, "finetune_steps": config.finetune_steps, **llm},
        "results": {"without_alignment": baseline, "lsvcr": method},
        "paper_online_ab": {"video_watch_time_percent": 0.3649, "video_interactions_percent": 0.7821, "comment_watch_time_percent": 4.1264, "comment_interactions_percent": 1.3557, "traffic": "Kuaishou, 20K users, 2 weeks"},
        "scope": "Executes q/v-projection LoRA SFT on a causal LM recommender, LLM text encoding, randomized positions, dual sequence Transformers, bidirectional cross-fusion, SSC/VCC preference alignment and joint item/comment fine-tuning. Amazon products/reviews replace proprietary Kuaishou videos/comments.",
    }
