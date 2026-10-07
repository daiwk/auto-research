
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_ppl_factory
from .report import render


ADAPTER = register(adapter_from_spec(key="ppl-factory", run=reproduce_ppl_factory, render=render))
