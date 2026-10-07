from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sis
from .report import render

ADAPTER = register(
    adapter_from_spec(key="sis", run=reproduce_sis, render=render)
)
