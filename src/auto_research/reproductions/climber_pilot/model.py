from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_climber_pilot


def climber_pilot_diagnostics(data, history):
    return _diagnostics("climber_pilot", data, history)
