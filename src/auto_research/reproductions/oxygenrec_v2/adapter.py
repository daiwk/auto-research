from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_oxygenrec_v2
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="oxygenrec-v2",
        paper=PaperMetadata(
            arxiv_id="2607.24255",
            title="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation",
            url="https://arxiv.org/abs/2607.24255",
            track="recommendation",
            organization="JD.COM",
            published="2026-07-27",
            topics=("generative-recommendation", "privileged-distillation", "behavior-instruction"),
            online_ab=(
                OnlineABEvidence("JD.COM six production surfaces", "UCTCVR", 4.44, "5–20% traffic, 5–8 days"),
                OnlineABEvidence("JD.COM homepage floor", "GMV", 21.21, "bucketed A/B, p<0.05"),
            ),
        ),
        run=reproduce_oxygenrec_v2,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "JD private multi-behavior logs",
            "three-level production semantic IDs",
            "3B-A1B MoE serving stack",
        ),
    )
)
