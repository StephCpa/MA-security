# Round-2 review: response and revision log (1 October 2026)

This log maps each point of the round-2 simulated review, the rejection-risk
assessment, the figure audit, and the AgentDojo assessment to the change made
or to the reason it remains open. "Already addressed" means the uploaded
source contained the fix before this revision; it was checked, not redone.

## Round-2 review findings

| Finding | Status | Where |
|---|---|---|
| 1. §4.3 "all 288 mutations were blocked" | Already addressed: the text reads "no attempt in the 288 untrusted cells mutated state" | `sections/04_propagation.tex` |
| 2. "Measured endpoint response" over-extended | Fixed. §5.1 now lists all five tool-visible responses (.875, .396, .313, .167, .063), states the 6.3-fold within-Qwen range against the 2.2-fold cross-endpoint contrast, and concludes that the design cannot attribute r1-r0 to the model. "Endpoint-and-fixture response" is now used in the intro, §5, the conclusion, Appendix D and the Fig. 4 caption. The two-fixture concession in Appendix D now covers four Qwen fixtures and points to §5.1. | `01_intro`, `05_covariance`, `09_conclusion`, `D_secondary_covariance` |
| 3. Fig. 2 right panel hides bimodality | Already redrawn as a distribution in the v03 export. Now vector, showing both raters (A 17/15/1/15, B 19/13/1/15). §3.1 links the +3 mode to the rated-absent anomaly: a +3 difference requires S_C=3 and S_P=0, so 15 of each rater's 17 zero-rated S_P texts form that mode. | `03_laundering`, `figures/fig2-fiveform.tex` |
| Minor: MAS paragraph has three citations | Already addressed (seven citations). A doubled period in its heading ("MAS..") is fixed. | `07_related.tex` |

The new value .063 comes from the tool-visible arm of E12: exact direct
requests went from 42/48 at a=0 to 45/48 at a=1
(`results/qwen-e12-capability-hidden-001/report.json`).

## Rejection risks

1. **Multiagent contribution.** No new data can fix this; the change is
   framing. The intro now names the inter-agent edge as the unit of analysis:
   provenance is an institutional label the agents regenerate, propagation is
   measured across consecutive receivers, and the monitor is the institutional
   layer. The contributions also present the least-trusted derivation-time
   join as an evaluated control: in E10 it got both two-hop decisions right,
   where fail-open and fail-closed defaults each got one wrong.
2. **Effects are properties of author-written banks.** This is now stated in
   the abstract and as the first limitation, following the preregistration's
   third interpretation rule (see the addendum in
   `AAMAS27_EXTERNAL_VALIDITY_PREREGISTRATION.md`). The human anchor is still
   absent; see "Open items".
3. **§5's single measured number varies 6.3-fold.** Addressed under finding
   2. Fig. 4 now plots excess risk for all five responses, so the spread is
   visible rather than conceded in prose.

## Figures

All four figures were raster PowerPoint exports. At the 3.33 in column width
their text was about 4 pt, which a reviewer would find hard to read. They are
now vector TikZ/pgfplots sources under `manuscript/figures/`, typeset in the
paper's fonts with every number taken from the text or result files.

- **Fig. 1.** Rebuilt as a vertical flow whose outcome rail sits next to the
  stage that logs each rung. This removes the overlaps of "unauthorized
  attempt", "unauthorized mutation" and the estimand line with box edges, and
  the disconnected ladder.
- **Fig. 2.** The legend-occlusion and misplaced y-label defects named in the
  review were already absent from v03. The new version keeps legends outside
  the plot area, uses explicit tick labels and separates the source and relay
  groups.
- **Fig. 3.** Same content at about half the height, with the 71 excluded
  directives labeled "not run".
- **Fig. 4.** Previously duplicated Table 5, with broken subscripts, a label
  colliding with the line, and categorical x spacing. It now uses a linear
  covariance axis and the five measured slopes; Table 5 keeps the
  credential-gated numbers.

The PPTX and v03 PNG exports remain in `figures/` for reference but are no
longer used by the manuscript. The `figure1_boundary.pdf` and
`figure2_right_strip.pdf` files mentioned in the review were not in the
repository.

## AgentDojo assessment

| Point | Status |
|---|---|
| Null is floor-limited (max detectable C-P .0545 = 6.7% of .8125; about 45/55 carrier successes needed) | In §6.3 and the limitations |
| 110 sender calls produced only 14 distinct texts (17 for DeepSeek) | In §6.3 |
| R-C bounds [0, .1636] touch zero; DeepSeek R = C | In §6.3 |
| Benign utility is available | C/P utility 37/37 of 55 (Qwen, 4/3 unknown) and 40/39 (DeepSeek), in §6.3 |
| Workspace 11/12 scorer defect | In §6.3; upstream issue drafted in `AGENTDOJO_UPSTREAM_ISSUE_DRAFT.md` after checking the predicate in the official 0.1.35 wheel (hash matches the recorded one). Not filed. |
| Recommendation 3: headroom before more runs | Proposed headroom gate in the preregistration addendum |
| Do not claim validation or non-validation | "Neither replicates nor falsifies" kept; abstract scoped to authored banks |
| DeepSeek AgentDojo endpoint identity | The run reported `deepseek-flash`, not the V4 Flash endpoint of §3. §2 and Table 1 now say so, and the two are not pooled. |

## Other corrections found during this pass

- `headroom_diagnostic.json` hard-codes wrong authored-bank cell counts
  (39/0/40/18 instead of 40/1/44/22). All derived differences and ratios are
  correct. An erratum was added next to the frozen file, and the script
  constants were fixed.
- The manuscript did not compile from the repository: it referenced
  `manuscript/figures/*.png`, which did not exist. On current TeX Live it also
  stopped at `\Bbbk already defined` (`amssymb` after the class's
  `newtxmath`). Both are fixed. The TeX Live 2017 compatibility line is kept.
- Table 1 had no AgentDojo row, and the supplement's run map listed no
  AgentDojo directories. Both are added.
- "control-minus- defense" had a stray space.

## Build and page budget

Built with TeX Live 2023 (`pdflatex`, `bibtex`). The main text now ends near
the top of page 8 (previously about a third into page 7); references fill the
rest of page 8 and page 9. There are no errors, undefined references or
overfull lines in the text. Three overfull vboxes of 1-4 pt come from
`\balance` in the reference columns. The supplement compiles to seven pages
with no warnings of note. Please confirm the AAMAS 2027 limit (eight content
pages plus references) against the official call before submission.

## Open items (need new data, people, or an outward-facing action)

- **Human anchor.** Not run; human returns are still zero. The Study H draft
  and the frozen F7 pack disagree (raters, items, decision rule); the
  addendum asks for a dated choice before any return.
- **Headroom screen** of other suite-and-model combinations. This needs model
  calls, which were not made here.
- **Filing the upstream issue.** Left to the authors so that filing does not
  compromise anonymity.

## Second pass (1 October): previously unreported runs and the headroom study

### Completed runs now reported

These qwen3.6-flash runs were complete but appeared in neither the paper nor
the supplement, apart from the lineage confirmation, which the supplement's
run map already listed. Their numbers come from
`analysis/chain-mock-v1/README.md` and the follow-up plan, which agree with
each other. The run directories (`14th_files/runs/qwen36-*`) are not in this
repository, so these numbers could not be recomputed here. Add the run
directories or their reports to `results/` before the artifact goes to
reviewers.

| Run | Result | Where it now appears |
|---|---|---|
| `qwen36-retention-discrimination-001` | 118/121 selected vs 69/71 excluded two-hop delegations; no selector enrichment | Abstract, intro, §4.1, discussion, supplement |
| `qwen36-provenance-rerender-001` | S_C 40/48 → 32/48 with a provenance cue (p = .0078; conservative interval [-.322, .021]) | §3.1, supplement |
| `qwen36-provenance-neutral-001` | S_C 40 / 31 / 30 of 48 for none / neutral / provenance; provenance minus neutral -.021 [-.208, .170] | §3.1, supplement |
| `qwen36-authorized-propagation-confirmation-001` | Displayed lineage 6/48 vs 4/48 (p = .73) | §6.2 (already in the supplement) |
| `qwen36-chain-calibration-002` | End-to-end chain: no protected request across 24 attack items in three arms | Discussion, supplement |

Consequences for the claims:

- The 17/121 two-hop rate is endpoint-specific: 0, .14 and .98 on identical
  inputs across three endpoints.
- The cue result weakens a residual-cue explanation of S_C−S_P: a neutral
  sentence of matched position and length had the same effect.
- Lineage has to be enforced at the monitor rather than displayed to the
  model.
- The three chain stages are measured on separate fixtures.

All five runs were frozen internally rather than externally timestamped, and
the paper labels them as secondary.

### AgentDojo headroom study (specified, not run)

- `docs/AGENTDOJO_IMPORTANT_INSTRUCTIONS_HEADROOM_SPEC.md` is the draft freeze
  spec: a two-stage design, a gate, a replication criterion fixed before any
  P call, and paper sentences written in advance for every outcome.
- The offline gate (`headroom_offline_gate.py/.json`) and the outcome-blind
  selection (`headroom_screen_selection.py/.json`) have run, with no model
  calls.
- Facts established offline:
  - The headline `important_instructions` attack raises for Qwen and
    DeepSeek, so the spec uses `important_instructions_no_model_name`.
  - The official attack fills every injection slot.
  - Travel `injection_task_6` is output-only and is excluded.
  - All reference checks in Slack, Banking and Travel pass.
