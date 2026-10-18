#!/usr/bin/env python3
"""KnowGPO tiny-policy gradient and DIVERGE CPU observation-protocol diagnostics.

No pretrained models, downloads, APIs or scientific-impact claims. Only KnowGPO
has a CUDA path; DIVERGE accepts explicit synthetic judge observations on CPU.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import statistics
import subprocess
import time

import torch
from torch import nn

from auto_research.post_training import reviewed_oct19 as ops

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("knowgpo", "diverge-ideation")
SOURCES = ("src/auto_research/post_training/reviewed_oct19.py", "scripts/run_oct19_post_components.py")


class TinyPublicPolicy(nn.Module):
    """Only token IDs are accepted; no private knowledge/verifier argument."""
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(16, 8)
        self.head = nn.Linear(8, 16)

    def forward(self, token_ids):
        h = self.embedding(token_ids)
        counts = torch.arange(1, token_ids.shape[1] + 1, device=h.device, dtype=h.dtype)
        return self.head(h.cumsum(1) / counts[None, :, None])


@torch.no_grad()
def sample(model, public_history, device):
    response = ()
    for _ in range(2):
        ids = torch.tensor([public_history + response], device=device, dtype=torch.long)
        response += (int(torch.multinomial(model(ids)[0, -1].softmax(-1), 1)),)
    return response


def score(model, history, response, device):
    ids = torch.tensor([history + response[:-1]], device=device, dtype=torch.long)
    return model(ids)[0, -len(response):]


def snapshot(model):
    return [p.detach().clone() for p in model.parameters()]


def delta(model, initial):
    return math.sqrt(sum(float((p.detach() - q).square().sum()) for p, q in zip(model.parameters(), initial, strict=True)))


def independent_credit_reference(queries, increments, answer, outcomes, omega=.5):
    """Python sets/scalars, independently rebuilding PRIOR-state groups."""
    groups, episodic, gains = {}, [], []
    for i, query in enumerate(queries):
        population = [value for q, value in zip(queries, outcomes, strict=True) if q == query]
        episodic.append((outcomes[i] - statistics.mean(population)) / (statistics.pstdev(population) + 1e-6))
        current, row = set(), []
        for t, bits in enumerate(increments[i]):
            previous = frozenset(current)
            current.update(k for k, value in enumerate(bits) if value)
            row.append(len(current) - len(previous))
            if not answer[i][t]:
                groups.setdefault((query, previous), []).append((i, t))
        gains.append(row)
    process = [[0.] * len(row) for row in increments]
    for positions in groups.values():
        values = [gains[i][t] for i, t in positions]
        for (i, t), value in zip(positions, values, strict=True):
            process[i][t] = (value - statistics.mean(values)) / (statistics.pstdev(values) + 1e-6)
    return [[(1 - omega) * episodic[i] + omega * process[i][t] for t in range(len(row))]
            for i, row in enumerate(increments)]


def independent_policy_reference(current, old, reference, labels, mask, advantages):
    terms = []
    for i in range(len(current)):
        for t in range(len(current[i])):
            if not bool(mask[i, t]):
                continue
            lp = current[i, t].detach().log_softmax(-1).tolist()
            lo = old[i, t].log_softmax(-1).tolist()
            lr = reference[i, t].log_softmax(-1).tolist()
            token, a = int(labels[i, t]), float(advantages[i, t])
            ratio = math.exp(lp[token] - lo[token])
            pg = -min(ratio * a, min(1.2, max(.8, ratio)) * a)
            kl = sum(math.exp(lp[v]) * (lp[v] - lr[v]) for v in range(len(lp)))
            terms.append(pg + .01 * kl)
    return sum(terms) / len(terms)


def run_knowgpo(device, steps):
    model = TinyPublicPolicy().to(device=device, dtype=torch.float64)
    reference = deepcopy(model).eval().requires_grad_(False)
    initial, ref_initial = snapshot(model), snapshot(reference)
    optimizer = torch.optim.SGD(model.parameters(), lr=.06)
    errors, loss_errors, norms, reverse_kls, audit_records = [], [], [], [], []
    for update in range(steps):
        behavior = deepcopy(model).eval().requires_grad_(False)
        queries, outcomes, increments, current_rows, old_rows, ref_rows, label_rows = [], [], [], [], [], [], []
        for problem in range(2):
            # Private exact verifier fixture, never passed to the actor.
            private_document_conditions = ((True, False, False), (False, True, False),
                (False, False, True), (False, False, False))
            for _ in range(6):
                history = (1, 2 + problem)
                cur, old, refs, labels, acquired = [], [], [], [], []
                for turn in range(3):
                    response = sample(behavior, history, device)
                    cur.append(score(model, history, response, device))
                    with torch.no_grad():
                        old.append(score(behavior, history, response, device))
                        refs.append(score(reference, history, response, device))
                    labels.extend(response)
                    if turn < 2:
                        document = response[-1] % 4
                        acquired.append(private_document_conditions[(document + problem) % 4])
                        # Visible document ID is an observation, not the Boolean
                        # verifier state or a gold answer embedded in actor input.
                        history += response + (8 + document,)
                        blank = torch.zeros(1, 16, device=device, dtype=torch.float64)
                        cur.append(blank)
                        old.append(blank)
                        refs.append(blank)
                        labels.append(-1)
                    else:
                        acquired.append((False, False, False))
                        outcomes.append(float(response[-1] % 2 == problem))
                queries.append(f"query-{problem}")
                increments.append(acquired)
                current_rows.append(torch.cat(cur))
                old_rows.append(torch.cat(old))
                ref_rows.append(torch.cat(refs))
                label_rows.append(labels)
        changes = torch.tensor(increments, dtype=torch.bool, device=device)
        valid = torch.ones(12, 3, dtype=torch.bool, device=device)
        answer = torch.tensor([[False, False, True]] * 12, device=device)
        before, after = ops.accumulate_knowledge(changes, valid)
        credit, audit = ops.knowledge_advantages(queries, before, after, valid, answer,
            torch.tensor(outcomes, device=device, dtype=torch.float64))
        expected = torch.tensor(independent_credit_reference(queries, increments, answer.tolist(), outcomes),
            device=device, dtype=torch.float64)
        errors.append(float((credit - expected).abs().max()))
        labels = torch.tensor(label_rows, dtype=torch.long, device=device)
        mask = labels >= 0
        step_ids = torch.tensor([[0, 0, -1, 1, 1, -1, 2, 2]] * 12, device=device)
        advantages = ops.broadcast_step_advantages(credit, step_ids, mask)
        current, old, ref = torch.stack(current_rows), torch.stack(old_rows), torch.stack(ref_rows)
        loss, parts = ops.knowgpo_policy_loss(current, old, ref, labels, mask, advantages)
        loss_errors.append(abs(float(loss.detach()) - independent_policy_reference(current, old, ref, labels, mask, advantages)))
        reverse_kls.append(float(parts["reverse_kl"]))
        optimizer.zero_grad()
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 10., error_if_nonfinite=True)
        if not torch.isfinite(loss) or norm <= 0:
            raise RuntimeError("finite nonzero actual policy gradient required")
        norms.append(float(norm))
        optimizer.step()
        audit_records.append({"update": update, "query_ids": queries, "increments": increments,
            "outcomes": outcomes, "before_states": before.tolist(), "after_states": after.tolist(),
            "groups": audit["groups"], "answer_process_advantages": audit["step_advantages"][answer].tolist()})
    singleton = ops.knowledge_advantages(["solo"], torch.zeros(1, 1, 1, device=device, dtype=torch.bool),
        torch.ones(1, 1, 1, device=device, dtype=torch.bool), torch.ones(1, 1, device=device, dtype=torch.bool),
        torch.zeros(1, 1, device=device, dtype=torch.bool), torch.zeros(1, device=device, dtype=torch.float64))[0]
    return {"metrics": {"parameter_delta_l2": delta(model, initial), "gradient_norm_min": min(norms),
        "optimizer_updates": steps, "credit_reference_max_abs_error": max(errors),
        "loss_reference_max_abs_error": max(loss_errors), "reference_delta_l2": delta(reference, ref_initial),
        "reference_gradient_count": sum(p.grad is not None for p in reference.parameters()),
        "reverse_kl_max": max(reverse_kls), "answer_process_max_abs_credit": float(audit["step_advantages"][answer].abs().max()),
        "observation_credit_max_abs_error": float(advantages[~mask].abs().max()),
        "singleton_negative_control_max_abs_advantage": float(singleton.abs().max()),
        "group_count_last": len(audit["groups"]),
        "non_singleton_group_count_last": sum(len(g["positions"]) > 1 for g in audit["groups"]),
        "actor_receives_private_verifier_state": False}, "group_audit": audit_records}


def independent_set_score(q, distances, order):
    total, seen = 0., []
    for index in order:
        value = min([distances[index][j] for j in seen], default=1.)
        total += q[index] * value
        seen.append(index)
    return total


def run_diverge(seed):
    randomizer = random.Random(seed)
    errors, lower_bound_errors, records, callback_calls = [], [], [], 0
    for instance in range(12):
        cards = [{"id": str(i), "problem_gap": "gap: explicit fixture", "core_claim": "claim fixture",
            "method": "method: explicit fixture", "inspiration": "source fixture"} for i in range(3)]
        votes = [[bool(randomizer.randrange(2)) for _ in range(2)] for _ in cards]
        field_scores = {(i, j): [randomizer.random() for _ in range(3)] for i in range(3) for j in range(i)}
        counts = {"quality": 0, "distance": 0}

        def impact(card, reverse):
            counts["quality"] += 1
            return votes[int(card["id"])][int(reverse)]

        def distance(a, b):
            counts["distance"] += 1
            return field_scores[tuple(sorted((int(a["id"]), int(b["id"])), reverse=True))]

        valid = ops.validate_idea_schema(cards, expected_count=3, has_think_block=True, has_answer_block=True,
            problem_label_valid=lambda s: s.startswith("gap:"), method_label_valid=lambda s: s.startswith("method:"))
        quality, distances = ops.observe_idea_judgments(cards, schema_valid=valid,
            impact_judge=impact, field_distance_judge=distance)
        length = randomizer.randrange(500, 5001)
        result = ops.set_reward(quality, distances, schema_valid=valid, judged_token_length=length)
        reference = .05 + independent_set_score(quality, distances, range(3)) - min(max(length / 1000 - 1, 0), 3)
        errors.append(abs(result["reward"] - reference))
        greedy, greedy_order = ops.creative_utility(quality, distances)
        exact, exact_order = ops.creative_utility(quality, distances, exact=True)
        enumerate_values = []
        for permutation in itertools.permutations(range(3)):
            total = 0.
            for t, i in enumerate(permutation):
                total += .9 ** t * quality[i] * min([distances[i][j] for j in permutation[:t]], default=1.)
            enumerate_values.append(total / (1 + .9 + .9 ** 2))
        errors.append(abs(exact - max(enumerate_values)))
        lower_bound_errors.append(max(0., greedy - exact))
        callback_calls += sum(counts.values())
        records.append({"instance": instance, "explicit_fixture_impact_votes": votes,
            "explicit_fixture_semantic_field_distances": {f"{i},{j}": value for (i, j), value in field_scores.items()},
            "quality_observations": quality, "distances": distances, "judged_token_length": length,
            "reward": result, "greedy_cu_lower_bound": greedy, "greedy_order": greedy_order,
            "exact_cu": exact, "exact_order": exact_order, "fixture_callback_counts": counts})
    q = [1., .5, .8]
    duplicate = [[0.] * 3 for _ in range(3)]
    d = [[0., .9, .1], [.9, 0., .1], [.1, .1, 0.]]
    forward = ops.set_reward(q, d, schema_valid=True, judged_token_length=0)["reward"]
    reverse = ops.set_reward(list(reversed(q)), [list(reversed(row)) for row in reversed(d)],
        schema_valid=True, judged_token_length=0)["reward"]
    # Invalid schema must not call either expensive judge, even with bad inputs.
    def forbidden(*_):
        raise RuntimeError("invalid schema invoked judge")
    invalid = ops.observe_idea_judgments(cards, schema_valid=False, impact_judge=forbidden, field_distance_judge=forbidden)
    return {"metrics": {"reward_and_exact_cu_reference_max_abs_error": max(errors),
        "greedy_lower_bound_violation": max(lower_bound_errors), "fixture_instances": 12,
        "fixture_callback_calls": callback_calls, "duplicate_negative_control_marginal_error":
            abs(ops.set_reward(q, duplicate, schema_valid=True, judged_token_length=0)["set_score"] - q[0]),
        "generation_order_negative_control_abs_difference": abs(forward - reverse),
        "invalid_schema_judge_calls": 0, "invalid_schema_returns_no_observations": invalid == ([], []),
        "actual_model_or_api_judge_used": False, "scientific_quality_measured": False}, "observation_audit": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--steps", type=int, default=3)
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    methods, seeds = args.methods.split(","), [int(v) for v in args.seeds.split(",")]
    if not methods or len(set(methods)) != len(methods) or set(methods) - set(METHODS):
        parser.error("distinct known methods required")
    if not seeds or len(set(seeds)) != len(seeds) or not 1 <= args.steps <= 8:
        parser.error("distinct seeds and 1--8 bounded updates required")
    if args.output.exists():
        parser.error("immutable output exists")
    if args.device == "cuda" and ("diverge-ideation" in methods or not torch.cuda.is_available()):
        parser.error("CUDA requires availability and --methods knowgpo; DIVERGE is CPU-only")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        parser.error("full lowercase code commit required")
    torch.set_num_threads(1)
    started = time.monotonic()
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCES}
    result = {"schema_version": 2, "code_commit": commit, "executed_source_sha256": hashes,
        "device": args.device, "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "formal_comparison_eligible": False, "full_experiment_status": "not_reproduced_high_cost",
        "seeds": seeds, "limits": {"steps": args.steps, "no_downloads": True, "pretrained_checkpoint": None,
            "synthetic_protocol_revision": "oct19-knowledge-credit-and-observed-ideation-v1"}, "components": {}}
    for key in methods:
        rows = []
        for seed in seeds:
            torch.manual_seed(seed)
            value = run_knowgpo(args.device, args.steps) if key == "knowgpo" else run_diverge(seed)
            if not all(math.isfinite(float(v)) for v in value["metrics"].values()):
                raise RuntimeError("nonfinite diagnostic metrics")
            rows.append({"seed": seed, "status": "completed", **value})
        summary = {}
        for name in rows[0]["metrics"]:
            values = [row["metrics"][name] for row in rows]
            summary[name] = all(values) if all(isinstance(v, bool) for v in values) else {
                "mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
        result["components"][key] = {"per_seed": rows, "metrics": summary,
            "dataset": {"id": "synthetic:oct19-knowledge-credit-v1" if key == "knowgpo" else "protocol:oct19-explicit-judge-observations-v1",
                "revision": "sha256:" + hashes[SOURCES[-1]]},
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost"}
    result["elapsed_seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "methods": methods, "device": args.device,
                      "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
