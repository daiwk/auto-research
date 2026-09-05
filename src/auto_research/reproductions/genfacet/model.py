from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_genfacet


def genfacet_diagnostics(data, history):
    return _diagnostics("genfacet", data, history)
