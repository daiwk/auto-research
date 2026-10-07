
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_lum
from .report import render_report


register(adapter_from_spec(key="lum", run=reproduce_lum, render=render_report))
