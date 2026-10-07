from __future__ import annotations
import importlib
import numpy as np
from .method_families.base import BaseAgent
from .method_bindings import AGENT_BINDINGS, _EXPORTS


def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(name)
    module, symbol = _EXPORTS[name]
    return getattr(importlib.import_module(module), symbol)


def build_agent(method: str, capacity: int, rng: np.random.Generator) -> BaseAgent:
    if method not in AGENT_BINDINGS:
        raise ValueError(f"unknown agent method: {method}")
    module, symbol = AGENT_BINDINGS[method]
    return getattr(importlib.import_module(module), symbol)(capacity, rng)
