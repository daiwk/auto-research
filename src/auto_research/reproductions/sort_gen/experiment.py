from __future__ import annotations

from pathlib import Path

from .data import load_sort_data
from .model import SortConfig, build_model, evaluate, formula_greedy, mask_driven_generate, train


def reproduce_sort_gen(dataset_dir: Path, seed: int = 42) -> dict:
    config = SortConfig(); data = load_sort_data(dataset_dir, list_size=config.list_size)
    model, training = train(build_model(data.features, config), data, config, seed)
    split = len(data.evaluation) // 2; validation = data.evaluation[:split]; test = data.evaluation[split:]
    lambdas = (0.70, 0.85, 1.0)
    validation_results = {str(value): evaluate(validation, lambda row, value=value: mask_driven_generate(model, row, data.features, config, value), data.features, config.list_size) for value in lambdas}
    selected = max(lambdas, key=lambda value: validation_results[str(value)]["click_per_slate"] + validation_results[str(value)]["pay_per_slate"] + 0.05 * validation_results[str(value)]["gmv_proxy_per_slate"] + validation_results[str(value)]["ilad"])
    baseline = evaluate(test, lambda row: formula_greedy(row, config.list_size), data.features, config.list_size)
    method = evaluate(test, lambda row: mask_driven_generate(model, row, data.features, config, selected), data.features, config.list_size)
    relative = {key + "_percent": 100 * (method[key] - baseline[key]) / max(abs(baseline[key]), 1e-12) for key in ("click_per_slate", "pay_per_slate", "gmv_proxy_per_slate", "ilad")}
    return {
        "paper": {"arxiv_id": "2505.07197", "title": "A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao", "url": "https://arxiv.org/abs/2505.07197", "organization": "Alibaba / Taobao & Tmall"},
        "dataset": {"name": "MovieLens 1M exposure-slate proxy", "training_slates": len(data.train), "validation_slates": len(validation), "test_slates": len(test), "candidate_size": 20, "output_size": config.list_size},
        "setup": {"seed": seed, "steps": config.training_steps, "selected_mmr_lambda": selected, "selection": "validation click + pay + 0.05*GMV + ILAD"},
        "baseline": {"name": "item-level greedy formula", **baseline}, "method": {"name": "SORT ordered regression + queues + mask-driven MMR", **method}, "relative": relative,
        "training": training, "validation": validation_results,
        "paper_results": {"vs_formula_CLICK_percent": 9.61, "vs_formula_ORDER_percent": 8.35, "vs_formula_GMV_percent": 13.67, "vs_deployed_FFT_fastDPP_CLICK_percent": 4.13, "vs_deployed_FFT_fastDPP_GMV_percent": 8.10, "latency_ms": 19},
        "scope": "实际训练 causal Transformer 的 CLICK/PAY ordered-regression threshold heads，并执行三路多目标队列、单次 batched model call、mask 去重和内嵌 MMR。MovieLens rating/genre/popularity 替代淘宝 exposure、CTR/CVR/GMV 和多模态 embedding；不宣称复现 19 ms 生产 kernel。",
    }
