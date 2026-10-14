from auto_research.paper_specs.runtime import adapter_from_spec
from ..registry import register
from .experiment import reproduce_lewam, render

ADAPTER = register(adapter_from_spec(key="lewam", run=reproduce_lewam, render=render))
