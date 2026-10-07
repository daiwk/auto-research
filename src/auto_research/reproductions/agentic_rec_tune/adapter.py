
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_agentic_rec_tune
from .report import render

ADAPTER = register(adapter_from_spec(key="agentic-rec-tune", run=reproduce_agentic_rec_tune, render=render))
