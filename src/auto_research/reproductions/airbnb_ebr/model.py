from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_airbnb_ebr


def airbnb_ebr_diagnostics(data, history):
    return _diagnostics("airbnb_ebr", data, history)
