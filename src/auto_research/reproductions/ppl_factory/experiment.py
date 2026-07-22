from __future__ import annotations

import copy
from pathlib import Path

import numpy as np

from auto_research.evolution.llm_data import load_llm_evolution_data
from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm

from ..llm_training import evaluate_language_model, require_torch, train_language_model
from .model import score_blocks, select_blocks


def reproduce_ppl_factory(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_llm_evolution_data(dataset_dir, True, vocab_size=1024, maximum_train_tokens=260_000, maximum_eval_tokens=32_000)
    config = MicroLMConfig(vocab_size=data.vocab_size, dimensions=80, layers=3, heads=4, sequence_length=64, expansion=3)
    torch.manual_seed(seed)
    scorer = build_micro_lm("llama_modern", config)
    pretraining = train_language_model(scorer, data.train[:120_000], steps=25, batch_size=6, length=64, learning_rate=8e-4, seed=seed, torch=torch)
    blocks, scores = score_blocks(scorer, data.train[120_000:], 65, torch)
    ratio = 0.20
    rows = {}
    for name, mode in (("Random", "random"), ("Easy-NLL", "easy"), ("PPL-Factory", None)):
        indices = select_blocks(scores, ratio, seed, mode)
        selected = blocks[indices].reshape(-1)
        torch.manual_seed(seed + 1)
        model = build_micro_lm("llama_modern", config)
        model.load_state_dict(copy.deepcopy(scorer.state_dict()))
        training = train_language_model(model, selected, steps=45, batch_size=6, length=64, learning_rate=5e-4, seed=seed + 1, torch=torch)
        metrics = evaluate_language_model(model, data.test, length=64, batches=32, torch=torch)
        rows[name] = {**training, **metrics, "selected_blocks": len(indices), "mean_selection_nll": float(scores[indices].mean())}
    baseline, method = rows["Random"], rows["PPL-Factory"]
    return {
        "paper": {"arxiv_id": "2607.18199", "title": "PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning", "url": "https://arxiv.org/abs/2607.18199", "track": "llm"},
        "dataset": {"name": "WikiText-2", "train_tokens": len(data.train), "test_tokens": len(data.test)},
        "setup": {"seed": seed, "selection_ratio": ratio, "block_size": 65, "fine_tuning_steps": 45, "same_selected_tokens_and_optimizer": True, "budget_rule": "middle"},
        "scorer_pretraining": pretraining,
        "variants": rows,
        "relative": {"perplexity_reduction_vs_random_percent": 100.0 * (baseline["perplexity"] - method["perplexity"]) / baseline["perplexity"]},
        "paper_results": {"gsm8k_vs_full_data_points_at_10_percent": 0.9, "math_vs_full_data_points_at_10_percent": 4.8, "minimum_reported_ratio_percent": 1},
        "scope": "实际先训练冻结的 causal LM scorer，按固定块计算逐 token NLL，再执行论文 Algorithm 1 的 random/easy/middle 选择，并从同一 checkpoint 以相同 token 与 step 预算微调。WikiText-2 CLM 复现论文的语言建模分支；未复现 Qwen2.5-7B GSM8K/MATH response-only NLL。",
    }
