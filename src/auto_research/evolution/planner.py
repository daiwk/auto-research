from __future__ import annotations

from dataclasses import replace
import random

from .models import Genome, PaperInspiration


def allowed_architectures(model: str, direction: str, papers: list[PaperInspiration]) -> list[str]:
    if model == "micro-llm":
        return [
            "gpt_baseline", "gpt_gqa", "llama_modern", "llama_gqa",
            "parallel_gelu", "parallel_swiglu", "llama_gqa_parallel",
            "hyper_connections", "mhc", "qkv_depthwise_conv",
        ]
    text = direction.lower()
    requested = []
    if "longer" in text or "长序列" in text or "long sequence" in text:
        requested.append("longer")
    if "unimixer" in text or "高效 transformer" in text or "efficient transformer" in text:
        requested.append("unimixer")
    for paper in papers:
        if paper.architecture in {"longer", "unimixer"} and paper.architecture not in requested:
            requested.append(paper.architecture)
    if model == "hyformer":
        values = ["hyformer"]
        if "longer" in requested: values.append("hyformer_longer")
        if "unimixer" in requested: values.append("hyformer_unimixer")
        if set(requested) >= {"longer", "unimixer"}: values.append("hyformer_longer_unimixer")
        return values
    values = ["rankmixer_dense"]
    if "longer" in requested: values.append("rankmixer_longer")
    if "unimixer" in requested: values.append("rankmixer_unimixer")
    if set(requested) >= {"longer", "unimixer"}: values.append("rankmixer_longer_unimixer")
    direct_terms = {
        "rankmixer_whale": ("whale", "wukong", "hstu"),
        "rankmixer_tmallgs": ("tmallgs", "天猫", "field-wise"),
        "rankmixer_long_history": (
            "long-history",
            "long history",
            "长历史",
            "缓存",
        ),
        "rankmixer_ramp": ("ramp", "隐私", "特征受限", "feature availability"),
    }
    for architecture, terms in direct_terms.items():
        if any(term in text for term in terms):
            values.append(architecture)
    mapping = {
        p.architecture: p.architecture for p in papers
        if p.architecture not in {"longer", "unimixer"}
        and (not text or p.architecture.replace("_", "") in text.replace("-", "").replace("_", "") or p.title.lower().split(":", 1)[0] in text)
    }
    values.extend(mapping.values())
    return list(dict.fromkeys(values))


def propose(parent: Genome, generation: int, index: int, architectures: list[str], rng: random.Random, model: str = "rankmixer"):
    if model == "micro-llm":
        return _propose_llm(parent, generation, index, architectures, rng)
    architecture = architectures[(index + generation - 1) % len(architectures)] if generation == 1 else rng.choice(architectures)
    genome = replace(parent, architecture=architecture)
    changes = [f"结构假设：{architecture}"]
    if generation == 1:
        changes.append("公平结构消融：保持基线超参数不变")
        return genome, "；".join(changes)
    knobs = (
        ("dimensions", [32, 64, 96, 128]), ("layers", [1, 2, 3, 4]),
        ("learning_rate", [1e-4, 3e-4, 6e-4, 1e-3]),
        ("optimizer", ["adamw", "adam", "adagrad"]), ("batch_size", [24, 32, 48, 64]),
    )
    name, values = knobs[(generation + index) % len(knobs)]
    value = rng.choice(values)
    genome = replace(genome, **{name: value})
    changes.append(f"控制变量：{name}={value}")
    return genome, "；".join(changes)


def _propose_llm(parent, generation, index, architectures, rng):
    if generation == 1:
        architecture = architectures[index % len(architectures)]
        return replace(parent, architecture=architecture), (
            f"结构研究：{architecture}；保持数据配方、训练预算和后训练方法不变"
        )
    if generation == 2:
        recipes = (
            ("wikitext", 0.0), ("mixed_narrative", 0.10),
            ("mixed_narrative", 0.20), ("mixed_narrative", 0.35),
            ("curriculum", 0.20), ("curriculum", 0.35),
        )
        recipe, ratio = recipes[index % len(recipes)]
        return replace(parent, data_recipe=recipe, data_mix_ratio=ratio), (
            f"数据研究：recipe={recipe}, narrative_ratio={ratio}；冻结冠军结构与训练参数"
        )
    if generation == 3:
        methods = (
            ("none", 0.0, 0),
            ("sft", 0.0, 24),
            ("sft_low_lr", 0.0, 24),
            ("neftune", 5.0, 24),
            ("dynamic_rubric", 0.0, 24),
            ("off_context_grpo", 0.0, 24),
            ("neftune", 10.0, 24),
            ("neftune", 15.0, 24),
        )
        method, alpha, steps = methods[index % len(methods)]
        return replace(parent, post_training=method, neftune_alpha=alpha, post_steps=steps), (
            f"后训练研究：method={method}, neftune_alpha={alpha}, post_steps={steps}；冻结结构和预训练数据配方"
        )
    knobs = (
        ("dimensions", [256, 384, 512]), ("layers", [4, 6, 8]),
        ("learning_rate", [1e-4, 3e-4, 6e-4]),
        ("batch_size", [2, 4, 8]), ("sequence_length", [64, 128, 256]),
    )
    name, values = knobs[(generation + index) % len(knobs)]
    value = rng.choice(values)
    return replace(parent, **{name: value}), f"联合优化：{name}={value}"


def round_record(generation, parent, trials, champion):
    ranked = sorted(trials, key=lambda trial: trial.fitness, reverse=True)
    return {
        "generation": generation, "parent": parent.trial_id,
        "hypotheses": [{"trial_id": t.trial_id, "rationale": t.rationale, "architecture": t.genome.architecture} for t in trials],
        "observations": [{"trial_id": t.trial_id, "fitness": t.fitness, "status": t.status,
                          "validation": t.validation} for t in ranked],
        "decision": f"下一轮围绕 {champion.trial_id} / {champion.genome.architecture} 继续搜索",
        "improved": champion.fitness > parent.fitness,
    }
