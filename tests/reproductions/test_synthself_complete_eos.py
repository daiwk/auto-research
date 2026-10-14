"""Full-response sequence-NLL token contracts; no alignment capability claim."""
import pytest

from auto_research.reproductions.synthself.algorithm import complete_response_tokens,naturally_complete_response


def test_gold_and_generated_rewrite_each_end_in_eos_exactly_once():
    assert complete_response_tokens((1,2),eos_token_id=99)==(1,2,99)
    assert complete_response_tokens((1,2,99),eos_token_id=99)==(1,2,99)
    assert complete_response_tokens((1,2,99,99),eos_token_id=99)==(1,2,99)
    assert complete_response_tokens((),eos_token_id=0)==(0,)


def test_internal_eos_cannot_silently_discard_following_response_tokens():
    with pytest.raises(ValueError,match="internal EOS"):
        complete_response_tokens((1,99,2),eos_token_id=99)


@pytest.mark.parametrize("eos",[None,-1,True])
def test_explicit_valid_eos_identity_is_required(eos):
    with pytest.raises(ValueError):
        complete_response_tokens((1,2),eos_token_id=eos)


def test_truncation_and_missing_native_eos_cannot_become_complete_evidence():
    assert naturally_complete_response((1,99),truncated=False,eos_token_id=99)
    assert not naturally_complete_response((1,99),truncated=True,eos_token_id=99)
    assert not naturally_complete_response((1,),truncated=False,eos_token_id=99)
    assert not naturally_complete_response((1,99,99),truncated=False,eos_token_id=99)


@pytest.mark.parametrize("partial_truncated",[True,False])
def test_apparently_better_partial_nll_blocks_selection_and_every_sft_update(monkeypatch,partial_truncated):
    from types import SimpleNamespace
    import torch
    from auto_research.post_training.response_policy import GeneratedResponse
    from auto_research.post_training.oct13_common import ExecutionFailure
    from auto_research.reproductions.synthself import checkpoint
    class Policy:
        device="cpu"
        vocabulary_sha256="unit-fixture"
        provenance={"kind":"unit-fixture-not-capability"}
        def __init__(self,role):
            self.role=role
            self.calls=0
            self.model=torch.nn.Linear(1,2 if role=="teacher" else 1)
            self.tokenizer=lambda *args,**kwargs:SimpleNamespace(input_ids=[1,1,1,1])
            self.tokenizer.eos_token_id=0
        def generate(self,messages,**kwargs):
            self.calls+=1
            if self.role=="teacher" and self.calls==1:
                return [GeneratedResponse((1,0),"\\boxed{97}",False)]
            return [GeneratedResponse((1,),"\\boxed{97}",partial_truncated if self.role=="teacher" else True)]
        def token_statistics(self,messages,tokens):
            return torch.full((len(tokens),),-2.),None
        def prepare_lora(self,**kwargs):
            raise AssertionError("incomplete aligner cannot execute any SFT")
    monkeypatch.setattr(checkpoint,"load_policy",lambda config,role="student",seed=42:Policy(role))
    rows=[{"question":"public training question "+str(i),"answer":"97"} for i in range(2)]
    monkeypatch.setattr(checkpoint,"load_split",lambda config:(rows,rows,{"verified":True}))
    with pytest.raises(ExecutionFailure) as failure:
        checkpoint.run({"student_id":"Qwen/Qwen2.5-0.5B","teacher_id":"Qwen/Qwen2.5-7B","device":"cpu","max_tokens":8})
    evidence=failure.value.evidence
    empirical=evidence["empirical_aligner_constraints"]
    assert empirical["diagnostic_bounded_rewrite_sequence_or_partial_nll"]<empirical["gold_sequence_nll"]
    assert empirical["aligner_quality"]>empirical["self_quality"]==0.
    assert empirical["rewrite_sequence_nll"] is None and empirical["satisfied"] is False
    assert empirical["selection_blocked_by_incomplete_outputs"] is True
    partial=evidence["rewrites"][1]
    assert partial["rewrite_scored_tokens"]==partial["tokens"]==1
    assert partial["rewrite_scored_eos_count"]==0 and partial["rewrite_canonical_eos_appended"] is False
    assert all(row["self_response_truncated"] and not row["self_natural_completion"] for row in evidence["rewrites"])
