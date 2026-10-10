"""Frozen Idefics3/SmolVLM Joint-KV backend, not a Qwen3-VL compatibility claim.

Original RoPE keys and absolute generation positions are retained. Every routing
decision reconstructs attention from persistent Coarse, selected original Fine,
and text banks; inactive Fine tokens remain stored and can be recalled later.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch

from .vimod import (DART, TRACE, auxiliary_call_loss, balanced_set_loss,
                    dart_distillation, joint_kv, online_teacher_loss, trace_policy_loss)


@dataclass
class CheckpointMemory:
    memory: object
    fine_banks: list
    coarse_banks: list
    text_banks: list
    input_token: torch.Tensor
    next_position: int
    hidden: torch.Tensor


class SmolVLMJointKV:
    def __init__(self, model, processor, dart: DART, trace: TRACE, group_size=4):
        if model.config.model_type not in ("idefics3", "smolvlm"):
            raise ValueError("this backend supports Idefics3/SmolVLM only; Qwen requires separate adapter")
        if group_size < 2 or math.isqrt(group_size) ** 2 != group_size:
            raise ValueError("group size must be a square 2D patch neighborhood")
        self.model, self.processor = model, processor
        self.dart, self.trace, self.group_size = dart, trace, group_size
        for parameter in model.parameters():
            parameter.requires_grad_(False)
        model.eval()

    def prefill(self, image, question):
        prompt = self.processor.apply_chat_template([
            {"role": "user", "content": [{"type": "image"},
                                          {"type": "text", "text": question}]}],
            add_generation_prompt=True)
        batch = self.processor(text=prompt, images=[image], return_tensors="pt")
        device = next(self.model.parameters()).device
        batch = {key: value.to(device) for key, value in batch.items()}
        with torch.no_grad():
            output = self.model(**batch, use_cache=True, output_hidden_states=True)
        ids = batch["input_ids"][0]
        image_positions = ids == self.model.config.image_token_id
        fine = output.hidden_states[0][0, image_positions].detach().float()
        if len(fine) < self.group_size:
            raise ValueError("not enough actual visual tokens")
        # SmolVLM pixel-shuffle projection preserves raster order within each
        # image crop. Reconstruct each crop's 2D grid, never merge groups across
        # crop boundaries or silently fall back to a 1D token-window proxy.
        vision = self.model.config.vision_config
        width = vision.image_size // vision.patch_size // self.model.config.scale_factor
        per_crop = width * width
        if not width or len(fine) % per_crop:
            raise ValueError("unsupported projected visual grid; explicit backend adapter required")
        side = math.isqrt(self.group_size)
        group_width = (width + side - 1) // side
        indices = torch.arange(len(fine), device=device)
        crop, patch = indices // per_crop, indices % per_crop
        row, column = patch // width, patch % width
        grid = crop * group_width**2 + (row // side) * group_width + column // side
        memory = self.dart(fine, grid)
        text_positions = ~image_positions
        text_positions[-1] = False
        fine_banks, text_banks, coarse_banks = [], [], []
        cache = output.past_key_values
        for layer in cache.layers:
            key, value = layer.keys[0].detach(), layer.values[0].detach()
            fine_kv = key[:, image_positions], value[:, image_positions]
            coarse = self.dart.coarse_kv(memory, fine_kv[0].float(), fine_kv[1].float())
            coarse = tuple(entry.to(key.dtype) for entry in coarse)
            fine_banks.append(fine_kv)
            text_banks.append((key[:, text_positions], value[:, text_positions]))
            coarse_banks.append(coarse)
        hidden = torch.stack([h[0, -1].detach().float()
                              for h in output.hidden_states[-len(self.trace.fusion):]])
        return CheckpointMemory(memory, fine_banks, coarse_banks, text_banks,
                                batch["input_ids"][:, -1:], len(ids) - 1, hidden)

    def decode_step(self, bank, active, *, full_visual=False):
        from transformers.cache_utils import DynamicCache
        entries = []
        for fine, coarse, text in zip(bank.fine_banks, bank.coarse_banks,
                                     bank.text_banks, strict=True):
            if full_visual:
                kv = tuple(torch.cat((f, t), -2) for f, t in zip(fine, text, strict=True))
            else:
                kv = joint_kv(bank.memory, active, coarse, fine, text)
            entries.append(tuple(value[None] for value in kv))
        cache = DynamicCache(entries)
        device = bank.input_token.device
        output = self.model(input_ids=bank.input_token, past_key_values=cache,
                            position_ids=torch.tensor([[bank.next_position]], device=device),
                            attention_mask=torch.ones(1, entries[0][0].shape[-2] + 1,
                                                      device=device, dtype=torch.long),
                            use_cache=True, output_hidden_states=True)
        text = []
        for old, layer in zip(bank.text_banks, output.past_key_values.layers, strict=True):
            text.append(tuple(torch.cat((entry, addition[0, :, -1:]), -2)
                              for entry, addition in zip(old, (layer.keys, layer.values), strict=True)))
        hidden = torch.stack([h[0, -1].float()
                              for h in output.hidden_states[-len(self.trace.fusion):]])
        return output.logits[:, -1].float(), text, hidden

    def distill_response(self, image, question, response, maximum_tokens=64):
        """Actual frozen checkpoint CE+forward-KL, identical verified prefixes."""
        bank = self.prefill(image, question)
        teacher_bank = CheckpointMemory(**vars(bank))
        targets = self.processor.tokenizer(response, return_tensors="pt",
                                           add_special_tokens=False)["input_ids"].to(bank.input_token.device)
        targets = targets[:, :maximum_tokens]
        if not targets.numel():
            raise ValueError("verified response must be nonempty")
        active = torch.zeros(len(bank.memory.counts), dtype=torch.bool, device=targets.device)
        losses = []
        for target in targets[0]:
            student_logits, text, hidden = self.decode_step(bank, active)
            with torch.no_grad():
                teacher_logits, teacher_text, teacher_hidden = self.decode_step(
                    teacher_bank, active, full_visual=True)
            losses.append(dart_distillation(student_logits, teacher_logits,
                                            target[None], torch.ones(1, dtype=torch.bool, device=targets.device)))
            bank.text_banks, bank.hidden = text, hidden
            teacher_bank.text_banks, teacher_bank.hidden = teacher_text, teacher_hidden
            bank.input_token = teacher_bank.input_token = target.reshape(1, 1)
            bank.next_position += 1
            teacher_bank.next_position += 1
        return torch.stack(losses).mean()

    def trace_supervised_loss(self, image, question, response, evidence_by_segment,
                              *, stage="set", routing_interval=16):
        """Train on externally annotated upcoming Fine working sets.

        evidence_by_segment contains actual Fine-token indices from box overlap;
        no answer-dependent heuristic or backbone-attention proxy is manufactured.
        Labels affect loss only; causal router observations contain no future text.
        """
        if stage not in ("set", "joint"):
            raise ValueError("TRACE supervised stage must be set or joint")
        for name, parameter in self.trace.named_parameters():
            projection = name.startswith(("query.", "key.", "threshold."))
            gate = name.startswith("gate.")
            parameter.requires_grad_(not gate if stage == "set" else not projection)
        self.dart.eval()
        with torch.no_grad():
            bank = self.prefill(image, question)
        tokens = self.processor.tokenizer(response, add_special_tokens=False,
                                          return_tensors="pt")["input_ids"][0].to(bank.input_token.device)
        active = torch.zeros(len(bank.memory.counts), dtype=torch.bool, device=tokens.device)
        state, losses, previous_target = None, [], torch.zeros_like(active)
        gate_logits, gate_targets = [], []
        for n, token in enumerate(tokens):
            if n % routing_interval == 0:
                segment = n // routing_interval
                if segment >= len(evidence_by_segment):
                    raise ValueError("missing upcoming-segment evidence annotations")
                ids = torch.tensor(evidence_by_segment[segment], device=tokens.device, dtype=torch.long)
                if ids.numel() and (int(ids.min()) < 0 or int(ids.max()) >= len(bank.memory.membership)):
                    raise ValueError("Fine evidence annotation outside image grid")
                target = torch.zeros_like(active)
                target[bank.memory.membership[ids]] = True
                output = self.trace(bank.hidden, bank.memory.coarse, active, state)
                state = output["state"]
                loss = balanced_set_loss(output["region_logits"], target)
                if stage == "joint":
                    changed = int(not torch.equal(target, previous_target))
                    gate_logits.append(output["gate_logits"])
                    gate_targets.append(changed)
                losses.append(loss)
                active, _, _, _ = self.trace.choose(output, active)
                previous_target = target
            with torch.no_grad():
                _, bank.text_banks, bank.hidden = self.decode_step(bank, active)
            bank.input_token, bank.next_position = token.reshape(1, 1), bank.next_position + 1
        if not losses:
            raise ValueError("nonempty response required")
        result = torch.stack(losses).mean()
        if gate_logits:
            labels = torch.tensor(gate_targets, device=tokens.device)
            terms = torch.nn.functional.cross_entropy(torch.stack(gate_logits), labels, reduction="none")
            result = result + sum(terms[labels == cls].sum() / (labels == cls).sum().clamp_min(1)
                                  for cls in (0, 1))
        return result

    def sampled_trajectory(self, image, question, *, maximum_tokens=64,
                           routing_interval=16, gate_bias=0., online_teacher=None):
        """Differentiable router actions around no-grad actual checkpoint decoding."""
        with torch.no_grad():
            bank = self.prefill(image, question)
        active = torch.zeros(len(bank.memory.counts), dtype=torch.bool, device=bank.input_token.device)
        state, generated, occupancy = None, [], []
        all_lp, region_lp, update_logits, teacher_losses, gates = [], [], [], [], []
        for n in range(maximum_tokens):
            if n % routing_interval == 0:
                output = self.trace(bank.hidden, bank.memory.coarse, active, state, gate_bias=gate_bias)
                state = output["state"]
                active, alp, rlp, gate = self.trace.choose(output, active, sample=True)
                all_lp.append(alp)
                region_lp.append(rlp)
                update_logits.append(output["gate_logits"][1] - output["gate_logits"][0])
                gates.append(gate)
                if online_teacher is not None:
                    # The callback receives only causally generated prefix, not
                    # a reference answer or any future student continuation.
                    prefix = self.processor.tokenizer.decode(generated, skip_special_tokens=True)
                    annotation = online_teacher(image=image, question=question, prefix=prefix)
                    labels = torch.as_tensor(annotation["labels"], device=active.device)
                    valid = torch.as_tensor(annotation["valid"], device=active.device)
                    if labels.shape != active.shape or valid.shape != active.shape:
                        raise ValueError("online teacher must map boxes to current C2F groups")
                    teacher_losses.append(online_teacher_loss(output["region_logits"], labels, valid))
            with torch.no_grad():
                logits, bank.text_banks, bank.hidden = self.decode_step(bank, active)
                token = logits.argmax(-1)
            generated.append(int(token))
            occupancy.append(int(bank.memory.counts[active].sum()))
            bank.input_token, bank.next_position = token.reshape(1, 1), bank.next_position + 1
            if int(token) == self.processor.tokenizer.eos_token_id:
                break
        return {"text": self.processor.tokenizer.decode(generated, skip_special_tokens=True),
                "all_logp": torch.stack(all_lp).sum(), "region_logp": torch.stack(region_lp).sum(),
                "update_logits": torch.stack(update_logits), "any_update": any(gates),
                "teacher_loss": torch.stack(teacher_losses).mean() if teacher_losses else all_lp[0] * 0,
                "occupancy": sum(occupancy) / len(occupancy) / len(bank.memory.membership)}

    def trace_rl_loss(self, image, question, verifier, online_teacher, *, group=16,
                      maximum_tokens=64, routing_interval=16):
        if group < 2 or online_teacher is None:
            raise ValueError("RLOO group and causal online teacher required")
        for parameter in self.trace.parameters():
            parameter.requires_grad_(True)
        self.dart.eval()
        bias = float(torch.empty(1).uniform_(-2.5, 2.5))
        trajectories = [self.sampled_trajectory(
            image, question, maximum_tokens=maximum_tokens, routing_interval=routing_interval,
            gate_bias=bias, online_teacher=online_teacher) for _ in range(group)]
        device = trajectories[0]["all_logp"].device
        correct = torch.tensor([float(verifier(row["text"])) for row in trajectories], device=device)
        costs = torch.tensor([row["occupancy"] for row in trajectories], device=device)
        policy = trace_policy_loss(torch.stack([row["all_logp"] for row in trajectories]),
                                   torch.stack([row["region_logp"] for row in trajectories]), correct, costs)
        teacher = torch.stack([row["teacher_loss"] for row in trajectories]).mean()
        all_failed = not bool(correct.any())
        any_update = any(row["any_update"] for row in trajectories)
        auxiliary = torch.stack([auxiliary_call_loss(row["update_logits"], all_failed, any_update)
                                 for row in trajectories]).mean()
        return policy + .3 * teacher + .1 * auxiliary, {
            "correctness_mean": float(correct.mean()), "fine_occupancy_mean": float(costs.mean()),
            "autonomous_updates": sum(row["any_update"] for row in trajectories)}

    @torch.no_grad()
    def generate(self, image, question, maximum_tokens=64, routing_interval=16,
                 boundary_offset=0.):
        if routing_interval < 1 or maximum_tokens < 1:
            raise ValueError("positive generation/routing budgets required")
        bank = self.prefill(image, question)
        active = torch.zeros(len(bank.memory.counts), dtype=torch.bool, device=bank.input_token.device)
        state, generated, occupancy, events = None, [], [], []
        for n in range(maximum_tokens):
            if n % routing_interval == 0:
                output = self.trace(bank.hidden, bank.memory.coarse, active, state,
                                    boundary_offset=boundary_offset)
                state = output["state"]
                active, _, _, gate = self.trace.choose(output, active)
                events.append({"token": n, "update": bool(gate),
                               "groups": torch.where(active)[0].tolist()})
            logits, text, hidden = self.decode_step(bank, active)
            token = logits.argmax(-1)
            generated.append(int(token))
            occupancy.append(int(bank.memory.counts[active].sum()))
            bank.text_banks, bank.hidden = text, hidden
            bank.input_token, bank.next_position = token.reshape(1, 1), bank.next_position + 1
            if int(token) == self.processor.tokenizer.eos_token_id:
                break
        fine_count = len(bank.memory.membership)
        return {"text": self.processor.tokenizer.decode(generated, skip_special_tokens=True),
                "tokens": len(generated), "routing": events,
                "mean_fine_occupancy": sum(occupancy) / len(occupancy) / fine_count,
                "mean_total_visual_occupancy": (len(active) + sum(occupancy) / len(occupancy)) / fine_count}
