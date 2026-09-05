from ..historical_p0_h04 import diagnostics as _diagnostics
from ..historical_p0_h04 import score_atomic_intent


def atomic_intent_diagnostics(data, history):
    return _diagnostics("atomic_intent", data, history)
