from ..historical_p0_h03 import diagnostics as _diagnostics, score_rag_generation

def rag_generation_diagnostics(data, history):
    return _diagnostics("rag_generation", data, history)
