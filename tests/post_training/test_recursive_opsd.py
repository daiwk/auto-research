import torch

from auto_research.post_training.local_lora import attach_lora, disabled_adapters
from auto_research.post_training.recursive_opsd import (
    accept_refinement,
    forward_kl,
    numeric_answer,
    teacher_prompt,
)


def test_forward_kl_is_zero_for_equal_logits_and_detaches_teacher():
    student = torch.tensor([[[1.0, 0.0], [0.0, 1.0]]], requires_grad=True)
    teacher = student.detach().clone().requires_grad_(True)
    loss = forward_kl(student, teacher)
    assert torch.allclose(loss, torch.zeros(()), atol=1e-7)
    loss.backward()
    assert teacher.grad is None


def test_forward_kl_uses_teacher_distribution():
    student = torch.tensor([[[0.0, 0.0]]], requires_grad=True)
    teacher = torch.tensor([[[3.0, 0.0]]])
    loss = forward_kl(student, teacher)
    assert loss.item() > 0
    loss.backward()
    assert student.grad is not None


def test_srcl_filter_requires_short_correct_natural_self_contained_rewrite():
    source = "We can calculate. Wait, let me reconsider. The result is 12. Answer: 12"
    good = "Six plus six is twelve. Answer: 12"
    assert accept_refinement(source, good, "12", source_tokens=25, rewrite_tokens=12, ended=True)
    assert not accept_refinement(source, good, "13", source_tokens=25, rewrite_tokens=12, ended=True)
    assert not accept_refinement(source, good, "12", source_tokens=25, rewrite_tokens=25, ended=True)
    assert not accept_refinement(source, good, "12", source_tokens=25, rewrite_tokens=12, ended=False)
    assert not accept_refinement(source, "Wait, Answer: 12", "12", source_tokens=25, rewrite_tokens=8, ended=True)
    assert not accept_refinement(source, "As shown above, Answer: 12", "12", source_tokens=25, rewrite_tokens=9, ended=True)


def test_teacher_prompt_puts_gold_in_assistant_and_rewrite_excludes_it():
    prompt = teacher_prompt("What is 6+6?", "12")
    assert prompt[0]["role"] == "user"
    assert prompt[1]["role"] == "assistant"
    assert "12" in prompt[1]["content"]
    assert numeric_answer("Reasoning. Answer: 12") == "12"
    assert numeric_answer("Reasoning. \\boxed{12}") == "12"


def test_local_lora_frozen_teacher_context_and_trainable_student():
    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.q_proj = torch.nn.Linear(3, 3, bias=False)

        def forward(self, inputs):
            return self.q_proj(inputs)

    model = attach_lora(Toy(), rank=2)
    assert not model.q_proj.base.weight.requires_grad
    with torch.no_grad():
        model.q_proj.b.fill_(0.25)
    inputs = torch.ones(1, 3)
    live = model(inputs)
    with disabled_adapters(model):
        frozen = model(inputs)
    assert not torch.allclose(live, frozen)
    assert torch.allclose(model(inputs), live)
    model(inputs).sum().backward()
    assert model.q_proj.a.grad is not None
    assert model.q_proj.b.grad is not None
