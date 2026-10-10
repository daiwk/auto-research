from dataclasses import replace

import pytest

from auto_research.agent_research.mass import (
    Conversation, Execution, Task, bradley_terry_ranking, run_mass,
)


def test_mass_search_internalization_and_bare_task_split():
    class Fixture:
        revision = "v0"
        count = 0

        def execute(self, task, workflow):
            self.count += 1
            return Execution(str(self.count), str(self.count), (
                Conversation("orchestrator", ({"role": "user", "content": task.prompt + workflow},
                                               {"role": "assistant", "content": "delegate"})),
                Conversation("worker", ({"role": "user", "content": "bounded assignment"},)),
            ))

        def propose(self, task, previous, incumbent, history):
            return "revised workflow"

        def compare(self, task, candidate, incumbent):
            return (float(int(candidate.workspace) > int(incumbent.workspace)), "diagnostic comparison")

        def fine_tune(self, training, validation):
            assert training[0].messages[0]["content"] == "bare task"
            assert training[1].messages[0]["content"] == "bounded assignment"
            assert training != validation
            updated = Fixture()
            updated.revision = self.revision + "+sft"
            return updated

    task = Task("t1", "bare task", "initial")
    updated, audits = run_mass(Fixture(), (task,), cycles=2)
    assert updated.revision == "v0+sft+sft"
    assert len(audits) == 2
    assert audits[0]["validation_episode"] not in audits[0]["training_episodes"]
    with pytest.raises(ValueError):
        run_mass(Fixture(), (replace(task, split="test"),))


def test_bradley_terry_ranking_respects_pairwise_preferences():
    ranking, scores = bradley_terry_ranking(3, [(0, 1, 1.), (0, 2, 1.), (1, 2, 1.)])
    assert ranking == (0, 1, 2) and scores[0] > scores[1] > scores[2]
