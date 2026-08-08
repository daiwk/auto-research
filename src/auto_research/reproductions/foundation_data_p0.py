"""Public-data implementations of DoReMi and Data Mixing Laws."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from auto_research.evolution.llm_data import load_llm_evolution_data


def _domains(dataset_dir: Path):
    data = load_llm_evolution_data(
        dataset_dir, allow_network=True, vocab_size=512,
        maximum_train_tokens=120_000, maximum_eval_tokens=12_000,
        benchmark_suite="core",
    )
    first = np.asarray(data.train, dtype=np.int64)
    second = np.asarray(data.narrative, dtype=np.int64)
    if len(second) < 1_000:
        second = first[1::2]
        first = first[::2]
    return data, (first, second)


def _distribution(tokens, vocab, smoothing=1.0):
    counts = np.bincount(tokens, minlength=vocab).astype(np.float64) + smoothing
    return counts / counts.sum()


def _loss(tokens, probability):
    return float(-np.log(probability[tokens] + 1e-12).mean())


def reproduce_doremi(dataset_dir: Path, seed: int = 42):
    data, domains = _domains(dataset_dir)
    vocab = data.vocab_size
    reference = [_distribution(domain[: len(domain) // 3], vocab) for domain in domains]
    proxy = np.ones(vocab) / vocab
    weights = np.ones(len(domains)) / len(domains)
    history = []
    for step in range(80):
        losses = np.asarray([_loss(domain, proxy) for domain in domains])
        reference_losses = np.asarray([
            _loss(domain, ref) for domain, ref in zip(domains, reference)
        ])
        excess = losses - reference_losses
        weights *= np.exp(0.2 * excess)
        weights = np.maximum(weights, 0.01)
        weights /= weights.sum()
        target = sum(
            weight * _distribution(domain, vocab)
            for weight, domain in zip(weights, domains)
        )
        proxy = 0.85 * proxy + 0.15 * target
        history.append({"step": step, "weights": weights.tolist(), "excess": excess.tolist()})
    uniform = sum(_distribution(domain, vocab) for domain in domains) / len(domains)
    validation_domains = [np.asarray(data.validation)[index::2] for index in range(2)]
    baseline = float(np.mean([_loss(domain, uniform) for domain in validation_domains]))
    proposed = float(np.mean([_loss(domain, proxy) for domain in validation_domains]))
    return {
        "paper": {"title": "DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining"},
        "dataset": {"name": "WikiText-2 + public narrative domain", "tokens": sum(map(len, domains))},
        "baseline": {"name": "uniform mixture", "validation_loss": baseline},
        "method": {"name": "DoReMi group-DRO mixture", "validation_loss": proposed},
        "relative": {"validation_loss_percent": 100 * (proposed - baseline) / baseline},
        "stages": {"proxy_steps": 80, "final_domain_weights": weights.tolist(),
                   "worst_excess_loss_updates": len(history), "reference_models": len(reference)},
        "paper_results": {"few_shot_accuracy_points": 6.5, "training_speedup_x": 2.6},
        "scope": "实际在两个公开文本域上训练 reference unigram proxy，执行 group-DRO excess-loss 指数权重更新，再以所学配比评估；未复刻 The Pile、280M proxy 与 8B target。",
    }


def reproduce_data_mixing_laws(dataset_dir: Path, seed: int = 42):
    data, domains = _domains(dataset_dir)
    vocab = data.vocab_size
    domain_probs = [_distribution(domain, vocab) for domain in domains]
    validation_domains = [np.asarray(data.validation)[index::2] for index in range(2)]
    proportions = np.linspace(0.05, 0.95, 10)
    observed = []
    for proportion in proportions:
        mixture = proportion * domain_probs[0] + (1 - proportion) * domain_probs[1]
        observed.append([_loss(domain, mixture) for domain in validation_domains])
    observed = np.asarray(observed)
    # The paper's law is exponential in a linear form of mixture proportions.
    # Fit log(loss - floor) per validation domain on small-mixture runs.
    predictions = []
    grid = np.linspace(0.01, 0.99, 99)
    for axis in range(observed.shape[1]):
        floor = 0.95 * observed[:, axis].min()
        coefficients = np.polyfit(proportions, np.log(observed[:, axis] - floor), 1)
        predictions.append(floor + np.exp(np.polyval(coefficients, grid)))
    predicted = np.stack(predictions, axis=1)
    optimum = float(grid[np.argmin(predicted.mean(1))])
    selected = optimum * domain_probs[0] + (1 - optimum) * domain_probs[1]
    uniform = 0.5 * (domain_probs[0] + domain_probs[1])
    baseline = float(np.mean([_loss(domain, uniform) for domain in validation_domains]))
    proposed = float(np.mean([_loss(domain, selected) for domain in validation_domains]))
    return {
        "paper": {"title": "Data Mixing Laws: Optimizing Data Mixtures by Predicting LM Performance"},
        "dataset": {"name": "WikiText-2 + public narrative domain", "tokens": sum(map(len, domains))},
        "baseline": {"name": "uniform mixture", "validation_loss": baseline},
        "method": {"name": "predicted optimal mixture", "validation_loss": proposed},
        "relative": {"validation_loss_percent": 100 * (proposed - baseline) / baseline},
        "stages": {"pilot_mixtures": len(proportions), "law": "L_i(p)=c_i+exp(a_i p+b_i)",
                   "selected_domain_0_weight": optimum, "unseen_grid_points": len(grid)},
        "paper_results": {"equivalent_extra_training_percent": 48.0},
        "scope": "实际用公开文本域的十组 pilot mixture 拟合逐域指数 mixing law，并在未训练配比网格上选择最优配比；小型 unigram proxy 不等同于 RedPajama 多模型 scaling curve。",
    }


def render(result):
    baseline, method = result["baseline"], result["method"]
    return "\n".join([
        f"# {result['paper']['title']}", "",
        f"公开数据：{result['dataset']['name']}（{result['dataset']['tokens']} tokens）", "",
        "| Variant | Validation loss |", "|---|---:|",
        f"| {baseline['name']} | {baseline['validation_loss']:.4f} |",
        f"| {method['name']} | {method['validation_loss']:.4f} |", "",
        f"相对均匀配比：loss {result['relative']['validation_loss_percent']:+.2f}%。", "",
        "## 复现边界", "", result["scope"], "",
    ])
