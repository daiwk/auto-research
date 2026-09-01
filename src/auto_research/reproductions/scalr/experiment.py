from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import build_translation, score_scalr, synthesize_events


def reproduce_scalr(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    state = build_translation(data)
    synthetic = synthesize_events(data, state, seed)
    baseline = evaluate(
        data, lambda history: score_scalr(data, synthetic, history, "deterministic")
    )
    method = evaluate(data, lambda history: score_scalr(data, synthetic, history, "sampled"))
    return summary_result(
        key="scalr",
        paper={
            "arxiv_id": "2606.00282",
            "title": "Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems",
            "url": "https://arxiv.org/abs/2606.00282",
            "organization": "Meta",
        },
        data=data,
        baseline_name="deterministic top-k cross-domain translation",
        method_name="SCALR probabilistic synthetic events",
        baseline=baseline,
        proposed=method,
        stages={
            "translation_domains": int(state["probabilities"].shape[0]),
            "synthetic_events": synthetic["synthetic_events"],
            "deterministic_catalog_coverage": synthetic["deterministic_catalog_coverage"],
            "sampled_catalog_coverage": synthetic["sampled_catalog_coverage"],
            "generation_strategy": "sample from empirical P(target item | source event)",
        },
        paper_results={
            "online_cvr_lift_percent_range": [0.14, 0.24],
            "experiment_duration": "multiple weeks",
        },
        scope=(
            "实际从重叠用户估计跨域 item translation distribution，分别生成 top-k 与概率采样事件并在同一"
            "公开切分评测；MovieLens genre 代理不同产品域，未复刻 Meta 私有 source surface 与转化日志。"
        ),
    )
