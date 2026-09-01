from ..historical_p0_h03 import diagnostics as _diagnostics, score_zorro

def zorro_diagnostics(data, history):
    return _diagnostics("zorro", data, history)
