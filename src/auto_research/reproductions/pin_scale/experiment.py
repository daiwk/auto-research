from pathlib import Path

from ..p1_2026_common import run_p1
from .model import build_pin_scale_scorer


def reproduce_pin_scale(dataset_dir: Path, seed: int = 42):
    return run_p1(
        key="pin-scale", dataset_dir=dataset_dir,
        build_method=build_pin_scale_scorer,
        baseline_name="unweighted semantic/content ranker",
        method_name="Pin-SCALE engagement-aware Semantic IDs",
        paper_results={"online_repin_percent": 3.67, "online_dau_percent": 0.05},
        scope="真实训练 engagement-weighted residual codebooks 并用 SID prefix 相似度召回；MovieLens popularity/transition 代理 Pinterest engagement，未复刻私有多模态 embedding 与线上生成服务。",
    )
