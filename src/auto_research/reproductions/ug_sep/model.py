from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_ug_sep


def ug_sep_diagnostics(data, history):
    return _diagnostics("ug_sep", data, history)
