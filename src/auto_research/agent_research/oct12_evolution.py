"""Executable October 9 evolution controllers; no registry or gold access."""

from __future__ import annotations
from dataclasses import dataclass
import ast
import math
import random


@dataclass(frozen=True)
class Edit:
    path: str
    old: str
    new: str


@dataclass(frozen=True)
class Evaluation:
    score: float
    trace: tuple[dict, ...]
    valid: bool = True
    mechanism_ran: bool = True


@dataclass
class HarnessNode:
    identifier: str
    files: dict[str, str]
    evaluation: Evaluation
    parent: str | None = None
    depth: int = 0
    donor: str | None = None


@dataclass(frozen=True)
class Trajectory:
    role: str
    mode: str
    messages: tuple[dict[str, str], ...]
    response: str
    reward: float
    valid: bool
    truncated: bool = False
    segments: tuple = ()


def apply_edits(files, edits):
    """Edit only existing candidate source, never a host path; AST is not exec."""
    edits = tuple(edits)
    if not edits:
        raise ValueError("empty/no-op edit sequence")
    result = dict(files)
    for edit in edits:
        if edit.path not in result or edit.path != "agent.py":
            raise ValueError("only candidate agent.py edits are authorized")
        if not edit.old or result[edit.path].count(edit.old) != 1:
            raise ValueError("edit must identify one exact source occurrence")
        if edit.new == edit.old:
            raise ValueError("no-op edit")
        result[edit.path] = result[edit.path].replace(edit.old, edit.new, 1)
        if len(result[edit.path].encode()) > 65536:
            raise ValueError("candidate source exceeds 64 KiB")
        ast.parse(result[edit.path])
    return result


def recover_prefix(files, edits, continue_from):
    current, prefix = dict(files), []
    for edit in edits:
        try:
            current = apply_edits(current, (edit,))
        except (ValueError, SyntaxError):
            suffix = tuple(continue_from(current, tuple(prefix)))
            return apply_edits(current, suffix), tuple(prefix) + suffix, True
        prefix.append(edit)
    return current, tuple(prefix), False


def parent_distribution(nodes, *, root_share=.2, epsilon=.05):
    if not 0 < root_share < 1 or epsilon <= 0:
        raise ValueError("invalid parent distribution")
    root = next(node for node in nodes if node.parent is None)
    others = [node for node in nodes if node is not root]
    if not others:
        return {root.identifier: 1.}
    weights = [epsilon + abs(node.evaluation.score - .5) for node in others]
    total = sum(weights)
    return {root.identifier: root_share, **{
        node.identifier: (1 - root_share) * weight / total
        for node, weight in zip(others, weights)}}


def retained_pool(nodes, *, per_depth=4, seed=42):
    if per_depth < 2:
        raise ValueError("pool needs space for elites and repair candidates")
    rng = random.Random(seed)
    pool = [next(node for node in nodes if node.parent is None)]
    for depth in sorted({node.depth for node in nodes if node.depth}):
        group = sorted([n for n in nodes if n.depth == depth and n.evaluation.valid],
                       key=lambda node: node.evaluation.score, reverse=True)
        elite = group[:max(1, per_depth // 2)]
        rest = group[len(elite):]
        pool.extend(elite + rng.sample(rest, min(per_depth - len(elite), len(rest))))
    return pool


class Evo2:
    """Shared Proposer/Reflector tree, crossover, SFT and interleaved GRPO.

    Evaluator executes candidate source with a fixed executor, fail-closed.
    A frozen counterpart is refreshed once per RL round, never per sample.
    """
    def __init__(self, policy, evaluate, initial_files, *, seed=42, split="validation"):
        if split != "validation":
            raise ValueError("harness selection is validation-only")
        self.policy, self.evaluate = policy, evaluate
        self.rng = random.Random(seed)
        self.nodes = [HarnessNode("root", initial_files, evaluate(initial_files))]
        self.trajectories, self.strategies, self.audit = [], [], []

    def parent(self):
        pool = retained_pool(self.nodes, seed=self.rng.randrange(2**31))
        probabilities = parent_distribution(pool)
        return self.rng.choices(pool, [probabilities[n.identifier] for n in pool])[0]

    def propose(self, policy, parent, directive=None, donor=None):
        response, edits, messages, truncated = policy.propose(parent, directive, donor)
        recovered = False
        try:
            files, edits, recovered = recover_prefix(parent.files, edits,
                lambda current, prefix: policy.continue_edits(current, prefix, directive))
            evaluation = self.evaluate(files)
            reward = evaluation.score - parent.evaluation.score if evaluation.valid else -1.
            valid = evaluation.valid
            node = HarnessNode("node-" + str(len(self.nodes)), files, evaluation,
                               parent.identifier, parent.depth + 1, donor)
            if evaluation.valid:
                self.nodes.append(node)
        except (ValueError, SyntaxError):
            node, reward, valid = parent, -1., False
        trajectory = Trajectory("proposer", "B" if directive else "A", tuple(messages),
                                response, reward, valid, truncated)
        self.trajectories.append(trajectory)
        self.audit.append({"role": "proposer", "recovered_prefix": recovered,
                           "reward": reward, "node": node.identifier})
        return node, trajectory

    def reflect(self, policy, candidate, counterpart, *, strategies):
        decision, response, messages, truncated = policy.reflect(candidate, strategies)
        action = decision["action"]
        directive, donor = decision.get("directive"), decision.get("donor")
        valid = action in {"keep", "revise", "crossover"}
        valid = valid and (action == "keep" or bool(directive))
        if action == "crossover":
            valid = valid and donor in {s["identifier"] for s in strategies}
        revised = candidate
        if valid and action != "keep":
            revised, directed_trajectory = self.propose(counterpart, candidate, directive, donor)
            valid = directed_trajectory.valid
        reward = revised.evaluation.score - candidate.evaluation.score if valid else -1.
        if reward > 0 and not revised.evaluation.mechanism_ran:
            reward = 0.
        trajectory = Trajectory("reflector", "crossover" if strategies else "local",
                                tuple(messages), response, reward, valid, truncated,
                                tuple(decision.get("training_segments", ())))
        self.trajectories.append(trajectory)
        self.audit.append({"role": "reflector", "action": action, "reward": reward,
                           "donor": donor, "valid": valid})
        return revised, trajectory

    def collect(self, iterations):
        for _ in range(iterations):
            parent = self.parent()
            candidate, _ = self.propose(self.policy, parent)
            revised, _ = self.reflect(self.policy, candidate, self.policy, strategies=self.strategies)
            if revised.identifier != parent.identifier and revised.evaluation.valid:
                self.strategies.append({"identifier": revised.identifier,
                    "description": self.policy.extract_strategy(parent, revised),
                    "source": revised.files, "observed_score": revised.evaluation.score})

    def train(self, *, warmup_iterations=2, rounds=2, group_size=2, steps=1):
        if group_size < 2 or rounds < 1:
            raise ValueError("role groups require alternatives and a training round")
        self.collect(warmup_iterations)
        selected = [t for t in self.trajectories if t.valid and t.reward >= 0 and not t.truncated]
        if {t.role for t in selected} != {"proposer", "reflector"}:
            raise RuntimeError("no native valid warm-start trajectory for both roles; no oracle fallback")
        warmup = self.policy.sft(selected, steps=steps)
        training = []
        for round_id in range(rounds):
            counterpart = self.policy.snapshot()
            for step in range(steps):
                parent = self.parent()
                directive = None
                if step % 2:
                    decision, _, _, _ = counterpart.reflect(parent, self.strategies)
                    directive = decision.get("directive")
                    if not directive:
                        directive = counterpart.revision_directive(parent)
                proposer_group = [self.propose(self.policy, parent, directive)[1]
                                  for _ in range(group_size)]
                candidate = self.parent()
                strategies = self.strategies if step % 2 else []
                reflector_group = [self.reflect(self.policy, candidate, counterpart,
                                               strategies=strategies)[1]
                                   for _ in range(group_size)]
                training.append(self.policy.interleaved_grpo(proposer_group, reflector_group,
                                                             round_id=round_id))
        return {"warmup": warmup, "training": training, "nodes": len(self.nodes),
            "strategies": len(self.strategies), "best_validation_score": max(
                n.evaluation.score for n in self.nodes), "audit": self.audit}


@dataclass(frozen=True)
class Feedback:
    context: str
    candidate: str
    prediction: float
    outcome: float
    observation: str
    policy_version: str
    model_version: str
    split: str = "train"


class RSIAnything:
    """Version-aware adaptation, policy revision and compatibility retention."""
    def __init__(self, backend, verify, *, initial_workflow, predictor,
                 error_threshold=.15, minimum_feedback=2):
        self.backend, self.verify = backend, verify
        self.workflow, self.predictor = initial_workflow, predictor
        self.error_threshold, self.minimum_feedback = error_threshold, minimum_feedback
        self.history, self.audit = [], []

    def select(self, context, workflow, predictor, candidates):
        proposals = self.backend.candidates(context, workflow, candidates)
        if not proposals:
            raise RuntimeError("policy produced no candidate")
        predictions = [self.backend.predict(predictor, context, item) for item in proposals]
        index = max(range(len(proposals)), key=predictions.__getitem__)
        return proposals[index], predictions[index]

    def error(self, predictor, records):
        if not records:
            return math.inf
        # Recompute with current predictor: do not mix obsolete-version scores.
        return sum((self.backend.predict(predictor, r.context, r.candidate) - r.outcome)**2
                   for r in records) / len(records)

    def gate(self, workflow, predictor, validation, candidates, *, return_records=False):
        scores, records = [], []
        for context in validation:
            candidate, prediction = self.select(context, workflow, predictor, candidates)
            evaluation = self.verify(context, candidate)
            scores.append(evaluation.score)
            records.append(Feedback(context,candidate,prediction,evaluation.score,str(evaluation.trace),
                self.backend.version(workflow),self.backend.version(predictor),"validation"))
        score = sum(scores) / len(scores)
        return (score,records) if return_records else score

    def run(self, train, validation, *, rounds=2, candidates=2, adaptation_steps=2):
        if not train or not validation or set(train) & set(validation):
            raise ValueError("nonempty disjoint train/validation contexts required")
        for cycle in range(rounds):
            for context in train:
                candidate, prediction = self.select(context, self.workflow, self.predictor, candidates)
                observed = self.verify(context, candidate)
                self.history.append(Feedback(context, candidate, prediction, observed.score,
                    str(observed.trace), self.backend.version(self.workflow),
                    self.backend.version(self.predictor)))
            old_score,old_records = self.gate(self.workflow,self.predictor,validation,candidates,
                                              return_records=True)
            proposed_workflow = self.backend.revise_workflow(self.workflow, self.history)
            policy_score = self.gate(proposed_workflow, self.predictor, validation, candidates)
            policy_accept = policy_score >= old_score and proposed_workflow != self.workflow
            current_error = self.error(self.predictor, self.history)
            reliability = ("insufficient" if len(self.history) < self.minimum_feedback else
                           "unreliable" if current_error > self.error_threshold else "reliable")
            proposed_model, training = self.predictor, None
            if reliability == "unreliable":
                proposed_model, training = self.backend.adapt(self.predictor, self.history,
                                                             steps=adaptation_steps)
            gate_records = []
            for context in validation:
                candidate, prediction = self.select(context, self.workflow, self.predictor, candidates)
                observed = self.verify(context, candidate)
                gate_records.append(Feedback(context, candidate, prediction, observed.score,
                    str(observed.trace), self.backend.version(self.workflow),
                    self.backend.version(self.predictor), "validation"))
            model_accept = proposed_model is not self.predictor and (
                self.error(proposed_model, gate_records) <= self.error(self.predictor, gate_records))
            pair_workflow = proposed_workflow if policy_accept else self.workflow
            pair_model = proposed_model if model_accept else self.predictor
            pair_score,pair_records = self.gate(pair_workflow,pair_model,validation,candidates,
                                               return_records=True)
            old_pair_error = self.error(self.predictor,old_records)
            pair_error = self.error(pair_model,pair_records)
            pair_accept = pair_score >= old_score and pair_error <= old_pair_error
            if pair_accept:
                self.workflow, self.predictor = pair_workflow, pair_model
            self.audit.append({"cycle": cycle, "reliability": reliability,
                "current_version_prediction_error": current_error, "policy_component_accepted": policy_accept,
                "model_component_accepted": model_accept, "pair_accepted": pair_accept,
                "old_validation_score": old_score, "pair_validation_score": pair_score,
                "old_pair_prediction_error":old_pair_error,"proposed_pair_prediction_error":pair_error,
                "training": training, "policy_version": self.backend.version(self.workflow),
                "model_version": self.backend.version(self.predictor)})
        return {"rounds": rounds, "feedback_records": len(self.history), "audit": self.audit}


def bradley_terry(count, comparisons, *, steps=100):
    import torch
    if count < 2 or not comparisons:
        raise ValueError("at least two candidates and comparisons required")
    scores = torch.zeros(count, requires_grad=True)
    optimizer = torch.optim.Adam([scores], lr=.1)
    for _ in range(steps):
        optimizer.zero_grad()
        loss = torch.stack([torch.nn.functional.binary_cross_entropy_with_logits(
            scores[i] - scores[j], torch.tensor(float(p))) for i, j, p in comparisons]).mean()
        loss.backward()
        optimizer.step()
        with torch.no_grad():
            scores.sub_(scores.mean())
    values = scores.detach()
    spread = values.max() - values.min()
    return ((values - values.min()) / spread if spread > 1e-9 else
            torch.full_like(values, .5)).tolist()


class Janus:
    """Graph-frontier predictions before execution; five evolving skill sets."""
    def __init__(self, backend, execute, *, initial_evidence):
        self.backend, self.execute = backend, execute
        self.graph = [{"id": "root", "parents": [], "proposal": "initial",
                       "status": "executed", "evidence": initial_evidence}]
        self.skills = {key: "" for key in ("intra", "cross", "prediction", "exploration", "coordination")}
        self.audit = []

    def tournament(self, proposals, remaining):
        comparisons = {key: [] for key in ("VI", "IG", "EV")}
        pairs = [(i, i + 1) for i in range(len(proposals) - 1)]
        for i, j in pairs:
            for criterion in comparisons:
                probability = self.backend.preference(proposals[i], proposals[j], criterion,
                    self.graph, self.skills, remaining)
                if not 0 <= probability <= 1:
                    raise ValueError("world-model preference outside [0,1]")
                comparisons[criterion].append((i, j, probability))
        scores = {criterion: bradley_terry(len(proposals), records)
                  for criterion, records in comparisons.items()}
        unpaired = [(i, j) for i in range(len(proposals)) for j in range(i + 1, len(proposals))
                    if (i, j) not in pairs]
        if unpaired:
            i, j = min(unpaired, key=lambda pair: sum(abs(v[pair[0]] - v[pair[1]])
                         for v in scores.values()))
            for criterion in comparisons:
                probability = self.backend.preference(proposals[i], proposals[j], criterion,
                    self.graph, self.skills, remaining)
                comparisons[criterion].append((i, j, probability))
                scores[criterion] = bradley_terry(len(proposals), comparisons[criterion])
        return scores, comparisons

    def run(self, *, budget=3, candidates=3):
        if budget < 1 or candidates < 2:
            raise ValueError("positive budget and competing proposals required")
        for iteration in range(budget):
            remaining = budget - iteration
            proposals = self.backend.proposals(self.graph, self.skills, remaining, candidates)
            if len(proposals) != candidates:
                raise ValueError("proposal count mismatch")
            scores, comparisons = self.tournament(proposals, remaining)
            beta, gamma = self.backend.exploration_weights(self.graph, self.skills, remaining)
            if min(beta, gamma) < 0 or not all(map(math.isfinite, (beta, gamma))):
                raise ValueError("nonnegative finite exploration weights required")
            def priority():
                return [(scores["VI"][i] + beta * scores["IG"][i] + gamma * scores["EV"][i]) /
                        (1 + beta + gamma) for i in range(candidates)]
            priorities = priority()
            selected = max(range(candidates), key=priorities.__getitem__)
            proposal = self.backend.debate(proposals[selected], scores, self.graph, self.skills)
            refined = proposal != proposals[selected]
            if refined:
                proposals[selected] = proposal
                scores, comparisons = self.tournament(proposals, remaining)
                priorities = priority()
                selected = max(range(candidates), key=priorities.__getitem__)
            ids = []
            for index, candidate in enumerate(proposals):
                identifier = "proposal-" + str(len(self.graph))
                ids.append(identifier)
                self.graph.append({"id": identifier, "parents": candidate["parents"],
                    "proposal": candidate["proposal"], "predictions": {
                        key: value[index] for key, value in scores.items()},
                    "priority": priorities[index], "status": "open" if index == selected else "pruned"})
            evidence = self.execute(proposals[selected], self.graph, self.skills)
            next(node for node in self.graph if node["id"] == ids[selected]).update(
                status="executed", evidence=evidence)
            updated = self.backend.evolve_skills(self.skills, self.graph,
                {"beta": beta, "gamma": gamma, "remaining": remaining})
            if set(updated) != set(self.skills):
                raise ValueError("five complete research/prediction/coordination skill sets required")
            self.skills = updated
            self.audit.append({"iteration": iteration, "selected": ids[selected],
                "beta": beta, "gamma": gamma, "remaining": remaining,
                "comparisons": comparisons, "debate_refined": refined, "evidence": evidence})
        return {"graph": self.graph, "skills": self.skills, "audit": self.audit}
