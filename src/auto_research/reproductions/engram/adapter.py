
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_engram


ADAPTER = register(adapter_from_spec(key="engram", run=reproduce_engram, render=render))
