
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_friend_gnn
from .report import render


ADAPTER = register(adapter_from_spec(key="friend-gnn", run=reproduce_friend_gnn, render=render))
