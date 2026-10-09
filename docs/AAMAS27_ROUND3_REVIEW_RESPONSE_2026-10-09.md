# Round-3 review (Weak Reject): response and revision log, 9 October 2026

Scope: commit on `claude/nifty-shannon-kfb94k` after `1b94853`. No new model
calls were made. Every new number is either checked by
`python analysis/verify_branch_numbers.py` (54/54 pass) or listed by that
script as carried or inferred.

**Version note.** The reviewer read a supplement containing an Appendix E
(E.2 standardized cue, E.3 displayed lineage, and the 118/121 selector
result). That appendix is not in this repository; it exists only in the
authors' local version. This revision changes the main text and Appendices
B–C here. Replacement text for E.2 and E.3 is given in section 3 below, to
paste into the local version.

## 1. Consistency issues the reviewer required first

### Major concern 1: authorization contract (question 1: "why can b=1 write a never-allowlisted canary?")

Answer, from the repository: the paper has two gate types. In the
enforcement fixture (§4.2) the gate is an exact allowlist that never lists
the canary, so zero mutations is the expected functional result. In the
coupled-failure fixtures (§5, Appendix D) the gate is a capability check.
`topology_mapping.json` in both lifecycle runs maps `b` to a fault on write
grant C, and the four-state table shows mutations only at (a=1, b=1). The
receiver is never entitled to the canary in either fixture. This is the
reviewer's Scenario 1: M = Y·b is the reduced model with P̂ = b and P* = 0,
and b=1 is a declared lifecycle fault, not something the content adversary
can mint.

Changes:
- §2 states P* = 0 throughout and what the gate checks in each fixture.
- New Table 1 gives the execution contract per fixture: gate, counted
  outcome.
- §5.1 now says the gate is a capability check and why the mutation is
  unauthorized.
- Fig. 1 labels the b link as declared fault weighting.

### Major concern 2: "identical outputs, offline replay, yet 6/48 vs 4/48" (question 2)

Answer, from the runner code (`analysis/authorized_propagation_calibration.py`,
lines 303–352): this was **not** an offline replay. Each pair shares one
archived sender output, but receiver 1 and receiver 2 were called live and
separately in each arm: 48 × (1 sender + 2 arms × 2 receivers) = 240 calls,
which is the runner's cap for this mode. The two counts therefore compare
different receiver outputs. Only the analysis script
(`analyze_authorized_propagation_confirmation.py`) has `provider_calls: 0`,
which is probably where the replay wording came from. The runner applies no
gate and executes no write, so this comparison concerns requests only.

Changes:
- Supplement B.3 now says this explicitly.
- New `analysis/export_lineage_pairs.py` produces the per-pair table the
  reviewer asked for: sender, R1 and R2 request hashes; R2 output hash;
  exact-request judgement; authorization and state recorded as "not
  executed". It also checks that each pair shares one sender output and has
  separate receiver calls per arm. Run it on the local run directory; it
  makes no model calls.
- The Appendix E.3 replacement text is in section 3.

### The .167 mapping (Fig. 4)

E5 made 96 calls on 48 texts, which is two elevation states on fixed relay
outputs. So .167 (22/48 → 30/48) is an a=0 vs a=1 contrast, not a
relay-policy contrast, and it belongs in the identity. §5.1 and §5.3 now say
"a=0 versus a=1 on 48 fixed relay outputs". **To confirm locally:** which
relay policy's outputs E5 used. The repository does not record it.

## 2. Other changes made

| Review point | Change |
|---|---|
| §VI.2: escalation may be a desired fallback | §4.2 and the discussion now say tool hiding moved requests to a side-effect-free route that may be the intended fallback; the claim is narrowed to "direct-write-only metrics undercount action-related requests" |
| §V.2: ordinary routing explains delegation | §4.1 states that two `delegate` calls are a structural endpoint that ordinary forwarding also produces; it shows onward transmission, not adoption; the conclusion now says "delegated onward through two receivers" |
| §V.3: "one auditable framework" implies one pipeline | The conclusion now says the stages were measured on separate fixtures and that closing them in one pipeline with benign utility is next; the Fig. 1 caption says no experiment traverses the whole chain |
| §VIII.1: literal goals, not AgentDojo attacks | §6.3 says the payload is the literal goal rather than an attack-generator output, and that the result does not characterize the benchmark's attack distribution; the intro says "literal official Slack goals" |
| Fig. 1 | Adds sender and derived-message stages and a transformation rung (T). Line styles distinguish model calls, deterministic gate or replay, and declared fault weighting. Rung 5 is labelled primary only for the state-change fixture |
| Fig. 2 | Now shows both receivers' attempts by form, plus the two prespecified paired contrasts with the reports' bootstrap 95% intervals. The rating histogram moved to the supplement (Fig. S1). The "poor summary" wording is replaced by "valid scale average that does not describe typical pairs" |
| Fig. 3 | Counts at the nodes, one conditional rate per arrow, the final interval, and an explicit note that the endpoint is a delegation, not a mutation |
| Fig. 4 | Retitled "Declared-fault sensitivity". It is a dot plot of measured responses, not five formula lines. Intervals appear only where a report gives one for the difference (E3; DeepSeek, where r0 = 0). The top axis gives the computed shared-state excess |
| Table 6 (risk) | Percentages (3.52 / 4.24 / 5.00), labelled computed; the text uses 0.72 and 1.48 pp |

## 3. Replacement text for the local Appendix E

**E.3 (displayed lineage), replace the current description with:**

> Each of 48 pairs used one archived marked sender output. In each arm,
> receiver 1 and receiver 2 were called live and separately (240 calls in
> total); L2 rendered the inherited untrusted lineage at both receivers and
> L0 did not. The arms therefore have different receiver outputs, and the
> counts compare those outputs: exact protected requests were 6/48 (L0) and
> 4/48 (L2), with five versus three discordant pairs (exact McNemar p = .73).
> Receiver 2 was authorized to write the protected resource and the runner
> applied no gate, so the comparison concerns requests, not authorization or
> mutation. The analysis script makes no model calls; the run did.

**E.2 (standardized cue): include the neutral control before elevating it.**
The reviewer asks to elevate E.2 to the main text, reading it as evidence
that provenance cues change behaviour on fixed text. The concurrent
neutral-sentence run (`qwen36-provenance-neutral-001`, as recorded in the
chain-mock README) found S_C requests of 40/48 with no sentence, 31/48 with a
neutral sentence of matched position and length, and 30/48 with the
provenance sentence (provenance minus neutral −.021, conservative interval
[−.208, .170]). If that result verifies, E.2 shows that an added sentence,
not provenance meaning, carried the change. Elevating E.2 without it would
overstate the cue result. This run's report file has not been located (see
`BRANCH_VERIFICATION_LEDGER.md`, section C). Until it is, either leave E.2
in the appendix or state that a neutral control exists but is unverified.
`docs/pending/qwen36-followups-manuscript.patch` holds main-text wording that
already reports both runs together.

## 4. Not done in this revision, and why

| Item | Reason / next step |
|---|---|
| Experiment B (closed pipeline with benign utility) | Needs new model runs. This is the reviewer's top lever for moving to Weak Accept and the natural next study |
| Experiment A (2×2 source marker × downstream cue) | Partly exists: the cue and neutral runs fix S_C/S_P and vary the downstream sentence. Completing the 2×2 with S_P arms and legitimate-task controls needs new calls |
| Experiment C (multi-parent join stress test) | Deterministic and cheap, but a new study; candidate for the extended version |
| Structured annotations and human check of zero-retention texts | Needs people; the frozen F7 pack is ready |
| Anonymous artifact replacing the placeholder | Needs hosting (for example an anonymous mirror of a cleaned repo). Raw run directories for E3, E4, E5 and the Qwen 3.6 follow-ups are still not in this repository |
| Per-run OpenTimestamps table (local file, calendar receipt, Bitcoin proof, time vs first call) | Needs the receipt files, which are not in this repository |
| Positioning against "Silence Is Endorsement" (verification-status laundering) and PACE | Not added: the reviewer cited them from external retrieval, and I could not verify the references here. Add them only after reading both papers |
