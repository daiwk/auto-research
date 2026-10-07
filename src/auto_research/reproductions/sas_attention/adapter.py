
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sas_attention
from .report import render


ADAPTER = register(adapter_from_spec(key="sas-attention", run=reproduce_sas_attention, render=render))
