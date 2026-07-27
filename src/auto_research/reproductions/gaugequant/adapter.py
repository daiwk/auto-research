from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_gaugequant


ADAPTER = register(ReproductionAdapter(
    key="gaugequant",
    paper=PaperMetadata(
        arxiv_id="2607.20757",
        title="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries",
        url="https://arxiv.org/abs/2607.20757", track="llm",
        code_url="https://github.com/MPedraBento/gauge-quant",
        organization="University of Cambridge", published="2026-07-22",
        topics=("llm-training", "quantization", "w4a4"),
    ),
    run=reproduce_gaugequant, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("LLaMA-2 7B training", "integer inference kernels"),
))
