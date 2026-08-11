import importlib.util
from pathlib import Path


_SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_gpu_paths.py"
_SPEC = importlib.util.spec_from_file_location("audit_gpu_paths", _SCRIPT)
assert _SPEC and _SPEC.loader
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
_implementation_files = _MODULE._implementation_files


def test_flat_shared_adapter_only_scans_its_source(tmp_path: Path):
    root = tmp_path / "reproductions"
    root.mkdir()
    source = root / "industrial_batch.py"
    sibling = root / "unrelated_gpu.py"
    source.write_text("pass\n")
    sibling.write_text("device_for(torch)\n")
    assert _implementation_files(source) == (source,)


def test_adapter_package_scans_sibling_modules(tmp_path: Path):
    package = tmp_path / "reproductions" / "rankmixer"
    package.mkdir(parents=True)
    source = package / "experiment.py"
    model = package / "model.py"
    source.write_text("pass\n")
    model.write_text("device_for(torch)\n")
    assert set(_implementation_files(source)) == {source, model}
