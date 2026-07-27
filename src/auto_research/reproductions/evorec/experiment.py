from pathlib import Path

from ..p0_2026_common import run_scoring_reproduction
from .model import evolve_skills


def reproduce_evorec(dataset_dir: Path, seed: int = 42):
    return run_scoring_reproduction(
        key="evorec", paper={"arxiv_id": "2606.28368", "title": "EvoRec: Self-Evolving Agentic Recommender Systems", "url": "https://arxiv.org/abs/2606.28368", "organization": "Alibaba International Digital Commerce Group"},
        dataset_dir=dataset_dir, build_method=lambda data: evolve_skills(data, generations=3),
        baseline_name="fixed heuristic ensemble", method_name="three-generation EvoRec skill memory",
        paper_results={"offline_best_percent": 5.54, "online_revenue_percent": 1.85, "online_ctr_percent": 1.02},
        scope="真实执行三代候选技能试验、validation 选择和跨代方法权重记忆；每一代只继承已验证技能。公开序列替代生产工具调用、业务知识库和线上 agent 调度。",
    )
