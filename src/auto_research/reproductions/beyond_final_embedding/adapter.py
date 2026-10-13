from auto_research.paper_specs.runtime import adapter_from_spec
from ..registry import register
from .experiment import reproduce_beyond, render

ADAPTER = register(adapter_from_spec(key="beyond-final-embedding", run=reproduce_beyond, render=render))
