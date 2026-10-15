from auto_research.paper_specs.runtime import adapter_from_spec
from auto_research.reproductions.registry import register

from .experiment import render, reproduce


ADAPTER = register(adapter_from_spec(key="pn-mix", run=reproduce, render=render))
