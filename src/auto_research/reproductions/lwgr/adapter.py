
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_lwgr
from .report import render


ADAPTER = register(
    adapter_from_spec(key="lwgr", run=reproduce_lwgr, render=render)
)
