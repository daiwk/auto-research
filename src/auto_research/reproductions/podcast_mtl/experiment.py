from pathlib import Path

from ..p1_2026_common import run_p1
from .model import build_podcast_mtl_scorer


def reproduce_podcast_mtl(dataset_dir: Path, seed: int = 42):
    return run_p1(
        key="podcast-mtl", dataset_dir=dataset_dir,
        build_method=build_podcast_mtl_scorer,
        baseline_name="single-task popularity/content ranker",
        method_name="Spotify shared low-rank multi-task model",
        paper_results={"effective_cost_per_stream_percent": -22.0, "podcast_play_rate_min_percent": 18.0, "podcast_play_rate_max_percent": 24.0},
        scope="真实联合拟合 organic stream 与 promotion 两个目标、共享低秩表示并单独评估冷物品；MovieLens item/genre 代理 podcast/ad 特征，未使用 Spotify 私有 impression 和出价日志。",
    )
