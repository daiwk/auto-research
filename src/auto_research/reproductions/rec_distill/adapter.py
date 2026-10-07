
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rec_distill
from .report import render


ADAPTER = register(
    adapter_from_spec(key="rec-distill", run=reproduce_rec_distill, render=render)
)
