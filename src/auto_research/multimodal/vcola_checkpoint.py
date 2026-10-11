"""Actual frozen Qwen3.5 V-CoLA forward, explicit no-cache reference backend.

The original vision encoder and every language layer execute; after layer one,
visual states are physically merged and at the configured deep layer removed.
Uncompressed original text mRoPE positions remain intact. This auditable backend
replays the prompt during generation and does NOT claim optimized decode speed.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch

from .vcola import delta_state_scores, early_exit_visual, merge_visual_tokens


@dataclass
class VisualPrefix:
    embeddings: torch.Tensor
    positions: torch.Tensor
    visual_mask: torch.Tensor
    next_position: int


class Qwen35VCoLA:
    def __init__(self, model):
        if model.config.model_type != "qwen3_5":
            raise ValueError("actual Qwen3.5 multimodal checkpoint required")
        self.model = model.eval().requires_grad_(False)
        self.text = model.model.language_model
        if self.text.config.layer_types[0] != "linear_attention":
            raise ValueError("V-CoLA requires a real first-layer Gated DeltaNet")

    @torch.no_grad()
    def prepare(self, batch):
        if batch['input_ids'].shape[0] != 1 or batch.get('pixel_values') is None:
            raise ValueError("one public image/question per forward required")
        outer = self.model.model
        embeddings = outer.get_input_embeddings()(batch['input_ids'])
        image = outer.get_image_features(batch['pixel_values'], batch['image_grid_thw'], return_dict=True)
        features = torch.cat(image.pooler_output).to(embeddings)
        mask, _ = outer.get_placeholder_mask(batch['input_ids'], embeddings, image_features=features)
        embeddings = embeddings.masked_scatter(mask, features)
        positions = outer.compute_3d_position_ids(input_ids=batch['input_ids'],
            image_grid_thw=batch['image_grid_thw'], inputs_embeds=embeddings,
            attention_mask=batch.get('attention_mask'), mm_token_type_ids=batch.get('mm_token_type_ids'))
        if positions is None or positions.shape != (3, 1, embeddings.shape[1]):
            raise ValueError("official processor must provide correct original multimodal positions")
        visual = batch['input_ids'][0] == self.model.config.image_token_id
        if bool(visual[-1]):
            raise ValueError("generation prompt must end in text")
        return VisualPrefix(embeddings, positions, visual, int(positions.max()) + 1)

    @torch.no_grad()
    def forward(self, prefix, *, remain_rate=1., exit_layer=None, collect_scores=False):
        from transformers.masking_utils import create_causal_mask, create_recurrent_attention_mask
        hidden, positions, visual = prefix.embeddings, prefix.positions, prefix.visual_mask
        if exit_layer is not None and not 1 < exit_layer < len(self.text.layers):
            raise ValueError("exit must be after layer one and before the final layer")
        captured, counts = {}, []
        first = self.text.layers[0].linear_attn
        original_kernel = first.chunk_gated_delta_rule

        def observed_kernel(q, k, v, **kwargs):
            result = original_kernel(q, k, v, **kwargs)
            if not kwargs.get('use_qk_l2norm_in_kernel') or kwargs.get('initial_state') is not None:
                raise ValueError("V-CoLA no-cache score capture requires normalized fresh delta state")
            scores = delta_state_scores(q, k, v, kwargs['g'], kwargs['beta'])
            relative = float((scores.recurrent_output - result[0].float()).norm()
                             / result[0].float().norm().clamp_min(1e-12))
            if not math.isfinite(relative) or relative > .03:
                raise RuntimeError(f"delta-state replay is not checkpoint-equivalent ({relative})")
            captured.update(scores=scores, recurrence_relative_error=relative)
            return result

        if remain_rate < 1 or collect_scores:
            first.chunk_gated_delta_rule = observed_kernel
        try:
            for index, layer in enumerate(self.text.layers):
                # No per-layer KV cache means shortening lengths does not create
                # cache-position drift. mRoPE uses original representative/text positions.
                attention = torch.ones(hidden.shape[:2], device=hidden.device, dtype=torch.long)
                mask_args = dict(config=self.text.config, inputs_embeds=hidden,
                                 attention_mask=attention, past_key_values=None)
                mask = (create_causal_mask(**mask_args) if layer.block_type == 'full_attention'
                        else create_recurrent_attention_mask(**mask_args))
                rotary = self.text.rotary_emb(hidden, positions)
                counts.append({'layer': index + 1, 'sequence_tokens': hidden.shape[1],
                               'visual_tokens': int(visual.sum())})
                hidden = layer(hidden, position_embeddings=rotary, attention_mask=mask,
                               position_ids=None, past_key_values=None, use_cache=False)
                if index == 0 and remain_rate < 1:
                    hidden, positions, visual, merge = merge_visual_tokens(
                        hidden, positions, visual, captured['scores'].combined[0], remain_rate=remain_rate)
                    captured['merge'] = merge
                if exit_layer == index + 1:
                    hidden, positions, visual = early_exit_visual(hidden, positions, visual)
        finally:
            first.chunk_gated_delta_rule = original_kernel
        logits = self.model.lm_head(self.text.norm(hidden[:, -1:]))[:, -1].float()
        if not bool(torch.isfinite(logits).all()):
            raise FloatingPointError("nonfinite actual checkpoint logits; no evidence generated")
        details = {'layers': counts, 'recurrence_relative_error': captured.get('recurrence_relative_error'),
                   'merge': captured.get('merge'), 'cache_used': False,
                   'original_text_positions_preserved': True}
        if 'scores' in captured:
            scores = captured['scores']
            visual = prefix.visual_mask
            details['importance_mean'] = float(scores.importance[0, visual].mean())
            details['uniqueness_mean'] = float(scores.uniqueness[0, visual].mean())
            details['score_std'] = float(scores.combined[0, visual].std(unbiased=False))
        return logits, details

    @torch.no_grad()
    def generate(self, prefix, tokenizer, *, remain_rate=.5, exit_layer=24, maximum_tokens=16):
        if maximum_tokens < 1:
            raise ValueError("positive response token budget required")
        current, generated, first = prefix, [], None
        eos = self.model.generation_config.eos_token_id
        eos = {eos} if isinstance(eos, int) else set(eos or [])
        for _ in range(maximum_tokens):
            logits, details = self.forward(current, remain_rate=remain_rate, exit_layer=exit_layer)
            if first is None:
                first = details
            token = int(logits.argmax(-1))
            generated.append(token)
            if token in eos:
                break
            embedding = self.text.embed_tokens(torch.tensor([[token]], device=logits.device))
            new_position = torch.full((3, 1, 1), current.next_position, device=logits.device, dtype=torch.long)
            current = VisualPrefix(torch.cat((current.embeddings, embedding), 1),
                torch.cat((current.positions, new_position), 2),
                torch.cat((current.visual_mask, torch.zeros(1, dtype=torch.bool, device=logits.device))),
                current.next_position + 1)
        return {'response': tokenizer.decode(generated, skip_special_tokens=True),
                'generated_tokens': len(generated), 'eos_reached': generated[-1] in eos,
                'truncated': generated[-1] not in eos, 'first_forward': first}
