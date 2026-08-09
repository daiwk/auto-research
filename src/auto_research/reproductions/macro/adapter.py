from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_macro, render_latest

ADAPTER = register(ReproductionAdapter(
    key="macro", paper=PaperMetadata(arxiv_id="2608.05872", title="MACRO: Markov Chain Routing of Transformer Layers",
        url="https://arxiv.org/abs/2608.05872", track="llm", code_url="https://github.com/Batorskq/MACRO",
        organization="Heinrich Heine University Düsseldorf", published="2026-08-06", topics=("network-architecture", "dynamic-routing", "inference-efficiency")),
    run=reproduce_macro, render=render_latest, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("open-weight LLM checkpoints", "full benchmark route search"),
))
