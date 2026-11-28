"""CPU-only frozen-source Habitats statistics, not policy/LLM training."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov28-latest"
BATCH = "2026-11-28-priority-source-followup"
SEEDS = [42, 43, 44]

_spec = importlib.util.spec_from_file_location("_nov28_runner_base", ROOT / "scripts/run_nov18_latest_components.py")
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)
_base.AUDIT, _base.BATCH, _base.__doc__ = AUDIT, BATCH, __doc__
config, load = _base.config, _base.load


def execution_files():
    return ["scripts/run_nov28_habitats_component.py", "scripts/run_nov18_latest_components.py",
            "scripts/oct18_frozen_sources.py", "docs/research-audits/nov28-latest/preflight.json",
            "src/auto_research/agent_research/habitats.py"]


def load_component(name):
    if name != "auto_research.agent_research.habitats":
        raise ValueError("import outside single accepted component")
    for part, location in (("_nov28_frozen", ROOT / "src/auto_research"),
                           ("_nov28_frozen.agent_research", ROOT / "src/auto_research/agent_research")):
        if part not in sys.modules:
            module = ModuleType(part)
            module.__path__ = [str(location)]
            sys.modules[part] = module
    qualified = "_nov28_frozen.agent_research.habitats"
    if qualified not in sys.modules:
        spec = importlib.util.spec_from_file_location(qualified, ROOT / "src/auto_research/agent_research/habitats.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[qualified] = module
        spec.loader.exec_module(module)
    return sys.modules[qualified]


_base.execution_files = execution_files
_base.importlib = SimpleNamespace(import_module=load_component)
_original_validate = _base.validate_raw


def validate_raw(raw, frozen):
    if raw.get("device") != "cpu":
        raise ValueError("No CUDA component was accepted for this intake")
    _original_validate(raw, frozen)


_base.validate_raw = validate_raw
source_hashes = _base.source_hashes

if __name__ == "__main__":
    # Reject before importing torch or initializing an accelerator.
    if "--device=cuda" in sys.argv or any(a == "--device" and b == "cuda" for a, b in zip(sys.argv, sys.argv[1:])):
        raise SystemExit("CPU-only intake: no CUDA implementation or run is claimed")
    _base.main()
