from ..historical_p0_h06_h07 import diagnostics as _diagnostics
from ..historical_p0_h06_h07 import score_mlcc


def mlcc_diagnostics(data, history):
    return _diagnostics("mlcc", data, history)
