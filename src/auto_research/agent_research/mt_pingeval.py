"""MT-PingEval v1 Name-game/evaluation-budget contracts, without an actor.

No official dataset, tokenizer, chess/image task or full-suite bridge is loaded.
"""
from dataclasses import dataclass

REQUIRES_GPU_VALIDATION = False


def _records(rows):
    if isinstance(rows, (str, bytes)):
        raise ValueError("explicit private record sequence required")
    rows = tuple(rows)
    if any(not isinstance(row, (tuple, list)) for row in rows):
        raise ValueError("explicit per-record field sequences required")
    rows = tuple(tuple(row) for row in rows)
    if not rows or any(len(row) != 5 or any(not isinstance(v, str) or not v for v in row) for row in rows):
        raise ValueError("five nonempty categorical fields per Name-game record required")
    if len(set(rows)) != len(rows):
        raise ValueError("each player's records must be unique")
    return rows


@dataclass(frozen=True)
class PrivateView:
    player: str
    records: tuple[tuple[str, ...], ...]


class NameGame:
    """Evaluator-owned pair; pass only view(player), never this object, to actors."""
    def __init__(self, alice, bob):
        self._rows = {"alice":_records(alice), "bob":_records(bob)}
        common = set(self._rows["alice"]) & set(self._rows["bob"])
        if len(common) != 1:
            raise ValueError("Name-game requires exactly one shared complete record")
        self._common = next(iter(common))

    def view(self, player: str) -> PrivateView:
        if player not in self._rows:
            raise ValueError("known player required")
        return PrivateView(player, self._rows[player])

    def score_selection(self, player: str, *, row_number: int) -> bool:
        """One-based SELECT ROW convention; full record, not name-only match."""
        if player not in self._rows or type(row_number) is not int or not 1 <= row_number <= len(self._rows[player]):
            raise ValueError("valid one-based row selection required")
        return self._rows[player][row_number-1] == self._common


class IsotokenBudget:
    """Alternating total turns; each player has the same total token budget.

    For 256 tokens/player and 16 alternating turns, cap=512//16=32 per
    utterance. The paper's 128/player example gives16 tokens/utterance.
    Supply actual tokenizer IDs: word counts are not substituted for tokens.
    """
    def __init__(self, *, tokens_per_player=256, total_turns=16):
        if type(tokens_per_player) is not int or tokens_per_player < 1 or type(total_turns) is not int or total_turns < 2 or total_turns % 2:
            raise ValueError("positive token budget and even alternating turn limit required")
        self.tokens_per_player, self.total_turns = tokens_per_player, total_turns
        self.per_turn = 2 * tokens_per_player // total_turns
        if self.per_turn < 1:
            raise ValueError("token budget cannot provide one token per turn")
        self.turns = 0
        self.used = {"alice":0,"bob":0}

    def submit(self, player: str, token_ids):
        expected = "alice" if self.turns % 2 == 0 else "bob"
        if self.turns >= self.total_turns or player != expected:
            raise ValueError("turn exhausted or wrong alternating player")
        if isinstance(token_ids, (str, bytes)):
            raise ValueError("actual tokenizer ID sequence required")
        tokens = tuple(token_ids)
        if any(type(token) is not int or token < 0 for token in tokens):
            raise ValueError("nonnegative integer tokenizer IDs required")
        accepted = tokens[:min(self.per_turn, self.tokens_per_player-self.used[player])]
        self.used[player] += len(accepted)
        self.turns += 1
        return accepted


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only evaluation contracts required")
    shared = ("Isabella","Leo","Tesla","Miles Davis","Eggs")
    similar = ("Isabella","Leo","HP","Miles Davis","Eggs")
    other = ("Michael","Scorpio","Cisco","John Coltrane","Corn")
    game = NameGame([shared, similar], [other, shared])
    budget = IsotokenBudget(tokens_per_player=128, total_turns=16)
    accepted = budget.submit("alice", range(30))
    checks = {"private_view_has_no_other_database":game.view("alice").records == (shared,similar),
              "same_name_not_enough":not game.score_selection("alice", row_number=2),
              "correct_record_selected":game.score_selection("bob", row_number=2),
              "isotoken_example_matches_paper":budget.per_turn == 16 and len(accepted) == 16,
              "truncation_charged_actual_ids":budget.used["alice"] == 16 and budget.used["bob"] == 0}
    return {"seed":seed,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","checks":checks,
            "metrics":{"contract_checks":len(checks),"tokens_per_utterance":budget.per_turn,"accepted_token_ids":len(accepted)}}
