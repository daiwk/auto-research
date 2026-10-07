
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tiger
from .report import render


ADAPTER = register(adapter_from_spec(key="tiger", run=reproduce_tiger, render=render))
