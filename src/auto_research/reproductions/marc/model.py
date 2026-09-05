from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_marc


def marc_diagnostics(data, history):
    return _diagnostics("marc", data, history)
