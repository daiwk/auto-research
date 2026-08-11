"""Local-first multimodal training and evaluation primitives."""

from .evaluator import MicroVLMEvaluator
from .data import (
    load_cifar10_qa, load_fashion_mnist_qa, load_multimodal_data,
    load_visual_shapes,
)

__all__ = [
    "MicroVLMEvaluator", "load_cifar10_qa", "load_fashion_mnist_qa",
    "load_multimodal_data", "load_visual_shapes",
]
