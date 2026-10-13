# NEAR / Beyond：公开检索 GPU 验证恢复说明

状态日期：2026-10-13。**GPU 验证为 TODO，当前不继续网络、远端探测、依赖安装或 CUDA。** 以下命令仅供用户之后明确恢复工作时使用，本轮没有执行它们。

本说明只记录本地已有返回状态，不存主机名、用户名、SSH 别名、驱动或构建字符串；未知状态明确写未知。不新增 GPU receipt，不将准备工作写成 GPU 完成。

## 当前已知状态

| 项目 | 本轮实际状态 | 不能据此宣称 |
| --- | --- | --- |
| 加速器只读查询 | 曾读到 NVIDIA A30，24 GiB；没有启动检索或训练 CUDA 任务 | GPU 实验已完成或性能已验证 |
| 共享 Python | Python 3.11.10，Torch 导入可用；未修改共享 Python/Torch | 所有模型依赖已兼容 |
| MiniLM | 7 个指定公开文件的传输最终返回 exit 0；可称完整传输成功 | 远端逐文件 SHA256 核验通过；该核验尚未进行 |
| LongMemEval 完整 raw JSON | 传输返回 exit 255；远端可能无文件或留下部分临时文件，实际状态未知 | 原始数据完整到位 |
| LongMemEval raw-only provenance | 传输返回 exit 255；远端状态未知 | provenance 已完整到位 |
| 独立 overlay | 创建请求对应连接返回 exit 255，是否创建或部分创建未知 | overlay 初始化成功 |
| Transformers 等依赖安装 | **没有提交任何网络 pip install 命令** | 小依赖安装成功 |
| NEAR seed 42/43/44 | **均未启动**，没有结果 JSON | 成功、失败、负结果或三 seed 比较已获得 |
| Beyond seed 42/43/44 | **均未启动**，没有结果 JSON | adapter 训练、参数更新或三 seed 比较已完成 |

本轮自有传输/环境准备进程已结束：三项失败操作返回 exit 255，MiniLM 返回 exit 0。对该 MiniLM 传输及其子进程的停止请求返回进程已不存在；随后本机按确切自有命令筛选，没有发现存活进程。没有停止其他任务的连接。没有删除已传资源、部分文件或断点。

## 固定源码与完整性

源码快照目录：`/tmp/auto-research-oct13-ccad3e67`。

主代理通过 `git archive` 制作的提交：`ccad3e679787f6f5383b8bd3dd1c7b58e7c8c5d0`。执行前的只读检查已将以下 **10 个运行相关文件** 的远端 SHA256 与本地 `git show <commit>:<path>` 字节逐一核对，全部一致。这是文件核验，不冒充远端有 `.git` 或根 provenance 声明。

| 文件（相对快照根目录） | 已核对的 SHA256 |
| --- | --- |
| `scripts/run_oct13_memory.py` | `1b2750f16e3bb82d4960f1767c8505826df92d92088ecb5437762c093559e616` |
| `src/auto_research/reproductions/near/__init__.py` | `e7526576c299eded95c33b11c8c535d972ae4e44052d240d29f9e14f3eb18703` |
| `src/auto_research/reproductions/near/adapter.py` | `2c44b4430af86b7b570bb55b8d366b684ae517530aa589ebe8339f2b4db28b3d` |
| `src/auto_research/reproductions/near/algorithm.py` | `2058bdd67dd04dabe2482a60c234a61bcb90ad132a7e43cf40d85ef3fedd1906` |
| `src/auto_research/reproductions/near/data.py` | `795416bdffeb25880aeaf85b4bfd6480b8677b45cddabe37ba2e49d7bf544eb8` |
| `src/auto_research/reproductions/near/experiment.py` | `dff15dd41eb74a102265b473f92b8885bab033be91f1ad7b0a8a4d8579607ea7` |
| `src/auto_research/reproductions/beyond_final_embedding/__init__.py` | `b61e251f3e7f6fbb26021eb9ad3996c8f8ca233175dc19b86796b695ecc44a43` |
| `src/auto_research/reproductions/beyond_final_embedding/adapter.py` | `3b58025b770656c4a5c2b647854a43977ce67a335abf9fda2d278ef9cd79bce9` |
| `src/auto_research/reproductions/beyond_final_embedding/algorithm.py` | `25ddc0d5276ca7f16d416410942a71beef721491633e0103d9b8f88a4f671622` |
| `src/auto_research/reproductions/beyond_final_embedding/experiment.py` | `9defb1afee9b3acf3818fd9fd76b5f357e707da900ecd74da27b9c34e3193665` |

恢复时应重新核对这些文件。若需要算法或 runner 修复，先报告，由主代理提交新的源码快照，再重跑；不要在原快照上热补丁，也不要补造成功 JSON。

## 唯一允许同步的公开资源

### MiniLM

- 本地镜像：`.cache/oct12-public/checkpoints/minilm/`。
- Public ID：`sentence-transformers/all-MiniLM-L6-v2`。
- 固定 revision：`1110a243fdf4706b3f48f1d95db1a4f5529b4d41`。
- 目的目录：`/tmp/auto-research-oct13-ccad3e67/public/minilm/`。
- 仅同步下表 6 个文件与 `provenance.json`；不传 `.cache/huggingface/`、锁文件或其他本地文件。

| 文件 | bytes | 已验证的本地 SHA256 |
| --- | ---: | --- |
| `model.safetensors` | 90,868,376 | `53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db` |
| `config.json` | 612 | `953f9c0d463486b10a6871cc2fd59f223b2c70184f49815e7efbcab5d8908b41` |
| `tokenizer.json` | 466,247 | `be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037` |
| `tokenizer_config.json` | 350 | `acb92769e8195aabd29b7b2137a9e6d6e25c476a4f15aa4355c233426c61576b` |
| `special_tokens_map.json` | 112 | `303df45a03609e4ead04bc3dc1536d0ab19b5358db685b6f3da123d05ec200e3` |
| `vocab.txt` | 231,508 | `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3` |

### LongMemEval

- 本地原始文件：`.cache/oct12-public/longmemeval/longmemeval_s_cleaned.json`。
- Public ID：`xiaowu0162/longmemeval-cleaned`。
- 固定 revision：`98d7416c24c778c2fee6e6f3006e7a073259d48f`。
- bytes：`277383467`。
- SHA256：`d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442`。
- 目的文件：`/tmp/auto-research-oct13-ccad3e67/public/longmemeval/longmemeval_s_cleaned.json`。
- 配套 raw-only 来源记录：`.cache/oct13-a30-memory-transfer/longmemeval-provenance.json`，目的为该目录下 `provenance.json`。

已有 `.cache/oct12-public/longmemeval/provenance.json` 描述的是之前的两条转换样本，不应冒充完整原始数据的 provenance。新 raw-only 记录只含公开 ID、固定 revision、完整原始文件 hash 与“无转换”声明；没有改动旧记录，也没有传 `t2mem-first2.jsonl`。

### 恢复传输（当前不执行）

先在已授权远端会话中创建目标目录，保留任何已有部分文件。连接目标由恢复工作的人通过 `APPROVED_TARGET` 提供，不写入本说明。

```bash
mkdir -p /tmp/auto-research-oct13-ccad3e67/public/minilm
mkdir -p /tmp/auto-research-oct13-ccad3e67/public/longmemeval
```

在本地仓库中逐项串行同步；先检查 MiniLM 已有文件，完整且 hash 一致时不必重传。失败返回不表示完整文件可用。

```bash
: "${APPROVED_TARGET:?请提供已授权的连接目标}"
rsync --archive --compress --partial --progress --timeout=60 \
  .cache/oct12-public/checkpoints/minilm/config.json \
  .cache/oct12-public/checkpoints/minilm/model.safetensors \
  .cache/oct12-public/checkpoints/minilm/tokenizer.json \
  .cache/oct12-public/checkpoints/minilm/tokenizer_config.json \
  .cache/oct12-public/checkpoints/minilm/special_tokens_map.json \
  .cache/oct12-public/checkpoints/minilm/vocab.txt \
  .cache/oct12-public/checkpoints/minilm/provenance.json \
  "${APPROVED_TARGET}:/tmp/auto-research-oct13-ccad3e67/public/minilm/"
rsync --archive --compress --partial --progress --timeout=60 \
  .cache/oct12-public/longmemeval/longmemeval_s_cleaned.json \
  "${APPROVED_TARGET}:/tmp/auto-research-oct13-ccad3e67/public/longmemeval/"
rsync --archive --compress --partial --progress --timeout=60 \
  .cache/oct13-a30-memory-transfer/longmemeval-provenance.json \
  "${APPROVED_TARGET}:/tmp/auto-research-oct13-ccad3e67/public/longmemeval/provenance.json"
```

恢复后，在远端读取两份公开 provenance，对每个实际文件做流式 SHA256 比较，再检查模型 ID/revision 与上述固定值。任何缺文件或 hash 不一致都应停止，不使用较小临时样本补过。

## 隔离依赖方案（尚未安装）

只读模块探测已确认缺：`transformers`、`huggingface_hub`、`tokenizers`、`safetensors`、`tqdm`。

只读探测找到了 `numpy`、`regex`、`requests`、`packaging`、`filelock`、`yaml` 的模块 spec；未逐包执行导入或版本核验，实际版本与兼容性未知。`sklearn` 未找到模块 spec，但这两个实现只使用自身 NumPy 聚类/索引逻辑，不需要补装 sklearn。

主代理已核验 Transformers 4.57.3 的官方依赖合同，并建议此固定的小依赖集合；这不是本轮安装结果：

```text
transformers==4.57.3
huggingface-hub==0.36.0
tokenizers==0.22.2
safetensors==0.8.0
tqdm==4.69.0
```

不要直接搬本地 Transformers 5.14.1，也不要为适配它升级共享 Torch。

计划 overlay：`/tmp/oct13-memory-overlay-ccad3e67`。恢复时先只读检查该目录；如果已部分创建，保留它并选择另一个全新目录，不能清空或覆盖未知内容。以下例子只在目录不存在时创建：

```bash
OVERLAY=/tmp/oct13-memory-overlay-ccad3e67
if [ ! -e "$OVERLAY" ]; then
  /usr/bin/python -m venv --system-site-packages --symlinks "$OVERLAY"
fi
SITE=$("$OVERLAY/bin/python" -c "import sysconfig; print(sysconfig.get_path('purelib'))")
case "$SITE" in
  "$OVERLAY"/*) ;;
  *) exit 1 ;;
esac
"$OVERLAY/bin/python" -m pip --isolated --disable-pip-version-check install \
  --no-deps --ignore-installed --no-cache-dir --upgrade --target "$SITE" \
  transformers==4.57.3 huggingface-hub==0.36.0 tokenizers==0.22.2 \
  safetensors==0.8.0 tqdm==4.69.0
"$OVERLAY/bin/python" -m pip --isolated --disable-pip-version-check list --path "$SITE"
```

此路径不得自动解析/安装依赖，避免重装 Torch/Triton/NVIDIA 包或修改继承环境。安装前后应确认 Torch 的实际文件来源与 `/usr/bin/python` 相同；无需在准备阶段初始化 CUDA。若随后发现其他缺包或版本不兼容，先报告具体依赖，再只在 overlay 固定小版本安装。

## 固定评测协议

六项计划顺序：NEAR 42、43、44；Beyond 42、43、44。每项参数一致：100 queries、max length 128、batch size 16、adapter epochs 2、显式 `query-disjoint-shared-bank`。任何时候只运行一个 CUDA 进程；恢复前应再次确认 GPU 独占授权。

本地公开原始数据的加载/切分检查已经完成：60 train、20 validation、20 test，三个集合均为 answerable queries；候选 session ID 数分别为 2820、951、964，100 queries 共有 4572 个不同 memory 文本。这是 CPU 数据协议检查，不是模型检索结果。

- Query ID 以无标签固定 hash 切分；encoder 与无监督 memory bank 可共享。
- 可选 query adapter 的 relevance labels 只用于 train loss；validation 选择 epoch/alpha 或 NEAR 参数；test 仅最后评分。
- Gold answer 不暴露给模型。保留 `shared_unlabelled_memory=true`、`unseen_bank_generalization=false`、`diagnostic_only=true`、`promotion_eligible=false`。
- 这是缩放、非官方固定索引诊断，不能写为完整 LMEB、原论文 backbone/HNSW 或未见 bank 泛化；不能与严格 bank-disjoint 协议合并统计。
- 之前 30-query strict CPU 负结果保留，不由本轮 TODO 或未来 shared-bank 结果替代。

### 六项顺序运行命令（当前不执行）

资源/依赖/源码均通过核验、用户明确恢复 GPU 工作后，才在指定源码目录执行。使用新的结果目录，不覆盖任何既有结果；失败原始日志也必须保留。

```bash
SOURCE=/tmp/auto-research-oct13-ccad3e67
OVERLAY=/tmp/oct13-memory-overlay-ccad3e67
cd "$SOURCE"
export PYTHONPATH=src
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export CUDA_VISIBLE_DEVICES=0
RUN_ROOT=runs/memory-eval-resume
LOG_ROOT=logs/memory-eval-resume
mkdir -p "$RUN_ROOT" "$LOG_ROOT"
for paper in near beyond-final-embedding; do
  for seed in 42 43 44; do
    output="$RUN_ROOT/$paper-seed$seed.json"
    if [ -e "$output" ]; then
      printf '已有不可变结果，先核验再决定：%s\n' "$output"
      continue
    fi
    "$OVERLAY/bin/python" scripts/run_oct13_memory.py \
      --paper "$paper" \
      --raw-data public/longmemeval/longmemeval_s_cleaned.json \
      --model-dir public/minilm --device cuda --seed "$seed" \
      --max-queries 100 --max-length 128 --batch-size 16 --adapter-epochs 2 \
      --split-policy query-disjoint-shared-bank --output "$output" \
      >> "$LOG_ROOT/$paper-seed$seed.log" 2>&1
    status=$?
    printf '%s seed=%s exit=%s\n' "$paper" "$seed" "$status"
    if [ "$status" -ne 0 ]; then
      printf '保留失败日志；先诊断，不补造成功 JSON。\n'
      break 2
    fi
  done
done
```

恢复后的每个真实 JSON 应核对 seed/device、60/20/20 split、public revisions/hash、validation-selected 参数、test/baseline 与 comparison contract；Beyond 还需检查两 epoch 的真实 loss 与参数更新证据。结果不佳、无提升、选择 epoch 0 或失败均按实际记录。原始 JSON 取回本地专用目录，由主代理决定正式指标汇总与 sanitized GPU receipt；本说明本身不是 receipt。

## 本地保留与清理边界

保留 `.cache/oct13-a30-memory-transfer/longmemeval-provenance.json` 作为公开 raw-only 来源记录，保留所有远端未知/部分文件用于恢复。没有删除共享资源 cache，也没有下载或传输其他模型、数据、源码或本地文件。此说明之外不改全局索引、manifest 或生成内容。
