# 多模态大模型研究

本研究域承载视觉—语言基础模型、训练数据、跨模态连接器和视觉后训练。第一阶段提供
一个可在 Mac、Linux CPU 和 GPU 从头训练的 `micro-vlm`，后续论文算子只有经过真实
图像实验和测试后才会进入 evolve。

## 当前能力

- `visual-shapes`：完全离线生成颜色、形状和方位问答图像；
- `fashion-mnist-qa`：约 30MB 的公开服饰图像，适合 Mac/CPU 快速复跑；
- `cifar10-qa`：官方 CIFAR-10 自然图像，MD5 校验后缓存，固定分层 validation/test；
- `micro_vlm_linear`、`micro_vlm_mlp`、`micro_vlm_query` 三种 connector；
- 强制报告原图、打乱图和空白图准确率，检查模型是否真的使用视觉信息；
- 与推荐、micro-LLM、后训练和 Agent 共用多轮控制器、隔离 test 和研究看板。

```bash
python -m pip install -e '.[multimodal]'

auto-research evolve \
  --model micro-vlm \
  --dataset visual-shapes \
  --direction "比较线性、MLP 和 query connector，要求模型真实使用视觉输入" \
  --offline --generations 2 --population 3 --steps 60 \
  --llm-dimensions 96 --llm-batch-size 16 --seeds 42
```

轻量公开图像入口（首次约下载 30MB，之后可加 `--offline`）：

```bash
auto-research evolve \
  --model micro-vlm --dataset fashion-mnist-qa \
  --direction "在真实服饰图像上比较 connector，并检查视觉依赖" \
  --generations 2 --population 3 --steps 100 \
  --maximum-examples 2000 --seeds 42
```

彩色自然图像入口（首次约下载 163MB）：

```bash
auto-research evolve \
  --model micro-vlm --dataset cifar10-qa \
  --direction "在真实图像上比较 connector，并检查视觉依赖" \
  --generations 2 --population 3 --steps 100 \
  --maximum-examples 2000 --seeds 42
```

## 浏览入口

- [方法索引](catalog.md)
- [按机构/公司/学校](catalog/by-organization.md)
- [按主题](catalog/by-topic.md)
- [按年份](catalog/by-year.md)
- [论文谱系与缺口](lineage.md)
- [统一评测协议](benchmark.md)

## 已验证的 L1 结果

Fashion-MNIST 固定 2,000 train / 1,000 validation / 1,000 test，seed 42、每个候选
150 steps。query connector 的 validation accuracy 为 **0.5010**，相对线性 connector
的 0.4240 提升 7.7 points；隔离 test 为 **0.4850**，打乱图/空白图只有
0.1070/0.1000。结构化结果见
[`metrics/fashion-mnist-qa-seed42.json`](metrics/fashion-mnist-qa-seed42.json)。

## 边界

`visual-shapes` 是 L0 系统 benchmark；Fashion-MNIST/CIFAR-10 是 L1 公开图像缩小实验。它们都
不是开放式 VQA 能力证明。ScienceQA、POPE、公开图文检索和 lmms-eval 属于 L2/L3；
已有 CLIP/LLaVA 的 MovieLens 代理结果也不会被当作正式多模态结果。
