
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce_random_attention


ADAPTER = register(adapter_from_spec(key="random-attention", run=reproduce_random_attention, render=render))
