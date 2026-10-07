
from auto_research.paper_specs.runtime import adapter_from_spec
from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_semantic_native_longseq
from .report import render


ADAPTER = register(
    adapter_from_spec(key="semantic-native-longseq", run=reproduce_semantic_native_longseq, render=render)
)
