"""RA-Eval CPU annotation protocol, not a source of LLM judgments.

Known answers are accepted only by the evaluator-only catch-trial gate.  Every
annotation verdict must be supplied by an external isolated judge; this module
does not infer preferences from gold answers or generate pretend judge labels.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Verdict:
    judge: str
    pair_id: str
    order: str
    winner: str

    def canonical(self) -> str:
        if not self.judge or not self.pair_id or self.order not in ("AB", "BA") or self.winner not in ("A", "B", "tie"):
            raise ValueError("judge/pair identifiers, AB/BA order and A/B/tie verdict required")
        if self.winner == "tie":
            return "tie"
        return self.order[0 if self.winner == "A" else 1]


@dataclass(frozen=True)
class Qualification:
    judge: str
    sensitivity: float
    qualified: bool
    catch_pair_ids: frozenset[str]


def qualify(judge: str, catches: list[tuple[Verdict, str]], minimum_sensitivity: float = .75) -> Qualification:
    """Evaluator-only known-answer catch trials; a tie is not a correct catch."""
    if not judge or not catches or not math.isfinite(minimum_sensitivity) or not 0 < minimum_sensitivity <= 1:
        raise ValueError("judge, nonempty catches and valid threshold required")
    if any(v.judge != judge or expected not in ("A", "B") for v, expected in catches):
        raise ValueError("catch identities/known canonical answers mismatch")
    ids = [v.pair_id for v, _ in catches]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate catches do not create independent calibration evidence")
    sensitivity = sum(v.canonical() == expected for v, expected in catches) / len(catches)
    return Qualification(judge, sensitivity, sensitivity >= minimum_sensitivity, frozenset(ids))


def join_swapped_judgments(pair_id: str, verdicts: list[Verdict],
                           qualifications: tuple[Qualification, Qualification]) -> dict:
    """Two named, qualified judges, each in both orders; disagreement is a tie.

    Distinct identifiers are necessary but cannot prove independent isolation;
    orchestration remains the caller's auditable responsibility.
    """
    if not pair_id or len(qualifications) != 2 or qualifications[0].judge == qualifications[1].judge:
        raise ValueError("two distinct judge identities required")
    if any(pair_id in q.catch_pair_ids for q in qualifications):
        raise ValueError("annotation and calibration pair IDs must be disjoint")
    judges = {q.judge for q in qualifications}
    if any(v.pair_id != pair_id or v.judge not in judges for v in verdicts):
        raise ValueError("annotation pair/judge mismatch")
    keys = [(v.judge, v.order) for v in verdicts]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate judge/order verdict")
    canonical = {(v.judge, v.order): v.canonical() for v in verdicts}
    votes = []
    reason = "agreement"
    if not all(q.qualified for q in qualifications):
        reason = "unqualified_judge"
    else:
        for q in qualifications:
            first, second = canonical.get((q.judge, "AB")), canonical.get((q.judge, "BA"))
            if first is None or second is None:
                reason = "missing_order"
                break
            if first != second or first == "tie":
                reason = "order_inconsistent_or_tied"
                break
            votes.append(first)
        if reason == "agreement" and votes[0] != votes[1]:
            reason = "judge_disagreement"
    winner = votes[0] if reason == "agreement" else "tie"
    return {"pair_id": pair_id, "winner": winner, "score_a": .5 if winner == "tie" else float(winner == "A"),
            "reason": reason, "preference_pair_eligible": winner != "tie"}


def check_split_isolation(calibration: set[str], training: set[str], heldout: set[str]) -> bool:
    return not (calibration & training or calibration & heldout or training & heldout)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU only")
    qualifications = tuple(qualify(j, [(Verdict(j, f"catch-{i}", "AB", "A"), "A") for i in range(4)])
                           for j in ("fixture-judge-1", "fixture-judge-2"))
    agreed = [Verdict(q.judge, "fixture-pair", order, "A" if order == "AB" else "B")
              for q in qualifications for order in ("AB", "BA")]
    result = join_swapped_judgments("fixture-pair", agreed, qualifications)
    disagreement = [Verdict(v.judge, v.pair_id, v.order,
                            ("B" if v.winner == "A" else "A") if v.judge == qualifications[1].judge else v.winner)
                    for v in agreed]
    tied = join_swapped_judgments("fixture-pair", disagreement, qualifications)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"canonical_swap_agreement": result["winner"] == "A",
                       "judge_disagreement_is_tie": tied["winner"] == "tie" and not tied["preference_pair_eligible"],
                       "missing_order_is_tie": join_swapped_judgments("fixture-pair", agreed[:-1], qualifications)["winner"] == "tie",
                       "test_not_shared_with_training": check_split_isolation({"c"}, {"t"}, {"h"}),
                       "overlap_is_rejected": not check_split_isolation({"c"}, {"t"}, {"t"})},
            "metrics": {"fixture_agreement_score_a": result["score_a"], "fixture_disagreement_score_a": tied["score_a"]}}
