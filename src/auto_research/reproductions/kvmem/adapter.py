
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce


ADAPTER = register(adapter_from_spec(key="kvmem", run=reproduce, render=render))
