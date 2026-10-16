#!/usr/bin/env python3
"""Six bounded post-training component diagnostics, with real byte-policy updates.

No pretrained model, paper benchmark, semantic mask annotator or long SIF rollout
is downloaded. A supplied immutable public text corpus is the only external data.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import time

import torch
from torch import nn
from torch.nn import functional as F

from auto_research.post_training import cce_opd, ggpo, sif, stopd, tf_opd, waypoint_opd

METHODS = ("tf-opd", "waypoint-opd", "ggpo", "stopd", "cce-opd", "sif")
PAPERS = dict(zip(METHODS, ("2610.22236", "2610.21601", "2610.20814", "2610.21337", "2610.21195", "2610.21392"), strict=True))
EOS = 256


class BytePolicy(nn.Module):
    """Causal cumulative-embedding policy; no checkpoint or heuristic logits."""
    def __init__(self, width=24):
        super().__init__()
        self.embedding = nn.Embedding(257, width)
        self.head = nn.Linear(width, 257)

    def forward(self, ids):
        values = self.embedding(ids)
        lengths = torch.arange(1, ids.shape[1] + 1, device=ids.device, dtype=values.dtype)
        hidden = values.cumsum(1) / lengths[None, :, None]
        return self.head(hidden)


def frozen_copy(model):
    return deepcopy(model).eval().requires_grad_(False)


def parameter_delta(model, before):
    return sum(float((p.detach() - q).square().sum()) for p, q in zip(model.parameters(), before, strict=True)) ** .5


def parameters(model):
    return [p.detach().clone() for p in model.parameters()]


def train_text(model, corpus, steps):
    model.train().requires_grad_(True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=.01)
    width = 24
    for _ in range(steps):
        starts = torch.randint(len(corpus) - width - 1, (8,), device=corpus.device)
        ids = torch.stack([corpus[s:s + width] for s in starts])
        # Explicit EOS at a short training segment boundary. Actual generation
        # still samples EOS from the policy; it is never appended by the sampler.
        target = torch.cat((ids[:, 1:], torch.full((len(ids), 1), EOS, device=ids.device, dtype=torch.long)), -1)
        loss = F.cross_entropy(model(ids).reshape(-1, 257), target.reshape(-1))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return model.eval()


@torch.no_grad()
def sample_group(model, prompt, *, count, max_tokens, cutoffs=None):
    """Autoregressive sampling; EOS counts as valid, post-EOS padding does not."""
    model.eval()
    prefix = prompt.repeat(count, 1)
    ids = prefix.clone()
    active = torch.ones(count, dtype=torch.bool, device=ids.device)
    cutoffs = torch.full((count,), max_tokens, device=ids.device, dtype=torch.long) if cutoffs is None else cutoffs
    masks, eos_count = [], 0
    for position in range(max_tokens):
        active = active & (position < cutoffs)
        if not active.any():
            break
        token = torch.multinomial(model(ids)[:, -1].softmax(-1), 1)
        token = torch.where(active[:, None], token, torch.zeros_like(token))
        masks.append(active.clone())
        ids = torch.cat((ids, token), -1)
        ended = active & (token[:, 0] == EOS)
        eos_count += int(ended.sum())
        active = active & ~ended
    mask = torch.stack(masks, -1)
    return ids, mask, eos_count


def scores(model, ids, prompt_length):
    logits = model(ids)[:, prompt_length - 1:-1]
    targets = ids[:, prompt_length:]
    sampled = logits.log_softmax(-1).gather(-1, targets.unsqueeze(-1)).squeeze(-1)
    return logits, sampled, targets


def heldout_nll(model, source):
    model.eval()
    with torch.no_grad():
        ids = source[:129][None, :]
        return float(F.cross_entropy(model(ids[:, :-1]).reshape(-1, 257), ids[:, 1:].reshape(-1)))


def rl_snapshots(initial, prompt, max_tokens):
    """One true, tiny RL trajectory; byte-parity reward is diagnostic, not quality."""
    learner = deepcopy(initial).train().requires_grad_(True)
    snapshots = [frozen_copy(learner)]
    optimizer = torch.optim.SGD(learner.parameters(), lr=.04)
    for step in range(2):
        for _ in range(16):
            ids, mask, _ = sample_group(learner, prompt, count=4, max_tokens=max_tokens)
            reward = (ids[:, prompt.shape[1]] % 2 == 0).float()
            if reward.min() != reward.max():
                break
        else:
            raise RuntimeError("bounded teacher RL collection found no mixed byte-parity group")
        learner.train()
        _, lp, _ = scores(learner, ids, prompt.shape[1])
        advantage = (reward - reward.mean()).detach()
        loss = -(advantage * lp.masked_fill(~mask, 0).sum(-1) / mask.sum(-1)).mean()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        snapshots.append(frozen_copy(learner))
    return snapshots, [{"run_id": "tiny-byte-parity-rl", "step": s} for s in range(3)]


def run_seed(args, seed, train, validation, test, selected):
    torch.manual_seed(seed)
    base = train_text(BytePolicy().to(args.device), train, args.teacher_steps)
    # Specialists share exactly one base; different disjoint public training
    # shards produce actual changes. This is SFT, not the paper's RL specialists.
    split = len(train) // 2
    teachers = [train_text(deepcopy(base), shard, 4) for shard in (train[:split], train[split:])]
    teachers = [frozen_copy(t) for t in teachers]
    teacher_before = [parameters(t) for t in teachers]
    prompt = train[:16][None, :]
    snapshot_models, lineage = rl_snapshots(base, prompt, min(12, args.max_tokens)) if "waypoint-opd" in selected else (None, None)
    snapshot_before = [parameters(t) for t in snapshot_models] if snapshot_models else []
    outcomes = {}

    if "tf-opd" in selected:
        statistics, audits = [], []
        for d, teacher in enumerate(teachers):
            rollouts = []
            for i in range(24):
                start = 32 * i + d * 1000
                rollout = tf_opd.sample_teacher_rollout(teacher, train[start:start + 16][None, :],
                    teacher_id=f"tiny-specialist-{d}", eos_token_id=EOS, max_new_tokens=64,
                    decode=lambda ids: bytes(t for t in ids if t < 256).decode("utf-8", errors="replace"))
                rollouts.append(rollout)
                if sum(tf_opd.retain_rollout(r) for r in rollouts) >= 4:
                    break
            grams, audit = tf_opd.collect_teacher_grams(teacher, rollouts, teacher_id=f"tiny-specialist-{d}")
            statistics.append(grams)
            audits.append(audit)
        fused, diagnostics = tf_opd.fuse_models(base, teachers, statistics)
        delta = parameter_delta(fused, parameters(base))
        if delta <= 0:
            raise RuntimeError("TF-OPD must actually change the fused parameters")
        outcomes["tf-opd"] = {"seed": seed, "parameter_delta_l2": delta,
            "baseline_validation_nll": heldout_nll(base, validation),
            "final_validation_nll": heldout_nll(fused, validation),
            "final_test_nll": heldout_nll(fused, test), "teacher_rollout_audits": audits,
            "linear_layers": diagnostics, "method_optimizer_updates": 0,
            "specialists": "same base; four SFT updates each, not RL specialists",
            "correctness_filter": "unavailable on unlabeled text; termination/loop filters only"}

    for method in selected:
        if method == "tf-opd":
            continue
        student = deepcopy(base).train().requires_grad_(True)
        reference = frozen_copy(student)
        initial_parameters = parameters(student)
        initial_nll = heldout_nll(student, validation)
        optimizer = torch.optim.SGD(student.parameters(), lr=.03)
        schedule = stopd.STOPDSchedule(args.max_tokens, max(1, args.max_tokens // 4)) if method == "stopd" else None
        policies = ggpo.GGPOPolicies.from_learner(student, refresh_interval=2) if method == "ggpo" else None
        if policies:
            policies.sync_behavior(student)
        history, generated, natural_eos, rejected_groups = [], 0, 0, 0
        for step in range(args.steps):
            local_prompt = train[128 + 32 * step:144 + 32 * step][None, :]
            if method == "cce-opd":
                premise = "The number n is even."
                question = "Let n be a positive integer. " + premise + " What is n modulo 2?\nPublic context:\n" + bytes(local_prompt[0].tolist()).decode("ascii", errors="replace")
                start = question.index(premise)
                pair = cce_opd.ConditionPair.from_reviewed_span(question, (start, start + len(premise)), semantic_reviewed=True)
                local_prompt = torch.tensor(list(question.encode("utf-8")), dtype=torch.long, device=args.device)[None, :]
            plan = schedule.begin_batch(4, device=args.device) if schedule else None
            source = policies.behavior if policies else student
            for attempt in range(16):
                ids, mask, eos_count = sample_group(source, local_prompt, count=4, max_tokens=args.max_tokens,
                    cutoffs=plan.cutoffs if plan else None)
                generated += int(mask.sum())
                natural_eos += eos_count
                with torch.no_grad():
                    old_logits, old_lp, sampled_ids = scores(source, ids, local_prompt.shape[1])
                    _, ref_lp, _ = scores(reference if not policies else policies.reference, ids, local_prompt.shape[1])
                    if method == "ggpo":
                        rewards = (sampled_ids[:, 0] % 2 == 0).float()[None, :]
                        usable = rewards.min() != rewards.max()
                    elif method == "sif":
                        certainties = sif.token_self_certainty(old_logits)[None, :]
                        default_credit = sif.prepare_credit(certainties, mask[None, :])
                        diagnostic_config = sif.VotingConfig(windows=2, width=4, minimum_stride=2, window_wins=2)
                        credit = sif.prepare_credit(certainties, mask[None, :], config=diagnostic_config)
                        usable = credit.retained_groups.any()
                    else:
                        usable = True
                if usable:
                    break
                rejected_groups += 1
            else:
                raise RuntimeError(f"bounded {method} collection produced no usable group")

            with torch.no_grad():
                if method == "waypoint-opd":
                    teacher_logits = [scores(t, ids, local_prompt.shape[1])[0] for t in snapshot_models]
                    credit = waypoint_opd.prepare_credit(old_logits, *teacher_logits, sampled_ids, ref_lp, mask,
                        top_k=16, snapshot_identities=lineage)
                elif method == "cce-opd":
                    def dual_score(question_view, prefix):
                        view_prompt = torch.tensor(list(question_view.encode("utf-8")), dtype=torch.long, device=args.device)[None, :].repeat(4, 1)
                        view_ids = torch.cat((view_prompt, prefix), -1)
                        return scores(teachers[0], view_ids, view_prompt.shape[1])[0]
                    full, masked = cce_opd.score_teacher_views(dual_score, pair, sampled_ids)
                    credit = cce_opd.prepare_credit(old_logits, full, masked, sampled_ids, mask,
                        torch.ones(4, dtype=torch.bool, device=args.device), top_k=16)
                elif method == "stopd":
                    teacher_logits = scores(teachers[0], ids, local_prompt.shape[1])[0]
            student.train()
            current_logits, current_lp, _ = scores(student, ids, local_prompt.shape[1])
            if method == "waypoint-opd":
                loss, diagnostics = waypoint_opd.waypoint_ppo_loss(current_logits, sampled_ids, credit, kl_coefficient=.1)
            elif method == "ggpo":
                loss, diagnostics = ggpo.ggpo_loss(current_lp[None, :], ref_lp[None, :], rewards, mask[None, :], beta=.1)
            elif method == "stopd":
                losses = stopd.reverse_kl_token_losses(current_logits, teacher_logits)
                loss, diagnostics = schedule.loss(plan, losses, mask)
            elif method == "cce-opd":
                loss, diagnostics = cce_opd.cce_ppo_loss(current_logits, sampled_ids, credit)
            else:
                loss, diagnostics = sif.sif_ppo_loss(current_lp[None, :], old_lp[None, :], ref_lp[None, :], credit)
                diagnostics.update({"paper_default_minimum_length": 550,
                    "paper_default_eligible_responses": int(default_credit.eligible.sum()),
                    "diagnostic_minimum_length": diagnostic_config.minimum_length,
                    "short_window_diagnostic_only": True})
            optimizer.zero_grad()
            loss.backward()
            norm = torch.nn.utils.clip_grad_norm_(student.parameters(), 1., error_if_nonfinite=True)
            if not float(norm) > 0:
                raise RuntimeError(f"{method} has no actual policy gradient")
            optimizer.step()
            if schedule:
                schedule.finish_batch(plan, mask)
            if policies:
                diagnostics["reference_refreshed"] = policies.after_optimizer_step(student)
            history.append({"step": step, "loss": float(loss.detach()), "gradient_norm": float(norm), **diagnostics})
        delta = parameter_delta(student, initial_parameters)
        if delta <= 0:
            raise RuntimeError(f"{method} did not actually update parameters")
        outcomes[method] = {"seed": seed, "parameter_delta_l2": delta,
            "baseline_validation_nll": initial_nll, "final_validation_nll": heldout_nll(student, validation),
            "final_test_nll": heldout_nll(student, test), "generated_tokens": generated,
            "natural_eos_rollouts": natural_eos, "rejected_diagnostic_groups": rejected_groups, "history": history}
        if policies:
            outcomes[method].update({"reference_refreshes": policies.reference_refreshes,
                "behavior_syncs": policies.behavior_syncs, "behavior_is_reference": False,
                "reward": "first sampled byte ID is even; verifier mechanism diagnostic, not text quality"})
        if method == "waypoint-opd":
            outcomes[method]["teacher_snapshot_lineage"] = lineage
            outcomes[method]["teacher_rl_reward"] = "first sampled byte ID is even; not language capability"
        if method == "cce-opd":
            outcomes[method]["condition_pair_source"] = "explicit controlled mathematical-premise fixture; removing evenness changes answer determinacy; no automatic semantic annotation"
    teacher_deltas = [parameter_delta(t, old) for t, old in zip(teachers, teacher_before, strict=True)]
    snapshot_deltas = [parameter_delta(t, old) for t, old in zip(snapshot_models or [], snapshot_before, strict=True)]
    if any(teacher_deltas + snapshot_deltas):
        raise RuntimeError("a frozen teacher was modified during student optimization")
    for result in outcomes.values():
        result["frozen_teacher_parameter_deltas_l2"] = teacher_deltas
        result["frozen_rl_snapshot_parameter_deltas_l2"] = snapshot_deltas
    return outcomes


def run(args):
    if args.output.exists():
        raise FileExistsError("choose a fresh output; previous evidence is immutable")
    seeds = [int(s) for s in args.seeds.split(",")]
    selected = METHODS if args.methods == "all" else tuple(args.methods.split(","))
    if not selected or any(m not in METHODS for m in selected):
        raise ValueError("unknown component")
    if len(seeds) not in (1, 2, 3) or len(set(seeds)) != len(seeds):
        raise ValueError("one to three distinct seeds required")
    if not 2 <= args.steps <= 10 or not 1 <= args.teacher_steps <= 32 or not 8 <= args.max_tokens <= 64:
        raise ValueError("bounded diagnostic budgets: steps2..10, teacher1..32, tokens8..64")
    initial_size = args.corpus_path.stat().st_size
    if not 4096 <= initial_size <= 2_000_000 or not args.corpus_id or not args.corpus_revision:
        raise ValueError("4KB..2MB corpus with explicit public identity/revision required")
    # Reject an oversized input before reading it; a bounded read also protects
    # against a file growing between stat and open. No accidental large download
    # or path typo may allocate the whole file merely to fail the cost gate.
    with args.corpus_path.open("rb") as handle:
        payload = handle.read(2_000_001)
    if len(payload) != initial_size:
        raise ValueError("corpus size changed during bounded read; immutable input required")
    digest = hashlib.sha256(payload).hexdigest()
    if args.corpus_sha256 and digest != args.corpus_sha256:
        raise ValueError("corpus does not match the declared immutable content hash")
    tokens = torch.tensor(list(payload), dtype=torch.long, device=args.device)
    a, b = int(.8 * len(tokens)), int(.9 * len(tokens))
    train, validation, test = tokens[:a], tokens[a:b], tokens[b:]
    started = time.monotonic()
    results = {key: [] for key in selected}
    for seed in seeds:
        for method, result in run_seed(args, seed, train, validation, test, selected).items():
            results[method].append(result)
    result = {"schema_version": 1, "evaluation_tier": "L1", "diagnostic_only": True,
        "promotion_eligible": False, "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost", "methods": list(selected),
        "papers": {key: PAPERS[key] + "v1" for key in selected}, "seeds": seeds, "results": results,
        "public_resources": {"corpus_id": args.corpus_id, "corpus_revision": args.corpus_revision,
            "corpus_sha256": digest, "byte_ranges": {"train": [0, a], "validation": [a, b], "test": [b, len(tokens)]},
            "checkpoint": "none; seeded BytePolicy trained with bounded public-text next-token warmup"},
        "protocol": {"model": "257-token causal cumulative-embedding BytePolicy, width24",
            "separate_train_validation_test": True, "selection": "none; fixed budgets, final heldout NLL only",
            "teacher_steps": args.teacher_steps, "specialist_steps": 4, "student_steps": args.steps,
            "max_new_tokens": args.max_tokens, "sif": "default550 exclusion plus explicit K2/w4/s2 short-window diagnostic",
            "tf_opd": "actual teacher self-generation; naturalEOS+DEFLATE filter; correctness ungraded text",
            "waypoint": "same actual tiny RL run, byte-parity reward, frozen initial/middle/final",
            "cce": "controlled mathematical premise fixture; same sampled prefix, no semantic extractor"},
        "not_claimed": ["paper benchmark reproduction", "pretrained LLM capability", "semantic condition extraction", "default550 SIF online training", "evolve integration"],
        "accelerator": torch.cuda.get_device_name() if args.device.startswith("cuda") else args.device,
        "elapsed_seconds": time.monotonic() - started}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"methods": list(selected), "seeds": seeds,
        "parameter_deltas": {k: [r["parameter_delta_l2"] for r in v] for k, v in results.items()},
        "elapsed_seconds": result["elapsed_seconds"]}))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-path", type=Path, required=True)
    parser.add_argument("--corpus-id", required=True)
    parser.add_argument("--corpus-revision", required=True)
    parser.add_argument("--corpus-sha256")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--methods", default="all")
    parser.add_argument("--steps", type=int, default=2)
    parser.add_argument("--teacher-steps", type=int, default=8)
    parser.add_argument("--max-tokens", type=int, default=16)
    args = parser.parse_args()
    if args.device == "cpu":
        torch.set_num_threads(1)
    run(args)


if __name__ == "__main__":
    main()
