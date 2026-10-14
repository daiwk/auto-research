"""Data contracts and CLI help must not load the optional vision runtime."""
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("entry", ["loader", "help"])
def test_cv_runner_metadata_without_pillow_or_transformers(entry):
    program = r'''
import builtins
import runpy
import sys

original_import = builtins.__import__
def reject_optional(name, *args, **kwargs):
    if name.split(".")[0] in {"PIL", "transformers", "torchvision"}:
        raise ModuleNotFoundError("optional vision runtime deliberately unavailable: " + name)
    return original_import(name, *args, **kwargs)
builtins.__import__ = reject_optional
path, entry = sys.argv[1:]
if entry == "help":
    sys.argv = [path, "--help"]
    try:
        runpy.run_path(path, run_name="__main__")
    except SystemExit as error:
        assert error.code == 0
else:
    namespace = runpy.run_path(path)
    assert callable(namespace["load_rows"])
    assert not any(name.split(".")[0] in {"PIL", "transformers", "torchvision"} for name in sys.modules)
    print("data loader available without optional vision runtime")
'''
    result = subprocess.run(
        [sys.executable, "-c", program, str(ROOT / "scripts/run_cv_opd.py"), entry],
        cwd=ROOT, capture_output=True, text=True, timeout=45,
    )
    assert result.returncode == 0, result.stderr
    assert ("--records" if entry == "help" else "data loader available") in result.stdout
