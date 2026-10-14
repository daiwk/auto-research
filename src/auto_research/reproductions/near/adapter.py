from auto_research.paper_specs.runtime import adapter_from_spec
from ..registry import register
from .experiment import reproduce_near, render

ADAPTER = register(adapter_from_spec(key="near", run=reproduce_near, render=render))
