from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260813_common import reproduce_metastrategy, render_latest


ADAPTER = register(ReproductionAdapter(
    key="metastrategy",
    paper=PaperMetadata(
        arxiv_id="2608.09440", title="MetaStrategy: Generative Ranking with Executable LLM Strategies",
        url="https://arxiv.org/abs/2608.09440", track="recommendation",
        organization="Alibaba / Taobao", published="2026-08-10",
        topics=("ranking", "llm-recommendation", "executable-strategy", "online-policy"),
        online_ab=(
            OnlineABEvidence("Taobao Homepage Guess You Like", "click PV", 2.11, "seven-day user-randomized online A/B", source_url="https://arxiv.org/pdf/2608.09440", source_location="Section 5.4 / online A/B table", experiment_duration="7 days", retrieved_at="2026-08-13"),
            OnlineABEvidence("Taobao Homepage Guess You Like", "transaction amount", 2.83, "seven-day user-randomized online A/B", source_url="https://arxiv.org/pdf/2608.09440", source_location="Section 5.4 / online A/B table", experiment_duration="7 days", retrieved_at="2026-08-13"),
        ),
    ),
    run=reproduce_metastrategy, render=render_latest,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Taobao private logs and production replay environment", "4B teacher to 0.8B student OPD", "diff-triggered nearline serving"),
))
