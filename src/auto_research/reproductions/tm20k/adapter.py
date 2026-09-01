from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tm20k
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="tm20k",
        paper=PaperMetadata(
            arxiv_id="2608.07055",
            title="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation",
            url="https://arxiv.org/abs/2608.07055",
            track="recommendation",
            organization="ByteDance",
            published="2026-08-07",
            topics=("advertising", "long-sequence", "token-merging", "distillation"),
            online_ab=(
                OnlineABEvidence(
                    "ByteDance e-commerce advertising",
                    "ADSS",
                    1.036,
                    "5-day experiment serving hundreds of millions of users",
                    source_url="https://arxiv.org/html/2608.07055v1",
                    source_location="Section 5.4, Table 7",
                    significance="reported p-value 0% after rounding",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_tm20k,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("20K private behavior streams", "M-Falcon serving", "advertising feature tower"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K (full public histories)",),
        baseline="same merged-token student without teacher distillation",
        metrics=("hit_at_10", "ndcg_at_10", "compression_ratio", "distilled_teacher_mse"),
        evolve_operators=("context:tm20k-merge",),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; at most 8 merged tokens",
        device_capabilities=("cpu",),
    )
)
