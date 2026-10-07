
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_pin_scale


ADAPTER = register(adapter_from_spec(key="pin-scale", run=reproduce_pin_scale, render=render_standard))
