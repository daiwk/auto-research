# auto-research

一个面向 macOS 本地环境的机器学习研究闭环：输入 topic，检索最新论文，在公开数据集上实现和迭代实验，生成隔离的 JSON/Markdown 产物，并可通过 GitHub CLI 提交 Pull Request（GitLab 语境中的 MR）。

可读版文档站：[daiwk.github.io/auto-research](https://daiwk.github.io/auto-research/)。站点支持全文搜索、MathJax 公式、Mermaid 架构图、深色模式和移动端横向滚动；本地预览方式见[文档说明](docs/getting-started.md)。

## 当前能力

项目包含三层互补能力：

1. **Topic research loop**：按 topic 检索 arXiv，通过独立迭代控制器运行可配置参数搜索，逐轮保存 checkpoint、事件日志和可复用指标缓存。
2. **Paper adapters**：每篇论文拥有独立模型、实验和报告代码，并强制声明复现保真度；省略核心模型的实现只能作为概念验证。
3. **Model evolution**：给定已有模型和数据集，在线检索相关论文，把已审计的结构算子与层数、维度、学习率、优化器等组成 genome，按 validation 做多代变异、淘汰和晋级，最终只对冠军运行一次 test。

所有论文文档都显式标注本地基线、实验组、主指标及相对变化；“内部消融提升”不会再被表述成相对统一基线或论文官方结果的提升。

支持两条研究轨道：

- `llm`：网络结构、预训练和后训练；内置 Tiny Shakespeare 低成本实验。
- `recommendation`：召回、粗排、精排、混排、loss、采样、训练与 serving；按论文优先使用 Amazon Beauty 5-core、MovieLens-1M 等公开数据。内部数据不可得时允许替换数据，但不允许用打分融合替代论文核心网络后仍宣称“复现”。

## 已审计的论文实现

下表与代码 registry 保持 **65/65** 对齐；推荐论文要求量化生产 A/B，纯 LLM 论文要求公开 benchmark 与真实训练对照。完整论文总结、公式、架构、线上/离线效果和本地指标从[论文实现索引](docs/reproductions/README.md)进入。

| Level | Adapter | Paper / organization | What actually runs |
|---|---|---|---|
| 核心机制 | `fluid` | FLUID · TikTok/ByteDance | 跨域内容融合、RQ-LUCID、prefix n-gram、ID-free late fusion 与 staged warmup；fresh Hit +100.00%、NDCG -20.63% |
| 核心机制 | `memory-grafting` | Memory Grafting · Tsinghua/MSRA | 离线 teacher hidden bank、最长 n-gram 匹配、Engram fallback、gate+ShortConv；PPL 较 Transformer -3.59% |
| 核心机制 | `mhc` | mHC · DeepSeek-AI | 动态两流 HC、Sinkhorn 双随机投影与稳定性测量；谱范数 1.089→1.000，短程 PPL 未提升 |
| 核心机制 | `degre` | DeGRe · Alibaba | 累计价值 evaluator、lookahead beam mining 与 dense prefix distillation；NDCG@10 +3.31% |
| 核心机制 | `harness-lm` | HARNESS-LM · Microsoft/Bing Ads | 强 teacher、L2 query alignment、冻结文档索引对比精修；NDCG@10 -28.05% |
| 核心机制 | `grc` | GRC · Alibaba International | 结构化反思纠错 SFT、trajectory GRPO 与 EGRS；NDCG@10 -11.12% |
| 核心机制 | `mbgr` | MBGR · Meituan | business-aware SID、共享 experts 与 LDR；NDCG@10 -5.92% |
| 核心机制 | `growthgr` | GrowthGR · Alibaba | ItemLTV、RQ-SID、MoPO 与 constrained retrieval；NDCG@10 +2.05% |
| 核心机制 | `mesh` | MESH · Pinterest | 模块化 sub-towers、signal amplifier 与 RGBC；NDCG@10 -3.54% |
| 核心机制 | `sam` | SAM · Alibaba | 双路径兴趣/节奏、ASGU、TTNP 与 log-mask；NDCG@10 -6.60% |
| 核心机制 | `danet` | DANet · Alibaba/Tmall | FFT 折扣分解、user/context correction 与辅助回归；fresh Hit@10 +50.00% |
| 核心机制 | `proximity-features` | Proximity Features · Airbnb | 自适应 ZIP 分桶、稳定 proximity key 与群体冷启动特征；NDCG@10 +22.91% |
| 核心机制 | `nontp` | NONTP · Meituan | NTP + EMA teacher TCL + 跨域 TDL 联合训练，辅助模块推理期移除；Hit@10 -4.93%、NDCG -8.62% |
| 核心机制 | `akt-rec` | AKT-Rec · Alibaba | 真实 SmolLM LoRA 双阶段训练、RQ-VAE SID、非对称 head→tail 迁移和活动度门控；AUC +3.44%、GAUC +5.53% |
| 完整核心链路 | `s-grec` | S-GRec · Tencent/WeChat | 真实 LLM PSJ 方面 SFT+GRPO、pairwise aggregator、SID 生成、5% 稀疏 A2PO；validation 晋级，test HR@10 +0%、NDCG -4.53% |
| 完整核心链路 | `pinterest-ads-llm` | Complementary LLM Predictor · Pinterest | SmolLM LoRA SFT+GRPO、advertiser constrained decoding、two-tower 补充召回与排序特征；GRPO Recall@20 +0%，排序 AUC +2.59% |
| 完整核心链路 | `lwgr` | LWGR · Alibaba International | IBQ parallel soft instructions 穿过真实 LLM、BOS cross-attention、reference constraint、primal-dual；Recall@10 +0%，NDCG -4.29% |
| 完整核心链路 | `sigma` | SIGMA · Alibaba/AliExpress | LLM 多视角 grounding、hybrid prefix+ID、七任务 SFT、三步生成/APF；选中 top1-prefix 的 HR@20 0.0078→0.0703，APF 未提升 |
| 完整核心链路 | `univa` | UniVA · Tencent/WeChat | Commercial SID、HSTU、MoR+Sparse-MoE、generation/value 双头、SL↔PPO/value、个性化 trie beam；HR@100 +4.76%，ValueHR +6.56%，wNDCG -8.43% |
| 核心机制 | `prompt-generation` | Prompt Generation · Alibaba/Taobao | 同源 Amazon Office、Qwen2.5-0.5B、双 JSON/mean merger/LoRA SFT；HR@10 -11.11%，压缩打分 -90.38% |
| 完整核心链路 | `precise` | PRECISE · Tencent/WeChat | SmolLM contextual token、top-k MoE、交替训练、UT→TT+BPR；Recall@10 +40.0%，Cold Recall -50.0% |
| 完整核心链路 | `pinrec` | PinRec · Pinterest | outcome conditioning、unordered window multi-token、ANN vectors；Recall@10 -27.78% |
| 完整核心链路 | `genrank` | GenRank · Xiaohongshu | item/action 组织对照、位置/时间偏置；延迟 -25.66%，AUC -0.46% |
| 完整核心链路 | `learn` | LEARN · Kuaishou | 冻结 LLM CEG、PCH、dense all-position；NDCG +233.10%，头部偏置明显 |
| 完整核心链路 | `notellm` | NoteLLM · Xiaohongshu | T5 compression token、行为 GCL、类别 CSFT；NDCG +7.15% |
| 完整核心链路 | `kar` | KAR · Huawei | SmolLM2 真实生成用户/物品知识、缓存、hybrid experts；AUC 均值 +0.81% |
| 完整核心链路 | `bahe` | BAHE · Ant Group | 浅层原子行为缓存、上层行为聚合；样本耗时 -53.61%，AUC -2.94% |
| 完整核心链路 | `beque` | BEQUE · Alibaba | T5 SFT、无泄漏 beam 自采样、离线检索反馈、PRO；feedback +30.03%，increment -66.02% |
| 完整核心链路 | `onerec-v2` | OneRec-V2 · Kuaishou | KuaiRand 真实时长反馈、RQ-SID、Lazy Decoder、DARS、GBPO；latency -54.78%，GBPO 均值 +21.66% |
| 完整核心链路 | `plum` | PLUM · Google/YouTube | 135M decoder-only LM；2×2 CPT 消融；CPT 降低 loss，但 Recall@10 未提升 |
| 完整核心链路 | `onerec` | OneRec · Kuaishou | RQ-SID、session MoE、reward model、self-hard DPO；DPO 后 NDCG 降至 0 |
| 完整核心链路 | `g2rec` | G2Rec · Meta | soft graph clustering、交替 interest token decoder、双 loss；NDCG@10 +11.92% |
| 核心机制 | `llm-ad-retrieval` | LLM Retrieval · Meta | domain SFT、LLM attribute head、层级 Jaccard 语义图；Recall@20 +11.90%，边分数漂移 -77.36% |
| 完整核心链路 | `seral` | SERAL · Alibaba | cognition profiles、CDI、SFT→IPO、nearline；相对 DIN NDCG@10 +50.60% |
| 完整核心链路 | `leadre` | LEADRE · Tencent | S-ID、intent/auxiliary tasks、SFT→DPO；相对 DIN +12.94%，DPO 消融退化 |
| 完整核心链路 | `cobra` | COBRA · Baidu | sparse→dense cascade、BeamFusion；相对 DIN +25.75% |
| 核心机制 | `argus` | ARGUS · Yandex | feedback→next-item decomposition；相对 DIN -4.12% |
| 核心机制 | `gr4ad` | GR4AD · Kuaishou | UA-SID、LazyAR、VSL、RSPO；相对 DIN +69.67%，头部集中 |
| 核心机制 | `cross-domain-kd` | Zero-shot KD · Google/YouTube | 跨域 teacher logits + auxiliary distillation；target split 相对 DIN -68.46% |
| 核心机制 | `mm-llm` | MM-LLM · Meta | query cross-attention caption tokens + ranking fusion；相对 DIN -13.23% |
| 完整核心链路 | `mixformer` | MixFormer · ByteDance/Douyin | matched-budget stacked/unified Transformer；NDCG@10 +17.41% |
| 完整核心链路 | `rankmixer` | RankMixer · ByteDance/Douyin | token mixing、per-token FFN、DTSI sparse MoE；dense 最优，sparse 未追平 |
| 完整核心链路 | `hyformer` | HyFormer · ByteDance/Douyin | query generation/decoding/boosting；NDCG@10 +143.77%，头部偏置同步上升 |
| 完整核心链路 | `onetrans` | OneTrans · ByteDance | mixed QKV/FFN、causal attention、pyramid；NDCG@10 +123.58%，head share 92% |
| 完整核心链路 | `rec-distill` | Rec-Distill · ByteDance | black-box logits、双塔去偏、batch+stream；本地 transferability -4.11% |
| 完整核心链路 | `sasrec` | SASRec | causal self-attention、point-wise FFN、pairwise BCE；全库 NDCG@10 0.02933，与 popularity 基本持平 |
| 完整核心链路 | `lsvcr` | LSVCR · Kuaishou | q/v-LoRA、双序列 SSC/VCC 对齐；comment NDCG +50.40%，item -56.42% |
| 完整核心链路 | `msd` | MSD · Meituan | teacher→T5 自回归蒸馏、LoRA、频次缓存融合；AUC +1.55% |
| 完整核心链路 | `lum` | LUM · Alibaba | next-condition-item、group query、DLRM 知识利用；AUC +14.60% |
| 核心机制 | `sessionrec` | SessionRec · Meituan | KuaiRand 真实 session、多正例召回与曝光困难负例；NDCG@20 -22.05% |
| 核心机制 | `saviorrec` | SaviorRec · Alibaba | 行为对齐 encoder、RQ-SID、zero-init MBA、双向注意力；cold AUC +6.92% |
| 核心机制 | `hstu` | HSTU · Meta | UVQK、非 softmax aggregation、U-gate、all-position training；matched SASRec 对照下 NDCG@10 -17.73% |
| 核心机制 | `din` | DIN · Alibaba | candidate-conditioned local activation、Dice、CTR BCE；mean-pool 对照下 NDCG@10 -6.97% |
| 核心机制 | `tiger` | TIGER · Google | RQ-VAE Semantic ID、collision token、自回归检索；matched random ID 对照下 NDCG@10 -39.16% |
| 核心机制 | `m6rec` | M6-Rec · Alibaba | 冻结真实预训练 LM、option tuning、逐层 adapter；3-seed AUC +0.12% ± 0.41% |
| 核心机制 | `transact-v2` | TransAct V2 · Pinterest | 候选锚定 lifelong retrieval、early fusion、sampled-softmax NAL；NDCG@10 +92.65%，头部占比明显上升 |
| 核心机制 | `pinfm` | PinFM · Pinterest | NTL/MTL/FTL 预训练、DCAT、下游微调；validation -6.46%，test -3.57%，长尾覆盖显著增加 |
| 核心机制 | `sis` | SIS | 论文的 off-policy token importance-sampling 变换 |
| 核心机制 | `mdcns` | MDCNS | 三源负采样、分歧/共识筛选与双模型更新 |
| 核心机制 | `memento` | Memento · Meta | query-conditioned MMR 长历史检索 |
| 核心机制 | `cluster-goobs` | Cluster GOOBS · Meta | cluster-conditioned online hard-negative sampling |
| 概念验证 | `llatte` | LLaTTE · Meta | 未实现 MLA、DHEN、semantic LLM features |
| 概念验证 | `self-evolving-rec` | Self-Evolving RecSys · Google | 未运行 LLM agent 和真实线上反馈闭环 |
| 概念验证 | `cmsl` | CMSL · Meta | 未训练 contextual lenses / HSTU backbone |
| 概念验证 | `longer` | LONGER · ByteDance/Douyin | 未训练 hybrid attention / InnerTrans |

三级定义和逐篇审计见[论文实现索引](docs/reproductions/README.md)。概念验证产生的旧指标只用于调试假设，不支持论文效果结论，也不再出现在默认批量复现中。

## 代码结构

```text
src/auto_research/
├── cli.py                         # run / reproduce / publish 命令入口
├── runner.py                      # research stages 编排
├── research_loop/                 # 迭代控制、指标缓存、事件日志
├── datasets.py                    # 公开数据下载和缓存
├── papers.py                      # arXiv 检索
└── reproductions/
    ├── base.py                    # adapter 稳定接口
    ├── registry.py                # 自动发现 */adapter.py
    ├── reporting.py               # 隔离的 JSON/Markdown 产物
    ├── rec_utils.py               # 序列推荐共享数据切分与指标
    ├── llm_rec_data.py            # LLM+推荐共享 CTR 文本数据与 AUC
    ├── sequence_training.py       # 序列模型共享的 all-position 训练与全库评估
    └── <paper>/
        ├── adapter.py             # 论文元数据与注册
        ├── model.py               # 论文特有模型或算法
        ├── experiment.py          # baseline、调参、评估
        └── report.py              # 论文专用 Markdown 报告

docs/reproductions/<arxiv-id>-<adapter>/README.md
docs/reproductions/catalog/          # 按公司 / 主题 / 年月的稳定导航
tests/reproductions/
```

新增论文不需要修改 CLI：registry 会自动发现带有 `adapter.py` 的论文目录。详细约定见[架构与扩展指南](docs/architecture.md)。

本轮参考了 [automated-w2s-research](https://github.com/safety-research/automated-w2s-research) 的 idea 隔离、统一配置、迭代研究和结果缓存设计，但没有合并其 Claude/Flask/RunPod/VERL 重型运行栈。逐项取舍见[架构采用记录](docs/design/automated-w2s-adoption.md)。

## 安装

要求 macOS/Linux 和 Python 3.11+。`auto-research` 不是需要单独下载的外部程序；它由本仓库 `pyproject.toml` 中的命令入口提供。在仓库根目录安装项目后，虚拟环境里就会出现该命令。

```bash
cd /path/to/auto-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip

# 模型自动进化、推荐网络与蒸馏实验
python -m pip install -e '.[neural-recs]'

# Mac 本地 decoder-only LLM 自动进化
python -m pip install -e '.[llm-evolution]'

# 验证命令已经安装
auto-research --help
auto-research evolve --help

# 开发和测试依赖（可选）
python -m pip install -e '.[dev]'

# PLUM 与 PRECISE 的真实 LLM 阶段另装可选依赖
python -m pip install -e '.[plum]'
```

这里的 `-e` 表示可编辑安装：更新本仓库的 Python 源码后通常不用重新安装。每次新开终端需要先执行 `source .venv/bin/activate`；不想激活环境时，也可以直接运行 `.venv/bin/auto-research --help`。若刚更新了依赖配置，再执行一次 `python -m pip install -e '.[neural-recs]'`。

### Mac、Linux GPU 与 Linux CPU

所有训练入口统一支持 `--device auto|cpu|mps|cuda|cuda:<index>`。`auto` 的探测顺序是 CUDA、Apple MPS、CPU；显式指定但不可用时会直接报错。Linux CPU 可用 `--cpu-threads` 控制每个 worker 的 PyTorch 线程数。

```bash
# Linux 单卡 GPU
auto-research reproduce --paper din --device cuda:0 --seed 42
auto-research evolve --model rankmixer --dataset movielens-1m \
  --direction "加入 LONGER 与 UniMixer" --device cuda:0 --workers 1

# Linux CPU
auto-research reproduce --paper din --device cpu --cpu-threads 16 --seed 42

# Mac MPS（不指定时也会自动探测）
auto-research reproduce --paper din --device mps --seed 42
```

CUDA/CPU PyTorch 的安装方式、多卡隔离和 worker 配置见 [GPU 与 Linux CPU 运行指南](docs/runtime.md)。

### 一键 Demo

仓库根目录提供自动识别平台的入口：

```bash
./demo.sh
```

也可以明确选择运行环境：

```bash
./demo-mac.sh
./demo-linux-cpu.sh
./demo-linux-gpu.sh
```

默认执行快速但真实的 RankMixer + MovieLens-100K evolve：仍然运行 3 个进化轮次，每轮 2 个候选，只缩小数据和单候选训练步数；基线是额外实验，不计作进化轮次。结果写到 `runs/demo-<platform>-recommendation/`。切换完整规模或 LLM 自动进化：

```bash
# 复用原 demo.sh 的 MovieLens-1M、3 代、6 candidates、3 seeds 设置
DEMO_PROFILE=full ./demo.sh

# 快速 micro-LLM 三轮结构/数据/后训练研究
DEMO_TRACK=llm ./demo.sh

# 完整 micro-LLM 研究
DEMO_TRACK=llm DEMO_PROFILE=full ./demo-linux-gpu.sh
```

首次运行会创建平台隔离的 `.venv-demo-*` 环境并安装依赖；后续直接复用。Linux GPU 如需指定 PyTorch CUDA wheel，可传 `TORCH_INDEX_URL`；其他参数见[运行环境指南](docs/runtime.md)。

Tiny Shakespeare、MovieLens-100K/1M、Amazon Beauty 5-core、KuaiRand-Pure 和 MDCNS 作者 Beauty 切分会按 adapter 首次运行时下载到 `data/`，之后复用本地缓存。M6-Rec 使用 MovieLens 官方文本元数据；OneRec-V2 使用 KuaiRand 的真实播放/时长/负反馈。下载器只接入体量适合本地 Mac 的公开原始数据，生产内部数据不会伪造为“原数据复现”。

博客选出的 KAR、BAHE、BEQUE 均使用 MovieLens-100K：KAR 会用本地小型指令模型真实生成知识，BAHE 会落盘复用原子行为表示，BEQUE 会训练 seq2seq 模型并用公开目录实现离线检索反馈。三者都保留生产论文的核心训练链路，但不声称 MovieLens 等价于企业私有日志。

博客两个“工业界+落地”章节已解析 94 个主条目、138 个 arXiv 链接；选文标准、实现状态、暂缓候选与本地结论统一维护在[复现总览](docs/reproductions/README.md)。

## 运行论文复现

列出的 key 会由 adapter registry 动态生成：

```bash
auto-research list
auto-research reproduce --help
```

运行单篇或全部论文：

```bash
auto-research reproduce --paper memento --seed 42
auto-research reproduce --paper sasrec --seed 42
auto-research reproduce --paper hstu --seed 42
auto-research reproduce --paper transact-v2 --seed 42
auto-research reproduce --paper pinfm --seed 42
auto-research reproduce --paper m6rec --seed 42
auto-research reproduce --paper kar --seed 42
auto-research reproduce --paper bahe --seed 42
auto-research reproduce --paper beque --seed 42
auto-research reproduce --paper precise --seed 42
auto-research reproduce --paper pinrec --seed 42
auto-research reproduce --paper genrank --seed 42
auto-research reproduce --paper learn --seed 42
auto-research reproduce --paper notellm --seed 42
auto-research reproduce --paper onerec-v2 --seed 42
auto-research reproduce --paper self-evolving-rec --seed 42
auto-research reproduce --paper prompt-generation --seed 42
auto-research reproduce --paper univa --seed 42
auto-research reproduce --paper pinterest-ads-llm --seed 42
auto-research reproduce --paper lwgr --seed 42
auto-research reproduce --paper sigma --seed 42
auto-research reproduce --paper s-grec --seed 42
auto-research reproduce --paper all --seed 42

# 仅在明确需要查看旧概念验证时加入
auto-research reproduce --paper all --include-concept-demos --seed 42
```

每篇论文、每次运行写入独立且不可变的目录：

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── result.json   # 机器可读事实来源
└── report.md     # adapter 渲染的实验结论
```

`data/` 与 `runs/` 默认不进入 Git。经过复核的长期结论写入 `docs/reproductions/<arxiv-id>-<adapter>/README.md`。

## 运行模型自动进化

内置基础模型包括推荐侧 RankMixer/HyFormer，以及可在 Mac、Linux GPU 或 Linux CPU 从头训练的 `micro-llm`。推荐正式实验建议使用 MovieLens-1M：

```bash
auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "加入 LONGER、UniMixer 和相关高效 Transformer 结构" \
  --workers 3 \
  --generations 3 \
  --population 4 \
  --steps 100 \
  --papers 8 \
  --seeds 42,43,44
```

调研方向同时约束论文检索和可执行结构空间；每一代并行比较论文启发结构与训练参数，再根据 validation 形成下一轮决策。目前还包括 LONGER、UniMixer 及组合结构；在线发现但尚未映射为安全算子的论文只进入证据池。

运行产物位于 `runs/evolution/<model>-<timestamp>/`，包含机器可读 JSON、中文 Markdown 报告和可直接打开的 HTML 研究看板。详细协议见[模型自动进化文档](docs/model-evolution.md)。

LLM 结构、预训练数据和后训练方法的三轮自动研究示例：

```bash
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

默认 `micro-llm` 约 12M–16M 参数；WikiText-2、Tiny Shakespeare、Stanford Alpaca 和 BPE tokenizer 自动下载/构建并缓存到 `data/`。第一轮只比较结构，第二轮只比较数据配方，第三轮只比较后训练方法。

## 运行 Topic research loop

LLM 示例：

```bash
auto-research run \
  --topic "efficient post-training and preference optimization" \
  --track llm \
  --trials 8 \
  --papers 8
```

推荐算法示例：

```bash
auto-research run \
  --topic "ranking loss and hard negative sampling" \
  --track recommendation \
  --trials 8 \
  --papers 8
```

通用运行产物位于 `runs/<timestamp>/report.md`、`result.json` 和 `events.jsonl`。内置低成本实验用于验证研究流水线和快速筛选假设，不等同于某篇论文的专用 adapter。

相同实验修订、数据目录、seed 和参数的已完成 trial 会复用 `.auto-research/cache/` 中的标量指标。使用 `--force-rerun` 可强制重跑。外部实验代码必须在配置中设置 `experiment_revision` 才会启用缓存，代码或数据协议变化后应更新该值。

## 接入外部真实实验

先生成配置：

```bash
auto-research init research.json --track recommendation
```

配置可指定实现命令、训练命令和搜索空间：

```json
{
  "topic": "new retrieval loss",
  "track": "recommendation",
  "max_papers": 10,
  "max_trials": 6,
  "implementation_command": ["codex", "exec", "Read AUTO_RESEARCH_MANIFEST and implement the selected hypothesis"],
  "proposal_command": ["python", "experiments/propose_next.py"],
  "experiment_command": ["python", "experiments/train.py"],
  "search_space": {
    "learning_rate": [0.0001, 0.0003],
    "architecture": ["baseline", "candidate"]
  },
  "metric_name": "validation_loss",
  "direction": "minimize",
  "experiment_revision": "retrieval-loss-v1",
  "timeout_seconds": 3600
}
```

论文清单通过 `AUTO_RESEARCH_MANIFEST` 传给实现命令，每轮参数通过 `AUTO_RESEARCH_PARAMS` 传给实验命令。实验命令最后一行必须输出指标 JSON，例如：

```json
{"validation_loss": 1.234}
```

如果配置 `proposal_command`，它会在每轮收到 `AUTO_RESEARCH_MANIFEST` 和 `AUTO_RESEARCH_HISTORY`，最后一行返回 `{"params": {...}}` 或 `{"stop": true}`。因此 agent 能依据前几轮成功、失败和缓存结果自适应选择下一组参数；未配置时继续使用确定性搜索空间。

## 提交 GitHub PR

```bash
brew install gh
gh auth login

auto-research publish runs/<timestamp>/report.md \
  --title "research: evaluate retrieval loss"
```

发布命令要求工作区没有无关修改；必要时从 `main`/`master` 创建 `agent/...` 分支，只暂存指定报告，提交、推送并创建 draft PR。增加 `--ready` 可创建非草稿 PR。

## 实验解释边界

- 论文新旧以 arXiv `submittedDate` 为准，并记录实际检索日期。
- 替换私有数据、缩小模型和省略生产基础设施是允许的规模折算；替换论文核心网络、训练目标或推理路径则必须降级为“概念验证（非论文复现）”。
- `reproduction_fidelity` 随每次 JSON/Markdown 产物写出；默认 `--paper all` 不运行概念验证。
- 论文披露的线上 A/B 与本机离线指标始终分开记录。
- 正向、负向和跨 seed 不稳定结果都会保留，参数只能根据 validation 选择。

## 测试

```bash
pytest
```

当前测试覆盖 adapter 自动发现、核心论文机制、运行产物隔离和通用 research loop。
