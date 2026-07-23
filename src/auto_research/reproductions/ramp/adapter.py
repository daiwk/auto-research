from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_ramp
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="ramp",
    paper=PaperMetadata(
        arxiv_id="2607.17473",
        title="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways",
        url="https://arxiv.org/abs/2607.17473",
        code_url="https://github.com/Ruixinhua/RAMP",
        track="recommendation",
        organization="Huawei Ireland Research Center / University College Dublin",
        published="2026-07-20",
        topics=("advertising", "privacy", "distillation", "missing-features"),
        online_ab=(
            OnlineABEvidence("Huawei industrial CVR prediction", "Total advertiser value", 3.0, "production A/B; paper reports over 3%"),
        ),
    ),
    run=reproduce_ramp,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private IndustryAd dataset and production CVR stack",),
))
