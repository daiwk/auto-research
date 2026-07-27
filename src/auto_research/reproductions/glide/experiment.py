from pathlib import Path

from ..p0_2026_common import run_scoring_reproduction
from .model import train_glide


def reproduce_glide(dataset_dir: Path, seed: int = 42):
    return run_scoring_reproduction(
        key="glide", paper={"arxiv_id": "2603.17540", "title": "Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify", "url": "https://arxiv.org/abs/2603.17540", "organization": "Spotify"},
        dataset_dir=dataset_dir, build_method=lambda data: train_glide(data, seed),
        baseline_name="conventional transition/content retrieval", method_name="Semantic-ID generation + dual-timescale prompts",
        paper_results={"online_non_habitual_streaming_percent": 5.4, "online_new_show_discovery_percent": 14.3},
        scope="真实生成三级 residual Semantic ID，以 code transition 执行自回归检索代理，并同时注入短期历史和长期内容画像。公开电影交互替代 Spotify podcast、生产 decoder 和约束 beam search。",
    )
