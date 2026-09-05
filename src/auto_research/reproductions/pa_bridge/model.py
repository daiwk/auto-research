from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_pa_bridge


def pa_bridge_diagnostics(data, history):
    return _diagnostics("pa_bridge", data, history)
