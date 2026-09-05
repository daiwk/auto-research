from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_promise


def promise_diagnostics(data, history):
    return _diagnostics("promise", data, history)
