from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_primal_dual_decoding


def primal_dual_decoding_diagnostics(data, history):
    return _diagnostics("primal_dual_decoding", data, history)
