from pathlib import Path
from ..foundational_ranking import run_foundational_reproduction

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_foundational_reproduction(
        dataset_dir, seed,
        paper={"arxiv_id": "1606.07792", "title": "Wide & Deep Learning for Recommender Systems", "url": "https://arxiv.org/abs/1606.07792", "organization": "Google"},
        baseline_kind="deep", method_kind="wide-deep",
        baseline_name="deep-only embedding MLP", method_name="joint wide crosses + deep MLP",
        paper_results={"offline_auc": 0.728, "online_acquisition_gain_percent": 3.9, "gain_over_deep_only_percent": 1.0},
        scope="实际联合训练 deep embedding MLP、候选 bias 与历史/候选 genre cross-product wide 路径。MovieLens 显式 genre cross 替代 Google Play 亿级稀疏安装特征。",
    )
