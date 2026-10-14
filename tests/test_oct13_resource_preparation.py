from types import SimpleNamespace
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("oct13_prepare", ROOT / "scripts/prepare_oct13_public_resources.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def item(name, size, sha=None):
    return SimpleNamespace(rfilename=name, size=size,
                           lfs=SimpleNamespace(sha256=sha) if sha else None)


def test_large_resource_requires_official_size_and_lfs_digest():
    info = SimpleNamespace(siblings=[item("weights.pt", 20_000_000)])
    with pytest.raises(ValueError, match="upstream SHA256"):
        module.selected_files(info, ["weights.pt"])
    info.siblings = [item("weights.pt", None)]
    with pytest.raises(ValueError, match="byte sizes"):
        module.selected_files(info, ["weights.pt"])


def test_preparer_never_silently_omits_requested_source_files():
    info = SimpleNamespace(siblings=[item("config.json", 10)])
    with pytest.raises(ValueError, match="misses requested"):
        module.selected_files(info, ["config.json", "weights.pt"])


def test_only_fixed_pins_and_bounded_explicit_file_lists():
    for resource in module.RESOURCES.values():
        assert len(resource["revision"]) == 40
        assert resource["files"]
        assert not any("*" in name or ".." in name or name.startswith("/") for name in resource["files"])
    assert module.RESOURCES["qwen-base"]["public_id"] == "Qwen/Qwen2.5-0.5B"
    assert module.RESOURCES["lewam-toolhang-data"]["files"] == ["toolhang.h5"]
