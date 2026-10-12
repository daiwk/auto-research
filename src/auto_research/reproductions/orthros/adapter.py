from auto_research.paper_specs.runtime import adapter_from_spec
from ..registry import register
from ..oct12_foundation_multimodal import reproduce_orthros, render

ADAPTER = register(adapter_from_spec(key="orthros", run=reproduce_orthros, render=render))
