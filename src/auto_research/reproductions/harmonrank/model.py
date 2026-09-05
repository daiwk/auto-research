from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_harmonrank


def harmonrank_diagnostics(data, history):
    return _diagnostics("harmonrank", data, history)
