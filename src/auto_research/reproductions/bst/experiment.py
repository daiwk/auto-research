from pathlib import Path
from ..foundational_ranking import run_foundational_reproduction

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_foundational_reproduction(
        dataset_dir, seed,
        paper={"arxiv_id": "1905.06874", "title": "Behavior Sequence Transformer for E-commerce Recommendation in Alibaba", "url": "https://arxiv.org/abs/1905.06874", "organization": "Alibaba"},
        baseline_kind="din", method_kind="bst",
        baseline_name="DIN target attention", method_name="Behavior Sequence Transformer",
        paper_results={"offline_auc": 0.7894, "online_ctr_gain_percent": 7.57, "average_latency_ms": 20},
        scope="实际训练位置感知 Transformer 编码行为序列与候选 token，再用候选状态预测点击；MovieLens 替代淘宝多域稀疏特征。",
    )
