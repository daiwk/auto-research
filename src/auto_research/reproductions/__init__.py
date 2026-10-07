"""Lazy public exports; importing a package does not load optional runtimes."""
import importlib

_EXPORTS = {'PaperMetadata': ('auto_research.reproductions.base', 'PaperMetadata'), 'ReproductionAdapter': ('auto_research.reproductions.base', 'ReproductionAdapter'), 'get_adapter': ('auto_research.reproductions.registry', 'get_adapter'), 'list_adapters': ('auto_research.reproductions.registry', 'list_adapters'), 'write_reproduction_result': ('auto_research.reproductions.reporting', 'write_reproduction_result')}
__all__ = list(_EXPORTS)

def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(name)
    module, attribute = _EXPORTS[name]
    value = getattr(importlib.import_module(module), attribute)
    globals()[name] = value
    return value
