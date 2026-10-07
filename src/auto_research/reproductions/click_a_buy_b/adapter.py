
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import (
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_click_a_buy_b
from .report import render

ADAPTER = register(
    adapter_from_spec(key="click-a-buy-b", run=reproduce_click_a_buy_b, render=render)
)
