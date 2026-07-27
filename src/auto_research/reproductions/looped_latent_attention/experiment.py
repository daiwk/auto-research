from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce_looped_latent_attention(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir, seed, key="looped-latent-attention",
        architecture="looped_latent_attention",
        paper_results={"maximum_kv_compression_x": 32.0, "math500_base": 0.43, "math500_at_4x": 0.66},
        scope="真实用共享 recurrent Transformer block、低维 K/V latent 与逐 loop 重建执行训练；本地压缩为 2× 并从头训练，未复刻论文大模型 post-training codec、32× serving kernel。",
    )
