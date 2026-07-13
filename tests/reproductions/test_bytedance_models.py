from auto_research.reproductions.hyformer.model import HyFormerConfig
from auto_research.reproductions.onetrans.model import OneTransConfig
from auto_research.reproductions.rankmixer.model import RankMixerConfig
from auto_research.reproductions.rec_distill.model import RecDistillConfig


def test_rankmixer_head_count_matches_token_count_for_parameter_free_mix():
    config = RankMixerConfig()
    assert config.tokens == config.heads
    assert config.dimensions % config.tokens == 0


def test_hyformer_query_boost_has_divisible_token_subspaces():
    config = HyFormerConfig()
    tokens = config.queries + config.non_sequence_tokens
    assert config.dimensions % tokens == 0


def test_onetrans_keeps_separate_non_sequence_tokens():
    config = OneTransConfig()
    assert config.non_sequence_tokens == 2
    assert config.layers >= 2


def test_rec_distill_has_batch_then_streaming_phases():
    config = RecDistillConfig()
    assert config.teacher_dimensions > config.student_dimensions
    assert config.student_batch_steps > config.student_stream_steps > 0
