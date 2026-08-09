from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_hrpo, render_latest

ADAPTER = register(ReproductionAdapter(
    key="hrpo", paper=PaperMetadata(
        arxiv_id="2608.00750", title="Hierarchical Residual Policy Optimization for Generative Recommendations",
        url="https://arxiv.org/abs/2608.00750", track="recommendation",
        code_url="https://github.com/Applied-Machine-Learning-Lab/KDD2026-HRPO",
        organization="City University of Hong Kong / Kuaishou", published="2026-08-01",
        publication_label="KDD 2026", topics=("generative-recommendation", "reinforcement-learning", "semantic-id", "credit-assignment"),
        online_ab=(
            OnlineABEvidence("Kuaishou Fiction IAA", "Target Cost", 3.49, "online A/B"),
            OnlineABEvidence("Kuaishou Mini-Game IAA", "Target Cost", .186, "online A/B"),
        )), run=reproduce_hrpo, render=render_latest,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Kuaishou private advertising logs", "production SID policy and periodic deployment"),
))
