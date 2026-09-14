from .experiment import reproduce
from .report import render
from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register


ADAPTER = register(ReproductionAdapter(
    key="sirf",
    paper=PaperMetadata(
        arxiv_id="2609.11752",
        title="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control",
        url="https://arxiv.org/abs/2609.11752",
        track="recommendation",
        organization="Xiaohongshu",
        published="2026-09-10",
        publication_label="arXiv v1",
        topics=("content-understanding", "risk-control", "foundation-model", "industrial-deployment"),
        online_ab=(OnlineABEvidence(
            product="Xiaohongshu freezing-risk adjudication",
            metric="relative mis-penalization reduction",
            lift_percent=70.0,
            traffic="random treatment/control split over the same released-user population; cumulative million-user scale",
            source_url="https://arxiv.org/html/2609.11752",
            source_location="Section 5.2",
            significance="weekly active penetration significantly better; paper reports high-single-digit to low-double-digit relative lift without an exact scalar",
            retrieved_at="2026-09-14",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=("8B Qwen continued pretraining", "private account-level data", "EntiGraph/MAGA language generation", "production adjudication serving"),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("deterministic synthetic policy cases",),
    baseline="same-source SFT linear features",
    metrics=("precision", "black_recall", "accuracy"),
    evolve_operators=(),
    default_seeds=(42, 43, 44),
    budget="4,000 train / 2,000 held-out policy cases",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
