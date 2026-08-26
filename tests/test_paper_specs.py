from __future__ import annotations

from pathlib import Path

from auto_research.paper_specs.schema import (
    adapter_directory, load_spec, spec_from_adapter, validate_spec,
)
from auto_research.reproductions.registry import list_adapters


ROOT = Path(__file__).resolve().parents[1]


def _path(adapter) -> Path:
    return adapter_directory(adapter, ROOT) / "paper.yaml"


def test_every_adapter_has_current_declarative_spec():
    adapters = list_adapters()
    assert len(adapters) >= 250
    for adapter in adapters:
        path = _path(adapter)
        assert path.exists(), adapter.key
        spec = load_spec(path)
        assert not validate_spec(spec, root=ROOT, adapter=adapter), adapter.key
        assert spec.to_dict() == spec_from_adapter(adapter, ROOT).to_dict(), adapter.key
