from ..base import (
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_genrec_netflix
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="genrec-netflix",
        paper=PaperMetadata(
            arxiv_id="2608.10257",
            title="GenRec: An LLM-Backed Recommendation Ranker at Netflix",
            url="https://arxiv.org/abs/2608.10257",
            track="recommendation",
            organization="Netflix",
            published="2026-08-10",
            topics=(
                "ranking",
                "llm-recommendation",
                "post-training",
                "reward-weighting",
                "context-engineering",
                "training-serving",
            ),
            online_ab=(
                OnlineABEvidence(
                    "Netflix batch-compute recommendation surfaces",
                    "short-term homepage engagement",
                    0.115,
                    "approximately 10% traffic",
                    source_url="https://arxiv.org/html/2608.10257v1#S5.SS1",
                    source_location="Section 5.1 / Figure 3",
                    experiment_duration="4 weeks",
                    significance="P = 3.1e-10",
                    retrieved_at="2026-08-13",
                ),
                OnlineABEvidence(
                    "Netflix batch-compute recommendation surfaces",
                    "long-term core metric",
                    0.006,
                    "approximately 10% traffic",
                    source_url="https://arxiv.org/html/2608.10257v1#S5.SS1",
                    source_location="Section 5.1 / Figure 3",
                    experiment_duration="4 weeks",
                    significance="P = 0.025",
                    retrieved_at="2026-08-13",
                ),
            ),
        ),
        run=reproduce_genrec_netflix,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Netflix proprietary Phase-1 foundation model and hundreds of billions of events",
            "private long-term satisfaction reward models",
            "production vLLM serving and batch-compute traffic",
        ),
        datasets=("MovieLens-1M",),
        baseline="ID-only discriminative GRU ranker with matched Phase-2 examples",
        metrics=("Hit@10", "NDCG@10", "MRR", "head share@10"),
        device_capabilities=("cpu", "mps", "cuda"),
    )
)
