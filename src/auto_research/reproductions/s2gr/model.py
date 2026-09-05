from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_s2gr


def s2gr_diagnostics(data, history):
    return _diagnostics("s2gr", data, history)
