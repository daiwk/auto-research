from pathlib import Path

from ..p1_2026_common import run_p1
from .model import build_mdl_scorer


def reproduce_mdl(dataset_dir: Path, seed: int = 42):
    return run_p1(
        key="mdl", dataset_dir=dataset_dir,
        build_method=build_mdl_scorer,
        baseline_name="shared non-tokenized ranker",
        method_name="MDL feature/scenario/task tokens",
        paper_results={"lt30_percent": 0.0626, "query_rewrite_rate_percent": -0.3267},
        scope="真实执行 feature/scenario/task token 化、feature self-attention 与 domain-feature attention；MovieLens genre 和 next-item/popularity 任务代理抖音多场景多任务分布。",
    )
