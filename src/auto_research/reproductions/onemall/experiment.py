from pathlib import Path

from ..p1_2026_common import run_p1
from .model import build_onemall_scorer


def reproduce_onemall(dataset_dir: Path, seed: int = 42):
    return run_p1(
        key="onemall", dataset_dir=dataset_dir,
        build_method=build_onemall_scorer,
        baseline_name="shared transition/content ensemble",
        method_name="OneMall domain-prompt generative scorer",
        paper_results={
            "product_card_gmv_percent": 13.01,
            "short_video_orders_percent": 15.32,
            "live_orders_percent": 2.78,
        },
        scope="真实构建三层 residual Semantic ID、按场景条件化的生成转移分布与跨行为融合；MovieLens genre 代理电商场景，未复刻快手私有 Query-Former、Sparse MoE、RL 或线上流量。",
    )
