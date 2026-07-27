from pathlib import Path

from ..p0_2026_common import run_scoring_reproduction
from .model import build_memory_scorer


def reproduce_msn(dataset_dir: Path, seed: int = 42):
    return run_scoring_reproduction(
        key="msn", paper={"arxiv_id": "2602.07526", "title": "MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation", "url": "https://arxiv.org/abs/2602.07526", "organization": "ByteDance / Douyin Search"},
        dataset_dir=dataset_dir, build_method=build_memory_scorer,
        baseline_name="dense transition/content ranker", method_name="gated top-k Product-Key Memory",
        paper_results={"online_active_days_percent": 0.0503, "online_watch_time_percent": 0.2958, "online_finish_rate_percent": 0.2071},
        scope="真实构建两轴 Product-Key Memory，只激活 top-k 记忆槽，并以可学习思想对应的置信门控融合主干。公开 genre/转移统计替代抖音搜索私有 query、超大记忆参数和定制 serving kernel。",
    )
