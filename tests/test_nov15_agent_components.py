"""Exact local mechanisms; these tests never measure agent capability."""
import math

import pytest
import torch

from auto_research.agent_research import ace_rl as ace
from auto_research.agent_research import caplite as cap
from auto_research.agent_research import coremem as mem


def outcome(arm='no_memory',resolved=False,steps=100,progress=1.,state='commit:a'):
    return mem.ReplayOutcome('boundary:1',state,arm,resolved,steps,progress)


def test_coremem_success_always_beats_any_failure_and_pairs_reject_state_drift():
    assert mem.success_first_reward(outcome(resolved=True,steps=100),max_steps=100) == 150.
    assert mem.success_first_reward(outcome(),max_steps=100) == 50.
    assert mem.paired_step_saving(outcome(steps=100),outcome('own_memory',steps=60)) == 40
    with pytest.raises(ValueError,match='identical inherited'):
        mem.paired_step_saving(outcome(),outcome('own_memory',state='commit:b'))
    with pytest.raises(ValueError,match='W >'):
        mem.success_first_reward(outcome(),max_steps=200,win=250.,alpha=50.)
    with pytest.raises(ValueError):
        mem.success_first_reward(outcome(steps=101),max_steps=100)


def test_coremem_first_use_is_not_anchor_repetition_or_counterfactual_reach():
    assert mem.provenance_gates([{'old'},{'counter'},{'new'},{'new'},{'late'}],
                               {'old','counter','new','late'},{'old'},[[{'counter'}]*8+[{'late'}]]) == (False,False,True,False,True)
    with pytest.raises(ValueError):
        mem.provenance_gates([{'x'}], 'x', [], [])


def test_coremem_fixed_scale_not_std_and_all_step_credit_not_erased():
    rewards=torch.tensor([10.,30.,50.,70.,0.],requires_grad=True)
    arms=('no_memory','no_memory','own_memory','own_memory','misplaced')
    gates=torch.tensor([[False,False],[False,False],[True,False],[False,False],[False,False]])
    valid=torch.ones_like(gates)
    adv,value=mem.step_advantages(rewards,arms,gates,valid)
    assert value.item() == 40.
    torch.testing.assert_close(adv,torch.tensor([[-.1,-.1],[.1,.1],[.3,-.1],[.1,.1],[-.2,-.2]]))
    assert not adv.requires_grad


def test_coremem_explicit_reduction_reference_kl_and_padding_gradient():
    logs=torch.full((2,3),-1.,requires_grad=True)
    adv=torch.tensor([[1.],[3.]],requires_grad=True)
    steps=torch.tensor([[0,-1,-1],[0,0,0]])
    mask=torch.tensor([[True,False,False],[True,True,True]])
    token=mem.policy_gradient_loss(logs,adv,steps,mask,beta=0.)
    session=mem.policy_gradient_loss(logs,adv,steps,mask,beta=0.,reduction='session_mean')
    assert token.item() == 2.5 and session.item() == 2.
    token.backward()
    assert logs.grad[0].tolist() == [-.25,0.,0.] and adv.grad is None
    with pytest.raises(ValueError,match='reference KL'):
        mem.policy_gradient_loss(logs,adv,steps,mask)
    kl=torch.full_like(logs,.5,requires_grad=True)
    assert mem.policy_gradient_loss(logs,adv,steps,mask,reference_kl=kl).item() == pytest.approx(2.6)


def sample(identity,role='actor',task='q',seed='s',reflection='',reward=.5):
    return ace.RoleSample(identity,role,task,seed,reflection,reward)


def test_ace_role_provenance_threshold_fractional_singleton_and_range_filter():
    rows=[sample('a',seed='s1',reward=0.),sample('b',seed='s2',reward=1.),
          sample('c','curator',reflection='z',reward=.5),
          sample('d','reflector',task='other',reward=.5),sample('e','reflector',task='other',reward=.5)]
    result=ace.role_advantages(rows)
    assert result['a'] == pytest.approx(-1.,rel=1e-5) and result['b'] == pytest.approx(1.,rel=1e-5)
    assert result['c'] == .5 and result['d'] == result['e'] == 0.
    assert set(ace.role_advantages(rows,filter_mode='range')) == {'a','b'}
    assert ace.role_advantages([sample('only',reward=1.)]) == {}
    assert ace.reflection_reward([]) == 0.
    assert ace.reflection_reward([.2,.8]) == .5


def test_ace_apply_admissibility_token_budget_and_stable_ids():
    # Explicit token IDs model a supplied tokenizer, not a claim about real text.
    tokenize=lambda text: [1]*len(text.split())
    book=('a','b')
    assert ace.apply_edits(book,[ace.Edit('REMOVE',bullet_id=0),ace.Edit('UPDATE','c',1)],tokenize=tokenize) == ('c',)
    assert ace.apply_edits(book,[ace.Edit('UPDATE','a',0)],tokenize=tokenize) is None
    assert ace.apply_edits(book,[ace.Edit('REMOVE',bullet_id=5)],tokenize=tokenize) is None
    assert ace.apply_edits(book,[ace.Edit('ADD','b')],tokenize=tokenize) is None
    assert ace.apply_edits(book,[ace.Edit('ADD','c')],tokenize=tokenize,max_tokens=1) is None
    with pytest.raises(ValueError,match='token IDs'):
        ace.apply_edits(book,[ace.Edit('ADD','c')],tokenize=lambda t:'not IDs')


def test_ace_retention_is_separate_from_credit_and_reset_is_per_task():
    store=ace.PlaybookStore(seed=42)
    store.begin('q');store.begin('other')
    assert store.retain('q',.8,[(('bad',),.5)]) == ()
    assert store.retain('q',.8,[(('good',),.8)]) == ('good',)
    assert store.begin('q') == ('good',)
    assert store.begin('q') == ()
    assert store.begin('other') == ()


def test_ace_asymmetric_dualclip_and_token_mean_with_detached_targets():
    ratios=torch.tensor([[1.5,1.],[4.,1.]])
    old=torch.full((2,2),-2.,requires_grad=True)
    new=(old.detach()+ratios.log()).requires_grad_()
    advantages=torch.tensor([1.,-1.],requires_grad=True)
    mask=torch.tensor([[True,True],[True,False]])
    loss=ace.joint_policy_loss(new,old,advantages,mask)
    assert loss.item() == pytest.approx(-(1.28+1.-3.)/3)
    loss.backward()
    assert old.grad is None and advantages.grad is None
    assert new.grad[0,0] == new.grad[1,0] == new.grad[1,1] == 0.
    assert new.grad[0,1].item() == pytest.approx(-1/3)


def schema():
    return {'type':'object','properties':{'recipient':{'type':'string'},'amount':{'type':'integer'},'body':{'type':'string'},'date':{'type':'string'},'enabled':{'type':'boolean'}},'required':['recipient','amount']}


def test_caplite_schema_authority_and_grounding_are_exact_not_substrings():
    policy=cap.ToolPolicy('send_money','Send money',schema())
    assert policy.operation == 'write'
    assert policy.kinds == {'recipient':'authority','amount':'authority','body':'payload','date':'temporal','enabled':'control'}
    grounding=cap.grounding_set('Send 100 to alice@example.com on 2026-11-15 with "hello world"')
    assert cap.canonical(1) not in grounding and cap.canonical(100) in grounding
    assert cap.canonical('HELLO   WORLD') in grounding
    assert policy.permits({'recipient':'alice@example.com','amount':100,'body':'malicious prose'},grounding)
    assert not policy.permits({'recipient':'evil@example.com','amount':100},grounding)
    assert not policy.permits({'recipient':'alice@example.com','amount':True},grounding)
    assert not policy.permits({'recipient':'alice@example.com','amount':100,'unknown':'x'},grounding)
    assert policy.permits({'recipient':'evil@example.com','amount':100},grounding,confirmed=['evil@example.com'])


def test_caplite_read_destinations_unknown_verbs_and_schema_snapshot():
    source={'type':'object','properties':{'url':{'type':'string'}},'required':['url']}
    policy=cap.ToolPolicy('fetch_url','Fetch a URL',source)
    source['properties']['url']['type']='boolean'
    assert policy.permits({'url':'https://example.com'},cap.grounding_set('Read https://example.com'))
    assert not policy.permits({'url':'https://evil.example'},cap.grounding_set('Read https://example.com'))
    assert cap.ToolPolicy('get_report','Write a report',source).operation == 'write'
    assert cap.ToolPolicy('calculate','Compute',source).operation == 'unknown'
    with pytest.raises(ValueError,match='unsupported schema'):
        cap.ToolPolicy('send','Send',{'type':'object','properties':{'arg':{'type':'object'}}})


def test_caplite_candidate_ids_and_prefix_stop_deny_reorder_and_tool_error():
    policy=cap.ToolPolicy('send','Send money',schema())
    grounded=cap.grounding_set('Send 100 to alice@example.com')
    rows=[cap.Candidate('a','alice@example.com','tool:a'),cap.Candidate('b','evil@example.com','tool:b')]
    assert [r.identity for r in policy.bind_candidates('recipient',rows,grounded)] == ['a']
    assert policy.bind_candidates('enabled',[cap.Candidate('yes',True,'tool:b')],grounded) == ()
    slots={'recipient':cap.Placeholder('r'),'amount':100}
    plan=cap.CommittedWrites('Send 100 to alice@example.com',[('send',slots),('send',slots)],{'send':policy})
    assert not plan.execute_next('other',{'recipient':'alice@example.com','amount':100},execute=lambda *a:None)
    assert plan.stopped and plan.executed_count == 0
    assert not plan.execute_next('send',{'recipient':'alice@example.com','amount':100},execute=lambda *a:None)
    plan=cap.CommittedWrites('Send 100 to alice@example.com',[('send',slots)],{'send':policy})
    def fail(*args):
        raise RuntimeError('real tool error')
    with pytest.raises(RuntimeError):
        plan.execute_next('send',{'recipient':'alice@example.com','amount':100},execute=fail)
    assert plan.stopped and plan.executed_count == 0


@pytest.mark.parametrize('module',[mem,ace,cap])
@pytest.mark.parametrize('seed',[42,43,44])
def test_diagnostics_never_claim_agent_capability(module,seed):
    result=module.diagnostic(seed)
    assert result['diagnostic_only'] is True and result['evaluation_tier'] == 'l1_mechanism'
    assert all(type(value) is bool and value for value in result['checks'].values())
    assert all(isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value) for value in result['metrics'].values())
    if not module.REQUIRES_GPU_VALIDATION:
        with pytest.raises(ValueError):
            module.diagnostic(seed,'cuda')
