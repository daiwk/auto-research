# MR-B：注册、命令、发现与论文规格重构

本轮承接 MR-A，不新增论文，不改变论文算法或既有证据等级。保留命令名称、参数、
adapter key 和所有论文页面地址；原工作区未提交内容不参与这次迁移。

## 范围与验收

| 原问题 | 本轮实现 | 验收 |
|---|---|---|
| registry 会加载全部模型 | 元数据读取 packaged paper spec，只有 run/render 才解析选中实现；Agent 按方法加载 | 无 PyTorch 的列表、manifest、完整 parser；仅选中 adapter 被导入 |
| CLI 单文件耦合且最小安装不可用 | 逐命令 parser/handler；公共包惰性导出；缺少可选依赖给出安装提示 | base-only wheel 安装和独立 CI job；原命令合同回归 |
| 网络成功被误作覆盖完成 | 每页持久化、查询/窗口/预算身份、失败后保留已取结果、继续其他查询 | 中断恢复、配置漂移拒绝、缓存与封顶不得完成 |
| spec 只是生成副本 | paper.yaml v2 驱动 runtime；按 domain/key 保存目录事实；manifest 为纯生成产物 | 371 个运行合同、736 条目录记录与迁移前语义一致；不依赖本地 docs 推断 |
| 日期批次成为长期实现边界 | 将相互依赖的函数/类迁往稳定 mechanisms 模块；旧日期模块保留兼容导出 | 旧 import、方法行为与已有测试保持兼容 |

## 元数据的唯一修改入口

复现 adapter 的 `paper.yaml` v2 是元数据和评测合同来源，`adapter.py` 只绑定
`run`、`render`，不会再执行 mini-suite 来猜测默认指标，也不从 README/metrics 推断设备或预算。
运行声明在 `execution` 下；与顶层共享的标题、论文身份、主题、fidelity、数据集、指标等不重复保存。
部分历史条目的展示日期/机构比早期运行声明完整，迁移保留这两个语义，避免无证据地改写历史运行合同。
`mechanisms` 为历史描述，不能自动推断实现保真度，真正边界仍由 fidelity 和 omitted_core_components 给出。

目录事实保存于 `src/auto_research/paper_specs/catalog/<domain>/<key>.json`。
复现条目只引用 spec key，运行字段由 paper.yaml 派生；其余领域的已复核论文事实保存在对应记录。
`docs/research-manifest.json` 及 Markdown 目录是产物，删除产物后也能从规格重建；
生成器不再把上一版产物作为隐藏输入。旧 `latest_*_catalog.py` 仅为兼容视图，
历史字段差异明确标作 compatibility override，不供新生成器读取。

新增论文时仍须补算法、评测与论文文档，不能只新增一个 spec 就声称已实现。
`manage_paper_specs.py check/validate` 与目录生成门禁会核对规格、路径、重复主键和合同。

## 扫描的三种状态

1. **传输状态**：请求成功、失败或缓存回退。
2. **查询覆盖**：每个配置内查询是否真正取尽；达到 maximum-results 上限是 capped，即使每页 HTTP 都成功。
3. **全文审查**：是否核验身份、正文实验与线上证据。下载成功不自动推进人工审查水位。

默认仍保留宽查询和本地日期/identifier-month 双通道过滤，不为缩短时间擅自用发表日期
过滤掉晚索引记录。宽查询达到上限会明确留下缺口；需要提高预算或补充官方来源，不能宣布全网无遗漏。
查询覆盖只针对本次查询矩阵，不等于所有来源，更不等于所有合格论文已实现。

```bash
python scripts/discover_papers.py --track agent \
  --start-date 2026-10-01 --end-date 2026-10-07 \
  --checkpoint-dir .cache/discovery/agent-oct07 \
  --output runs/agent-candidates.json
# 中断后：完全相同窗口、查询矩阵与预算，追加 --resume
```

每一页成功后原子保存游标和候选；某个查询失败不丢掉此前页面，也不阻塞其他查询。
缓存页只提供待审线索，不推进已验证游标。恢复会校验完整扫描身份。
不带 `--resume` 表示新扫描，使用新的 scan id，避免复用同窗口的旧页面。
GitHub Actions 上传进度文件供排查；没有自动把历史进度当成下一天的新扫描结果。

## 安装与迁移边界

`pip install .` 只需要基础依赖即可查看帮助、目录、协议和生成 manifest。
训练命令仍按文档安装对应 extra；惰性加载不会让缺失依赖的训练伪装成功。
wheel 中包含 spec 和目录资源，不要求用户 clone 后保留 docs 目录。

本轮源码版本变化会触发 MR-A 的实验身份校验：旧运行可读，但不跨版本复用旧分数。
移动模块不改变论文的计算公式；GPU 路径仍需在实际 NVIDIA 设备上通过执行回归后交付。

## 本轮验收记录（2026-10-07）

- 全套测试 1251 项通过；入口声明表再次抽离后，Agent 与 MR-B 定向测试 124 项通过。
- 371 个 adapter 运行合同、736 条公开目录记录在迁移前后语义一致；目录、看板生成无漂移。
- 对迁移定义逐一比较语法树：364 个算法定义保持不变，8 个 adapter 工厂仅改为规格绑定。
- 实际构建 wheel，隔离环境仅安装项目和 NumPy，不安装 PyTorch/Transformers；完整命令解析、
  目录、manifest 和初始化命令通过。CI 新增独立的最小安装任务。
- NVIDIA A100 上使用公开 MovieLens-100k，执行 DIN/均值池化训练（42/43/44 三个 seed，
  每个 seed 3 步）、惰性 adapter 独立进程、`reproduce` 命令，以及 RPTune/CARM 的 CUDA 前后向。
  13 次设备解析均为 CUDA；[脱敏回执](../gpu-validations/architecture-mrb-a100-20261007.json)
  固定了源码提交与数据指纹。短训练只验证运行链路，不作为论文级效果比较。
- Ruff、规格检查、指标 schema 审计、平台完整性审计、GPU 证据检查和严格文档构建通过。

迁移后的旧日期模块只提供兼容导出；新论文应直接进入稳定的算法模块和领域规格记录，
不要继续把新算法追加到旧批次文件。上述测试是本轮回归范围，不声称替代所有论文的完整规模复现。
