import json

import numpy as np

from auto_research.agent_research.capability_models import CapabilityObservation, ToolFeedback
from auto_research.agent_research.coskill_rollout import Decision, collect_group, role_advantages
from auto_research.agent_research.sep7_mechanisms import HierarchicalSkills


def test_credit_does_not_length_weight_episode_returns():
    rows = [Decision("reasoning", "", "", str(i), "long", "task", episode_return=1)
            for i in range(8)]
    rows.append(Decision("reasoning", "", "", "other", "short", "task", episode_return=0))
    assert np.allclose(role_advantages(rows, step_weight=0), [1] * 8 + [-1])


def test_private_edits_require_reset_and_never_reach_baseline():
    observation = CapabilityObservation("id", "train", "family", "request", ("tag",), ())
    skills = HierarchicalSkills()
    resets = []

    def reset():
        resets.append(1)
        return lambda tool: ToolFeedback("ok", "executed", terminal=True)

    def generate(role, prompt):
        assert not skills.bundles
        if role == "editing":
            return json.dumps({"operation": "insert", "procedure": "new step"})
        return '{"tool":"read"}'

    decisions, records = collect_group(observation, reset, generate, skills,
                                       group_size=2, verification_attempts=2)
    assert len(resets) == 6
    assert all(row["delta"] == 0 for row in records)
    assert not skills.bundles  # no improvement, no promotion
    assert sum(row.role == "editing" for row in decisions) == 2
    assert sum(row.role == "reasoning" for row in decisions) == 6


def test_checkpoint_similarity_selects_active_child_without_lexical_overlap():
    observation = CapabilityObservation("id", "train", "family", "request", ("tag",), ())
    skills = HierarchicalSkills(similarity=lambda state, child: 1.0 if child == "semantic-best" else 0.0)
    skills.bundles["request"] = ["lexical tag", "semantic-best"]
    prompts = []

    def generate(role, prompt):
        prompts.append(prompt)
        return '{"tool":"read"}' if role == "reasoning" else '{"operation":"keep"}'

    collect_group(observation, lambda: lambda tool: ToolFeedback("ok", "done", terminal=True),
                  generate, skills, group_size=2, verification_attempts=1)
    reasoning = [json.loads(prompt.split("\n", 1)[1]) for prompt in prompts if prompt.startswith("Choose")]
    assert reasoning and all(row["step_skill"] == "semantic-best" for row in reasoning)
