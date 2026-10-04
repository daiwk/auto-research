"""Historical, frozen TabPFN distance estimation for T2SPO (Sec. 4.1–4.2)."""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np


@dataclass
class TrajectoryMemory:
    capacity: int = 4096
    _features: list = field(default_factory=list, init=False, repr=False)
    _targets: list = field(default_factory=list, init=False, repr=False)
    version: int = field(default=0, init=False)

    def __post_init__(self):
        if self.capacity < 2:
            raise ValueError("capacity must be at least two")

    def add_completed(self, states: np.ndarray, *, successful: bool) -> None:
        """Call only after the entire current batch is scored; no failed labels."""
        values = np.asarray(states, dtype=float)
        if values.ndim != 2 or not len(values) or not np.isfinite(values).all():
            raise ValueError("states must be a finite [turn, feature] matrix")
        if self._features and values.shape[1] != len(self._features[0]):
            raise ValueError("state feature dimensions changed")
        if successful:
            self._features.extend(values.copy())
            self._targets.extend(range(len(values), 0, -1))
            self._features = self._features[-self.capacity :]
            self._targets = self._targets[-self.capacity :]
            self.version += 1

    def snapshot(self) -> tuple[np.ndarray, np.ndarray, int]:
        return (
            np.array(self._features, copy=True),
            np.array(self._targets, dtype=float),
            self.version,
        )


class FrozenDistanceEstimator:
    """Real TabPFN + support-only standardization/SVD; defaults to CPU.

    No surrogate fallback is permitted. A local official checkpoint is required
    to avoid implicit downloads and to make the revision a caller-owned input.
    Caller computes frozen encoder features from pre-action observations only,
    with step and collection round appended, as in the paper.
    """

    def __init__(self, checkpoint: str, *, dimensions: int = 32, seed: int = 42):
        from pathlib import Path

        if not Path(checkpoint).is_file():
            raise FileNotFoundError("provide a downloaded official TabPFN regressor checkpoint")
        if dimensions < 1:
            raise ValueError("dimensions must be positive")
        from tabpfn import TabPFNRegressor

        self.regressor = TabPFNRegressor(device="cpu", model_path=checkpoint, random_state=seed)
        self.dimensions = dimensions
        self.context_version = None

    def fit_snapshot(self, memory: TrajectoryMemory) -> None:
        features, targets, version = memory.snapshot()
        if len(targets) < 2:
            raise ValueError("insufficient historical support; use outcome signal only")
        self.mean = features.mean(0)
        self.scale = features.std(0)
        self.scale[self.scale < 1e-8] = 1.0
        standardized = (features - self.mean) / self.scale
        _, _, vt = np.linalg.svd(standardized, full_matrices=False)
        self.components = vt[: min(self.dimensions, len(vt))].T
        self.regressor.fit(standardized @ self.components, targets)
        self.context_version = version

    def predict(self, states: np.ndarray, *, maximum: float = 100.0) -> np.ndarray:
        if self.context_version is None:
            raise RuntimeError("fit a historical snapshot before scoring a batch")
        values = np.asarray(states, dtype=float)
        if (
            values.ndim != 2
            or values.shape[1] != len(self.mean)
            or not np.isfinite(values).all()
            or maximum <= 0
        ):
            raise ValueError("invalid query features or maximum distance")
        transformed = ((values - self.mean) / self.scale) @ self.components
        predictions = np.asarray(self.regressor.predict(transformed))
        if not np.isfinite(predictions).all():
            raise ValueError("TabPFN returned non-finite distances")
        return np.clip(predictions, 0, maximum)
