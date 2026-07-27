from pathlib import Path

from ..p0_2026_common import run_scoring_reproduction
from .model import train_solaris


def reproduce_solaris(dataset_dir: Path, seed: int = 42):
    return run_scoring_reproduction(
        key="solaris", paper={"arxiv_id": "2604.12110", "title": "SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling", "url": "https://arxiv.org/abs/2604.12110", "organization": "Meta"},
        dataset_dir=dataset_dir, build_method=train_solaris,
        baseline_name="request-time transition/content ranker", method_name="future-pair predictor + asynchronous latent cache",
        paper_results={"online_revenue_percent": 0.67, "fully_deployed": True},
        scope="真实用未来三步监督训练 pair predictor，离线生成稀疏 latent cache，并在请求时走 cache/fallback 双路径。公开数据只验证预测预计算机制，不复刻 Meta foundation model、缓存集群和全流量 serving。",
    )
