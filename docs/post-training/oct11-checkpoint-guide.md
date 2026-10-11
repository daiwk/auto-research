# 10 月 11 日 checkpoint 诊断运行说明

这些入口执行真实模型，不自动把短运行升级为论文复现收益。建议在 Linux NVIDIA GPU 上运行；已验证设备为 A100。路径由用户提供，不包含开发机器身份或 SSH 配置。

```bash
python -m pip install -e '.[post-training-gpu]'
python scripts/split_public_training_jsonl.py --help
python scripts/run_vfold_checkpoint.py --help
python scripts/run_recal_checkpoint.py --help
python scripts/run_zcpo_checkpoint.py --help
python scripts/run_opd_learning_signals.py --help
python scripts/prepare_pivot_banking77.py --help
python scripts/run_pivot_checkpoint.py --help
python scripts/run_sguid_checkpoint.py --help
python scripts/run_memento3_checkpoint.py --help
python scripts/run_vcola_checkpoint.py --help
python scripts/run_data_space_iteration.py --help
```

## 公共模型和数据

基础模型为 `Qwen/Qwen3-4B-Instruct-2507`，revision `cdbee75f17c01a7cc42f958dc650907174af0554`；OPD 另需同词表教师 `Siye01/Qwen3-4B-Inst-MOPD`，revision `b61a9f00b77302b6e947af1215b7cb994b884c4a`。下载到本地目录后传 `--checkpoint-path`，或 OPD 的 `--student-path/--teacher-path`，同时传 ID 和 revision。运行器不会下载或上传私有数据。

GSM8K 来源为 `openai/grade-school-math`，revision `3101c7d5072418e28b9008a6636bde82a006892c`。仅将官方 **train** JSONL 传给切分脚本：按归一化问题的 SHA-256 做确定性 90%/10% holdout，保存 train/validation/split.json。官方 test 不放进 validation 路径。运行器用 `--split-manifest` 核验源 split、revision、分区哈希、计数及问题不重叠；缺失 manifest 的旧入口不声称 test 隔离。

## 一个可改路径的完整例子

```bash
python scripts/run_zcpo_checkpoint.py \
  --checkpoint-path checkpoints/qwen3-4b \
  --checkpoint-id Qwen/Qwen3-4B-Instruct-2507 \
  --checkpoint-revision cdbee75f17c01a7cc42f958dc650907174af0554 \
  --dataset-revision 3101c7d5072418e28b9008a6636bde82a006892c \
  --train-path data/gsm8k-holdout/train.jsonl \
  --validation-path data/gsm8k-holdout/validation.jsonl \
  --split-manifest data/gsm8k-holdout/split.json \
  --steps 24 --group 4 --max-tokens 256 --validation-examples 8 \
  --seed 42 --device cuda --output runs/zcpo-42.json
```

其他论文的可执行完整 argv 在各自 GPU 回执的 `command` 中；`checkpoints/*` 是需要替换的本地公开 checkpoint 目录。回执不包含权重，只保存可审查命令、revision、执行提交和源码哈希。

## 能说明什么

PIVOT 使用单独的 Banking77 官方 train-only 385/77 分区与 Qwen2.5-0.5B / 7B，不能把 GSM8K 路径直接代入领域实验。其 GPU 回执包含可改路径的完整三配方命令和固定模型版本；8 题短跑三配方准确率均为 0%，保留为真实机制诊断。

## 其他领域的入口

- [SGUID](2610.12367-sguid/README.md)：真实支持 thinking 切换的 Qwen3.5-9B 文本分支；GSM8K 训练集派生 holdout。A100 第一轮完成、第二轮持久性筛选失败并精确恢复；没有通过回执，整体两轮尚未验收。实际渲染前缀必须通过检查，不能以模型接受参数代替协议核验。
- [Memento3](../agent-research/2610.11794-memento3/README.md)：公开 7B 生成世界模型，通过有界 AST 解释器与真实 FrozenLake 交互。该运行模型被证伪且任务失败，不代表 ARC/Pong 复现成功。
- [V-CoLA](../multimodal-models/2610.11251-vcola/README.md)：真实 9B 多模态 checkpoint 与 CIFAR-10 train-only 图像；实际状态贡献、视觉合并和退出，受限首字母诊断不等于完整生成准确率。
- [Data-Space Iteration](../foundation-models/2610.12102-data-space-iteration/README.md)：公开 CIFAR-10 训练图像上从零训练小 UNet teacher，再分别运行两种 DMD 配方；三种子结果混合，像素池化距离不是论文 FID。

图像入口只需要官方五份 CIFAR-10 `data_batch_*` 训练文件，逐份核验 MD5；不要传入官方 test 来代替 validation。各方法使用自己的预算和评价合同，不能把不同领域的短诊断指标直接横向排名。

各入口的附加依赖分开安装，不把 micro-LLM 的 `llm-evolution` 扩展误认为 checkpoint 环境：

```bash
# 真实稀疏 CUDA kernel（Linux NVIDIA）
python -m pip install -e '.[sparse-decoding-gpu]'
# V-CoLA 的图像 processor / Qwen3.5 多模态运行环境
python -m pip install -e '.[multimodal]'
# 从零训练图像 teacher / DMD，并计算 SciPy Fréchet 诊断
python -m pip install -e '.[data-space-gpu]'
# Memento3 固定环境版本；模型依赖由 post-training-gpu 提供
python -m pip install -e '.[post-training-gpu]' 'gymnasium==1.1.1'
# Option-Channel 使用 Laya 公开 checkpoint
python -m pip install -e '.[system-one-gpu]'
```

这些结果验证真实 forward/backward、参数或缓存改变及数据隔离。单 seed、几道验证题不能支撑稳定提升；LoRA 位移不是全参数位移，持久缓存占用不是端到端峰值或延迟。Evolve 只有在控制器能调用并评估算子后才登记为已集成；本批除 ZIP/ZE 优化器外，没有据论文名称自动晋级。
