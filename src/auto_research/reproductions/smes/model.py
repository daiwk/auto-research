from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_smes


def smes_diagnostics(data, history):
    return _diagnostics("smes", data, history)
