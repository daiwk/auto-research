from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_pin_scale


ADAPTER = register(ReproductionAdapter(
    key="pin-scale",
    paper=PaperMetadata(
        arxiv_id="sigir2026-pin-scale",
        title="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations",
        url="https://sigir2026.org/SIGIR2026_program.pdf", track="recommendation",
        organization="Pinterest", published="2026-07-19",
        publication_label="SIGIR 2026 paper P074",
        publication_source="Pinterest Labs / SIGIR 2026",
        topics=("semantic-id", "engagement-aware", "generative-retrieval"),
        online_ab=(
            OnlineABEvidence("Pinterest", "Repin", 3.67, "online A/B"),
            OnlineABEvidence("Pinterest", "DAU", 0.05, "online A/B"),
        ),
    ),
    run=reproduce_pin_scale, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private Pinterest multimodal embeddings", "production serving stack"),
))
