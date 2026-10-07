
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_self_evolving_rec
from .report import render

ADAPTER = register(
    adapter_from_spec(key="self-evolving-rec", run=reproduce_self_evolving_rec, render=render)
)
