
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_onemall


ADAPTER = register(adapter_from_spec(key="onemall", run=reproduce_onemall, render=render_standard))
