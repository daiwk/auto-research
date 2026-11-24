"""Authored DCA/StableKL pages and append-once learning proposals.

Root owns shared catalog/learning integration and execution evidence. This
script uses already visually reviewed crops and captured official sources.
"""

from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov24-latest"
CACHE = ROOT / ".cache/nov24-latest/foundation-primary"
DATE = "2026-11-24"
SECTIONS = ["背景与主要改动", "核心公式", "同主题比较与边界", "数据协议与代码映射", "高成本完整实验"]

CONTENT = {
    "deep-cross-attention": {
        "aid": "2502.06785", "version": "v2", "module": "deep_cross_attention",
        "peer": "foundation-models:rd-attnres", "peer_path": "reproductions/2608.01075-rd-attnres/README.md",
        "card": "foundation-models/conditional-compute", "page": 4, "box": [306, 68, 544, 304],
        "caption": "Figure 4: Computation diagram of a DCA decoder block.",
        "sections_read": ["3.1-3.2", "5 Tables1,4,5,7", "fixed-v2 Figures3-4", "official Nov23 Google blog"],
        "formula": r"g_t=(G_t\odot(b_t+\bar w_t))\mathbf1,\qquad \bar w_t=\mathbf1\operatorname{ReLU}(w_t^TG_t),\qquad (q,k,v)=\big(\mathrm{GRN}_Q(G_t),\mathrm{GRN}_K(G_t),\mathrm{GRN}_V(G_t)\big).",
        "diagram": "flowchart LR\n H[原始输入与逐层增量输出] --> S[最新层优先的深度stack]\n S --> Q[独立Q GRN]\n S --> K[独立K GRN]\n S --> V[独立V GRN]\n Q --> A[普通因果token attention]\n K --> A\n V --> A\n A --> O[仅attention输出，不冒充完整decoder]",
        "diagram_en": "flowchart LR\n H[Original input and incremental layer outputs] --> S[Newest first depth stack]\n S --> Q[Independent Q GRN]\n S --> K[Independent K GRN]\n S --> V[Independent V GRN]\n Q --> A[Ordinary causal token attention]\n K --> A\n V --> A\n A --> O[Attention output only not a full decoder]",
        "cn": {
            "overview": "传统残差把原始输入和历层增量输出直接相加。DCA把这份历史保留下来，由可学习的feature×history基础权重，加上逐token、逐历史项的动态项，选择层输入；Q、K、V分别使用独立GRN-v3。这里的深度路由不是在层维做softmax，而是直接加权求和；普通attention仍在token维计算。",
            "detail": "固定v2§3.1文字公式为b+ReLU(wᵀG)：b初始化为1，w初始化为0。按PyTorch的ReLU'(0)=0，精确零初始化时动态w的第一步梯度为0；本地把它作为可见负控，而不是偷偷换激活或随机初始化。Figure3还画了文字公式未明确的Norm和不同的activation次序；本地声明按文字公式解释，不声称复刻作者训练器。Figure4的Q/K/V外部Norm以三套LayerNorm实现。",
            "results": "固定v2 Table5中6层LM1B模型的DCA为49.73M参数、PPL18.06±0.01，Transformer为49.65M、18.98±0.01；Table1的2-DCA速度5.39±0.06 batches/s低于基线8.14±0.18，但达到基线最终PPL的归一化训练时间为0.33。少用训练时间达到同PPL不等于每step更快。未报告生产线上A/B；这些是作者完整训练结果，不是本地路由核测量。",
            "local": "实现GRN-v3文字公式、三套独立参数、first+middle-sum+last-k历史栈、小型多头因果attention及真实autograd。历史元素是原始输入和各层增量输出，不是重复累加的完整residual state。有限历史不直接丢弃中间层，而把它们保存在未加权sum桶中。没有完整FFN/外层残差接线、LM训练、预训练checkpoint改装、KV cache或benchmark收益。非零w的梯度检查使用显式参数干预，不冒充w从零学出了动态路由。",
            "compare": "RD-AttnRes从Block AttnRes出发保留共享QK路由、单独解耦V，采用其attention-residual深度选择机制。DCA的Q/K/V三路均独立，并以feature-dependent基础权重加ReLU动态项线性求和，不是把RD的V路由复制三份。两者都改变attention输入来源，却不能互换归一化、历史缓存或完整训练证据。",
            "cost": "§5默认embedding512、FFN宽4倍、sequence128、batch2048，在64个TPU上训练500k steps，共131B tokens；另扫6至42层、C4多规模和ImageNet。完整矩阵显然超出单A100/A30或Mac，直接成本过高不复现，不做模型/数据下载或试训。仅2×5token、8宽、4历史源的小型核，三seed预算小于30秒（估计）；CUDA路径必须由本批真实A100/A30收据独立验收。",
            "date": "2025-02-10T18:58:52Z；核对版本v2为2025-07-23T19:32:20Z。2026-11-23 Google官方博客触发历史补录，**不是11月新发表论文**。",
        },
        "en": {
            "overview": "Standard residuals sum the input and previous incremental layer outputs. DCA retains that history and combines feature-by-history base weights with token/history-dependent terms. Q, K and V have independent GRN-v3 modules. Depth routing is an unnormalized weighted sum, not a layer-wise softmax; ordinary attention still operates across tokens.",
            "detail": "The fixed-v2 Section3.1 text specifies b+ReLU(wᵀG), initializing b to one and w to zero. Under PyTorch's ReLU'(0)=0 convention, the initial dynamic-w gradient is zero. We expose that negative control instead of changing activation or initialization. Figure3 additionally depicts normalization and a different activation ordering not explicit in the text equation. Local code declares the text-formula interpretation, not the authors' training implementation. Three LayerNorms follow the Q/K/V routes as in Figure4.",
            "results": "Fixed-v2 Table5 reports49.73M parameters and PPL18.06±0.01 for six-layer DCA on LM1B versus49.65M and18.98±0.01 for the Transformer. Table1's2-DCA runs5.39±0.06 batches/s versus8.14±0.18, but its normalized time to reach the baseline's final PPL is0.33. Less time to a quality target is not faster individual steps. No production online A/B is reported. These are full-training paper results, not local routing timings.",
            "local": "Implemented: text-formula GRN-v3, three independent routes, first/middle-sum/last-k history, small multi-head causal attention and actual autograd. History contains original input and incremental outputs, not repeatedly accumulated residual states. Limited history preserves intermediate outputs in an unweighted sum bucket rather than dropping them. Full FFN/outer-residual wiring, LM training, checkpoint retrofit, KV caching and benchmark gains are absent. Nonzero-w gradient checks use explicit parameter interventions, not a claim that dynamic routing was learned from zero initialization.",
            "compare": "RD-AttnRes starts from Block AttnRes, retains one QK route and separates V through its attention-residual mechanism. DCA instead separates all three Q/K/V routes and uses feature-dependent base weights plus ReLU dynamic terms in a linear sum. It is not three copies of RD's V route. Their normalization, historical storage and full-training evidence are not interchangeable.",
            "cost": "Section5 uses width512, four-times-wider FFNs, sequence128 and batch2048 over64 TPUs for500k steps, totaling131B tokens, plus6–42-layer, C4-scale and ImageNet sweeps. This clearly exceeds one A100/A30 or Mac. No model/data download or trial training is attempted. Only a2×5-token,8-wide,4-source core is budgeted below30seconds across three seeds (estimate). The advertised CUDA path requires this batch's independent real-A100/A30 receipt.",
            "date": "2025-02-10T18:58:52Z; reviewedv2 is2025-07-23T19:32:20Z. A Google blog published2026-11-23 triggered this historical backfill; it is **not a newly published November paper**.",
        },
        "qa": [
            ["history-is-increments", "basics", "DCA历史栈为什么不能装每层完整residual state？", "文字定义G保存输入和每层增量f_i(g_i)，完整state已经含旧层之和，再次把它们相加会重复计数。", "教学例：输入x、增量a和b应累成x+a+b；若存x、x+a、x+a+b再相加，会变成3x+2a+b。", "Why must DCA history store increments rather than full residual states?", "G contains the input and incremental f_i(g_i) outputs. Full states already sum earlier outputs, so summing them again double-counts history.", "Illustration: x,a,b sum to x+a+b. Summing states x,x+a,x+a+b gives3x+2a+b."],
            ["not-layer-softmax", "mechanism", "GRN-v3的动态项为什么不是普通softmax层注意力？", "它把b与ReLU(wᵀG)相加后直接线性加权；系数不要求非负或和为1，基础项还逐feature变化。", "教学例：三份全1历史、b=1且w=0输出3，不是softmax均值1；把b改成−2会输出−6。", "Why is GRN-v3 not ordinary softmax attention across layers?", "It directly weights history by b+ReLU(wᵀG). Coefficients need not be nonnegative or sum to one, and base weights vary by feature.", "Illustration: three all-one sources with b=1,w=0 yield3, not the softmax mean1. With b=−2 they yield−6."],
            ["three-versus-role-split", "comparison", "DCA与RD-AttnRes的Q/K/V解耦边界有什么区别？", "RD-AttnRes保留共享QK、解耦V；DCA对Q、K、V各自配置独立GRN-v3，且深度混合公式不同。", "教学例：只修改DCA的Q基础权重，K和V路由输出必须逐位不变；RD中Q和K本来共享路由。", "How does DCA's Q/K/V separation differ from RD-AttnRes?", "RD-AttnRes retains shared QK routing and separates V. DCA has three independent GRN-v3 modules and a different depth-mixing formula.", "Illustration: changing only DCA's Q base weights must leave K/V route outputs bitwise unchanged; RD shares the Q/K route."],
            ["zero-relu-not-hidden", "implementation", "零初始化w配ReLU时，怎样避免把动态路由诊断写成训练成功？", "先按原公式保留w=0并记录ReLU零点导数下初始梯度为0；再用明确标注的非零参数干预检查动态公式与梯度，不能悄悄随机初始化后声称忠实复刻训练。", "教学例：第一个测试断言w梯度全0；另一个测试手工设w=0.05后检查有限非零梯度。两项都不是LM收敛实验。", "How do we avoid calling zero-w/ReLU diagnostics successful dynamic-route training?", "Retain the specified zero initialization and expose its initial zero gradient under PyTorch's convention. Test the dynamic formula with a clearly labeled nonzero parameter intervention, not a hidden initialization change.", "Illustration: one test requires zero w gradients; another explicitly sets w=0.05 before checking nonzero finite gradients. Neither is an LM convergence experiment."],
        ],
    },
    "stablekl": {
        "aid": "2611.30835", "version": "v1", "module": "stablekl",
        "peer": "foundation-models:stochastic-rounding", "peer_path": "foundation-models/2611.13545-stochastic-rounding/README.md",
        "card": "foundation-models/training-budget", "page": 2, "box": [53, 66, 544, 314],
        "caption": "Figure 1: The problem and one consequence.",
        "sections_read": ["2-4", "5", "B.1", "B.4", "C.4", "fixed upstream Exponential source and README"],
        "formula": r"x=\frac{\lambda_q-\lambda_p}{\lambda_p},\quad \varphi(x)=x-\log(1+x)\approx\frac{x^2}{2+x}-2s^3\sum_{k=1}^{17}\frac{s^{2(k-1)}}{2k+1},\quad s=\frac{x}{2+x};\qquad \partial_{\lambda_p}KL=-\frac{x}{\lambda_p},\quad\partial_{\lambda_q}KL=\frac{x}{\lambda_q}.",
        "diagram": "flowchart LR\n P[FP32原始正rate参数] --> D[先做rate差值再除]\n D --> S[近等区间17项Horner级数]\n D --> F[远区间条件良好log公式]\n S --> V[非负KL值]\n F --> V\n D --> G[显式解析rate梯度]\n V --> O[CPU普通范围Rewrite，不是strict认证]\n G --> O",
        "diagram_en": "flowchart LR\n P[Raw positive FP32 rates] --> D[Difference before division]\n D --> S[17 term Horner series near equality]\n D --> F[Well conditioned log formulas far away]\n S --> V[Nonnegative KL]\n F --> V\n D --> G[Explicit analytic rate gradients]\n V --> O[CPU ordinary range Rewrite not strict certification]\n G --> O",
        "cn": {
            "overview": "近等分布的真实KL是二阶小量，但教科书公式往往由一阶或常数量相减得到，容易返回零、负数或错误梯度。StableKL把闭式KL重写成非负小量的组合，配合差值、补偿算术和解析梯度；它还区分F.kl_div算子误差与输入log-prob本身已丢失的信息。本地只选择其中Exponential族的Rewrite核。",
            "detail": "Exponential的x先由原始rate之差计算，避免先取ratio再减1。在−0.75≤x≤3上，FP32用K=17的Horner级数计算φ；两侧使用条件良好的log1p或log(rate_q/rate_p)分支。自定义autograd直接返回两rate解析导数。末端非负截断只是稳定公式的边界约定，不是对原始消去公式clamp就算修复。原文strict模式、区间算术与其他分布的误差自由变换不在本地范围。",
            "results": "作者在约8.5M输入、18个同族闭式KL及F.kl_div上报告值和梯度错误；相同working format的Rewrite去掉每配置超过97%的显著KL错误，严格模式在7.2M闭式样本上无显著错误。上述是作者冻结基准结果，不是本地几十个Exponential样本的覆盖结论；正确舍入的567M算子分量也不能借给本组件。未报告生产线上A/B。",
            "local": "仅FP32 CPU、形状匹配的正rate输入，17项φ级数、远区间分支及一阶解析autograd。对非有限/非正参数、dtype/形状/设备不符、ratio溢出/下溢和非有限结果直接拒绝，不冒充极端范围mantissa/exponent处理。独立80位Decimal参考以实际FP32存储值为输入，校验近等、区间边界、远区间、梯度和精确恒等；它不是区间认证。没有完整18族、FP16/BF16、strict正确舍入、F.kl_div、logits修复或蒸馏训练。",
            "compare": "随机舍入处理的是FP32小更新转BF16时落回同一格点，靠随机相邻格点在条件期望上保留变化。StableKL处理的是已存参数上的确定性代数消去，靠公式重写与解析梯度减少误差。前者不修复错误KL公式，后者也不能恢复输入量化前已经消失的更新；提高precision、clamp和随机舍入都不是可互换的补丁。",
            "cost": "作者仓库的冻结benchmark为10.8GB，README列明每配置CPU数小时、全部53配置需集群；下游含10seed大词表蒸馏、Qwen2.5-1.5B与GPT-2量化/电路实验，需额外模型数据。C.4还报告未融合参考算子的开销，不能把小核时间当完整包吞吐。完整实验直接成本过高不复现，不下载10.8GB或模型。仅32个近等标量与小型公式单测，三seed预算小于10秒（估计），CPU-only并拒绝CUDA。",
            "date": "2026-11-23T15:18:30Z；固定v1，本轮2026-11-24核对的新首发，不把公告/抓取日期替代原始时间。",
        },
        "en": {
            "overview": "For nearby distributions, true KL is second order, while textbook formulas subtract first-order or constant terms. They can return zero, negative values or inaccurate gradients. StableKL uses nonnegative decompositions, accurate differences, compensated arithmetic and analytic gradients, distinguishing operator error from information already lost in rounded log-probabilities. Local code covers only the Exponential Rewrite core.",
            "detail": "The Exponential argument is formed from the raw rate difference before division, not ratio-minus-one. On−0.75≤x≤3, FP32 uses a17-term Horner series for phi. Outside it, well-conditioned log1p or log(rate_q/rate_p) branches are used. Custom autograd returns analytic gradients for both rates. A final nonnegative clamp is a boundary convention of the stable formula, not a repair obtained by clamping the cancelling textbook formula. Strict mode, interval arithmetic and error-free transformations for other families are absent.",
            "results": "Across about8.5M inputs,18 same-family closed forms and F.kl_div, the authors report value/gradient failures. Same-format Rewrite removes over97% of significant KL errors per configuration; strict mode has no significant errors on7.2M closed-form samples. These are frozen paper-benchmark results, not coverage established by a few dozen local Exponential examples. Correct rounding on567M operator components cannot certify this component. No production online A/B is reported.",
            "local": "Only positive, matching-shape FP32 CPU rates, a17-term phi series, far-range branches and first-order analytic autograd are implemented. Nonfinite/nonpositive inputs, unsupported dtype/shape/device, ratio overflow/underflow and nonfinite outputs are rejected; extreme-range mantissa/exponent handling is not claimed. An independent80-digit Decimal reference uses actual stored FP32 values to check near equality, branch boundaries, far values, gradients and exact identity. It is not interval certification. All18 families, FP16/BF16, strict correct rounding, F.kl_div, logits repair and distillation are absent.",
            "compare": "Stochastic rounding addresses FP32 updates disappearing on conversion to the BF16 grid, preserving changes in conditional expectation through randomized adjacent values. StableKL addresses deterministic algebraic cancellation on already stored parameters through formula rewrites and analytic gradients. The former does not repair KL algebra; the latter cannot recover an update lost before input storage. Precision promotion, clamping and stochastic rounding are not interchangeable patches.",
            "cost": "The author repository lists a10.8GB frozen benchmark, CPU hours per configuration and a cluster for all53. Downstream work includes ten-seed large-vocabulary distillation and Qwen2.5-1.5B/GPT-2 quantization/circuit studies with additional downloads. Appendix C.4 reports overhead of unfused reference operators; a tiny core is not full-package throughput. Full experiments are too expensive and not attempted. No10.8GB data or models are downloaded. Only32 nearby scalars and small formula tests are budgeted below10seconds across three seeds (estimate), CPU-only with CUDA rejected.",
            "date": "2026-11-23T15:18:30Z; fixedv1, newly first-released and reviewed2026-11-24. Announcement/retrieval dates do not replace original publication time.",
        },
        "qa": [
            ["positive-not-accurate", "basics", "KL结果非负就说明计算正确吗？", "不是。消去可以把真实正KL变成0，也会产生正但偏差很大的值。clamp只去掉负号，不能恢复被舍掉的二阶量或梯度。", "教学例：rate_p=1、FP32 rate_q=1.0001时，朴素公式可为0，而存储输入的KL约5×10⁻9。", "Does nonnegative KL establish numerical correctness?", "No. Cancellation can turn positive KL into zero or leave a positive but inaccurate result. Clamping removes the sign without recovering the second-order value or gradient.", "Illustration: rates1 and FP32 1.0001 can give zero naively, while KL for those stored inputs is about5×10⁻9."],
            ["difference-before-ratio", "mechanism", "为什么Exponential修复要先做rate差，而不是ratio−1？", "近等浮点输入的直接减法可精确保留差值；先做ratio会在1附近舍入，再减1暴露该误差。φ级数随后直接表示二阶小量，解析梯度避免再经过消去链。", "教学例：把q设成1的下一个FP32数，d=q−1仍非零；稳定级数输出约7.1×10⁻15，而常数量相减可能归零。", "Why form the rate difference before computing the ratio-minus-one argument?", "Direct subtraction preserves nearby stored differences, while a ratio is rounded near one before subtraction exposes that error. The phi series represents the second-order quantity directly, and analytic gradients avoid another cancelling chain.", "Illustration: q equal to the next FP32 value above1 has nonzero d=q−1. The stable series gives about7.1×10⁻15, while constant-term subtraction may give zero."],
            ["not-stochastic-rounding", "comparison", "StableKL与随机舍入能互相替代吗？", "不能。随机舍入解决量化格点吞掉更新，并引入受控随机性；StableKL解决已存输入上的确定性消去。丢失在输入表示中的信息也不属于KL算子能恢复的范围。", "教学例：BF16把两个rate先都存成1，StableKL只能正确给0；若FP32仍保留两者差值，它才可通过重写恢复小的正KL。", "Can StableKL and stochastic rounding replace one another?", "No. Stochastic rounding addresses updates lost to a quantization grid; StableKL addresses deterministic cancellation on stored inputs. Information already lost in the input representation cannot be restored by the KL operator.", "Illustration: if BF16 first stores both rates as1, StableKL correctly returns0. If FP32 retains their difference, rewriting can recover the small positive KL."],
            ["reference-not-certification", "implementation", "本地80位Decimal对照为什么不能写成论文strict正确舍入验收？", "它只是有限样本的独立高精度参考，没有误差区间、舍入边界判定或Ziv重试，也只覆盖一个FP32分布族。严格认证与抽样数值一致是不同证据等级。", "教学例：32个近等输入相对误差小于2×10⁻6只能支持这个小核诊断，不能外推到18族或567M F.kl_div分量全部正确舍入。", "Why is the local80-digit Decimal comparison not strict correctly-rounded certification?", "It is a finite independent high-precision reference without interval bounds, midpoint decisions or Ziv retries, covering only one FP32 family. Agreement on samples and certified rounding are different evidence levels.", "Illustration: relative error below2×10⁻6 on32 inputs supports this small diagnostic, not correct rounding across18 families or567M F.kl_div components."],
        ],
    },
}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def document(spec, p, english):
    t = p["en" if english else "cn"]
    labels = (["Paper information", "Original paper summary", "Background and main changes", "Key original figure", "Core formula", "Paper results", "Same-topic comparison and boundaries", "Local reproduction", "Data protocol and code mapping", "Results and limitations", "High-cost full experiments"] if english else ["论文信息", "原始论文总结", "背景与主要改动", "原论文关键图", "核心公式", "论文离线与线上效果", "同主题比较与边界", "本地复现", "数据协议与代码映射", "结果、负控与边界", "高成本完整实验"])
    code = ("No verified paper-specific author repository was found in fixedv2 or the linked Google blog; this does not prove that none was ever released." if english else spec["code_status"])
    if spec["code"]:
        code = (f"[Author repository]({spec['code']}), pinned `{spec['upstream_revision']}`, BSD-3-Clause; local code is only the Exponential Rewrite component." if english else f"[原作者仓库]({spec['code']})，固定`{spec['upstream_revision']}`，BSD-3-Clause；本地只是Exponential Rewrite组件。")
    organization = (f"First author {spec['first_author']}: {spec['first_author_affiliation']}. " + ("Google Research collaborators are verified, not a Google first-author attribution." if spec["key"] == "deep-cross-attention" else "Other affiliations include Oxford, Cambridge, Fudan, Wake Forest and City University of Hong Kong (Dongguan).") if english else f"一作{spec['first_author']}：{spec['first_author_affiliation']}；" + ("Google Research合作者已核实，不把一作归为Google。" if spec["key"] == "deep-cross-attention" else "其余作者机构包括Oxford、Cambridge、Fudan、Wake Forest和City University of Hong Kong (Dongguan)。"))
    link = "[简体中文](README.md)" if english else "[English](README-en.md)"
    boundary = ("L1 component, diagnostic only; not complete paper/capability reproduction. Full experiments are too expensive, not reproduced (review DONE); no Evolve promotion." if english else "L1组件，diagnostic only，不是完整论文或模型能力复现。完整实验成本过高，不复现（审查 DONE）；不接Evolve晋级。")
    formula = p["formula"]
    command = f"PYTHONPATH=src python -c 'from auto_research.foundation_models.{p['module']} import diagnostic; print(diagnostic(42))'"
    test = "dca" if spec["key"] == "deep-cross-attention" else "stablekl"
    runtime = ("CPU three-seed component evidence is recorded separately. CUDA claims require this batch's real A100/A30 receipt, not CPU success." if spec["requires_gpu_validation"] else "CPU-only; CUDA is rejected. No GPU validation or model capability is claimed.") if english else ("CPU三seed组件证据单独记录。CUDA路径须以本批真实A100/A30收据验收，不能以CPU通过代替。" if spec["requires_gpu_validation"] else "CPU-only并拒绝CUDA；不宣称GPU验收或模型能力。")
    return f"""# {spec['title']}

{link}

> {boundary}

## {labels[0]}

| {'Field' if english else '字段'} | {'Value' if english else '内容'} |
| --- | --- |
| {'Paper link' if english else '论文链接'} | [arXiv:{p['aid']}{p['version']}]({spec['paper_url']}); [fixed PDF]({spec['reviewed_version_url']}) |
| {'Company / author institution' if english else '公司 / 作者机构'} | {organization} |
| {'Original publication' if english else '首次公开日期'} | {t['date']} |
| {'Author code' if english else '原作者开源代码'} | {code} |
| {'Local adapter / key' if english else '本地 adapter / key'} | `{spec['key']}`; `adapter: null`; not Evolve-integrated |
| {'Local code' if english else '本地复现代码'} | `src/auto_research/foundation_models/{p['module']}.py` |

## {labels[1]}

### {labels[2]}

{t['overview']}

<!-- paper-figure:start -->
### {labels[3]}

[![{p['caption']}](assets/paper-figure-01.png)]({spec['reviewed_version_url']}#page={p['page']})

{'Original fixed-version PDF crop including the complete original caption; visually checked without scientific-content edits. Copyright belongs to the authors. The full method/result in the figure is not local capability evidence.' if english else '固定版本PDF原图与完整原图注，已视觉核对，无科学内容编辑；版权归原作者所有。图中的完整方法/实验结果不是本地能力证据。'} [Provenance/SHA256](assets/provenance.json).
<!-- paper-figure:end -->

```mermaid
{p['diagram_en'] if english else p['diagram']}
```

### {labels[4]}

$$
{formula}
$$

{t['detail']}

### {labels[5]}

{t['results']}

### {labels[6]}

{t['compare']}

## {labels[7]}

### {labels[8]}

{t['local']}

```bash
{command}
PYTHONPATH=src python -m pytest -q tests/test_nov24_{test}.py
```

### {labels[9]}

{runtime} [CPU component evidence](metrics/component-cpu-seeds42-44.json).

### {labels[10]}

{t['cost']}

{'Terminal full-experiment status: not_reproduced_high_cost, review DONE, excluded from automatic retries/implementation queues. Component execution is not a full-model comparison.' if english else '完整实验为not_reproduced_high_cost终态、审查DONE，不进入自动重试/实现队列；组件执行不是完整模型对比。'}
"""


def main():
    if (AUDIT / "foundation-authored-bundle.json").exists():
        raise ValueError("append-once proposals already exist")
    specs = json.loads((AUDIT / "paper-proposals-foundation.json").read_text())["papers"]
    bank, english, proposals, accepted = {}, {}, [], []
    for spec in specs:
        p, identity = CONTENT[spec["key"]], "foundation-models:" + spec["key"]
        directory = ROOT / "docs" / spec["detail_path"]
        cn, en = document(spec, p, False), document(spec, p, True)
        directory.parent.mkdir(parents=True, exist_ok=True)
        directory.write_text(cn)
        directory.with_name("README-en.md").write_text("<!-- source-sha256: " + sha256(cn.encode()).hexdigest() + " -->\n" + en)
        source = CACHE / (p["aid"] + p["version"] + ".pdf")
        image = directory.parent / "assets/paper-figure-01.png"
        dump(image.with_name("provenance.json"), {
            "schema_version": 1, "paper_url": spec["paper_url"], "source_url": spec["reviewed_version_url"] + f"#page={p['page']}",
            "source_sha256": sha256(source.read_bytes()).hexdigest(), "source_pdf_sha256": sha256(source.read_bytes()).hexdigest(),
            "pdf_page": p["page"], "page": p["page"], "figure": p["caption"].split(":")[0], "caption": p["caption"],
            "crop_pdf_points": p["box"], "crop_box_pdf_points": p["box"], "render_scale": 3 if p["module"] != "stablekl" else 2,
            "asset_sha256": sha256(image.read_bytes()).hexdigest(), "image_sha256": sha256(image.read_bytes()).hexdigest(),
            "retrieved_on": DATE, "reviewed_version": p["version"], "visually_reviewed": True,
            "scientific_content_modified": False, "extraction": "Original PDF crop including complete caption",
            "copyright": "Copyright belongs to the original authors.",
        })
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
        revisions = {identity: sha256(cn.encode()).hexdigest(), p["peer"]: sha256((ROOT / "docs" / p["peer_path"]).read_bytes()).hexdigest()}
        comparison = questions[2]
        proposals.append({"paper": identity, "target_card": p["card"], "source_revisions": revisions,
                          "comparison": {"position": p["cn"]["overview"], "tradeoff": p["cn"]["compare"], "sections": SECTIONS[:3]},
                          "analysis": {"title": spec["title"], "body": p["cn"]["compare"] + " " + p["cn"]["detail"], "papers": pair},
                          "question": {"id": "nov24-" + spec["key"], "question": comparison["question"], "answer": comparison["answer"], "example": comparison["example"], "papers": pair},
                          "update": {"date": DATE, "papers": pair, "summary": p["cn"]["compare"] + " 完整实验不复现与本地L1组件分开，不晋级Evolve。"},
                          "english": {"comparison": {"position": p["en"]["overview"], "tradeoff": p["en"]["compare"]},
                                      "analysis": {"title": spec["title"], "body": p["en"]["compare"] + " " + p["en"]["detail"]},
                                      "question": translations[comparison["id"]], "update": p["en"]["compare"] + " Full-experiment non-reproduction remains separate from L1 components; no Evolve promotion."}})
        accepted.append({"arxiv_id": p["aid"], "identity": identity, "key": spec["key"], "domain": "foundation-models",
                         "title": spec["title"], "first_author": spec["first_author"], "first_author_affiliation": spec["first_author_affiliation"],
                         "first_published_at": spec["published_at"], "announced_on": spec["announced_on"], "intake_class": spec["intake_class"],
                         "reviewed_version": p["version"], "reviewed_source_url": spec["reviewed_version_url"], "source_sha256": sha256(source.read_bytes()).hexdigest(),
                         "html_sha256": sha256((CACHE / (p["aid"] + p["version"] + ".html")).read_bytes()).hexdigest(),
                         "sections_read": p["sections_read"], "scope": p["en"]["local"], "cost_basis": p["en"]["cost"],
                         "implementation_status": "component_only", "evaluation_tier": "l1_mechanism", "local_detail_path": spec["detail_path"],
                         "requires_gpu_validation": spec["requires_gpu_validation"], "gpu_validation_passed": False,
                         "code_url": spec["code"], "upstream_revision": spec["upstream_revision"],
                         "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
                         "review_done": True, "automatic_retry": False, "automatic_implementation_queue": False})
    dump(AUDIT / "foundation-authored-bundle.json", {"schema_version": 1, "date": DATE, "papers": bank, "english_question_units": english})
    dump(AUDIT / "deep-dive-proposals-foundation.json", {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "proposals": proposals})
    dump(AUDIT / "foundation-review.json", {"schema_version": 1, "reviewed_on": DATE, "accepted": accepted,
                                          "preflight_before_implementation": True, "available_resource": "one A100 or A30, or local Mac",
                                          "watermark_change_claimed": False, "large_downloads_authorized_or_needed": False,
                                          "scope": "One Google-blog-triggered historical priority backfill and one Nov23 first release; finite selection, not exhaustive coverage."})
    print("Authored two bilingual papers, eight reviewed questions and two same-topic update proposals; shared banks untouched.")


if __name__ == "__main__":
    main()
