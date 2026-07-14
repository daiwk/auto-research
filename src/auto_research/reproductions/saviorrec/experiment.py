from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from ..action_data import load_action_ctr, load_action_sequences
from .model import SaviorConfig, build_ranker, train_behavior_encoder, train_ranker


def reproduce_saviorrec(dataset_dir: Path, seed: int = 42):
    config = SaviorConfig(
        encoder_steps=int(os.environ.get("AUTO_RESEARCH_SAVIOR_ENCODER_STEPS", "160")),
        ranker_steps=int(os.environ.get("AUTO_RESEARCH_SAVIOR_STEPS", "180")),
    )
    sequence_data = load_action_sequences(dataset_dir)
    train, test, item_count = load_action_ctr(dataset_dir)
    pairs = []
    for sequence in sequence_data.train_items:
        pairs.extend(zip(sequence[:-1], sequence[1:]))
    aligned, codes, encoder = train_behavior_encoder(sequence_data.item_features, pairs, config, seed)
    frequency = np.bincount([row.candidate for row in train], minlength=item_count)
    baseline = train_ranker(build_ranker(item_count, aligned, codes, config, False), train, test, frequency, config, seed)
    method = train_ranker(build_ranker(item_count, aligned, codes, config, True), train, test, frequency, config, seed)
    return {
        "paper": {"arxiv_id": "2508.01375", "title": "SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation", "url": "https://arxiv.org/abs/2508.01375", "track": "recommendation"},
        "dataset": "MovieLens-100K genre modality and chronological co-interactions",
        "setup": {"seed": seed, "items": item_count, "train": min(len(train), config.maximum_train), "test": min(len(test), config.maximum_test), "encoder_steps": config.encoder_steps, "ranker_steps": config.ranker_steps},
        "behavior_encoder": encoder,
        "results": {"content_ranker": baseline, "saviorrec": method},
        "paper_online_ab": {"clicks_percent": 13.31, "orders_percent": 13.44, "ctr_percent": 12.80, "product": "Taobao Guess You Like cold-start traffic"},
        "scope": "Executes behavior-supervised content encoding, residual semantic IDs, zero-initialized modal-behavior alignment codebooks, bidirectional target/history attention and cold-item CTR evaluation. MovieLens genres replace proprietary image/text encoders.",
    }
