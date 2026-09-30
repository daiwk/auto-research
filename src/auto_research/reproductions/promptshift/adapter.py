from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce


ADAPTER = register(ReproductionAdapter(
    key="promptshift",
    paper=PaperMetadata(
        arxiv_id="2609.34229",
        title=(
            "Measuring and Mitigating Identity-Cue Preference Drift in "
            "LLM-based Recommender Systems"
        ),
        url="https://arxiv.org/abs/2609.34229",
        track="recommendation",
        organization="University of Electronic Science and Technology of China",
        published="2026-09-28",
        topics=("llm-recommendation", "identity-cue-drift", "fairness"),
        selection_exception=(
            "用户明确批准本轮 P1 学术推荐研究条目；该条目不作为工业线上 A/B 证据样本。"
        ),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("proprietary LLM recommendations", "real identity slices"),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("deterministic public identity-slice fixture",),
    baseline="identity-cued ranking without adaptive mitigation",
    metrics=("drift", "slice shift", "difficulty at k"),
    default_seeds=(42, 43, 44),
    budget="one ten-item diagnostic ranking per seed",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
