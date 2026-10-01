# AAMAS 2027 OpenReview 注册填写清单

更新时间：2026-09-15。依据 AAMAS 2027 官方说明、OpenReview 当前 Submission invitation schema，以及本项目当前 `main.tex`。

## 现在应填写

### Title

`Provenance after Generative-Agent Relay: Transformation, Propagation, and Coupled Authorization`

### Authors / Author IDs

- 在 OpenReview 中填写真实作者，而不是 `Anonymous Author(s)`。
- 按最终计划的作者顺序添加所有作者；逐一选择准确的 OpenReview profile。
- 每位作者的 profile 应包含：完整发表姓名、当前职位、机构邮箱、DBLP URL（如有）。
- 投稿 PDF 继续保持双盲，不在 PDF 或匿名补充材料中写作者身份。

### TL;DR

`Generative relays can erase explicit provenance markers while preserving action influence; derivation-time lineage and independently enforced write capabilities are both needed to prevent unauthorized state changes.`

该文本为 215 个字符，低于表单 250 字符上限。

### Abstract

直接粘贴当前 `main.tex` 的 abstract（约 199 词，满足官网建议的 100--300 词）：

> Generative multi-agent systems relay externally supplied content between models, tools, and shared state. This collaboration pattern creates a compositional safety problem: a sender can rewrite content in ways that remove an explicit provenance boundary while preserving enough of the requested action to influence a downstream agent. We separate this process into relay transformation, agent-to-agent propagation, and capability-mediated state change. In paired, preregistered experiments, a visible untrusted-content marker reduced protected-write attempts from 40/48 to 1/48. A normal model relay removed the literal marker from all 96 regenerated outputs, yet texts derived from marked inputs remained less actionable than matched texts derived from unmarked inputs (22/48 versus 44/48 attempts). A byte-identical Qwen evaluation reproduced both differences, while an adaptive relay policy largely removed the residual protection. An outcome-blind selector then identified 17/121 complete two-hop chains in a disjoint high-retention stratum without a faithful-relay instruction. Capability enforcement reduced unauthorized state mutations from 36/48 to 0/48 even though models continued to attempt writes. Finally, we show that residual risk under coupled controls decomposes exactly into cross-control failure covariance times the measured endpoint-and-fixture response to instruction elevation. These results motivate agent protocols that preserve lineage across derivation and separate semantic elevation from write authority.

### Subject areas

- Primary subject area: `Generative and Agentic AI (GAAI)`
- Secondary subject area 1: `Engineering and Analysis of Multiagent Systems (EMAS)`
- Secondary subject area 2: `Coordination, Organizations, Institutions, Norms, and Ethics (COINE)`

不要选择 GTEP。本稿没有效用函数、策略均衡或博弈论实证；博弈论方向留给后续论文。

### Area topics（选满 3 个）

1. `GAAI: Assurance, verification, and safety in generative and agentic AI systems`
2. `GAAI: Interaction protocols for agentic AI`
3. `GAAI: Benchmarks, evaluation, and metrics for generative and agentic AI systems`

第三项也可考虑 runtime support，但当前稿件的主要贡献是安全测量与评估，因此 benchmarks/evaluation/metrics 更准确。

### Findings of AAMAS 2027

按当前“若 AAMAS 主 Proceedings 未接收，则转投 USENIX Security Cycle 2”的路线，建议选择 `No`。AAMAS Findings 是正式、可引用的 CC-BY archival publication；若选择 `Yes` 并被 Findings 接收，同一工作通常不能再投 USENIX。

只有在作者团队认为“进入 AAMAS Findings”优先于保留 USENIX 转投机会时，才改选 `Yes`。这是本表中最需要全体作者共同确认的策略项。

### Reciprocal reviewer nomination

必须指定至少一名合格作者，除非确实满足豁免条件。优先指定符合下列任一条件的合作者：

1. 已获得计算机科学或相关领域博士学位；或
2. 博士三年级及以上，并至少有 3 篇相关同行评审论文。

若有合格作者，选择：

`We have nominated a qualified author (see above)`

并在上一栏选该作者的 OpenReview profile。不要为了通过表单而错误声明“无人符合资格”。

### Submission policies acknowledgement

逐项核实后勾选全部四项。尤其确认：

- 当前没有把本稿或实质相似版本同时投向另一 archival venue；
- 其他相关同时投稿如存在，已经以匿名 `under review` 方式引用；
- 所有作者 profile 已更新；
- 人类作者对 AI 辅助内容、引用和实验结果承担责任。

本项目中 AI 实际参与了假设、方法和实验设计，因此最终论文或补充材料需要披露所用工具、模型版本和相关 prompts。当前 `main.tex` 尚未包含这份披露，必须在正式 PDF 截止前补齐。

### Workshop Outreach Pipeline

不勾选，并将后面两个 workshop 字段留空。只有论文此前确实在列出的、符合条件的非 archival workshop 展示过并通过该通道投稿时才使用。

## 现在可以留空

- PDF：当前 OpenReview schema 标为 optional；作者注册阶段不用上传。正式提交时再上传双盲 PDF。
- Supplementary material：当前 optional；正式提交时再上传单个不超过 25 MB 的匿名 ZIP。

## 当前表单中暂未出现、但官网提到的字段

- Student paper：若第一作者或共同第一作者是任何类型的在读学生，官网要求勾选。当前 OpenReview schema 暂无该字段；在摘要截止前复查 Edit 页面，若仍无此项，联系 PC。
- Keywords：官网说明摘要提交时会要求关键词，但当前 schema 没有独立 keywords 字段；不要把关键词塞进 TL;DR 或 abstract。若后续字段出现，使用：`generative agents; multi-agent systems; prompt injection; provenance; agent protocols; capability security; evaluation`。

## 截止时间与提交前检查

- 所有作者完成 OpenReview 账号/profile：2026-09-17 AoE；折算北京时间约为 2026-09-18 20:00，建议立即完成。
- Abstract submission：2026-10-01 AoE；北京时间约为 2026-10-02 20:00。
- Full paper：2026-10-08 AoE；北京时间约为 2026-10-09 20:00。

创建注册后检查：标题无 LaTeX 换行、作者顺序正确、所有 profile 可解析、primary area 为 GAAI、三个 topics 无误、Findings 与团队的 USENIX 转投策略一致、reciprocal reviewer 声明真实、Workshop Outreach 未误选。
