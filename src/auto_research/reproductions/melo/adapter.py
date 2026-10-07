
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from auto_research.reproductions.mechanisms.reproduce_reco_reward import reproduce_melo
from ..registry import register


ADAPTER = register(adapter_from_spec(key="melo", run=reproduce_melo, render=render_standard))
