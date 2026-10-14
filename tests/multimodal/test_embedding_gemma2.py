from types import SimpleNamespace

import pytest
import torch

from auto_research.multimodal.embedding_gemma2 import EmbeddingGemma2Encoder, masked_mean, retrieval_recall


def test_pooling_excludes_padding_and_renormalizes_truncated_prefix():
    hidden = torch.ones(1, 3, 768)
    hidden[:, 2] = 1000
    mask = torch.tensor([[1, 1, 0]])
    value = masked_mean(hidden, mask, dimensions=128)
    assert value.shape == (1, 128)
    assert torch.allclose(value.norm(dim=-1), torch.ones(1))
    assert torch.allclose(value, torch.full_like(value, 128 ** -.5))
    with pytest.raises(ValueError):
        masked_mean(hidden, torch.zeros_like(mask))


def test_encoding_keeps_processor_metadata_and_uses_asymmetric_prompts():
    calls = []
    def processor(**kwargs):
        calls.append(kwargs)
        return {"input_ids": torch.ones(1, 2, dtype=torch.long),
                "attention_mask": torch.tensor([[1, 0]]), "image_position_ids": torch.tensor([[7]])}
    def model(**kwargs):
        assert "image_position_ids" in kwargs
        return SimpleNamespace(last_hidden_state=torch.ones(1, 2, 768))
    encoder = EmbeddingGemma2Encoder(processor, model)
    encoder.encode(texts=["hello"], role="query")
    encoder.encode(texts=["hello"], role="document")
    assert calls[0]["text"][0].startswith("task: search result | query:")
    assert calls[1]["text"][0].startswith("title: none | text:")


def test_multipositive_retrieval_and_no_unpaired_caption():
    image = torch.eye(2)
    text = torch.tensor([[1.,0.], [1.,0.], [0.,1.]])
    metrics = retrieval_recall(image, text, ["a","a","b"], ["a","b"])
    assert metrics["image_to_text.recall_at_1"] == 1
    assert metrics["text_to_image.recall_at_1"] == 1
    with pytest.raises(ValueError):
        retrieval_recall(image, text, ["a","a","missing"], ["a","b"])


def test_floating_checkpoint_revision_rejected_before_download():
    with pytest.raises(ValueError, match="immutable"):
        EmbeddingGemma2Encoder.load(revision="main")
