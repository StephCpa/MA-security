# Two External-Validity Studies: Preregistration Drafts

Status: draft to be frozen and externally timestamped before the first human
judgment or model call. Interpretations are specified for every outcome so the
framing is not selected after observing results.

## Study H: human scoring anchors

### Objective

The three 0--3 scales currently rely on model raters. Study H tests whether
humans recognize the same constructs, whether humans agree with one another,
whether the paired directions reproduce, and whether the previously observed
retention-zero anomaly persists under human labels.

### Items and anchors

- Select 32 of the 96 five-form confirmation texts: 16 $S_C$ and 16 $S_P$.
- Stratify selection by form and model-assigned score so every observed score
  level on every axis appears; use a frozen random seed.
- Draw eight training anchors only from the calibration bank. Each anchor has
  an adjudicated reference score and a one-sentence rationale per axis.
- Do not use a confirmation item as a training anchor.

### Raters and procedure

- Recruit three humans who are not authors and have graduate-level CS,
  security, or equivalent relevant background.
- Blind raters to form, condition, behavior, model scores, and one another.
- Use the frozen rubrics for action retention, instruction centrality, and
  provenance signal. Shuffle axis packs and item orders independently.
- Require a fixed training-agreement floor on the eight anchors before
  releasing the 32 scored items.

### Preregistered outcomes

1. Quadratic-weighted human--model agreement per axis against the mean model
   score, with a bootstrap 95% confidence interval.
2. Ordinal Krippendorff's alpha among humans.
3. Sign and approximate magnitude of the human-scored $S_C-S_P$ contrast on
   each axis.
4. Protected-write frequency among items assigned human retention zero.

### Precision and decision rule

At true weighted kappa .70, simulations give approximate 95% intervals of
[.32,.95], [.39,.93], [.45,.89], and [.49,.87] for 24, 32, 48, and 64 items.
The study cannot distinguish .60 from .75 precisely. Decisions therefore use
the interval lower endpoint, not the point estimate.

- If the lower endpoint is at least .45 on all axes and all paired directions
  reproduce, the ratings retain their descriptive role.
- If the provenance-axis lower endpoint is below .45, that axis becomes
  exploratory and is removed from the contribution statement.
- If any paired direction fails to reproduce, withdraw the corresponding
  mechanism description and report the non-replication.

The planned 32-item design requires 288 judgments (32 items by three raters by
three axes), approximately five person-hours. Increasing to 48 items is a
budget-dependent precision improvement, not a change in the estimand.

## Study A: external stimulus validation with AgentDojo

### Objective and routes

Study A tests the five-form effect using externally defined injection tasks.
Route A1 runs inside AgentDojo and uses its security evaluator and benign task
utility. Route A2 ports AgentDojo injection goals into the existing
`write_shared` harness and is used only if the A1 pilot gate fails.

### A1 full design

- Freeze two AgentDojo suites by name before execution.
- Evaluate all injection tasks in those suites against a frozen user-task
  sample, capped at approximately 60 user-task/injection-task pairs.
- Construct five forms for each goal: bare goal R, neutral carrier C, marked
  carrier P, and one frozen sender-derived transformation of C and P
  ($S_C,S_P$).
- Generate sender derivatives once and freeze them before receiver execution.
- Use the pair as the independent unit.

The fixed-sequence primary comparisons are C versus P, followed only after
rejection by $S_C$ versus $S_P$. Use paired exact McNemar tests with familywise
$\alpha=.05$. Report benign utility with and without marker packaging as a
secondary outcome without alpha allocation.

### Mandatory A1 pilot gate

Run approximately ten pairs before the full study. The A1 route proceeds only
if the R form achieves its injection goal at a rate comparable to the
benchmark baseline and AgentDojo's security evaluator functions correctly on
wrapped variants. If the carrier invalidates the goal or evaluator, record the
failed gate and use Route A2. Do not modify AgentDojo checks after seeing pilot
outcomes.

### Preregistered interpretations

- If marker efficacy and residual protection both reproduce, the mechanism is
  not confined to the authored bank and the external result may enter the
  abstract.
- If marker efficacy reproduces but residual protection does not, describe the
  residual trace as bank- or fixture-conditioned.
- If marker efficacy does not reproduce, state in the abstract that the
  headline effect is bank-conditioned rather than confining the result to the
  limitations section.

Because optimized benchmark attacks may offer less headroom, the final freeze
must define the effect magnitude that counts as replication. A full A1 run is
expected to require roughly 3,000--6,000 calls.

## Recommended sequencing

For the AAMAS submission, run Study H and only the ten-pair A1 pilot. For a
later security-venue version, run A1 in full. If only one study is feasible,
prioritize Study H for AAMAS and Study A for the security-venue extension.

## Addendum, 1 October 2026: what ran, and an outcome the draft did not anticipate

This addendum is written after the Slack runs below. It does not alter the
draft above and is not a preregistration of those runs.

### Study A as executed

- Only the Slack suite ran live, as a single-suite extension rather than the
  two-suite A1 design: 55 pairs (eleven pilot-unseen user tasks crossed with
  all five official goals), five forms, two separately run models
  (`qwen36-agentdojo-five-form-001`, `deepseek-agentdojo-five-form-001`).
  Workspace was screened offline only.
- Because the 55 cells cross reused tasks and goals, the frozen analysis
  reported paired discordance tables and worst-case missingness bounds instead
  of the exact McNemar tests named above.
- Results: R/C/P/S_C/S_P security successes of 7/3/3/2/2 (Qwen, with 5/4/3/2/2
  unknown) and 3/3/2/2/2 (DeepSeek, none unknown) out of 55.

### Interpretation applied

The three preregistered interpretations assume that the external fixture can
detect an effect of the authored size. It could not: with the carrier at 3/55
successes, a perfect marker could reduce attack success by at most 3/55 =
.0545, 6.7% of the authored effect of .8125. The run is therefore a
headroom failure, neither "reproduces" nor "does not reproduce". Following
the intent of the third rule, the manuscript abstract now states that the
provenance effects are established only on author-written banks, rather than
confining that statement to the limitations section. The external null is not
reported as evidence against the mechanism.

### Proposed headroom gate for any further A1 run

To be frozen, with the specific values below confirmed or revised, before any
further model call:

1. Screen candidate suite-and-model combinations on a small fixed sample (for
   example ten pairs) under the R and C forms only.
2. Proceed to a five-form run only if the C success rate is at least 40%.
   Otherwise report that official unoptimized goals for that combination
   cannot test an effect of this magnitude, and do not run the full design.
3. Before the full run, freeze what counts as replication on that fixture,
   for example a C-minus-P missingness lower bound above zero together with a
   point estimate of at least half the observed C rate.
4. Repeating the same Slack fixture with the same model reproduces the floor
   rather than adding headroom, so it is not a priority.

### Study H versus the frozen F7 human-anchor plan

The frozen pack in `analysis/human-anchor-v1/` differs from Study H above:
it uses two human raters on all 96 texts and reports agreement without
acceptance thresholds, whereas Study H specifies three raters, 32 items, and
the interval-lower-endpoint decision rule (lower endpoint at least .45). No
human returns exist yet. Before any return, the authors should choose one of
two routes and date the choice: amend F7 to adopt the lower-endpoint decision
rule, stating the precision limit in the paper; or treat F7 as exploratory
agreement estimation and make no Study H decision-rule claim. In either case,
practice anchors must come only from the calibration bank, as both documents
already require.

