"""Exact bounded components, not substitutes for full LLM experiments."""
import importlib
import itertools
import math
import hashlib
import json
from pathlib import Path

import pytest
import torch

from auto_research.post_training.scar_shapley_credit import exact_shapley, scatter_dense_rewards
from auto_research.post_training.probabilistic_autorater import proper_rewards, parse_probability
from auto_research.post_training.rm_memorization_protocol import counterfactual_memorization
from auto_research.post_training.benchmark_self_bias import per_segment_ranks, self_bias


def test_scar_matches_independent_permutation_definition_signed_and_linear():
    values=torch.tensor([0.,-1.,2.,4.,0.,-1.,2.,4.],dtype=torch.float64,requires_grad=True)
    result=exact_shapley(values)
    reference=torch.zeros(3,dtype=torch.float64)
    for permutation in itertools.permutations(range(3)):
        coalition=0
        for i in permutation:
            reference[i] += (values.detach()[coalition | (1 << i)]-values.detach()[coalition])/6
            coalition |= 1 << i
    torch.testing.assert_close(result,reference)
    torch.testing.assert_close(exact_shapley(2*values),2*result)
    assert result[2] == 0 and not result.requires_grad
    assert exact_shapley(torch.tensor([0.,-2.]))[0] == -2
    assert result.sum() == values[-1]


@pytest.mark.parametrize('alpha',[0.,.3,1.])
def test_scar_rewards_only_at_span_ends_and_no_discounted_invariance_claim(alpha):
    credits=torch.tensor([2.,-1.,3.],dtype=torch.float64)
    ends=torch.tensor([1,4,6]);kl=-torch.arange(7,dtype=torch.float64)/100
    actual=scatter_dense_rewards(credits,ends,kl,terminal_reward=4.,alpha=alpha)
    expected=kl.clone();expected[ends]+=alpha*credits;expected[-1]+=(1-alpha)*4
    torch.testing.assert_close(actual,expected)
    assert float(actual.sum()-kl.sum()) == pytest.approx(4.)
    with pytest.raises(ValueError,match='discount'):
        scatter_dense_rewards(credits,ends,kl,terminal_reward=4.,discount=.99)
    with pytest.raises(ValueError,match='efficiency'):
        scatter_dense_rewards(credits,ends,kl,terminal_reward=5.)


@pytest.mark.parametrize('values',[torch.zeros(3),torch.zeros(2048),torch.tensor([1.,2.]),torch.tensor([0.,float('nan')])])
def test_scar_invalid_or_high_cost_coalitions_rejected(values):
    with pytest.raises(ValueError): exact_shapley(values)


@pytest.mark.parametrize('response,expected',[
    ('<think>rationale</think><prob_rb_better>0.3</prob_rb_better>',.3),
    ('<prob_rb_better>1</prob_rb_better>',1.),
    ('<prob_rb_better>nan</prob_rb_better>',None),
    ('<prob_rb_better>1.1</prob_rb_better>',None),
    ('0.4',None),
    ('<prob_rb_better>.2</prob_rb_better><prob_rb_better>.4</prob_rb_better>',None)])
def test_local_parser_is_explicit_and_fail_closed(response,expected):
    assert parse_probability(response) == expected


def test_autorater_piecewise_reward_values_gradients_and_label_detachment():
    p=torch.tensor([.2,.8,0.,1.,float('nan')],dtype=torch.float64,requires_grad=True)
    labels=torch.tensor([0.,1.,1.,0.,1.],dtype=torch.float64,requires_grad=True)
    valid=torch.tensor([True,True,True,True,False])
    b,l=proper_rewards(p,labels,valid)
    torch.testing.assert_close(b,torch.tensor([.96,.96,0.,0.,0.],dtype=torch.float64))
    torch.testing.assert_close(l,torch.tensor([math.log(.8),math.log(.8),math.log(.001),math.log(.001),math.log(.001)],dtype=torch.float64))
    (b+l).sum().backward()
    assert p.grad.isfinite().all() and p.grad[-1] == 0 and labels.grad is None
    # Clipped log's derivative is zero beyond bounds; Brier still has a signal.
    assert p.grad[2] == 2 and p.grad[3] == -2
    for epsilon in [0.,.5,float('nan')]:
        with pytest.raises(ValueError): proper_rewards(p,labels,valid,epsilon=epsilon)


def test_autorater_truthful_probability_maximizes_expected_reward_up_to_log_clipping():
    p=torch.linspace(0,1,1001,dtype=torch.float64)
    q=.37;valid=torch.ones_like(p,dtype=torch.bool)
    b1,l1=proper_rewards(p,torch.ones_like(p),valid)
    b0,l0=proper_rewards(p,torch.zeros_like(p),valid)
    assert p[(q*b1+(1-q)*b0).argmax()].item() == pytest.approx(q)
    assert p[(q*l1+(1-q)*l0).argmax()].item() == pytest.approx(q)


def test_memorization_conditions_on_inclusion_before_averaging_and_preserves_negative_cm():
    margins=torch.tensor([[0.,2.,-2.,1.],[0.,-2.,2.,1.]],dtype=torch.float64,requires_grad=True)
    membership=torch.tensor([[1,1,0,0],[1,1,0,0]],dtype=torch.bool)
    users=torch.tensor([4,4])
    result=counterfactual_memorization(margins,membership,users,train_runs=2,test_runs=2)
    expected_tm=margins.detach().sigmoid()[:,:2].mean(1)
    expected_tg=margins.detach().sigmoid()[:,2:].mean(1)
    torch.testing.assert_close(result['training_memorization'],expected_tm)
    torch.testing.assert_close(result['testing_generalization'],expected_tg)
    assert result['counterfactual_memorization'][1] < 0
    assert not result['counterfactual_memorization'].requires_grad
    assert not torch.allclose(result['training_memorization'],margins[:,:2].mean(1).sigmoid())
    membership[1]=torch.tensor([0,0,1,1],dtype=torch.bool)
    with pytest.raises(ValueError,match='user-level leakage'):
        counterfactual_memorization(margins,membership,users,train_runs=2,test_runs=2)


def test_memorization_requires_complete_run_manifest_and_counts():
    margins=torch.randn(2,25);membership=torch.ones(2,25,dtype=torch.bool)
    with pytest.raises(ValueError,match='in/out counts'):
        counterfactual_memorization(margins,membership,torch.tensor([0,1]))
    with pytest.raises(ValueError,match='complete'):
        counterfactual_memorization(margins[:,:24],membership[:,:24],torch.tensor([0,1]))


def test_self_bias_axis_orientation_ties_direction_and_peer_exclusion():
    scores=torch.tensor([[[9.,2.,3.],[2.,8.,2.],[3.,3.,7.]],[[9.,2.,3.],[3.,8.,1.],[3.,3.,7.]]])
    ranks=per_segment_ranks(scores,higher_is_better=True,tie_policy='average')
    # First role ranks target0 first, target1 worse than target2 on segment0.
    torch.testing.assert_close(ranks[0,:,0],torch.tensor([1.,3.,2.],dtype=torch.float64))
    torch.testing.assert_close(ranks[1,:,0],torch.tensor([1.,2.5,2.5],dtype=torch.float64))
    bias=self_bias(ranks)
    expected=torch.tensor([1-(3+2)/2,1-(2.75+3)/2,1-(2.25+2)/2],dtype=torch.float64)
    torch.testing.assert_close(bias,expected)
    assert not torch.allclose(bias,1-ranks.mean((0,2)))  # self excluded from peers
    torch.testing.assert_close(per_segment_ranks(-scores,higher_is_better=False,tie_policy='average'),ranks)
    with pytest.raises(ValueError): per_segment_ranks(scores,higher_is_better=True,tie_policy='unspecified')
    with pytest.raises(ValueError): self_bias(torch.ones(2,1,1))


@pytest.mark.parametrize('module',['scar_shapley_credit','probabilistic_autorater','rm_memorization_protocol','benchmark_self_bias'])
@pytest.mark.parametrize('seed',[42,43,44])
def test_diagnostics_are_finite_scalar_l1_not_capability(module,seed):
    result=importlib.import_module('auto_research.post_training.'+module).diagnostic(seed)
    assert result['seed'] == seed and result['diagnostic_only']
    assert all(type(v) is bool and v for v in result['checks'].values())
    assert all(type(v) in (int,float) and math.isfinite(v) for v in result['metrics'].values())
    assert result['metrics']['model_calls'] == 0


@pytest.mark.parametrize('paper,key,component',[
    ('2505.20417','scar-shapley-credit',True),('2510.00263','probabilistic-autorater',True),
    ('2607.24484','rm-memorization-protocol',True),('2509.26600','benchmark-self-bias',True),
    ('2601.12208','coreflect',False),('2605.12483','sparse-to-dense-reward-principle',False),
    ('2603.17070','cross-script-knowledge-transfer',False),('2606.24579','cross-lingual-exploration',False)])
def test_eight_reviewed_papers_keep_versions_cost_and_evidence_separate(paper,key,component):
    root=Path(__file__).resolve().parents[2]
    domain={'coreflect':'agent-research','cross-lingual-exploration':'foundation-models'}.get(key,'post-training')
    metadata=json.loads((root/f'src/auto_research/paper_specs/catalog/{domain}/{key}.json').read_text())
    assert metadata['domain'] == domain
    assert metadata['paper_url'] == f'https://arxiv.org/abs/{paper}v1'
    assert metadata['published_at'].endswith('Z') and metadata['published'] == metadata['published_at'][:10]
    assert metadata['reviewed_version_url'].endswith(paper+metadata['method_source_version'])
    assert metadata['first_author'] and metadata['first_author_affiliation']
    assert metadata['implementation_status'] == ('component_only' if component else 'deferred_high_cost')
    assert metadata['requires_gpu_validation'] is component
    assert metadata['full_experiment_status'] == 'not_reproduced_high_cost'
    assert metadata['review_done'] and metadata['full_experiment_review_done']
    assert not metadata['automatic_retry'] and not metadata['automatic_implementation_queue']
    assert not metadata['promotion_eligible'] and not metadata['evolve_integrated']
    folder=root/f'docs/{domain}/{paper}-{key}'
    text=(folder/'README.md').read_text()
    for literal in ['### 背景与主要改动','图片来自[原论文]','版权归原作者所有','## 论文信息','原作者代码','原作者代码许可','本地代码','成本过高，不复现（审查 DONE）']:
        assert literal in text
    provenance=json.loads((folder/'assets/provenance.json').read_text())
    png=(folder/'assets/paper-figure-01.png').read_bytes()
    assert png.startswith(b'\x89PNG\r\n\x1a\n') and hashlib.sha256(png).hexdigest() == provenance['sha256']
    assert provenance['visually_verified'] and provenance['paper_id'] == paper+metadata['method_source_version']
    if key == 'sparse-to-dense-reward-principle':
        assert metadata['author_order_randomized'] and metadata['first_author_source_version'] == 'v1_pdf_order_v5_affiliation'
    if component:
        assert metadata['gpu_validation_artifact'] == f'docs/gpu-validations/{key}-a100-20261025.json'
    else:
        assert 'local_operator' not in metadata and 'local_command' not in metadata
