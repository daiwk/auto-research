from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce


ADAPTER = register(ReproductionAdapter(
    key="cohortmix-ts",
    paper=PaperMetadata(
        arxiv_id="2609.37800",
        title="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation",
        url="https://arxiv.org/abs/2609.37800",
        track="recommendation",
        code_url="https://github.com/etowho/university-games",
        organization="DFKI / RPTU Kaiserslautern-Landau",
        published="2026-09-29",
        topics=("cold-start", "slate-bandit", "cross-cohort-transfer"),
        online_ab=(OnlineABEvidence(
            "Campus Games quiz",
            "early-to-late correctness change difference (percentage points)",
            6.23,
            "25-day randomized deployment; 356 treatment and 357 control registrants; reported restricted complete-window subgroup",
            source_url="https://arxiv.org/html/2609.37800v1#S6.SS4",
            source_location="Section 6.4",
            experiment_duration="25 days",
            significance="bootstrap 95% CI [0.5, 11.9] pp; p=0.043; post-assignment subgroup caveat",
            retrieved_at="2026-10-01",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("historical matrix factorization", "25-day Campus Games deployment"),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("deterministic public cross-cohort bandit fixture",),
    baseline="uninformative Beta(1,1) Thompson sampling",
    metrics=("prior mean", "selected slate", "posterior update"),
    default_seeds=(42, 43, 44),
    budget="one warm-started slate and posterior update per seed",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
