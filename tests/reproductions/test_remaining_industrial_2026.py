from pathlib import Path

from auto_research.reproductions.registry import get_adapter


DATA = Path(__file__).resolve().parents[2] / "data"
KEYS = ("degre", "harness-lm", "grc", "mbgr", "growthgr", "mesh", "sam", "danet", "proximity-features")


def test_remaining_papers_have_quantified_ab_and_complete_metadata():
    for key in KEYS:
        adapter = get_adapter(key)
        assert adapter.paper.has_online_ab
        assert adapter.paper.organization
        assert adapter.paper.published
        assert adapter.paper.url.startswith("https://arxiv.org/abs/")


def test_method_telemetry_covers_the_paper_specific_paths():
    required = {
        "degre": ("dense_kl_labels", "beam_size"),
        "harness-lm": ("alignment_mse_after", "contrastive_loss_final", "frozen_document_index"),
        "grc": ("structured_sft_trajectories", "grpo_iterations", "egrs"),
        "mbgr": ("ldr_masked_targets", "semantic_id_levels"),
        "growthgr": ("mean_predicted_uplift", "mopo_iterations", "trie_constrained"),
        "mesh": ("modular_towers", "residual_gated_bias_correction"),
        "sam": ("learned_category_cycles", "ttnp_auxiliary_mse"),
        "danet": ("low_frequency_bins", "distribution_correction_user", "upstream_code_consulted"),
        "proximity-features": ("target_bucket_size", "buckets", "selected_blend"),
    }
    for key, fields in required.items():
        result = get_adapter(key).run(DATA, 42)
        assert all(field in result["stages"] for field in fields)
        assert result["setup"]["same_split_and_candidates"] is True
