# 多模态大模型统一评测协议

## L0：本地机制验证

`visual-shapes` 使用真实像素图像询问颜色、形状和方位。必须同时报告：

- 原图 accuracy；
- 打乱图 accuracy 与 `visual_dependency_delta`；
- 空白图 accuracy 与 `blank_image_delta`；
- 参数量、设备、训练步数、seed 和 connector。

Fitness 为：

$$
F=\operatorname{accuracy}+0.25\max(0,\operatorname{accuracy}-\operatorname{accuracy}_{shuffle}).
$$

## L1：公开自然图像缩小实验

`fashion-mnist-qa` 与 `cifar10-qa` 从同一多模态接口询问图像类别，分别覆盖轻量服饰
图像和 32×32 彩色自然图像。二者固定保留 1,000 条 validation 和 1,000 条 test，首次
下载逐文件校验官方 MD5，后续缓存可完全离线复跑。仍须报告原图、打乱图和空白图；
若视觉依赖差值接近零，不得把 accuracy 提升归因于 connector。

## L2：标准公开 benchmark

MR3 新增独立的 `multimodal-eval`，不把开放式问答和图文检索伪装成固定类别分类。
评测器只消费公开标注和模型预测，因而可以接入本项目 micro-VLM、任意 Hugging Face
checkpoint 或远程推理服务，同时保持指标实现不变。

MR6 再加入 `multimodal-retrieval-predict`：真实加载 CLIP/SigLIP 类公开 checkpoint，批量
编码图片和 caption，并在 GPU 上计算两个方向的精确正样本 rank。完整 COCO 5K 若保存所有
排序会产生约 1.25 亿个 ID，因此预测文件只保留 top-10 与精确首个正样本 rank；Recall@1/5/10
和 median rank 均无损，文件也可以提交独立 scorer 审计。

| benchmark | 标注格式 | 必报指标 |
|---|---|---|
| ScienceQA | 官方目录，含 `problems.json`、`pid_splits.json` | accuracy、image/text slice、parse rate |
| POPE | 官方 JSONL，逐行包含 `question_id`、`label`（兼容转换后的 `answer`） | accuracy、precision、recall、F1、yes ratio、parse rate |
| COCO/Flickr30K retrieval | Karpathy JSON，含 `images[].sentences[]` | I2T/T2I Recall@1/5/10、median rank、mean recall |

ScienceQA 随机基线管线检查：

```bash
auto-research multimodal-eval \
  --benchmark scienceqa \
  --annotations data/scienceqa \
  --baseline random --seeds 42,43,44
```

真实模型预测使用相同协议。`{seed}` 会分别读取三个独立预测文件：

```bash
auto-research multimodal-eval \
  --benchmark pope \
  --annotations data/pope/coco_pope_random.jsonl \
  --predictions 'runs/pope/predictions-seed{seed}.jsonl' \
  --seeds 42,43,44
```

### 直接从公开 checkpoint 生成预测

`multimodal-predict` 固定 `do_sample=false`，每完成一条就追加到 JSONL；同一路径重跑会
跳过已有 ID。在线机器会把 `main` 解析成不可变 Hugging Face commit；隔离开发机可把
事先同步的 snapshot 放在任意目录，同时显式保留官方模型 ID 与 commit：

```bash
auto-research multimodal-predict \
  --benchmark scienceqa \
  --annotations data/scienceqa \
  --image-root data/scienceqa/images \
  --output runs/scienceqa/predictions.jsonl \
  --model-id HuggingFaceTB/SmolVLM2-256M-Video-Instruct \
  --model-revision 067788b187b95ebe7b2e040b3e4299e342e5b8fd \
  --checkpoint-path checkpoints/smolvlm2-256m \
  --maximum-examples 500 --batch-size 8 --device cuda --offline

auto-research multimodal-eval \
  --benchmark scienceqa --annotations data/scienceqa \
  --predictions runs/scienceqa/predictions.jsonl \
  --maximum-examples 500 --seeds 42
```

不传 `--checkpoint-path --offline` 时会直接从 `--model-id` 下载。生成器旁路文件
`predictions.jsonl.metadata.json` 记录 revision、prompt/解码参数、设备和续跑计数；模型权重
与预测全集不提交 Git。

`--batch-size` 默认为 1，保证未知 checkpoint 的兼容性；正式 GPU 评测可从 8 开始逐步增加。
生成器会为 decoder-only VLM 临时启用左 padding，避免短提示从 PAD token 后错误续写；批次
过大导致 OOM 时，缩小 batch 后使用同一输出文件即可从已落盘 ID 继续，不必重算。

图文检索使用独立预测入口：

```bash
auto-research multimodal-retrieval-predict \
  --benchmark coco-retrieval \
  --annotations data/coco/dataset_coco.json \
  --image-root data/coco/images \
  --output runs/coco/clip-predictions.jsonl \
  --model-id openai/clip-vit-base-patch32 \
  --checkpoint-path checkpoints/clip-vit-base-patch32 \
  --batch-size 64 --score-batch-size 256 --device cuda --offline

auto-research multimodal-eval \
  --benchmark coco-retrieval \
  --annotations data/coco/dataset_coco.json \
  --predictions runs/coco/clip-predictions.jsonl \
  --seeds 42 --device cuda
```

同一个命令可将 benchmark 换为 `flickr30k-retrieval`。预测 metadata 只记录公开模型 ID、
不可变 revision、通用平台/设备、耗时和峰值显存，不记录主机名、系统发行版本、内部
PyTorch 构建串或本地绝对路径。

四类任务也可以用同一脚本按已经配置的数据集批量执行；未配置的任务会跳过，至少需要配置
一项：

```bash
SCIENCEQA_ROOT=data/scienceqa \
POPE_ANNOTATIONS=data/pope/coco_pope_adversarial.json \
POPE_IMAGE_ROOT=data/coco/val2014 \
COCO_ANNOTATIONS=data/coco/dataset_coco.json \
COCO_IMAGE_ROOT=data/coco \
VLM_CHECKPOINT_PATH=checkpoints/smolvlm2-256m \
RETRIEVAL_CHECKPOINT_PATH=checkpoints/clip-vit-base-patch32 \
DEVICE=cuda ./scripts/run-multimodal-checkpoint-matrix.sh
```

脚本默认不截断官方 split。生成式预测可续跑；图片、checkpoint、逐题预测和完整 ranking
均留在 `runs/`，Git 只保存最终聚合指标和复现配方。

### 用真实 checkpoint 做多轮 evolve

`vlm-checkpoint` 不训练或复制模型权重，而是在同一个已加载 checkpoint 上使用官方
ScienceQA **validation** 选择推理配方，搜索提示模板、hint、图像预缩放和确定性解码预算。
所有轮次结束后，控制器才在 **test** 上各运行一次初始基线与冠军，避免 test 泄漏：

```bash
auto-research evolve \
  --model vlm-checkpoint --dataset scienceqa \
  --direction "比较提示模板、hint、图像分辨率和解码预算" \
  --checkpoint-model-id HuggingFaceTB/SmolVLM2-256M-Video-Instruct \
  --checkpoint-revision 067788b187b95ebe7b2e040b3e4299e342e5b8fd \
  --checkpoint-path checkpoints/smolvlm2-256m \
  --checkpoint-annotations data/scienceqa \
  --checkpoint-image-root data/scienceqa/images \
  --maximum-examples 500 --generations 3 --population 4 \
  --workers 1 --seeds 42 --device cuda --offline
```

本地数据必须同时包含 `pid_splits.json`、`problems.json`、`images/val/` 和
`images/test/`。只下载 test 图片足够运行 `multimodal-predict --split test`，但不足以执行
无泄漏 evolve。单卡默认 `--workers 1`，因此 checkpoint 只加载一次；提高 workers 会让每个
隔离 worker 独立加载模型，应同时设置 `--gpu-slots` 和 `--gpu-memory-per-trial-mb`。

报告逐 trial 保存模型不可变 revision、实际 CUDA device、accuracy、image/text accuracy、
parse rate、单样本延迟和峰值显存。checkpoint、逐题预测和 `runs/` 仍不进入 Git。

2026-08-11 在 NVIDIA A30 上使用 SmolVLM2-256M revision
`067788b187b95ebe7b2e040b3e4299e342e5b8fd` 做过真实 checkpoint 工程 smoke：2 代、每代
2 个候选，加独立基线共 5 个 trial，全部在 CUDA 完成；峰值显存约 852.6–853.5 MiB，
parse rate 为 1.0。两题临时 split 的 accuracy 为 0.5，冠军仍为初始配方。这里的两题来自真实
ScienceQA 图文样本，但只是验证 checkpoint 加载、validation→test 控制流和报告链路，**不是**
官方 benchmark，也不能据此比较配方效果；正式结论必须使用完整官方 val/test 图像。
逐 trial 精确指标保存在
[`a30-vlm-checkpoint-smoke-20260811.json`](../experiments/a30-vlm-checkpoint-smoke-20260811.json)。

ScienceQA/POPE 的每行预测为：

```json
{"id": "question-id", "prediction": "yes / no / A / choice text"}
```

检索预测必须同时提供两个方向。手写完整 ranking 仍受支持；checkpoint 生成器使用紧凑格式：

```json
{"image_id": "10", "ranked_text_ids": ["100", "101"], "relevant_text_rank": 1}
{"text_id": "100", "ranked_image_ids": ["10", "20"], "relevant_image_rank": 1}
```

随机基线只验证标注解析、指标和多 seed 聚合，不代表 VLM 能力。真实结果必须保留生成
预测时的 checkpoint、prompt、图像预处理和 seed。公开数据请从
[ScienceQA](https://github.com/lupantech/ScienceQA)、
[POPE](https://github.com/RUCAIBox/POPE)、[COCO](https://cocodataset.org/) 和
[Flickr30K](https://shannon.cs.illinois.edu/DenotationGraph/) 的原始发布页取得；仓库不提交
图片、数据压缩包或模型 checkpoint。

## CIFAR-10 正式多 seed 入口

以下命令固定 architecture 和训练预算，validation 用于诊断，test 只做隔离报告：

```bash
auto-research multimodal-eval \
  --benchmark cifar10-qa --architecture micro_vlm_query \
  --steps 300 --maximum-examples 5000 --dimensions 192 \
  --batch-size 32 --seeds 42,43,44
```

生成目录同时包含机器可读 `metrics.json` 和中文 `report.md`。三个及以上 seed 才标记为
正式比较；报告统一包含 mean、sample std 与 95% CI 半径。

本仓库已按上述配方在官方 CIFAR-10 上完成 CPU 三 seed 实验：test accuracy
**19.43% ± 0.25 points**，打乱图/空白图为 10.43%/10.00%。结构化结果见
[`metrics/cifar10-qa-seeds42-44.json`](metrics/cifar10-qa-seeds42-44.json)。

## 已执行的 ScienceQA checkpoint 结果

MR6 已在官方完整 test split 4,241 条上执行同一 SmolVLM2-256M revision：accuracy
**54.92%**，image/text accuracy **62.82% / 47.75%**，coverage **100%**，parse rate
**99.95%**。这是单次确定性 checkpoint 运行，不标记为多 seed 正式比较。结构化结果见
[`metrics/scienceqa-smolvlm2-256m-full.json`](metrics/scienceqa-smolvlm2-256m-full.json)。

同一 checkpoint 在官方 POPE COCO adversarial 完整 3,000 条上的 accuracy **75.17%**，
precision **95.76%**、recall **52.67%**、F1 **67.96%**、yes ratio **27.50%**，解析率
**100%**。accuracy 受回答 no 的偏置影响，必须与 recall、F1 和 yes ratio 一起解读。
结构化结果见
[`metrics/pope-adversarial-smolvlm2-256m-full.json`](metrics/pope-adversarial-smolvlm2-256m-full.json)。

### 历史固定子集

单卡 A30、SmolVLM2-256M commit `067788b…`、官方 test 固定前 500 条，确定性 zero-shot
accuracy **56.80%**，image/text accuracy **62.87% / 51.33%**，parse rate **99.80%**。
该结果用于证明“真实 checkpoint → 可续跑预测 → 独立 scorer”闭环，不是完整 test 榜单或
多 seed 稳定性结论。完整配置与数据指纹见
[`metrics/scienceqa-smolvlm2-256m-500.json`](metrics/scienceqa-smolvlm2-256m-500.json)。

## 评测层级

| 层级 | 数据 | 可声明结论 |
|---|---|---|
| L1 | Fashion-MNIST / CIFAR-10 object QA | 真实公开图像上的缩小实验 |
| L2 | ScienceQA、POPE、COCO/Flickr retrieval | 可审计的真实 checkpoint 公开 benchmark 结果；固定子集必须显式标注 |
| L3 | `lmms-eval` 完整任务套件、跨 checkpoint 同预算矩阵 | 标准 VLM 能力与效率对照 |

## MR7：跨 checkpoint 矩阵

MR7 把单 checkpoint 运行升级为可恢复矩阵。每个 cell 固定 benchmark、样本上限、seed 与 batch fallback；OOM 只回退配置中显式列出的 batch，已写入预测继续复用。生成式 VLM 和检索编码器按 `family / benchmark` 分组，绝不放进同一排行榜。

本地还用缓存的官方 `SmolVLM2-256M-Video-Instruct` 不可变 revision 对一个真实像素 POPE smoke cell 跑通完整加载、生成、归一化、scorer、状态文件和 Markdown 报告链路；该样例仅验证执行路径，不作为模型质量结论。多 checkpoint 的比较结果必须在相同公开 split 和预算上另行运行，不能用 smoke 样本冒充。

```bash
auto-research multimodal-matrix \
  --config configs/multimodal-checkpoint-matrix.example.json \
  --output-dir runs/multimodal-matrix \
  --device cuda
```

输出 `matrix.json` 保存 revision、性能、延迟和峰值显存，`report.md` 给出同类可比较表。配置中的数据和 checkpoint 路径均为本地路径，仓库不提交数据或权重。

## MR8：完整 split 公平矩阵

MR8 把 MR7 的执行链路用于真实 L3 对照。生成式组固定相同 prompt、hint、确定性解码、
样本顺序与生成长度，比较 SmolVLM2 256M、500M 和 2.2B；检索组固定相同 COCO
Karpathy test 5K、图像预处理入口和全库双向排序，比较 CLIP ViT-B/32 与 SigLIP2
Base P16-224。每个模型均锁定 40 位不可变 revision。两组任务的目标函数和输出空间不同，
因此只在各自 `family / benchmark` 内比较，不计算跨组总排名。

公开 COCO 标注与图像可用校验和脚本准备：

```bash
./scripts/prepare-coco-retrieval.sh data/coco
```

脚本验证 Stanford Karpathy 标注的 SHA-256 与 COCO val2014 ZIP 的 MD5，只提取 test split
需要的 5,000 张图片并删除临时 ZIP，避免为一次 5K 评测长期占用完整 val2014 的磁盘空间。

完整矩阵配置位于
[`configs/multimodal-checkpoint-matrix.mr8.json`](https://github.com/daiwk/auto-research/blob/main/configs/multimodal-checkpoint-matrix.mr8.json)。
直接联网运行时无需填写 `checkpoint_path`；开发机离线运行时，在本地副本中为每个 cell
补充对应 snapshot 路径，然后执行：

```bash
auto-research multimodal-matrix \
  --config configs/multimodal-checkpoint-matrix.mr8.json \
  --output-dir runs/multimodal-matrix-mr8 \
  --seed 42 --device cuda --offline
```

执行器会拒绝同组中 split、样本数、prompt、hint、图像尺寸或解码预算不一致的配置；状态
文件同时绑定完整配置与 seed 的 SHA-256，修改协议后不能误续跑旧结果。checkpoint、COCO
图像和逐样本预测仍不提交 Git，只保存可审计的聚合指标、不可变 revision 与复现命令。

## 官方 lmms-eval 接口

仓库以可选依赖接入上游 `lmms-eval 0.7`，通过 argv 列表启动而非 shell 字符串，并保存完整 request。先 dry-run 审计命令：

```bash
pip install -e '.[lmms-eval]'
auto-research multimodal-lmms-eval \
  --model qwen2_5_vl \
  --model-args pretrained=Qwen/Qwen2.5-VL-3B-Instruct,device_map=auto \
  --tasks mme,mmmu_val \
  --limit 8 \
  --output-dir runs/lmms-eval/qwen25vl \
  --dry-run
```

去掉 `--dry-run` 才会下载任务并推理。上游任务模板和 scorer 属于 `lmms-eval`；本仓库只负责可审计调用、运行目录与后续统一矩阵汇总。

任何仅在 L0 获得的提升都不能表述为通用视觉语言能力提升。
