
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_looped_latent_attention


ADAPTER = register(adapter_from_spec(key="looped-latent-attention", run=reproduce_looped_latent_attention, render=render))
