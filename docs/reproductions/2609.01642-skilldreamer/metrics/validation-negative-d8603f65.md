# 固定 8 条 validation 的 7B 负结果诊断

2026-10-14，固定 Qwen2.5-7B-Instruct revision `bb46c15ee4bb56c5b63245ef50fd7637234d6f75` 在真实 NVIDIA A100 上执行 seed42 的 question-only 格式探针。算法源为 `0f5dca9f`，独立 probe 源为 `d8603f65`；原预算为 600 秒硬限、最多 240 calls、每次 256 tokens、8 个工具动作、top-k3。只使用预先固定的 validation IDs `13/1/4/6/23/21/14/15`，无 gold/scorer，未使用 16 个 evaluation ID。

实际用时 596.9424 秒、210 calls、29194 generated tokens，8/8 调用流程结束；但这不代表核心链路通过。PSG/HSR 实际进入 7/8 题，真实 CSI 与 gallery load 各2次，工具动作0次，提交答案0次。保留为 **negative validation diagnostic**，无 passed receipt，不可 promotion，不构成模型能力比较。

完整指标、来源及逐题分类见 [sanitized negative artifact](public-a100-validation-negative-d8603f65.json)，绑定的 [final raw](raw/validation-negative-d8603f65/seed42.json)、[partial raw](raw/validation-negative-d8603f65/seed42.partial.json)、[210次实际调用 trace](raw/validation-negative-d8603f65/seed42.trace.jsonl) 与 [CPU逐条分类](raw/validation-negative-d8603f65/trace-analysis.json) 均为原文件逐字拷贝，SHA256 保留在 artifact 中。这里的模型响应不是 gold answer。

## 失败分类

| validation ID | calls / tokens | runtime调用 | JSON缺失/非法 | CSI行序/缺行 | 非法decision | 空字段 | 正常load后再询问 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 1 / 208 | 0 | PSG JSON语法错 | 0 | 0 | 0 | 0 |
| 1 | 30 / 4309 | 24 | 5 | 18 | 1 | 0 | 0 |
| 4 | 30 / 4153 | 24 | 0 | 13 | 8 | 2 | 1 |
| 6 | 30 / 3353 | 24 | 7 | 9 | 7 | 0 | 1 |
| 23 | 30 / 3920 | 24 | 0 | 4 | 14 | 6 | 0 |
| 21 | 30 / 3939 | 24 | 0 | 4 | 18 | 2 | 0 |
| 14 | 30 / 5194 | 24 | 0 | 12 | 12 | 0 | 0 |
| 15 | 29 / 4118 | 24 | 0 | 19 | 5 | 0 | 0 |

分类按原执行顺序互斥归因：168次 runtime CSI 中，12次无合法action JSON、79次标签行序/缺行、65次非法DECISION首词、10次空字段、2次实际load。7题都用尽原24次runtime调用，不是正常finish结束。

ID4 在全局call51加载rates后，call52–61是5次缺行与5次非法decision；ID6在call90加载arithmetic，call91为 `DECISION: Load the arithmetic skill.`，被原enum gate拒绝。所有11次load后响应均低于256个可见tokens，不能归因为截断。最长输入822tokens，低于原2048context上限。41个响应可见长度达到256（33个pseudo guidance、8个CSI）；原trace没有逐次token IDs/stop reason，因此不补造单次停止标记。

## 提示契约不足与解析失败必须分开

原固定源 `algorithm.py` 的126–131行只要求五个标签并提MATCH/PARTIAL_MATCH，没有明确五个非空 `LABEL: value` 行，也没有完整列出解析器接受的四个DECISION首词。134–146行解析器则严格要求顺序、冒号、非空值及 `MATCH/PARTIAL_MATCH/NO_MATCH/NO_CAPABILITY_GAP`。这是**提示契约欠明确**，未确认parser bug。

两个完整五行与合法action JSON却违反enum的实例：ID4/call54使用 `DECISION: Use the rates skill to calculate the reduced hourly wage.`；ID6/call91使用 `DECISION: Load the arithmetic skill.`。另两个包含合法 `DECISION: MATCH` 的实例（ID4/call55、ID15/call196）拥有合法calculator JSON，却缺第5个NEXT行；这里JSON解析通过，拒绝来自CSI行协议，不能误称“合法action被JSON误拒绝”。实际没有完整合法CSI却被action JSON解析拒绝的响应。

首次load后再询问是原 `execute_agent` 的显式流程，不是丢失动作：模型必须先看到真实gallery body，然后生成fresh action。环境每次step都计动作，finish同样计动作；因此0动作/answer=null证明没有到达实际工具入口。没有实际unknown-tool执行，也没有工具RuntimeError。

随后仅对提示文本补清非空冒号行、完整enum和JSON位置；parser、枚举、PSG/HSR/CSI算法、自动纠正/fallback、gold角色、评价IDs与预算均不改变。占位模板不填任务答案或技能判断。CPU fixture 验证严格拒绝保持、load后fresh calculator/finish入口可用；fixture不是模型能力证据。后续701f/5c07的独立同预算测量另见 [核心执行但零提交](validation-no-submit-5c07ef42.md)；**本负结果仍绑定原0f/d860源，不能重标为澄清后结果。** 原0.5B三seed失败也继续保留。
