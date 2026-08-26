"""Cross-domain experiment registry and static dashboard."""

from .store import ExperimentStore, sync_experiments

__all__ = ["ExperimentStore", "sync_experiments"]
