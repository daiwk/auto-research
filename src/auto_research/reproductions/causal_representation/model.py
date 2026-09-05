from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_causal_representation


def causal_representation_diagnostics(data, history):
    return _diagnostics("causal_representation", data, history)
