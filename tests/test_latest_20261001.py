import numpy as np
import pytest

torch = pytest.importorskip("torch")

from auto_research.agent_research.latest_20261001 import (
    MetaSkillBank,
    ProposedAction,
    apply_context_file,
    compact_artifact_state,
    meta_reasoning_dispatch,
    route_branch,
    suffix_cache_reuse,
    update_branch_subsets,
)
from auto_research.evolution.compatibility import operator_registry
from auto_research.foundation_latest_20261001 import (
    ce_guided_router,
    pumba_window,
    splash_memory,
    splash_select_layout,
    tadm_fusion,
    vjepa_policy_losses,
)
from auto_research.post_training.latest_20261001 import (
    advisd_contrast,
    advisd_gate,
    flowmap_separated_loss,
    gats_schedule,
    interpolated_policy,
    maestro_disagreement,
)
from auto_research.recommendation_latest_20261001 import (
    cohortmix_prior,
    cohortmix_slate,
    cohortmix_update,
    recap_recursive_routes,
)
from auto_research.reproductions.rankmixer.model import RankMixerConfig, build_model


def test_meta_reasoning_uses_feasible_value_per_call_and_persistent_memory():
    selected, audit = meta_reasoning_dispatch([
        ProposedAction("deep", 10, 6),
        ProposedAction("reuse", 8, 2, ("artifact-a",)),
        ProposedAction("too-expensive", 20, 11),
    ], remaining_budget=10)
    assert selected.name == "reuse"
    assert audit == {"stopped": False, "selected": "reuse", "budget_after": 8, "context_items": 1}
    state = compact_artifact_state(
        {"memory": {"a": {"id": "a", "value": 1}}},
        [{"id": "b", "value": 2}, {"id": "c", "value": 3}], keep=1,
    )
    assert state["frontier"] == ("c",) and set(state["memory"]) == {"a", "b", "c"}


def test_context_lm_edits_file_and_suffix_cache_stops_at_first_mismatch():
    context = apply_context_file(
        "goal:old\nfact:a", [
            {"operation": "replace", "old": "goal:old", "new": "goal:new"},
            {"operation": "append", "text": "\nfact:b"},
        ], maximum_characters=100,
    )
    assert context == "goal:new\nfact:a\nfact:b"
    matched, suffix = suffix_cache_reuse([1, 2, 3, 4], [1, 2, 9, 4])
    assert matched == 2 and suffix == (9, 4)


def test_meta_skill_revision_is_development_only_and_branch_router_uses_features():
    bank = MetaSkillBank()
    bank.revise([
        {"skill": "verify", "reward": 1, "when": ["code"], "provide": ["tests"], "use": ["before-submit"]},
        {"skill": "guess", "reward": -1, "when": ["code"]},
    ])
    assert bank.select(["code"], limit=1) == ("verify",)
    subsets = update_branch_subsets({"a": {"x": 1, "common": 1}, "b": {"y": 1, "common": 1}})
    assert subsets == {"a": ("x",), "b": ("y",)}
    selected, scores = route_branch({"math": 1, "code": 0}, {"a": {"math": 2}, "b": {"code": 3}})
    assert selected == "a" and scores["a"] == 2


def test_advisd_gate_uses_paired_contrast_and_donor_calibration():
    with_advice = torch.tensor([[-1.0, -2.0], [-1.0, -1.0], [-3.0, -3.0]])
    without = torch.tensor([[-2.0, -3.0], [-1.1, -1.1], [-1.0, -1.0]])
    contrast = advisd_contrast(with_advice, without)
    selected, threshold = advisd_gate(
        contrast, torch.tensor([.05, .1, .2, .3]), torch.tensor([False, False, True]), quantile=.5,
    )
    assert selected.tolist() == [True, False, True]
    assert threshold == pytest.approx(.15)


def test_gats_lagged_gap_decreases_then_permanently_withdraws_teacher():
    weight, withdrawn, audit = gats_schedule([.7, .8, .9], [.2, .4], window=2)
    assert weight == pytest.approx(1 - .3 / .85) and not withdrawn
    weight, withdrawn, audit = gats_schedule([.7, .8, .9], [.9, .95], window=2)
    assert weight == 0 and withdrawn and audit["student_reference"] > audit["teacher_reference"]
    assert gats_schedule([.7, .8, .9], [.1], window=1, withdrawn=True)[:2] == (0.0, True)


def test_maestro_and_ipd_preserve_policy_boundaries():
    teacher = torch.tensor([[[.7, .2, .1], [.2, .7, .1]]])
    student = torch.tensor([[[.6, .1, .3], [.1, .8, .1]]])
    token_pds, prefix_pds = maestro_disagreement(teacher, student, top_k=2)
    assert token_pds.shape == (1, 2) and prefix_pds.shape == (1,)
    assert torch.all((token_pds >= 0) & (token_pds <= 1))
    mixed = interpolated_policy(student, teacher, .25)
    assert torch.allclose(mixed, .75 * student + .25 * teacher)
    assert torch.allclose(mixed.sum(-1), torch.ones_like(mixed.sum(-1)))


def test_flowmap_separates_rollout_graph_from_kernel_optimization():
    states = torch.randn(8, 4, requires_grad=True)
    student = torch.nn.Linear(4, 3)
    teacher = torch.nn.Linear(4, 3)
    loss, detached = flowmap_separated_loss(states, student, teacher)
    loss.backward()
    assert states.grad is None and not detached.requires_grad
    assert student.weight.grad is not None and teacher.weight.grad is None


def test_vjepa_flow_matching_stops_target_latent_gradient():
    predicted = torch.randn(2, 3, requires_grad=True)
    target = torch.randn(2, 3, requires_grad=True)
    action = torch.randn(2, 4)
    noise = torch.randn(2, 4)
    time = torch.tensor([.2, .8])

    class Velocity(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.proj = torch.nn.Linear(7, 4)

        def forward(self, sample, latent):
            return self.proj(torch.cat((sample, latent), dim=-1))

    loss, audit = vjepa_policy_losses(predicted, target, Velocity(), action, noise, time)
    loss.backward()
    assert predicted.grad is not None and target.grad is None
    assert set(audit) == {"latent_loss", "action_loss"}


def test_ce_guided_router_attenuates_high_predicted_error():
    prob, adjusted = ce_guided_router(
        torch.tensor([[1.0, 1.0, 1.0]]), torch.tensor([[.1, 10.0, 1.0]])
    )
    assert prob.argmax(-1).item() == 0
    assert adjusted[0, 1] < adjusted[0, 2] < adjusted[0, 0]


def test_tadm_fuses_stale_anchor_with_bounded_current_correction():
    stale = torch.zeros(2, 3)
    current = torch.ones(2, 3)
    fused, gate = tadm_fusion(
        stale, current,
        lambda c, h: torch.zeros_like(c),
        lambda c, h: c - h,
    )
    assert torch.allclose(gate, torch.full_like(gate, .5))
    assert torch.allclose(fused, torch.full_like(fused, .5))


def test_pumba_later_loss_backpropagates_through_carry():
    initial = torch.randn(2, 3, 5, requires_grad=True)
    targets = torch.randint(0, 5, (2, 3))

    def step(logits, carry, _step):
        carry = logits if carry is None else .5 * carry + logits
        return carry, carry

    loss, detached, losses = pumba_window(step, initial, targets, window=3)
    loss.backward()
    assert initial.grad is not None and initial.grad.abs().sum() > 0
    assert len(losses) == 3 and not detached.requires_grad


def test_splash_memory_and_transition_aware_layout_selection():
    arguments = dict(attention_weights=120, batch=8, kv_heads=2, sequence=16, tensor_parallel=4)
    assert splash_memory("dop", **arguments) < splash_memory("tp", **arguments)
    assert splash_memory("dop", **arguments) < splash_memory("dp", **arguments)
    layout, costs = splash_select_layout(
        {"tp": 1.0, "dop": .8}, "tp", {("tp", "dop"): 4.0}, remaining_steps=5,
    )
    assert layout == "tp"
    layout, _ = splash_select_layout(
        {"tp": 1.0, "dop": .8}, "tp", {("tp", "dop"): 4.0}, remaining_steps=50,
    )
    assert layout == "dop" and costs["dop"] > .8


def test_recap_routes_average_and_rankmixer_operator_executes():
    torch.manual_seed(0)
    block = torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.Tanh())
    averaged, audit = recap_recursive_routes(torch.randn(3, 4), block, routes=3, ema_decay=.9)
    assert averaged.shape == (3, 4) and audit["routes"].shape == (3, 3, 4)
    assert torch.allclose(averaged, audit["routes"].mean(0))
    spec = operator_registry()["rankmixer_recap"]
    assert spec.paper_ids == ("2609.37905",) and spec.compatible_models == ("rankmixer",)

    class Data:
        item_count = 7
        item_features = np.eye(7, 4, dtype=np.float32)

    model = build_model(
        "rankmixer_recap", Data,
        RankMixerConfig(dimensions=8, tokens=4, heads=4, layers=1, recap_routes=3),
    )
    assert model(torch.tensor([[0, 1, 2, 3]])).shape == (1, 7)


def test_cohortmix_prior_slate_and_posterior_update():
    alpha, beta = cohortmix_prior(
        [.75, .25], [[8, 2, 5], [1, 7, 2]], [[2, 8, 5], [9, 3, 8]],
        alpha0=1, beta0=1, strength=10,
    )
    assert np.allclose(alpha + beta, 10)
    chosen, _ = cohortmix_slate(alpha, beta, size=2, seed=42)
    updated_alpha, updated_beta = cohortmix_update(alpha, beta, chosen, [1, 0])
    assert np.isclose((updated_alpha + updated_beta).sum(), (alpha + beta).sum() + 2)
