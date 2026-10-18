"""Bounded provider-code patch transactions inspired by MemScope.

Only syntax/interface/locality and trusted caller probes are checked. This is
not an OS sandbox, a learned Patch Agent, or proof of memory/QA correctness.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import dataclass, replace
from difflib import SequenceMatcher


@dataclass(frozen=True)
class Provider:
    provider_id: str
    schema_version: str
    code: str


@dataclass(frozen=True)
class PatchResult:
    provider: Provider
    memory: object
    accepted: bool
    failure_stage: str | None
    change_ratio: float


def _interface(code):
    tree = ast.parse(code)
    return {node.name: ast.dump(node.args) for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")}


def patch_provider(provider: Provider, memory, *, old: str, new: str, probe,
                   max_change_ratio=.25) -> PatchResult:
    """Preserve provider identity, public signatures, and the existing memory.

The probe receives deep copies, so failed compatibility checks cannot mutate
the live memory. Exceptions retain their stage, not private exception content.
"""
    original_memory = deepcopy(memory)
    ratio = 0.
    stage = "localized_edit"
    try:
        if not provider.provider_id or not provider.schema_version or not 0 < max_change_ratio <= 1:
            raise ValueError("identified provider and bounded change budget required")
        if not old or old == new or provider.code.count(old) != 1:
            raise ValueError("one exact nonempty old-to-new replacement required")
        code = provider.code.replace(old, new, 1)
        ratio = 1 - SequenceMatcher(None, provider.code, code, autojunk=False).ratio()
        if ratio > max_change_ratio:
            raise ValueError("edit exceeds locality budget")
        stage = "syntax_interface"
        original_interface = _interface(provider.code)
        if not original_interface or _interface(code) != original_interface:
            raise ValueError("public provider interface must remain unchanged")
        candidate = replace(provider, code=code)
        stage = "compatibility_probe"
        if probe(deepcopy(candidate), deepcopy(original_memory)) is not True:
            raise ValueError("candidate compatibility check failed")
        return PatchResult(candidate, deepcopy(original_memory), True, None, ratio)
    except Exception:
        return PatchResult(provider, deepcopy(original_memory), False, stage, ratio)
