from __future__ import annotations

import gc
import os
from pathlib import Path

from .data import load_office_dataset
from .model import deterministic_split, evaluate_sampled_catalog, train_pg
from .protocol import PromptConfig


CONFIG_DIR = Path(__file__).parent / "configs"


def reproduce_prompt_generation(dataset_dir: Path, seed: int = 42) -> dict:
    model_name = os.environ.get("AUTO_RESEARCH_PG_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
    steps = int(os.environ.get("AUTO_RESEARCH_PG_STEPS", "20"))
    batch_size = int(os.environ.get("AUTO_RESEARCH_PG_BATCH_SIZE", "2"))
    train_limit = int(os.environ.get("AUTO_RESEARCH_PG_TRAIN_ROWS", "4000"))
    eval_users = int(os.environ.get("AUTO_RESEARCH_PG_EVAL_USERS", "12"))
    candidates = int(os.environ.get("AUTO_RESEARCH_PG_CANDIDATES", "20"))
    dataset = load_office_dataset(dataset_dir, train_limit=train_limit)
    validation_rows = deterministic_split(dataset.validation, eval_users, seed)
    test_rows = deterministic_split(dataset.test, eval_users, seed + 1)
    variants = {
        "sid_only": "sid_only.json",
        "sid_plus_title": "title.json",
        "sid_plus_merged_title_brand": "title_brand_merged.json",
    }
    results = {}
    for name, filename in variants.items():
        config = PromptConfig.load(CONFIG_DIR / "prompt_template.json", CONFIG_DIR / filename)
        trained = train_pg(dataset, config, model_name, steps, batch_size, seed)
        results[name] = {
            "configuration": filename,
            "training": trained.training,
            "validation": evaluate_sampled_catalog(
                trained, dataset, validation_rows, candidates, seed + 10
            ),
            "test": evaluate_sampled_catalog(
                trained, dataset, test_rows, candidates, seed + 20
            ),
        }
        del trained
        gc.collect()
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            elif torch.backends.mps.is_available():
                torch.mps.empty_cache()
        except ImportError:
            pass
    best = max(
        variants,
        key=lambda name: (
            results[name]["validation"].get("hr_at_10", 0.0),
            results[name]["validation"].get("hr_at_5", 0.0),
            -results[name]["training"]["mean_prompt_tokens"],
        ),
    )
    return {
        "paper": {
            "arxiv_id": "2607.11326",
            "title": "Prompt Generation Technical Report",
            "url": "https://arxiv.org/abs/2607.11326",
            "organization": "Alibaba / Taobao Search",
        },
        "dataset": {
            "name": "MiniOneRec Amazon Reviews 2018 Office_Products",
            "source": str(dataset.source),
            "paper_train_rows": 36586,
            "paper_test_rows": 4828,
            "local_train_rows": len(dataset.train),
            "catalog_items": len(dataset.item_sids),
        },
        "setup": {
            "model": model_name,
            "seed": seed,
            "steps_per_variant": steps,
            "validation_users": len(validation_rows),
            "test_users": len(test_rows),
            "sampled_candidates": candidates,
            "selection_metric": "validation HR@10, then HR@5, then shorter prompt",
        },
        "variants": results,
        "selected_variant": best,
        "paper_results": {
            "office_sid_only_hr_at_1": 7.52,
            "office_best_hr_at_1": 8.06,
            "office_sid_only_hr_at_50": 18.81,
            "office_merged_title_brand_hr_at_50": 19.37,
            "taobao_search_transaction_lift_percent": 0.47,
            "taobao_search_gmv_lift_percent": 0.51,
            "taobao_recommendation_ipv_lift_percent": 0.66,
            "taobao_recommendation_pvr_lift_percent": 7.93,
            "shop_search_transaction_lift_percent": 4.01,
        },
        "scope": (
            "Executes the paper's shared two-JSON prompt protocol, heterogeneous sequence/text "
            "features, embedding-space mean merger, Qwen2.5-0.5B LoRA SFT, configuration-only "
            "feature iterations, validation-only selection, and held-out candidate scoring on the "
            "same MiniOneRec Office domain and published SID mapping. Local runtime uses short "
            f"LoRA runs and a deterministic {candidates}-item sampled catalog; it does not reproduce "
            "Alibaba's full-data SFT, C++ batching kernels, event-log replay, or online serving."
        ),
    }
