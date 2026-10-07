"""Lazy public exports; importing a package does not load optional runtimes."""
import importlib

_EXPORTS = {'PostTrainingConfig': ('auto_research.post_training.models', 'PostTrainingConfig'), 'PostTrainingResult': ('auto_research.post_training.models', 'PostTrainingResult'), 'PostTrainingRunner': ('auto_research.post_training.runner', 'PostTrainingRunner')}
__all__ = list(_EXPORTS)

def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(name)
    module, attribute = _EXPORTS[name]
    value = getattr(importlib.import_module(module), attribute)
    globals()[name] = value
    return value
