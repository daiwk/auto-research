from pathlib import Path

import numpy as np

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.reproductions.fluid.model import prefix_ids
from auto_research.reproductions.memory_grafting.model import frequent_ngrams
from auto_research.reproductions.registry import get_adapter


DATA = Path(__file__).resolve().parents[2] / "data"


def test_fluid_has_ab_evidence_and_executes_id_free_final_stage():
    adapter = get_adapter("fluid")
    assert adapter.paper.has_online_ab
    result = adapter.run(DATA, 42)
    assert result["stages"]["candidate_item_id_in_final_model"] is False
    assert result["stages"]["separate_slice_and_room_tables"] is True
    assert set(result["stages"]) >= {
        "stage_1_slice_add_on", "stage_2_item_id_phase_out", "stage_3_room_add_on"
    }


def test_prefix_ids_encode_the_full_rq_path():
    codes = np.asarray([[1, 2, 3], [2, 2, 3]])
    prefixes = prefix_ids(codes, width=8)
    assert prefixes.tolist() == [[1, 10, 83], [2, 18, 147]]


def test_llm_papers_do_not_require_online_ab():
    assert get_adapter("memory-grafting").paper.track == "llm"
    assert not get_adapter("memory-grafting").paper.has_online_ab
    assert get_adapter("mhc").paper.track == "llm"


def test_memory_keys_include_longest_match_orders():
    keys = frequent_ngrams(np.asarray([1, 2, 3, 4, 1, 2, 3, 4]), capacity=20)
    assert {len(key) for key in keys} == {2, 3, 4}


def test_mhc_projection_is_doubly_stochastic():
    torch = __import__("pytest").importorskip("torch")
    config = MicroLMConfig(vocab_size=32, dimensions=16, layers=1, heads=2, sequence_length=8)
    model = build_micro_lm("mhc", config)
    stats = model.connection_stats(torch.randint(0, 32, (2, 8)))
    assert stats["row_sum_error"] < 1e-5
    assert stats["column_sum_error"] < 1e-5
    assert stats["spectral_norm_max"] <= 1.0001
