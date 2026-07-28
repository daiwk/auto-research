from pathlib import Path
from ..foundational_ranking import run_foundational_reproduction

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_foundational_reproduction(
        dataset_dir, seed,
        paper={"arxiv_id": "2008.13535", "title": "DCN V2: Improved Deep & Cross Network", "url": "https://arxiv.org/abs/2008.13535", "organization": "Google"},
        baseline_kind="deep", method_kind="dcn-v2",
        baseline_name="embedding MLP", method_name="low-rank CrossNet-Mix + deep features",
        paper_results={"online": "significant business-metric gains across Google web-scale LTR systems; exact lift not disclosed"},
        scope="实际训练两个低秩 cross experts、输入依赖 gate、显式 x0⊙f(x) cross 与输出层；公开小数据替代 Google web-scale sparse features。",
    )
