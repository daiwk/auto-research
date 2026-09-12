from auto_research.reproductions.sep7_models import EvidenceController


def test_fresh_proposals_consume_executed_ledger_and_resume(tmp_path):
    path = tmp_path / "ledger.json"
    controller = EvidenceController({"ndcg_at_10": 0.1}, path)
    seen = []

    def propose(context):
        seen.append(len(context["records"]))
        return [{"key": f"candidate-{len(context['records'])}",
                 "evidence": "public paper", "steps": len(context["records"]) + 1}]

    def review(proposal, context):
        return {"feasible": proposal["steps"] <= 3, "score": proposal["steps"]}

    executed = []

    def execute(proposal):
        executed.append(proposal["steps"])
        return {"ndcg_at_10": 0.1 + proposal["steps"] * 0.01}

    controller.research(propose, [review, review],
                        lambda proposal: {"passed": True, "checks": ["unit-test"]},
                        execute, {}, rounds=2)
    assert seen == [0, 1] and executed == [1, 2]
    restored = EvidenceController({"ndcg_at_10": 0.1}, path)
    assert restored.incumbent == "candidate-1"
    assert restored.records[-1]["proposal"]["steps"] == 2
    assert all(not row["online_authorized"] for row in restored.records)


def test_failed_execution_verification_cannot_run_candidate():
    controller = EvidenceController({"ndcg_at_10": 0.1})
    calls = []
    row = controller.evaluate(
        {"key": "bad", "evidence": "paper", "reviews": []},
        lambda candidate: calls.append(candidate), {}, verify=lambda candidate: {"passed": False},
    )
    assert not calls and row["verdict"] == "failed"
    assert "execution-verified" not in row["events"]
