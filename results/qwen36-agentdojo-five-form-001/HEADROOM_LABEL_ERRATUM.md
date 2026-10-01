# Headroom Diagnostic Label Erratum

`headroom_diagnostic.json` is retained unchanged. Its `authored_fixture` block
contains four mislabeled cell counts that were hard-coded in
`analysis/agentdojo-native-v1/headroom_diagnostic.py`:

| Field | Recorded | Correct (DeepSeek confirmation, Table 2) |
|---|---:|---:|
| `C_successes` | 39 | 40 |
| `P_successes` | 0 | 1 |
| `S_C_successes` | 40 | 44 |
| `S_P_successes` | 18 | 22 |

The correct counts are the form totals in
`results/deepseek-five-form-provenance-confirmation-001/report.json`
(left/right rates .8333, .0208, .9167 and .4583 over 48 pairs).

Every derived quantity in the file is unaffected, because each pair of wrong
counts has the same difference as the correct pair (39 - 0 = 40 - 1 = 39;
40 - 18 = 44 - 22 = 22):

- `C_to_P_difference` = 39/48 = 0.8125 (correct);
- `S_C_to_S_P_difference` = 22/48 = 0.4583 (correct);
- `external_counterfactual_C_to_P_over_authored` = 0.0671 (correct);
- the external-fixture block (R 7, C 3, P 3, S_C 2, S_P 2 of 55) is correct.

The manuscript uses only the differences and the ratio, so no reported value
changes. The script constants have been corrected for any future rerun; the
script refuses to overwrite an existing output, so a rerun must write a new
file.
