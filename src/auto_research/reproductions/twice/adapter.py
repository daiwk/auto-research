from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..latest_20260729_common import reproduce_twice
from ..registry import register


ADAPTER = register(ReproductionAdapter(
    key="twice",
    paper=PaperMetadata(
        arxiv_id="2607.25404",
        title="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising",
        url="https://arxiv.org/abs/2607.25404",
        track="recommendation",
        organization="Kuaishou",
        published="2026-07-28",
        topics=("advertising", "cvr", "delayed-feedback", "full-traffic"),
        online_ab=(
            OnlineABEvidence("Kwai advertising", "expected revenue", 2.486, "online A/B; later full traffic"),
            OnlineABEvidence("Kwai advertising", "conversions", 2.061, "online A/B; later full traffic"),
        ),
    ),
    run=reproduce_twice,
    render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private advertising conversion logs", "production aggregate record pipeline"),
))
