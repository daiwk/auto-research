from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_rolegen


def rolegen_diagnostics(data, history):
    return _diagnostics("rolegen", data, history)
