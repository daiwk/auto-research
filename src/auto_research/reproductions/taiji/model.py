from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_taiji


def taiji_diagnostics(data, history):
    return _diagnostics("taiji", data, history)
