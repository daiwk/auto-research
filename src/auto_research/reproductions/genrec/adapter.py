
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_genrec

ADAPTER = register(adapter_from_spec(key="genrec", run=reproduce_genrec, render=render_standard))
