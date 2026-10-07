
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import (
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_fuxi_alpha
from .report import render

ADAPTER = register(
    adapter_from_spec(key="fuxi-alpha", run=reproduce_fuxi_alpha, render=render)
)
