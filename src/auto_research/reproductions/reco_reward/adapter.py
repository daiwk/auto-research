from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..latest_20260729_common import reproduce_reco_reward
from ..registry import register


ADAPTER = register(ReproductionAdapter(
    key="reco-reward",
    paper=PaperMetadata(
        arxiv_id="2607.25901",
        title="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation",
        url="https://arxiv.org/abs/2607.25901",
        track="recommendation",
        organization="Kuaishou / Nankai University / Chinese Academy of Sciences",
        published="2026-07-28",
        topics=("llm-recommendation", "multimodal", "reinforcement-learning", "retrieval"),
        online_ab=(
            OnlineABEvidence("Kuaishou live recommendation", "key-page effective-user penetration", 0.265, "one-week online A/B"),
            OnlineABEvidence("Kuaishou live recommendation", "outflow exposure", 0.791, "one-week online A/B"),
        ),
    ),
    run=reproduce_reco_reward,
    render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Qwen3.5-9B multimodal policy", "private Kuaishou live-stream behavior"),
))
