"""Deprecated compatibility imports.

New paper implementations live under :mod:`auto_research.reproductions`, one
package per paper. This module remains so existing integrations do not break.
"""

from pathlib import Path
from typing import Any

from .reproductions.mdcns.experiment import ranking_metrics as _ranking_metrics
from .reproductions.mdcns.experiment import reproduce_mdcns
from .reproductions.mdcns.model import SequentialModel
from .reproductions.registry import list_adapters
from .reproductions.reporting import write_legacy_combined_report
from .reproductions.sis.algorithm import sis_topk_weight
from .reproductions.sis.experiment import reproduce_sis

SIS_PAPER = next(
    adapter.paper.to_dict() for adapter in list_adapters() if adapter.key == "sis"
)
MDCNS_PAPER = next(
    adapter.paper.to_dict() for adapter in list_adapters() if adapter.key == "mdcns"
)


def write_reproduction_report(results: list[dict[str, Any]], output: Path) -> None:
    """Compatibility wrapper for the pre-registry combined report API."""
    by_id = {adapter.paper.arxiv_id: adapter for adapter in list_adapters()}
    entries = [(by_id[result["paper"]["arxiv_id"]], result) for result in results]
    write_legacy_combined_report(entries, output)


__all__ = [
    "SequentialModel",
    "MDCNS_PAPER",
    "SIS_PAPER",
    "_ranking_metrics",
    "reproduce_mdcns",
    "reproduce_sis",
    "sis_topk_weight",
    "write_reproduction_report",
]
