# 本批后训练算法：真实 checkpoint 运行说明

这组实现不是把预设答案直接返回：学生先采样，教师计算真实 token 概率，目标函数更新实际 LoRA 参数。DIAL、Meta、Semi-OPD 用不同的蒸馏更新方式；GRPODropout 使用外部数值验证奖励；RA / Co-RA 结合教师分布残差与验证奖励。Co-RA 还更新教师 LoRA，下轮才使用更新后的指导。

## 准备环境与数据

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[post-training-gpu]'
```

准备已下载的公开因果 LM checkpoint，两者的 token 词表必须完全一致，且包含 `q_proj` / `v_proj`。本批 A100 验证使用 Qwen3-4B-Instruct-2507 与公开 Qwen3-4B-Inst-MOPD；也可传其他符合合同的模型，结果必须保留实际模型 ID / revision。

公开 GSM8K 数据每行是 `{"question": "...", "answer": "... #### 42"}`。训练与验证的问题不得重叠；验证答案只进入评分器，采样器看不到。少量验证只说明运行通过，不能作为收益证据。模型和数据 revision 必须对应你实际下载的版本，不能直接照抄示例替另一份文件背书。

## 单算法运行

下面使用本批验证的固定公开 revision；把路径改成你本机下载位置：

```bash
PYTHONPATH=src python scripts/run_oct10_post_training.py \
  --objective dial-opd \
  --student-path checkpoints/qwen3-4b \
  --student-id Qwen/Qwen3-4B-Instruct-2507 \
  --student-revision cdbee75f17c01a7cc42f958dc650907174af0554 \
  --teacher-path checkpoints/qwen3-4b-mopd \
  --teacher-id Siye01/Qwen3-4B-Inst-MOPD \
  --teacher-revision b61a9f00b77302b6e947af1215b7cb994b884c4a \
  --train-path data/gsm8k/train.jsonl \
  --validation-path data/gsm8k/validation.jsonl \
  --dataset-revision 3101c7d5072418e28b9008a6636bde82a006892c \
  --output-dir runs/dial-opd --device cuda \
  --seed 42 --steps 2 --group 2 --max-tokens 128
```

替换 `--objective` 为 `meta-opd`、`semi-opd`、`grpo-dropout`、`residual-advantage`、`co-ra`。另有 `opd` 对照。GRPO / Co-RA 要给模型足够的生成长度，并检查组内真实奖励方差；全部成功或全部失败可能没有序列奖励梯度，这不是通过改假奖励解决的问题。

## 顺序批跑与查看结果

`scripts/validate_oct10_post_training.sh` 可顺序跑六个目标，要求通过环境变量显式提供 `STUDENT_PATH`、`TEACHER_PATH`、两者 ID / revision、`TRAIN_PATH`、`VALIDATION_PATH` 与 `DATASET_REVISION`。默认是短预算验证，不是论文完整实验。

每个输出目录含 `report.json` 和本地 `adapter.pt`。重点检查 loss、真实奖励方差、有效梯度步数、学生 / 教师参数变化、筛选后的响应数，以及最终隔离验证。权重不自动推送到 GitHub；没有自动调用在线模型或上传训练数据。

当前不接入统一 evolve 控制器；这些目标有独立可执行训练入口，不能仅凭登记的论文名称宣称已经进入多轮自进化。
