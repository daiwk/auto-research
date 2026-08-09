from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result
from .model import actor_critic_search, recipe_scorer


def reproduce_agentic_rec_tune(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    baseline = evaluate(data, lambda h: base_scores(data, h))
    champion, trace = actor_critic_search(data)
    method = evaluate(data, recipe_scorer(data, champion))
    return summary_result(key="agentic-rec-tune", paper={"arxiv_id": "2604.26969", "title": "AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization", "url": "https://arxiv.org/abs/2604.26969", "organization": "Google / Discover"}, data=data, baseline_name="fixed hand-tuned ranker", method_name="AgenticRecTune champion", baseline=baseline, proposed=method, stages={"generations": 3, "actor_critic": True, "skillhub": [list(row) for row in [entry["skillhub_champion"] for entry in trace]], "champion": champion, "research_trace": trace}, paper_results={"value_retrieval_engagement1_percent": 0.75, "value_retrieval_engagement2_percent": 0.90, "diversity_reranking_percent": 3.43}, scope="实际运行三轮 Actor 提案、Critic 公共 validation 评价和 SkillHub 冠军继承；本地动作是可审计的排序权重 genome，未接入 Google 实验平台和私有 agent 工具。")
