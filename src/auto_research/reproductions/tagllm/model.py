from ..historical_p0_h05 import diagnostics as _diagnostics
from ..historical_p0_h05 import score_tagllm


def tagllm_diagnostics(data, history):
    return _diagnostics("tagllm", data, history)
