from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_unimvt


def unimvt_diagnostics(data, history):
    return _diagnostics("unimvt", data, history)
