
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rd_attnres
from .report import render


ADAPTER = register(adapter_from_spec(key="rd-attnres", run=reproduce_rd_attnres, render=render))
