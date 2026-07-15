import json
from pathlib import Path

import numpy as np
import pytest

from auto_research.reproductions.prompt_generation.protocol import PromptCompiler, PromptConfig
from auto_research.reproductions.registry import get_adapter


def test_adapter_has_quantified_production_ab():
    adapter = get_adapter("prompt-generation")
    assert adapter.paper.organization == "Alibaba / Taobao Search"
    assert {entry.lift_percent for entry in adapter.paper.online_ab} >= {0.47, 0.51, 4.01}


def test_protocol_rejects_training_serving_schema_skew(tmp_path: Path):
    template = tmp_path / "template.json"
    features = tmp_path / "features.json"
    template.write_text(json.dumps({"template": "{{history}} {{missing}}"}))
    features.write_text(json.dumps({"features": [{"feature_name": "history", "feature_type": "text"}]}))
    with pytest.raises(ValueError, match="mismatch"):
        PromptConfig.load(template, features)


def test_four_feature_types_and_mean_merger_compile():
    config = PromptConfig(
        template="prefix {{mixed}} suffix",
        features=(
            {
                "feature_name": "mixed",
                "feature_type": "sequence",
                "expression": "titles",
                "max_length": 2,
                "features": [
                    {"feature_name": "text", "feature_type": "text", "expression": "titles"},
                    {
                        "feature_name": "combo",
                        "feature_type": "combo",
                        "merger": {"type": "mean"},
                        "features": [
                            {"feature_name": "brand", "feature_type": "text", "expression": "brands"},
                            {"feature_name": "vector", "feature_type": "embedding", "expression": "vectors"},
                        ],
                    },
                ],
            },
        ),
    )
    config.validate()
    compiler = PromptCompiler(config)

    def encode_text(value):
        return np.full((1, 2), len(value), dtype=float)

    def encode_embedding(value):
        return np.asarray(value, dtype=float).reshape(1, 2)

    def merge(values, _):
        return np.concatenate(values).mean(0, keepdims=True)

    segments = compiler.compile(
        {"titles": ["old", "new"], "brands": ["a", "bb"], "vectors": [[1, 2], [3, 4]]},
        encode_text,
        encode_embedding,
        merge,
    )
    assert sum(segment.shape[0] for segment in segments) == 6


def test_repository_configs_are_valid():
    root = Path(__file__).parents[2] / "src/auto_research/reproductions/prompt_generation/configs"
    for feature_file in ("sid_only.json", "title.json", "title_brand_merged.json"):
        PromptConfig.load(root / "prompt_template.json", root / feature_file)
