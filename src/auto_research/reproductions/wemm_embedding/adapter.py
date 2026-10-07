
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_wemm_embedding
from .report import render


ADAPTER = register(adapter_from_spec(key="wemm-embedding", run=reproduce_wemm_embedding, render=render))
