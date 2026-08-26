"""Declarative paper specifications used by adapters, docs and CI."""

from .schema import PaperSpec, load_spec, spec_from_adapter, validate_spec

__all__ = ["PaperSpec", "load_spec", "spec_from_adapter", "validate_spec"]
