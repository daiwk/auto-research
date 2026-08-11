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

| benchmark | 标注格式 | 必报指标 |
|---|---|---|
| ScienceQA | 官方目录，含 `problems.json`、`pid_splits.json` | accuracy、image/text slice、parse rate |
| POPE | 官方 JSONL，逐行包含 `question_id`、`answer` | accuracy、precision、recall、F1、yes ratio、parse rate |
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
  --maximum-examples 500 --device cuda --offline

auto-research multimodal-eval \
  --benchmark scienceqa --annotations data/scienceqa \
  --predictions runs/scienceqa/predictions.jsonl \
  --maximum-examples 500 --seeds 42
```

不传 `--checkpoint-path --offline` 时会直接从 `--model-id` 下载。生成器旁路文件
`predictions.jsonl.metadata.json` 记录 revision、prompt/解码参数、设备和续跑计数；模型权重
与预测全集不提交 Git。

ScienceQA/POPE 的每行预测为：

```json
{"id": "question-id", "prediction": "yes / no / A / choice text"}
```

检索预测必须同时提供两个方向：

```json
{"image_id": "10", "ranked_text_ids": ["100", "101", "200"]}
{"text_id": "100", "ranked_image_ids": ["10", "20"]}
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

## 已执行的 ScienceQA checkpoint 子集

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
| L3 | lmms-eval 完整任务套件、跨 checkpoint 同预算矩阵 | 标准 VLM 能力与效率对照 |

任何仅在 L0 获得的提升都不能表述为通用视觉语言能力提升。
