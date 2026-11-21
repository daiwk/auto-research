"""One-shot reviewed Nov21 overlap-paper documentation and authored learning.

Small fixed-v1 PDFs must already be captured; this does not download models,
execute training, edit shared learning banks, or certify CUDA validation.
"""

from hashlib import sha256
import json
from pathlib import Path

import fitz

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov21-latest/foundation"
AUDIT = ROOT / "docs/research-audits/nov21-latest"
DATE = "2026-11-21"
SECTIONS = ["背景与主要改动", "核心公式", "数据协议与代码映射", "同主题比较与边界", "高成本完整实验"]

PAPERS = [
    {
        "aid": "2611.26020", "key": "frontier-replay", "module": "frontier_replay",
        "title": "FrontierReplay: Split-Free Exact Prefix Caching for Hybrid Language Models",
        "author": "Zekun Wang", "org": "Beijing Institute of Technology",
        "published_at": "2026-11-19T12:34:25Z", "gpu": False,
        "topic": ["推理与系统效率", "混合模型前缀缓存与检查点"],
        "card": "foundation-models/compression-and-cache", "peer": "foundation-models:replayssm",
        "sections_read": ["2 Eq1-2", "3", "4.1-4.6", "5", "6.1-6.5"],
        "figure": [6, [53, 75, 562, 322], "Figure 5: FrontierReplay architecture."],
        "diagram": "flowchart LR\n A[Observed template turn and branch boundaries] --> B[16 token planner and bounded window]\n B --> C[Lease live anchor or exact cut fallback]\n C --> D[Explicit pending checkpoint]\n E[External completion signal] --> F[Publish only completed checkpoint]\n D --> F\n F --> G[Dead superseded speculative proven running tiers]\n G --> H[Loss estimate then LRU eviction]\n H --> I[Bounded dead slot reclaim decision]",
        "formula": r"\mathrm{tier}(c)\in\{-1,0,1,2,3,4\},\quad c_{\mathrm{evict}}=\arg\min_{c\in\mathcal E}(\mathrm{tier}(c),\widehat{\mathrm{lost}}(c),\mathrm{lastUsed}(c)),\qquad r\le\min(16,2d,C-C_{\min}).",
        "cn": {
            "overview": "混合模型的attention KV可按页复用，但递归状态只在保存过的精确位置恢复。FrontierReplay先根据已观察到的模板稳定尾、已完成turn和分叉点规划检查点；原生prefill不断开，之后只重放短窗递归输入生成精确状态。保留策略优先保护仍在执行的请求锚点和已证明可复用的分叉，而非只看历史频率。",
            "detail": "正文§4.3使用16-token页；native chunk end必须已经16对齐，不能静默向下取整来虚构该位置已有状态。完成turn可按原文取decode已经经过的最后页边界，结构目标仍可向下对齐后请求回放。分叉至少256token，回放窗最多1024token；缺少活锚点/日志页则退化为exact cut。Falcon-H1不在1568token以下保存或恢复状态。§4.4分层为dead=-1、superseded=0、natural=1、未用template/turn=2、proven=3、running=4；两次来自同一request的restore不能晋升proven。只有完成事件后才公开新检查点，失败/未完成状态不能命中；lease保护正在用的锚点。长前缀额外保护稳定尾之前一个prefill预算内、深度至少4096的最深natural检查点。",
            "results": "作者在vLLM0.30、A80080GB、32GiB联合缓存预算下比较Qwen3.5-9B与Falcon-H1-7B，覆盖聊天、Agent、文档问答和树搜索。报告精确缓存相对vLLM的goodput为1.11至4.26倍，median TTFT降低16%至89%；这些是作者原生完整serving实验，不是本地CPU调度器速度。没有生产线上A/B。27B/34B另用双卡张量并行。",
            "local": "实现纯CPU host-policy组件：观察边界规划、显式pending/completion发布、lease、分层准入/驱逐、长前缀保护和每16请求的回收决策。KV驻留、已观察progress、稳定尾与非自身驱逐信号均由调用方显式提供；没有自主观察真实服务或用户日志。状态槽只是合成token前缀元数据，不是模型状态。没有GDN/Mamba回放kernel、舍入bitmask、vLLM、CUDA事件、VMM或实际内存借出，因此不能称精确CUDA重放、服务接入或吞吐复现。",
            "compare": "ReplaySSM主要减少decode/投机时的逐token矩阵状态写回，把输入缓存、output-only读取和接受回滚联动；FrontierReplay主要为下一次prefill的结构边界补造精确检查点，并管理哪些状态值得保留。前者的周期刷新和高低精度anchor不是后者的会话frontier保留策略。本地ReplaySSM已有独立Triton证据，但不能把那份执行回执借给本页的host策略，更不能把两种输入日志视为可互换。",
            "cost": "完整论文包含4B至34B五种模型、四类长上下文轨迹、多基线负载/SLO扫点、原生Triton和vLLM集成；27B/34B明确双卡张量并行，部分点为三次配对运行。单A100/A30或Mac不适合日常重跑完整矩阵，直接成本过高不复现。仅纯CPU策略诊断预期三seed合计小于10秒，无模型/数据下载、API或原生serving进程；该时间是预算估计，不是完整实验实测。",
        },
        "en": {
            "overview": "Attention KV is reusable by page, but hybrid recurrent state can resume only at an exactly saved position. FrontierReplay plans checkpoints from observed template-stable ends, finished turns and branch junctions. Native prefill remains uncut; short-window state-only replay later materializes exact states. Retention protects active anchors and proven branches instead of relying only on historical frequency.",
            "detail": "Section4.3 uses16-token pages. Native chunk ends must already be16-aligned: silently rounding them down would invent an exposed state. Completed turns may use the last page passed during decode, while structural targets may be rounded down and still require replay. Branch depths are at least256, and the replay window is1024tokens. Missing live anchors or log pages force an exact cut. Falcon-H1 never saves/restores below1568tokens. Section4.4 tiers are dead−1, superseded0, natural1, unused template/turn2, proven3 and running4. Repeated restores by one request do not prove reuse. A checkpoint becomes visible only after completion; failed or pending states cannot hit, and leases protect in-use anchors. Long-prefix protection selects the deepest natural checkpoint within one prefill budget before the stable end, at depth at least4096.",
            "results": "The authors compare Qwen3.5-9B and Falcon-H1-7B under vLLM0.30 on an A80080GB with a32GiB combined cache, across chat, agent, document-QA and tree-search traces. Reported exact-cache goodput is1.11–4.26times vLLM and median TTFT falls16–89%. These are native serving measurements, not timings of the local CPU policy. No production online A/B is reported. The27B/34B experiments additionally use two-way tensor parallelism.",
            "local": "A CPU-only host-policy component implements observed-boundary planning, explicit pending/completion publication, leases, tiered admission/eviction, long-prefix protection and a sixteen-request reclaim decision. The caller supplies KV residency, observed progress, stable ends and non-self eviction signals; there is no autonomous service or user-log observation. Slots contain synthetic token-prefix metadata, not model state. No GDN/Mamba replay kernel, precision-rounding bitmask, vLLM, CUDA event, VMM or actual memory lending is implemented. This is not exact CUDA replay, serving integration or a throughput reproduction.",
            "compare": "ReplaySSM reduces per-token matrix-state writes during decoding/speculation through input caching, output-only reads and acceptance rollback. FrontierReplay instead materializes exact checkpoints at structural boundaries for subsequent prefill and decides which states remain useful. Periodic refresh and split-precision anchors are not conversation-frontier retention. Existing standalone Triton evidence for local ReplaySSM cannot certify this host-policy component; the two input logs are not interchangeable.",
            "cost": "The complete study spans five4B–34B models, four long-context workloads, multiple baseline/load/SLO sweeps and native Triton/vLLM integration. The27B/34B runs explicitly require two-way tensor parallelism, and some points have three paired runs. The complete campaign is too expensive for routine single-A100/A30 or Mac reproduction. Only CPU policy diagnostics are budgeted below10seconds across three seeds, without model/data downloads, APIs or native serving. This is a budget estimate, not measured full-experiment time.",
        },
        "qa": [
            ["exact-boundary", "basics", "为什么有KV页仍可能无法复用整段混合模型前缀？", "递归状态是覆盖更新的。即使KV页还在，恢复位置也必须有完全对应的递归检查点；不能把较晚状态截短成较早状态。", "教学例：KV覆盖到640token，但最近状态只在528；原生服务仍需从528重算到640。", "Why can resident KV pages still fail to reuse a hybrid prefix?", "Recurrent state is overwritten in place. Resumption needs the exact matching checkpoint; a later state cannot simply be truncated to an earlier one.", "Illustration: KV reaches640tokens but the nearest state is at528; the native model must recompute the remainder."],
            ["distinct-restore", "mechanism", "一个request恢复同一检查点两次，就算proven了吗？", "不算。需要至少两个不同恢复request，或者它本来就是已知分叉；否则每条会话的祖先都会被单次后继访问永久保护。", "教学例：request b重复restore只留tier2；b和c都restore后才进入tier3。", "Do two restores by one request make a checkpoint proven?", "No. Promotion needs at least two distinct restoring requests, or an already-known branch. Otherwise ordinary single-successor conversation anchors would all become protected.", "Illustration: repeated restores by b remain tier2; restores by both b and c qualify for tier3."],
            ["decode-versus-prefill", "comparison", "FrontierReplay和ReplaySSM都记录输入，解决的是同一个问题吗？", "不是。ReplaySSM围绕decode状态写回、output-only和投机回滚；FrontierReplay围绕prefill结构边界的检查点产生与保留。相似代数不代表服务策略、精度或证据可直接共用。", "教学例：16步decode刷新正确，不能证明下一会话的模板边界已保存、仍驻留且可命中。", "Do FrontierReplay and ReplaySSM solve the same problem because both log inputs?", "No. ReplaySSM targets decode-state writes, output-only computation and speculative rollback; FrontierReplay targets checkpoint production and retention at prefill structural boundaries. Similar algebra does not share serving policies, precision contracts or evidence.", "Illustration: a correct sixteen-step decode refresh does not prove that a next-turn template boundary was saved and remains reachable."],
            ["publish-after-completion", "implementation", "为什么不能在prepare后立即把检查点放进lookup？", "prepare只预留位置，设备写入尚未完成；提前公开会让其他request读到部分状态。这里只在显式成功完成后发布，失败则撤销，lease未释放的锚点不可驱逐。", "教学例：pending的640状态必须查不到；失败后删除，不能用全零状态代替成功检查点。", "Why must lookup exclude a checkpoint immediately after prepare?", "Prepare only reserves a slot; device writes may be incomplete. Publication before completion could expose partial state. This component publishes only explicit success, removes failed reservations and never evicts leased anchors.", "Illustration: a pending640-token state must miss; failure removes it rather than publishing zero state."],
        ],
    },
    {
        "aid": "2611.25172", "key": "mv-jepa", "module": "mv_jepa",
        "title": "MV-JEPA: Post-Training Video Encoders for Cross-View Understanding",
        "author": "Yangchen Zhao", "org": "University of Minnesota, Twin Cities",
        "published_at": "2026-11-18T20:58:38Z", "gpu": True,
        "topic": ["JEPA与世界模型", "跨视角表征与预测后训练"],
        "card": "multimodal-models/world-state-actions", "peer": "foundation-models:time-jepa",
        "sections_read": ["1-2", "3 Eq1-4", "4.1-4.5", "5"],
        "figure": [3, [107, 82, 505, 368], "Figure 1: MV-JEPA overview."],
        "diagram": "flowchart LR\n C[Context token views] --> V[Visible tokens independently encoded]\n V --> P[Shared projection plus distinct view IDs]\n M[Masked context queries] --> J[Joint self attention predictor]\n H[Held out queries no visual input] --> J\n P --> J\n F[Full context and held out views teacher only] --> T[Frozen EMA teacher plus per token LN]\n J --> L[Masked context and all held out token L1]\n T --> L\n S[152 multi view 148 replay shuffled schedule] --> L\n L --> U[Online optimizer then explicit EMA]",
        "formula": r"\mathcal L_{MV}=\frac{\sum_k\sum_{p\in M_k}D^{-1}\|\hat y_{k,p}-\operatorname{sg}(y_{k,p})\|_1+\sum_{p\in\Omega_h}D^{-1}\|\hat y_{h,p}-\operatorname{sg}(y_{h,p})\|_1}{\sum_k|M_k|+|\Omega_h|},\qquad\bar\theta\leftarrow0.99925\bar\theta+0.00075\theta.",
        "cn": {
            "overview": "MV-JEPA直接后训练已有JEPA视频编码器，强化不同摄像头视角之间的对象/时刻对应。共享student分别编码各context view的可见token；联合predictor利用所有context特征，既重建被mask的context位置，又预测一个完全held-out视图。held-out图像/特征从不进入student或predictor，只提供teacher目标；推理仍可独立编码单视角。",
            "detail": "完整context和held-out由EMA teacher编码，经逐token LayerNorm并stop-gradient。context视图分配互异随机view ID，held-out使用专属ID；masked-context和held-out使用两种不同mask embedding。Eq4对masked-context和全部held-out目标token等权，先逐example归一化，再对batch取均值，不能按view等权或全batch微平均。每epoch随机打散152次多视图与148次原始单视图replay，共享online encoder和predictor；optimizer后按0.99925更新teacher。",
            "results": "作者V-JEPA2-L后训练后，ABO Recall@1从52.82%到62.18%（+9.36个百分点），Ego-Exo4D六候选moment检索从30.11%到44.75%（+14.64个百分点）。这些是冻结真实视频encoder的原文评测，不是本地tiny token模型的准确率；相对百分比和百分点不可混用。原文还报告迁移和多种冻结probe，未报告生产线上A/B。",
            "local": "实现真实小型shared self-attention encoder、独立context编码、联合predictor、两种query、互异view ID、teacher-only held-out、Eq4损失、共享单视图replay和显式EMA。输入为人工构造token特征，不是像素，不加载V-JEPA权重；位置编码是声明过的tiny一维正弦码，不冒充原生时空position。没有八block视频mask器、数据裁剪/解码、V-JEPA2.1多层5632维监督或visible距离加权、完整训练和真实检索。诊断检查隔离与梯度，不是视觉能力或Evolve证据。",
            "compare": "Time-JEPA用物理时序作额外训练目标，在同一online encoder上执行masked潜变量预测和unmasked物理态回归；MV-JEPA用另一个摄像头的latent作held-out目标，并让联合predictor从多个独立context视图推断。两者都不能把训练目标喂回推理输入，但MV-JEPA的跨view query不是Time-JEPA的传感器head；重放保持表征和物理时序对齐也是不同验收。",
            "cost": "正文明确V-JEPA2-L使用16帧256×256输入，多视图batch48/replay24、30epoch即9000updates，在单RTX PRO6000 Blackwell约18小时；另有MVImgNet2.0、Ego-Exo4D与ImageNet/Kinetics/SSv2重放及大量probe。按单A100/A30或Mac预算，完整实验成本过高，不复现，不做昂贵试跑。只验收8宽tiny token机制，预期三seed小于30秒，无模型/数据下载或API；CUDA结果须等本批真实GPU回执，不以CPU测试代替。",
        },
        "en": {
            "overview": "MV-JEPA post-trains a pretrained JEPA video encoder for object and moment correspondence across camera views. A shared student independently encodes visible tokens from each context view. A joint predictor reconstructs masked context positions and predicts an entirely held-out view. Held-out pixels/features never enter the student or predictor; they only supply teacher targets. Single-view inference remains independent.",
            "detail": "The EMA teacher encodes full context and held-out observations; targets receive per-token LayerNorm and stop-gradient. Contexts receive distinct randomly assigned view IDs, while held-out queries have a reserved ID; the two query types use separate mask embeddings. Eq4 gives equal weight to masked-context and all held-out target tokens, normalizing each example before averaging the batch. It is neither view-wise averaging nor a batch-wide micro-average. Each epoch shuffles152multiview and148original single-view replay updates with shared online encoder/predictor. Teacher EMA follows the optimizer at momentum0.99925.",
            "results": "For V-JEPA2-L, the authors report ABO Recall@1 rising52.82% to62.18% (+9.36percentage points), and six-candidate Ego-Exo4D moment retrieval30.11% to44.75% (+14.64points). These are frozen real-video-encoder evaluations, not accuracy measurements of the local tiny token model. Relative percentages and percentage points differ. The paper also reports transfer and frozen probes, without production online A/B.",
            "local": "A real tiny shared self-attention encoder, independently encoded contexts, joint predictor, two query types, distinct view IDs, teacher-only held-out targets, Eq4 loss, shared single-view replay and explicit EMA are implemented. Inputs are synthetic token features, not pixels; no V-JEPA weights are loaded. The declared tiny one-dimensional sinusoidal encoding is not the native spatiotemporal position code. Eight-block video masks, data crops/decoding, V-JEPA2.1 multi-layer5632-dimensional targets and visible-distance weighting, full training and real retrieval are absent. Isolation/gradient diagnostics are not visual capability or Evolve evidence.",
            "compare": "Time-JEPA supplies physical time-series targets through masked latent prediction and unmasked physical-state regression on one online encoder. MV-JEPA instead predicts another camera's latent targets through a joint predictor over independently encoded context views. Both keep training targets out of inference inputs, but cross-view queries are not Time-JEPA's sensor head; replay-based retention and physical-time alignment require different checks.",
            "cost": "The paper explicitly uses16-frame256×256 inputs, multiview batch48/replay24 and9000updates over30epochs; V-JEPA2-L takes roughly18hours on one RTX PRO6000 Blackwell. MVImgNet2.0/Ego-Exo4D, ImageNet/Kinetics/SSv2 replay and many probes add cost. The complete experiment is too expensive for this single-A100/A30 or Mac budget and is not attempted. Only an8-wide tiny token mechanism is budgeted below30seconds across three seeds, with no model/data downloads or APIs. CPU tests do not complete CUDA validation; that requires this batch's real-GPU receipt.",
        },
        "qa": [
            ["heldout-not-extra-input", "basics", "held-out视图是多给student一台摄像头吗？", "不是。它只由teacher产生目标；student和predictor必须根据其他context视图推断它，推理时也不要求该额外观察。", "教学例：遮住背面照片，只给正面和侧面；背面latent只在loss端使用。", "Is the held-out view an extra camera input to the student?", "No. Only the teacher turns it into a target. The student and predictor infer it from other contexts, and inference does not require that additional observation.", "Illustration: provide front and side views, while a hidden back view supplies targets only at the loss."],
            ["token-normalization", "mechanism", "为什么Eq4不能先对每个view的loss求平均？", "mask数量可能不同；论文给每个监督token同等权重，而不是每个view同等权重。还要先逐example归一化，再平均batch。", "教学例：两个context各1和3个mask，加held-out4个token；总共8个目标等权，不是三组各占三分之一。", "Why not average a loss for each view before applying Eq4?", "Views may have different mask counts. The paper weights supervised tokens equally, not views, and normalizes each example before batch averaging.", "Illustration: contexts with one and three masked tokens plus four held-out tokens create eight equally weighted targets, not three equally weighted groups."],
            ["time-jepa-targets", "comparison", "MV-JEPA和Time-JEPA都用额外监督，目标能互换吗？", "不能。前者是跨摄像头latent并需要联合view predictor；后者是对齐物理时序并有unmasked回归分支。二者训练目标都不应变成student输入。", "教学例：速度标量属于Time-JEPA物理head，背面视图的一组token属于MV-JEPA held-out query；换标签不等于同一任务。", "Can MV-JEPA and Time-JEPA swap their additional targets?", "No. MV-JEPA predicts cross-camera latents through a joint-view predictor; Time-JEPA aligns physical sequences through an unmasked regression branch. Neither target should become a student input.", "Illustration: a velocity scalar belongs to a physical head; back-view tokens belong to held-out queries. Replacing labels does not preserve the task."],
            ["leak-gradient-control", "implementation", "怎样检查held-out和masked context没有偷进student？", "固定view ID，任意改held-out内容或被mask的context token，predictor输出应不变；这些改动可改变teacher目标/loss，但不能产生held-out输入梯度。teacher参数也必须无梯度，只做显式EMA。", "教学例：把held-out token乘30后，预测不变而目标可变；若预测变化，就有训练输入泄漏。", "How do we test that held-out and masked context observations do not leak?", "With fixed view IDs, changing held-out values or masked context tokens must leave predictor outputs unchanged. Teacher targets/loss may change, but held-out inputs must receive no gradient. Teacher parameters remain gradient-free and update only by explicit EMA.", "Illustration: multiplying held-out tokens by30 may change targets but not predictions; changing predictions reveals input leakage."],
        ],
    },
]


def dump(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def document(p, english=False):
    text = p["en" if english else "cn"]
    heading = ["Paper information", "Original paper summary", "Background and main changes", "Key original figure",
               "Core formula", "Paper results", "Local reproduction", "Data protocol and code mapping",
               "Same-topic comparison and boundaries", "High-cost full experiments"] if english else [
                   "论文信息", "原始论文总结", "背景与主要改动", "原论文关键图", "核心公式", "论文离线与线上效果",
                   "本地复现", "数据协议与代码映射", "同主题比较与边界", "高成本完整实验"]
    page, _, caption = p["figure"]
    url = f"https://arxiv.org/pdf/{p['aid']}v1"
    link = "[简体中文](README.md)" if english else "[English](README-en.md)"
    status = "L1 host-policy/token-wiring component; not a complete paper reproduction. High-cost full experiments are not reproduced (review DONE)." if english else "L1策略/训练连线组件，不是完整论文复现。完整实验：成本过高，不复现（审查 DONE）。"
    no_code = "No verifiable paper-specific author code found in fixedv1 or this finite repository search; generic dependencies and same-name unrelated repositories are not author releases." if english else "固定v1及本轮有限公开仓库检索未找到可核验的论文专用作者代码；不把通用依赖或无关同名仓库当作开源实现。"
    attribution = (f"Original fixed-v1 PDF crop, page{page}; copyright belongs to the authors. Visually checked, with no scientific-content edits. [Crop/provenance](assets/provenance.json). The figure illustrates the author's full method, not the local diagnostic."
                   if english else f"图片来自[原论文]({url}#page={page})第{page}页，版权归原作者所有；原图及图注已视觉核对，无科学内容编辑。[裁剪与SHA256](assets/provenance.json)。图示是作者完整方法，不是本地诊断结果。")
    command = f"PYTHONPATH=src python -c 'from auto_research.foundation_models.{p['module']} import diagnostic; print(diagnostic(42))'"
    evidence = ("The batch runner records source-bound diagnostics separately. Counts, loss and gradient controls are not model accuracy or throughput. A missing real CUDA receipt is not a pass; no capability or Evolve promotion is claimed."
                if english else "源绑定的实际诊断由本批runner单独记录；计数、loss与梯度负控不是模型准确率或吞吐。缺少真实CUDA回执不能算通过，不宣称能力提升或Evolve晋级。")
    return f"""# {p['title']}

{link}

> {status}

## {heading[0]}

| {'Field' if english else '字段'} | {'Value' if english else '内容'} |
| --- | --- |
| {'Paper link' if english else '论文链接'} | [arXiv:{p['aid']}v1](https://arxiv.org/abs/{p['aid']}v1); [fixed PDF]({url}) |
| {'Company / institution / school' if english else '公司 / 机构 / 学校'} | {p['author']}: {p['org']} (fixed-v1 first-author byline) |
| {'Original publication date' if english else '首次公开日期'} | {p['published_at']}; arXiv announcement2026-11-20; selected2026-11-21, not a new first release today |
| {'Original author code' if english else '原作者开源代码'} | {no_code} |
| {'Local adapter / key' if english else '本地 adapter / 稳定键'} | `{p['key']}`; `adapter: null`; not Evolve-integrated |
| {'Local code directory' if english else '本地复现代码目录'} | `src/auto_research/foundation_models/{p['module']}.py` |

## {heading[1]}

### {heading[2]}

{text['overview']}

```mermaid
{p['diagram']}
```

<!-- paper-figure:start -->
### {heading[3]}

[![{caption}](assets/paper-figure-01.png)]({url}#page={page})

{attribution}
<!-- paper-figure:end -->

### {heading[4]}

$$
{p['formula']}
$$

{text['detail']}

### {heading[5]}

{text['results']}

## {heading[6]}

### {heading[7]}

{text['local']}

```bash
{command}
PYTHONPATH=src python -m pytest tests/test_nov21_{p['module']}.py -q
```

{evidence}

### {heading[8]}

{text['compare']}

### {heading[9]}

{text['cost']}

{'High-cost full experiments are review DONE / not reproduced, terminal and not automatically retried. No result from another paper certifies this implementation.' if english else '高成本完整实验为审查 DONE / 不复现，终态且不自动重试；不能借用其他论文的运行回执验收本页实现。'}
"""


def main():
    if (AUDIT / "foundation-authored-bundle.json").exists():
        raise RuntimeError("one-shot authored integration exists; preserve reviewed and executed state")
    paths = {row["domain"] + ":" + row["key"]: row["detail_path"]
             for row in json.loads((ROOT / "docs/research-manifest.json").read_text())["papers"]}
    bank, english, proposals, accepted = {}, {}, [], []
    for p in PAPERS:
        identity = "foundation-models:" + p["key"]
        detail = f"foundation-models/{p['aid']}-{p['key']}/README.md"
        paths[identity] = detail
        directory = ROOT / "docs" / detail
        assets = directory.parent / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        pdf = CACHE / (p["aid"] + ".pdf")
        pdf_hash = sha256(pdf.read_bytes()).hexdigest()
        page, box, caption = p["figure"]
        doc = fitz.open(pdf)
        image = assets / "paper-figure-01.png"
        doc[page - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(box), alpha=False).save(image)
        dump(assets / "provenance.json", {"source_url": f"https://arxiv.org/pdf/{p['aid']}v1#page={page}",
             "paper_url": f"https://arxiv.org/abs/{p['aid']}v1", "reviewed_version": "v1", "retrieved_on": DATE,
             "page": page, "crop_box_pdf_points": box, "caption": caption,
             "caption_note": "Full original caption is retained in the crop; this text is its short title, not a substituted local caption.",
             "extraction": "Original PDF crop including original caption; no semantic editing",
             "visually_reviewed": True, "source_pdf_sha256": pdf_hash,
             "asset_sha256": sha256(image.read_bytes()).hexdigest(), "copyright": "Copyright belongs to the original authors."})
        cn = document(p)
        directory.write_text(cn)
        directory.with_name("README-en.md").write_text("<!-- source-sha256: " + sha256(cn.encode()).hexdigest() + " -->\n" + document(p, True))
        spec = {"domain": "foundation-models", "key": p["key"], "title": p["title"],
                "paper_url": f"https://arxiv.org/abs/{p['aid']}v1", "reviewed_version_url": f"https://arxiv.org/pdf/{p['aid']}v1",
                "reviewed_version": "v1", "published": p["published_at"][:10], "published_at": p["published_at"],
                "announced_on": "2026-11-20", "detail_path": detail, "topic": p["topic"],
                "first_author": p["author"], "first_author_affiliation": p["org"],
                "affiliation_evidence": "Fixed-v1 PDF and HTML byline; model provider and collaborator do not change first-author affiliation.",
                "verified_priority_organizations": [], "code": None,
                "code_status": "固定v1及本轮有限公开检索未找到可核验的论文专用原作者实现；不把通用依赖或无关同名库当作代码。",
                "code_license": None, "upstream_revision": None, "method_source_sha256": pdf_hash,
                "adapter": None, "priority": "P1", "intake_class": "overlap_selection_backfill",
                "implementation_status": "component_only", "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
                "promotion_eligible": False, "evolve_integrated": False,
                "local_operator": f"auto_research.foundation_models.{p['module']}.diagnostic",
                "local_command": f"PYTHONPATH=src python -c 'from auto_research.foundation_models.{p['module']} import diagnostic; print(diagnostic(42))'",
                "requires_gpu_validation": p["gpu"], "gpu_validation_passed": False,
                "gpu_validation_artifact": f"docs/gpu-validations/{p['key']}-a100-20261121-latest.json" if p["gpu"] else None,
                "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
                "review_done": True, "review_resolution": "not_reproduced_high_cost",
                "automatic_retry": False, "automatic_implementation_queue": False,
                "cost_assessment": {"source": f"https://arxiv.org/pdf/{p['aid']}v1", "sections": p["sections_read"],
                                    "available_resource": "one A100 or A30, or local Mac", "paper_configuration": p["cn"]["cost"],
                                    "estimated_cost_basis": "Fixed-paper configuration; full experiment not attempted. Component budget is an estimate, not a measured full-run cost.",
                                    "decision": "成本过高，不复现（审查 DONE）；仅验收低成本声明组件"},
                "summary": p["cn"]["overview"] + " " + p["cn"]["local"]}
        dump(ROOT / f"src/auto_research/paper_specs/catalog/foundation-models/{p['key']}.json", spec)
        accepted.append({"arxiv_id": p["aid"], "identity": identity, "key": p["key"], "domain": "foundation-models",
                         "title": p["title"], "first_author": p["author"], "first_author_affiliation": p["org"],
                         "first_published_at": p["published_at"], "announced_on": "2026-11-20", "intake_class": "overlap_selection_backfill",
                         "reviewed_version": "v1", "reviewed_source_url": spec["reviewed_version_url"], "source_sha256": pdf_hash,
                         "html_sha256": sha256((CACHE / (p["aid"] + ".html")).read_bytes()).hexdigest(),
                         "sections_read": p["sections_read"], "implementation_status": "component_only", "evaluation_tier": "l1_mechanism",
                         "scope": p["en"]["local"], "cost_basis": p["en"]["cost"], "local_detail_path": detail,
                         "requires_gpu_validation": p["gpu"], "gpu_validation_passed": False,
                         "code_url": None, "upstream_revision": None, "full_experiment_status": "not_reproduced_high_cost",
                         "full_experiment_review_done": True, "review_done": True, "automatic_retry": False,
                         "automatic_implementation_queue": False})
        questions, translations = [], {}
        for qid, level, q, a, example, eq, ea, ee in p["qa"]:
            questions.append({"id": qid, "level": level, "question": q, "answer": a, "example": example,
                              "source_sections": SECTIONS, "added": DATE})
            translations[qid] = {"question": eq, "answer": ea, "example": ee}
        bank[identity] = {"questions": questions}
        units = question_units({identity: questions})
        for q in questions:
            uid = f"qa/{identity}/{q['id']}"
            english[uid] = {"source_sha256": units[uid].source_sha256, "reviewed": True, "fields": translations[q["id"]]}
        pair = [identity, p["peer"]]
        revisions = {key: sha256((ROOT / "docs" / paths[key]).read_bytes()).hexdigest() for key in pair}
        comparison = questions[2]
        proposals.append({"paper": identity, "target_card": p["card"], "source_revisions": revisions,
                          "comparison": {"position": p["cn"]["overview"], "tradeoff": p["cn"]["compare"], "sections": SECTIONS[:2] + [SECTIONS[3]]},
                          "analysis": {"title": p["title"], "body": p["cn"]["compare"] + " " + p["cn"]["detail"], "papers": pair},
                          "question": {"id": "nov21-" + p["key"], "question": comparison["question"], "answer": comparison["answer"], "example": comparison["example"], "papers": pair},
                          "update": {"date": DATE, "papers": pair, "summary": p["cn"]["compare"] + " 本地组件证据与完整实验不复现分开记录。"},
                          "english": {"comparison": {"position": p["en"]["overview"], "tradeoff": p["en"]["compare"]},
                                      "analysis": {"title": p["title"], "body": p["en"]["compare"] + " " + p["en"]["detail"]},
                                      "question": translations[comparison["id"]], "update": p["en"]["compare"] + " Local component evidence remains separate from high-cost non-reproduction."}})
    dump(AUDIT / "foundation-authored-bundle.json", {"schema_version": 1, "date": DATE, "papers": bank, "english_question_units": english})
    dump(AUDIT / "deep-dive-proposals-foundation.json", {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "proposals": proposals})
    dump(AUDIT / "foundation-review.json", {"schema_version": 1, "reviewed_on": DATE, "requested_window": ["2026-11-20", DATE],
         "scope": "Finite overlap selection: neither paper is a Nov20/21 first release; no full-source or watermark-advance claim.",
         "preflight_before_implementation": True, "available_resource": "one A100 or A30, or local Mac",
         "large_downloads_authorized_or_needed": False, "watermark_change_claimed": False, "accepted": accepted,
         "selection_notes": ["Both papers are genuine new selections from the Nov20 bulletin, not newly first-published today.",
                             "MV-JEPA first-author affiliation is UMN; Cisco collaboration and V-JEPA backbone do not make it a Meta paper.",
                             "Unrelated SCU-zly/GGO-JEPA medical CT code is not the MV-JEPA paper's author release.",
                             "No complete training/serving campaign, checkpoint/data download, paid API or Evolve promotion."]})
    print("Authored2papers,8reviewed bilingual questions and2deep-dive proposals; shared banks untouched.")


if __name__ == "__main__":
    main()
