
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_harness_lm
from .report import render

ADAPTER = register(adapter_from_spec(key="harness-lm", run=reproduce_harness_lm, render=render))
