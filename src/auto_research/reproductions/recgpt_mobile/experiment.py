from __future__ import annotations

import os
from pathlib import Path

from .data import load_mobile_intent_data
from .model import MobileConfig, evaluate, load_model, quantize_weight_only, serialized_megabytes, train_lora, trigger_diagnostics


def reproduce_recgpt_mobile(dataset_dir: Path, seed: int = 42) -> dict:
    config = MobileConfig(sft_steps=int(os.environ.get("AUTO_RESEARCH_RECGPT_MOBILE_STEPS", "80")))
    data = load_mobile_intent_data(dataset_dir)
    intent_lm = load_model(config, seed)
    # All three variants are compared on the exact same held-out rows.
    base = evaluate(intent_lm, data.test, data, config)
    fp32_mb = serialized_megabytes(intent_lm.model)
    training = train_lora(intent_lm, data, config, seed)
    lora = evaluate(intent_lm, data.test, data, config)
    quantized = quantize_weight_only(intent_lm)
    quantized_mb = serialized_megabytes(quantized.model)
    lora_quantized = evaluate(quantized, data.test, data, config)
    return {
        "paper": {"arxiv_id": "2605.04726", "title": "RecGPT-Mobile", "url": "https://arxiv.org/abs/2605.04726", "organization": "Alibaba / Taobao"},
        "dataset": {"name": "MovieLens 1M next-intent proxy", "training_examples": len(data.train), "validation_users": len(data.validation), "test_users": len(data.test), "intent_categories": len(data.genres)},
        "setup": {"seed": seed, "model": config.model_name, "token_budget": config.token_budget, "sft_steps": config.sft_steps},
        "baseline": {"name": "base SmolLM2-135M", **base}, "method": {"name": "LoRA SFT", **lora}, "quantized_method": {"name": "LoRA + weight-only INT8", **lora_quantized},
        "relative": {"lora_semantic_accuracy_percent": 100 * (lora["semantic_intent_accuracy"] - base["semantic_intent_accuracy"]) / max(base["semantic_intent_accuracy"], 1e-12), "quantized_vs_lora_semantic_percent": 100 * (lora_quantized["semantic_intent_accuracy"] - lora["semantic_intent_accuracy"]) / max(lora["semantic_intent_accuracy"], 1e-12), "serialized_size_reduction_percent": 100 * (1 - quantized_mb / fp32_mb)},
        "training": training, "trigger": trigger_diagnostics(data.test, data, config.trigger_threshold), "model_size_mb": {"fp32": fp32_mb, "weight_only_int8": quantized_mb},
        "paper_results": {"qwen3_4b_base_total": 0.677, "qwen3_4b_lora_total": 0.829, "qwen3_4b_lora_quant_total": 0.794, "online_CLICK_percent": 1.8, "online_PAY_percent": 2.7, "online_GMV_percent": 2.5},
        "scope": "真实 SmolLM2-135M causal LM、q/v LoRA SFT、预算约束 adaptive prompt、entropy/Jaccard/JS trigger 和逐输出通道 weight-only INT8 均实际执行。当前 Mac PyTorch 无量化 kernel，前向会反量化计算，因此只比较量化误差和存储量，不把 CPU latency 冒充真机 INT8 latency。MovieLens movie/genre intent 替代淘宝购买/搜索 query；没有 GPT 改写、人审样本、生产 retrieval 或真机 fleet latency。",
    }
