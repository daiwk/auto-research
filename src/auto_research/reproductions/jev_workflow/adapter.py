from auto_research.paper_specs.runtime import adapter_from_spec
from ..registry import register


def reproduce(dataset_dir, seed):
    from auto_research.agent_research.oct12_entrypoint import reproduce_config
    return reproduce_config("jev-workflow", dataset_dir, seed)


def render(result):
    from auto_research.agent_research.oct12_entrypoint import render_result
    return render_result(result)


ADAPTER = register(adapter_from_spec(key="jev-workflow", run=reproduce, render=render))
