"""Keep the paper mini-card collection current during MkDocs builds and previews."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def on_pre_build(config):
    """Run the shared generator before MkDocs discovers documentation files."""
    module_name = "_auto_research_learning_cards_generator"
    spec = spec_from_file_location(module_name, ROOT / "scripts/generate_learning_cards.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the learning-card generator")
    generator = module_from_spec(spec)
    sys.modules[module_name] = generator
    spec.loader.exec_module(generator)
    generator.generate(ROOT)
