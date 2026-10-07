
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sessionrec
from .report import render_report


register(adapter_from_spec(key="sessionrec", run=reproduce_sessionrec, render=render_report))
