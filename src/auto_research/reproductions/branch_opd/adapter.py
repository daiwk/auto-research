from auto_research.paper_specs.runtime import adapter_from_spec
from ..registry import register


def reproduce(dataset_dir, seed=42):
    from auto_research.post_training.oct12_checkpoint import run_adapter
    return run_adapter("branch-opd", dataset_dir, seed)


def render(result):
    from auto_research.post_training.oct12_checkpoint import render as render_checkpoint
    return render_checkpoint(result)


ADAPTER = register(adapter_from_spec(key="branch-opd", run=reproduce, render=render))
