"""Paper-specific numerical/control checks, never model-capability tests."""
import math

import pytest
import torch

from auto_research.agent_research import clarification_sgp as sgp
from auto_research.agent_research import co_director as co
from auto_research.agent_research import instruct_to_act as ita
from auto_research.agent_research import mt_pingeval as ping
from auto_research.agent_research import policybank as pb
from auto_research.post_training import maple_icl as maple
from auto_research.post_training import social_meta_learning as sml


def rollout(identity, interpretation, accuracy, actions=("answer",), overlap=1., words=0):
    return sgp.Rollout(identity, interpretation, actions, accuracy, words, overlap)


def test_sgp_interpretation_means_not_sample_frequency_or_lucky_max():
    rows = [rollout("a", "i", 1.), rollout("b", "i", 1.), rollout("c", "j", 0.),
            rollout("d", "i", .7, ("multi_answer",)), rollout("e", "j", .7, ("multi_answer",))]
    result = sgp.select_rollouts(rows, ("i","j"), alpha=0., beta=0., minimum_accuracy=0.)
    assert result["action_sequence"] == ("multi_answer",)
    assert result["sequence_rewards"][("answer",)] == 50.
    assert [r.identity for r in result["selected"]] == ["d","e"]


def test_sgp_invalid_filter_and_missing_coverage_are_not_fabricated():
    rows = [rollout("a", "i", .9, overlap=.49), rollout("b", "j", .09)]
    with pytest.raises(ValueError, match="covers"):
        sgp.select_rollouts(rows, ("i","j"), alpha=0., beta=0., minimum_accuracy=.1)
    assert sgp.reward(rollout("x","i",1.,("clarify","answer"),words=3), .1,.2) == pytest.approx(99.3)


@pytest.mark.parametrize("actions", [("clarify","clarify","answer"), ([],), "answer"])
def test_sgp_sequence_validation(actions):
    with pytest.raises(ValueError):
        rollout("x","i",1.,actions)


def test_sml_success_and_student_masks_have_exact_gradient_boundary():
    logits = torch.randn(2,3,4,requires_grad=True)
    targets = torch.tensor([[0,1,2],[1,2,3]])
    mask = torch.tensor([[True,False,True],[True,True,True]])
    success = torch.tensor([True,False])
    loss = sml.successful_student_loss(logits,targets,mask,success)
    expected = torch.nn.functional.cross_entropy(logits[0,[0,2]],targets[0,[0,2]])
    assert torch.equal(loss, expected)
    loss.backward()
    assert torch.count_nonzero(logits.grad[1]) == 0
    assert torch.count_nonzero(logits.grad[0,1]) == 0
    assert torch.count_nonzero(logits.grad[0,0]) > 0
    assert sml.q_priming_probability(3,incorrect=True) == .75**3
    assert sml.q_priming_probability(0,incorrect=False) == 0.


def test_sml_no_success_is_not_fake_zero_training():
    with pytest.raises(ValueError,match="no successful"):
        sml.successful_student_loss(torch.zeros(1,2,3),torch.zeros(1,2,dtype=torch.long),
                                    torch.ones(1,2,dtype=torch.bool),torch.tensor([False]))


@pytest.mark.parametrize("turn,incorrect", [(-1,True),(True,True),(1,1)])
def test_sml_priming_type_contract(turn,incorrect):
    with pytest.raises(ValueError):
        sml.q_priming_probability(turn,incorrect=incorrect)


def test_maple_categorical_not_euclidean_distance_and_stable_ties():
    schema = {"length":(50.,100.,1000.),"area":("x","y")}
    rows = [maple.Donation("a",{"length":50.,"area":"x"},"a","consent:a"),
            maple.Donation("b",{"length":1000.,"area":"x"},"b","consent:b"),
            maple.Donation("c",{"length":100.,"area":"y"},"c","consent:c")]
    result = maple.select_examples({"length":100.,"area":"x"},rows,schema,k=2)
    assert [(r.identity,d) for r,d in result] == [("a",1),("b",1)]
    assert result[0][0] is rows[0]
    with pytest.raises(ValueError,match="categorical"):
        maple.select_examples({"length":51.,"area":"x"},rows,schema)
    with pytest.raises(ValueError):
        maple.select_examples({"length":50.},rows,schema)


def capability(identity="cancel",eligibility="rule"):
    return pb.Capability(identity,"cancel_tool","header","trigger","verify",eligibility,"action","insight")


def test_policybank_two_stage_retrieval_and_explicit_feedback_revisions():
    first, second = capability(),capability(eligibility="new external rule")
    bank = pb.PolicyBank([first])
    assert bank.headers() == (("cancel","cancel_tool","header"),)
    assert bank.retrieve([]) == ()
    bank.apply_after_task(pb.Change("revise",second,"trace:1","feedback:1"))
    assert bank.retrieve(["cancel"]) == (second,)
    bank.apply_after_task(pb.Change("omit",None,"trace:2","feedback:2"))
    assert len(bank.headers()) == 1 and len(bank.changes) == 2
    with pytest.raises(ValueError):
        bank.apply_after_task(pb.Change("add",second,"trace:3","feedback:3"))
    with pytest.raises(ValueError):
        bank.apply_after_task(pb.Change("revise",capability("other"),"trace:3","feedback:3"))
    with pytest.raises(ValueError):
        bank.retrieve(["missing"])


def test_ping_private_views_full_record_scoring_and_unique_intersection():
    shared=("a","b","c","d","e")
    similar=("a","b","different","d","e")
    other=("z","b","c","d","e")
    game=ping.NameGame([shared,similar],[other,shared])
    assert game.view("alice").records == (shared,similar)
    assert not hasattr(game.view("alice"),"gold")
    assert not game.score_selection("alice",row_number=2)
    assert game.score_selection("bob",row_number=2)
    with pytest.raises(ValueError):
        ping.NameGame([shared,similar],[shared,similar])
    with pytest.raises(ValueError):
        ping.NameGame(["abcde"],[shared])


def test_ping_budget_actual_token_ids_and_upper_limits():
    budget=ping.IsotokenBudget(tokens_per_player=128,total_turns=16)
    assert budget.per_turn == 16
    for turn in range(16):
        assert len(budget.submit("alice" if turn%2==0 else "bob",list(range(100)))) == 16
    assert budget.used == {"alice":128,"bob":128}
    with pytest.raises(ValueError):
        budget.submit("alice",[1])
    with pytest.raises(ValueError):
        ping.IsotokenBudget(total_turns=3)


def test_codirector_factored_updates_and_actual_ucb_after_all_arms_tried():
    bandit=co.FactoredUCB(seed=42,exploration=2.)
    for index in range(4):
        choices=(co.AXES["strategy"][index%3],co.AXES["narrative"][index%3],co.AXES["aesthetic"][index])
        bandit.update(co.VideoEvaluation(str(index),choices,(10.*index,20.*index,30.*index),100.-index))
    stats=bandit.statistics()
    # Strategy index2 has mean20 and one pull, beating index0 mean15/two pulls.
    assert bandit.select()[0] == co.AXES["strategy"][2]
    assert stats["strategy"][co.AXES["strategy"][0]]["pulls"] == 2
    assert bandit.best_video().identity == "0"
    with pytest.raises(ValueError):
        bandit.update(co.VideoEvaluation("0",choices,(0.,0.,0.),0.))


def test_instruct_intervals_and_exact_losses_not_dreamer_substitute():
    labels, ends=ita.interval_labels(5,[(0,1),(3,4)])
    assert labels == (True,True,False,True,True)
    assert ends == (False,True,False,False,True)
    with pytest.raises(ValueError):
        ita.interval_labels(5,[(0,2),(2,3)])
    logs=torch.full((1,3),-math.log(2),requires_grad=True)
    stop=torch.zeros((1,3),requires_grad=True)
    loss=ita.instruction_losses(logs,stop,torch.tensor([[True,True,False]]),
                                torch.tensor([[False,True,False]]),torch.tensor([[True,True,True]]),bc_weight=.5)
    assert loss["bc"].item() == pytest.approx(math.log(2))
    assert loss["stop"].item() == pytest.approx(3*math.log(2))
    loss["total"].backward()
    assert logs.grad.tolist() == [[-.5,-.5,0.]]
    assert stop.grad[0,2] > 0


@pytest.mark.parametrize("module", [sgp,sml,maple,pb,ping,co,ita])
@pytest.mark.parametrize("seed", [42,43,44])
def test_all_diagnostics_are_finite_mechanism_checks(module,seed):
    result=module.diagnostic(seed)
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == ("l0_interface" if module is pb else "l1_mechanism")
    assert all(type(x) is bool and x for x in result["checks"].values())
    assert all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in result["metrics"].values())
    if not module.REQUIRES_GPU_VALIDATION:
        with pytest.raises(ValueError):
            module.diagnostic(seed,"cuda")
