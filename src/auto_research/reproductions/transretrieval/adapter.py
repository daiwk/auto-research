from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_transretrieval
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="transretrieval",
    paper=PaperMetadata(
        arxiv_id="2608.25528",
        title="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation",
        url="https://arxiv.org/abs/2608.25528", track="recommendation",
        organization="Renmin University of China / Taobao & Tmall Group, Alibaba",
        published="2026-08-26",
        topics=("retrieval", "transformer-scaling", "target-token-compression", "multi-domain"),
        online_ab=(
            OnlineABEvidence("Alibaba display advertising", "platform revenue", 2.53, "5% traffic; month-long A/B; p<0.0001", source_url="https://arxiv.org/html/2608.25528v1#S4.SS5", source_location="Section 4.5 / Table 7", experiment_duration="one month", significance="p<0.0001", retrieved_at="2026-08-28"),
            OnlineABEvidence("Alibaba display advertising", "RPM", 1.28, "5% traffic; month-long A/B; p<0.0001", source_url="https://arxiv.org/html/2608.25528v1#S4.SS5", source_location="Section 4.5 / Table 7", experiment_duration="one month", significance="p<0.0001", retrieved_at="2026-08-28"),
        ),
    ),
    run=reproduce_transretrieval, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("40B industrial interactions", "52M-item advertisement corpus", "production ANN serving"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens-1M",),
    baseline="same-feature Transformer-style two-tower mean aggregation",
    metrics=("Hit@10", "NDCG@10", "head share@10", "token norm dispersion"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
