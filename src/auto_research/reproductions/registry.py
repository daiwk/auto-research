from __future__ import annotations

import importlib
from pathlib import Path

from .base import ReproductionAdapter

_ADAPTERS: dict[str, ReproductionAdapter] = {}
_ROOT = Path(__file__).parent


def register(adapter: ReproductionAdapter) -> ReproductionAdapter:
    adapter.paper.validate_catalog_entry()
    if adapter.key in _ADAPTERS:
        raise ValueError(f"duplicate reproduction adapter: {adapter.key}")
    _ADAPTERS[adapter.key] = adapter
    return adapter


def list_adapters() -> tuple[ReproductionAdapter, ...]:
    _load_builtins()
    return tuple(_ADAPTERS[key] for key in sorted(_ADAPTERS))


def get_adapter(key: str) -> ReproductionAdapter:
    _load_builtins()
    try:
        return _ADAPTERS[key]
    except KeyError as exc:
        choices = ", ".join(sorted(_ADAPTERS))
        raise ValueError(f"unknown paper adapter {key!r}; choose from: {choices}") from exc


def _load_builtins() -> None:
    for package in sorted(_ROOT.iterdir()):
        if package.is_dir() and (package / "adapter.py").exists():
            importlib.import_module(
                f"auto_research.reproductions.{package.name}.adapter"
            )
