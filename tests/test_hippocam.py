from auto_research.agent_research.hippocam import CapacityExhausted, Hippocam
import pytest


def memory(**kwargs):
    return Hippocam(str.split, lambda *args: "Narrative: done. Knowledge: verified.",
                    min_saving=3, minimum_tail=2, rounds=1, **kwargs)


def test_nested_closures_exclude_new_response_and_recall_is_one_layer():
    m = memory()
    m.janus(open_intents=(("root", "finish"), ("sub", "verified")), guidance="begin root and sub")
    m.append("assistant", "old work evidence with concrete result", round_id="r1")
    m.complete_round("r1")
    m.janus(close=1, guidance="sub complete")
    new_id = m.append("assistant", "new independent work", round_id="r2", complete=False)
    m.after_response()
    summary = next(x for x in m.context if x.direct_intent)
    assert new_id not in {x.identifier for x in m.recall(summary.identifier)}
    assert m.context[-1].identifier == new_id
    assert len(m.intents) == 1


def test_pressure_protects_complete_exchanges_and_fails_closed():
    m = memory(capacity=30)
    m.append("user", "old " * 40)
    m.append("assistant", "calling tool " * 3, round_id="r1", complete=False)
    m.append("tool", "tool answer " * 3, round_id="r1", complete=False)
    m.complete_round("r1")
    m.pressure_control()
    assert [x.role for x in m.context[-2:]] == ["assistant", "tool"]
    assert m.archive
    m.append("assistant", "unfinished " * 50, round_id="r2", complete=False)
    with pytest.raises(CapacityExhausted):
        m.pressure_control()


def test_failed_summary_does_not_delete_original():
    m = Hippocam(str.split, lambda *args: "verbose " * 50,
                 capacity=20, rounds=1, minimum_tail=0, min_saving=3)
    old = m.append("user", "data " * 30)
    with pytest.raises(CapacityExhausted):
        m.pressure_control()
    assert m.context[0].identifier == old and not m.archive


def test_close_hook_never_archives_partial_exchange():
    m = memory()
    m.janus(open_intents=(("inspect", "done"),), guidance="begin inspect")
    user = m.append("user", "new request", round_id="r", complete=False)
    m.append("assistant", "call tool", round_id="r", complete=False)
    m.janus(close=1, guidance="inspection finished")
    m.append("assistant", "new work")
    m.after_response()
    assert user in {x.identifier for x in m.context}
    assert all(user not in {x.identifier for x in children} for children in m.archive.values())
