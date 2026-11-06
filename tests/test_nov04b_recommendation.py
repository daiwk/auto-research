"""Paper-specific CPU contracts, not retrieval or slate-quality benchmarks."""
import math

import pytest

from auto_research.reproductions.reusegr_components import (
    ClickRow, cache_route, composite_score, label_reuse_depth, wilson_lower,
)
from auto_research.reproductions.spade_components import (
    Beam, merge_pair, oa_pair_scores, sdbs_step, sigmoid_bonus,
)
from auto_research.reproductions.onetrans_gsr_components import (
    Candidate, TagRule, business_logits, geometric_reward, separate_advantages,
)


def test_reusegr_whole_row_leave_out_and_row_macro():
    rows=[ClickRow('a',(1,1,1,1),100),ClickRow('b',(2,2,2,2),1)]
    result=label_reuse_depth(rows,top_n=1,min_rows=2)
    # Removing a means removing all 100 clicks, not just one repeated click.
    assert result.coverages==(0.,0.,0.)
    assert result.depth==0 and result.known


def test_reusegr_all_ancestors_must_pass_and_unknown_is_not_cache_miss():
    rows=[ClickRow(str(i),(1,1,i,i),1) for i in range(8)]
    result=label_reuse_depth(rows,top_n=2)
    assert result.depth==2
    assert result.lower_bounds[0]>=.4 and result.lower_bounds[1]>=.4
    assert result.lower_bounds[2]<.4
    assert label_reuse_depth(rows[:4]).known is False
    assert cache_route(True,0)=='prepared_root'
    assert cache_route(False,0)=='cold_e2e'
    assert cache_route(True,2)=='prepared_prefix'
    assert composite_score(-2.,[-.5,-.25])==-2.75
    assert wilson_lower(0,8)==0.
    assert wilson_lower(8,8)==pytest.approx(.6755843804891231)


def test_reusegr_cannot_skip_failed_shallow_level_when_deeper_level_passes():
    rows=[ClickRow('a',(1,1,1,1),50),ClickRow('b',(1,2,2,2),50)]
    rows += [ClickRow(str(i),(0,0,0,i),10) for i in range(6)]
    result=label_reuse_depth(rows,top_n=1)
    assert result.lower_bounds[0]==0.
    assert result.lower_bounds[1]>.4
    assert result.depth==0


def test_oa_bpe_counts_adjacent_occurrences_and_reduces_to_unweighted():
    corpus=[('a','a','a'),('b','c')]
    assert oa_pair_scores(corpus,[1.,1.])=={('a','a'):2.,('b','c'):1.}
    assert oa_pair_scores(corpus,[1.,3.])[('b','c')]==3.
    assert merge_pair(('a','a','a'),('a','a'))==('aa','a')
    # A merge is non-overlapping even though scoring counted both occurrences.
    with pytest.raises(ValueError):oa_pair_scores(corpus,[1.,-1.])


def test_sdbs_adds_bonus_per_parent_rank_not_child_token_overlap():
    assert sigmoid_bonus(0)==0.
    bonuses=[sigmoid_bonus(rank) for rank in range(10)]
    assert all(a<b for a,b in zip(bonuses,bonuses[1:]))
    assert all(bonuses[i+1]-bonuses[i]>=bonuses[i+2]-bonuses[i+1] for i in range(8))
    assert bonuses[-1]<.2
    beams=[Beam(('A',),0.),Beam(('B',),-.01)]
    next_tokens=[[('x',-.1),('y',-.2)],[('x',-.1),('y',-.2)]]
    result=sdbs_step(beams,next_tokens,beam_size=2)
    assert result[0].tokens==('B','x')  # top parent is unbonused, not guaranteed to remain top
    assert sdbs_step(beams,next_tokens,beam_size=2,beta=0)[0].tokens==('A','x')
    with pytest.raises(ValueError):sigmoid_bonus(1,gamma=2.)


def test_onetrans_hard_mask_finite_soft_penalty_and_noncompletion_guarantee():
    candidates=[Candidate('p',frozenset({'ad'})),Candidate('q',frozenset()),Candidate('r',frozenset())]
    # In the next slot, an untagged candidate makes the window minimum unreachable.
    rule=TagRule('ad',window=2,minimum=1,maximum=1)
    scores=business_logits(candidates,[0.,0.,0.],['q'],[rule],{'ad':1})
    assert scores[1]==-math.inf  # selected item cannot be repeated
    assert scores[2]==-.1       # quota is a finite adjustment, not a mandatory mask
    assert scores[0]==0.
    hard=TagRule('ad',window=2,minimum=1,maximum=1,mandatory=True)
    hard_scores=business_logits(candidates,[0.,0.,0.],['q'],[hard],{'ad':1})
    assert hard_scores[2]==-math.inf
    with pytest.raises(ValueError,match='unmasked'):
        business_logits(candidates,[0.,0.,0.],['p','q','r'],[],{})


def test_onetrans_group_constant_geometric_floor_and_separate_standardization():
    # Equal objective weights, exact per-request range normalization and positive floor.
    rewards=geometric_reward([[1.,5.],[2.,5.],[3.,5.]],[.5,.5])
    assert rewards[0]==pytest.approx(1e-4)
    assert rewards[-1]==pytest.approx(math.sqrt(1e-4*2/(2+1e-8)))
    advantages=separate_advantages([2.,2.,2.],[0.,1.,2.],rule_weight=.1)
    assert advantages[1]==0.
    assert advantages[0]<0<advantages[2]
    with pytest.raises(ValueError):geometric_reward([[1.],[2.]],[0.])
    with pytest.raises(ValueError,match='overflows'):
        geometric_reward([[-1e308],[1e308]],[1.])


def test_onetrans_iterator_rules_cannot_skip_masks_after_first_candidate():
    candidates=[Candidate('adA',frozenset({'ad'})),Candidate('adB',frozenset({'ad'})),Candidate('organic',frozenset())]
    rule=TagRule('ad',1,0,0,mandatory=True)
    expected=(-math.inf,-math.inf,0.)
    for rules in ([rule],(rule,),iter([rule])):
        assert business_logits(candidates,[0.,0.,0.],[],rules,{'ad':2})==expected


@pytest.mark.parametrize('module',['reusegr_components','spade_components','onetrans_gsr_components'])
def test_small_cpu_diagnostic_has_actual_checks_without_capability_claim(module):
    from importlib import import_module
    result=import_module('auto_research.reproductions.'+module).diagnostic(42)
    assert result['diagnostic_only'] and result['evaluation_tier']=='l1_mechanism'
    assert result['seed']==42 and all(result['checks'].values())
    assert result['metrics'] and all(math.isfinite(value) for value in result['metrics'].values())
