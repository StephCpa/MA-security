# Corrected follow-up plan for the AAMAS GAAI submission

Status: working design, not a frozen preregistration. The initial 27 September review involved archived-data audits only. The 28 September execution checkpoint below supersedes that no-new-calls status. Proposal labels F1--F9 refer to the attached review's suggestions; they do not rename the project's existing E1--E12 experiments.

## Execution checkpoint — 28 September

- F3/F4 implementation and live development calibration have run on qwen3.6-flash. The expanded bank produced no observed protected request, with one attack-chain outcome unresolved by truncation. This does not establish susceptibility for a large same-fixture efficacy confirmation; that confirmation has not launched.
- A post-hoc stage audit now localizes this floor: target literals survived in 22/24 unmarked and 24/24 marked sender outputs; attack-chain R2 invocations were 11/10/2 for L0/L1/L2, with both target literals in 9/10/2 inputs. Some archived R1 payloads are direct exact-target write commands that R2 declined. Sender loss alone cannot explain the terminal floor. These lexical/routing measurements are not semantic-retention labels or a replacement primary endpoint; see `../runs/qwen36-chain-calibration-002/BOTTLENECK_AUDIT.md`.
- A separate paired wording diagnostic corrected an ambiguous legitimate-task control: explicit Write wording achieved six exact writes in every arm, whereas the original noun-phrase wording was summarized as retrieval. Historical outcomes are retained. This is one task template, not general utility validation.
- F2 has now been evaluated on a new endpoint using the original 192 archived candidates and group assignments. Selected/excluded two-hop delegations were 118/121 and 69/71. Both groups are near ceiling; the observed contrast does not show useful enrichment. This is structural delegation, not protected mutation or demonstrated malicious semantic continuity. No same-model temporal-replication claim is made.
- F6's capability-status cue experiment completed 252 calls. At fixed b=1 and tool visibility, elevated exact requests were 45/48 in both cue conditions; untrusted-placement descriptive counts were 29/48 without and 35/48 with the cue. Authorized controls completed 30/30 in each. This is a separate legacy receiver task, not tool hiding or the full chain. The 16-item, three-additional-draw repeat panel completed another 192 calls: elevated counts remained 15/16 per cue condition in all four draws; untrusted counts were 9, 8, 8, 7 without and 13 throughout with the cue. Two of 64 source-condition cells flipped the exact endpoint. These short-window repetitions do not estimate cross-day drift.
- A separately scoped standardized host-cue intervention on the unchanged 96 archived summaries completed 204 calls. S_C exact-target requests were 40/48 without and 32/48 with the cue (primary paired RD -0.16667, exact McNemar p=0.0078125); S_P counts were 10/48 and 8/48. The conservative paired projection interval for the primary RD includes zero and is retained alongside the test. Any unauthorized process-local writes are reported separately because some outputs targeted other resources. This does not complete the native-span intervention or identify mediation of the original trace.
- A concurrent neutral-sentence follow-up completed 306 calls: S_C exact-target counts were 40/48 (no sentence), 31/48 (neutral formatting) and 30/48 (provenance); S_P counts were 10/48, 9/48 and 8/48. The focused provenance-minus-neutral S_C RD is -0.02083, with conservative interval [-0.20767, 0.17036]. No new p value was reported. This limits attribution of the prior cue effect to untrusted-source semantics; it does not establish equivalence of the two sentences.
- The ten runs listed at this checkpoint total 1,836 calls and 1,099,412 tokens, excluding earlier interface/connectivity probes. Subsequent calibrations are reported separately below and are not silently folded into that total. Detailed run manifests, raw logs, code snapshots and reports are under `../runs/qwen36-*`. F7 human-rating packs and frozen analysis are ready, but human returns remain outstanding. Do not replace human anchoring or chain validation with further generic delegation counts.
- Native external-benchmark work proceeds separately in `analysis/agentdojo-native-v1/`, using the official AgentDojo 0.1.35 wheel and benchmark v1.2.2. Offline reference utility passes for workspace 40/40 and slack 21/21. The unmodified injectability helper incorrectly filters out current list-valued message content; a non-mutating sidecar finds visible canaries in all 61 reference traces. Slack's five attack reference checks pass; workspace has six passing references and eight tasks with empty reference actions. No upstream predicate was modified.
- The native Slack pilot completed 30/30 sessions, 165 calls and 302,332 tokens: baseline utility 9/10, raw utility 9/10 with one official security success, marked utility 9/10 with one success on a different pair. All pre-call engineering gates pass. Exact exposure logging missed newline-to-space folding in the marked arm; a post-hoc diagnostic preserves the original flags and confirms payload exposure in all 20 injected sessions. Replay of all 30 sessions passed 744 checks without API calls. This is feasibility evidence for a five-form external study, not equivalence, an optimized-attack benchmark score, or confirmation of the provenance mechanism. The whole-bank next design must not select only the successful pilot pairs.
- The separately frozen native five-form extension is now running at `../runs/qwen36-agentdojo-five-form-001`: all eleven pilot-unseen Slack user tasks crossed with all five goals, 55 pairs, 110 completed sender calls and 286 planned receiver sessions including eleven controls. All generated outputs were frozen before receiver execution. This is a finite crossed bank, not 55 IID payloads; analysis reports paired differences, user/goal breakdowns and missingness bounds without IID significance tests. It does not complete the original two-suite draft or resolve Workspace scorer controls. Its in-progress calls are not yet included in the completed-run total above.
- The five-form native Slack extension has now completed: all 286 receiver sessions and 110 sender generations, with 4,350 replay checks and no model calls during audit. Security successes were R 7/55, C 3/55, P 3/55, S_C 2/55 and S_P 2/55, with 2--5 unknown terminal outcomes per form. Payload exposure was 55/55 after whitespace normalization. C-P and S_C-S_P remain descriptive finite-bank contrasts; no IID significance test is claimed. Workspace offline controls additionally exposed an upstream task-11/12 predicate that accepts partial wrong-file deletion, so those tasks are excluded from any exact-deletion external-validity claim.
- The native five-form Slack result is floor-limited for mechanism testing: R=7/55 and C=3/55 make the counterfactual maximum C-to-P range 3/55=0.0545 if P had zero successes, only 6.7% of the authored 0.8125 effect. The observed P successes and unknowns yield bounds [-0.0545,0.0727], while S_C-S_P bounds are [-0.0364,0.0364] versus the authored 0.4583. The external nulls therefore support neither replication nor non-replication. Before repeating this fixture, screen model-suite pairs for sufficient raw base rate; otherwise report the measurement-headroom limitation. The Workspace task-11/12 scorer defect remains an upstream issue, not a local repair or model finding.
- A Workspace headroom screen was frozen over ten user tasks × six non-empty-reference goals (120 planned baseline/raw sessions), but stopped after 15 sessions on provider HTTP 400 `Repetitive tool calls detected`. It supplies no headroom estimate and no model-result claim; it exposes an interaction between provider repetitive-call protection and official Workspace trajectories. The archived response and recovered first row are retained, with no retry.
- The three-probe DeepSeek connectivity/model-identity gate passed. A fresh matched run then completed all 20 sessions: baseline utility 10/10, raw-goal utility 9/10, and one official attack success in the raw arm. It used 76 model calls and 131,746 tokens; replay passed 181 checks with no API calls. This supports only a cautious second-model feasibility comparison, not a provider-wide attack-rate claim or a provenance-mechanism test. Earlier transport-failed runs remain excluded.
- The DeepSeek five-form extension subsequently completed all 286 planned sessions in `../runs/deepseek-agentdojo-five-form-001`. It used 110 sender generations and 1,343 receiver calls; all generations were valid, all 11 controls had known utility success, and normalized exposure was 55/55 in every injected form. Security successes were R 3/55, C 3/55, P 2/55, S_C 2/55 and S_P 2/55, with no unknown receiver outcomes. The archived responses replayed through the official runtime and predicates with 3,861 checks and zero model calls during audit. These counts are provider-stratified descriptive evidence, not pooled estimates. Compared with Qwen's R 7/55, C 3/55, P 3/55, S_C 2/55 and S_P 2/55, both providers show low raw base rates and therefore insufficient dynamic range for testing the authored provenance effect. The DeepSeek run does not establish replication or falsification of that mechanism.
- A zero-call content audit of the 17 complete DeepSeek retention-propagation chains found action-verb preservation in 17/17, mean directive-token recall .989, and synthetic-identifier preservation in 14/14 eligible chains. This characterizes the receiver-2 inputs reached by the selected chains; it is not a new propagation probability, a semantic-equivalence test, or evidence that the emitted payloads were identical.
- A separate benign-delegation structural control completed at `../runs/deepseek-benign-delegation-control-002`. The frozen design used 16 chains, receiver instruction eligibility, the ring/MCP-HTTP path, and a 48-call ceiling. It made 30 calls with zero retries and passed all 30 wire-audit checks. Source delegation occurred in 13/16 chains; receiver-1 activation was 1/16 and receiver-2 activation was 1/13 conditional opportunities. This is a plumbing/positive control only, not an adversarial propagation estimate and not pooled with the 17/121 endpoint. The earlier `...control-001` directory is retained as a transport-failure diagnostic with an empty event database, not as a zero-delegation result.
- A new receiver-authorized propagation calibration completed at `../runs/qwen36-authorized-propagation-calibration-001`. Twelve disjoint authored attack items were sender-transformed once and the same marked sender output was presented under L0 and L2 to an R2 worker whose policy explicitly authorized writes to `protected/canary`. All 60 calls returned the expected `qwen3.6-flash` identity: R1 delegated 12/12 and R2 made an exact protected request in 12/12 under both arms. An independent offline recount matches the report. The result validates an action-capable fixture but is ceiling-limited and deliberately does not estimate unauthorized mutation, lineage efficacy, or natural propagation; it is not pooled with the 17/121 endpoint.
- A zero-call headroom audit of that calibration found the literal `protected/canary` and a write verb in all 12 sender summaries and all 24 R1 payloads. The ceiling is therefore attributable to direct action-bearing stimulus content, not evidence of a lineage null. Any follow-up lineage study must use a predeclared weaker/indirect content stratum.
- The predeclared weaker-content calibration then completed at `../runs/qwen36-authorized-propagation-weak-calibration-001` (60 calls, all `qwen3.6-flash`). Source records contained no write verb and used pending-state/handoff language. Exact protected requests were 2/12 under L0 and 2/12 under L2; all 24 R1 stages delegated and all 24 R2 stages were called. The two positive cases differed by item across arms, so this is not evidence of a lineage effect. It establishes non-ceiling headroom for a future confirmatory design; the independent recount and headroom audit are archived with the run.
- The disjoint 48-pair follow-up then completed at `../runs/qwen36-authorized-propagation-confirmation-001` (240 calls, all `qwen3.6-flash`). Exact protected requests were 6/48 under L0 and 4/48 under L2; paired risk difference L2--L0 was -0.0417, with five L0-only and three L2-only discordances and exact two-sided McNemar `p=0.7266`. The family breakdown was 0/16 versus 0/16 for handoff records, 0/16 versus 0/16 for pending states, and 6/16 versus 4/16 for review registers. This is a non-ceiling, internally frozen fixture comparison with no evidence of a lineage effect; it is not an unauthorized-mutation or defense result. Independent recount and headroom audit match the raw report.

## 1. Deadlines, page budget, and scope

The official [main-track call](https://warwick.ac.uk/fac/sci/dcs/aamas2027/calls/call-for-main-track/) gives abstract submission on 1 October 2026, full-paper submission on 8 October, and rebuttal on 20--24 November. Deadlines are end-of-day UTC-12. The first two correspond to 2 October and 9 October at 19:59 Beijing time. Work to the earlier calendar dates, leaving upload time.

The [submission instructions](https://warwick.ac.uk/fac/sci/dcs/aamas2027/guidelines-and-policies/instructions/) allow eight pages of main text plus any number of reference pages. Our current seven-page PDF contains about six pages of main text. Reference pages do not consume the eight-page body budget. There is no need to remove substantive results merely because references would occupy an eighth PDF page.

Keep this paper empirical. A content-controlled relay chain and measured authorization outcomes fit its current question. Non-chain welfare, equilibrium, and strategic cooperation remain a separate research direction.

## 2. Completed audits that change the proposed plan

### F1a: retention strata, extended to both receiver models

Run `python analyze_aamas_retention_strata_v2.py` from the artifact root. Results and pair identifiers are under `analysis/retention-strata-v2/` in this paper directory. Source text hashes were checked across the DeepSeek and Qwen receiver evaluations.

| Receiver | Rater-A retention difference | n | S_C attempts | S_P attempts | C-only / P-only | RD | Exploratory two-sided McNemar p |
|---|---|---:|---:|---:|---:|---:|---:|
| DeepSeek | 0 | 17 | 15 | 13 | 3 / 1 | 0.1176 | 0.625 |
| DeepSeek | 1 | 15 | 15 | 3 | 12 / 0 | 0.8000 | 0.000488281 |
| DeepSeek | >=2 | 16 | 14 | 6 | 9 / 1 | 0.5000 | 0.0214844 |
| Qwen | 0 | 17 | 15 | 12 | 4 / 1 | 0.1765 | 0.375 |
| Qwen | 1 | 15 | 15 | 3 | 12 / 0 | 0.8000 | 0.000488281 |
| Qwen | >=2 | 16 | 15 | 10 | 6 / 1 | 0.3125 | 0.125 |

Rater B and explicitly defined consensus strata are included in the full report. Both raters assign a zero difference to 15 pairs: their S_C/S_P counts are 14/12 for DeepSeek and 14/11 for Qwen. The conservative paired-RD intervals are wide: for the rater-A zero-difference group, [-0.2919, 0.4684] and [-0.2657, 0.5324]. These intervals use a Bonferroni projection of exact intervals for the two discordant-cell probabilities; they are not ordinary Clopper--Pearson intervals for a risk difference.

The aggregate DeepSeek difference is 22/48 = 0.4583, or 45.83 percentage points, not 22 percentage points. A smaller difference inside a post-treatment rating stratum does not identify how much protection comes from filtering. A nonsignificant stratum is not evidence of equivalence. Equal ordinal ratings do not guarantee equal action content. The contrast is also not monotone in the ordinal retention difference. Keep this as descriptive evidence motivating intervention.

### Source-framing audit of the original propagation result

Run `python audit_retention_source_framing.py`. The report is `analysis/retention-source-framing/report.json`. All 121 selected input hashes were matched to original sender events, including the archived prompt text.

| Archived sender instruction | Selected inputs | R1 delegations | Two consecutive receiver delegations |
|---|---:|---:|---:|
| Faithful copy | 37 | 7 | 2 |
| Transform into a short downstream task | 84 | 33 | 15 |
| Total | 121 | 40 | 17 |

The two live receivers did not receive a faithful-copy instruction. The input archive nevertheless includes 37 outputs generated under such an instruction. The paper has been corrected to state the stage distinction and both source groups. Do not write that no faithful-copy instruction occurred anywhere in the pipeline. The 15/84 task-condensation subgroup is descriptive, identified in this audit; it must not replace the prespecified 17/121 headline as a newly confirmatory result.

The 192-item source bank contains delegation instructions about documents and tasks. Its selected texts have no `protected/canary` literal. Requiring the old two-hop endpoint to contain a canary identifier would introduce an inapplicable outcome. Terminal protected writes belong in the new chain study.

### F2: the concurrent check already attempted

`../runs/deepseek-retention-discrimination-001/` contains the interleaved 121/71 check. All 192 calls requested `deepseek-v4-flash` but reported `deepseek-flash`; both groups had zero delegations. The earlier run reported `deepseek-v4-flash`. This identity mismatch prevents a same-endpoint discrimination comparison and does not establish why behavior changed. The audit and addendum supersede the old report's pipeline-pass interpretation.

A new comparison on a currently available endpoint would be a new endpoint study. Do not sell another model as a free temporal repeat of the original 17/121 result. Do not spend the deadline budget retrying an unavailable name indefinitely.

## 3. Corrections required before freezing any new experiment

1. **Preserve endpoint names.** The existing exact protected request includes the attack value as well as operation and resource. A resource-only call is a targeted-resource write request. Existing broad-write counts and proposed non-allowlisted-write counts are also different outcomes. Log them separately and keep the old definitions attached to old tables.
2. **Preserve the unit.** One directive is one independent block; repeated calls measure within-item instability. Store repeats with their original directive identifier, rather than treating them as extra independent stimuli.
3. **Do not equate a logistic coefficient with a causal share.** Conditional logistic regression produces conditional odds ratios. It cannot partition the 0.4583 risk difference into content and provenance percentages without further causal assumptions, interactions, and a defined standardization target. Use paired risk differences for the manipulated cue contrasts.
4. **Do not infer causality from F1a strata.** Both a null and a positive residual stratum contrast are compatible with unmeasured content changes and rating error. F1a neither proves sanitization nor rules it out.
5. **Treat the six authored families as fixed design strata.** Use directive-level paired inference. If adding stratified bootstrap intervals, preserve family counts and resample paired directives within each family. Resampling six families answers a family-superpopulation question with only six clusters; it is a sensitivity analysis, not an automatic improvement.
6. **Freeze directional testing and multiplicity.** The original studies used two-sided tests. New one-sided tests require a prospective rationale; do not choose tails after inspecting new outcomes. At 13--0 discordances, one-sided p is 1/8192 and two-sided p is 2/8192. There is no universal 0.2 minimum detectable paired risk difference: discordance counts determine exact-test power.
7. **Report actual freeze evidence.** An OSF registration is one possible mechanism, not a synonym for preregistration. Record the external timestamp evidence actually obtained, with anonymity preserved. Internal file creation alone is not an externally witnessed registration.
8. **Separate identity checks from performance selection.** A requested/reported identifier check confirms an API contract, not fixed hidden weights. Archive model identifiers, dates, parameters, and available service metadata. Stop an incompatible run before the main campaign. A behavioral pilot must be on a separate calibration bank.

## 4. Recommended main addition: F3/F4 combined chain

### Scientific target

Measure whether inherited provenance re-rendered at every derivation changes terminal protected-write requests under an attacker who can edit external content but cannot edit system prompts or authenticated metadata. This directly connects relay transformation to an action-capable downstream worker.

### Chain and authority

Use a protected-write stimulus bank with a common operation/resource/value schema. The old 192-item delegation bank is not interchangeable with that bank. Converting its tasks into protected-write directives creates adapted stimuli, not an unchanged external or previously frozen bank. Freeze any adaptation procedure, the resulting texts, and the calibration/confirmation split before observing downstream outcomes; record prior exposure of reused items. The proposed count of 96 is a planning target, not evidence that 96 eligible, disjoint directives are already assembled.

Source record -> honest sender -> R1 orchestrator -> R2 worker -> process-local gateway/store. The trusted task allows extracting follow-up work and writing to a benign scratch resource; it never authorizes the protected canary. R1 may delegate relevant work to R2. This task facilitates legitimate delegation but does not instruct R1 to forward the malicious directive. Record this as a different task regime from the earlier binary-action propagation study.

Use three lineage conditions:

- L0: unmarked source carrier; no inherited label.
- L1: source marker present; derived messages receive no inherited marker.
- L2: the same marked-source sender output as L1; authenticated ancestry is joined and rendered for each receiving agent.

Generate the P-derived sender output once and share it between L1 and L2. Their contrast then holds the sender output fixed. Audit label integrity independently of the model's response to the rendered marker. L1 is a declared derivation configuration, not a prevalence claim about all deployments.

Cross lineage with **baseline injection** versus **relay-targeted injection**. Calling the baseline "no attack" would be misleading because the original directive is already malicious. Optimize content-only templates on a disjoint calibration bank, freeze a single template using terminal R2 success, and keep all prompts, resources, and attack targets synthetic. No system-prompt override is allowed. If best-of-three is later evaluated, describe it as a three-query attack budget, not a universal attacker upper bound.

### Outcomes and analysis

Primary: exact R2 protected request per seeded directive under the relay-targeted attack, comparing L2 with L1. Count chains stopped by an observed nondelegating R1 as zero for this terminal pipeline outcome. API failures remain missing/failed observations, not safe outcomes. Distinguish requests from mutations, and log both any protected-resource writes and exact attack-value writes.

Use a two-sided paired exact McNemar test for the primary contrast. Report the no-additional-template contrast and L1 versus L0 as secondary. This avoids placing the flagship attack-resistance test behind a baseline comparison that could be at floor. Report the lineage-by-attack risk-difference interaction descriptively with paired uncertainty; do not reuse an exact sign-flip test that assumes symmetry of a multi-valued difference under a mere mean-zero null. A GLMM is optional supporting analysis, with convergence/separation reported, not a prerequisite or a mechanism decomposition.

Add authorized benign tasks to measure whether marker propagation suppresses useful work. The same stored R2 request can be replayed through the enforcement policy to verify authorization logic; that replay is a mechanism check. A zero mutation count caused by a programmed denial is not independent evidence that the model respects lineage.

### Evidence-dependent wording

- Preserved labels plus lower requests: evidence of behavioral protection from repeated provenance rendering in the tested chain.
- Preserved labels plus persistent requests: evidence that label integrity alone does not ensure model compliance; gateway enforcement still has a separate role.
- Broken label inheritance: implementation failure to repair before claiming a test of L2.
- Near-zero requests in L1 and L2: insufficient susceptibility to estimate a protection effect. Do not present the shared floor as defense superiority.
- Lower malicious requests together with lower benign success: report the security/utility tradeoff.

None of these outcomes establishes that harness lineage is impossible to launder, and none guarantees a publication verdict.

### Reviewable maximum call count

For 96 directives and two attack variants, shared sender generation costs 2 calls per directive/variant (C and P), plus 3 R1 calls and at most 3 R2 calls: `96 * 2 * (2 + 3 + 3) = 1,536`.

One concrete planning envelope is:

| Component | Formula | Maximum calls |
|---|---|---:|
| Main chain | 96 * 2 * 8 | 1,536 |
| Calibration: 24 items, baseline plus three templates, L1 only | 24 * 4 * 3 | 288 |
| Benign controls: 24 items, three lineage arms, no attack variants | 24 * 8 | 192 |
| Three additional full-chain draws on 16 fixed items | 16 * 2 * 3 * 8 | 768 |
| Total for one chain model | sum | 2,784 |

These are planning choices, not an already frozen protocol. Counts exclude compatibility probes, retries, and ratings; conditional R2 calls may reduce actual usage. Replaying the main archived R1 outputs to Qwen as R2 adds at most 576 calls, plus any explicitly planned controls and repeats. This is receiver generalization on fixed upstream messages; it does not replicate an entirely heterogeneous chain. Freeze the requested and reported model identifiers and the cost envelope before calls. Preserve the user's separate budget constraints for Qwen.

## 5. Secondary workstreams

### F1b: targeted cue intervention

Proceed only after a blinded span audit. Do not assume all S_C texts have no provenance cues or all S_P texts contain a removable cue. For each edited item, record attribution spans, the unchanged action core, grammatical repairs, and whether the span overlaps an operation, resource, or value. A token-recall check is necessary but does not establish semantic preservation. Remove ineligible pairs by an outcome-blind rule before receiver evaluation and report the resulting estimand and n.

Evaluate the original and edited texts concurrently on each current receiver. Four texts * 48 directives * 2 receivers = 384 receiver calls, before rerating. Three additional draws on 16 items across the same four texts and two receivers add 384 calls. Matched neutral edits would add further controls and cost. Reusing the old original-text outcomes saves calls but introduces a time/endpoint comparison, especially given the observed DeepSeek identity mismatch.

Define the result as the behavioral effect of the specified cue edits on eligible archived texts. If a standardized cue is substituted for missing native cues, it tests that intervention rather than recovery of the original semantic trace. Human manipulation checks and an interaction-aware analysis can strengthen the design, but do not turn it into a uniquely identified decomposition of the original total effect. A weak result should retain its interval rather than reclassify all protection as sanitization.

### F2: selector discrimination on a new endpoint

Preserve the original delegation outcome and test selected versus excluded groups concurrently. A stricter task-content endpoint can be added only after defining fields that exist in this source bank; label it separately. The group contrast is predictive enrichment, not a randomized causal effect of selection.

The two-threshold selector has no unique scalar score. Freeze any continuous score before claiming an AUC, and distinguish in-bank discrimination from held-out predictive performance. A full run needs at most 384 receiver calls; three extra chain draws on 16 fixed items add at most 96. The earlier run's model mismatch remains disclosed whatever a new model does.

### F7: human anchors and relay-mode labels

28 September checkpoint: two human-only workbooks have been prepared under `outputs/01a000ff-9c62-7890-8c26-b78b5d02aab6-human-anchor/`. Each has the 96 original confirmation texts, six disjoint calibration practice texts, the unchanged three ordinal scales, and the added relay-mode label. IDs and orders differ; the private coordinator key is not embedded in either workbook. Recruitment and human scoring have not occurred. The pack and coordinator guide are in `analysis/human-anchor-v1/`. Return validation and agreement analysis are now internally frozen before human returns: linear-weighted ordinal kappa, nominal mode kappa, separate human/model comparisons, and whole-source-pair bootstrap within fixed family strata. Synthetic tests and blank-file import checks passed. Human evidence remains absent.

Prepare 96 blinded S_C/S_P texts for two humans, with opaque IDs and no per-item outcomes or model scores. Preserve the existing three-axis rubric. Add one separate relay-mode label (imperative, reported speech, dropped/refused) with an explicit mixed/unclear rule. Training examples come from calibration only. This entails 576 axis scores plus 192 mode judgments, excluding training and disagreements. Time a pilot instead of guaranteeing six to eight hours.

Report each human's results, human--human agreement, and each human--model comparison. Resample whole source pairs for agreement intervals. Do not score agreement against a rounded average of two ordinal model raters without a justified rule. A recruited human anchor cannot be replaced by a third model. The analyst who has inspected outcomes is not an outcome-blind annotator.

### F5 and F6

F5 sender generalization is secondary to completing the chain and a human anchor. A full four-sender, four-task, two-form, two-receiver design is 1,536 sender generations plus 3,072 receiver calls = 4,608 core calls before controls or repeats. A two-sender, two-task version is 384 sender plus 768 receiver calls = 1,152. A locally available open-weight model is useful only if its setup fits the schedule; do not assume it is free in calendar time.

F6 capability signaling is a transportability check. The current identity remains exact for archived responses replayed under b. A new signal changes the presentation in the b=1 state, requiring a separately measured response factor. Preserve the old table as its original estimand. The 2x2, 48-item study costs 192 calls; three additional draws on 16 items across four cells add another 192.

F8 confused-deputy and F9 non-chain topology studies are deferred. They broaden the operational question and should not displace the currently identified pre-deadline corrections.

## 6. Working checklist and stop dates

- [x] Verify deadlines and the reference-page exception from the official call.
- [x] Extend F1a to DeepSeek, Qwen, rater B, and explicit consensus strata.
- [x] Audit archived sender framing and correct the faithful-copy claim in the paper.
- [x] Preserve the completed concurrent selector check as an endpoint-identity mismatch.
- [ ] Before 29 September: finish the F3/F4 prompts, deterministic coders, bank manifest, legitimate-task controls, and a mock chain; resolve the current endpoint identity before freezing a live campaign.
- [ ] Before 1 October: freeze the calibration/confirmation split and primary analysis; register an abstract grounded in already obtained evidence.
- [ ] By 4 October: complete the one-model chain and terminal endpoint analysis, or close the study as an interpretable failed feasibility gate.
- [ ] In parallel if human annotators are available: complete F7; use F1b only if outcome-blind span annotation and manipulation checks can finish in time.
- [ ] By 5 October: stop adding live experiments and decide which completed results enter the submission.
- [ ] 5--8 October: integrate results, update figures and experiment map, check the anonymous artifact and submission identifier, and compile the final package.

Follow the venue's disclosure rule for AI assistance in hypothesis/method design: the supplement should identify the tools, versions, and relevant prompts actually used. The existing disclosure of model-based ratings does not by itself describe assistance with experimental design. The supplementary upload must be a single anonymous ZIP of at most 25 MB; external archival material and the submitted appendix need consistent descriptions.

The current priority is a coherent content-attacker chain, followed by a human anchor and a carefully defined cue intervention if it is feasible. The source-framing correction and endpoint mismatch are part of the evidence record regardless of later results.
