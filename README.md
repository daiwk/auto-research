# auto-research

一个面向 macOS/Linux 的机器学习研究平台，由两条正交工作流组成：**论文实现与评测**
负责把论文变成可信组件、公开数据实验和中文结论；**自动研究与进化**负责围绕给定
topic 或当前系统检索证据、并行实验和多轮迭代。两条工作流都可服务搜广推与 LLM
应用、基础模型、LLM 后训练、Agent，也可通过统一 adapter 扩展到其他主题。

可读版文档站：[daiwk.github.io/auto-research](https://daiwk.github.io/auto-research/)。站点支持全文搜索、MathJax 公式、Mermaid 架构图、深色模式和移动端横向滚动；本地预览方式见[文档说明](docs/getting-started.md)。

## 当前能力

### 论文实现与评测

每篇论文拥有独立模型、实验和报告代码，并强制声明复现保真度。当前包含四个研究域：

- **搜广推与 LLM 应用**：召回、粗排/精排、混排、内容理解、审核风控、广告、生成式推荐及 LLM 工业应用，要求真实
  线上 A/B 或用户明确认可的全流量证据；
- **基础模型**：网络结构、预训练、数据配方、多模态和推理效率，以公共 benchmark
  和真实训练对照为筛选依据；
- **LLM 后训练**：偏好优化、RL、OPD、reward 与训练稳定性；
- **Agent**：记忆、规划、工具使用和自我进化方法；既有可重复 mini-suite，也有真实
  临时仓库、文件编辑与回归测试的代码 Agent sandbox。

### 自动研究与进化

- **Topic research loop**：按任意 topic 检索论文，通过可配置实验命令和 search
  space 运行迭代，保存事件日志与指标缓存；
- **Directed evolution**：给定当前系统、数据和自然语言方向，把已审计组件与超参数
  组成 genome，按 validation 多代变异、淘汰和晋级，最终只对冠军运行 test；
- **内置 adapter**：搜广推支持 RankMixer/HyFormer，基础模型支持 micro‑LLM 的结构
  与数据配方进化，后训练支持 objective genome；Agent 的论文约束 genome 与多代 adapter 已接入统一控制器。
- **多模态大模型**：新增可从头训练的 `micro-vlm`、离线视觉问答 benchmark、视觉依赖对照和 connector 多轮进化；后续真实论文复现由同一 provider 承载。

所有论文文档都显式标注本地基线、实验组、主指标及相对变化；“内部消融提升”不会再被表述成相对统一基线或论文官方结果的提升。

支持两条研究轨道：

- `llm`：网络结构、预训练和后训练；内置 Tiny Shakespeare 低成本实验。
- `recommendation`：召回、粗排、精排、混排、loss、采样、训练与 serving；按论文优先使用 Amazon Beauty 5-core、MovieLens-1M 等公开数据。内部数据不可得时允许替换数据，但不允许用打分融合替代论文核心网络后仍宣称“复现”。

## 已审计的论文实现

仓库目前注册 **186 个**论文 adapter，统一事实源是
[`docs/research-manifest.json`](docs/research-manifest.json)。站点提供按研究域、机构、
主题和年份浏览的[论文实现索引](docs/reproductions/README.md)，每篇详情页包含论文链接、
一作机构、发布日期、原作者代码状态、本地 adapter/代码路径、架构与公式、原文线上/离线
结果以及本地公开数据结论。

工业搜广推论文必须给出量化线上 A/B 或用户认可的全流量证据；具名经典基线是逐篇记录的
例外。基础模型使用公开 benchmark 和同预算训练对照。历史指标已经统一迁移到 schema v2，
保留原始 seed 数量：少于 3 个 seed 的记录明确标成 smoke，不会被包装成稳定提升。

新增或更新 adapter 时，CI 会检查 registry、统一 manifest、论文信息块、证据定位、实验协议
和历史指标 schema 是否同步，不再手工维护 README 中容易过期的 186 行清单。

## 代码结构

```text
src/auto_research/
├── cli.py                         # run / reproduce / publish 命令入口
├── runner.py                      # research stages 编排
├── research_loop/                 # 迭代控制、指标缓存、事件日志
├── evolution/                     # 推荐与 micro-LLM 多代模型进化
├── post_training/                 # OPD、RL、偏好与过程奖励
├── agent_research/                # Agent 记忆、规划与工具评测
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

### 公开数据准备

推荐 adapter 会按既有数据入口准备 MovieLens；本批基础模型 adapter 使用官方 GSM8K 和 Stanford Alpaca，可一键下载到被 Git 忽略的 `data/`：

```bash
scripts/download_public_data.sh all

auto-research reproduce --paper off-context-grpo --dataset-dir data --seed 42
auto-research reproduce --paper dynamic-rubric --dataset-dir data --seed 42
```

脚本也支持单独传入 `gsm8k` 或 `alpaca`。数据、checkpoint 和单次 `runs/` 不提交 Git，只提交复核后的稳定 JSON 指标和复现说明。

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

# 两个新增子模块的零下载 smoke
./demo-post-training.sh
./demo-agent.sh
```

默认执行快速但真实的 RankMixer + MovieLens-100K evolve：仍然运行 3 个进化轮次，每轮 2 个候选，只缩小数据和单候选训练步数；基线是额外实验，不计作进化轮次。结果写到 `runs/demo-<platform>-recommendation/`。切换完整规模或 LLM 自动进化：

```bash
# 复用原 demo.sh 的 MovieLens-1M、3 代、6 candidates、3 seeds 设置
DEMO_PROFILE=full ./demo.sh

# 快速 micro-LLM 三轮结构/数据/后训练研究
DEMO_TRACK=llm ./demo.sh

# 完全离线的多模态训练与进化
DEMO_TRACK=multimodal ./demo.sh

# 完整 micro-LLM 研究
DEMO_TRACK=llm DEMO_PROFILE=full ./demo-linux-gpu.sh
```

首次运行会创建平台隔离的 `.venv-demo-*` 环境并安装依赖；后续直接复用。Linux GPU 如需指定 PyTorch CUDA wheel，可传 `TORCH_INDEX_URL`；其他参数见[运行环境指南](docs/runtime.md)。

后训练 demo 默认运行 Lightning OPD；可用同一 CLI 切换 DPO、KTO、ORPO、GRPO、
SLiC-HF、SteerLM、SPIN、
DAPO、GSPO、PPO-RLHF、RLOO、ReMax、Constitutional AI、RRHF、RAFT、GPRL、TCR、
IPO、SimPO、LUSPO 或 CoBA-RL。IPO、SimPO、LUSPO、CoBA-RL 使用真实 tokenizer
自由生成、verifier 和多 seed。Agent demo 还支持 WebGPT、SayCan、PAL、ART、
MRKL、HuggingGPT、Generative Agents、MemGPT，可通过
`METHOD=react|reflexion|metagpt|critic|agent-lightning|swe-agent|openhands
BENCHMARK=swebench-local EPISODES=12
./demo-agent.sh` 切换方法和环境。完整说明见
[LLM 后训练](docs/post-training/README.md)和[Agent 论文研究](docs/agent-research/README.md)。

后训练与 Agent 也已接入统一的多轮控制器，不再只能单算法运行：

```bash
auto-research evolve --model post-training --dataset arithmetic-smoke \
  --direction "组合比较 GRPO、DPO、OPD 与学习率、group size" \
  --generations 3 --population 6 --maximum-examples 512 --seeds 42,43,44

auto-research evolve --model post-training --dataset arithmetic-generate \
  --direction "比较 IPO、SimPO、LUSPO 与边界课程" \
  --generations 3 --population 4 --workers 2 --seeds 42,43,44

auto-research evolve --model agent --dataset evomem-mini \
  --direction "联合进化 memory、planner、tool policy 和 critic" \
  --generations 3 --population 8 --agent-episodes 240 --seeds 42,43,44

auto-research evolve --model agent --dataset swebench-local \
  --direction "组合 MetaGPT SOP、CRITIC、Agent Lightning 与代码 ACI" \
  --generations 3 --population 5 --workers 2 --agent-episodes 12
```

它们与推荐/LLM evolve 共用 validation 晋级、隔离 test、父子 genome、并行实验、失败留档和 HTML 研究看板。完整参数见[模型自动进化](docs/model-evolution.md)。

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

正式批量比较建议使用统一筛选、三个 seed 和可恢复状态文件：

```bash
auto-research reproduce --paper all --track recommendation --topic ranking \
  --fidelity full_pipeline --seeds 42,43,44 --workers 3 \
  --state-file runs/reproductions/ranking-state.json
```

新结果使用 schema v2，写入论文 manifest、L0–L3 评测层级、代码 commit、环境、预算
和 seed；多 seed 批次额外生成均值、标准差和 95% 置信区间。单 seed 只属于 smoke，
不能表述为稳定提升。

`--budget smoke|standard` 不是标签：每个 adapter 会在独立进程执行，分别施加 5 分钟
和 60 分钟硬截止，超时后终止进程并返回失败；可用 `--budget-seconds` 做显式覆盖。
`paper-specific` 保留论文 adapter 自己声明的训练日程，不增加统一截止。

每篇论文、每次运行写入独立且不可变的目录：

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── result.json   # 机器可读事实来源
└── report.md     # adapter 渲染的实验结论
```

`data/` 与 `runs/` 默认不进入 Git。经过复核的长期结论写入 `docs/reproductions/<arxiv-id>-<adapter>/README.md`。

## 运行模型自动进化

内置基础模型包括推荐侧 RankMixer/HyFormer，以及可在 Mac、Linux GPU 或 Linux CPU 从头训练的 `micro-llm`。推荐正式实验建议使用 MovieLens-1M：

候选来源需要先区分清楚：

- 运行时会按 `--direction` 搜索最新论文，但尚未在仓库实现的论文只标记为
  `evidence-only`，不会直接执行；
- 真正进入训练的论文结构或算法都已经在本仓库实现、测试并登记映射；
- 系统会在这些白名单算子之间做组合和超参数变异。这可以产生新的工程实验假设，
  默认不会根据论文 PDF 现场执行任意代码。可选的 `--candidate-generator-command`
  只把外部生成结果写入隔离候选区并执行验证；仍需显式 `candidate promote --approve`
  后，候选才可能在后续运行注册为可执行算子。

具体例子、离线模式和报告中的来源标记见
[候选到底从哪里来](docs/model-evolution.md#candidate-sources)。

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
  --benchmark-suite public \
  --fitness-metric public_composite \
  --seeds 42,43,44
```

调研方向同时约束论文检索和可执行结构空间；每一代并行比较论文启发结构与训练参数，再根据 validation 形成下一轮决策。目前包括 LONGER、UniMixer、WHALE、TMallGS、Long-History Transformer、RAMP 及组合结构；在线发现但尚未映射为安全算子的论文只进入证据池。

公共评测套件会在 MovieLens 上固定评估 overall、长历史、长尾目标、recent-only 和个性化特征受限切片；`public_composite` 用这些切片 NDCG 的等权平均晋级。若只想保持原先总体 NDCG 选择口径，使用 `--fitness-metric primary`；若要跳过额外切片，使用 `--benchmark-suite core`。

统一排序研究还可使用
`--benchmark-suite unirank --fitness-metric unirank_composite`，增加时间序
pointwise AUC/logloss；协议、官方五数据集和完整 runner 的边界见
[UniRank 公共评测接入](docs/unirank.md)。

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
  --benchmark-suite public \
  --fitness-metric public_composite \
  --seeds 42
```

默认 `micro-llm` 约 12M–16M 参数；WikiText-2、Tiny Shakespeare、Stanford Alpaca、官方 GSM8K 和 BPE tokenizer 自动下载/构建并缓存到 `data/`。第一轮只比较结构，第二轮只比较数据配方，第三轮比较 SFT、NEFTune、DynamicRubric 与 Off-Context GRPO。public suite 同时记录 Alpaca preference accuracy 和 GSM8K candidate Pass@1；详细定义见[模型自动进化文档](docs/model-evolution.md)。

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
