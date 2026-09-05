from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_toolrec


def toolrec_diagnostics(data, history):
    return _diagnostics("toolrec", data, history)
