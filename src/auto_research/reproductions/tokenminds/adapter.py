from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tokenminds
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="tokenminds",
        paper=PaperMetadata(
            arxiv_id="2606.25147",
            title="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems",
            url="https://arxiv.org/abs/2606.25147",
            track="recommendation",
            organization="Google DeepMind / YouTube",
            published="2026-06-23",
            topics=(
                "llm-recommendation",
                "user-modeling",
                "semantic-id",
                "cross-scenario",
                "ranking",
                "serving",
            ),
            online_ab=(
                OnlineABEvidence(
                    "YouTube SFV",
                    "Engaged Users",
                    0.11,
                    "seven-day production A/B; subsequently full user traffic",
                    source_url="https://arxiv.org/pdf/2606.25147",
                    source_location="Table 4 and Section 4.3",
                    experiment_duration="7 days",
                    significance="95% confidence",
                    retrieved_at="2026-08-09",
                ),
                OnlineABEvidence(
                    "YouTube SFV",
                    "Satisfied Engagement",
                    0.62,
                    "seven-day production A/B; subsequently full user traffic",
                    source_url="https://arxiv.org/pdf/2606.25147",
                    source_location="Table 4 and Section 4.3",
                    experiment_duration="7 days",
                    significance="95% confidence",
                    retrieved_at="2026-08-09",
                ),
            ),
        ),
        run=reproduce_tokenminds,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Gemini 370M MoE encoder and 370M decoder with PLUM CPT",
            "YouTube LFV/SFV/search private training corpus",
            "multi-context beam decoding and asynchronous billion-user serving",
        ),
    )
)
