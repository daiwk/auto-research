"""Reviewed P0/P1 papers for the 2026-10-03 intake."""

from __future__ import annotations


def _paper(
    domain, key, title, arxiv_id, slug, topic, author, affiliation, *,
    priority="P1", code=None, published="2026-10-01",
):
    root = "reproductions" if domain == "recommendation" else domain
    return {
        "domain": domain,
        "key": key,
        "title": title,
        "paper_url": f"https://arxiv.org/abs/{arxiv_id}",
        "detail_path": f"{root}/{arxiv_id}-{slug}/README.md",
        "topic": topic,
        "first_author": author,
        "first_author_affiliation": affiliation,
        "published": published,
        "code": code,
        "adapter": key,
        "priority": priority,
    }


LATEST_METHOD_PAPERS = (
    _paper("recommendation", "rptune", "RPTune: Learned Context Curation for LLM Catalog Search", "2610.00964", "rptune", ["搜索", "LLM 推荐", "上下文编排"], "Chuxuan Hu", "Google", priority="P0"),
    _paper("recommendation", "agent-web-rec", "AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation", "2610.01705", "agent-web-rec", ["Agent 推荐", "私有记忆", "证据融合"], "Haoran Qiang", "Beihang University"),
    _paper("foundation-models", "llm2jev", "LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them", "2610.02076", "llm2jev", ["Jev", "决策模型", "校准"], "Yinheng Li", "Microsoft（按作者邮箱）", priority="P0"),
    _paper("foundation-models", "omni-embed-mini", "Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation", "2610.02148", "omni-embed-mini", ["多模态嵌入", "蒸馏", "LoRA"], "Mohammed Irfan Kurpath", "原文首页未列第一作者机构"),
    _paper("foundation-models", "mwop", "MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs", "2610.01434", "mwop", ["多模态大模型", "结构剪枝", "推理效率"], "Xudong Wang", "原文首页未列第一作者机构"),
    _paper("foundation-models", "af-muon", "AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models", "2610.01395", "af-muon", ["优化器", "Muon", "显存效率"], "Arash Lagzian", "原文首页未列第一作者机构"),
    _paper("foundation-models", "rea", "Role-aware Heuristic Episodic Attention for Conversational LLMs", "2610.00958", "rea", ["长上下文", "会话记忆", "注意力"], "Wanyang Hong", "原文首页未列第一作者机构"),
    _paper("foundation-models", "hawk", "HAWK: Rethinking Multimodal Drafting for Speculative Decoding", "2610.00623", "hawk", ["多模态推理", "投机解码", "蒸馏"], "Wenhan Yang", "原文首页未列第一作者机构", published="2026-09-30"),
    _paper("foundation-models", "irekogpt", "IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs", "2610.00426", "irekogpt", ["结构剪枝", "可伸缩模型", "推理效率"], "Pietro Moriello", "University of Modena and Reggio Emilia", code="https://github.com/aimagelab/IrekoGPT"),
    _paper("post-training", "sharpening-tax", "Sharpening Tax in Post-Training", "2610.01509", "sharpening-tax", ["RL 后训练", "覆盖率", "Agentic RL"], "Changdae Oh", "Meta Superintelligence Labs / University of Wisconsin–Madison", priority="P0", code="https://github.com/changdaeoh/sharpening-tax"),
    _paper("post-training", "carm", "CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning", "2610.02039", "carm", ["RLVR", "off-policy", "响应掩码"], "Yafei Zhang", "Moore Threads AI"),
    _paper("post-training", "gmc-grpo", "Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis", "2610.01896", "gmc-grpo", ["异步 RL", "GRPO", "重要性采样"], "Qijia He", "The Ohio State University"),
    _paper("post-training", "gaw-po", "GAW-PO: Preference Optimization with Gradient-Aligned Token Weights", "2610.01511", "gaw-po", ["偏好优化", "token credit", "DPO"], "Andreea Dutulescu", "National University of Science and Technology POLITEHNICA Bucharest"),
    _paper("post-training", "sharpo", "SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning", "2610.00838", "sharpo", ["Agentic RL", "segment credit", "GRPO"], "Xinchen Du", "Georgia Institute of Technology", published="2026-09-30"),
    _paper("post-training", "tvrl", "Token-Level Video Reinforcement Learning", "2610.01973", "tvrl", ["视频生成", "token credit", "GRPO"], "Yifan Wang", "原文首页未列第一作者机构"),
    _paper("post-training", "lego-opd", "LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation", "2610.00333", "lego-opd", ["OPD", "多模态后训练", "teacher composition"], "Jaeyun Shin", "KAIST", published="2026-09-29"),
    _paper("post-training", "drift-opd", "DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies", "2610.00317", "drift-opd", ["OPD", "VLA", "长程信用"], "Youngjun Jun", "KAIST", published="2026-09-29"),
    _paper("agent-research", "autocompact", "AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents", "2610.02163", "autocompact", ["Coding Agent", "上下文压缩", "RL"], "Xuan Zhang", "原文首页未列第一作者机构", priority="P0"),
    _paper("agent-research", "belief-state-pos", "Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States", "2610.01415", "belief-state-pos", ["长程 Agent", "belief state", "恢复"], "Yu Luo", "原文首页未列第一作者机构"),
    _paper("agent-research", "pace-capability", "PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents", "2610.01349", "pace-capability", ["Agent 安全", "工具权限", "provenance"], "Fengpeng Li", "原文首页未列第一作者机构"),
    _paper("agent-research", "rule-evolve", "Self-Evolving Coding Rules for AI Coding Agents", "2610.00650", "rule-evolve", ["RSI", "Coding Agent", "规则进化"], "Zhengyuan Jiang", "原文首页未列第一作者机构", published="2026-09-30"),
    _paper("agent-research", "jev-spawn", "JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces", "2610.00437", "jev-spawn", ["Jev", "Agent 推理", "分支搜索"], "Haoyang Su", "原文首页未列第一作者机构", published="2026-09-30"),
    _paper("agent-research", "memfit", "MemFit: Efficient Long-Term Agentic Memory", "2610.00872", "memfit", ["Agent 记忆", "无损写入", "混合检索"], "Mitchell Piehl", "原文首页未列第一作者机构", published="2026-09-30"),
)
