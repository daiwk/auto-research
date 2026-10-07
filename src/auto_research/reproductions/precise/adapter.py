
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_precise
from .report import render_report


register(adapter_from_spec(key="precise", run=reproduce_precise, render=render_report))
