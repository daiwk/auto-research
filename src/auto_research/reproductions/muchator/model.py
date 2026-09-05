from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_muchator


def muchator_diagnostics(data, history):
    return _diagnostics("muchator", data, history)
