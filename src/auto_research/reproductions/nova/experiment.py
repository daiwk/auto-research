from pathlib import Path

from ..industrial_2026 import base_scores
from ..p0_2026_common import run_scoring_reproduction
from .model import verified_candidate_search


def reproduce_nova(dataset_dir: Path, seed: int = 42):
    def build(data):
        candidates = [
            ("transition-specialist", lambda h: data.transition[h[-1]]),
            ("content-specialist", lambda h: data.cosine[list(h[-6:])].mean(0)),
            ("popularity-specialist", lambda h: data.popularity),
            ("invalid-shape-control", lambda h: data.popularity[:-1]),
        ]
        return verified_candidate_search(data, candidates)

    return run_scoring_reproduction(
        key="nova", paper={"arxiv_id": "2606.27243", "title": "NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems", "url": "https://arxiv.org/abs/2606.27243", "organization": "Tencent"},
        dataset_dir=dataset_dir, build_method=build,
        baseline_name="fixed transition/content/popularity ensemble",
        method_name="NOVA verified specialist selection",
        paper_results={"online_gmv_stage1_percent": 1.25, "online_gmv_stage2_percent": 1.70, "online_gmv_stage3_percent": 2.02},
        scope="真实执行候选生成后的四级验证：输出契约、可执行性、数值有限性和隔离 validation 离线门禁，并保留被拒候选。公开 MovieLens 替代广告特征、生产 agent 和线上灰度平台。",
    )
