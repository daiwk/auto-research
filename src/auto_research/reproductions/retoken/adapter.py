from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_retoken


ADAPTER = register(ReproductionAdapter(
    key="retoken",
    paper=PaperMetadata(
        arxiv_id="2607.28627",
        title="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval",
        url="https://arxiv.org/abs/2607.28627",
        track="llm",
        code_url="https://github.com/avaxiao/ReToken",
        organization="UIUC / Microsoft Research / Google DeepMind",
        published="2026-07-30",
        topics=("vision-language-model", "visual-retrieval", "kv-cache", "sparse-attention"),
    ),
    run=reproduce_retoken,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "frozen billion-parameter VLM",
        "MIRAGE multi-image QA supervision",
        "long-video visual KV cache",
    ),
))
