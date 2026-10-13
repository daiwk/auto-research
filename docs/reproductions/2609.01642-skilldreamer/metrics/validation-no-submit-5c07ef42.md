# 五行格式澄清后的 native validation：核心执行但零提交

2026-10-14，真实 NVIDIA A100 上执行唯一 seed42 探针，算法源固定 `701f45007be75cf6153f98812ef94e087c94a8f0`、独立runner固定 `5c07ef42bbb008e7adc3fc03fd5e85695c2bcc86`。复用原 Qwen2.5-7B-Instruct revision `bb46c15ee4bb56c5b63245ef50fd7637234d6f75`、MiniLM revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` 和原8个validation IDs，只有question，无gold/scorer，未使用16个evaluation ID。预算仍是600秒双硬限、240calls、每次256tokens、action8、top-k3；没有重试或扩预算。

实际退出码0，launcher用时401.4411秒（runner400.5552秒），159calls、19369tokens。PSG/HSR各7题，65次真实CSI、7个episode实际加载gallery，9次load后fresh-action重询。共56次**环境step调用**，不是56次成功工具：54次calculator尝试中48次成功返回、6次错误，另2次未知工具错误。**finish为0、提交为0**，不签passed receipt、不宣称能力提升或任务成功，不做外部正确率评分。

完整来源、预算及raw SHA见 [native diagnostic artifact](public-a100-validation-no-submit-5c07ef42.json)。[原final](raw/validation-no-submit-5c07ef42/seed42.json)、[原partial](raw/validation-no-submit-5c07ef42/seed42.partial.json)、[159次调用trace](raw/validation-no-submit-5c07ef42/seed42.trace.jsonl) 与 [CPU逐条回放/分类](raw/validation-no-submit-5c07ef42/submission-analysis.json) 逐字保存；[脱敏exit](raw/validation-no-submit-5c07ef42/exit.sanitized.json) 绑定原exit SHA。未将原0f/d860负结果或0.5B三seed失败混入新source。

| validation ID | calls / tokens | CSI | 实际加载技能 | env.step | calculator成功 / 错误 | 未知工具 | 已成功算式重复次数 | finish |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: | ---: |
| 13 | 1 / 208 | 0 | 无（PSG失败保留） | 0 | 0 / 0 | 0 | 0 | 0 |
| 1 | 28 / 3198 | 9 | scheduling | 8 | 1 / 6 | 1 | 0 | 0 |
| 4 | 17 / 2321 | 9 | rates | 8 | 7 / 0 | 1 | 4 | 0 |
| 6 | 27 / 2932 | 9 | arithmetic | 8 | 8 / 0 | 0 | 3 | 0 |
| 23 | 19 / 2481 | 10 | money、arithmetic | 8 | 8 / 0 | 0 | 7 | 0 |
| 21 | 16 / 2167 | 9 | rates | 8 | 8 / 0 | 0 | 6 | 0 |
| 14 | 25 / 3257 | 10 | money、arithmetic | 8 | 8 / 0 | 0 | 4 | 0 |
| 15 | 26 / 2805 | 9 | rates | 8 | 8 / 0 | 0 | 4 | 0 |

117次runtime调用按实际入口分为9load、56env.step和52schema失败；7个执行题均耗尽action8而未提交。重复计数28是“与此前已成功表达式AST一致，并且先前结果已在当前观察历史中”的可复查下界，不是使用gold判断答案正确。

## 零finish的两类证据

**策略停滞/非合规选择**：例如ID21/call100已计算 `5 * 2 * 5` 并得到 `Calculator result: 50`；call101的实际prompt明确包含该结果，却仍把SUBGOAL设为同一距离计算、NEXT与JSON再调用同一算式。后续继续重复。65次有效CSI的NEXT均未提finish/submit。因此不能把模型自称的“未解决子目标”直接当成真实缺少计算结果；反馈并未被API丢弃。其他题也有已得到结果后反复算同一表达式，或先计算总量又退回局部子步骤。无scorer，不能据此声称整题答案正确。

另两次实际请求为ID1/call20的 `assess_capability` 和ID4/call38的 `load_skill`，环境按原协议返回 `Invalid action schema`，未自动纠正；6次calculator错误包括自然语言方程/程序语句或不支持的运算符。它们是实际policy请求/工具错误，不是隐式工具执行成功。

**接口说明不对称**：执行源 `algorithm.py` 的 `execute_agent` 给baseline拼入generic `SYSTEM_PROMPT`，明确calculator用于计算、finish用于提交且仅支持算术表达式。Skill的 `capability_context` 当时只给calculator/finish JSON示例，没有同等完整工具语义文字，也没有明确CSI五行及skill_id加载不是额外工具。这是源码与实际prompt可核对的公平API说明差异；**没有隔离出其对零finish的因果效应**。28次重复成功计算与API说明缺口应分开陈述，不能只归因为提示或只归因为模型能力。

## 独立CPU回放与后续边界

公开artifact附带逐字、固定SHA的 [701f算法源码](raw/validation-no-submit-5c07ef42/frozen-source/skill_probe_701f/skilldreamer/algorithm.py) 和 [实际环境源码](raw/validation-no-submit-5c07ef42/frozen-source/skill_probe_701f/state_opd/environment.py)。`tests/test_skilldreamer_native_no_submit.py` 在独立namespace导入这些旧source，回放7个episode的原response，逐次核对完整prompt及全部返回字段，不依赖之后改动的当前prompt，也不生成新模型响应或运行CUDA。

后续只补清公平API文字：仅calculator/finish；calculator返回值但不提交；模型显式finish才提交并终止；能力评估是五行而不是工具；skill_id由executor加载并显示真实gallery后再询问，不存在load_skill/assess_capability工具。不提供题目数字、gold或当前ID的答案/技能判断，不强制finish，不根据28次重复自动调整策略。parser、gallery、execute_agent和action_budget不变。**这次追加API文字尚未GPU执行，不能重绑本记录或宣称因果/能力改善。**
