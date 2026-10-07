
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_univa
from .report import render


ADAPTER = register(
    adapter_from_spec(key="univa", run=reproduce_univa, render=render)
)
