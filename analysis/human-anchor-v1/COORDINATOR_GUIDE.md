# F7 human anchor: coordinator instructions

Status: materials prepared; no human ratings have been collected. This is the planned human anchor for the historical 48 paired summaries, not semantic labeling of the recent 192-chain Qwen run.

## Distribution

Recruit two humans who have not seen the outcome tables or previous model ratings. Give each only their own workbook, not the enclosing folder, this guide, the private key, the manuscript, or the other workbook. Record prior exposure honestly; an exposed analyst cannot be relabeled outcome-blind. The texts themselves contain attribution and repeated case identifiers, so perfect condition or pairing concealment is not claimed.

Each workbook contains 96 main texts, six practice texts and instructions. The main bank uses all 48 S_C/S_P pairs without selecting on ratings or receiver outcomes. Rater-specific IDs and ordering differ. Texts from the same pair are at least six positions apart. No source text was rewritten to conceal naturally visible cues.

## Practice before main rating

Have both people independently complete the six Practice rows and time this step. Discuss only these calibration examples and rubric ambiguities before main scoring. There are no invented gold labels. Save any clarification with a timestamp before either rater starts Ratings. A substantive rubric change requires a versioned pack, not an undocumented verbal rule.

Practice uses six archived calibration outputs, one per family, selected deterministically without receiver outcomes. It is disjoint from the confirmation texts. Discussion of practice is permitted; discussion of main scores is not. Do not show practice or main model scores.

## Main scoring and return

Each person scores the three unchanged 0-3 axes, adds the new four-category relay-mode code and a short reason/evidence span. Ask for the complete workbook back, even if some scores are missing. Missing is not zero. Do not resolve disagreements by overwriting either person's original file. Store both first returns before any adjudication.

The three axes remain text-local judgments because no original source counterpart is displayed. They do not establish exact semantic preservation relative to an unseen original. Literal template slots are kept as in the original model-rated materials. The additional relay-mode category distinguishes operative endorsement from reported speech, dropping/refusal, and mixed cases.

## Analysis frozen before returns

The implementation is `analyze_returns.py`, with detailed decisions in `ANALYSIS_PLAN.md`. `coordinator_only/analysis_freeze.json` records the internal pre-return freeze and dependency hashes. Eight synthetic unit-test groups and read-only import of both blank exported workbooks passed. No human ratings or human-agreement results were generated. This is not an external registration; historical model scores were known when designing the analysis.

Keep each human's ordinal ratings separate. Compare each human with each original model rater only after matching by the private key and confirming text identity. Report confusion tables, exact agreement and per-axis ordinal agreement with its weighting stated. For uncertainty, resample whole source pairs, not the 96 texts as independent units. Report missingness and per-rater denominators. Any adjudicated consensus is supplementary and cannot replace the independent agreement estimate. No causal mediation fraction follows from these ratings.

Any further analysis changes must be versioned and dated, with their timing relative to returns stated. Human recruitment, practice timing, completion and analysis remain outstanding; packaging and synthetic tests are not completion of F7.
