import numpy as np
import pytest

from auto_research.agent_research.ontrack import Event, MonitorConfig, OnTrackMonitor, PrefixGraph, Reference, ToolContract
from auto_research.agent_research.ontrack_transport import CouplingState


WORDS = ["search", "read", "edit", "test", "commit", "weather", "args", "output", "error"]


def embed(texts):
    # Synthetic embeddings are for binary mechanism tests, never public metrics.
    return np.array([np.eye(len(WORDS))[WORDS.index(t or "output")] for t in texts])


def reference(provenance="mined"):
    return Reference((Event("search", "search", "args", "output", produces=("file",)),
                      Event("edit", "edit", "args", "output", parents=(0,), consumes=("file",), produces=("patch",)),
                      Event("test", "test", "args", "output", parents=(1,), consumes=("patch",), produces=("passed",)),
                      Event("commit", "commit", "args", "output", parents=(2,), consumes=("passed",))), provenance)


def test_gate_missing_prerequisite_blocks_before_mutation_but_reversible_exploration_allowed():
    monitor = OnTrackMonitor(embed, contracts={"commit": ToolContract(True, ("passed",))})
    assert monitor.gate(Event("commit", "commit", "args"))["verdict"] == "BLOCK"
    assert monitor.graph.events == []
    assert monitor.gate(Event("weather", "weather", "args"))["verdict"] == "OK"
    assert OnTrackMonitor(embed).gate(Event("commit", "commit", "args"))["verdict"] == "OK"


def test_gate_uses_current_coupling_not_previous_cached_frontier():
    monitor = OnTrackMonitor(embed, references=[reference()], contracts={"commit": ToolContract(True, ("passed",))})
    for event in reference().events[:3]:
        monitor.admit(event)
    ref = monitor.references[0]
    # The old cached frontier explicitly excludes commit; the current coupling
    # has satisfied all three prerequisites. This reproduces the paper's bug.
    ref.active[:] = False
    t = np.zeros((3, 4))
    t[0, 0] = t[1, 1] = t[2, 2] = .25
    ref.state = CouplingState(t, np.zeros(3), np.zeros(4))
    assert monitor.gate(reference().events[3])["verdict"] == "OK"
    assert len(monitor.graph.events) == 3


def test_planner_reference_cannot_automatically_halt_on_bad_proposal():
    monitor = OnTrackMonitor(embed, references=[reference("planner")], contracts={"commit": ToolContract(True)})
    result = monitor.gate(Event("weather", "commit", "args"))
    assert result["verdict"] == "WARN" and not result["automatic_intervention"]


def test_artifact_discovery_repairs_old_edges_and_removes_young_structure_discount():
    graph = PrefixGraph()
    graph.append(Event("search", "search", "args"))
    graph.append(Event("edit", "edit", "args", consumes=("file",)))
    assert graph.parents[1] == set()
    graph.register_artifact(0, "file")
    assert graph.parents[1] == {0}
    assert graph.ages().tolist() == [1., 0.]
    with pytest.raises(ValueError, match="precede"):
        graph.append(Event("read", "read", "args", parents=(3,)))
    assert len(graph.events) == 2


def test_retry_error_exemption_is_bounded_and_loop_has_no_reference_requirement():
    monitor = OnTrackMonitor(embed)
    event = Event("read", "read", "args", "error", errored=True)
    assert monitor.admit(event)["verdict"] == "OK"
    assert monitor.admit(event)["verdict"] == "OK"
    assert monitor.admit(event)["verdict"] == "OK"
    assert monitor.admit(event)["verdict"] == "LOOP"
    other = OnTrackMonitor(embed)
    other.admit(Event("read", "read", "args", "output"))
    assert other.admit(Event("read", "read", "args", "output"))["verdict"] == "LOOP"


def test_finalization_is_cold_unmasked_independent_of_stream_history():
    a = OnTrackMonitor(embed, references=[reference()])
    b = OnTrackMonitor(embed, references=[reference()])
    for event in reference().events:
        a.admit(event)
        b.admit(event)
    a.references[0].state.coupling[:] = 100
    a.references[0].lookahead = 1
    assert a.finalize() == b.finalize()
    assert a.finalize()["age_weights_disabled"]


def test_transport_intervention_requires_escalated_current_solve():
    monitor = OnTrackMonitor(embed, references=[reference()])
    result = monitor.admit(Event("test", "test", "args", "output"))
    assert result["verdict"] == "CAUSAL_INVERSION"
    assert result["escalated"] and result["automatic_intervention"]


def test_configuration_rejects_invalid_protocol():
    with pytest.raises(ValueError):
        MonitorConfig(grace=0)
    with pytest.raises(ValueError):
        Reference(reference().events, "unspecified")
