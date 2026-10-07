
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from auto_research.reproductions.mechanisms.reproduce_kgd import reproduce_twitch_mor
from auto_research.reproductions.mechanisms.generative_slate_report import render_latest

ADAPTER = register(adapter_from_spec(key="twitch-mor", run=reproduce_twitch_mor, render=render_latest))
