# 安装、数据与 Demo

[返回项目首页](README.md) · [文档站](https://daiwk.github.io/auto-research/)

## 安装

要求 macOS/Linux 和 Python 3.11+。`auto-research` 不是需要单独下载的外部程序；它由本仓库 `pyproject.toml` 中的命令入口提供。在仓库根目录安装项目后，虚拟环境里就会出现该命令。

```bash
cd /path/to/auto-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

# 模型自动进化、推荐网络与蒸馏实验
auto-research-install-runtime --extras neural-recs

# Mac 本地 decoder-only LLM 自动进化
auto-research-install-runtime --extras llm-evolution

# 验证命令已经安装
auto-research --help
auto-research evolve --help

# 开发和测试依赖（可选）
python -m pip install -e '.[dev]'

# PLUM 与 PRECISE 的真实 LLM 阶段另装可选依赖
auto-research-install-runtime --extras plum
```

这里的 `-e` 表示可编辑安装：更新本仓库的 Python 源码后通常不用重新安装。
`auto-research-install-runtime` 会先 dry-run；如果可选依赖准备替换现有 PyTorch，会在真正
安装前退出。每次新开终端需要先执行 `source .venv/bin/activate`；不想激活环境时，也可以
直接运行 `.venv/bin/auto-research --help`。

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

# CIFAR-10 固定配方三 seed 正式评测（首次下载约 163MB）
auto-research multimodal-eval --benchmark cifar10-qa \
  --architecture micro_vlm_query --steps 300 --seeds 42,43,44

# 真实视频/音频 checkpoint 评测；先按文档准备官方媒体子集
auto-research multimodal-video-eval --help
auto-research multimodal-audio-eval --help

# 完整 micro-LLM 研究
DEMO_TRACK=llm DEMO_PROFILE=full ./demo-linux-gpu.sh
```

首次运行会创建平台隔离的 `.venv-demo-*` 环境并安装依赖；后续直接复用。Linux GPU 如需指定 PyTorch CUDA wheel，可传 `TORCH_INDEX_URL`；其他参数见[运行环境指南](docs/runtime.md)。
视频、音频公开 checkpoint、固定数据 revision 和 A30 验证结果见
[视频与音频评测](docs/multimodal-models/video-audio.md)。

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

真实 checkpoint / executor 与具身训练入口：

```bash
auto-research agent-policy-train --steps 10 \
  --train-episodes 10 --validation-episodes 4 --test-episodes 4 \
  --seeds 42,43,44 --device cuda
auto-research agent-matrix --episodes 12 --seeds 42,43,44
auto-research embodied-post-train --dataset-root data/svla_so100_pickplace \
  --checkpoint-path checkpoints/smolvla_base \
  --vlm-checkpoint-path checkpoints/SmolVLM2-500M-Video-Instruct \
  --offline --steps 1 --device cuda
```

前两条分别把 Agent Lightning transition credit 回传到 SmolLM2 和比较同预算真实
代码 executor；第三条调用官方 LeRobot 对 SmolVLA 做 flow-matching 后训练。数据、模型、
checkpoint 不提交，只保留 revision、命令、指标和边界。

它们与推荐/LLM evolve 共用 validation 晋级、隔离 test、父子 genome、并行实验、失败留档和 HTML 研究看板。完整参数见[模型自动进化](docs/model-evolution.md)。

Tiny Shakespeare、MovieLens-100K/1M、Amazon Beauty 5-core、KuaiRand-Pure 和 MDCNS 作者 Beauty 切分会按 adapter 首次运行时下载到 `data/`，之后复用本地缓存。M6-Rec 使用 MovieLens 官方文本元数据；OneRec-V2 使用 KuaiRand 的真实播放/时长/负反馈。下载器只接入体量适合本地 Mac 的公开原始数据，生产内部数据不会伪造为“原数据复现”。

博客选出的 KAR、BAHE、BEQUE 均使用 MovieLens-100K：KAR 会用本地小型指令模型真实生成知识，BAHE 会落盘复用原子行为表示，BEQUE 会训练 seq2seq 模型并用公开目录实现离线检索反馈。三者都保留生产论文的核心训练链路，但不声称 MovieLens 等价于企业私有日志。

博客两个“工业界+落地”章节已解析 94 个主条目、138 个 arXiv 链接；选文标准、实现状态、暂缓候选与本地结论统一维护在[复现总览](docs/reproductions/README.md)。
