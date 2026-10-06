"""Paper-mechanism contracts for DepGPO's recorded-trace credit operator."""

import pytest

from auto_research.agent_research.depgpo import (
    WHOLE_FILE,
    CommandTrace,
    assign_dependency_credit,
)


def credit(commands, *, files=None, tokens=(1, 1, 1), advantage=0.8):
    return assign_dependency_credit(
        commands,
        verifier_files=set(files or {"/answer"}),
        token_counts=tokens,
        group_advantage=advantage,
    )


def test_supporting_read_and_indirect_write_receive_credit():
    result = credit([
        CommandTrace("read", 0),
        CommandTrace("stage", 1, written_records=(("/staging", 1),),
                     stdout_source_ids=("read",)),
        CommandTrace("answer", 2, read_files=("/staging",),
                     written_records=(("/answer", 1),)),
    ])
    assert result.command_credit == {"stage": 1.0, "answer": 1.0, "read": 0.75}
    assert result.step_credit == (0.75, 1.0, 1.0)
    assert result.step_factor == pytest.approx((0.0, 1.5, 1.5))
    assert sum(result.token_weight) / 3 == pytest.approx(1.0)
    assert sum(result.redistributed_advantage) / 3 == pytest.approx(0.8)
    assert not result.fallback


def test_overwritten_answer_gets_no_credit_without_read_dependency():
    result = credit([
        CommandTrace("old", 0, written_records=(("/answer", 1),)),
        CommandTrace("replacement", 1, written_records=(("/answer", 1),)),
        CommandTrace("postread", 2, read_files=("/answer",)),
    ])
    assert result.command_credit == {"old": 0.0, "replacement": 1.0, "postread": 0.0}
    assert result.step_factor == pytest.approx((0.0, 3.0, 0.0))


def test_multi_record_fraction_and_shortest_path_once():
    result = credit([
        CommandTrace("reader", 0),
        CommandTrace("writer", 1, written_records=(("/answer", 1), ("/noise", 1)),
                     stdout_source_ids=("reader",)),
        CommandTrace("unused", 2, stdout_source_ids=("reader",)),
    ])
    assert result.command_credit["writer"] == 0.5
    assert result.command_credit["reader"] == 0.25


def test_read_requires_observed_information_flow_and_same_file_edit_is_not_indirect():
    result = credit([
        CommandTrace("read", 0, read_files=("/other",)),
        CommandTrace("stage", 1, written_records=(("/staging", 1),)),
        CommandTrace("replace", 2, read_files=("/staging",),
                     written_records=(("/staging", 1), ("/answer", 1))),
    ])
    assert result.command_credit["read"] == 0.0
    assert result.command_credit["stage"] == 0.0
    assert result.command_credit["replace"] == 0.5


def test_fallback_and_length_normalization_preserve_signed_mean():
    result = credit([
        CommandTrace("irrelevant", 0, written_records=(("/other", WHOLE_FILE),)),
    ], tokens=(2, 8, 1), advantage=-0.4)
    assert result.fallback
    assert result.token_weight == (1.0, 1.0, 1.0)
    assert result.redistributed_advantage == (-0.4, -0.4, -0.4)

    result = credit([
        CommandTrace("writer", 0, written_records=(("/answer", 1),)),
        CommandTrace("reader", 1),
    ], tokens=(2, 8, 1), advantage=-0.4)
    assert not result.fallback
    assert sum(n * w for n, w in zip((2, 8, 1), result.token_weight)) / 11 == pytest.approx(1)
    assert all(value <= 0 for value in result.redistributed_advantage)


def test_invalid_trace_rejected():
    with pytest.raises(ValueError, match="earlier command"):
        credit([CommandTrace("read", 0, stdout_source_ids=("unknown",))])
    with pytest.raises(ValueError, match="unique"):
        credit([CommandTrace("same", 0), CommandTrace("same", 1)])
    with pytest.raises(ValueError, match="step"):
        credit([CommandTrace("late", 4)])
