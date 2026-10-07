
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_rankgraph2

ADAPTER = register(adapter_from_spec(key="rankgraph2", run=reproduce_rankgraph2, render=render_standard))
