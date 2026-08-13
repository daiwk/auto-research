# 基础模型论文谱系与缺口

## 已覆盖主干

```mermaid
flowchart LR
  T["Dense Transformer"] --> M["MoE / Switch Transformer"]
  T --> S["SSM / Mamba / Naju"]
  T --> A["Sparse / Gated Attention"]
  T --> C["Engram / Memory Grafting"]
  A --> L["Long context / KV compression"]
  T --> D["Data curation / optimizer"]
  T --> V["Vision-language token retrieval"]
  L --> I["Quantization / dynamic compute / speculative decoding"]
```

当前已覆盖 MoE、状态空间模型、稀疏和门控注意力、条件记忆、长上下文位置编码、
预训练数据编排、优化器、量化、动态宽度、推测解码与视觉 token 检索。能够在本地
真实训练的算子已逐步接入 LLM evolve；只有 kernel 或大规模集群才能体现的方法会
保持明确的系统复现边界。

## 仍需补齐

| 优先级 | 缺口 | 接入前提 |
|---|---|---|
| P1 | test-time compute、verifier 与动态 reasoning budget | 同时报告正确率、token、延迟和调用成本 |
| P1 | 多模态视频、音频、具身与大规模后训练 | 可下载数据、真实 encoder/tokenizer 和公共 benchmark |

预训练 data mixture/curriculum、多模态图文理解、RoPE/ALiBi 已完成独立实现并进入
evolve，不再列为待办。
Chinchilla 一类 scaling law 需要多个 compute/data 预算点，也
不能用单次小模型训练替代完整曲线。
