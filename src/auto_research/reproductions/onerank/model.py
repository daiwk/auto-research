from ..historical_p0_h03 import diagnostics as _diagnostics, score_onerank

def onerank_diagnostics(data, history):
    return _diagnostics("onerank", data, history)
