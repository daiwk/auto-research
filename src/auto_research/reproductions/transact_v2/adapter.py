
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_transact_v2
from .report import render


ADAPTER = register(adapter_from_spec(key="transact-v2", run=reproduce_transact_v2, render=render))
