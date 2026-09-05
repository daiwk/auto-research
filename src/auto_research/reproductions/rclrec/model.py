from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_rclrec


def rclrec_diagnostics(data, history):
    return _diagnostics("rclrec", data, history)
