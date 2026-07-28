from pathlib import Path

import numpy as np

from auto_research.reproductions.classic_multitask import (
    MultiTaskConfig,
    build_multitask_model,
)
from auto_research.reproductions.foundational_ranking import (
    FoundationalConfig,
    build_foundational_model,
)
from auto_research.reproductions.registry import get_adapter


def test_named_classic_exceptions_keep_complete_metadata():
    expected = {
        "deepfm": ("Huawei Noah's Ark Lab", "2017-03-13"),
        "youtube-dnn": ("Google / YouTube", "2016-09-15"),
        "esmm": ("Alibaba", "2018-04-21"),
        "mmoe": ("Google", "2018-08-19"),
        "ple": ("Tencent", "2020-09-22"),
    }
    for key, (organization, published) in expected.items():
        adapter = get_adapter(key)
        assert adapter.paper.organization == organization
        assert adapter.paper.published == published
        assert adapter.paper.selection_exception
        assert adapter.paper.code_url is None
        assert Path(
            f"src/auto_research/reproductions/{key.replace('-', '_')}"
        ).is_dir()


def test_deepfm_and_youtube_dnn_are_trainable_networks():
    import torch

    features = np.eye(12, 6, dtype=np.float32)
    config = FoundationalConfig(
        dimensions=8, history_length=4, batch_size=2, steps=1
    )
    histories = torch.randint(0, 12, (3, 4))
    candidates = torch.randint(0, 12, (3,))
    for kind in ("deepfm", "youtube-dnn"):
        model = build_foundational_model(kind, 12, features, config)
        logits = model(histories, candidates)
        assert logits.shape == (3,)
        logits.sum().backward()
        assert model.item.weight.grad is not None


def test_esmm_mmoe_and_ple_execute_distinct_multitask_graphs():
    import torch

    config = MultiTaskConfig(
        dimensions=8, experts=3, batch_size=4, steps=1,
        maximum_users=8, maximum_items=12,
    )
    users = torch.randint(0, 8, (5,))
    items = torch.randint(0, 12, (5,))
    parameter_counts = {}
    for kind in ("clicked-cvr", "esmm", "shared-bottom", "mmoe", "ple"):
        model = build_multitask_model(kind, 8, 12, config)
        click, conversion = model(users, items)
        assert click.shape == conversion.shape == (5,)
        (click.sum() + conversion.sum()).backward()
        assert model.user.weight.grad is not None
        parameter_counts[kind] = sum(parameter.numel() for parameter in model.parameters())
    assert parameter_counts["mmoe"] > parameter_counts["shared-bottom"]
    assert parameter_counts["ple"] > parameter_counts["mmoe"]
