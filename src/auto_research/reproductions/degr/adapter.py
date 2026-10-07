
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_degr
from .report import render


ADAPTER = register(adapter_from_spec(key="degr", run=reproduce_degr, render=render))
