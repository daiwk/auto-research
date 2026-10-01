from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce


ADAPTER = register(ReproductionAdapter(
    key="recap-ctr",
    paper=PaperMetadata(
        arxiv_id="2609.37905",
        title="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction",
        url="https://arxiv.org/abs/2609.37905",
        track="recommendation",
        organization="Georgia Institute of Technology / Google Research",
        published="2026-09-29",
        topics=("ctr", "estimator-scaling", "recursive-network"),
        selection_exception=(
            "用户明确批准本轮 P1 学术推荐/Evolve 条目；全文没有量化线上 A/B，"
            "因此只作为 L1 核心机制诊断，不进入工业线上证据样本。"
        ),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("paper benchmark training", "independent-model distillation"),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("deterministic public mechanism mini-suite",),
    baseline="single recursive route",
    metrics=("route diversity", "averaged-logit variance", "trajectory EMA"),
    evolve_operators=("rankmixer_recap",),
    default_seeds=(42, 43, 44),
    budget="three weight-shared recursive routes per seed",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
