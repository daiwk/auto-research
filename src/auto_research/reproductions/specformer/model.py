from ..historical_p0_h03 import diagnostics as _diagnostics, score_specformer

def specformer_diagnostics(data, history):
    return _diagnostics("specformer", data, history)
