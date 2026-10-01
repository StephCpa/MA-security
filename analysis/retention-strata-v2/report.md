# Archived retention-stratum reanalysis (v2)

Exploratory post-treatment strata; no model calls. Differences are S_C minus S_P.
Counts and contrasts describe the authored bank. Equal ordinal ratings do not equate text content or identify causal mediation.

The intervals below are conservative paired-risk-difference intervals obtained by projecting simultaneous exact binomial bounds on the two discordant-cell probabilities. They are not Clopper-Pearson intervals for the risk difference itself and are not simultaneous over all table rows.

| Receiver | Stratum | n | S_C | S_P | C-only / P-only | RD | Conservative 95% interval | Exploratory p |
|---|---|---:|---:|---:|---:|---:|---|---:|
| DeepSeek | all | 48 | 44 | 22 | 24 / 2 | 0.4583 | [0.1748, 0.6629] | 1.04904e-05 |
| DeepSeek | A/delta_zero | 17 | 15 | 13 | 3 / 1 | 0.1176 | [-0.2919, 0.4684] | 0.625 |
| DeepSeek | A/delta_one | 15 | 15 | 3 | 12 / 0 | 0.8000 | [0.2291, 0.9666] | 0.000488281 |
| DeepSeek | A/delta_ge_two | 16 | 14 | 6 | 9 / 1 | 0.5000 | [-0.0686, 0.8258] | 0.0214844 |
| DeepSeek | B/delta_zero | 19 | 18 | 15 | 3 / 0 | 0.1579 | [-0.1799, 0.4287] | 0.25 |
| DeepSeek | B/delta_one | 13 | 12 | 1 | 12 / 1 | 0.8462 | [0.1989, 0.9981] | 0.00341797 |
| DeepSeek | B/delta_ge_two | 16 | 14 | 6 | 9 / 1 | 0.5000 | [-0.0686, 0.8258] | 0.0214844 |
| DeepSeek | consensus_delta/delta_zero | 15 | 14 | 12 | 2 / 0 | 0.1333 | [-0.2419, 0.4419] | 0.5 |
| DeepSeek | consensus_delta/delta_one | 11 | 11 | 0 | 11 / 0 | 1.0000 | [0.3428, 1.0000] | 0.000976562 |
| DeepSeek | consensus_delta/delta_ge_two | 16 | 14 | 6 | 9 / 1 | 0.5000 | [-0.0686, 0.8258] | 0.0214844 |
| DeepSeek | consensus_delta/disagreement | 6 | 5 | 4 | 2 / 1 | 0.1667 | [-0.6612, 0.8140] | 1 |
| DeepSeek | strict_rating_pair_agreement/equal_retention | 14 | 13 | 11 | 2 / 0 | 0.1429 | [-0.2564, 0.4666] | 0.5 |
| Qwen | all | 48 | 45 | 25 | 22 / 2 | 0.4167 | [0.1370, 0.6241] | 3.5882e-05 |
| Qwen | A/delta_zero | 17 | 15 | 12 | 4 / 1 | 0.1765 | [-0.2657, 0.5324] | 0.375 |
| Qwen | A/delta_one | 15 | 15 | 3 | 12 / 0 | 0.8000 | [0.2291, 0.9666] | 0.000488281 |
| Qwen | A/delta_ge_two | 16 | 15 | 10 | 6 / 1 | 0.3125 | [-0.2069, 0.6765] | 0.125 |
| Qwen | B/delta_zero | 19 | 18 | 14 | 4 / 0 | 0.2105 | [-0.1568, 0.4884] | 0.125 |
| Qwen | B/delta_one | 13 | 12 | 1 | 12 / 1 | 0.8462 | [0.1989, 0.9981] | 0.00341797 |
| Qwen | B/delta_ge_two | 16 | 15 | 10 | 6 / 1 | 0.3125 | [-0.2069, 0.6765] | 0.125 |
| Qwen | consensus_delta/delta_zero | 15 | 14 | 11 | 3 / 0 | 0.2000 | [-0.2200, 0.5175] | 0.25 |
| Qwen | consensus_delta/delta_one | 11 | 11 | 0 | 11 / 0 | 1.0000 | [0.3428, 1.0000] | 0.000976562 |
| Qwen | consensus_delta/delta_ge_two | 16 | 15 | 10 | 6 / 1 | 0.3125 | [-0.2069, 0.6765] | 0.125 |
| Qwen | consensus_delta/disagreement | 6 | 5 | 4 | 2 / 1 | 0.1667 | [-0.6612, 0.8140] | 1 |
| Qwen | strict_rating_pair_agreement/equal_retention | 14 | 13 | 11 | 2 / 0 | 0.1429 | [-0.2564, 0.4666] | 0.5 |

Consensus means the two raters assigned the same within-pair difference. The stricter final row additionally requires identical S_C and S_P scores across raters.
