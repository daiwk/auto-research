from pathlib import Path

from ..p0_2026_common import run_scoring_reproduction
from .model import train_id_proxy


def reproduce_idproxy(dataset_dir: Path, seed: int = 42):
    return run_scoring_reproduction(
        key="idproxy", paper={"arxiv_id": "2603.01590", "title": "IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs", "url": "https://arxiv.org/abs/2603.01590", "organization": "Xiaohongshu / Shanghai Jiao Tong University / Fudan University"},
        dataset_dir=dataset_dir, build_method=train_id_proxy,
        baseline_name="ID-only transition/content ranker", method_name="coarse-to-fine IDProxy alignment",
        paper_results={"content_feed_time_percent": 0.22, "content_reads_percent": 0.39, "ads_impression_percent": 1.28, "ads_cost_percent": 1.73},
        scope="用 MovieLens genre 作为公开多模态代理，真实训练到行为 ID 空间的 ridge 投影，执行粗粒度对齐、多层非线性 proxy 和残差门控。未下载 InternVL 权重，也不声称复刻小红书私有图文及广告特征。",
    )
