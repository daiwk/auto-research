"""XLGoBench five algorithmic task scorers and bounded structured generators.

Independent Sec.2 / AppendixC implementation, not the official multilingual
template release or a model benchmark. Translations require externally supplied,
human-validated templates; this module does not invent validated translations.
Gold is computed only by the scorer, NEVER sent to the model callback.
"""
from collections import deque
from collections.abc import Callable
from copy import deepcopy
import json
import math
import random

TASKS = ("slt", "dsa", "pr_dsa", "graph_sp", "t_rank")
FIELDS = {"slt": {"start", "initial_wealth", "transactions"},
          "dsa": {"states", "alphabet", "start", "actions", "transitions"},
          "pr_dsa": {"states", "alphabet", "start", "actions", "transitions"},
          "graph_sp": {"nodes", "edges", "source", "target"}, "t_rank": {"nodes", "edges"}}


def _solve(public: dict) -> dict:
    """Scorer-only algorithm; never called by the model/prompt rendering path."""
    task, p = public["task"], public["problem"]
    if task not in TASKS or not isinstance(p, dict) or set(p) != FIELDS[task] or len(json.dumps(p)) > 200_000:
        raise ValueError("known task and bounded public problem required")
    if task == "slt":
        records = p["transactions"]
        if (not 1 <= len(records) <= 128 or any(len(r) != 4 for r in records)
                or len({r[0] for r in records}) != len(records)):
            raise ValueError("bounded uniquely keyed transaction chain required")
        by_source = {r[0]: r[1:] for r in records}
        node, wealth, chain, seen = p["start"], p["initial_wealth"], [p["initial_wealth"]], set()
        while node in by_source:
            if node in seen:
                raise ValueError("cyclic SLT chain")
            seen.add(node)
            target, a, b = by_source[node]
            if any(isinstance(v, bool) or not isinstance(v, int) or not -9 <= v <= 9 for v in (a, b, wealth)):
                raise ValueError("SLT coefficients and wealth must be integers in[-9,9]")
            wealth = a * wealth + b
            if not -9 <= wealth <= 9:
                raise ValueError("SLT wealth outside paper range")
            chain.append(wealth)
            node = target
        if len(seen) != len(records):
            raise ValueError("disconnected SLT transactions")
        return {"chain": chain}
    if task in ("dsa", "pr_dsa"):
        states, actions, transitions = p["states"], p["actions"], p["transitions"]
        if (not 2 <= len(states) <= 64 or len(set(states)) != len(states) or len(actions) > 64
                or any(action not in p["alphabet"] for action in actions) or p["start"] not in states):
            raise ValueError("bounded known automaton states/actions required")
        if (set(transitions) != set(states) or len(set(p["alphabet"])) != len(p["alphabet"])
                or any(set(row) != set(p["alphabet"]) for row in transitions.values())):
            raise ValueError("only declared transition states/actions are public")
        if task == "dsa":
            if len(p["alphabet"]) != len(states):
                raise ValueError("DSA has equal numbers of states and actions")
            state = p["start"]
            for action in actions:
                state = transitions[state][action]
                if state not in states:
                    raise ValueError("unknown next state")
            return {"state": state}
        if len(p["alphabet"]) != 15 or len(states) < 9:
            raise ValueError("Pr-DSA has15 actions and at least9 states for a nontrivial top8")
        probabilities = {state: float(state == p["start"]) for state in states}
        for action in actions:
            following = dict.fromkeys(states, 0.)
            for state in states:
                branches = transitions[state][action]
                if (len(branches) != 2 or any(v not in states or not math.isfinite(prob) or not 0 <= prob <= 1 for v, prob in branches)
                        or not math.isclose(sum(prob for _, prob in branches), 1., abs_tol=1e-12)):
                    raise ValueError("two normalized probabilistic successors required")
                for destination, probability in branches:
                    following[destination] += probabilities[state] * probability
            probabilities = following
        ranked = sorted(states, key=lambda state: (-probabilities[state], state))
        if math.isclose(probabilities[ranked[7]], probabilities[ranked[8]], rel_tol=0., abs_tol=1e-12):
            raise ValueError("top8 boundary is tied; no unique answer set")
        return {"states": ranked[:8]}
    nodes, edges = p["nodes"], p["edges"]
    if (not 2 <= len(nodes) <= 128 or len(set(nodes)) != len(nodes) or len(edges) > 2048
            or len({tuple(e) for e in edges}) != len(edges)
            or any(len(e) != 2 or e[0] not in nodes or e[1] not in nodes or e[0] == e[1] for e in edges)):
        raise ValueError("bounded simple known-node graph required")
    adjacency = {node: [] for node in nodes}
    if task == "graph_sp":
        for a, b in edges:
            adjacency[a].append(b)
            adjacency[b].append(a)
        source, target = p["source"], p["target"]
        distance, ways, parent = {source: 0}, {source: 1}, {}
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for other in adjacency[node]:
                if other not in distance:
                    distance[other], ways[other], parent[other] = distance[node] + 1, ways[node], node
                    queue.append(other)
                elif distance[other] == distance[node] + 1:
                    ways[other] += ways[node]
        if target not in distance or ways[target] != 1:
            raise ValueError("benchmark requires a unique shortest path")
        path, node = [target], target
        while node != source:
            node = parent[node]
            path.append(node)
        return {"path": path[::-1]}
    if len(edges) != 3 * len(nodes):
        raise ValueError("T-Rank preserves paper1:3 node/edge ratio")
    indegree = dict.fromkeys(nodes, 0)
    for a, b in edges:
        adjacency[a].append(b)
        indegree[b] += 1
    ranking = []
    while len(ranking) < len(nodes):
        ready = [node for node in nodes if indegree[node] == 0 and node not in ranking]
        if len(ready) != 1:
            raise ValueError("T-Rank requires a unique acyclic total order")
        node = ready[0]
        ranking.append(node)
        for other in adjacency[node]:
            indegree[other] -= 1
    return {"ranking": ranking}


def make_case(task: str, seed: int, *, complexity: int = 12) -> dict:
    """Small structured cases, not the official distribution or seven-language prompts.

    Graph-SP uses the exact AppendixC.1 backbone+bypasses with rho0 (no noise).
    T-Rank starts with a Hamiltonian path and adds only transitive edges to3N.
    """
    if task not in TASKS or not isinstance(complexity, int) or not 9 <= complexity <= 32:
        raise ValueError("known task and local bounded complexity9..32 required")
    if task == "graph_sp" and complexity != 12:
        raise ValueError("local graph_sp generator fixes12 nodes; not a scaling implementation")
    rng = random.Random(seed)
    nodes = [f"A{i:04d}" for i in range(complexity)]
    if task == "slt":
        wealth = initial = rng.randrange(-9, 10)
        transactions = []
        for i in range(complexity - 1):
            choices = [(a, b) for a in range(-9, 10) for b in range(-9, 10) if -9 <= a * wealth + b <= 9]
            a, b = rng.choice(choices)
            transactions.append([nodes[i], nodes[i + 1], a, b])
            wealth = a * wealth + b
        rng.shuffle(transactions)
        problem = {"start": nodes[0], "initial_wealth": initial, "transactions": transactions}
    elif task in ("dsa", "pr_dsa"):
        alphabet = [f"K{i:03d}" for i in range(complexity if task == "dsa" else 15)]
        transitions = {}
        for node in nodes:
            transitions[node] = {}
            for action in alphabet:
                if task == "dsa":
                    transitions[node][action] = rng.choice(nodes)
                else:
                    a, b = rng.sample(nodes, 2)
                    probability = rng.uniform(.05, .95)
                    transitions[node][action] = [[a, probability], [b, 1 - probability]]
        problem = {"states": nodes, "alphabet": alphabet, "start": nodes[0],
                   "actions": [rng.choice(alphabet) for _ in range(15)], "transitions": transitions}
    elif task == "graph_sp":
        # d3, nc2, ce2, rho0: unique length3 path, bypasses length5.
        nodes = [f"A{i:04d}" for i in range(12)]
        edges = [[nodes[i], nodes[i + 1]] for i in range(3)]
        for chain in ([nodes[0], *nodes[4:8], nodes[3]], [nodes[0], *nodes[8:12], nodes[3]]):
            edges.extend([a, b] for a, b in zip(chain, chain[1:]))
        rng.shuffle(edges)
        problem = {"nodes": nodes, "edges": edges, "source": nodes[0], "target": nodes[3]}
    else:
        order = nodes.copy()
        rng.shuffle(order)
        edges = {(order[i], order[i + 1]) for i in range(complexity - 1)}
        candidates = [(order[i], order[j]) for i in range(complexity) for j in range(i + 2, complexity)]
        rng.shuffle(candidates)
        edges.update(candidates[:3 * complexity - len(edges)])
        edges = [list(edge) for edge in sorted(edges)]
        rng.shuffle(edges)
        problem = {"nodes": nodes, "edges": edges}
    public = {"task": task, "problem": problem}
    _solve(public)  # Validate construction; never attach the computed answer.
    return public


def score_response(public: dict, response: str | dict) -> bool:
    """Whole JSON answer exact match; Pr-DSA ignores order but rejects duplicates."""
    if isinstance(response, str):
        try:
            response = json.loads(response)
        except (ValueError, TypeError):
            return False
    expected = _solve(public)
    if not isinstance(response, dict) or set(response) != set(expected):
        return False
    if public["task"] == "pr_dsa":
        states = response.get("states")
        return isinstance(states, list) and len(states) == 8 and all(isinstance(s, str) for s in states) and set(states) == set(expected["states"])
    # Bool is not accepted as an integer wealth, despite Python True==1.
    if public["task"] == "slt" and (not isinstance(response.get("chain"), list) or any(type(x) is not int for x in response["chain"])):
        return False
    return response == expected


def evaluate(public: dict, model: Callable[[dict], str | dict]) -> dict:
    """Pass ONLY a copied task/problem payload; private answers remain in scorer."""
    if set(public) != {"task", "problem"}:
        raise ValueError("public payload must have exactly task/problem; no gold fields")
    _solve(public)
    response = model(deepcopy(public))
    return {"correct": score_response(public, response), "task": public["task"]}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU protocol only")
    cases = [make_case(task, seed, complexity=12) for task in TASKS]
    positives = sum(score_response(case, _solve(case)) for case in cases)
    wrong = sum(score_response(case, {"not_an_answer": []}) for case in cases)
    seen = []

    def blind_callback(payload):
        seen.append(deepcopy(payload))
        payload["problem"].clear()  # A callback cannot mutate the scorer's input.
        return {"not_an_answer": []}

    before = deepcopy(cases)
    model_correct = sum(evaluate(case, blind_callback)["correct"] for case in cases)
    pr = cases[2]
    permuted = list(reversed(_solve(pr)["states"]))
    checks = {"all_five_exact_algorithmic_scorers": positives == 5 and wrong == 0,
              "probabilistic_top8_order_invariant": score_response(pr, {"states": permuted}),
              "no_gold_in_model_payload": all(set(payload) == {"task", "problem"} for payload in seen),
              "callback_cannot_mutate_scorer_case": cases == before,
              "wrong_model_not_reported_success": model_correct == 0}
    if not all(checks.values()):
        raise RuntimeError(f"XLGoBench protocol contract failed: {checks}")
    return {"seed": seed, "metrics": {"scorer_positive_controls": positives, "scorer_wrong_controls_accepted": wrong,
        "blind_fixture_model_correct": model_correct, "model_payloads_without_gold": len(seen), "task_families": 5,
        "pretrained_model_calls": 0, "human_validated_translation_templates_executed": 0}, "checks": checks}
