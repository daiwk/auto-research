from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import numpy as np

from ..rec_utils import load_movielens_1m_sequences
from .data import build_cpt_corpus, build_sft_examples
from .llm import TrainingConfig, run_ablation
from .model import SemanticIDIndex, build_semantic_ids, load_movie_metadata


def reproduce_plum(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    output_dir = Path(os.environ.get("AUTO_RESEARCH_PLUM_CHECKPOINTS", "runs/plum-checkpoints"))
    config = _training_config()
    prior_payload = _prior_payload()
    data = load_movielens_1m_sequences(dataset_dir)
    metadata = load_movie_metadata(dataset_dir)
    resume_sid = (
        None
        if config.resume_dir is None
        else config.resume_dir / "sid" / "semantic_ids.npy"
    )
    if resume_sid is not None and resume_sid.exists():
        if prior_payload is None:
            raise RuntimeError("resuming SID codes requires the previous result.json")
        index = SemanticIDIndex(
            codes=np.load(resume_sid),
            cardinalities=tuple(prior_payload["setup"]["sid_cardinalities"]),
            training_metrics=prior_payload["setup"]["sid_training"],
        )
    else:
        index = build_semantic_ids(
            data, metadata, seed=seed, checkpoint_dir=output_dir / "sid"
        )
    cpt = build_cpt_corpus(data, metadata, index, seed)
    sft = build_sft_examples(data, index, seed)
    variants = (
        ("R1", False, False),
        ("R2", True, False),
        ("CR1", False, True),
        ("CR2", True, True),
    )
    results = {
        name: run_ablation(
            name,
            llm_initialized,
            use_cpt,
            cpt,
            sft,
            data,
            index,
            seed,
            output_dir,
            config,
            None if prior_payload is None else prior_payload["results"][name],
        )
        for name, llm_initialized, use_cpt in variants
    }
    return {
        "paper": {
            "arxiv_id": "2510.07784",
            "title": "PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations",
            "url": "https://arxiv.org/abs/2510.07784",
            "track": "recommendation",
        },
        "dataset": "MovieLens 1M",
        "setup": {
            "users": len(data.train),
            "items": data.item_count,
            "base_model": "HuggingFaceTB/SmolLM2-135M",
            "full_parameter_training": True,
            "sid_cardinalities": list(index.cardinalities),
            "sid_uniqueness": index.uniqueness,
            "sid_training": index.training_metrics,
            "cpt_examples": len(cpt),
            "cpt_behavior_share": 0.5,
            "sft_examples": len(sft),
            "cpt_steps": (
                config.cpt_steps
                if prior_payload is None
                else prior_payload["setup"]["cpt_steps"]
            ),
            "sft_steps": config.sft_steps
            + (0 if prior_payload is None else prior_payload["setup"]["sft_steps"]),
            "batch_size": config.batch_size,
            "learning_rate": config.learning_rate,
            "beam_size": config.beam_size,
            "seed": seed,
        },
        "results": results,
        "effects": {
            "cpt_recall_gain_random_init": results["CR1"]["recall_at_10"]
            - results["R1"]["recall_at_10"],
            "cpt_recall_gain_llm_init": results["CR2"]["recall_at_10"]
            - results["R2"]["recall_at_10"],
            "llm_init_recall_gain_without_cpt": results["R2"]["recall_at_10"]
            - results["R1"]["recall_at_10"],
            "llm_init_recall_gain_with_cpt": results["CR2"]["recall_at_10"]
            - results["CR1"]["recall_at_10"],
        },
        "paper_online_ab": {
            "lfv_engaged_users_percent": 0.07,
            "lfv_panel_ctr_percent": 0.76,
            "shorts_engaged_users_percent": 0.28,
            "shorts_panel_ctr_percent": 4.96,
        },
        "scope": (
            "Runs the paper's real decoder-only 2x2 CPT ablation with full-parameter "
            "CPT, completion-masked next-SID SFT, and token-level constrained beam "
            "search. Public MovieLens text/genre/co-occurrence features and a 135M dense "
            "LLM replace private YouTube multimodal data and Gemini MoE scale."
        ),
    }


def _training_config() -> TrainingConfig:
    """Environment overrides make smoke runs cheap without weakening defaults."""

    return TrainingConfig(
        cpt_steps=int(os.environ.get("AUTO_RESEARCH_PLUM_CPT_STEPS", "240")),
        sft_steps=int(os.environ.get("AUTO_RESEARCH_PLUM_SFT_STEPS", "240")),
        batch_size=int(os.environ.get("AUTO_RESEARCH_PLUM_BATCH_SIZE", "16")),
        evaluation_users=int(os.environ.get("AUTO_RESEARCH_PLUM_EVAL_USERS", "200")),
        beam_size=int(os.environ.get("AUTO_RESEARCH_PLUM_BEAM_SIZE", "10")),
        resume_dir=(
            Path(os.environ["AUTO_RESEARCH_PLUM_RESUME_DIR"])
            if "AUTO_RESEARCH_PLUM_RESUME_DIR" in os.environ
            else None
        ),
    )


def _prior_payload() -> dict[str, Any] | None:
    path = os.environ.get("AUTO_RESEARCH_PLUM_PREVIOUS_RESULT")
    if path is None:
        return None
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)
