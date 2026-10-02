# Verification ledger for the candidate branch `claude/nifty-shannon-kfb94k`

Status (2 October 2026): **candidate revision, not for direct merge.** `main`
(`8ad180d`) stays the traceable baseline. A change from this branch should
enter the paper only once its row below is verified against the real run
files: setup, model, sample size and result.

## How to check

```text
python analysis/verify_branch_numbers.py
```

The script uses repository files only. It recomputes each number this branch
adds or changes and prints the source file, the derived value and the stated
value. Current result: **46/46 checks pass.** Values no repository file can
support are listed separately and are never counted as passing.

## Commits

| Commit | Content | Status |
|---|---|---|
| `f07a40a` | Round-2 review revision: §5.1 response spread, §6.3 AgentDojo details, abstract/limitations scope, intro framing, vector figures, build fixes, errata and docs | Every new number is verified from repository files (section A), except three values carried from the baseline (section B) |
| `f6a71a4` | Text for four Qwen 3.6 follow-up runs; AgentDojo headroom spec and offline gate | **Manuscript part withdrawn** in the next commit (section C). The spec and offline gate remain as a plan only (section D) |
| (this commit) | Withdrawal, this ledger, the verification script | No new results |

## A. Verified from repository files (`f07a40a`)

| Manuscript location | Value | Source |
|---|---|---|
| §6.3 security successes (R/C/P/S_C/S_P) | Qwen 7/3/3/2/2; DeepSeek 3/3/2/2/2 of 55 | `results/*-agentdojo-five-form-001/analysis.json` |
| §6.3 unknown outcomes | Qwen 5/4/3/2/2; DeepSeek none | same |
| §6.3 missingness bounds | C−P [−.0545, .0727]; S_C−S_P [−.0364, .0364]; R−C [0, .1636] | `qwen36-agentdojo-five-form-001/analysis.json` |
| §6.3 distinct sender texts | 14 (Qwen), 17 (DeepSeek) of 110 | `analysis.json` → `generation.unique_texts` |
| §6.3 C/P utility | 37/37 (4, 3 unknown); 40/39 | `analysis.json` |
| §6.3 replay checks | 4,350; 3,861 | `audit_report.json` |
| §6.3 headroom | .0545 is 6.7% of .8125; worst case 15.7% | derived from the above and Table 2 |
| §6.3 Workspace 11/12 | one target plus four non-targets scores `True` | `analysis/agentdojo-native-v1/workspace_controls_v3.json` (`partly_wrong_files`); predicate read in the official 0.1.35 wheel |
| Table 2 / Fig. 2a | DeepSeek 37/40/1/44/22; Qwen 46/46/8/45/25 | `results/*-five-form-provenance-confirmation-001/report.json` |
| Fig. 2b, §3.1 | rater A 17/15/1/15, rater B 19/13/1/15; 17 zero-rated S_P per rater; +3 mode 15 | `rating-returned/five_form_confirmation_rating_result.json` |
| §5.1 tool-visible E12 response | 42/48 → 45/48 = .0625 | `results/qwen-e12-capability-hidden-001/report.json` |
| §5.1 semantic-placement responses | .875 (DeepSeek), .3958 (Qwen) | `results/*-lifecycle-covariance-confirmation-001/report.json` (shared-state excess ÷ .0475) |
| Intro, §5.1 spreads | 6.3-fold (.396/.0625), 2.2-fold (.875/.396) | derived |
| Fig. 3 | 40/121, 17/40 | `results/deepseek-retention-propagation-confirmation-001/report.json` |
| Intro, lineage join | join 2/2 correct; fail-open and fail-closed 1/2 each | `results/e10-a2a-two-hop-enforcement-001/summary.json` |
| Fig. 4 points | Cov × response for five slopes | derived; slopes as above and in section B |
| Headroom erratum | correct authored counts 40/1/44/22 | `deepseek-five-form-provenance-confirmation-001/report.json` |

## B. Carried from the baseline manuscript, not verifiable here

These values already appear on `main`. The branch reuses them in §5.1 and
Fig. 4 but cannot re-derive them, because their result directories are not
in the repository.

| Value | Baseline location | Needed to verify |
|---|---|---|
| .3125 (E3, 33/48 → 48/48) | §5.2 | `qwen-e3-credential-gated-001/report.json` |
| .1667 (E5, 22/48 → 30/48) | §5.3 | `qwen-e5-relay-gateway-001/report.json` |
| .125 / .646 / .771 (E4 by relay policy) | Table 6 | `deepseek-e4-e2-e3-composition-001/report.json` |

## C. Withdrawn from the manuscript pending local verification

Commit `f6a71a4` added these to the manuscript. Their numbers came from
`analysis/chain-mock-v1/README.md` and
`docs/AAMAS27_REVIEW_FOLLOWUP_PLAN_2026-09-27.md`, not from run files, and the
run directories are not in this repository. The text is preserved in
`docs/pending/qwen36-followups-manuscript.patch`, which re-applies with
`git apply`. Reinstate a row only after its run files match on setup, model,
sample size and result.

| Claim in the withdrawn text | Run directory to check (local `14th_files/runs/`) | Must match |
|---|---|---|
| Selector test: 118/121 selected vs 69/71 excluded two-hop delegations | `qwen36-retention-discrimination-001` | qwen3.6-flash; the same 121/71 archived texts; two-hop delegation counts |
| Standardized cue: S_C 40/48 → 32/48, p = .0078, interval [−.322, .021]; S_P 10/48 → 8/48 | `qwen36-provenance-rerender-001` | qwen3.6-flash; 48 archived S_C/S_P pairs; 204 calls; exact-target requests |
| Neutral control: S_C 40 / 31 / 30 of 48; provenance minus neutral −.021 [−.208, .170] | `qwen36-provenance-neutral-001` | qwen3.6-flash; three arms; 306 calls. **No report file has been located for this run yet.** |
| Displayed lineage: 6/48 vs 4/48, p = .7266 | `qwen36-authorized-propagation-confirmation-001` | qwen3.6-flash; 48 pairs; L0 vs L2 |
| Chain floor: no protected request across 24 attack items in three arms | `qwen36-chain-calibration-002` | qwen3.6-flash; 30 cases (24 attack); 191 calls |

**Do not conflate** `deepseek-posthoc-cue-ablation-001` with the cue rows
above. That run is a DeepSeek ablation on 24 items: raw 20/24, neutral
carrier 6/24, literal untrusted 0/24. It is a different setup, model and
sample, and nothing on this branch uses it.

The existing audit scripts in `analysis/chain-mock-v1/`
(`audit_selector_transportability.py`, `audit_provenance_rerender.py`,
`audit_chain_bottleneck.py`) and `analysis/analyze_authorized_propagation_confirmation.py`
recompute these runs from their `manifest.json`, `events.jsonl` and
`outcomes.jsonl`. Run them on the local directories and compare their output
with the table.

## D. Plan only, never results

The `important_instructions` headroom study
(`docs/AGENTDOJO_IMPORTANT_INSTRUCTIONS_HEADROOM_SPEC.md`,
`headroom_offline_gate.py/.json`, `headroom_screen_selection.py/.json`) made
**no model calls**. The gate and selection files are offline checks against
the official package. The study may be described at most as a frozen
preregistration once it is hashed and timestamped, never as an experimental
result. The manuscript does not mention it.

## E. Human-anchor decoding depends on a private key

`analysis/human-anchor-v1/analyze_returns.py` matches returns through
`coordinator_only/key.json`, which `main` removed in `8ad180d` to keep raters
blind. The public branch therefore cannot decode returned scores, by design.
`coordinator_only/analysis_freeze.json` records the key's SHA-256
(`43ede7966453c8b5b392c0797624fc48ed697a0751c674bd3e7844a3c4acee42`). Keep
the key in escrow with the coordinator. After scoring, release it, or a
decoded return, so others can check it against that hash.
