
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_ramp
from .report import render


ADAPTER = register(adapter_from_spec(key="ramp", run=reproduce_ramp, render=render))
