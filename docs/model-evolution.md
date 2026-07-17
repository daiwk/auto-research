# 模型自动进化

该功能面向“已有一个可训练模型，希望围绕一段自然语言调研方向持续做实验”的场景，适用于推荐模型和语言模型。输入基础模型、公开数据集和调研方向后，系统自动检索论文、形成结构/数据/训练假设、并行训练、根据 validation 观察决定下一轮方向，最后隔离 test，并生成可读研究档案。

## 流程

```mermaid
flowchart LR
  A[基础模型 + 完整数据集 + 调研方向] --> B[方向转成检索词和结构约束]
  B --> C[论文证据缓存]
  C --> D[映射到已审计结构算子]
  D --> E[结构 + 超参数 Genome]
  E --> F[训练并评估 Validation]
  F --> G[并行实验与失败留档]
  G --> H{达到设定代数?}
  H -- 否 --> I[围绕冠军继续变异]
  I --> F
  H -- 是 --> J[基线与冠军最终 Test]
  J --> K[JSON + Markdown + HTML 研究看板]
```

结构与普通参数在同一个 genome 中共同搜索：

```text
architecture, dimensions, layers, learning_rate, optimizer,
batch_size, experts, interval_residual, auxiliary_weight
```

每个 trial 保存 `generation`、`parent_id`、论文来源、变异理由、validation 指标、训练 loss、参数量和耗时，因此可以完整回溯模型如何演化。

## RankMixer 首批论文算子

| 论文 | 内置结构 | 实际加入当前网络的机制 |
|---|---|---|
| [RankMixer](https://arxiv.org/abs/2507.15551) | `rankmixer_smoe` | parameter-free token mixing、per-token FFN、ReLU routed MoE |
| [TokenMixer-Large](https://arxiv.org/abs/2602.06563) | `tokenmixer_large` | mixing-reverting、per-token SwiGLU、interval residual、middle auxiliary head |
| [Zenith](https://arxiv.org/abs/2601.21285) | `zenith` | Prime Token RSA Fusion 与 tokenwise SwiGLU Token Boost |
| [MOI-Mixer](https://arxiv.org/abs/2108.07505) | `moi_mixer` | 一阶线性项与二阶显式交互 channel mixing |

在线 arXiv 检索仍会返回其他相关论文。只有已映射并经过 shape/训练测试的结构才能进入 population；其余论文保留为 `evidence-only`，避免从论文文本直接执行不可审计代码。

## 安装命令

`auto-research` 是本项目安装后生成的命令，不是另一个需要单独下载的软件。第一次使用时，在仓库根目录执行：

```bash
cd /path/to/auto-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[neural-recs]'
```

确认安装成功：

```bash
auto-research --help
auto-research evolve --help
```

`-e` 是可编辑安装，修改或更新项目源码后通常无需重新安装。新开一个终端后，需要重新激活虚拟环境：

```bash
cd /path/to/auto-research
source .venv/bin/activate
```

如果不想激活环境，可直接使用完整路径：

```bash
.venv/bin/auto-research evolve --help
```

只有 `pyproject.toml` 中的依赖发生变化时，才需要重新执行安装命令。

## 方向驱动的使用方式

```bash
auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "把 LONGER、UniMixer 及相关高效 Transformer 结构加入 RankMixer，比较长序列压缩、可学习 token mixing 及其组合" \
  --generations 3 \
  --population 6 \
  --workers 3 \
  --steps 300 \
  --papers 8 \
  --seeds 42,43,44
```

基础模型也可以换成 HyFormer：

```bash
auto-research evolve \
  --model hyformer \
  --dataset movielens-1m \
  --direction "引入 LONGER 的长序列压缩和 UniMixer 的参数化 mixing，升级高效 Transformer" \
  --generations 3 --population 6 --workers 3 --steps 300
```

## LLM 自动进化

`micro-llm` 是可在 Mac、Linux GPU 和 Linux CPU 训练的 decoder-only Transformer。默认配置约 1200 万至 1600 万参数（具体取决于结构），使用 4K 本地 BPE、384 hidden size、6 layers 和 128 context；这些都可通过 CLI 缩放。它不是为了冒充生产大模型，而是让结构、数据配比和后训练方法能够真实训练、比较和迭代。

```bash
python -m pip install -e '.[llm-evolution]'

auto-research evolve \
  --model micro-llm \
  --dataset wikitext-2 \
  --direction "调研高效 LLM 结构、训练数据配比和 SFT/NEFTune 后训练方法" \
  --generations 3 \
  --population 6 \
  --workers 1 \
  --steps 300 \
  --papers 8 \
  --seeds 42
```

所有 evolve 模型共用 `--device auto|cpu|mps|cuda|cuda:<index>`；Linux CPU 还可传 `--cpu-threads`。安装、CUDA 选择与多卡隔离见[运行环境指南](runtime.md)。

三轮默认分工：

1. **结构轮**：GPT baseline、GQA、LLaMA-style RMSNorm/RoPE/SwiGLU、parallel attention/FFN 及组合；数据和训练预算保持不变。
2. **数据轮**：WikiText-only、WikiText + Tiny Shakespeare narrative mixture、从 narrative 向 WikiText 退火的 curriculum；冻结冠军结构。
3. **后训练轮**：普通 SFT、低学习率 SFT、不同噪声强度的 NEFTune；使用 Stanford Alpaca train/held-out 子集并冻结预训练配方。

当 `--generations` 大于 3 时，后续轮次会继续搜索 hidden size、层数、学习率、batch size 和 context length；每个候选仍继承上一轮冠军，形成可追溯的多轮进化链。

选择目标为 `WikiText validation loss + 0.15 × instruction validation loss`。WikiText test 和最终冠军只在三轮结束后评估。默认使用完整 WikiText-2 train；`--maximum-train-tokens` 仅用于 smoke test。

### 本地诊断实验

为了验证整条链路，Mac MPS 上用 0.54M 参数、40 pretraining steps、24 post-training steps、seed 42 跑了三轮，每轮 4 个候选：

| 阶段 | 当轮观察 |
|---|---|
| 结构 | `parallel_gelu` 胜出；matched-budget validation PPL 447.469，略优于 GPT baseline 449.032 |
| 数据 | WikiText-only 胜出；混入 10%/20%/35% narrative 会改善少量 instruction loss，但使 WikiText PPL 变差 |
| 后训练 | 普通 SFT 胜出；优于低学习率 SFT 和本轮 NEFTune alpha 5/10 |

最终隔离 test PPL 从 `416.134` 降到 `405.328`（`-2.60%`），instruction validation loss 从 `6.3804` 降到 `6.2309`。这只是单 seed、极小预算的系统诊断，不能外推到默认 12M+ 模型或标准大模型能力；稳定事实记录见 [`evolution/micro-llm-wikitext2-diagnostic-seed42.json`](evolution/micro-llm-wikitext2-diagnostic-seed42.json)。

每一代的候选会并行执行。macOS 上多 worker 使用独立进程，避免多个实验共享随机数状态或模型；每个实验仍保持相同 split、seed 和训练预算。完整过程写入：

- `result.json`：机器可读的论文、配置、父子关系、指标、失败原因和每轮决策。
- `report.md`：适合代码审查和长期归档的中文研究报告。
- `index.html`：无需服务即可打开的响应式研究看板，展示效果、假设、观察和下一轮决策。

第一轮是公平结构消融：所有候选继承基础模型的相同超参数，只改变结构。第二轮起才围绕上一轮冠军分别调整层数、维度、学习率、优化器和 batch size，避免把结构收益和调参收益混在一起。

## 数据规模

默认不再裁剪训练数据：MovieLens-100K 使用完整的 932 个有效用户和 1,682 个物品；MovieLens-1M 使用完整 leave-two-out 序列。为控制每个候选的全库排序成本，默认用固定且均匀覆盖的 1,000 用户 cohort 做 validation/test；传入 `--evaluation-users 0` 可评估全部用户。只有为了快速验证流程时，才显式传入 `--maximum-users` 和 `--maximum-items`。数据规模与评估 cohort 都会记录到报告中，避免把 smoke test 误写成正式实验。

| 推荐方向 | RankMixer 候选 | HyFormer 候选 | 实际机制 |
|---|---|---|---|
| LONGER | `rankmixer_longer` | `hyformer_longer` | 分块 token merge、global interest、recent token 保留 |
| UniMixer | `rankmixer_unimixer` | `hyformer_unimixer` | 可学习 token mixing 与逐 token channel mixing |
| 组合 | `rankmixer_longer_unimixer` | `hyformer_longer_unimixer` | 同时验证长序列压缩与参数化 mixing 是否互补 |

## 早期小规模诊断记录

MovieLens-100K compact 使用 220 个用户、360 个物品，训练 40 steps；运行两代、每代三个子代、seed 42。

| 模型 | Validation NDCG@10 | Test Hit@10 | Test NDCG@10 |
|---|---:|---:|---:|
| 初始 RankMixer dense | 0.00956 | 0.05000 | 0.02402 |
| 进化冠军：MOI-Mixer，1 层，batch 24 | **0.01335** | **0.07727** | **0.03864** |

冠军相对初始模型 validation NDCG `+39.65%`，最终隔离 test NDCG `+60.87%`。与此同时 head share 从 `0.08864` 上升到 `0.14727`，说明效果提升伴随更强的头部集中，不能只看单一主指标。

稳定指标见 [`evolution/rankmixer-movielens-2g3p-seed42.json`](evolution/rankmixer-movielens-2g3p-seed42.json)。该结果是一次小预算功能验证，不等同于论文复现或多 seed 稳定结论。

## 评估纪律

- 初始模型和全部子代共享数据切分、候选全集、训练 steps 和 seed。
- 结构与参数晋级只能读取 validation；test 不参与任何一轮选择。
- 全部代际结束后，初始基线与冠军从头训练并各评估一次 test。
- 负结果和失败 trial 保留；不会为了“进化成功”删除落后结构。
- checkpoint、数据和原始 runs 不提交 Git，只保留复现命令和稳定标量。

## 后续扩展

增加新目标模型时，实现一个 evaluator：把 `Genome` 转成该模型配置，训练后返回统一 validation/test 指标。增加新论文结构时，在目标模型中实现独立 architecture operator，并补充论文 ID、方法摘要、shape 测试和最小训练测试。自然语言负责约束研究空间，不能直接生成并执行未经审计的任意代码。
