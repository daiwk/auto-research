
from auto_research.paper_specs.runtime import adapter_from_spec
from .experiment import reproduce
from .report import render
from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register


ADAPTER = register(adapter_from_spec(key="sirf", run=reproduce, render=render))
