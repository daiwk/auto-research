from __future__ import annotations

from .base import ReproductionAdapter
from .protocols import normalize_adapter_protocol

_ADAPTERS: dict[str, ReproductionAdapter] = {}
_DECLARED: dict[str, ReproductionAdapter] = {}


def register(adapter: ReproductionAdapter) -> ReproductionAdapter:
    adapter.paper.validate_catalog_entry()
    from ..paper_specs.runtime import spec_index

    if adapter.key not in spec_index():
        adapter = normalize_adapter_protocol(adapter)
    if adapter.key in _ADAPTERS:
        raise ValueError(f"duplicate reproduction adapter: {adapter.key}")
    _ADAPTERS[adapter.key] = adapter
    return adapter


def list_adapters() -> tuple[ReproductionAdapter, ...]:
    _load_builtins()
    return tuple(
        {**_ADAPTERS, **_DECLARED}[key] for key in sorted(_DECLARED.keys() | _ADAPTERS.keys())
    )


def get_adapter(key: str) -> ReproductionAdapter:
    _load_builtins()
    try:
        return _DECLARED[key] if key in _DECLARED else _ADAPTERS[key]
    except KeyError as exc:
        choices = ", ".join(sorted(_DECLARED.keys() | _ADAPTERS.keys()))
        raise ValueError(f"unknown paper adapter {key!r}; choose from: {choices}") from exc


def _load_builtins() -> None:
    from ..paper_specs.runtime import adapter_from_spec, spec_index

    if not _DECLARED:
        _DECLARED.update((key, adapter_from_spec(key)) for key in spec_index())
