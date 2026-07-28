from pathlib import Path
from ..foundational_ranking import run_foundational_reproduction

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_foundational_reproduction(
        dataset_dir, seed,
        paper={"arxiv_id": "1809.03672", "title": "Deep Interest Evolution Network for Click-Through Rate Prediction", "url": "https://arxiv.org/abs/1809.03672", "organization": "Alibaba"},
        baseline_kind="din", method_kind="dien",
        baseline_name="DIN target attention", method_name="GRU extractor + auxiliary loss + AUGRU",
        paper_results={"online_ctr_gain_percent": 20.7, "online_ecpm_gain_percent": 17.1, "online_ppc_change_percent": -3.0},
        scope="实际训练 GRU interest extractor、next-item auxiliary classifier 和 target-aware AUGRU 更新；MovieLens 行为序列替代淘宝广告日志。",
    )
