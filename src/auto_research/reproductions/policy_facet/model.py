from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_policy_facet


def policy_facet_diagnostics(data, history):
    return _diagnostics("policy_facet", data, history)
