# 多模态大模型方法索引

## 内置研究底座

| 方法 | 类型 | 当前数据 | 状态 |
|---|---|---|---|
| `micro_vlm_linear` | patch encoder + 线性连接器 | L0 + Fashion-MNIST/CIFAR-10 L1 | 可执行 |
| `micro_vlm_mlp` | patch encoder + MLP projector | L0 + Fashion-MNIST/CIFAR-10 L1 | 可执行 |
| `micro_vlm_query` | patch encoder + 可学习视觉 query | L0 + Fashion-MNIST/CIFAR-10 L1 | 可执行 |

1A 只收录本地研究底座，不把它们伪装成论文复现。正式论文将在具备独立 adapter、
论文信息块、真实图像实验和固定指标后进入本页。
