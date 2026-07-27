from pathlib import Path

from ..p0_2026_common import run_scoring_reproduction
from .model import build_rankgraph2


def reproduce_rankgraph2(dataset_dir: Path, seed: int = 42):
    return run_scoring_reproduction(
        key="rankgraph2", paper={"arxiv_id": "2606.18379", "title": "RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation", "url": "https://arxiv.org/abs/2606.18379", "organization": "Meta"},
        dataset_dir=dataset_dir, build_method=lambda data: build_rankgraph2(data, seed),
        baseline_name="one-hop transition/content retrieval", method_name="debiased PPR + co-learned cluster index",
        paper_results={"compute_reduction_percent": 83.0, "online_ctr_percent": 0.96, "online_cvr_percent": 2.75, "production_launches": 20},
        scope="真实执行流行度校正边采样、离线多跳 PPR 和基于 PPR 表征的聚类索引，再以簇先验服务。MovieLens 图替代 Meta 超大图，未复刻分布式预计算与线上 ANN 基础设施。",
    )
