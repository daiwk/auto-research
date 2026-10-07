
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_dynamic_rubric
from .report import render


ADAPTER = register(adapter_from_spec(key="dynamic-rubric", run=reproduce_dynamic_rubric, render=render))
