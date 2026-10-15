from auto_research.paper_specs.runtime import adapter_from_spec

from ..registry import register
from .experiment import render, reproduce

ADAPTER = register(adapter_from_spec(key="smrc-pmrc", run=reproduce, render=render))
