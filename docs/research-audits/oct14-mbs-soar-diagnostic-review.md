# Oct14 MBS / SOAR 失败诊断边界

本审计只读核对既有原始运行；随后仅增强本地诊断记录和消除 SOAR 提示中的
斜杠占位歧义，未运行 CUDA、未新增下载、未更改奖励、解析器、门槛或采样预算。
CPU fixture 不是模型能力证据。以下旧失败保持原样，不追加不存在的响应或拒绝原因。

## 已执行的 MBS bounded seed42

- 执行源码：`0f5dca9f7f0319c6e3bb57aa578cfe26499a6e7e`；52 个 launch
  source SHA 均与该 Git 版本匹配。16 个训练候选、group4、cap1024、最多4 hard roots、
  depth1、decomposition/synthesis retries 各2、teacher attempts2，未改变预算。
- 原始失败：`.cache/oct14-post-training/mbs-bounded-raw-attempt02/evidence/failure.json`，
  SHA256 `adcca5400a7e38042407eba85ffac4a8d44ada3493fce8c06ca3b09c94d69df0`。
  exit1；348.2407392859459 秒；36129 个实际生成 token（含1541个既有 validation
  baseline token）。这里“train-only”限定候选构造与校准，不表示整个原调用未评估 validation。
- hard roots 为训练索引4、7、8，均实际四次成功率0且四次非截断。
  hard-root 门槛通过不等于教师独立验证通过，更不等于后续 Goldilocks 通过。
- construction audit 顺序为 root4 hardness、root7 hardness/verify失败、
  root8 hardness/verify失败；root4 在 decomposition 中没有产生可用树。
  全局成本仅有一次 student/teacher effectivity baseline 各一组和两次
  construction-teacher 调用。结合无 scaffold/effectivity audit，可把 root4
  限定在未形成至少两个验证成功的子题，但没有原响应，不能分辨 JSON、字段、截断或独立解题失败。
  这是根据执行源码控制流与成本的推断，不是旧运行保存的逐拒绝 trace。
  没有 target-policy-Goldilocks audit；不能称“三个根均 Goldilocks 失败”。
- `paired_rl_root_indices=[]`，未进入方法或对照 RLVR 更新。旧失败不是 passed receipt。

MBS 原 source 的 gold 作用域：`CheckpointConstruction.verify` 只把题目送给独立解题
教师，答案在外部 scorer；effectivity 只允许独立子题 worked examples，不能把 parent
答案或完整 parent plan 送入待测策略；`teacher_json` 的 decomposition、synthesis、
scaffold、blueprint construction context 可以看到训练 parent/candidate 的答案与 trace。
训练构造教师有 gold，不得宣传所有教师或所有生成调用均不见 gold。

## 已执行的 SOAR 7B 格式 probe

- 执行源码：`57b2314db1d5b8a8ebeb0aa7fbb6b7fee523df55`；54 个记录 source SHA
  均与该 Git 版本匹配。固定 Qwen/Qwen2.5-7B-Instruct revision
  `bb46c15ee4bb56c5b63245ef50fd7637234d6f75`，Elliotes/EcoAgent revision
  `bc5db40a20b254c5249401d2220ea71b06c86a5c` 的独立 catalog 训练 QA 前4题，各2次。
- 原始结果：`.cache/oct14-post-training/soar-format-raw-attempt02/evidence/diagnosis.json`，
  SHA256 `22d58ccfac06e99547d9f50391f8920b5eb7539cb37355670ec6a614bc0b6d9b`。
  probe exit0 只表示诊断执行完成；`no-format-signal`，whole-method GPU validation=false。
  外层34.612656300887465秒；probe内部32.17066810838878秒；实际433生成 token。
- 八次首 turn 全部 `invalid`、`truncated=false`，token 数为
  51、48、23、107、50、49、51、54；search=0、format=0、source-match=0。
  没有 LoRA/optimizer 更新，没有 assessment，没有 validation/test 内容读取。
- 旧 SYSTEM 要求 think 后选择 search 或 source+answer；其 source 占位文字为
  `<information_source>internal/external</information_source>`，但 parser 只接受
  精确 `internal` 或 `external`。CPU 反例中原样复制斜杠占位会被拒绝，两个独立模板则均合法。
  这是静态提示歧义，不是八次实际失败的已证实原因。
- 旧 probe 仅存 response text SHA、长度及截断标志，不存 text/token IDs；runtime
  也未打印逐响应。不能原文引用、反解 hash，或断言模型实际复制了斜杠、漏 tag、大小写错误。

## 本地诊断增强，不回填历史证据

SOAR SYSTEM 明确列出两个合法 final-answer 模板，原 think/search/source/answer
语义不变；解析器、奖励和预算未变。格式 probe 保存本次真实 policy response text、
原始 token IDs、SHA 和截断标志；episode 开始即登记未完成 audit，中途异常时保留已经
返回的 turn，不伪造最终 answer、reward 或 completed 状态。只在固定训练前缀执行，
不把训练 gold 或工具答案作为新提示示例。

MBS backend 保存实际 calibration、effectivity、construction-teacher、question-only
verification 响应及其 role/input-gold-scope、原 token IDs、SHA、截断和外部验证结果。
构造各 continue 分支记录明确 reject reason，不新增任何采样；正常失败及中断 payload
保留实际已有 trace。这些本地响应可能含训练构造答案，不应复制进脱敏 GPU receipt。

上述初始检查点的新 source 当时尚未执行 GPU。后续必须另行冻结源码、使用独立不可覆盖运行目录，在原预算内
执行明确授权的 probe；旧失败不能重新绑定新源码，不能据 CPU fixture 宣称门禁通过。

## 10月14日 b908 新响应诊断

两项实际执行均绑定 `b90862754bf51b1beeb5add3f7dc2a51ca00ace4`，54个源文件SHA与Git一致；
响应文本SHA及原token长度另经CPU独立核对。没有回填旧运行响应。

- MBS原限定预算运行 exit1，实际exit记录343.03794秒；failure SHA
  `a86f6e78c3a9c2c4abd1dbcfcf9c520db64d9bfd7d339c5d367ae20001916a0a`。
  root4的独立解题通过；两次分解各仅一个子题通过验证。第二子题缺失必要数量/关系，
  独立解题产生104、2p或2，均不等于提案答案。root7/8的教师解题也实际算错。
  八条拒绝均非截断且数值不等，没有发现纯数值书写等价被拒绝的证据。
  仍无合格合成后代和RL更新，不签通过回执。
- SOAR原train-only格式探针 exit0，实际35.97100秒；diagnosis SHA
  `29f7478df63701917e2f5370ca502712c7f320a17d7abd8b29250217025a8b1f`。
  3条有效轨迹、2条source-match、3次实际检索；某同题两次source奖励不同，
  去source奖励则相同。全部答案准确率为0、optimizer更新为0；这是格式信号，
  不是整方法验收或能力提升。完整原训练/消融另行执行。

MBS论文§3.3和附录E要求子题自包含、正确worked solution和简洁最终答案。
现有提示已有self-contained词面要求；新修仅操作化该说明：question包含所有必需数量、
单位、时间区间、关系和假设，不依赖父题、兄弟题或answer/trace字段；trace给完整解法，
answer给单一数值。不是复原未公开的作者生产wrapper，也不保证教师算术错误因此消失。
独立验证仍只读question，不补父题上下文，不改JSON schema、验证器、重试数或预算，
不注入本次训练题数字、答案或示例。新提示须冻结并真实GPU重测；旧b908失败不重绑。

## 5c自包含说明的实际重测

源码`5c863ab8`的同预算重测实际exit1、322.58302秒，failure SHA
`6597edd5e23e3c776d20bba3fdb631205e32a61e5f978ab47ee7fa3c69eee0b6`。
仍选到相同3个hard根，空paired根和0次RL更新。root4两次构造输出均不是完整合法的
JSON对象数组：有字符串内未转义换行、另一次混乱的字符串数组；原解析只能取到局部对象，
不能作为两子题数组接受。其余两根的独立验证仍失败。没有自动修补输出或接受残缺对象。

后续只在同一通用child说明中明确JSON转义与对象数组类型，解析器、schema、模型采样、
重试数和预算仍不变；新增CPU反例保证非法数组不会被修补为合格子题。
这也是接口说明，不是提高数学正确率或保证合成成功。必须另冻结源码和独立运行，
不能用这项提示修复把5c原失败重新标为通过。
