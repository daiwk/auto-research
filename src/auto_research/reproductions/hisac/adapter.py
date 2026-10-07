
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_hisac


ADAPTER = register(adapter_from_spec(key="hisac", run=reproduce_hisac, render=render_standard))
