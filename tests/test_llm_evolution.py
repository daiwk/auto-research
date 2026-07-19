from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm


def test_all_micro_llm_architectures_preserve_causal_lm_shape():
    import torch

    config = MicroLMConfig(vocab_size=128, dimensions=64, layers=2, heads=4, sequence_length=24)
    tokens = torch.randint(0, config.vocab_size, (3, config.sequence_length))
    architectures = (
        "gpt_baseline", "gpt_gqa", "llama_modern", "llama_gqa",
        "parallel_gelu", "parallel_swiglu", "llama_gqa_parallel",
        "hyper_connections", "mhc",
    )
    for architecture in architectures:
        model = build_micro_lm(architecture, config)
        assert model(tokens).shape == (3, config.sequence_length, config.vocab_size)


def test_neftune_noise_only_changes_training_forward():
    import torch

    torch.manual_seed(1)
    config = MicroLMConfig(vocab_size=64, dimensions=32, layers=1, heads=4, sequence_length=12)
    model = build_micro_lm("llama_modern", config)
    tokens = torch.randint(0, config.vocab_size, (2, config.sequence_length))
    model.eval()
    clean = model(tokens, embedding_noise_alpha=10.0)
    assert torch.equal(clean, model(tokens, embedding_noise_alpha=0.0))
    model.train()
    assert not torch.equal(model(tokens, embedding_noise_alpha=10.0), model(tokens, embedding_noise_alpha=0.0))
