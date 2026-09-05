from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_hpgr


def hpgr_diagnostics(data, history):
    return _diagnostics("hpgr", data, history)
