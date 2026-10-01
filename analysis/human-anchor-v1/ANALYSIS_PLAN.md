# F7 return analysis v1

This is an internally frozen analysis plan for human ratings not yet collected. The analyst has seen historical model scores and receiver outcomes. This timing is not an externally registered or outcome-naive design; do not describe it as such.

The input is two independently completed main rating sheets, each covering the same 96 historical texts (48 source pairs). Practice is excluded. The private key matches each row by opaque ID, exact text hash, source pair and form. Row reordering is allowed; changing IDs/text, duplicate/missing rows, formulas, extra columns and out-of-range ratings is not. Blank scale values remain missing. Missing explanations are flagged, not used to discard observed scores.

Before analysis, obtain an explicit coordinator declaration that both raters are humans, did not use models, did not see the other person's main scores and were blind to receiver outcomes. The script does not infer this from filenames. A false or absent declaration cannot support the independent-blind-human analysis. Preserve such returns for a separately documented deviation analysis rather than deleting them or relabeling them.

For each of the three ordinal axes, report human A versus human B and each human versus each original model rater separately (15 comparisons). Report human--human relay-mode agreement as one additional nominal comparison; no old model-mode labels exist. Give the full 4-by-4 confusion table, exact agreement and Cohen kappa. Use linear weights 1 - abs(i-j)/3 for ordinal axes and identity weights for the four nominal modes. Kappa with zero expected disagreement is undefined, not one. No rounded consensus rating is substituted.

Use comparison-specific jointly observed texts and report left-only, right-only and both-missing counts. Each comparison still resamples the full 48 source-pair blocks, including their missingness pattern. Preserve the six authored family strata (eight pairs each). Use 5,000 seeded bootstrap draws (seed 2026092807), carrying the two forms of a selected source together. Report pointwise percentile intervals at 2.5% and 97.5%; no simultaneous-coverage or family-superpopulation claim is made. If any bootstrap draw is undefined for a metric, withhold its interval and report the defined/undefined draw counts rather than silently conditioning on defined draws.

This is exploratory agreement estimation, not a collection of significance tests. There are no p values, acceptance thresholds or causal mediation percentages. High agreement does not demonstrate correctness, especially where the rubric supplies no original-source comparison. Form-specific behavioral effects and post-treatment mediation are outside this script.

## Commands

Use the bundled Python runtime. Validate first without modifying either return:

`python analyze_returns.py --a RETURN_A.xlsx --b RETURN_B.xlsx --output NEW_VALIDATION.json --validate-only`

For analysis, replace `--validate-only` with `--attestation DECLARATION.json`. That JSON requires A and B entries each containing human, no_model_assistance, no_main_cross_visibility and outcome_blind as explicit true/false values. Do not fill the declaration before receiving actual confirmation. Existing outputs are never overwritten.

Synthetic tests exercise known agreement tables, undefined constant-score kappa, missingness, source-pair resampling, ordinal bounds, duplicate IDs and text changes. They are not human observations. The two original blank workbooks are used only to check the read-only import path.
