from ..historical_b04_b06 import HistoricalMechanism


class Model(HistoricalMechanism):
    """Paper-owned ml-dcn mechanism."""

    def __init__(self, seed: int = 42):
        super().__init__('ml_dcn', seed)
