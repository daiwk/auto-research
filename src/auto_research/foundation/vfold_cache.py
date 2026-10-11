"""Transformers 5 dynamic-cache bridge; batch-one paired full-attention only."""
import inspect

from transformers.cache_utils import DynamicCache, DynamicLayer

from .vfold import ValueBanks


class VFoldCache(DynamicCache):
    def __init__(self, num_layers, *, sink=4, recent=128):
        super().__init__()
        self.layers = [DynamicLayer() for _ in range(num_layers)]
        self.banks = ValueBanks(num_layers, sink, recent)

    def update(self, key_states, value_states, layer_idx, *args, **kwargs):
        keys, values = self.banks.update(layer_idx, key_states, value_states)
        layer = self.layers[layer_idx]
        if not layer.is_initialized:
            # Audited runtime variants accept key only or key/value. Resolve
            # before mutation; an exception retry could corrupt pending state.
            arity = len(inspect.signature(layer.lazy_initialization).parameters)
            if arity == 1:
                layer.lazy_initialization(key_states)
            elif arity == 2:
                layer.lazy_initialization(key_states, value_states)
            else:
                raise TypeError("unsupported DynamicLayer initialization contract")
        layer.keys = keys
        # Never persist one materialized full value tensor per layer.
        return keys, values

    def finish_layer(self, index):
        self.banks.finish_layer(index)

    def crop(self, max_length):
        raise NotImplementedError("VFold eager backend does not support speculative rollback")

    def reorder_cache(self, beam_idx):
        raise NotImplementedError("VFold eager backend supports batch-one non-beam decoding")

    def batch_repeat_interleave(self, repeats):
        raise NotImplementedError("VFold eager backend supports batch-one decoding")

    def batch_select_indices(self, indices):
        raise NotImplementedError("VFold eager backend supports batch-one decoding")
