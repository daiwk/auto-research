"""Declarative grpo-difficulty-curriculum binding; no tensor/model import on catalog discovery."""
from auto_research.paper_specs.runtime import adapter_from_spec
from auto_research.reproductions.registry import register


def run(dataset_dir, seed):
    from auto_research.post_training.oct13_common import adapter_run
    return adapter_run("grpo-difficulty-curriculum", dataset_dir, seed)


def render(result):
    from auto_research.post_training.oct13_common import render_result
    return render_result(result)


ADAPTER = register(adapter_from_spec(key="grpo-difficulty-curriculum", run=run, render=render))
