"""November 4 post-training component contracts, distinct from agent tests."""
from __future__ import annotations

import copy
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import pytest
import torch

from auto_research.post_training import p2_mopd, shuffled_opsd, targeted_guidance


def test_prior_optimizer_matches_explicit_base_and_coefficient_adam_multiple_steps():
    base = torch.tensor([[.2, -.4], [.8, .1]], dtype=torch.float64)
    directions = torch.tensor([[[1., 0.], [0., .3]], [[0., .4], [-.5, 0.]]], dtype=torch.float64)
    alpha = torch.tensor([.25, .25], dtype=torch.float64)
    module = p2_mopd.PriorModule(base, directions, alpha)
    optimizer = p2_mopd.ParameterPriorOptimizer([module], lr_weight=.03, lr_coefficient=.07,
                                               weight_clip=.2, coefficient_clip=.1)
    explicit_base = torch.nn.Parameter(base.clone())
    explicit_alpha = torch.nn.Parameter(alpha.clone())
    weight_optimizer = torch.optim.AdamW([explicit_base], lr=.03, weight_decay=0.)
    alpha_optimizer = torch.optim.Adam([explicit_alpha], lr=.07)
    target = torch.tensor([[1., 2.], [-1., 1.]], dtype=torch.float64)
    for _ in range(6):
        optimizer.zero_grad()
        weight_optimizer.zero_grad(); alpha_optimizer.zero_grad()
        materialized_loss = (module.weight - target).square().sum()
        materialized_loss.backward()
        explicit = explicit_base + torch.einsum('k,kij->ij', explicit_alpha, directions)
        (explicit - target).square().sum().backward()
        torch.nn.utils.clip_grad_norm_([explicit_base], .2)
        torch.nn.utils.clip_grad_norm_([explicit_alpha], .1)
        weight_optimizer.step(); alpha_optimizer.step()
        assert optimizer.step()
        torch.testing.assert_close(module.weight, explicit_base + torch.einsum('k,kij->ij', explicit_alpha, directions), rtol=1e-12, atol=1e-12)
        torch.testing.assert_close(module.coefficients, explicit_alpha, rtol=1e-12, atol=1e-12)
    torch.testing.assert_close(module.equivalent_base(), explicit_base, rtol=1e-12, atol=1e-12)
    assert module.task_vectors.grad is None
    assert not module.task_vectors.requires_grad


def test_coefficient_gradient_uses_unclipped_gradient_and_independent_budget():
    module = p2_mopd.PriorModule(torch.zeros(2, dtype=torch.float64),
                                 torch.tensor([[2., 0.]], dtype=torch.float64), torch.tensor([0.], dtype=torch.float64))
    optimizer = p2_mopd.ParameterPriorOptimizer([module], lr_weight=.01, lr_coefficient=.02,
                                               weight_clip=.01, coefficient_clip=100.)
    module.weight.grad = torch.tensor([3., 4.], dtype=torch.float64)
    assert optimizer.step()
    assert float(module.coefficients.grad[0]) == 6.
    assert float(module.weight.grad.norm()) <= .01
    # A wrong implementation calculating the inner product after clipping gets .012.
    assert float(module.coefficients.grad[0]) > 100 * float(module.weight.grad[0])


def test_global_weight_clipping_includes_nonprojection_parameters():
    module = p2_mopd.PriorModule(torch.zeros(1, dtype=torch.float64),
                                 torch.ones(1, 1, dtype=torch.float64), torch.zeros(1, dtype=torch.float64))
    other = torch.nn.Parameter(torch.zeros(1, dtype=torch.float64))
    optimizer = p2_mopd.ParameterPriorOptimizer([module], other_parameters=[other], weight_clip=1., coefficient_clip=100.)
    module.weight.grad = torch.tensor([3.], dtype=torch.float64)
    other.grad = torch.tensor([4.], dtype=torch.float64)
    assert optimizer.step()
    assert float(module.weight.grad[0]) == pytest.approx(.6, abs=1e-6)
    assert float(other.grad[0]) == pytest.approx(.8, abs=1e-6)


def test_nonfinite_prior_step_does_not_change_parameters_or_optimizer_state():
    module = p2_mopd.PriorModule(torch.zeros(2), torch.ones(1, 2), torch.zeros(1))
    optimizer = p2_mopd.ParameterPriorOptimizer([module])
    module.weight.grad = torch.ones_like(module.weight)
    assert optimizer.step()
    weight, alpha = module.weight.detach().clone(), module.coefficients.detach().clone()
    state = copy.deepcopy(optimizer.weight_optimizer.state_dict())
    alpha_state = copy.deepcopy(optimizer.coefficient_optimizer.state_dict())
    module.weight.grad = torch.tensor([float('nan'), 1.])
    assert optimizer.step() is False
    assert torch.equal(module.weight, weight) and torch.equal(module.coefficients, alpha)
    for saved, actual in [(state, optimizer.weight_optimizer.state_dict()),
                          (alpha_state, optimizer.coefficient_optimizer.state_dict())]:
        assert saved['param_groups'] == actual['param_groups']
        for parameter in saved['state']:
            for key, value in saved['state'][parameter].items():
                assert torch.equal(value, actual['state'][parameter][key])


def test_prior_directions_are_frozen_copies_not_mutable_input_aliases():
    directions = torch.ones(1, 2, requires_grad=True)
    module = p2_mopd.PriorModule(torch.zeros(2), directions, torch.zeros(1))
    with torch.no_grad(): directions.fill_(7)
    assert torch.equal(module.task_vectors, torch.ones(1, 2))
    with pytest.raises(ValueError):
        p2_mopd.PriorModule(torch.zeros(2), torch.zeros(1, 3), torch.zeros(1))


def test_shared_shuffle_preserves_words_blocks_and_fixed_unrelated_references():
    problems = [f'problem {i} has four named objects' for i in range(5)]
    examples = [f'worked example {i}: solution remains in order' for i in range(5)]
    inputs = shuffled_opsd.prepare_shared_inputs(problems, examples, seed=42, block_size=2)
    assert inputs.student_problems == inputs.teacher_problems
    assert inputs.reference_indices == (1, 2, 3, 4, 0)  # (i + 111) % 5
    assert inputs.teacher_examples == tuple(examples[i] for i in inputs.reference_indices)
    for original, transformed in zip(problems, inputs.student_problems):
        assert Counter(original.split()) == Counter(transformed.split())
        blocks = [' '.join(original.split()[i:i + 2]) for i in range(0, len(original.split()), 2)]
        assert all(block in transformed for block in blocks)
    assert inputs == shuffled_opsd.prepare_shared_inputs(problems, examples, seed=42, block_size=2)
    assert all('solution' not in problem for problem in inputs.student_problems)


def test_reference_shift_cannot_pair_an_example_with_itself():
    with pytest.raises(ValueError):
        shuffled_opsd.prepare_shared_inputs(['a', 'b', 'c'], ['A', 'B', 'C'], seed=1)
    with pytest.raises(ValueError):
        shuffled_opsd.prepare_shared_inputs(['a', 'b'], ['A', 'B'], seed=1, block_size=0)


def test_signed_vocabulary_cap_is_not_ordinary_kl_or_nonnegative_clipping():
    student = torch.tensor([[[.99, .01]]], dtype=torch.float64).log().requires_grad_()
    teacher = torch.tensor([[[.5, .5]]], dtype=torch.float64).log().requires_grad_()
    mask = torch.ones(1, 1, dtype=torch.bool)
    loss = shuffled_opsd.capped_distillation_loss(student, teacher, mask, temperature=1.)
    expected = .5 * math.log(.5 / .99) + .05
    assert float(loss.detach()) == pytest.approx(expected)
    assert loss < 0  # The upper-capped signed sum need not be a divergence.
    loss.backward()
    assert teacher.grad is None and student.grad is not None


def test_capped_loss_weights_each_response_equally_and_masks_padding_nan():
    student = torch.zeros(2, 3, 2, dtype=torch.float64, requires_grad=True)
    teacher = torch.tensor([[[2., 0.], [float('nan')]*2, [float('nan')]*2],
                            [[.2, -.2], [.2, -.2], [.2, -.2]]], dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[True, False, False], [True, True, True]])
    first = shuffled_opsd.capped_distillation_loss(student[:1, :1], teacher[:1, :1], mask[:1, :1])
    second = shuffled_opsd.capped_distillation_loss(student[1:], teacher[1:], mask[1:])
    loss = shuffled_opsd.capped_distillation_loss(student, teacher, mask)
    torch.testing.assert_close(loss, (first + second) / 2)
    loss.backward()
    assert teacher.grad is None
    assert torch.equal(student.grad[~mask], torch.zeros_like(student.grad[~mask]))
    assert student.grad.isfinite().all()


def test_capped_loss_autograd_and_temperature_without_temperature_squared():
    generator = torch.Generator().manual_seed(11)
    student = torch.randn(2, 2, 3, dtype=torch.float64, generator=generator, requires_grad=True)
    teacher = torch.randn(2, 2, 3, dtype=torch.float64, generator=generator)
    mask = torch.ones(2, 2, dtype=torch.bool)
    assert torch.autograd.gradcheck(lambda value: shuffled_opsd.capped_distillation_loss(value, teacher, mask, cap=20., temperature=1.7), (student,))
    q = (teacher / 1.7).softmax(-1)
    manual = (q * ((teacher / 1.7).log_softmax(-1) - (student / 1.7).log_softmax(-1))).sum(-1).mean()
    torch.testing.assert_close(shuffled_opsd.capped_distillation_loss(student, teacher, mask, cap=20., temperature=1.7), manual)


@pytest.mark.parametrize('failure', ['empty_response', 'teacher_nan', 'bad_temperature', 'bad_cap', 'mask_dtype'])
def test_capped_loss_rejects_invalid_active_protocol(failure):
    student = torch.zeros(1, 2, 3)
    teacher = student.clone()
    mask = torch.ones(1, 2, dtype=torch.bool)
    options = {}
    if failure == 'empty_response': mask[:] = False
    if failure == 'teacher_nan': teacher[0, 0, 0] = float('nan')
    if failure == 'bad_temperature': options['temperature'] = 0.
    if failure == 'bad_cap': options['cap'] = float('inf')
    if failure == 'mask_dtype': mask = mask.float()
    with pytest.raises(ValueError):
        shuffled_opsd.capped_distillation_loss(student, teacher, mask, **options)


def test_targeted_reverse_kl_only_failed_turns_with_all_response_token_denominator():
    student = torch.tensor([[[.8, .2], [.5, .5], [.5, .5], [.5, .5]]], dtype=torch.float64).log().requires_grad_()
    teacher = torch.tensor([[[.2, .8], [.9, .1], [.9, .1], [.9, .1]]], dtype=torch.float64).log().requires_grad_()
    response = torch.ones(1, 4, dtype=torch.bool)
    failed = torch.tensor([[True, False, False, False]])
    grpo = student.sum() * 0
    loss = targeted_guidance.targeted_guidance_loss(student, teacher, response, failed, grpo_loss=grpo, guidance_weight=1.)
    expected = (.8 * math.log(4) + .2 * math.log(.25)) / 4
    assert float(loss.detach()) == pytest.approx(expected)
    loss.backward()
    assert teacher.grad is None
    assert torch.equal(student.grad[~failed], torch.zeros_like(student.grad[~failed]))
    assert student.grad[failed].norm() > 0


def test_turn_failure_mapping_excludes_padding_and_handles_multiple_failed_turns():
    turns = torch.tensor([[0, 0, 1, 1, -1], [0, 1, 1, 2, 2]])
    failed_turns = torch.tensor([[False, True, False], [True, False, True]])
    actual = targeted_guidance.token_failure_mask(turns, failed_turns)
    assert actual.tolist() == [[False, False, True, True, False], [True, False, False, True, True]]
    with pytest.raises(ValueError):
        targeted_guidance.token_failure_mask(torch.tensor([[4]]), torch.tensor([[True]]))


def test_no_failures_or_zero_guidance_returns_original_rl_loss_and_gradient():
    student = torch.randn(1, 3, 4, dtype=torch.float64, requires_grad=True)
    teacher = torch.full_like(student, float('nan'), requires_grad=True)
    response = torch.ones(1, 3, dtype=torch.bool)
    no_failures = torch.zeros_like(response)
    grpo = 3 * student[0, 0, 0]
    loss = targeted_guidance.targeted_guidance_loss(student, teacher, response, no_failures, grpo_loss=grpo)
    torch.testing.assert_close(loss, grpo)
    loss.backward()
    assert student.grad[0, 0, 0] == 3 and torch.count_nonzero(student.grad) == 1
    assert teacher.grad is None


@pytest.mark.parametrize('weight,has_failure', [(0., True), (.1, False)])
def test_disabled_guidance_never_overflows_while_constructing_zero(weight, has_failure):
    student = torch.full((1, 3, 4), torch.finfo(torch.float32).max / 4, requires_grad=True)
    teacher = torch.full_like(student, float('nan'), requires_grad=True)
    response = torch.ones(1, 3, dtype=torch.bool)
    failed = torch.full_like(response, has_failure)
    grpo = torch.tensor(2., requires_grad=True)
    loss = targeted_guidance.targeted_guidance_loss(student, teacher, response, failed,
                                                   grpo_loss=grpo, guidance_weight=weight)
    assert torch.isfinite(loss) and loss == 2
    loss.backward()
    assert torch.equal(student.grad, torch.zeros_like(student))
    assert teacher.grad is None and grpo.grad == 1


def test_targeted_guidance_gradcheck_and_not_forward_kl():
    student = torch.tensor([[[.7, .2, .1]]], dtype=torch.float64).log().requires_grad_()
    teacher = torch.tensor([[[.1, .4, .5]]], dtype=torch.float64).log()
    mask = torch.ones(1, 1, dtype=torch.bool)
    fn = lambda value: targeted_guidance.targeted_guidance_loss(value, teacher, mask, mask, grpo_loss=value.sum()*0, guidance_weight=.3)
    assert torch.autograd.gradcheck(fn, (student,))
    p, q = student.softmax(-1), teacher.softmax(-1)
    reverse = .3 * (p * (student.log_softmax(-1)-teacher.log_softmax(-1))).sum()
    forward = .3 * (q * (teacher.log_softmax(-1)-student.log_softmax(-1))).sum()
    torch.testing.assert_close(fn(student), reverse)
    assert not torch.isclose(reverse, forward)


@pytest.mark.parametrize('failure', ['failure_on_padding', 'teacher_nan', 'empty_response', 'negative_weight', 'vector_rl'])
def test_targeted_loss_rejects_incompatible_protocol(failure):
    student = torch.zeros(1, 2, 3)
    teacher = student.clone()
    response = torch.tensor([[True, False]])
    failed = torch.tensor([[True, False]])
    grpo = torch.tensor(0.)
    weight = .1
    if failure == 'failure_on_padding': failed[0, 1] = True
    if failure == 'teacher_nan': teacher[0, 0, 0] = float('nan')
    if failure == 'empty_response': response[:] = False
    if failure == 'negative_weight': weight = -.1
    if failure == 'vector_rl': grpo = torch.zeros(1)
    with pytest.raises(ValueError):
        targeted_guidance.targeted_guidance_loss(student, teacher, response, failed,
                                                grpo_loss=grpo, guidance_weight=weight)


def test_half_precision_probability_reductions_promote_to_float32():
    student = torch.zeros(1, 2, 3, dtype=torch.float16, requires_grad=True)
    teacher = torch.ones_like(student)
    mask = torch.ones(1, 2, dtype=torch.bool)
    assert shuffled_opsd.capped_distillation_loss(student, teacher, mask).dtype == torch.float32
    assert targeted_guidance.targeted_guidance_loss(student, teacher, mask, mask,
                                                   grpo_loss=torch.tensor(0.)).dtype == torch.float32


@pytest.mark.parametrize('module', [p2_mopd, shuffled_opsd, targeted_guidance])
@pytest.mark.parametrize('seed', [42, 43, 44])
def test_component_diagnostics_are_finite_strictly_l1_and_behavior_checked(module, seed):
    result = module.diagnostic(seed, device='cpu')
    assert result['seed'] == seed and result['diagnostic_only']
    assert result['evaluation_tier'] == 'l1_mechanism'
    assert result['metrics']['model_calls'] == 0
    assert all(type(value) is bool and value for value in result['checks'].values()), result
    assert all(math.isfinite(value) for value in result['metrics'].values())


@pytest.mark.parametrize('key,paper_id,published_at', [
    ('p2-mopd', '2611.03953', '2026-11-02T20:53:15Z'),
    ('shuffled-opsd', '2611.04958', '2026-11-03T14:17:20Z'),
    ('targeted-guidance', '2611.05266', '2026-11-03T17:54:33Z'),
])
def test_documentation_learning_and_source_figure_contract(key, paper_id, published_at):
    root = Path(__file__).resolve().parents[2]
    catalog = json.loads((root / f'src/auto_research/paper_specs/catalog/post-training/{key}.json').read_text())
    assert catalog['published_at'] == published_at and catalog['announced_on'] == '2026-11-04'
    assert catalog['code'] is None and catalog['upstream_revision'] is None
    assert catalog['adapter'] is None and catalog['implementation_status'] == 'component_only'
    assert catalog['requires_gpu_validation'] and catalog['diagnostic_only']
    assert not catalog['promotion_eligible'] and not catalog['evolve_integrated']
    assert catalog['full_experiment_status'] == 'not_reproduced_high_cost'
    assert catalog['full_experiment_review_done'] and catalog['review_done']
    assert not catalog['automatic_retry'] and not catalog['automatic_implementation_queue']
    folder = root / f'docs/post-training/{paper_id}-{key}'
    chinese = (folder / 'README.md').read_bytes()
    english = (folder / 'README-en.md').read_text()
    assert f'<!-- source-sha256: {hashlib.sha256(chinese).hexdigest()} -->' in english
    assert all(ord(char) >= 32 or char in '\n\r\t' for char in chinese.decode())
    for field in ['## 论文信息', '原始发布日期', '原作者代码', '本地 Adapter / key',
                  '本地代码', '成本过高，不复现（审查 DONE）', '未报告']:
        assert field in chinese.decode()
    provenance = json.loads((folder / 'assets/provenance.json').read_text())
    assert provenance['paper_id'] == paper_id + 'v1' and provenance['figure'] == '2'
    assert hashlib.sha256((folder / 'assets' / provenance['local_path']).read_bytes()).hexdigest() == provenance['sha256']
    assert 'non-exclusive' in provenance['license'] and provenance['visual_review']
    qa = json.loads((root / 'docs/learning/questions/nov04b-post.json').read_text())
    translations = json.loads((root / 'docs/en/learning/translations/qa-nov04b-post.json').read_text())['units']
    questions = qa['papers']['post-training:' + key]['questions']
    assert {question['level'] for question in questions} == {'basics', 'mechanism', 'comparison', 'implementation'}
    for question in questions:
        assert question['added'] == '2026-11-04' and question['example'] and question['source_sections']
        entry = translations[f"qa/post-training:{key}/{question['id']}"]
        serialized = json.dumps(question, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        assert entry['source_sha256'] == hashlib.sha256(serialized.encode()).hexdigest()
        assert entry['reviewed'] is True and all(entry['fields'][field] for field in ['question', 'answer', 'example'])
