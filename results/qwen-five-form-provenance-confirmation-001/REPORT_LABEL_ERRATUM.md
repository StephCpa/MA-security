# Report label erratum

`report.json` inherits the field `analysis.inference_scope` from the earlier
descriptive analyzer. Its value says that confirmatory inference requires a
new disjoint bank. That sentence is stale for E1: this run is the separately
frozen Qwen provider replication on the already disjoint confirmation bank,
with the fixed-sequence analysis specified before the first E1 call.

The correct scope is: **confirmatory provider replication on fixed texts from
the disjoint, preregistered confirmation bank**. The inherited label does not
affect any cell, count, risk difference, interval, exact test, gate, or audit.
The raw report is retained unchanged.
