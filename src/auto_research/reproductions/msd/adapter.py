from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_msd
from .report import render_report


register(ReproductionAdapter(
    key="msd",
    paper=PaperMetadata(
        arxiv_id="2412.06860", title="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction",
        url="https://arxiv.org/abs/2412.06860", track="recommendation", organization="Meituan", published="2024-12",
        topics=("LLM distillation", "CTR", "serving efficiency"),
        online_ab=(
            OnlineABEvidence("Meituan sponsored search", "CTR", 2.12, "2024-10-20 to 2024-10-30"),
            OnlineABEvidence("Meituan sponsored search", "CPM", 2.59, "2024-10-20 to 2024-10-30"),
        ),
    ), run=reproduce_msd, render=render_report,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
    omitted_core_components=("proprietary ad features", "production cache service"),
))
