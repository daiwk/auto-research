from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_sid_coord


def sid_coord_diagnostics(data, history):
    return _diagnostics("sid_coord", data, history)
