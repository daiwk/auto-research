
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier,OnlineABEvidence,PaperMetadata,ReproductionAdapter,ReproductionFidelity
from ..registry import register
from .experiment import render,reproduce_recevolve


ADAPTER=register(adapter_from_spec(key="recevolve", run=reproduce_recevolve, render=render))
