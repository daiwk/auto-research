"""L0 instrumented tests; these fixtures are not checkpoint/GPU evidence."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch
from PIL import Image

from auto_research.multimodal.system_one_rerank import (
    ForwardVLMReranker,
    MultimodalInput,
    RerankCandidate,
    build_choice_content,
    diagnostic,
    run_checkpoint_cases,
)


class Tokenizer:
    unk_token_id = 99

    def encode(self, text, add_special_tokens=False):
        assert not add_special_tokens
        return [ord(text) - 64]


class Processor:
    tokenizer = Tokenizer()

    def apply_chat_template(self, messages, **kwargs):
        self.messages, self.template_kwargs = messages, kwargs
        return "rendered user turn and assistant answer prefix"

    def __call__(self, **kwargs):
        self.processing_kwargs = kwargs
        images = kwargs.get("images", [])
        return {
            "input_ids": torch.tensor([[7, 8, 9]]),
            "attention_mask": torch.ones(1, 3, dtype=torch.long),
            "pixel_values": torch.tensor([sum(image.getpixel((0, 0))) for image in images]),
        }


class InstrumentedForwardModel(torch.nn.Module):
    """A parameterized L0 spy, deliberately not advertised as a trained VLM."""

    def __init__(self, selected=(0.0, 1.0, 2.0, 3.0)):
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.tensor(0.0))
        self.selected = selected
        self.calls = 0
        self.grad_enabled = None
        self.was_training_in_forward = None

    def forward(self, input_ids, attention_mask, pixel_values, use_cache):
        assert not use_cache
        self.calls += 1
        self.grad_enabled = torch.is_grad_enabled()
        self.was_training_in_forward = self.training
        logits = torch.zeros(1, 3, 128)
        # Reading another sequence position would give a different result.
        logits[0, 0, 1] = 100
        logits[0, -1, 80] = 30  # outside labels: restricted, not full-vocab softmax
        logits[0, -1, 1:1 + len(self.selected)] = torch.tensor(self.selected)
        if pixel_values.numel():
            logits[0, -1, 1] += pixel_values.float().sum() / 1000
        return SimpleNamespace(logits=logits)

    def generate(self, **kwargs):
        raise AssertionError("the readout must not autoregressively generate")


def candidates(count=4, *, image=None):
    return tuple(RerankCandidate(
        f"doc-{index}", MultimodalInput(f"document {index}", (image,) if image is not None else ())
    ) for index in range(count))


def test_real_forward_is_called_once_at_last_answer_position_without_generation():
    processor, model = Processor(), InstrumentedForwardModel()
    model.train()
    result = ForwardVLMReranker(processor, model).rank(
        MultimodalInput("question"), candidates(), instruction="retrieve evidence",
    )
    assert result.ranked_ids == ("doc-3", "doc-2", "doc-1", "doc-0")
    assert result.forward_passes == model.calls == 1
    assert result.autoregressive_decode_steps == 0
    assert result.prompt_tokens == 3
    assert result.label_token_ids == (1, 2, 3, 4)
    assert len(result.input_ids_sha256) == len(result.selected_logits_sha256) == 64
    torch.testing.assert_close(torch.tensor(result.probabilities), torch.arange(4.).softmax(0))
    assert sum(result.probabilities) == pytest.approx(1)
    assert result.restricted_probability_mass < 1e-9
    assert not model.grad_enabled and not model.was_training_in_forward
    assert model.training  # the caller's mode is restored
    assert processor.template_kwargs == {
        "tokenize": False, "add_generation_prompt": True, "enable_thinking": False,
    }


def test_images_are_passed_to_processor_and_can_change_forward_logits():
    dark, light = Image.new("RGB", (8, 8), "black"), Image.new("RGB", (8, 8), "white")
    processor, model = Processor(), InstrumentedForwardModel()
    ranker = ForwardVLMReranker(processor, model)
    first = ranker.rank(MultimodalInput("question"), candidates(image=dark), instruction="find image")
    second = ranker.rank(MultimodalInput("question"), candidates(image=light), instruction="find image")
    assert first.probabilities != second.probabilities
    assert len(processor.processing_kwargs["images"]) == 4
    assert len(second.image_provenance) == 4
    assert second.image_provenance[0]["jpeg_quality"] == 90
    assert len(second.image_provenance[0]["jpeg_sha256"]) == 64


def test_prompt_uses_images_before_text_and_never_inserts_candidate_identifiers():
    image = Image.new("RGBA", (10, 10), (1, 2, 3, 255))
    visible = (RerankCandidate("secret-external-id", MultimodalInput("a\n  b", (image,))),
               RerankCandidate("other-id", MultimodalInput("c")))
    content, images, metadata = build_choice_content(
        MultimodalInput("q", (image,)), visible, "instruction\n  text",
    )
    assert content[0]["text"] == "Instruction: instruction text\nQuery:"
    assert content[1]["type"] == "image" and content[2]["text"] == "q"
    index = next(i for i, part in enumerate(content) if part.get("text") == "\nCandidate A:")
    assert content[index + 1]["type"] == "image"
    assert content[index + 2]["text"] == "a b"
    assert "(A-B)" in content[-1]["text"]
    assert "secret-external-id" not in str(content)
    assert len(images) == len(metadata) == 2
    assert all(image.mode == "RGB" for image in images)


def test_paper_image_cap_preserves_aspect_ratio_and_source_image():
    image = Image.new("RGB", (100, 50), "red")
    _, images, metadata = build_choice_content(
        MultimodalInput("q"), candidates(2, image=image), "find image", max_pixels=500,
    )
    assert images[0].width * images[0].height <= 500
    assert images[0].width / images[0].height == pytest.approx(2, abs=.1)
    assert metadata[0]["original_size"] == [100, 50]
    assert image.size == (100, 50)


def test_ties_keep_first_stage_order_and_candidates_below_depth_are_untouched():
    model = InstrumentedForwardModel((2., 2., 1., 1.))
    result = ForwardVLMReranker(Processor(), model).rank(
        MultimodalInput("q"), candidates(7), instruction="rank", depth=4,
    )
    assert result.ranked_ids == tuple(f"doc-{i}" for i in range(7))
    assert len(result.probabilities) == result.rerank_depth == 4
    assert result.ranked_indices[4:] == (4, 5, 6)


@pytest.mark.parametrize("encoded", [[1, 2], [], [99], [-1], [True]])
def test_invalid_label_tokenization_fails_before_model_forward(encoded):
    processor, model = Processor(), InstrumentedForwardModel()
    processor.tokenizer = SimpleNamespace(encode=lambda *a, **k: encoded, unk_token_id=99)
    with pytest.raises(ValueError, match="label"):
        ForwardVLMReranker(processor, model).rank(
            MultimodalInput("q"), candidates(), instruction="rank",
        )
    assert model.calls == 0


def test_duplicate_label_tokens_and_candidate_ids_are_rejected():
    processor, model = Processor(), InstrumentedForwardModel()
    processor.tokenizer = SimpleNamespace(encode=lambda *a, **k: [1])
    with pytest.raises(ValueError, match="distinct"):
        ForwardVLMReranker(processor, model).rank(
            MultimodalInput("q"), candidates(), instruction="rank",
        )
    duplicate = (candidates()[0], candidates()[0])
    with pytest.raises(ValueError, match="unique"):
        ForwardVLMReranker(Processor(), model).rank(
            MultimodalInput("q"), duplicate, instruction="rank",
        )


def test_request_failure_explicitly_preserves_original_order_without_fake_scores():
    processor, model = Processor(), InstrumentedForwardModel()
    processor.tokenizer = SimpleNamespace(encode=lambda *a, **k: [])
    result = ForwardVLMReranker(processor, model).rank(
        MultimodalInput("q"), candidates(), instruction="rank", on_error="keep_first_stage",
    )
    assert result.fallback_used and result.failure_type == "ValueError"
    assert result.ranked_ids == result.candidate_ids
    assert result.probabilities is None and result.restricted_probability_mass is None
    assert result.forward_passes == 0


def test_non_finite_model_logits_fail_closed_and_restore_model_mode():
    model = InstrumentedForwardModel((float("nan"), 1., 2., 3.))
    model.eval()
    with pytest.raises(ValueError, match="non-finite"):
        ForwardVLMReranker(Processor(), model).rank(
            MultimodalInput("q"), candidates(), instruction="rank",
        )
    assert not model.training and model.calls == 1


def test_forward_exception_restores_callers_training_mode():
    class BrokenModel(InstrumentedForwardModel):
        def forward(self, **kwargs):
            assert not self.training
            raise RuntimeError("deliberate forward failure")

    model = BrokenModel()
    model.train()
    with pytest.raises(RuntimeError, match="deliberate"):
        ForwardVLMReranker(Processor(), model).rank(
            MultimodalInput("q"), candidates(), instruction="rank",
        )
    assert model.training


def test_padded_answer_position_is_not_silently_read():
    class PaddedProcessor(Processor):
        def __call__(self, **kwargs):
            batch = super().__call__(**kwargs)
            batch["attention_mask"][0, -1] = 0
            return batch

    model = InstrumentedForwardModel()
    with pytest.raises(ValueError, match="last position"):
        ForwardVLMReranker(PaddedProcessor(), model).rank(
            MultimodalInput("q"), candidates(), instruction="rank",
        )
    assert model.calls == 0


def test_trivial_candidate_list_does_not_claim_a_model_execution():
    model = InstrumentedForwardModel()
    result = ForwardVLMReranker(Processor(), model).rank(
        MultimodalInput("q"), candidates(1), instruction="rank",
    )
    assert result.forward_passes == model.calls == 0
    assert result.probabilities is None


def test_cuda_runner_refuses_cpu_and_does_not_fabricate_a_receipt(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    with pytest.raises(RuntimeError, match="real CUDA"):
        run_checkpoint_cases(
            Processor(), InstrumentedForwardModel(), [], checkpoint_id="public/model",
            checkpoint_revision="a" * 40, dataset={}, seed=42,
        )
    with pytest.raises(RuntimeError, match="real CUDA"):
        diagnostic(42, "cuda", InstrumentedForwardModel(), Processor())


def test_only_explicit_input_fields_can_reach_the_prompt():
    class LeakyInput(MultimodalInput):
        gold_answer = "secret"

    with pytest.raises(TypeError, match="explicit"):
        build_choice_content(LeakyInput("q"), candidates(), "rank")
    with pytest.raises(TypeError):
        MultimodalInput(text={"gold_answer": "secret"})
