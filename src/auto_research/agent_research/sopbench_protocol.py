"""SOPBench's nested constraint/procedure evaluator, not its seven-domain agent.

All oracle verdicts and final-state references belong to the POST-TRAJECTORY
evaluator. This module never passes them to a policy or executes external tools.
Helper names are argument-qualified call identities supplied by the environment;
raw function-name coincidence is not sufficient evidence of checking a request.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
import random
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Rule:
    kind: str
    name: str = ""
    helpers: tuple[str, ...] = ()
    children: tuple["Rule", ...] = ()

    def __post_init__(self):
        if self.kind == "single":
            if not self.name or not self.helpers or self.children or len(set(self.helpers)) != len(self.helpers):
                raise ValueError("single constraint needs a name and distinct qualified helper identities")
        elif self.kind in {"and", "or", "chain"}:
            if self.name or self.helpers or not self.children or not all(isinstance(c, Rule) for c in self.children):
                raise ValueError("composition requires nonempty child rules only")
        else:
            raise ValueError("supported compositions: single, and, or, chain")


def permissible(rule: Rule, oracle_verdicts: Mapping[str, bool]) -> bool:
    """Evaluate oracle constraint truth, not the agent's self-reported result."""
    if rule.kind == "single":
        value = oracle_verdicts[rule.name]
        if type(value) is not bool:
            raise ValueError("oracle constraint verdicts must be Boolean")
        return value
    values = [permissible(c, oracle_verdicts) for c in rule.children]
    return any(values) if rule.kind == "or" else all(values)


def _witnesses(rule: Rule, calls: Sequence[str], oracle: Mapping[str, bool]) -> set[tuple[int, int]]:
    if not permissible(rule, oracle):
        return set()
    if rule.kind == "single":
        positions = [[i for i, name in enumerate(calls) if name == helper] for helper in rule.helpers]
        return {(min(indices), max(indices)) for indices in product(*positions)}
    options = [_witnesses(child, calls, oracle) for child in rule.children]
    if rule.kind == "or":
        return set().union(*options)
    result = set()
    for intervals in product(*options):
        if rule.kind == "chain" and any(a[1] >= b[0] for a, b in zip(intervals, intervals[1:])):
            continue
        result.add((min(x[0] for x in intervals), max(x[1] for x in intervals)))
    return result


def evaluate_trace(service_rules: Mapping[str, Rule], oracle_verdicts: Mapping[str, bool],
                   calls: Sequence[str], agent_final_state: object, oracle_final_state: object) -> dict:
    """Paper §2.3: permissible actions AND matching DB AND complete procedures.

    Checks EACH invoked service against its preceding helper-call prefix.
    AND allows either order; CHAIN requires strict prerequisite order; OR needs
    a verified true alternative. No service call gives vacuous action/procedure
    checks: a correct refusal still needs the oracle final database to match.
    This does not recreate domain verifiers, tools, agent inference or test data.
    """
    if not service_rules or not all(isinstance(k, str) and k and isinstance(v, Rule) for k, v in service_rules.items()):
        raise ValueError("nonempty service-rule map required")
    if not all(isinstance(c, str) and c for c in calls):
        raise ValueError("qualified tool-call identity strings required")
    action_pass = procedure_pass = True
    services = 0
    for position, call in enumerate(calls):
        if call in service_rules:
            services += 1
            rule = service_rules[call]
            action_pass = permissible(rule, oracle_verdicts) and action_pass
            procedure_pass = bool(_witnesses(rule, calls[:position], oracle_verdicts)) and procedure_pass
    # JSON-exact comparison prevents True==1 from hiding distinct DB values.
    def canonical(value):
        return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    database_pass = canonical(agent_final_state) == canonical(oracle_final_state)
    return {"action_permissibility": action_pass, "database_outcome_match": database_pass,
            "procedure_completeness": procedure_pass, "passed": action_pass and database_pass and procedure_pass,
            "service_calls": services}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("pure CPU protocol diagnostic requires integer seed and device='cpu'")
    a, b = Rule("single", "identity", ("identity(user=1)",)), Rule("single", "credit", ("credit(user=1)",))
    rules = {"loan(user=1)": Rule("chain", children=(a, b))}
    oracle = {"identity": True, "credit": True}
    cases = [(["identity(user=1)", "credit(user=1)", "loan(user=1)"], {"loan": 1}, True),
             (["credit(user=1)", "identity(user=1)", "loan(user=1)"], {"loan": 1}, False),
             (["identity(user=2)", "credit(user=1)", "loan(user=1)"], {"loan": 1}, False),
             (["identity(user=1)", "credit(user=1)", "loan(user=1)"], {"loan": 0}, False)]
    random.Random(seed).shuffle(cases)
    results = [(evaluate_trace(rules, oracle, calls, state, {"loan": 1}), expected)
               for calls, state, expected in cases]
    false_accepts = sum(r["passed"] and not expected for r, expected in results)
    false_success = evaluate_trace(rules, {"identity": True, "credit": False},
        ["identity(user=1)", "credit(user=1)", "loan(user=1)"], {"loan": 1}, {"loan": 1})
    return {"seed": seed, "metrics": {"fixture_cases": len(cases), "observed_pass_cases": sum(r["passed"] for r, _ in results),
        "false_accepts": false_accepts, "model_calls": 0}, "checks": {
        "three_dimensions_conjoined": all(r["passed"] == expected for r, expected in results),
        "chain_order_enforced": any(not r["procedure_completeness"] for r, _ in results),
        "wrong_request_helper_rejected": false_accepts == 0,
        "oracle_refutes_claimed_success": not false_success["passed"] and not false_success["action_permissibility"]}}
