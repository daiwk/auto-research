from __future__ import annotations

import copy
import os
from pathlib import Path

from .model import (
    OneRecV2Config, build_encoder_decoder, build_lazy_decoder, evaluate,
    load_kuairand_examples, require_backend, train_gbpo, train_sft,
)


def reproduce_onerec_v2(dataset_dir: Path, seed: int = 42):
    torch, _ = require_backend()
    config = OneRecV2Config(
        sft_steps=int(os.environ.get("AUTO_RESEARCH_ONEREC_V2_SFT_STEPS", "160")),
        gbpo_steps=int(os.environ.get("AUTO_RESEARCH_ONEREC_V2_GBPO_STEPS", "80")),
        maximum_events=int(os.environ.get("AUTO_RESEARCH_ONEREC_V2_EVENTS", "180000")),
        maximum_examples=int(os.environ.get("AUTO_RESEARCH_ONEREC_V2_EXAMPLES", "36000")),
    )
    data = load_kuairand_examples(dataset_dir, config)
    torch.manual_seed(seed)
    baseline = build_encoder_decoder(data, config)
    baseline_training = train_sft(baseline, data.train, config, seed)
    baseline_metrics = evaluate(baseline, data.validation, config)
    torch.manual_seed(seed)
    lazy = build_lazy_decoder(data, config)
    lazy_training = train_sft(lazy, data.train, config, seed)
    sft_metrics = evaluate(lazy, data.validation, config)
    aligned = copy.deepcopy(lazy)
    gbpo_training = train_gbpo(aligned, data.train, config, seed + 1)
    gbpo_metrics = evaluate(aligned, data.validation, config)
    return {
        "paper": {"arxiv_id": "2508.20900", "title": "OneRec-V2 Technical Report", "url": "https://arxiv.org/abs/2508.20900", "track": "recommendation"},
        "dataset": "KuaiRand-Pure official public Kuaishou logs",
        "setup": {"seed": seed, "events": data.events, "train_examples": len(data.train), "validation_examples": len(data.validation), "items": data.items, "semantic_cardinalities": list(data.cardinalities), "sid_uniqueness": data.sid_uniqueness, "sft_steps": config.sft_steps, "gbpo_steps": config.gbpo_steps},
        "training": {"encoder_decoder": baseline_training, "lazy_decoder": lazy_training, "gbpo": gbpo_training},
        "results": {"encoder_decoder": baseline_metrics, "lazy_decoder_sft": sft_metrics, "lazy_decoder_gbpo": gbpo_metrics},
        "paper_online_ab": {"traffic": "5% for one week", "kuaishou_app_stay_time_percent": 0.467, "kuaishou_lite_app_stay_time_percent": 0.741, "kuaishou_like_percent": 3.924, "kuaishou_lite_forward_percent": 7.958},
        "scope": "Executes newest-impression-only SFT, a lazy decoder with layer-shared context K/V, three-level constrained semantic IDs, duration-aware reward shaping on real KuaiRand play/duration feedback, and GBPO. Production scale, heterogeneous proprietary features, and distributed serving are reduced locally.",
    }
