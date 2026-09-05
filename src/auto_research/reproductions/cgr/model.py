from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_cgr


def cgr_diagnostics(data, history):
    return _diagnostics("cgr", data, history)
