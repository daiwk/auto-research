from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_rq_gmm


def rq_gmm_diagnostics(data, history):
    return _diagnostics("rq_gmm", data, history)
