"""Real local-checkpoint bindings for Evo2, RSI-Anything and JANUS.

The bounded Evo2 harness edits only a generated prompt in executable agent.py;
it does not claim arbitrary production-harness or coding-benchmark fidelity.
Generated source executes exclusively through Linux bubblewrap/prlimit.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import math
import re

from .oct10_backend import LocalLanguageModel
from .oct12_evolution import Edit, Evaluation
from .program_sandbox import CIRCLE_TASK, ProgramSandbox


INITIAL_PROMPT = "Write a valid complete Python circle-packing solver. Return source code only."


def harness_source(prompt):
    return "import json\nPROMPT = " + repr(prompt) + "\nprint(json.dumps({'prompt': PROMPT}))\n"


def parameter_digest(model, *, trainable_only=False):
    digest = hashlib.sha256()
    for parameter in model.parameters():
        if trainable_only and not parameter.requires_grad:
            continue
        digest.update(parameter.detach().float().cpu().numpy().tobytes())
    return digest.hexdigest()


def extract_source(output):
    match = re.search(r"```(?:python)?\s*([\s\S]*?)```", output)
    return match.group(1).strip() if match else output.strip()


class CheckpointPolicy(LocalLanguageModel):
    def __init__(self, checkpoint, **kwargs):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        device, seed = kwargs.get("device","cpu"), kwargs.get("seed",42)
        torch.manual_seed(seed)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint,local_files_only=True,trust_remote_code=False)
        self.model = AutoModelForCausalLM.from_pretrained(checkpoint,local_files_only=True,
            trust_remote_code=False,use_safetensors=True,
            torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
            attn_implementation="eager").to(device)
        self.device,self.max_tokens = device,kwargs.get("max_tokens",256)
        self.revision,self.training_audits = "initial",[]
        self.last_truncated = False
        self.embedding_cache = {}

    def generate(self, messages, *, sample=True):
        import torch
        self.model.eval()
        ids = self.prompt_ids(messages)
        with torch.no_grad():
            output = self.model.generate(ids, attention_mask=torch.ones_like(ids),
                max_new_tokens=self.max_tokens, do_sample=sample,
                **({"temperature": .8, "top_p": .95} if sample else {}),
                pad_token_id=self.tokenizer.eos_token_id, use_cache=True)
        tokens = output[0, ids.shape[1]:]
        self.last_truncated = len(tokens) >= self.max_tokens and (
            not len(tokens) or int(tokens[-1]) != self.tokenizer.eos_token_id)
        return self.tokenizer.decode(tokens, skip_special_tokens=True)

    def continuation_ids(self, messages, tokens):
        """Untruncated full-prompt likelihood, with no training KV cache."""
        import torch
        prompt = self.prompt_ids(messages)[0]
        response = torch.tensor(tokens, device=self.device)
        if not response.numel():
            raise ValueError("nonempty continuation required")
        ids = torch.cat((prompt, response))[None]
        logits = self.model(ids, attention_mask=torch.ones_like(ids), use_cache=False).logits.float()
        selected = logits[:, prompt.numel() - 1:-1].log_softmax(-1)
        return selected.gather(-1, response[None, :, None]).squeeze(-1)[0]

    def probabilities(self, messages, choices):
        import torch
        with torch.no_grad():
            logits = torch.stack([self.continuation(messages, choice).mean() for choice in choices])
        return logits.softmax(0)

    def sample_choice(self, messages, choices):
        import torch
        return choices[int(torch.multinomial(self.probabilities(messages, choices), 1))]

    def embedding(self, text):
        import torch
        # Encoder is fixed for world-model adaptation; cache does not read labels.
        if text not in self.embedding_cache:
            ids = torch.tensor([self.tokenizer.encode(text, add_special_tokens=False)[:512] or
                                [self.tokenizer.eos_token_id]], device=self.device)
            self.model.eval()
            with torch.no_grad():
                hidden = self.model(ids, output_hidden_states=True).hidden_states[-1].float().mean(1)[0]
            self.embedding_cache[text] = torch.nn.functional.normalize(hidden, dim=0).detach()
        return self.embedding_cache[text]


class HarnessEvaluator:
    """Candidate harness and generated solver are separately isolated.

    No source is imported/exec'ed on the host, and no unsafe fallback exists.
    Fixed executor weights and greedy decoding are identical across candidates.
    """
    def __init__(self, executor, *, sandbox=None):
        self.executor = executor
        self.sandbox = sandbox or ProgramSandbox()
        for parameter in executor.model.parameters():
            parameter.requires_grad_(False)
        self.initial_digest = parameter_digest(executor.model)
        self.calls = 0

    def __call__(self, files):
        output, error, status = self.sandbox.execute(files["agent.py"])
        if status:
            if error.startswith("bwrap:") or "Operation not permitted" in error:
                raise RuntimeError("sandbox setup failed: " + error)
            return Evaluation(0., ({"stage": "harness", "error": error},), False, False)
        try:
            payload = json.loads(output)
            prompt = payload["prompt"]
            if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 16384:
                raise ValueError("invalid candidate prompt")
        except (ValueError, KeyError, TypeError):
            return Evaluation(0., ({"stage": "harness", "error": "invalid typed output"},), False, False)
        response = self.executor.generate([{"role": "user", "content": CIRCLE_TASK + "\n" + prompt}],
                                          sample=False)
        result = self.sandbox.evaluate_packing(extract_source(response))
        self.calls += 1
        # Area bound: sum of 26 radii cannot exceed sqrt(26/pi). No gold value.
        score = min(1., result.score / math.sqrt(26 / math.pi))
        return Evaluation(score, ({"stage": "fixed_executor", "raw_geometry_score": result.score,
            "feedback": result.feedback, "generated_program": result.code},), True, True)

    def frozen_audit(self):
        return {"executor_calls": self.calls, "executor_weights_unchanged":
                parameter_digest(self.executor.model) == self.initial_digest}


class Evo2Policy(CheckpointPolicy):
    def prepare_memory_efficient_training(self):
        """Checkpoint activations, never shorten prompts or change the loss.

        The supported public Qwen checkpoints have zero training dropout, so
        train-mode checkpointing preserves the original eval-mode likelihood.
        Positive-dropout checkpoints fail closed rather than change that loss.
        """
        config = getattr(self.model, "config", None)
        if config is not None:
            for name in ("attention_dropout", "hidden_dropout", "hidden_dropout_prob", "dropout"):
                if float(getattr(config, name, 0.) or 0.) != 0.:
                    raise ValueError("strict equivalent memory mode requires zero dropout")
            config.use_cache = False
        if hasattr(self.model, "gradient_checkpointing_enable"):
            self.model.gradient_checkpointing_enable()
            self.model.enable_input_require_grads()
        self.model.train()

    def propose(self, parent, directive=None, donor=None):
        messages = [{"role": "user", "content": json.dumps({
            "role": "Type B directed Proposer" if directive else "Type A autonomous Proposer",
            "candidate_source": parent.files, "observed_score": parent.evaluation.score,
            "execution_feedback": parent.evaluation.trace, "directive": directive, "donor": donor,
            "instruction": "Write the replacement PROMPT string for agent.py. Return only its text. "
            "No solutions or claimed scores; this prompt is consumed by a fixed coding executor."})}]
        response = self.generate(messages)
        edits = self.extract_edits(parent.files, response)
        return response, edits, messages, self.last_truncated

    @staticmethod
    def extract_edits(files, response):
        # Exact full-file edit/tool calls are supported; bare text is the declared
        # prompt-only edit action. It is not a fixed candidate from a fixture.
        try:
            parsed = json.loads(response)
            if isinstance(parsed, dict) and "edits" in parsed:
                return tuple(Edit(**edit) for edit in parsed["edits"])
        except (ValueError, TypeError):
            pass
        module = ast.parse(files["agent.py"])
        assignment = next(n for n in module.body if isinstance(n, ast.Assign) and
                          any(isinstance(t, ast.Name) and t.id == "PROMPT" for t in n.targets))
        old = ast.get_source_segment(files["agent.py"], assignment)
        text = response.strip().removeprefix("PROMPT:").strip()
        if not text:
            return ()
        return (Edit("agent.py", old, "PROMPT = " + repr(text)),)

    def continue_edits(self, files, prefix, directive):
        response = self.generate([{"role": "user", "content": json.dumps({
            "source_after_valid_prefix": files, "applied_edits": [e.__dict__ for e in prefix],
            "directive": directive, "instruction": "Resume the failed edit suffix. Write replacement PROMPT only."})}])
        return self.extract_edits(files, response)

    def reflect(self, candidate, strategies):
        messages = [{"role": "user", "content": json.dumps({"role": "Reflector",
            "source": candidate.files, "evaluation": candidate.evaluation.__dict__,
            "strategies": strategies,
            "instruction": "Choose keep, revise or crossover from measured execution evidence. "
            "Crossover must integrate a donor mechanism, not its score."})}]
        choices = ("keep", "revise", "crossover") if strategies else ("keep", "revise")
        action = self.sample_choice(messages, choices)
        decision = {"action": action, "training_segments": [(tuple(messages), action)]}
        response, truncated = action, False
        if action != "keep":
            continuation = messages + [{"role": "assistant", "content": action},
                {"role": "user", "content": "Give one concrete edit directive grounded in the trace."}]
            directive = self.generate(continuation)
            truncated = self.last_truncated
            response += "\n" + directive
            # Training scores exactly the sampled conditional directive, not an
            # invented combined prompt. Separate action record remains audited.
            messages = continuation
            response = directive
            decision["directive"] = directive
            decision["training_segments"].append((tuple(continuation), directive))
            if action == "crossover":
                decision["donor"] = self.sample_choice(messages, tuple(s["identifier"] for s in strategies))
                decision["training_segments"].append((tuple(messages), decision["donor"]))
                donor = next(s for s in strategies if s["identifier"] == decision["donor"])
                decision["directive"] += "\nDonor mechanism: " + donor["description"]
        return decision, response, messages, truncated

    def revision_directive(self, candidate):
        return self.generate([{"role": "user", "content": json.dumps({
            "role": "Reflector directed-edit case", "source": candidate.files,
            "execution_feedback": candidate.evaluation.trace,
            "instruction": "Write a concrete revision directive from this observed feedback."})}])

    def trajectory_logps(self, trajectory):
        import torch
        segments = trajectory.segments or ((trajectory.messages, trajectory.response),)
        return torch.cat([self.continuation(messages, response) for messages, response in segments])

    def extract_strategy(self, parent, child):
        return self.generate([{"role": "user", "content": json.dumps({
            "parent": parent.files, "child": child.files, "observed_feedback": child.evaluation.trace,
            "instruction": "Describe the executable change and observed effect without inventing success."})}])

    def snapshot(self):
        result = object.__new__(type(self))
        result.__dict__ = {key: value for key, value in self.__dict__.items()
                           if key not in {"model", "optimizer", "embedding_cache"}}
        result.model = copy.deepcopy(self.model).eval()
        result.embedding_cache = {}
        for parameter in result.model.parameters():
            parameter.requires_grad_(False)
        return result

    def sft(self, trajectories, *, steps=1):
        import torch
        from auto_research.post_training.oct10_checkpoint import install_lora
        install_lora(self.model)
        parameters = [p for p in self.model.parameters() if p.requires_grad]
        self.optimizer = torch.optim.AdamW(parameters, lr=3e-5)
        self.prepare_memory_efficient_training()
        history = []
        before = parameter_digest(self.model,trainable_only=True)
        for step in range(steps):
            self.optimizer.zero_grad()
            loss_value = 0.
            for role in ("proposer", "reflector"):
                rows = [t for t in trajectories if t.role == role]
                row = rows[step % len(rows)]
                # Same mean over two roles, but only one live trajectory graph.
                term = -self.trajectory_logps(row).mean() / 2
                loss_value += float(term.detach())
                term.backward()
                del term
            norm = torch.nn.utils.clip_grad_norm_(parameters, 1.)
            self.optimizer.step()
            history.append({"loss": loss_value, "gradient_norm": float(norm)})
        return {"steps": history, "parameters_changed": parameter_digest(self.model,trainable_only=True) != before,
                "native_trajectories": len(trajectories),
                "neutral_trajectories": sum(t.reward == 0 for t in trajectories)}

    def interleaved_grpo(self, proposer_group, reflector_group, *, round_id):
        import torch
        parameters = [p for p in self.model.parameters() if p.requires_grad]
        groups = (proposer_group, reflector_group)
        old = []
        self.model.eval()
        with torch.no_grad():
            for group in groups:
                old.append([self.trajectory_logps(t).detach() if not t.truncated else None
                            for t in group])
        self.optimizer.zero_grad()
        role_count = sum(any(value is not None for value in previous) for previous in old)
        loss_value, audit = 0., []
        before = parameter_digest(self.model,trainable_only=True)
        learning_signal = False
        for group, previous in zip(groups, old):
            rewards = torch.tensor([t.reward for t in group], device=self.device)
            advantages = rewards - rewards.mean()
            learning_signal |= any(value is not None and float(advantages[i]) != 0.
                                   for i, value in enumerate(previous))
            audit.append({"role": group[0].role, "rewards": rewards.tolist(),
                "advantages": advantages.tolist(), "masked_truncated": sum(t.truncated for t in group)})
        if not role_count or not learning_signal:
            # SFT leaves Adam momentum behind. A zero-valued loss followed by
            # optimizer.step() would move parameters with no GRPO evidence.
            return {"round":round_id,"updated":False,"parameters_changed":False,
                    "gradient_norm":0.,"loss":0.,"groups":audit,
                    "reason":"all samples truncated" if not role_count else "no eligible nonzero advantage"}
        self.prepare_memory_efficient_training()
        for group, previous in zip(groups, old):
            rewards = torch.tensor([t.reward for t in group], device=self.device)
            advantages = rewards - rewards.mean()
            eligible = sum(value is not None for value in previous)
            for index, trajectory in enumerate(group):
                if previous[index] is None:
                    continue  # paper masks truncated responses, no fabricated suffix
                current = self.trajectory_logps(trajectory)
                ratio = (current - previous[index]).exp()
                clipped = ratio.clamp(.8, 1.2)
                # Exactly the original eligible-sample mean, then role mean.
                term = -torch.minimum(ratio * advantages[index], clipped * advantages[index]).sum()
                term = term / self.max_tokens / eligible / role_count
                loss_value += float(term.detach())
                term.backward()
                del current, ratio, clipped, term
        norm = torch.nn.utils.clip_grad_norm_(parameters, 1.)
        if not torch.isfinite(norm):
            raise RuntimeError("non-finite GRPO gradient; no optimizer step executed")
        if float(norm) == 0.:
            return {"round":round_id,"updated":False,"parameters_changed":False,
                    "gradient_norm":0.,"loss":loss_value,"groups":audit,
                    "reason":"eligible advantages yielded zero gradient"}
        self.optimizer.step()
        return {"round": round_id, "updated": True, "loss": loss_value,
                "parameters_changed":parameter_digest(self.model,trainable_only=True) != before,
                "gradient_norm": float(norm), "groups": audit}


def make_factorized_predictor(dimension, device):
    """Small trainable action-conditioned OPF-style latent predictor, not JEPA weights."""
    import torch
    from torch import nn
    class Predictor(nn.Module):
        def __init__(self):
            super().__init__()
            self.context = nn.Sequential(nn.Linear(dimension * 2, 64), nn.GELU())
            self.factors = nn.ModuleList([nn.Linear(64, dimension) for _ in range(3)])
            self.readout = nn.Linear(dimension, 1)
        def forward(self, context, action):
            hidden = self.context(torch.cat((context, action), -1))
            factors = torch.stack([layer(hidden) for layer in self.factors], -2)
            latent = factors.mean(-2)
            return self.readout(latent).squeeze(-1).sigmoid(), latent, factors
    return Predictor().to(device)


class RSIBackend(CheckpointPolicy):
    def candidates(self, context, workflow, count):
        return [extract_source(self.generate([{"role": "user", "content":
                 context + "\nPersistent workflow:\n" + workflow + "\nReturn complete Python source only."}]))
                for _ in range(count)]

    def predict(self, predictor, context, candidate):
        import torch
        predictor.eval()
        with torch.no_grad():
            prediction, _, _ = predictor(self.embedding(context), self.embedding(candidate))
        return float(prediction)

    def version(self, item):
        return hashlib.sha256(item.encode()).hexdigest() if isinstance(item, str) else parameter_digest(item)

    def revise_workflow(self, workflow, feedback):
        return self.generate([{"role": "user", "content": json.dumps({"workflow": workflow,
            "observed_feedback": [r.__dict__ for r in feedback],
            "instruction": "Revise persistent solver workflow from actual outcomes. Return workflow only."})}])

    def adapt(self, predictor, records, *, steps):
        import torch
        if any(row.split != "train" for row in records):
            raise ValueError("predictor adaptation cannot read validation/test labels")
        candidate = copy.deepcopy(predictor)
        optimizer = torch.optim.AdamW(candidate.parameters(), lr=1e-3)
        history = []
        for _ in range(steps):
            losses = []
            for row in records:
                prediction, latent, factors = candidate(self.embedding(row.context), self.embedding(row.candidate))
                target = self.embedding(row.observation)
                normalized = torch.nn.functional.normalize(factors, dim=-1)
                gram = normalized @ normalized.transpose(-1, -2)
                orthogonal = (gram - torch.eye(3, device=self.device)).square().mean()
                loss = (prediction - row.outcome)**2 + (latent - target).square().mean() + .01 * orthogonal
                losses.append(loss)
            optimizer.zero_grad()
            loss = torch.stack(losses).mean()
            loss.backward()
            norm = torch.nn.utils.clip_grad_norm_(candidate.parameters(), 1.)
            optimizer.step()
            history.append({"loss": float(loss.detach()), "gradient_norm": float(norm)})
        return candidate, {"steps": history, "latent_target": "encoded observed execution feedback",
                           "source_model": "local small predictor, not authors JEPA-Anything checkpoint"}


class JanusBackend(CheckpointPolicy):
    def proposals(self, graph, skills, remaining, count):
        parents = tuple(n["id"] for n in graph if n["status"] == "executed")
        return [{"parents": [self.sample_choice([{"role": "user", "content":
                    json.dumps({"graph": graph, "skills": skills, "remaining": remaining,
                                "instruction": "Choose reusable experimental evidence parent."})}], parents)],
                 "proposal": self.generate([{"role": "user", "content": json.dumps({
                    "task": CIRCLE_TASK, "graph": graph, "skills": skills, "remaining": remaining,
                    "instruction": "Propose a concrete new solver experiment, not a claimed result."})}])}
                for _ in range(count)]

    def preference(self, left, right, criterion, graph, skills, remaining):
        messages = [{"role": "user", "content": json.dumps({"A": left, "B": right,
            "criterion": {"VI": "immediate value gain", "IG": "uncertainty reduction",
                          "EV": "follow-up exploration utility"}[criterion],
            "graph": graph, "skills": skills, "remaining": remaining,
            "instruction": "Predict which unexecuted proposal is better under this criterion: A or B."})}]
        return float(self.probabilities(messages, ("A", "B"))[0])

    def exploration_weights(self, graph, skills, remaining):
        prompt = [{"role": "user", "content": json.dumps({"graph": graph, "skills": skills,
            "remaining": remaining, "instruction": "Set information/exploration weights from progress and budget."})}]
        return tuple(float(self.sample_choice(prompt + [{"role": "user", "content": key}],
                     ("0", "0.5", "1", "2"))) for key in ("information", "exploration"))

    def debate(self, proposal, predictions, graph, skills):
        refined = self.generate([{"role": "user", "content": json.dumps({"proposal": proposal,
            "predictions": predictions, "graph": graph, "coordination": skills["coordination"],
            "instruction": "Critique and refine the experiment before execution. Return revised proposal only."})}])
        return {**proposal, "proposal": refined}

    def evolve_skills(self, skills, graph, strategy):
        updated = {}
        for key in skills:
            context = {"skill": key, "previous": skills[key], "strategy": strategy,
                "evidence": graph, "intra_skills": updated.get("intra", skills["intra"]),
                "instruction": "Update this skill from actual success/failure and forecast errors. "
                    "Cross skills must generalize intra skills; never invent experimental results."}
            updated[key] = self.generate([{"role": "user", "content": json.dumps(context)}])
        return updated

    def execute(self, proposal, graph, skills):
        output = self.generate([{"role": "user", "content": CIRCLE_TASK + "\nExperiment:\n" +
            proposal["proposal"] + "\nSkills:\n" + json.dumps(skills) + "\nReturn complete Python code only."}])
        result = ProgramSandbox().evaluate_packing(extract_source(output))
        return {"score": result.score, "feedback": result.feedback,
                "implementation": result.code, "environment": "public-circle-packing-26"}
