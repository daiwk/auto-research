"""Keep the paper mini-card collection current during MkDocs builds and previews."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def _curated_entries(items):
    curated = []
    for item in items:
        for title, value in item.items():
            if isinstance(value, list):
                curated.extend(_curated_entries(value))
            elif isinstance(value, str) and value.startswith("learning/") and not value.startswith(
                "learning/paths/"
            ) and value not in {
                "learning/index.md", "learning/all.md", "learning/topics.md", "learning/inbox.md", "learning/recent.md",
            }:
                curated.append({title: value})
    return curated


def on_config(config):
    """Generate the collection and its folded navigation before file discovery."""
    module_name = "_auto_research_learning_cards_generator"
    spec = spec_from_file_location(module_name, ROOT / "scripts/generate_learning_cards.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the learning-card generator")
    generator = module_from_spec(spec)
    sys.modules[module_name] = generator
    spec.loader.exec_module(generator)
    generator.generate(ROOT, require_questions=True)
    _, themes = generator._collection(ROOT)
    topic_nav = generator._topic_module().navigation(themes)
    for entry in config["nav"]:
        if "学习卡片" not in entry:
            continue
        curated = _curated_entries(entry["学习卡片"])
        entry["学习卡片"] = [
            {"学习入口": "learning/index.md"},
            {"最近新增问题": "learning/recent.md"},
            {"全部论文问答": "learning/all.md"},
            {"按主题找问题": [
                *topic_nav,
                {"专题串读": curated},
            ]},
            {"待归类的新论文": "learning/inbox.md"},
        ]
    return config
