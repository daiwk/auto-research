"""Lazy public exports; importing a package does not load optional runtimes."""
import importlib

_EXPORTS = {'ModelEvolutionEngine': ('auto_research.evolution.engine', 'ModelEvolutionEngine'), 'EvolutionConfig': ('auto_research.evolution.models', 'EvolutionConfig'), 'EvolutionResult': ('auto_research.evolution.models', 'EvolutionResult'), 'EvolutionTrial': ('auto_research.evolution.models', 'EvolutionTrial'), 'Genome': ('auto_research.evolution.models', 'Genome'), 'PaperInspiration': ('auto_research.evolution.models', 'PaperInspiration')}
__all__ = list(_EXPORTS)

def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(name)
    module, attribute = _EXPORTS[name]
    value = getattr(importlib.import_module(module), attribute)
    globals()[name] = value
    return value
