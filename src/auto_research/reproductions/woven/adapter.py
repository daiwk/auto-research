from auto_research.paper_specs.runtime import adapter_from_spec
from ..registry import register
from ..oct12_foundation_multimodal import reproduce_woven, render

ADAPTER = register(adapter_from_spec(key="woven", run=reproduce_woven, render=render))
