from ..historical_p0_h03 import diagnostics as _diagnostics, score_egr

def egr_diagnostics(data, history):
    return _diagnostics("egr", data, history)
