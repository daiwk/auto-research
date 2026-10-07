
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce_pace_vlm


ADAPTER = register(adapter_from_spec(key="pace-vlm", run=reproduce_pace_vlm, render=render))
