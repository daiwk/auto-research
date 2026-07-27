from pathlib import Path

from ..p1_2026_common import run_p1
from .model import build_dos_scorer


def reproduce_dos(dataset_dir: Path, seed: int = 42):
    return run_p1(
        key="dos", dataset_dir=dataset_dir,
        build_method=build_dos_scorer,
        baseline_name="unrotated content/collaborative ensemble",
        method_name="DOS dual-flow ORQ",
        paper_results={"online_revenue_percent": 1.15, "traffic_percent": 30.0, "duration_days": 7},
        scope="真实执行协同/内容双流的 Procrustes 正交对齐及三层 residual quantization；公开 MovieLens 替代美团私有 LLM item embedding、生成器和线上 codebook 联训。",
    )
