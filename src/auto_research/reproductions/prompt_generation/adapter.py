from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_prompt_generation
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="prompt-generation",
        paper=PaperMetadata(
            arxiv_id="2607.11326",
            title="Prompt Generation Technical Report",
            url="https://arxiv.org/abs/2607.11326",
            track="recommendation",
            organization="Alibaba / Taobao Search",
            published="2026-07",
            topics=("llm-recommendation", "generative-retrieval", "autoresearch", "serving"),
            online_ab=(
                OnlineABEvidence("Taobao Search", "transaction count", 0.47, "1% traffic for 14 days"),
                OnlineABEvidence("Taobao Search", "GMV", 0.51, "1% traffic for 14 days"),
                OnlineABEvidence("Taobao Recommendation Newdetail", "IPV", 0.66, "2% traffic for 12 days"),
                OnlineABEvidence("Taobao Shop Search", "transaction count", 4.01, "10% traffic for over two weeks"),
            ),
        ),
        run=reproduce_prompt_generation,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "full 36,586-row SFT schedule and production-scale evaluation",
            "C++ batched assembly and Alibaba serving infrastructure",
            "online event tracking/replay and live A/B traffic",
        ),
    )
)

