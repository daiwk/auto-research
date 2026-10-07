
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_data_orchestra
from .report import render


ADAPTER = register(
    adapter_from_spec(key="data-orchestra", run=reproduce_data_orchestra, render=render)
)
