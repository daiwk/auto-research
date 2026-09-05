from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_zenith


def zenith_diagnostics(data, history):
    return _diagnostics("zenith", data, history)
