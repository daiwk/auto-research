import copy
import json
import numpy as np
import pytest
import torch

from auto_research.agent_research.causal_memory_policy import (
    balanced_exposure,
    estimate_utility,
    query_decision,
)
from auto_research.agent_research.mingbird import (
    LoopMonitor,
    flat_prefill,
    rescue_tool_call,
    run_task,
)
from auto_research.agent_research.t2spo import TrajectoryMemory, FrozenDistanceEstimator
from auto_research.post_training.oct04_objectives import (
    t2spo_credit,
    clipped_policy_loss,
    weakest_link_rewards,
    weakest_link_loss,
    rlcpr_rewards,
    rlcpr_sampling_probabilities,
)
from auto_research.post_training.tess import fit_tess, pointwise_value_matching
from auto_research.system_one.lookahead import simulate_options, choose_with_lookahead
from auto_research.system_one.contracts import SystemOneResponse, DecisionAnswer


def test_t2spo_masks_terminal_semantics_and_no_gradient_to_estimator():
    d = torch.tensor([3.0, 3.0, 3.0, 3.0], requires_grad=True)
    kwargs = dict(
        mask=torch.tensor([True, True, True, False]),
        success_terminal=torch.tensor([True, False, False, False]),
        failure_terminal=torch.tensor([False, True, False, False]),
        truncated=torch.tensor([False, False, True, False]),
    )
    grpo = t2spo_credit(d, torch.ones(4), **kwargs)
    ppo = t2spo_credit(d, torch.ones(4), optimizer="ppo", **kwargs)
    assert grpo[0] > 0 and grpo[1:].tolist() == [0.0, 0.0, 0.0]
    assert ppo[2] > 0 and not grpo.requires_grad
    logp = torch.zeros(4, requires_grad=True)
    clipped_policy_loss(logp, logp.detach(), grpo, kwargs["mask"]).backward()
    assert logp.grad[0] < 0 and logp.grad[3] == 0 and d.grad is None


def test_t2spo_memory_excludes_failure_and_copies_snapshot():
    memory = TrajectoryMemory(capacity=3)
    memory.add_completed(np.ones((2, 3)), successful=False)
    assert not len(memory.snapshot()[1])
    memory.add_completed(np.ones((2, 3)), successful=True)
    features, targets, version = memory.snapshot()
    assert targets.tolist() == [2.0, 1.0]
    memory.add_completed(np.full((2, 3), 5.0), successful=True)
    assert memory.snapshot()[1].tolist() == [1.0, 2.0, 1.0]
    assert np.all(features == 1) and version == 1
    with pytest.raises(FileNotFoundError):
        FrozenDistanceEstimator("/nonexistent/tabpfn.ckpt")


def test_weakest_link_prefix_violation_cannot_be_compensated():
    rewards, violated = weakest_link_rewards(
        torch.tensor([-4.0, -0.1, -0.1]), torch.ones(3), budget=2, penalty=7
    )
    assert violated.all() and rewards.tolist() == [-7.0, -7.0, -7.0]
    safe, bad = weakest_link_rewards(torch.tensor([-1.0, -1.0]), torch.ones(2), budget=2, penalty=7)
    assert not bad.any() and safe.tolist() == [1.0, 1.0]


def test_weakest_link_exact_immediate_gradient_matches_enumeration():
    # One-step case has no future MC term; compare full action enumeration.
    logits = torch.tensor([[0.2, -0.1]], requires_grad=True)
    teacher = torch.tensor([[-0.1, -3.0]], requires_grad=True)
    loss = weakest_link_loss(
        logits, torch.tensor([0]), teacher, torch.ones_like(logits), budget=1, penalty=4
    )
    (grad,) = torch.autograd.grad(loss, logits)
    other = logits.detach().clone().requires_grad_()
    reference = -(other.softmax(-1) * torch.tensor([[1.0, -4.0]])).sum()
    (expected,) = torch.autograd.grad(reference, other)
    assert torch.allclose(grad, expected)
    assert grad[0, 0] < 0 and teacher.grad is None


def test_weakest_link_future_penalty_reaches_prior_actions():
    logits = torch.zeros((2, 2), requires_grad=True)
    loss = weakest_link_loss(
        logits,
        torch.tensor([0, 1]),
        torch.tensor([[-0.1, -0.1], [-0.1, -8.0]]),
        torch.ones_like(logits),
        budget=1,
        penalty=4,
    )
    loss.backward()
    assert logits.grad[0, 0] > 0  # earlier sampled action gets negative future return


def test_rlcpr_only_penalizes_long_concentrated_groups():
    post = torch.tensor([[0.1, 0.9], [0.50, 0.51]])
    lengths = torch.tensor([[1.0, 2.0], [100.0, 200.0]])
    shaped, active = rlcpr_rewards(post, lengths)
    assert active.tolist() == [False, True]
    assert torch.equal(shaped[0], post[0])
    assert shaped[1, 0] == post[1, 0] and shaped[1, 1] < post[1, 1]
    probs = rlcpr_sampling_probabilities(torch.tensor([0.0, 1.0, 2.0, 3.0]))
    assert probs.sum().item() == pytest.approx(1) and probs[0] > probs[-1]
    assert torch.allclose(rlcpr_sampling_probabilities(torch.ones(4)), torch.full((4,), 0.25))


def test_cmp_balancing_positivity_and_reproducibility():
    z = balanced_exposure(32, 90, 2)
    assert np.all(z.sum(1) == 2)
    assert set(z.sum(0)) == {5, 6}
    assert np.array_equal(z, balanced_exposure(32, 90, 2))
    assert not np.array_equal(z, balanced_exposure(32, 90, 2, seed=43))
    with pytest.raises(ValueError, match="support"):
        balanced_exposure(32, 2, 2)


def test_cmp_utility_recovers_randomized_effect_and_abstains():
    z = balanced_exposure(3, 300, 1)
    outcomes = 2.0 * z[:, 0] - z[:, 1]
    values, se = estimate_utility(z, outcomes)
    assert values[0] > 0 and values[1] < 0 and (se >= 0).all()
    assert query_decision(2, 0.01) == "noop"
    assert query_decision(-2, 0.01) == "forget"
    assert query_decision(-0.01, 1) == "noop"
    assert query_decision(-2, float("inf")) == "noop"


def test_tess_pvm_stops_teacher_gradient_and_trains_selector():
    p = torch.tensor([0.2, 0.3], requires_grad=True)
    u = torch.tensor([2.0, 1.0], requires_grad=True)
    w = torch.tensor([1.0, 1.0], requires_grad=True)
    pointwise_value_matching(p, u, w).backward()
    assert u.grad is None and w.grad is None and p.grad[0] < 0
    torch.manual_seed(42)
    x = torch.linspace(-2, 2, 32)[:, None]
    train = (x, (x[:, 0] > 0).long())
    validation = (x, (x[:, 0] > 0.5).long())
    model, selector = torch.nn.Linear(1, 2), torch.nn.Linear(1, 1)
    original = copy.deepcopy(model.state_dict())
    result = fit_tess(
        model,
        selector,
        train_batch=train,
        validation_batch=validation,
        train_features=x,
        pool_features=x[:7],
        steps=20,
        selector_steps=60,
        per_example_loss=lambda m, b: torch.nn.functional.cross_entropy(
            m(b[0]), b[1], reduction="none"
        ),
    )
    assert result["scores"].shape == (7,)
    assert result["pvm_losses"][-1] < result["pvm_losses"][0]
    assert all(torch.equal(original[k], model.state_dict()[k]) for k in original)


class TextWorld:
    def __init__(self):
        self.place = "hall"

    def fork(self):
        return copy.deepcopy(self)

    def admissible_commands(self):
        return ("sink", "drawer") if self.place == "hall" else ("wash", "leave")

    def step(self, command):
        self.place = command
        return "at " + command


def test_jev_simulates_separate_branches_and_calls_existing_provider_contract():
    world = TextWorld()
    options = simulate_options(world)
    assert world.place == "hall" and options[0].newly_possible == ("wash", "leave")

    class RecordingProvider:
        def decide(self, request):
            assert "then newly possible" in request.questions["action"].criteria["0"]
            assert set(request.state) == {"task", "observation", "history"}
            return SystemOneResponse(
                model="diagnostic",
                answers={
                    "action": DecisionAnswer(
                        type="choice", value="0", probabilities={"0": 0.8, "1": 0.2}, confidence=0.8
                    )
                },
            )

    command, _ = choose_with_lookahead(world, RecordingProvider(), task="wash", observation="hall")
    assert command == "sink" and world.place == "hall"


def test_mingbird_utf8_budget_and_signature_normalization():
    tools = {"read": {"domains": ["files"], "parameters": {"路径": "str"}}}
    prompt = flat_prefill(tools, domain="files", budget_bytes=100)
    with pytest.raises(ValueError, match="budget"):
        flat_prefill(tools, domain="files", budget_bytes=len(prompt))
    monitor = LoopMonitor()
    for i in range(5):
        assert (
            monitor.record(
                "read", {"a": 1, "b": 2} if i % 2 else {"b": 2, "a": 1}, produced_output=True
            )
            is None
        )
    assert "repeated" in monitor.record("read", {"a": 1, "b": 2}, produced_output=True)
    with pytest.raises(ValueError):
        rescue_tool_call('__import__("os").system("id")', {"read"})


def test_mingbird_false_finish_recovery_executes_tool_and_rechecks():
    state, sequence = (
        {},
        iter(["finish", json.dumps({"tool": "write", "arguments": {"value": "done"}}), "finish"]),
    )

    def write(value):
        state["artifact"] = value
        return "wrote artifact"

    result = run_task(
        lambda _: next(sequence),
        {"write": write},
        {"artifact": lambda: state.get("artifact") == "done"},
        task="write artifact",
        max_turns=3,
    )
    assert result["complete"] and result["trace"][0]["complete"] is False
    assert result["trace"][-1]["complete"] is True


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_invalid_reward_inputs_rejected(bad):
    with pytest.raises(ValueError):
        weakest_link_rewards(torch.tensor([bad]), torch.ones(1), budget=2, penalty=1)


def test_seven_paper_metadata_and_diagnostic_receipts_are_complete():
    from pathlib import Path
    from auto_research.latest_20261004_followup_catalog import LATEST_METHOD_PAPERS

    root = Path(__file__).resolve().parents[1]
    assert len(LATEST_METHOD_PAPERS) == 7
    assert sum(p["priority"] == "P0" for p in LATEST_METHOD_PAPERS) == 3
    for paper in LATEST_METHOD_PAPERS:
        page = root / "docs" / paper["detail_path"]
        body = page.read_text()
        for heading in (
            "论文信息",
            "原始论文总结",
            "背景与主要改动",
            "核心公式",
            "论文离线与线上效果",
            "本地复现",
            "复现边界",
        ):
            assert heading in body, (paper["key"], heading)
        for field in (
            "论文链接",
            "公司/机构",
            "首次公开日期",
            "原文开源代码",
            "Adapter",
            "本地复现代码",
        ):
            assert f"| {field} |" in body
        assert paper["published"] in body and paper["paper_url"] in body
        result = json.loads((page.parent / "metrics/mechanism-seeds42-44.json").read_text())
        assert result["diagnostic_only"] and not result["evaluation_protocol"]["formal_comparison"]
        assert [row["seed"] for row in result["seed_results"]] == [42, 43, 44]
        assert "seed_mean" not in result["aggregate_metrics"]
    real = json.loads(
        (root / "docs/post-training/2610.00388-t2spo/metrics/tabpfn-cpu.json").read_text()
    )
    assert len(real["provenance"]["checkpoint_sha256"]) == 64
    assert len(real["provenance"]["checkpoint_revision"]) == 40
    assert real["provenance"]["device"] == "cpu" and len(real["seed_results"]) == 3


def test_mingbird_repeated_tool_is_not_executed_sixth_time():
    calls = []
    result = run_task(
        lambda _: '{"tool":"read","arguments":{}}',
        {"read": lambda: calls.append(1)},
        {"done": lambda: False},
        task="read",
        max_turns=8,
    )
    assert len(calls) == 5 and not result["complete"]
    assert result["trace"][-1]["kind"] == "correction"


def test_jev_rejects_shared_state_and_inadmissible_provider_result():
    class BrokenFork(TextWorld):
        def fork(self):
            return self

    with pytest.raises(ValueError, match="isolate"):
        simulate_options(BrokenFork())

    class WrongProvider:
        def decide(self, request):
            return SystemOneResponse(
                model="diagnostic",
                answers={
                    "action": DecisionAnswer(
                        type="choice",
                        value="outside",
                        probabilities={"outside": 1.0},
                        confidence=1.0,
                    )
                },
            )

    with pytest.raises(ValueError, match="inadmissible"):
        choose_with_lookahead(TextWorld(), WrongProvider(), task="wash", observation="hall")


def test_rlcpr_equal_threshold_does_not_penalize():
    post = torch.tensor([[0.5, 0.5], [0.5, 0.5]])
    lengths = torch.tensor([[10.0, 20.0], [10.0, 20.0]])
    rewards, active = rlcpr_rewards(post, lengths)
    assert not active.any() and torch.equal(rewards, post)


def test_mingbird_no_output_warning_allows_recovery():
    calls = []
    actions = iter(
        [json.dumps({"tool": "empty", "arguments": {"i": i}}) for i in range(15)]
        + [json.dumps({"tool": "repair", "arguments": {}}), "finish"]
    )

    def repair():
        calls.append("repaired")
        return "wrote result"

    result = run_task(
        lambda _: next(actions),
        {"empty": lambda i: None, "repair": repair},
        {"artifact": lambda: bool(calls)},
        task="repair",
        max_turns=17,
    )
    assert result["complete"] and calls == ["repaired"]
    assert sum(row["kind"] == "correction" for row in result["trace"]) == 1


def test_new_papers_appear_in_all_browse_dimensions():
    from pathlib import Path
    from auto_research.latest_20261004_followup_catalog import LATEST_METHOD_PAPERS

    root = Path(__file__).resolve().parents[1] / "docs"
    for paper in LATEST_METHOD_PAPERS:
        for dimension in ("organization", "topic", "year"):
            body = (root / paper["domain"] / "catalog" / f"by-{dimension}.md").read_text()
            assert paper["paper_url"].rsplit("/", 1)[-1] in body, (paper["key"], dimension)
