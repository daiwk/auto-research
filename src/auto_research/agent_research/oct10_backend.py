"""Real local causal-LM backends for October Agent mechanisms.

The small text scaffold is not the authors' production coding-agent harness.
All roles share one checkpoint; no gold answer is passed to generation/judging.
"""

from __future__ import annotations

import hashlib
import json
import uuid

from .mass import Conversation, Execution


class LocalLanguageModel:
    def __init__(self, checkpoint, *, device="cpu", seed=42, max_tokens=128):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        torch.manual_seed(seed)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            checkpoint, local_files_only=True,
            torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
            attn_implementation="eager").to(device)
        self.device, self.max_tokens = device, max_tokens
        self.revision = "initial"
        self.training_audits = []

    def prompt_ids(self, messages):
        import torch
        text = self.tokenizer.apply_chat_template(list(messages), tokenize=False,
                                                 add_generation_prompt=True)
        return torch.tensor([self.tokenizer.encode(text, add_special_tokens=False)],
                            device=self.device)

    def generate(self, messages, *, sample=True):
        import torch
        self.model.eval()
        ids = self.prompt_ids(messages)
        with torch.no_grad():
            output = self.model.generate(
                ids, attention_mask=torch.ones_like(ids), max_new_tokens=self.max_tokens,
                do_sample=sample, **({"temperature": .8, "top_p": .95} if sample else {}),
                pad_token_id=self.tokenizer.eos_token_id)
        return self.tokenizer.decode(output[0, ids.shape[1]:], skip_special_tokens=True)

    def continuation(self, messages, target):
        return self.continuation_ids(messages, self.tokenizer.encode(target, add_special_tokens=False))

    def continuation_ids(self, messages, tokens):
        import torch
        prompt = self.prompt_ids(messages)[0]
        response = torch.tensor(tokens, device=self.device)
        if not response.numel():
            raise ValueError("nonempty continuation required")
        ids = torch.cat((prompt, response))[None]
        logits = self.model(ids, attention_mask=torch.ones_like(ids)).logits.float()
        selected = logits[:, prompt.numel() - 1:-1].log_softmax(-1)
        return selected.gather(-1, response[None, :, None]).squeeze(-1)[0]

    def choose(self, messages, choices):
        import torch
        self.model.eval()
        with torch.no_grad():
            scores = [float(self.continuation(messages, choice).mean()) for choice in choices]
        return choices[max(range(len(scores)), key=scores.__getitem__)]

    def summarize(self, component, messages, intents, purpose, attempt):
        source = [{"role": m.role, "content": m.content, "reference": m.identifier}
                  for m in messages]
        requirement = ("Preserve concrete outcomes, evidence provenance, unresolved material and informative failures "
                       "needed by the enclosing purposes. Do not interpret unprocessed evidence."
                       if component == "precip" else
                       "Separate Narrative and Knowledge. Coarsen narrative; preserve identifying details, "
                       "temporal changes and grounded knowledge, merging updates without inventing lessons.")
        return self.generate([{"role": "user", "content": json.dumps({
            "component": component, "purpose": purpose,
            "enclosing_intents": [i.purpose for i in intents], "messages": source,
            "instruction": requirement + " Write a concise first-person memory. "
            + ("Use fewer words than the previous attempt." if attempt else "")})}], sample=False)

    def train_conversations(self, training, validation, *, steps=3, lr=3e-5):
        """Assistant-only SFT, uniform tasks at caller; role windows sampled 1:2."""
        import torch
        from auto_research.post_training.oct10_checkpoint import LowRankLinear, install_lora

        # Internalize the preceding cycle, then initialize a fresh adapter and
        # optimizer; do not silently carry Adam moments across MASS cycles.
        for name, module in list(self.model.named_modules()):
            if isinstance(module, LowRankLinear):
                with torch.no_grad():
                    merged = module.base.weight.float() + module.scale * (module.b @ module.a)
                    module.base.weight.copy_(merged.to(module.base.weight.dtype))
                parent_name, child = name.rsplit(".", 1)
                setattr(self.model.get_submodule(parent_name), child, module.base)
        install_lora(self.model)
        parameters = [p for p in self.model.parameters() if p.requires_grad]
        self.optimizer = torch.optim.AdamW(parameters, lr=lr, betas=(.9, .95))
        buckets = {role: [c for c in training if c.role == role]
                   for role in ("orchestrator", "worker")}
        if not all(buckets.values()) or not validation:
            raise ValueError("MASS requires both roles and disjoint validation conversations")

        def objective(conversation):
            losses, counts = [], []
            for index, message in enumerate(conversation.messages):
                if message["role"] == "assistant" and message["content"].strip():
                    values = self.continuation(conversation.messages[:index], message["content"])
                    losses.append(-values.sum())
                    counts.append(values.numel())
            if not losses:
                raise ValueError("no assistant supervision in conversation")
            return sum(losses) / sum(counts), sum(counts)

        history = []
        role_indices = {role: 0 for role in buckets}
        self.model.train()
        for step in range(steps):
            # Exact 1/3 orchestrator, 2/3 worker frequency over complete triplets.
            role = "orchestrator" if step % 3 == 0 else "worker"
            conversation = buckets[role][role_indices[role] % len(buckets[role])]
            role_indices[role] += 1
            self.optimizer.zero_grad()
            loss, count = objective(conversation)
            loss.backward()
            torch.nn.utils.clip_grad_norm_([p for p in self.model.parameters() if p.requires_grad], 1.)
            self.optimizer.step()
            history.append({"loss": float(loss.detach()), "role": role, "assistant_tokens": count})
        self.model.eval()
        with torch.no_grad():
            validation_loss = sum(float(objective(c)[0]) for c in validation) / len(validation)
        digest = hashlib.sha256()
        for parameter in self.model.parameters():
            if parameter.requires_grad:
                digest.update(parameter.detach().float().cpu().numpy().tobytes())
        self.revision = digest.hexdigest()
        self.training_audits.append({"steps": history, "validation_loss": validation_loss,
                                    "revision": self.revision})
        return self


class MASSBackend(LocalLanguageModel):
    def execute(self, task, workflow):
        """Bounded two-worker scaffold; all outputs genuinely generated."""
        conversations, outputs = [], []
        for role in ("independent solver", "critical verifier"):
            messages = [{"role": "system", "content": "You are a bounded worker: " + role},
                        {"role": "user", "content": task.prompt + "\nWorkflow:\n" + workflow
                         + "\nPrior worker output:\n" + "\n".join(outputs)}]
            answer = self.generate(messages)
            messages.append({"role": "assistant", "content": answer})
            conversations.append(Conversation("worker", tuple(messages)))
            outputs.append(answer)
        messages = [{"role": "system", "content": "Integrate workers' evidence; state uncertainties."},
                    {"role": "user", "content": task.prompt + "\nWorkflow:\n" + workflow},
                    {"role": "user", "content": "Worker deliverables:\n" + "\n".join(outputs)}]
        answer = self.generate(messages)
        messages.append({"role": "assistant", "content": answer})
        conversations.append(Conversation("orchestrator", tuple(messages)))
        return Execution(uuid.uuid4().hex, answer, tuple(conversations))

    def propose(self, task, previous, incumbent, history):
        return self.generate([{"role": "user", "content": json.dumps({
            "task": task.prompt, "previous_workflow": previous, "best_workflow": incumbent,
            "self_feedback": history,
            "instruction": "Revise the two-worker information flow and bounded role instructions. "
            "Keep an independent solver, a verifier, and a final orchestrator. Return workflow only."})}])

    def compare(self, task, candidate, incumbent):
        messages = [{"role": "user", "content": json.dumps({"task": task.prompt,
            "A": candidate.workspace, "B": incumbent.workspace,
            "instruction": "Judge correctness, evidence and completeness without external references. "
            "Return A, B or TIE."})}]
        choice = self.choose(messages, ("A", "B", "TIE"))
        return {"A": 1., "B": 0., "TIE": .5}[choice], "Shared-checkpoint verdict: " + choice

    def fine_tune(self, training, validation):
        return self.train_conversations(training, validation)


class HippocamBackend(LocalLanguageModel):
    def janus(self, memory):
        context = [{"role": m.role, "content": m.content} for m in memory.context]
        prompt = [{"role": "user", "content": json.dumps({
            "context": context,
            "intents": [{"purpose": i.purpose, "exit_condition": i.exit_condition}
                        for i in memory.intents],
            "instruction": "Maintain nested purposes, not a full plan. Choose CONTINUE, DEEPEN, "
            "CLOSE, or SHIFT. Close only a concluded top suffix."})}]
        choices = ("CONTINUE", "DEEPEN", "CLOSE", "SHIFT") if memory.intents else ("CONTINUE", "DEEPEN")
        operation = self.choose(prompt, choices)
        close = 0
        if operation in {"CLOSE", "SHIFT"}:
            count = self.choose(prompt + [{"role": "assistant", "content": operation},
                                         {"role": "user", "content": "How many top intents concluded?"}],
                                tuple(str(i) for i in range(1, len(memory.intents) + 1)))
            close = int(count)
        open_intents = ()
        if operation in {"DEEPEN", "SHIFT"}:
            purpose = self.generate(prompt + [{"role": "user", "content":
                "State the immediate nested purpose in one sentence."}], sample=False)
            exit_condition = self.generate(prompt + [{"role": "user", "content":
                "Purpose: " + purpose + "\nState concrete success and failure exit conditions."}], sample=False)
            open_intents = ((purpose, exit_condition),)
        guidance = self.generate(prompt + [{"role": "user", "content":
            json.dumps({"operation": operation, "close": close, "open": open_intents})
            + "\nWrite concise first-person guidance for the next inference."}], sample=False)
        return {"close": close, "open_intents": open_intents, "guidance": guidance}


class EvoAllocBackend(LocalLanguageModel):
    def __init__(self, checkpoint, **kwargs):
        super().__init__(checkpoint, **kwargs)
        from .program_sandbox import CIRCLE_INITIAL, ProgramSandbox
        self.sandbox = ProgramSandbox()
        self.programs = {"initial": CIRCLE_INITIAL}
        self.proposals = 0

    def propose(self, archive, history):
        from .evoalloc import Candidate
        from .program_sandbox import CIRCLE_TASK
        parent = max(archive, key=archive.get)
        output = self.generate([{"role": "user", "content": CIRCLE_TASK
            + "\nParent program:\n" + self.programs[parent]
            + "\nObserved parent score:" + str(archive[parent])
            + "\nReturn revised complete Python code only."}])
        if "```" in output:
            pieces = output.split("```")
            output = pieces[1].removeprefix("python").strip() if len(pieces) > 1 else output
        self.proposals += 1
        key = "proposal-" + str(self.proposals)
        self.programs[key] = output
        return Candidate(key, output, archive[parent])

    def decide(self, candidate, context, strategy, experiences, partial):
        from dataclasses import asdict
        # Circle packing has no Partial evaluator in the original benchmark.
        return self.choose([{"role": "user", "content": json.dumps({
            "candidate": candidate.program, "context": context, "strategy": strategy,
            "experiences": [asdict(e) for e in experiences if e.status != "stale"],
            "instruction": "Allocate FULL_EVAL or DISCARD. No current full score is known."})}],
            ("FULL_EVAL", "DISCARD"))

    def full_evaluate(self, candidate):
        return self.sandbox.evaluate_packing(candidate.program).score

    def update_experiences(self, previous, history):
        from dataclasses import asdict
        from .evoalloc import apply_experience_operations
        cases = [{"case": i, "decision": entry["allocation"].actions,
                  "score": entry["observed_score"], "new_best": entry["new_best"],
                  "reason": entry["evaluation_reason"]}
                 for i, entry in enumerate(history) if entry["observed_score"] is not None]
        prompt = [{"role": "user", "content": json.dumps({
            "previous": [asdict(e) for e in previous], "observed_cases": cases,
            "instruction": "Consolidate grounded allocation lessons. Cite case indices; distinguish "
            "support and contradiction. Mark active, tentative or stale. Do not infer denied outcomes."})}]
        choices = ["NONE"]
        if sum(e.status != "stale" for e in previous) < 4:
            choices.append("ADD")
        if previous:
            choices.extend(("UPDATE", "DELETE"))
        action = self.choose(prompt, tuple(choices))
        if action == "NONE":
            return previous
        if action == "ADD":
            content = self.generate(prompt + [{"role": "user", "content":
                "Write one descriptive recurring pattern with decision-time applicability and observed tendency. "
                "Do not prescribe allocation actions."}])
            key = "experience-" + uuid.uuid4().hex
        else:
            key = self.choose(prompt + [{"role": "user", "content": "Choose the experience identifier."}],
                              tuple(e.identifier for e in previous))
            content = None
        operation = {"operation": action, "identifier": key}
        if action != "DELETE":
            case = int(self.choose(prompt + [{"role": "user", "content": "Choose observed evidence case index."}],
                                   tuple(str(c["case"]) for c in cases)))
            polarity = self.choose(prompt + [{"role": "user", "content":
                f"Does case {case} support or contradict the fixed statement?"}], ("support", "counter"))
            operation[polarity + "_cases"] = (case,)
            if action == "ADD":
                operation["content"] = content
            else:
                statuses = ["active", "tentative"]
                if sum(e.status == "stale" for e in previous) < 4:
                    statuses.append("stale")
                operation["status"] = self.choose(prompt + [{"role": "user", "content":
                    "Choose grounded statement status."}], tuple(statuses))
        return apply_experience_operations(previous, (operation,), (c["case"] for c in cases))

    def reflect_strategy(self, strategy, experiences, history):
        from dataclasses import asdict
        return self.generate([{"role": "user", "content": json.dumps({
            "strategy": strategy, "experiences": [asdict(e) for e in experiences],
            "instruction": "Propose one explicit revised allocation strategy grounded in observed evidence. "
            "Avoid missing promising new-best candidates before minimizing evaluation cost."})}])


def race_action_likelihoods(backend, trajectory):
    import torch
    context, values = trajectory.question, []
    backend.model.eval()
    with torch.no_grad():
        for turn in trajectory.turns:
            messages = [{"role": "user", "content": context}]
            if turn.token_ids:
                tokens = list(turn.token_ids)
                if not turn.reasoning:
                    tokens = [token for i, token in enumerate(tokens)
                              if not (turn.sampled_mask[i] and i < len(tokens) - 1)]
                scores = backend.continuation_ids(messages, tokens)
                if turn.action_choices:
                    alternatives = [backend.tokenizer.encode(a, add_special_tokens=False)
                                    for a in turn.action_choices]
                    option_lp = torch.stack([backend.continuation_ids(messages, tokens[:-1] + a)[-1]
                                             for a in alternatives])
                    values.append(float(option_lp.log_softmax(0)[turn.action_choices.index(turn.action)]))
                else:
                    values.append(float(scores[-1]))
                rendered = backend.tokenizer.decode(tokens, skip_special_tokens=False)
            else:
                rendered = "<think>" + turn.reasoning + "</think>\nAction:" + turn.action
                scores = backend.continuation(messages, rendered)
                action_count = len(backend.tokenizer.encode(turn.action, add_special_tokens=False))
                values.append(float(scores[-action_count:].mean()))
            context += "\n" + rendered
            context += "\nObservation:" + turn.observation
    return tuple(values)


def race_sft(backend, trajectory, *, epsilon=.001, steps=3):
    from .race import logic_cover
    covered, skipped, audit = logic_cover(
        trajectory, lambda t: race_action_likelihoods(backend, t), epsilon)
    messages = [{"role": "user", "content": covered.question}]
    for turn in covered.turns:
        messages.append({"role": "assistant", "content":
                         "<think>" + turn.reasoning + "</think>\nAction:" + turn.action})
        messages.append({"role": "user", "content": "Observation:" + turn.observation})
    conversation = Conversation("orchestrator", tuple(messages))
    # Generic SFT helper requires both roles; RACE has no role-balanced objective.
    import torch
    from auto_research.post_training.oct10_checkpoint import install_lora
    install_lora(backend.model)
    parameters = [p for p in backend.model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=3e-5)
    history = []
    for _ in range(steps):
        backend.model.train()
        optimizer.zero_grad()
        tokens = [backend.continuation(conversation.messages[:i], m["content"])
                  for i, m in enumerate(messages) if m["role"] == "assistant"]
        loss = -sum(t.sum() for t in tokens) / sum(t.numel() for t in tokens)
        loss.backward()
        optimizer.step()
        history.append(float(loss.detach()))
    return {"skipped_turns": skipped, "likelihood_audit": audit, "sft_losses": history}


def race_actor_step(backend, trajectories, advantages, optimizer, *, epsilon=.001):
    """Cover-aware RL on caller's on-policy training rollouts, with closure gradients.

    The caller/environment computes success and group advantages. This function
    does not generate actions from reference trajectories or inspect test labels.
    """
    import torch
    from .race import cover_aware_loss, logic_cover

    if len(trajectories) != len(advantages) or not trajectories:
        raise ValueError("one external group advantage per on-policy trajectory required")
    plans = []
    for trajectory in trajectories:
        if trajectory.successful:
            covered, skipped, audit = logic_cover(
                trajectory, lambda t: race_action_likelihoods(backend, t), epsilon)
        else:
            covered, skipped, audit = trajectory, (), []
        plans.append((trajectory, covered, skipped, audit))

    def token_arrays():
        rows, masks, closure = [], [], []
        for original, covered, skipped, _ in plans:
            context = original.question
            compressed = covered.question
            for index, turn in enumerate(original.turns):
                target = "<think>" + turn.reasoning + "</think>\nAction:" + turn.action
                offsets = backend.tokenizer(target, add_special_tokens=False,
                                            return_offsets_mapping=True)["offset_mapping"]
                messages = [{"role": "user", "content": context}]
                row = (backend.continuation_ids(messages, turn.token_ids) if turn.token_ids
                       else backend.continuation(messages, target))
                if turn.action_choices:
                    # Environment-constrained single-token action policy: use
                    # its normalized legal-action distribution in PPO ratios.
                    ids = [backend.tokenizer.encode(a, add_special_tokens=False) for a in turn.action_choices]
                    if any(len(tokens) != 1 for tokens in ids):
                        raise ValueError("bounded action choices must be single tokens")
                    prefix = list(turn.token_ids[:-1])
                    option_lp = torch.stack([backend.continuation_ids(messages, prefix + tokens)[-1]
                                             for tokens in ids])
                    index_choice = turn.action_choices.index(turn.action)
                    row = torch.cat((row[:-1], option_lp.log_softmax(0)[index_choice][None]))
                reasoning_start, reasoning_end = len("<think>"), len("<think>") + len(turn.reasoning)
                if turn.sampled_mask:
                    # Controlled syntax isn't sampled policy output. Native
                    # reasoning tokens precede the final sampled action token.
                    mask = torch.tensor([index in skipped and flag and j < len(turn.sampled_mask) - 1
                                         for j, flag in enumerate(turn.sampled_mask)], device=backend.device)
                else:
                    mask = torch.tensor([index in skipped and a >= reasoning_start and b <= reasoning_end
                                         and b > a for a, b in offsets], device=backend.device)
                rows.append(row)
                masks.append(mask)
                if index in skipped:
                    close = backend.continuation(
                        [{"role": "user", "content": compressed + "\n<think>"}], "</think>")
                    # Paper's terminal closure token, not all multi-token marker pieces.
                    closure.append(close[-1])
                context += "\n" + (turn.raw_target or target) + "\nObservation:" + turn.observation
                compact_turn = covered.turns[index]
                if compact_turn.token_ids:
                    compact_tokens = list(compact_turn.token_ids)
                    if not compact_turn.reasoning:
                        compact_tokens = [token for i, token in enumerate(compact_tokens)
                                          if not (compact_turn.sampled_mask[i] and i < len(compact_tokens) - 1)]
                    compressed += "\n" + backend.tokenizer.decode(compact_tokens, skip_special_tokens=False)
                else:
                    compressed += "\n<think>" + compact_turn.reasoning + "</think>\nAction:" + turn.action
                compressed += "\nObservation:" + turn.observation
        return rows, masks, closure

    backend.model.eval()
    with torch.no_grad():
        old, _, _ = token_arrays()
        old = [row.detach() for row in old]
    optimizer.zero_grad()
    # Keep dropout disabled so the old/current importance ratio differs only by weights.
    current, skipped_masks, closure = token_arrays()
    size = max(row.numel() for row in current)
    pad = lambda rows: torch.stack([torch.nn.functional.pad(row, (0, size - row.numel())) for row in rows])
    sampling_masks = []
    for trajectory in trajectories:
        for turn in trajectory.turns:
            sampling_masks.append(torch.tensor(turn.sampled_mask, device=backend.device, dtype=torch.bool)
                                  if turn.sampled_mask else torch.ones_like(current[len(sampling_masks)], dtype=torch.bool))
    policy = pad(sampling_masks)
    labels = [float(a) for trajectory, a in zip(trajectories, advantages) for _ in trajectory.turns]
    loss = cover_aware_loss(pad(current), pad(old), torch.tensor(labels, device=backend.device),
                            policy, pad(skipped_masks),
                            torch.stack(closure) if closure else torch.zeros(0, device=backend.device),
                            sum(len(t.turns) for t in trajectories))
    loss.backward()
    optimizer.step()
    return {"loss": float(loss.detach()), "closure_terms": len(closure),
            "original_policy_tokens": int(policy.sum()),
            "skipped_reasoning_tokens": int(pad(skipped_masks).sum()),
            "likelihood_audits": [p[3] for p in plans]}


def bounded_calculator_rollouts(backend, *, episodes=8, reasoning_tokens=4):
    """Public executable L1 environment; legal tool policy is genuinely sampled.

    A invokes the trusted arithmetic tool, B finishes. The answer/reference plan
    is not provided to the LM. Syntax is forced and excluded from policy loss.
    """
    import torch
    from .race import TrainingTrajectory, Turn
    question = ("Compute 2 + 3 using the calculator tool and finish with its observed result. "
                "Available actions: A = invoke calculator on 2 + 3; B = finish current result. "
                "Use the real tool observation, not a memorized answer.")
    choices = ("A", "B")
    action_ids = [backend.tokenizer.encode(a, add_special_tokens=False) for a in choices]
    if any(len(tokens) != 1 for tokens in action_ids):
        raise ValueError("checkpoint does not support single-token action contract")
    trajectories, rewards = [], []
    backend.model.eval()
    for _ in range(episodes):
        context, turns, calculated, successful = question, [], False, False
        for _turn in range(2):
            prompt = backend.prompt_ids([{"role": "user", "content": context}])
            opening = backend.tokenizer.encode("<think>", add_special_tokens=False)
            closing = backend.tokenizer.encode("</think>\nAction:", add_special_tokens=False)
            base = torch.cat((prompt, torch.tensor([opening], device=backend.device)), dim=1)
            with torch.no_grad():
                generated = backend.model.generate(base, attention_mask=torch.ones_like(base),
                    max_new_tokens=reasoning_tokens, do_sample=True, temperature=1., top_p=1.,
                    pad_token_id=backend.tokenizer.eos_token_id)
                reasoning_ids = generated[0, base.shape[1]:].tolist()
                prefix = opening + reasoning_ids + closing
                full = torch.cat((prompt, torch.tensor([prefix], device=backend.device)), dim=1)
                logits = backend.model(full, attention_mask=torch.ones_like(full)).logits[0, -1].float()
                probabilities = logits[torch.tensor([a[0] for a in action_ids], device=backend.device)].softmax(0)
                selection = int(torch.multinomial(probabilities, 1))
            action = choices[selection]
            token_ids = tuple(prefix + action_ids[selection])
            if action == "A":
                calculated = True
                observation = json.dumps({"calculator_expression": "2 + 3", "result": 2 + 3})
            else:
                successful = calculated
                observation = "Environment finished: " + ("tool result accepted" if successful else "no tool result")
            reasoning = backend.tokenizer.decode(reasoning_ids, skip_special_tokens=True)
            target = backend.tokenizer.decode(token_ids, skip_special_tokens=False)
            mask = tuple([False] * len(opening) + [True] * len(reasoning_ids)
                         + [False] * len(closing) + [True])
            turns.append(Turn(reasoning, action, observation, token_ids, mask, choices, target))
            context += "\n" + target + "\nObservation:" + observation
            if action == "B":
                break
        trajectories.append(TrainingTrajectory(question, tuple(turns), successful))
        # Verifier-private success; progress fallback gives no gold information.
        rewards.append(float(successful))
    reward = torch.tensor(rewards, device=backend.device)
    advantages = ((reward - reward.mean()) / reward.std(unbiased=False).clamp_min(1e-6)).tolist()
    return tuple(trajectories), advantages, rewards
