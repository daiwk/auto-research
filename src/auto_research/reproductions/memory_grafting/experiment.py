from __future__ import annotations

from pathlib import Path

from auto_research.evolution.llm_data import load_llm_evolution_data

from ..llm_training import evaluate_language_model, require_torch, train_language_model
from .model import build_frozen_bank, build_recipient, frequent_ngrams, memory_injector


def reproduce_memory_grafting(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_llm_evolution_data(
        dataset_dir, True, vocab_size=1024,
        maximum_train_tokens=180_000, maximum_eval_tokens=24_000,
    )
    torch.manual_seed(seed + 100)
    teacher, config = build_recipient(data.vocab_size)
    teacher_training = train_language_model(
        teacher, data.train, steps=30, batch_size=4,
        length=config.sequence_length, learning_rate=8e-4,
        seed=seed + 100, torch=torch,
    )
    keys = frequent_ngrams(data.train[:100_000], capacity=192)
    bank = build_frozen_bank(teacher, keys, torch)

    rows = {}
    for name in ("Transformer", "Engram", "Memory Grafting"):
        torch.manual_seed(seed)
        model, config = build_recipient(data.vocab_size)
        injector = None
        if name != "Transformer":
            injector = memory_injector(
                keys, bank, config.dimensions, hash_buckets=256,
                exact=name == "Memory Grafting", torch=torch,
            )
            model.attach_memory(injector, layer=0)
        training = train_language_model(
            model, data.train, steps=45, batch_size=4,
            length=config.sequence_length, learning_rate=8e-4,
            seed=seed, torch=torch,
        )
        metrics = evaluate_language_model(
            model, data.validation, length=config.sequence_length,
            batches=24, torch=torch,
        )
        rows[name] = {
            **training, **metrics,
            "memory_hit_rate": 0.0 if injector is None else injector.last_hit_rate,
            "frozen_memory_vectors": 0 if injector is None else len(keys),
        }

    baseline, engram, method = rows["Transformer"], rows["Engram"], rows["Memory Grafting"]
    return {
        "paper": {
            "arxiv_id": "2605.20948",
            "title": "Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory",
            "url": "https://arxiv.org/abs/2605.20948",
            "track": "llm",
        },
        "dataset": {"name": "WikiText-2", "train_tokens": len(data.train), "validation_tokens": len(data.validation)},
        "setup": {"seed": seed, "recipient_steps": 45, "teacher_steps": 30, "ngram_orders": [2, 3, 4], "memory_capacity": len(keys), "same_recipient_budget": True},
        "teacher": teacher_training,
        "variants": rows,
        "relative": {
            "ppl_vs_transformer_percent": 100.0 * (baseline["perplexity"] - method["perplexity"]) / baseline["perplexity"],
            "ppl_vs_engram_percent": 100.0 * (engram["perplexity"] - method["perplexity"]) / engram["perplexity"],
        },
        "paper_results": {"MoE_average": 51.95, "Engram_average": 52.43, "Memory_Grafting_average": 53.86},
        "stages": {
            "offline_teacher": True,
            "frozen_exact_ngram_bank": True,
            "longest_match_orders": [4, 3, 2],
            "engram_fallback": True,
            "query_key_gate": True,
            "short_convolution": True,
        },
        "scope": "实际预训练 grafting model，离线抽取 frequent 2/3/4-gram 最后 token hidden state并冻结；recipient 执行最长后缀精确查询、Engram hash fallback、独立 K/V 投影、query-key gate、short convolution 和 residual write。WikiText-2 的 64-d 模型与 192-entry bank 替代论文 0.92B/2.8B 模型和 3M-entry bank。",
    }
