from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260813_common import reproduce_sona, render_latest


ADAPTER = register(ReproductionAdapter(
    key="sona",
    paper=PaperMetadata(
        arxiv_id="2608.11015", title="Sona Technical Report",
        url="https://arxiv.org/abs/2608.11015", track="recommendation",
        organization="Yandex", published="2026-08-11",
        topics=("generative-recommendation", "semantic-id", "ranking", "history-compression"),
        online_ab=(
            OnlineABEvidence("Yandex Music My Vibe smart speakers", "active users", 4.53, "live-traffic online A/B; cascade replaced by one model", source_url="https://arxiv.org/pdf/2608.11015", source_location="Online evaluation section", significance="reported statistically significant", retrieved_at="2026-08-13"),
            OnlineABEvidence("Yandex Music My Vibe smart speakers", "total listening time", 6.30, "live-traffic online A/B; cascade replaced by one model", source_url="https://arxiv.org/pdf/2608.11015", source_location="Online evaluation section", significance="reported statistically significant", retrieved_at="2026-08-13"),
        ),
    ),
    run=reproduce_sona, render=render_latest,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Yandex private music logs and semantic tokenizer", "production candidate cascade and smart-speaker serving", "full-capacity distillation teacher"),
))
