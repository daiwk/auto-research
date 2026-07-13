import sys

from auto_research.models import Trial
from auto_research.research_loop import CommandProposer


def test_command_proposer_receives_history_and_can_stop(tmp_path):
    command = [
        sys.executable,
        "-c",
        (
            "import json,os; h=json.loads(os.environ['AUTO_RESEARCH_HISTORY']); "
            "print(json.dumps({'stop': True} if len(h) else {'params': {'lr': 0.1}}))"
        ),
    ]
    proposer = CommandProposer(command, {"topic": "test"}, 3, 10, tmp_path)

    assert proposer.propose(()) == {"lr": 0.1}
    history = (Trial(1, {"lr": 0.1}, 1.0, "completed", 0.1),)
    assert proposer.propose(history) is None
