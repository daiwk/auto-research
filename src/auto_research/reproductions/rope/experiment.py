from pathlib import Path
from ..llm_evolve_2026_common import run_llm_evolve_reproduction
def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(dataset_dir, seed, key="rope", architecture="rope", paper_results={"long_text_classification_improvement": "reported across six tasks"}, scope="实际对每个注意力 head 的 Q/K 执行复数平面旋转并由相对相位进入 dot product；WikiText-2 64d 小模型替代论文中文 RoFormer 预训练。")
