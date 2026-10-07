
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rocs
from .report import render


ADAPTER = register(adapter_from_spec(key="rocs", run=reproduce_rocs, render=render))
