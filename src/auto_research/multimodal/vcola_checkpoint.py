"""Actual frozen Qwen3.5 V-CoLA forward, explicit no-cache reference backend.

The original vision encoder and every language layer execute; after layer one,
visual states are physically merged and at the configured deep layer removed.
Uncompressed original text mRoPE positions remain intact. This auditable backend
replays the prompt during generation and does NOT claim optimized decode speed.
"""
from __future__ import annotations

from contextlib import contextmanager, nullcontext
from contextvars import ContextVar
from dataclasses import dataclass
import inspect
import math
from threading import RLock
from types import CellType, FunctionType, MethodType
from weakref import WeakKeyDictionary

import torch

from .vcola import delta_state_scores, early_exit_visual, merge_visual_tokens


_ACTIVE_DELTA_CAPTURE = ContextVar('vcola_delta_capture', default=None)
_CAPTURE_LOCKS = WeakKeyDictionary()
_CAPTURE_LOCKS_GUARD = RLock()
_MISSING = object()


def _private_kernel_forward(function, kernel_name, observed_kernel):
    """Clone original forward/decorators with private globals, never patch a module.

    Transformers >=5.19 calls the module kernel from a decorated forward. Keep
    the wrapper code and its other closure cells (including accelerate hooks),
    rebinding only the wrapped-function cell. Unknown wrapper layouts fail
    closed rather than bypassing the original decorated path.
    """
    if not isinstance(function, FunctionType):
        raise RuntimeError('unsupported Qwen forward wrapper; safe kernel observation unavailable')
    wrapped = getattr(function, '__wrapped__', None)
    namespace = function.__globals__
    closure = function.__closure__
    if wrapped is not None:
        replacement = _private_kernel_forward(wrapped, kernel_name, observed_kernel)
        rebound = False
        cells = []
        for cell in closure or ():
            if cell.cell_contents is wrapped:
                cells.append(CellType(replacement))
                rebound = True
            else:
                cells.append(cell)
        if not rebound:
            raise RuntimeError('unsupported Qwen decorator closure; refusing to bypass hooks')
        closure = tuple(cells)
    else:
        if kernel_name not in function.__code__.co_names or kernel_name not in namespace:
            raise RuntimeError('original Qwen forward does not expose the actual prefill kernel')
        namespace = dict(namespace)
        namespace[kernel_name] = observed_kernel
    cloned = FunctionType(function.__code__, namespace, function.__name__, function.__defaults__, closure)
    cloned.__kwdefaults__ = function.__kwdefaults__
    cloned.__annotations__ = dict(function.__annotations__)
    cloned.__dict__.update(function.__dict__)
    cloned.__qualname__, cloned.__module__, cloned.__doc__ = (
        function.__qualname__, function.__module__, function.__doc__)
    if wrapped is not None:
        cloned.__wrapped__ = replacement
    return cloned


@contextmanager
def observe_delta_prefill(first, observe):
    """Observe only this instance/call and restore exact attributes on any exit.

    Old releases expose an instance kernel; new releases need a private forward
    function namespace. Neither path changes module/class globals. ContextVar
    isolation also keeps unrelated calls in other threads on the original
    kernel even while this instance temporarily has a capture wrapper.
    """
    with _CAPTURE_LOCKS_GUARD:
        lock = _CAPTURE_LOCKS.setdefault(first, RLock())
    with lock:
        owner = object()
        instance_kernel = getattr(first, 'chunk_gated_delta_rule', None)
        if callable(instance_kernel):
            attribute = 'chunk_gated_delta_rule'
            api = 'instance_kernel'
            original_kernel = instance_kernel
        else:
            attribute = 'forward'
            api = 'private_forward_globals'
            bound = first.forward
            if not isinstance(bound, MethodType):
                raise RuntimeError('unsupported instance Qwen forward; safe observation unavailable')
            raw = inspect.unwrap(bound.__func__)
            original_kernel = raw.__globals__.get('torch_chunk_gated_delta_rule')
            if not callable(original_kernel):
                raise RuntimeError('actual Qwen module prefill kernel not found')

        def observed_kernel(q, k, v, **kwargs):
            result = original_kernel(q, k, v, **kwargs)
            if _ACTIVE_DELTA_CAPTURE.get() is owner:
                observe(q, k, v, kwargs, result)
            return result

        replacement = observed_kernel if attribute != 'forward' else MethodType(
            _private_kernel_forward(bound.__func__, 'torch_chunk_gated_delta_rule', observed_kernel), first)
        previous = vars(first).get(attribute, _MISSING)
        token = _ACTIVE_DELTA_CAPTURE.set(owner)
        try:
            setattr(first, attribute, replacement)
            yield api
        finally:
            if previous is _MISSING:
                if attribute in vars(first):
                    delattr(first, attribute)
            else:
                setattr(first, attribute, previous)
            _ACTIVE_DELTA_CAPTURE.reset(token)


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

        def observe(q, k, v, kwargs, result):
            if not kwargs.get('use_qk_l2norm_in_kernel') or kwargs.get('initial_state') is not None:
                raise ValueError("V-CoLA no-cache score capture requires normalized fresh delta state")
            scores = delta_state_scores(q, k, v, kwargs['g'], kwargs['beta'])
            relative = float((scores.recurrent_output - result[0].float()).norm()
                             / result[0].float().norm().clamp_min(1e-12))
            if not math.isfinite(relative) or relative > .03:
                raise RuntimeError(f"delta-state replay is not checkpoint-equivalent ({relative})")
            captured.update(scores=scores, recurrence_relative_error=relative)

        capture = remain_rate < 1 or collect_scores
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
            context = observe_delta_prefill(first, observe) if index == 0 and capture else nullcontext()
            with context as capture_api:
                hidden = layer(hidden, position_embeddings=rotary, attention_mask=mask,
                               position_ids=None, past_key_values=None, use_cache=False)
                if index == 0 and capture:
                    captured['delta_capture_api'] = capture_api
            if index == 0 and capture and 'scores' not in captured:
                raise RuntimeError('original target layer did not execute an observable prefill kernel')
            if index == 0 and remain_rate < 1:
                hidden, positions, visual, merge = merge_visual_tokens(
                    hidden, positions, visual, captured['scores'].combined[0], remain_rate=remain_rate)
                captured['merge'] = merge
            if exit_layer == index + 1:
                hidden, positions, visual = early_exit_visual(hidden, positions, visual)
        logits = self.model.lm_head(self.text.norm(hidden[:, -1:]))[:, -1].float()
        if not bool(torch.isfinite(logits).all()):
            raise FloatingPointError("nonfinite actual checkpoint logits; no evidence generated")
        details = {'layers': counts, 'recurrence_relative_error': captured.get('recurrence_relative_error'),
                   'delta_capture_api': captured.get('delta_capture_api'),
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
