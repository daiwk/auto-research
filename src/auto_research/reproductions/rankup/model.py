from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_rankup


def rankup_diagnostics(data, history):
    return _diagnostics("rankup", data, history)
