from auto_research.reproductions.hyformer.model import HyFormerConfig, build_model as build_hyformer
from auto_research.reproductions.onetrans.model import OneTransConfig
from auto_research.reproductions.rankmixer.model import RankMixerConfig, build_model
from auto_research.reproductions.rec_distill.model import RecDistillConfig


def test_rankmixer_head_count_matches_token_count_for_parameter_free_mix():
    config = RankMixerConfig()
    assert config.tokens == config.heads
    assert config.dimensions % config.tokens == 0


def test_rankmixer_evolution_variants_preserve_candidate_score_shape():
    import torch

    class Data:
        item_count = 20
        item_features = __import__("numpy").eye(20, 8, dtype="float32")

    config = RankMixerConfig(dimensions=32, heads=4, tokens=4, layers=2, sequence_length=6)
    history = torch.randint(0, Data.item_count, (3, 6))
    candidates = torch.randint(0, Data.item_count, (3, 5))
    for architecture in ("rankmixer_dense", "rankmixer_smoe", "tokenmixer_large", "zenith", "moi_mixer", "rankmixer_longer", "rankmixer_unimixer", "rankmixer_longer_unimixer"):
        model = build_model(architecture, Data, config)
        assert model.pair_scores(history, candidates).shape == (3, 5)


def test_hyformer_query_boost_has_divisible_token_subspaces():
    config = HyFormerConfig()
    tokens = config.queries + config.non_sequence_tokens
    assert config.dimensions % tokens == 0


def test_hyformer_directional_variants_preserve_full_catalog_shape():
    import numpy as np
    import torch

    class Data:
        item_count = 20
        item_features = np.eye(20, 8, dtype="float32")

    config = HyFormerConfig(dimensions=32, heads=4, layers=1, sequence_length=16)
    history = torch.randint(0, Data.item_count, (3, 16))
    for architecture in ("hyformer", "hyformer_longer", "hyformer_unimixer", "hyformer_longer_unimixer"):
        assert build_hyformer(architecture, Data, config)(history).shape == (3, Data.item_count)


def test_onetrans_keeps_separate_non_sequence_tokens():
    config = OneTransConfig()
    assert config.non_sequence_tokens == 2
    assert config.layers >= 2


def test_rec_distill_has_batch_then_streaming_phases():
    config = RecDistillConfig()
    assert config.teacher_dimensions > config.student_dimensions
    assert config.student_batch_steps > config.student_stream_steps > 0
