from pathlib import Path

from ..p1_2026_common import run_p1
from .model import build_hisac_scorer


def reproduce_hisac(dataset_dir: Path, seed: int = 42):
    return run_p1(
        key="hisac", dataset_dir=dataset_dir,
        build_method=build_hisac_scorer,
        baseline_name="recent-window dense attention proxy",
        method_name="HiSAC hierarchical sparse interest agents",
        paper_results={"online_ctr_percent": 1.65},
        scope="真实执行三层 RQ、层级投票生成 user-specific interest agents，再以 query-conditioned soft routing 聚合；MovieLens 最长 64 行为验证算法路径，不等同于淘宝超长序列和线上 kernel。",
    )
