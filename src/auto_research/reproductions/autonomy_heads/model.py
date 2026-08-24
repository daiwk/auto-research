from ..historical_b07 import _method


PAPER_KEY = 'autonomy-heads'


def apply(suite, seed=42):
    return _method(PAPER_KEY, suite, seed)
