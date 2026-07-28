from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_data_orchestra
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="data-orchestra",
        paper=PaperMetadata(
            arxiv_id="2607.24717",
            title="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data",
            url="https://arxiv.org/abs/2607.24717",
            track="llm",
            code_url="https://github.com/GAIR-NLP/DataOrchestra",
            organization="Fudan University / Shanghai Jiao Tong University / SII-GAIR",
            published="2026-07-27",
            topics=(
                "llm-pretraining",
                "data-curation",
                "data-cleaning",
                "learned-orchestration",
            ),
        ),
        run=reproduce_data_orchestra,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "LLM-generated orchestration supervision",
            "20B/30B-token multi-corpus pretraining",
            "0.5B/1.5B/7B model scaling",
        ),
    )
)
