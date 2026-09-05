from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_ssrlive


def ssrlive_diagnostics(data, history):
    return _diagnostics("ssrlive", data, history)
