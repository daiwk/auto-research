# 多模态大模型研究

本研究域承载视觉—语言基础模型、训练数据、跨模态连接器和视觉后训练。第一阶段提供
一个可在 Mac、Linux CPU 和 GPU 从头训练的 `micro-vlm`，后续论文算子只有经过真实
图像实验和测试后才会进入 evolve。

## 当前能力

- `visual-shapes`：完全离线生成颜色、形状和方位问答图像；
- `fashion-mnist-qa`：约 30MB 的公开服饰图像，适合 Mac/CPU 快速复跑；
- `cifar10-qa`：官方 CIFAR-10 自然图像，MD5 校验后缓存，固定分层 validation/test；
- `micro_vlm_linear`、`micro_vlm_mlp`、`micro_vlm_query`、`micro_vlm_qformer`、`micro_vlm_gated`、`micro_vlm_pixelshuffle` 六种 connector；
- CLIP、BLIP-2、LLaVA、SigLIP 2 与 SmolVLM 独立 adapter，以及可组合的 `objective:siglip2` 训练目标；
- 强制报告原图、打乱图和空白图准确率，检查模型是否真的使用视觉信息；
- `multimodal-predict` 真实加载公开 VLM checkpoint，支持 ScienceQA/POPE、不可变 revision、离线镜像与逐条续跑；
- `vlm-checkpoint` 在冻结的真实 checkpoint 上，以 ScienceQA validation 多轮搜索 prompt、hint、图像预处理和解码预算，最终隔离 test；
- ScienceQA、POPE、COCO/Flickr retrieval 的框架无关 L2 scorer，支持固定子集、三 seed、95% CI 和可审计预测文件；
- 与推荐、micro-LLM、后训练和 Agent 共用多轮控制器、隔离 test 和研究看板。

```bash
python -m pip install -e '.[multimodal]'

auto-research evolve \
  --model micro-vlm \
  --dataset visual-shapes \
  --direction "比较 LLaVA、BLIP-2、SigLIP 2 和 SmolVLM 算子，要求模型真实使用视觉输入" \
  --offline --generations 2 --population 3 --steps 60 \
  --llm-dimensions 96 --llm-batch-size 16 --seeds 42
```

固定配方的 CIFAR-10 三 seed 正式入口，以及 ScienceQA/POPE/检索预测格式见
[统一评测协议](benchmark.md)。预测器与 scorer 分离：前者加载真实 checkpoint 并落盘，
后者只读取标注和预测；随机基线仍只用于检查评测管线。

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

CIFAR-10 固定 5,000 train / 1,000 validation / 1,000 test，query connector、300 steps、
seeds 42/43/44。validation accuracy 为 **20.00% ± 1.28 points**；隔离 test 为
**19.43% ± 0.25 points**，打乱图/空白图为 10.43%/10.00%，说明模型确实依赖视觉输入，
但这个小模型结果仍只是 L1 object-QA，不代表开放式 VQA。完整单 seed、均值、sample std
与 95% CI 见
[`metrics/cifar10-qa-seeds42-44.json`](metrics/cifar10-qa-seeds42-44.json)。

## 论文级公开图像结果

所有结果均使用 Fashion-MNIST 真实像素、2,000 条训练样本和 seed 42；论文原始结论与本地
缩小实验分开记录。

| 论文机制 | 公平基线 | 本地 test | 视觉依赖 / 效率诊断 |
|---|---:|---:|---|
| CLIP 对称式图文对比 | 均匀检索 10.0% | **72.0%** | 打乱图 10.3% |
| LLaVA 两层 MLP projector | 线性 connector 46.8% | **43.4%** | -3.4 points；保留负结果 |
| BLIP-2 四 query Q-Former | 线性 connector 46.8% | **41.5%** | -5.3 points；token 16→4 |
| SigLIP 2 sigmoid + masked view | 均匀检索 10.0% | **66.9%** | 打乱图 10.8% |
| SmolVLM pixel shuffle | 线性 connector 46.8% | **65.8%** | +19.0 points；token 16→4 |

详细公式、原文结果、论文关键图、命令和边界见[方法索引](catalog.md)。

## 真实公开 checkpoint 结果

在官方 ScienceQA test split 固定前 500 条上，`SmolVLM2-256M-Video-Instruct`
（commit `067788b187b95ebe7b2e040b3e4299e342e5b8fd`）确定性 zero-shot accuracy 为
**56.80%**；image/text 分项为 **62.87% / 51.33%**，输出解析率 **99.80%**。
模型先在 M3 Pro Mac CPU 完成真实加载/单图冒烟，再在单卡 NVIDIA A30 上评测。
这是固定子集的单次 checkpoint 结果，不是完整 test leaderboard，也不是多 seed 提升。
结构化证据见
[`metrics/scienceqa-smolvlm2-256m-500.json`](metrics/scienceqa-smolvlm2-256m-500.json)。

## 边界

`visual-shapes` 是 L0 系统 benchmark；Fashion-MNIST/CIFAR-10 是 L1 公开图像缩小实验。它们都
不是开放式 VQA 能力证明。ScienceQA/POPE 的真实 checkpoint 生成与公开 benchmark scorer
已接入 L2；COCO/Flickr 目前只接入 scorer。仓库不提交 checkpoint 或公开数据，lmms-eval
完整任务套件仍属于 L3。论文 adapter 的 L1 缩小实验不会被写成通用 VLM 能力证明。
