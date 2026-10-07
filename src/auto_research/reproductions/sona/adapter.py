
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from auto_research.reproductions.mechanisms.metastrategy_family import reproduce_sona
from auto_research.reproductions.mechanisms.strategy_semantic_report import render_latest


ADAPTER = register(adapter_from_spec(key="sona", run=reproduce_sona, render=render_latest))
