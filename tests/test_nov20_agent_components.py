import math

import pytest

from auto_research.agent_research import buggymle_cci as cci
from auto_research.agent_research.grepmem import GrepMemory
from auto_research.system_one.looproute import LoopRouter, public_state_key


def calibration(**changes):
    values = dict(reference_id="synthetic-test-only", feature_means=(0.,)*10,
                  feature_stds=(1.,)*10, group_stds=(1.,)*3,
                  coefficients=(.64, -.34, -.99), raw_min=-2., raw_max=2.)
    return cci.Calibration(**(values | changes))


def features(**changes):
    return {name: 0. for name in cci.FEATURES} | changes


def test_cci_exact_three_stage_scaling_and_conditional_signs():
    c = calibration(feature_means=(1.,)*10, feature_stds=(2.,)*10,
                    group_stds=(2., 3., 4.))
    row = cci.project(features(**{k: math.e**3-1 for k in cci.FEATURES}), c)
    assert row["group_scores"] == pytest.approx({"repo": .5, "dep": 1/3, "patch": .25})
    assert row["raw_cci"] == pytest.approx(-(.64*.5-.34/3-.99*.25))
    assert row["scaled_cci"] == pytest.approx((row["raw_cci"]+2)/4)
    assert row["predicted_solve_rate"] is None


def test_cci_median_not_mean_and_no_test_time_refit_or_clipping():
    b = features()
    high = features(**{k: 100. for k in cci.GROUPS["patch"]})
    assert cci.benchmark_medians([b,b,high]) == b
    assert cci.project(high, calibration())["scaled_cci"] > 1
    assert cci.project(features(lines_of_code=100000), calibration())["raw_cci"] < 0
    assert cci.project(b, calibration(intercept=1000))["predicted_solve_rate"] == 1
    assert cci.project(b, calibration(intercept=-1000))["predicted_solve_rate"] == 0


@pytest.mark.parametrize("change", [{"lines_added": -1}, {"hunks": True},
                                  {"total_lines_delta": -2}, {"file_count": math.nan}])
def test_cci_rejects_undefined_feature_transforms(change):
    with pytest.raises(ValueError):
        cci.project(features(**change), calibration())


@pytest.mark.parametrize("change", [{"feature_stds": (0.,)*10}, {"group_stds": (0.,)*3},
                                  {"raw_min": 2.}, {"reference_id": ""},
                                  {"coefficients": (math.inf,0,0)}])
def test_cci_requires_complete_nondegenerate_external_calibration(change):
    with pytest.raises(ValueError):
        calibration(**change)


def test_cci_does_not_take_absolute_net_delta():
    negative = cci.project(features(total_lines_delta=-.5), calibration())
    positive = cci.project(features(total_lines_delta=.5), calibration())
    assert negative["raw_cci"] < 0 < positive["raw_cci"]


def test_public_keys_exclude_history_and_are_canonical():
    a = {"facts": {"location": "kitchen", "inventory": []}, "admissible_actions": ["look","take"]}
    b = {"admissible_actions": ["take","look"], "facts": {"inventory": [], "location": "kitchen"}}
    assert public_state_key("alfworld",a) == public_state_key("alfworld",b)
    with pytest.raises(ValueError):
        public_state_key("alfworld", a | {"step":3})
    with pytest.raises(ValueError):
        public_state_key("alfworld", a | {"gold_answer":"hidden"})
    assert public_state_key("alfworld",a) != public_state_key("alfworld",a | {"facts":{"location":"hall"}})


def execute_twice(router):
    for _ in range(2):
        assert router.route("same", "look").policy == "decision"
        router.record_execution("look")


def test_alfworld_intercepts_third_proposal_before_execution_and_resets_after_two_actions():
    r = LoopRouter("alfworld")
    execute_twice(r)
    d = r.route("same", "look")
    assert d.intercepted and d.policy == "llm" and r.counts["same","look"] == 2
    r.record_execution("open")
    assert r.counts["same","open"] == 0 and r.remaining == 1
    assert r.route("other").policy == "llm"
    r.record_execution("take")
    assert r.remaining == 0 and not r.counts
    assert r.route("same","look").policy == "decision"


@pytest.mark.parametrize("benchmark", ["mapreader", "textworld"])
def test_other_adapters_count_both_policies_and_keep_episode_counts(benchmark):
    r = LoopRouter(benchmark)
    execute_twice(r)
    r.route("same","look");r.record_execution("open")
    r.route("same");r.record_execution("open")
    assert r.counts["same","open"] == 2
    assert r.route("same","open").intercepted


def test_only_executed_decisions_count_and_information_reset_is_alfworld_specific():
    r = LoopRouter("alfworld")
    r.route("same","look")
    with pytest.raises(RuntimeError):
        r.route("same","look")
    with pytest.raises(ValueError):
        r.record_execution("different")
    assert not r.counts
    r.record_execution("look",new_information=True)
    assert not r.counts
    x = LoopRouter("mapreader");x.route("same","look")
    with pytest.raises(ValueError):
        x.record_execution("look",new_information=True)


def test_termination_ends_takeover_immediately():
    r = LoopRouter("alfworld");execute_twice(r);r.route("same","look")
    r.record_execution("finish",terminated=True)
    assert r.remaining == 0
    with pytest.raises(RuntimeError):r.route("same","look")


def memory():
    m = GrepMemory("Use observed records only.", "Look up IDs.")
    m.append("tool","[turn 1 get_document]","before\nID: Alpha\nID: Beta\nafter")
    return m


def test_grep_disabled_before_compaction_and_log_is_lossless():
    m = memory();old=m.export_log()
    with pytest.raises(RuntimeError):m.grep("Alpha")
    m.compact("Two IDs were observed.")
    assert m.export_log().startswith(old)
    assert len(m.working_context)==3
    assert "Alpha" not in m.working_context[-1].text


def test_grep_pagination_case_context_offsets_and_recursive_output_exclusion():
    m = memory();m.compact("IDs observed.")
    a = m.grep("id:",max_matches=1)
    assert a["total_matches"]==2 and a["next_offset"]==1
    assert "2: ID: Alpha" in a["text"] and "1- before" in a["text"]
    m.append("tool","[turn 2 grep_history]",a["text"],tool_name="grep_history")
    b=m.grep("ID:",offset=1,max_matches=1,context_lines=0)
    assert b["total_matches"]==2 and b["next_offset"] is None
    assert "3: ID: Beta" in b["text"] and "Alpha" not in b["text"]
    count=m.grep("id:",count=True)
    assert count["total_matches"]==2 and count["returned_matches"]==0


def test_invalid_pattern_returns_compiler_error_and_path_strings_are_not_opened():
    m=memory();m.compact("ok")
    assert "error" in m.grep("[")
    assert m.grep("/etc/passwd")["total_matches"]==0


def test_regex_timeout_kills_only_the_search_worker():
    m=GrepMemory("public", "task")
    m.append("tool","[observed]","a"*1000+"!");m.compact("summary")
    r=m.grep("(a+)+$",timeout_seconds=.1)
    assert r["timed_out"]
    assert m.grep("a{5}")["total_matches"]==1


def test_output_cap_clipping_and_pages_make_progress():
    m=GrepMemory("public", "task")
    m.append("tool","[record]","\n".join("x"*500+"needle"+"x"*500 for _ in range(80)))
    m.compact("summary")
    a=m.grep("needle",max_matches=30,context_lines=3)
    assert a["output_characters"]<=6000 and 0<a["returned_matches"]<30
    assert "needle" in a["text"] and a["next_offset"]==a["returned_matches"]
    b=m.grep("needle",offset=a["next_offset"],max_matches=30)
    assert b["next_offset"]>a["next_offset"]


@pytest.mark.parametrize("kwargs", [{"max_matches":31},{"max_matches":True},
                                  {"offset":-1},{"context_lines":4},{"count":1},
                                  {"timeout_seconds":11}])
def test_grep_validates_bounded_tool_arguments(kwargs):
    m=memory();m.compact("summary")
    with pytest.raises(ValueError):m.grep("a",**kwargs)


@pytest.mark.parametrize("seed",[42,43,44])
def test_diagnostics_are_controls_not_agent_success(seed):
    from auto_research.agent_research.grepmem import diagnostic as grep
    from auto_research.system_one.looproute import diagnostic as route
    for fn in [cci.diagnostic,grep,route]:
        result=fn(seed)
        assert result["diagnostic_only"] and all(result["checks"].values())
