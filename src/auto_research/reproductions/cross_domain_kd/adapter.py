
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_cross_domain_kd
from .report import render


ADAPTER = register(adapter_from_spec(key="cross-domain-kd", run=reproduce_cross_domain_kd, render=render))
