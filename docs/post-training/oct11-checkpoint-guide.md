# 10 月 11 日 checkpoint 诊断运行说明

这些入口执行真实模型，不自动把短运行升级为论文复现收益。建议在 Linux NVIDIA GPU 上运行；已验证设备为 A100。路径由用户提供，不包含开发机器身份或 SSH 配置。

```bash
python -m pip install -e '.[llm-evolution]'
python scripts/split_public_training_jsonl.py --help
python scripts/run_vfold_checkpoint.py --help
python scripts/run_recal_checkpoint.py --help
python scripts/run_zcpo_checkpoint.py --help
python scripts/run_opd_learning_signals.py --help
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

这些结果验证真实 forward/backward、参数或缓存改变及数据隔离。单 seed、几道验证题不能支撑稳定提升；LoRA 位移不是全参数位移，持久缓存占用不是端到端峰值或延迟。Evolve 只有在控制器能调用并评估算子后才登记为已集成；本批除 ZIP/ZE 优化器外，没有据论文名称自动晋级。
