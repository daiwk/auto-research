
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_gaugequant


ADAPTER = register(adapter_from_spec(key="gaugequant", run=reproduce_gaugequant, render=render))
