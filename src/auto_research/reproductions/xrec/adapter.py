
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_xrec
from .report import render


ADAPTER = register(adapter_from_spec(key="xrec", run=reproduce_xrec, render=render))
