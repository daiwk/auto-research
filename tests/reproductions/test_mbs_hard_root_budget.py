"""CPU budget fixtures only; not construction, capability or GPU evidence."""
import pytest

from auto_research.reproductions.magicbeanstalk.algorithm import MagicBeanStalk,Problem
from auto_research.reproductions.magicbeanstalk import checkpoint


class CalibrationFixture:
    def __init__(self,outcomes):
        self.outcomes=outcomes
        self.calls=[]
    def target_outcomes(self,problem):
        index=int(problem.question.rsplit("-",1)[1])
        self.calls.append(index)
        return self.outcomes[index]


def training_rows(count=16):
    return [{"question":f"training-question-{index}","answer":"EXTERNAL TRAIN GOLD"} for index in range(count)]


def test_only_first_four_verified_hard_roots_enter_tree_and_control_is_paired():
    outcomes=[([1,1],[False,False]),([0,0],[True,False])]+[([0,0],[False,False])]*14
    backend=CalibrationFixture(outcomes)
    class Builder:
        def __init__(self): self.calls=[]
        def construct(self,root,*,calibration):
            self.calls.append((root,calibration))
            # An unsuccessful tree cannot silently enter the seed-RL control.
            return None if root.question.endswith("-3") else Problem("actual fixture descendant of "+root.question,"2","trace")
    builder=Builder()
    synthetic,controls,audit=checkpoint.construct_paired_hard_roots(training_rows(),backend,builder,hard_root_limit=4)
    assert backend.calls==list(range(6))
    assert [root.question for root,_ in builder.calls]==[f"training-question-{i}" for i in (2,3,4,5)]
    assert len(synthetic)==len(controls)==3
    assert [root.question for root in controls]==[f"training-question-{i}" for i in (2,4,5)]
    assert audit["calibrated_training_candidates"]==6
    assert audit["tree_construction_attempts"]==4
    assert audit["paired_rl_root_indices"]==[2,4,5]


def test_no_eligible_seed_scans_only_the_real_training_prefix_without_tree():
    backend=CalibrationFixture([([0,0],[True,False])]*16)
    class NeverConstruct:
        def construct(self,*args,**kwargs):
            raise AssertionError("truncated zero-success outputs are not verified hard roots")
    synthetic,controls,audit=checkpoint.construct_paired_hard_roots(training_rows(),backend,NeverConstruct(),hard_root_limit=4)
    assert synthetic==controls==[]
    assert backend.calls==list(range(16))
    assert audit["tree_construction_attempts"]==0
    assert audit["verified_hard_roots_selected"]==0


@pytest.mark.parametrize("limit",[0,-1])
def test_hard_root_budget_requires_a_positive_explicit_limit(limit):
    with pytest.raises(ValueError):
        checkpoint.construct_paired_hard_roots(training_rows(),CalibrationFixture([]),None,hard_root_limit=limit)


@pytest.mark.parametrize("calibration",[([0,0],[True,False]),([1,0],[False,False])])
def test_reused_calibration_never_bypasses_normal_completion_or_zero_success(calibration):
    class NeverDecompose:
        def target_outcomes(self,*args):
            raise AssertionError("provided actual calibration must not be sampled or charged twice")
        def verify(self,*args):
            raise AssertionError("not a verified hard root")
    builder=MagicBeanStalk(NeverDecompose())
    assert builder.construct(Problem("root","7",""),calibration=calibration) is None
    assert builder.audit[0]["accepted"] is False


@pytest.mark.parametrize("calibration",[([],[]),([0,0],[False]),([0,.5],[False,False]),([0,0],[0,False])])
def test_invalid_precalibration_cannot_be_promoted_to_verified_hard_root(calibration):
    builder=MagicBeanStalk(None)
    with pytest.raises(ValueError):
        builder.construct(Problem("root","7",""),calibration=calibration)
