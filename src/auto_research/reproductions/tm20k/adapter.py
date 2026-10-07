
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tm20k
from .report import render


ADAPTER = register(
    adapter_from_spec(key="tm20k", run=reproduce_tm20k, render=render)
)
