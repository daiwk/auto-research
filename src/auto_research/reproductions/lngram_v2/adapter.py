
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce_lngram_v2


ADAPTER=register(adapter_from_spec(key="lngram-v2", run=reproduce_lngram_v2, render=render))
