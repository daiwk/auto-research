"""Paper-specific, independently extensible reproduction adapters."""

from .base import PaperMetadata, ReproductionAdapter
from .registry import get_adapter, list_adapters
from .reporting import write_reproduction_result

__all__ = [
    "PaperMetadata",
    "ReproductionAdapter",
    "get_adapter",
    "list_adapters",
    "write_reproduction_result",
]
