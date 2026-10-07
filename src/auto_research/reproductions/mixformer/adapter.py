
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mixformer
from .report import render

ADAPTER = register(
    adapter_from_spec(key="mixformer", run=reproduce_mixformer, render=render)
)
