# 视频与音频公开 checkpoint 评测

本页对应 roadmap 的 MM-001 与 MM-002。两条链路都直接加载公开 checkpoint、消费公开
benchmark 原始媒体，并把逐样本预测与聚合指标分离；checkpoint、视频、音频和预测全集不提交
到 Git。

## MM-001：Video-MME-v2 × SmolVLM2

- checkpoint：`HuggingFaceTB/SmolVLM2-256M-Video-Instruct`，固定 commit
  `067788b187b95ebe7b2e040b3e4299e342e5b8fd`；
- benchmark：`MME-Benchmarks/Video-MME-v2`，固定数据 revision
  `6e4bebb03202e1ddbf3d37703e560e51c5aa2d64`；
- 输入：官方 Parquet/JSONL 与本地 MP4；
- 输出：每个 seed 独立的可续跑 JSONL、accuracy、parse rate、sample std 和 95% CI。

```bash
python scripts/prepare-media-benchmarks.py video-mme-v2 \
  --output data/video-mme-v2-smoke --videos 1

auto-research multimodal-video-eval \
  --annotations data/video-mme-v2-smoke/test-subset.jsonl \
  --video-root data/video-mme-v2-smoke/videos \
  --model-revision 067788b187b95ebe7b2e040b3e4299e342e5b8fd \
  --checkpoint-path checkpoints/smolvlm2-video \
  --seeds 42,43,44 --maximum-examples 4 --num-frames 32 \
  --output-dir runs/video-mme-v2-smoke --device cuda --offline
```

准备脚本默认从固定 Hugging Face revision 下载官方分卷并只提取所需 MP4；首卷约 2GB，
比重新抓取可能下线或要求登录的 YouTube 源更可重复。磁盘或带宽受限时可以显式加
`--source youtube`，但脚本会在公开视频不可访问时失败，不能静默拿其他视频替代。

默认确定性解码用于 checkpoint 回归，因此三个 seed 可能产生相同预测和零方差。若研究生成
随机性，可加 `--sample --temperature 0.2`；不能把确定性重复运行描述为训练稳定性证据。
使用 `--maximum-examples` 时报告会明确标记为公开 benchmark 子集 smoke，不冒充完整榜单。

真实 A30 回归覆盖官方视频 `001` 的完整四题组、保留源 fps/时间戳的 32 个均匀采样帧和
3 个确定性 seed，
parse rate 为 `1.000`，但 256M checkpoint 四题均未答对，accuracy 为 `0.000`。这说明
媒体解码、真实 checkpoint、逐题续跑和指标链路已打通，同时也说明该小模型不能作为
Video-MME-v2 能力基线；完整记录见
[Video-MME-v2 × SmolVLM2 归档](metrics/video-mme-v2-smolvlm2-a30-4x3.json)。

## MM-002：ESC-50/ESC-10 × CLAP

- checkpoint：`laion/clap-htsat-unfused`，固定 commit
  `8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a`；
- benchmark：官方 ESC-50；快速验证使用其中许可更宽松的 ESC-10 子集；
- 输入：官方 WAV 和 metadata CSV；
- 输出：zero-shot top-1/top-5、逐样本预测、模型/数据 fingerprint 和文本 embedding 缓存。

```bash
python scripts/prepare-media-benchmarks.py esc10 \
  --output data/esc10 --examples-per-class 3

auto-research multimodal-audio-eval \
  --annotations data/esc10/esc10-subset.csv \
  --audio-root data/esc10/audio \
  --model-revision 8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a \
  --checkpoint-path checkpoints/clap \
  --maximum-examples 30 --output-dir runs/esc10-clap \
  --device cuda --offline
```

文本 embedding 缓存同时绑定 checkpoint commit、完整 label 集和 prompt template；任一变化
都会拒绝旧缓存。ESC-10 零样本子集结果不能写成完整五折、监督训练的 ESC-50 指标。

真实 A30 回归在固定的 30 条 ESC-10 子集上得到 zero-shot top-1/top-5 均为 `1.000`，并已
通过第二次运行验证逐样本续跑与 text embedding cache 命中。该小子集很容易，结果只用于
证明公开 WAV、真实 checkpoint、缓存和指标链路可执行；完整指标见
[ESC-10 × CLAP 归档](metrics/esc10-clap-a30-30.json)。

## 隔离开发机

联网 Mac 可先用 Hugging Face snapshot 下载固定 revision，再将 snapshot 目录同步到 Linux/GPU。
开发机命令显式传 `--checkpoint-path --offline`，因此不会因 `main` 漂移，也不会在无外网环境
静默切换模型。代码记录公共模型 ID 和 resolved revision，不记录机器专属路径或包构建串。
