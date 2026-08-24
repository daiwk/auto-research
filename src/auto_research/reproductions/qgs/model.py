from ..historical_b01_b03 import HistoricalMechanism


class Model(HistoricalMechanism):
    """Paper-owned qgs mechanism."""

    def __init__(self, seed: int = 42):
        super().__init__('qgs', seed)
