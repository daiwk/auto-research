"""Multimodal formula/label-isolation unit tests; fixtures are not evidence."""
import random
from types import SimpleNamespace

import pytest
torch = pytest.importorskip("torch")
from torch import nn
from torch.nn import functional as F

from auto_research.multimodal.oct12_reward_transition import (
    LoRALinear, append_response, caption_negative, group_split, in_batch_bt,
    mean_response_states, mint_verified_pair, select_probe_layer,
    train_reward_head, verifier_score, woven_prompt,
)


def test_woven_keeps_real_image_references_and_excludes_gold_metadata():
    sentinel1, sentinel2 = object(), object()
    row = {"question": "Before <image_1>, after an action which state?", "images": [sentinel1, sentinel2],
           "answer": "C", "options": [
               {"label": label, "content": "<image_2>" if label == "B" else f"State {label}",
                "is_correct": label == "C", "distractor_type": "SECRET GOLD", "is_static": label == "A"}
               for label in "ABCD"]}
    messages, target = woven_prompt(row, rotation=1)
    content = messages[0]["content"]
    assert target == "B"
    assert [c["image"] for c in content if c["type"] == "image"] == [sentinel1, sentinel2]
    text = "".join(c["text"] for c in content if c["type"] == "text")
    assert "SECRET" not in text and "is_correct" not in text and "is_static" not in text
    assert "Answer with one option letter." in text
    # Option permutation relocates the target, not its content/observed image.
    assert [woven_prompt(row, r)[1] for r in range(4)] == ["C", "B", "A", "D"]


def test_grouped_split_has_exact_disjoint_sources_and_hashes():
    rows = [{"source_id": str(i // 3), "id": str(i)} for i in range(30)]
    split, metadata = group_split(rows, "source_id", 42)
    groups = [{row["source_id"] for row in split[s]} for s in ("train", "validation", "test")]
    assert not groups[0] & groups[1] and not groups[1] & groups[2] and not groups[0] & groups[2]
    assert sum(len(v) for v in split.values()) == 30
    assert metadata["split_counts"] == {"train": {"examples": 18, "groups": 6},
        "validation": {"examples": 6, "groups": 2}, "test": {"examples": 6, "groups": 2}}
    assert metadata == group_split(rows, "source_id", 42)[1]
    assert all(len(h) == 64 for h in metadata["item_sha256"].values())


def test_response_pooling_excludes_image_and_prompt_tokens():
    states = torch.tensor([[[1000., -1000.], [10., 50.], [1., 3.], [5., 7.]]])
    mask = torch.tensor([[False, False, True, True]])
    torch.testing.assert_close(mean_response_states(states, mask), torch.tensor([[3., 5.]]))
    with pytest.raises(ValueError):
        mean_response_states(states, torch.zeros_like(mask))


def test_append_response_preserves_image_pixels_and_masks_prompt():
    class Tokenizer:
        eos_token_id = 9
        def __call__(self, response, **kwargs):
            return SimpleNamespace(input_ids=torch.tensor([[4, 5]]))
    processor = SimpleNamespace(tokenizer=Tokenizer())
    pixels = torch.randn(1, 1, 3, 4, 4)
    prefix = {"input_ids": torch.tensor([[1, 2, 3]]), "attention_mask": torch.ones(1, 3, dtype=torch.long),
              "pixel_values": pixels, "pixel_attention_mask": torch.ones(1, 1, 4, 4)}
    inputs, mask = append_response(processor, prefix, "actual response", eos=True)
    assert inputs["pixel_values"] is pixels
    assert inputs["input_ids"].tolist() == [[1, 2, 3, 4, 5, 9]]
    assert mask.tolist() == [[False, False, False, True, True, True]]
    assert prefix["input_ids"].shape[1] == 3


def test_matrix_bt_uses_every_cross_entry_not_only_same_pair():
    head = nn.Linear(2, 1, bias=False)
    with torch.no_grad():
        head.weight.copy_(torch.tensor([[1., -.5]]))
    positive = torch.tensor([[2., 1.], [1., -2.]])
    negative = torch.tensor([[.4, -.2], [-1., 1.]])
    plus, minus = head(positive).flatten(), head(negative).flatten()
    expected = torch.stack([F.softplus(-.1 * (a - b)) for a in plus for b in minus]).mean()
    torch.testing.assert_close(in_batch_bt(head, positive, negative), expected)
    assert head.bias is None


def test_reward_head_learns_actual_features_and_selects_only_validation():
    positive, negative = torch.tensor([[1., 0.], [2., 0.]]), torch.tensor([[-1., 0.], [-2., 0.]])
    head = train_reward_head(positive, negative, seed=7, steps=50)
    assert head.weight[0, 0] > 0
    assert select_probe_layer({1: .5, 4: .8, 7: .6}) == 4
    assert select_probe_layer({1: .8, 4: .8}) == 1


def test_single_span_negative_is_same_style_and_word_count():
    class Near(random.Random):
        def random(self):
            return .25
    caption = "Two brown horses beside a red fence"
    negative, operator = caption_negative(caption, "A dog is running", Near(11))
    assert operator == "near_one_span"
    assert len(negative.split()) == len(caption.split())
    assert sum(a != b for a, b in zip(caption.split(), negative.split())) == 1


def test_bootstrap_verifier_is_distinct_and_preserves_no_pair_outcome():
    pair = mint_verified_pair(["A dog beside a person", "A dog beside an elephant"], {"dog", "person"})
    assert pair == ("A dog beside a person", "A dog beside an elephant", 1., .5)
    assert verifier_score("beautiful scene", {"dog"}) is None  # no vacuous positive
    assert mint_verified_pair(["A dog", "A dog runs"], {"dog"}) is None
    assert mint_verified_pair(["", "nice view"], {"dog"}) is None


def test_lora_preserves_frozen_backbone_and_trains_actual_residual():
    torch.manual_seed(13)
    base = nn.Linear(4, 3)
    layer = LoRALinear(base, rank=2, dropout=0)
    x, target = torch.randn(6, 4), torch.randn(6, 3)
    torch.testing.assert_close(layer(x), base(x))
    optimizer = torch.optim.SGD([layer.a, layer.b], lr=.1)
    loss = (layer(x) - target).square().mean()
    loss.backward()
    optimizer.step()
    assert not torch.allclose(layer(x), base(x))
    assert all(not p.requires_grad and p.grad is None for p in base.parameters())
