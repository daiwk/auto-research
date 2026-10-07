"""Lazy public exports; importing a package does not load optional runtimes."""
import importlib

_EXPORTS = {'AgentResearchConfig': ('auto_research.agent_research.models', 'AgentResearchConfig'), 'AgentResearchResult': ('auto_research.agent_research.models', 'AgentResearchResult'), 'AgentResearchRunner': ('auto_research.agent_research.runner', 'AgentResearchRunner'), 'run_executor_matrix': ('auto_research.agent_research.executor_matrix', 'run_executor_matrix'), 'LightningPolicyConfig': ('auto_research.agent_research.lightning_policy', 'LightningPolicyConfig'), 'run_lightning_policy_training': ('auto_research.agent_research.lightning_policy', 'run_lightning_policy_training'), 'CapabilitySuiteConfig': ('auto_research.agent_research.capability_runner', 'CapabilitySuiteConfig'), 'run_capability_suite': ('auto_research.agent_research.capability_runner', 'run_capability_suite')}
__all__ = list(_EXPORTS)

def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(name)
    module, attribute = _EXPORTS[name]
    value = getattr(importlib.import_module(module), attribute)
    globals()[name] = value
    return value
