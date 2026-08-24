from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rare
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="rare",
    paper=PaperMetadata(
        arxiv_id="2608.21236", title="RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models",
        url="https://arxiv.org/abs/2608.21236", track="llm",
        organization="Huazhong University of Science and Technology", published="2026-08-21",
        topics=("llm-architecture", "mixture-of-experts", "representation-steering", "model-editing"),
    ),
    run=reproduce_rare, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("large pretrained MoE checkpoints", "TruthfulQA and CounterFact full evaluation"),
    evaluation_tier=EvaluationTier.MECHANISM, datasets=("deterministic MoE routing mini-suite",),
    baseline="unprojected representation steering", metrics=("route agreement", "route flip rate", "steering gain"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
