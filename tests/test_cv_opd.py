import math

import pytest
import torch

from auto_research.multimodal.cv_opd import intersection_over_union, jsd, negative_crop, objective, sampled_training_rollouts, topk_tail, verify_answer


@pytest.fixture(autouse=True)
def fixed_contract_random_state():
    state = torch.random.get_rng_state()
    torch.manual_seed(42)
    yield
    torch.random.set_rng_state(state)


def test_real_box_size_iou_and_impossible_crop():
    positive = (5, 5, 25, 25)
    negative = negative_crop((80, 80), positive, generator=torch.Generator().manual_seed(2))
    assert (negative[2] - negative[0], negative[3] - negative[1]) == (20, 20)
    assert intersection_over_union(positive, negative) <= .1
    with pytest.raises(ValueError, match="no same-size"):
        negative_crop((10, 10), (0, 0, 10, 10))


def test_jsd_symmetric_bounds_and_student_topk_tail_mass():
    p, q = torch.rand(2, 3, 7).softmax(-1), torch.rand(2, 3, 7).softmax(-1)
    distance = jsd(p.log(), q.log())
    torch.testing.assert_close(distance, jsd(q.log(), p.log()))
    assert (distance >= 0).all() and (distance <= math.log(2)).all()
    reduced_p, reduced_q = topk_tail(p.log(), q.log(), 2)
    torch.testing.assert_close(reduced_p.exp().sum(-1), torch.ones(2, 3))
    torch.testing.assert_close(reduced_q.exp().sum(-1), torch.ones(2, 3))
    support = p.topk(2, -1).indices
    torch.testing.assert_close(reduced_q[..., :2].exp(), q.gather(-1, support))


def test_sample_gate_keeps_incorrect_siblings_and_detaches_teacher():
    torch.manual_seed(2)
    student = torch.randn(4, 3, 6, requires_grad=True)
    positive = torch.randn(4, 3, 6, requires_grad=True)
    negative = torch.randn(4, 3, 6, requires_grad=True)
    mask = torch.ones(4, 3, dtype=torch.bool)
    loss, parts = objective(student, positive, negative, mask,
                             torch.tensor([True, False, False, False]),
                             torch.tensor([0, 0, 1, 1]), topk=2)
    assert parts["retained_samples"] == 1
    assert parts["retained_rollouts"] == 2  # don't wrongly retain only correct rollout
    assert parts["valid_tokens"] == 6
    loss.backward()
    assert positive.grad is None and negative.grad is None
    assert student.grad[:2].abs().sum() > 0
    assert student.grad[2:].abs().sum() == 0


def test_zero_correct_returns_real_zero_gradient_and_strict_batch_gate():
    student = torch.zeros(2, 3, 6, requires_grad=True)
    teacher = torch.zeros_like(student)
    loss, parts = objective(student, teacher, teacher, torch.ones(2, 3, dtype=torch.bool),
                             torch.zeros(2, dtype=torch.bool), torch.zeros(2, dtype=torch.long), topk=2)
    loss.backward()
    assert float(loss.detach()) == 0 and student.grad.abs().sum() == 0
    assert parts["gated_tokens"] == 0
    assert verify_answer("Yes, there is.", ["yes"])
    assert not verify_answer("No.", ["yes"])
    assert not verify_answer("unsure", ["yes"])


def test_multiclass_verifier_is_strict_except_indefinite_article():
    assert verify_answer("A cat.", ["cat"])
    assert verify_answer("CAT", ["cat"])
    assert verify_answer("  an  animal ", ["animal"])
    for response in ("not a cat", "cat or dog", "a cat in a room", "cats", "the cat", "a dog"):
        assert not verify_answer(response, ["cat"])
    with pytest.raises(ValueError, match="nonempty"):
        verify_answer("cat", [])


def test_training_verifier_gold_cannot_reach_rollout_policy_calls():
    import re
    from types import SimpleNamespace

    calls = []
    question = "Name the main object in this picture. Reply with one COCO category name and no other words."

    class Policy:
        processor = SimpleNamespace(tokenizer=SimpleNamespace(decode=lambda tokens, **kwargs: "A cat."))

        def rollout(self, image, policy_question, maximum_tokens):
            calls.append((image, policy_question, maximum_tokens))
            return torch.tensor([1, 2])

    policy = Policy()
    tokens, correct = sampled_training_rollouts(policy, "image pixels", question, ["cat"], 2, 16)
    assert correct == [True, True]
    _, changed_gold = sampled_training_rollouts(policy, "image pixels", question, ["dog"], 2, 16)
    assert changed_gold == [False, False]
    assert calls[:2] == calls[2:]
    assert all(not re.search(r"\b(cat|dog)\b", prompt.lower()) for _, prompt, _ in calls)
    assert all(torch.equal(row, torch.tensor([1, 2])) for row in tokens)


def test_cv_records_require_original_train_source_and_hashed_images(tmp_path):
    import hashlib
    import json
    from pathlib import Path
    import runpy

    from auto_research.foundation_models.oct13_runtime import check_dataset_identity

    loader = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_cv_opd.py"))["load_rows"]
    row = {"id": "fixture-only", "image": "image.png", "question": "Name the main object in this picture.",
           "answer": "cat", "bbox": [0, 0, 4, 4], "split": "train", "verified": True}
    (tmp_path / "records.jsonl").write_text(json.dumps(row) + "\n")
    (tmp_path / "image.png").write_bytes(b"non-capability loader fixture")
    files = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in tmp_path.iterdir()}
    manifest = {"kind": "dataset", "public_id": "COCO2017/train2017", "revision": "fixed-test-fixture",
                "source_split": "train2017", "rows": 1, "files": files}
    (tmp_path / "provenance.json").write_text(json.dumps(manifest))
    verified = check_dataset_identity(tmp_path, manifest["public_id"], manifest["revision"], ("records.jsonl",))
    assert loader(tmp_path / "records.jsonl", verified)[0]["references"] == ["cat"]
    with pytest.raises(ValueError, match="original COCO train2017"):
        loader(tmp_path / "records.jsonl", {**verified, "source_split": "val2017"})
    with pytest.raises(ValueError, match="every CV image"):
        loader(tmp_path / "records.jsonl", {**verified, "files": {"records.jsonl": files["records.jsonl"]}})
    # Renaming both row ID and image path does not evade a pixel-file overlap.
    (tmp_path / "renamed.png").write_bytes((tmp_path / "image.png").read_bytes())
    other = {**row, "id": "different-id", "image": "renamed.png", "split": "validation"}
    (tmp_path / "records.jsonl").write_text(json.dumps(row) + "\n" + json.dumps(other) + "\n")
    overlap = {**verified, "rows": 2, "files": {
        **verified["files"], "renamed.png": verified["files"]["image.png"],
        "records.jsonl": hashlib.sha256((tmp_path / "records.jsonl").read_bytes()).hexdigest()}}
    with pytest.raises(ValueError, match="training/held-out boundary"):
        loader(tmp_path / "records.jsonl", overlap)
