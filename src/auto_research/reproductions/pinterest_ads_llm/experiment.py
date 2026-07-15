from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from .data import load_ads_data
from .model import (
    predict_scores,
    tower_scores,
    train_grpo,
    train_predictor,
    train_two_tower,
)


def reproduce_pinterest_ads_llm(dataset_dir: Path, seed: int = 42) -> dict:
    model_name = os.environ.get(
        "AUTO_RESEARCH_PIN_ADS_MODEL", "HuggingFaceTB/SmolLM2-135M-Instruct"
    )
    sft_steps = int(os.environ.get("AUTO_RESEARCH_PIN_ADS_SFT_STEPS", "48"))
    grpo_steps = int(os.environ.get("AUTO_RESEARCH_PIN_ADS_GRPO_STEPS", "16"))
    tower_steps = int(os.environ.get("AUTO_RESEARCH_PIN_ADS_TOWER_STEPS", "160"))
    train_rows = int(os.environ.get("AUTO_RESEARCH_PIN_ADS_TRAIN_ROWS", "12000"))
    eval_users = int(os.environ.get("AUTO_RESEARCH_PIN_ADS_EVAL_USERS", "32"))
    data = load_ads_data(dataset_dir, train_rows, eval_users, 48, seed)
    predictor, sft_training = train_predictor(data, model_name, sft_steps, seed)
    validation_sft = evaluate_advertisers(predictor, data.validation, False)
    test_sft = evaluate_advertisers(predictor, data.test, False)
    grpo_training = train_grpo(predictor, data, grpo_steps, seed + 1)
    validation_grpo = evaluate_advertisers(predictor, data.validation, True)
    test_grpo = evaluate_advertisers(predictor, data.test, True)
    selected = "sft_grpo" if validation_grpo["recall_at_20"] >= validation_sft["recall_at_20"] else "sft"
    use_grpo = selected == "sft_grpo"
    user_tower, item_tower, tower_training = train_two_tower(data, tower_steps, seed)
    downstream = evaluate_downstream(
        predictor, user_tower, item_tower, data, use_grpo, seed
    )
    return {
        "paper": {
            "arxiv_id": "2605.27856",
            "title": "Fine-Tuned LLM as a Complementary Predictor Improving Ads System",
            "url": "https://arxiv.org/abs/2605.27856",
            "organization": "Pinterest",
        },
        "dataset": {
            "name": "MiniOneRec Amazon Office_Products advertiser proxy",
            "source": str(data.source),
            "train_rows": len(data.train),
            "validation_users": len(data.validation),
            "test_users": len(data.test),
            "advertisers": len(data.advertiser_names),
            "items": len(data.item_vectors),
        },
        "setup": {
            "model": model_name,
            "seed": seed,
            "selection": "validation advertiser Recall@20",
            "selected_variant": selected,
        },
        "training": {
            "sft": sft_training,
            "grpo": grpo_training,
            "two_tower": tower_training,
        },
        "validation": {"sft": validation_sft, "sft_grpo": validation_grpo},
        "test": {"sft": test_sft, "sft_grpo": test_grpo},
        "downstream": downstream,
        "paper_results": {
            "v1_zero_shot_recall_at_20": 0.422,
            "v1_sft_grpo_recall_at_20": 0.683,
            "v1_sid_sft_grpo_recall_at_20": 0.755,
            "ctcvr_auc_lift_percent": 0.06,
            "vtcvr_auc_lift_percent": 0.09,
            "online_roas_percent": 4.94,
            "online_opt_in_roas_percent": 6.69,
        },
        "scope": (
            "Executes an open-source causal LM with LoRA SFT on next-advertiser text, "
            "group-relative clipped policy optimization using the paper's position and "
            "format reward, constrained advertiser decoding, a trained two-tower item "
            "retriever, fixed-quota complementary retrieval, and downstream advertiser-score "
            "feature fusion. Amazon brands and purchases replace Pinterest advertisers, "
            "cross-site conversions, URLs, private SIDs, and live traffic."
        ),
    }


def evaluate_advertisers(predictor, rows, use_grpo):
    ranks = []
    for row in rows:
        scores = predict_scores(predictor, row, use_grpo)
        order = np.argsort(scores)[::-1]
        ranks.append(int(np.flatnonzero(order == row.target_advertiser)[0]) + 1)
    return {
        "users": len(rows),
        "recall_at_1": float(np.mean([rank <= 1 for rank in ranks])),
        "recall_at_5": float(np.mean([rank <= 5 for rank in ranks])),
        "recall_at_20": float(np.mean([rank <= 20 for rank in ranks])),
        "mean_rank": float(np.mean(ranks)),
    }


def evaluate_downstream(predictor, user_tower, item_tower, data, use_grpo, seed):
    validation = _downstream_rows(
        predictor, user_tower, item_tower, data, data.validation, use_grpo, seed
    )
    coefficients = (0.0, 0.1, 0.25, 0.5, 1.0)
    selected = max(coefficients, key=lambda value: _ranking_auc(validation, value))
    test = _downstream_rows(
        predictor, user_tower, item_tower, data, data.test, use_grpo, seed + 1
    )
    quotas = (0, 5, 10, 20)
    quota = max(quotas, key=lambda value: (_retrieval_recall(validation, value), -value))
    return {
        "retrieval_recall_at_50_baseline": _retrieval_recall(test, 0),
        "retrieval_recall_at_50_complementary": _retrieval_recall(test, quota),
        "retrieval_llm_quota": quota,
        "ranking_llm_feature_coefficient": selected,
        "ranking_auc_baseline": _ranking_auc(test, 0.0),
        "ranking_auc_with_llm_feature": _ranking_auc(test, selected),
        "quota": f"{50 - quota} conventional + {quota} advertiser-filtered items",
    }


def _downstream_rows(predictor, user_tower, item_tower, data, rows, use_grpo, seed):
    rng = np.random.default_rng(seed)
    output = []
    for row in rows:
        advertiser_scores = predict_scores(predictor, row, use_grpo)
        item_scores = tower_scores(user_tower, item_tower, data, row)
        item_scores[list(set(row.history))] = -np.inf
        top_advertisers = set(np.argsort(advertiser_scores)[::-1][:5])
        eligible = np.flatnonzero(np.isin(data.item_advertisers, list(top_advertisers)))
        extra = eligible[np.argsort(item_scores[eligible])[::-1][:50]]
        conventional = np.argsort(item_scores)[::-1][:50]
        negative_pool = np.asarray(
            [item for item in range(len(data.item_vectors)) if item != row.target_item]
        )
        negatives = rng.choice(negative_pool, 19, replace=False).tolist()
        candidates = [row.target_item, *negatives]
        labels = np.asarray([1] + [0] * len(negatives), dtype=np.float32)
        brand_score = np.asarray(
            [
                advertiser_scores[data.item_advertisers[item]]
                if data.item_advertisers[item] >= 0
                else advertiser_scores.min()
                for item in candidates
            ]
        )
        output.append(
            {
                "target": row.target_item,
                "conventional": conventional,
                "extra": extra,
                "labels": labels,
                "base": item_scores[candidates],
                "llm": brand_score,
            }
        )
    return output


def _retrieval_recall(rows, quota):
    hits = []
    for row in rows:
        blended = np.concatenate((row["conventional"][: 50 - quota], row["extra"][:quota]))
        hits.append(row["target"] in set(blended))
    return float(np.mean(hits))


def _ranking_auc(rows, coefficient):
    positives, negatives = [], []
    for row in rows:
        base = _zscore(row["base"])
        llm = _zscore(row["llm"])
        score = base + coefficient * llm
        positives.extend(score[row["labels"] == 1])
        negatives.extend(score[row["labels"] == 0])
    if not positives or not negatives:
        return 0.5
    return float(np.mean([positive > negative for positive in positives for negative in negatives]))


def _zscore(values):
    finite = np.nan_to_num(np.asarray(values, dtype=np.float64), neginf=-20.0)
    return (finite - finite.mean()) / max(float(finite.std()), 1e-8)
