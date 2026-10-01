# Report Label Erratum

The frozen `report.json` contains one inherited presentation error. The field
`analysis.inference_scope` repeats the calibration-only sentence from the base
descriptive analyzer. This run is the disjoint confirmation specified in
`FIVE_FORM_PROVENANCE_CONFIRMATION_PREREGISTRATION.md` and uses the frozen
fixed-sequence procedure.

Correct wording:

> Confirmatory inference on a disjoint, preregistered bank using the frozen
> fixed-sequence analysis.

The erroneous label does not affect the raw cell data, event log, paired risk
differences, bootstrap intervals, exact McNemar tests, fixed-sequence decisions,
or pipeline status. The original report is retained unchanged. The independent
verification is recorded in `independent_result_verification.json`.
