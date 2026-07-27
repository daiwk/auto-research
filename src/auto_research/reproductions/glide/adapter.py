from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_glide

ADAPTER = register(ReproductionAdapter(
    key="glide", paper=PaperMetadata(
        arxiv_id="2603.17540", title="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify",
        url="https://arxiv.org/abs/2603.17540", track="recommendation",
        organization="Spotify", published="2026-03-18",
        topics=("generative-retrieval", "semantic-id", "soft-prompt"),
        online_ab=(
            OnlineABEvidence("Spotify", "Non-habitual streaming", 5.4, "online A/B"),
            OnlineABEvidence("Spotify", "New-show discovery", 14.3, "online A/B"),
        ),
    ), run=reproduce_glide, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Spotify catalog and private user embeddings", "production constrained decoder"),
))
