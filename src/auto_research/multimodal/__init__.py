"""Local-first multimodal training and evaluation primitives."""

from .evaluator import MicroVLMEvaluator
from .benchmarks import (
    BENCHMARKS, run_cifar10_benchmark, run_public_benchmark,
    score_benchmark, write_benchmark_report,
)
from .data import (
    load_cifar10_qa, load_fashion_mnist_qa, load_multimodal_data,
    load_visual_shapes,
)
from .checkpoint import (
    CheckpointPredictionConfig, GENERATIVE_BENCHMARKS,
    generate_checkpoint_predictions,
)

__all__ = [
    "MicroVLMEvaluator", "load_cifar10_qa", "load_fashion_mnist_qa",
    "load_multimodal_data", "load_visual_shapes", "BENCHMARKS",
    "run_cifar10_benchmark", "run_public_benchmark", "score_benchmark",
    "write_benchmark_report",
    "CheckpointPredictionConfig", "GENERATIVE_BENCHMARKS",
    "generate_checkpoint_predictions",
]
