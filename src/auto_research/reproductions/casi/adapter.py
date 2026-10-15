"""Lazy binding of the CPU-only CASI component audit."""
from auto_research.paper_specs.runtime import adapter_from_spec


def reproduce(dataset_dir, seed):
    from .experiment import run
    return run(dataset_dir, seed)


def render(result):
    from .experiment import render as render_result
    return render_result(result)


ADAPTER = adapter_from_spec("casi", run=reproduce, render=render)
