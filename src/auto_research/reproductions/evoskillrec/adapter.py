from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce


ADAPTER = register(ReproductionAdapter(
    key="evoskillrec",
    paper=PaperMetadata(
        arxiv_id="2609.34552",
        title="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery",
        url="https://arxiv.org/abs/2609.34552",
        track="recommendation",
        code_url="https://github.com/Xiaopengli1/EvoSkill-Rec",
        organization="City University of Hong Kong",
        published="2026-09-28",
        topics=("recommendation-auto-evolution", "architecture-search", "skill-genome"),
        selection_exception=(
            "用户明确批准本轮 P1 学术推荐研究条目；该条目不作为工业线上 A/B 证据样本。"
        ),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "LLM-driven skill invention",
        "paper-scale recommender architecture search",
    ),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("deterministic public mechanism mini-suite",),
    baseline="untransformed feature genome",
    metrics=("validation score", "promotion decision", "reusable genome count"),
    evolve_operators=("rankmixer_evoskill",),
    default_seeds=(42, 43, 44),
    budget="one typed-genome promotion cycle per seed",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
