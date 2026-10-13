from auto_research.paper_specs.runtime import adapter_from_spec
from ..registry import register
from .experiment import reproduce_skilldreamer, render

ADAPTER = register(adapter_from_spec(key="skilldreamer", run=reproduce_skilldreamer, render=render))
