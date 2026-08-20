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
from .retrieval import (
    RETRIEVAL_BENCHMARKS, RetrievalPredictionConfig,
    generate_retrieval_predictions,
)
from .matrix import MatrixCell, load_matrix, run_checkpoint_matrix
from .lmms_eval import (
    LMMSEvalConfig,
    build_lmms_eval_command,
    normalize_lmms_eval_results,
    run_lmms_eval,
)
from .video import VideoBenchmarkConfig, run_video_benchmark
from .audio import AudioBenchmarkConfig, run_audio_benchmark

__all__ = [
    "MicroVLMEvaluator", "load_cifar10_qa", "load_fashion_mnist_qa",
    "load_multimodal_data", "load_visual_shapes", "BENCHMARKS",
    "run_cifar10_benchmark", "run_public_benchmark", "score_benchmark",
    "write_benchmark_report",
    "CheckpointPredictionConfig", "GENERATIVE_BENCHMARKS",
    "generate_checkpoint_predictions",
    "RETRIEVAL_BENCHMARKS", "RetrievalPredictionConfig",
    "generate_retrieval_predictions",
    "MatrixCell", "load_matrix", "run_checkpoint_matrix",
    "LMMSEvalConfig", "build_lmms_eval_command", "normalize_lmms_eval_results",
    "run_lmms_eval",
    "VideoBenchmarkConfig", "run_video_benchmark",
    "AudioBenchmarkConfig", "run_audio_benchmark",
]
