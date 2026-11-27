"""Frozen bounded diagnostics for a finite overlap/revision selection."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov27-latest"
BATCH = "2026-11-27-overlap-components"
SEEDS = [42, 43, 44]

_spec = importlib.util.spec_from_file_location("_nov27_runner_base", ROOT / "scripts/run_nov18_latest_components.py")
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)
_base.AUDIT, _base.BATCH = AUDIT, BATCH
config, load = _base.config, _base.load


def execution_files():
    return ["scripts/run_nov27_latest_components.py", "scripts/run_nov18_latest_components.py",
            "scripts/oct18_frozen_sources.py", "docs/research-audits/nov27-latest/preflight.json",
            *("src/auto_research/" + row["module"] for row in config()["components"].values())]


def load_component(name):
    relative = name.removeprefix("auto_research.")
    module_path = relative.replace(".", "/") + ".py"
    if not name.startswith("auto_research.") or module_path not in {x["module"] for x in config()["components"].values()}:
        raise ValueError("import outside fixed diagnostic scope")
    namespace = "_nov27_frozen"
    parts = relative.split(".")
    for i in range(len(parts)):
        parent = ".".join([namespace, *parts[:i]])
        if parent not in sys.modules:
            package = ModuleType(parent)
            package.__path__ = [str(ROOT / "src/auto_research" / "/".join(parts[:i]))]
            sys.modules[parent] = package
    qualified = namespace + "." + relative
    if qualified not in sys.modules:
        spec = importlib.util.spec_from_file_location(qualified, ROOT / "src/auto_research" / module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[qualified] = module
        spec.loader.exec_module(module)
    return sys.modules[qualified]


_base.execution_files = execution_files
_base.importlib = SimpleNamespace(import_module=load_component)
_original_validate = _base.validate_raw


def validate_raw(raw, frozen):
    _original_validate(raw, frozen)
    allowed = {str((ROOT / name).resolve()) for name in execution_files()}
    for name, module in tuple(sys.modules.items()):
        if name.startswith("_nov27_frozen.") and getattr(module, "__file__", None):
            if str(Path(module.__file__).resolve()) not in allowed:
                raise ValueError("unbound diagnostic import: " + name)


_base.validate_raw = validate_raw
source_hashes = _base.source_hashes

if __name__ == "__main__":
    _base.main()
