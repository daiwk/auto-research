from __future__ import annotations

from dataclasses import replace
import random

from .models import Genome, PaperInspiration


def allowed_architectures(model: str, direction: str, papers: list[PaperInspiration]) -> list[str]:
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
    mapping = {
        p.architecture: p.architecture for p in papers
        if p.architecture not in {"longer", "unimixer"}
        and (not text or p.architecture.replace("_", "") in text.replace("-", "").replace("_", "") or p.title.lower().split(":", 1)[0] in text)
    }
    values.extend(mapping.values())
    return list(dict.fromkeys(values))


def propose(parent: Genome, generation: int, index: int, architectures: list[str], rng: random.Random):
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


def round_record(generation, parent, trials, champion):
    ranked = sorted(trials, key=lambda trial: trial.fitness, reverse=True)
    return {
        "generation": generation, "parent": parent.trial_id,
        "hypotheses": [{"trial_id": t.trial_id, "rationale": t.rationale, "architecture": t.genome.architecture} for t in trials],
        "observations": [{"trial_id": t.trial_id, "ndcg_at_10": t.fitness, "status": t.status} for t in ranked],
        "decision": f"下一轮围绕 {champion.trial_id} / {champion.genome.architecture} 继续搜索",
        "improved": champion.fitness > parent.fitness,
    }
