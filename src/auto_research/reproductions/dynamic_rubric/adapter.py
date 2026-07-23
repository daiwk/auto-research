from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_dynamic_rubric
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="dynamic-rubric",
    paper=PaperMetadata(
        arxiv_id="2607.20083",
        title="Co-Evolving LLM Evaluators and Policies via DynamicRubric",
        url="https://arxiv.org/abs/2607.20083",
        track="llm",
        organization="WeChat / Tencent and Tsinghua University",
        published="2026-07-22",
        topics=("post-training", "reward-model", "evaluator", "co-evolution"),
        selection_exception="The paper reports statistically significant online A/B gains and a full-traffic WeChat Search deployment, but withholds exact lifts.",
    ),
    run=reproduce_dynamic_rubric,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Qwen3-8B policy and evaluator", "70B/235B production judges and private WeChat traffic"),
))
