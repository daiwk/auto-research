from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..latest_20260729_common import reproduce_melo
from ..registry import register


ADAPTER = register(ReproductionAdapter(
    key="melo",
    paper=PaperMetadata(
        arxiv_id="2607.23718",
        title="Melo: A Production LLM-Powered Music Recommendation Agent",
        url="https://arxiv.org/abs/2607.23718",
        track="recommendation",
        organization="NetEase Cloud Music / Zhejiang University of Technology",
        published="2026-07-26",
        topics=("llm-recommendation", "agent", "entity-grounding", "reflection"),
        online_ab=(
            OnlineABEvidence("NetEase Cloud Music playlist surfaces", "playlist retention lower bound (pp)", 2.0, "one-month randomized system-level A/B"),
        ),
    ),
    run=reproduce_melo,
    render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("production music search index", "Muse Mix product surface and private traffic"),
))
