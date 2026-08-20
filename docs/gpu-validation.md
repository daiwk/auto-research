# A30 GPU 回溯验证

本页记录 2026-08-11 对仓库 GPU 路径的工程回溯。它回答“代码能否在真实 CUDA 环境执行”，
不替代论文 benchmark，也不把单 seed、缩步数 smoke 写成效果结论。

## 环境与口径

| 项目 | 值 |
|---|---|
| 主机 | 用户提供的单卡 Linux 开发环境 |
| GPU | NVIDIA A30 24GB，单卡 |
| CUDA | 12.8 |
| 数据 | MovieLens、Amazon Beauty、MiniOneRec 等本地公开数据 |
| 通过条件 | adapter 成功结束，且证据日志至少记录一次实际解析到 CUDA 的 `device_for` 调用 |

扫描器只检查 adapter 自己的实现文件。扁平共享 adapter 不再因为同目录中无关模块使用 PyTorch
而被误判为 GPU adapter；修复这一边界后，显式 GPU 路径从带 30 个假阳性的 92 项收敛为
**62 项**。

## 结论

- 有效 GPU adapter：**62**；最终 `gpu_pass`：**62/62**；遗留失败或超时：**0**。
- 初轮结果为 41 通过、15 失败、6 超时。失败项逐一补齐公开数据/本地模型缓存并修复代码；
  超时项使用相同数据和缩步数 smoke 或更长硬超时重跑。
- 62 项有效运行时之和约 1,926.8 秒。这个数字不包含定位问题时的失败尝试，也不是吞吐 benchmark。
- checkpoint、模型缓存、逐 adapter 原始 JSONL 和训练产物只保留在开发机，不进入 Git。

最终通过的 adapter：

<details>
<summary>展开 62 项</summary>

`akt-rec`、`argus`、`asarl`、`bahe`、`barge`、`beque`、`ccformer`、`cobra`、
`core-relevance`、`cross-domain-kd`、`data-orchestra`、`degr`、`g2rec`、`genrank`、
`gr4ad`、`gryphon-v2`、`gzip-sparse-attention`、`kar`、`leadre`、`learn`、
`llm-ad-retrieval`、`lsvcr`、`lum`、`lwgr`、`m6rec`、`minimax-sparse-attention`、
`mixformer`、`mm-llm`、`mobius-rope`、`mosaic`、`msd`、`notellm`、`onerec`、
`onerec-v2`、`onetrans`、`open-web-ufm`、`oxygenrec-v2`、`pinequalizer`、
`pinterest-ads-llm`、`plum`、`precise`、`prompt-generation`、`rankmixer`、
`rec-distill`、`recap`、`recgpt-mobile`、`recgpt-v3`、`rocs`、`s-grec`、
`saviorrec`、`self-evolving-rec`、`seral`、`sessionrec`、`sigma`、`slimper`、
`sort-gen`、`tiger`、`tokenminds`、`uame`、`unir2`、`univa`、`windowed-mtp`。

</details>

## 回溯发现并修复的问题

| 路径 | 问题 | 修复与 A30 结果 |
|---|---|---|
| RecGPT-Mobile | weight-only INT8 重建为 FP32，与 BF16 activation 矩阵乘类型不一致 | 重建权重和 bias 对齐 activation device/dtype；124.1 秒通过 |
| PLUM | 服务器 PyTorch 无 CPU LAPACK，Transformers 新词表协方差初始化失败；默认训练不适合 smoke | 只对明确 LAPACK 错误回退标准初始化；smoke 保留四分支但缩小 SID/CPT/SFT 步数；370.2 秒通过 |
| M6Rec / BAHE / LEARN | 老 BERT-tiny config 缺 `model_type`，Transformers 5 的 Auto 类无法推断 | 使用实现本就依赖的 `BertModel` / `BertTokenizer`；三项均通过 |
| BAHE | Transformers 4/5 的 `BertLayer` 返回类型不同，旧 `[0]` 在 v5 错删 batch 维 | 统一提取 tuple/tensor hidden，并拒绝旧错误维度缓存；5.2 秒通过 |
| LWGR | cuDNN GRU hidden 非连续；BF16 LLM 与 FP32 recommender 边界未显式转换 | hidden contiguous，LLM 输入/输出显式跨 dtype；9.6 秒通过 |
| AKT-Rec / S-GRec / SIGMA | BF16 checkpoint hidden 直接进入 FP32 辅助 head | 在 checkpoint 与任务 head 边界显式转换；三项均通过 |
| RECAP | 正式 80/60/45 step 路径超过统一 smoke 时限 | smoke 使用 1/1/1 step，正式参数不变；238.3 秒通过 |
| GPU 扫描器 | 共享 `reproductions/` 目录让 30 个无 GPU adapter 继承无关 hook | 扁平 adapter 只扫描自身文件；最终有效集合 62 项 |

## evolve 代表链路

除论文 adapter 外，还在同一 A30 验证了统一多轮控制器的四类 GPU 链路：

| 链路 | 工程 smoke 结果 |
|---|---|
| RankMixer / MovieLens | baseline + 两个候选均完成；LONGER 候选 validation NDCG@10 `0.01145`，仅为截断 smoke |
| micro-LLM / WikiText-2 | GQA 冠军；validation perplexity `254.498`，instruction loss `5.521` |
| micro-VLM / visual-shapes | validation accuracy `0.325`；验证图像 connector 与 CUDA 训练链路 |
| post-training / arithmetic | IPO free-generation 路径完成；accuracy `0`，仅证明训练/生成/评分链路可执行 |
| real VLM checkpoint / ScienceQA | SmolVLM2-256M 共 5 trial 全部完成；详见[多模态统一评测](multimodal-models/benchmark.md) |
| real causal LM / reasoning budget | 固定 SmolLM2-135M revision 的 baseline 与 2-sample 候选均完成；候选生成 152 tokens，accuracy `0`，验证预算/延迟/成本约束和报告链路 |
| real causal LM / GSM8K SFT | BF16 单步参数更新完成；从 `checkpoint-1` 恢复后只执行 step 2，`resumed_from_step=1` |
| real causal LM / UltraFeedback | 固定公开 train/test preference 子集分别完成 DPO 与 ORPO 单步更新；held-out accuracy 均为 `0`，只作为工程 smoke |
| micro-LLM / scaling-law | 四个模型规模/数据/step 预算点均在 CUDA 完成；loss `6.8678→6.5692`，log-RMSE `0.002153`，仅为 FM-002 工程 smoke |

后三项于 2026-08-20 补测，结构化记录见
[`a30-reasoning-posttraining-smoke-20260820.json`](experiments/a30-reasoning-posttraining-smoke-20260820.json)。
checkpoint 与公开数据子集不提交到 Git；JSON 只保留复现所需的版本、命令口径和指标。
FM-002 的 Mac/A30 双路径结果保存在
[`fm002-scaling-law-mac-seed42.json`](experiments/fm002-scaling-law-mac-seed42.json)。

## 复现审计

单卡建议分片串行执行，避免多个大模型 adapter 同时占显存：

```bash
for shard in 0 1 2; do
  PYTHONPATH=src python scripts/audit_gpu_paths.py \
    --dataset-dir data \
    --output "runs/gpu-audit/a30-shard-${shard}.json" \
    --timeout-seconds 600 \
    --only-explicit-device-packages \
    --include-concept-demos \
    --shards 3 --shard-index "${shard}"
done
```

LLM adapter 应先准备 README 指定的 checkpoint，并在无外网开发机设置
`HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`。需要缩步数时只使用各 adapter 已公开的
`AUTO_RESEARCH_*` smoke 环境变量；正式论文复现不要沿用这些覆盖。
