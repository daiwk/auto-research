from pathlib import Path

from ..p1_2026_common import run_p1
from .model import build_causal_retrieval_scorer


def reproduce_causal_retrieval(dataset_dir: Path, seed: int = 42):
    return run_p1(
        key="causal-retrieval", dataset_dir=dataset_dir,
        build_method=build_causal_retrieval_scorer,
        baseline_name="fixed non-causal retrieval ensemble",
        method_name="doubly-robust causal trigger",
        paper_results={"shopping_trigger_reduction_percent": 85.0, "total_session_percent": 0.26, "pin_save_percent": 1.10},
        scope="真实拟合 propensity、双 outcome model 与 doubly-robust pseudo-outcome，再由 uplift 阈值控制候选生成器；MovieLens 构造随机 treatment 以保证反事实覆盖，不冒充 Pinterest 随机日志或线上成本。",
    )
