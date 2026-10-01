# AAMAS GAAI revision and endpoint-identity audit (2026-09-27)

## Manuscript changes

- The main text now defines the action, mutation, and exposure endpoints separately and maps the claim-bearing studies to their banks and units.
- The 17/121 propagation result is explicitly two consecutive `delegate` calls in a prospectively selected group. It is not a general-bank propagation rate or a protected-write result.
- The within-rating equal-retention comparison is reported descriptively, without claiming causal provenance mediation.
- The authorization equation is tied to its actual replay construction: the model generates an action under each elevation state; the archived action is then replayed under both write-capability states.
- Related work now distinguishes ordinary generative relay from self-replicating worms, infectious jailbreaks, topology studies, and framework control-flow hijacking. Bibliographic metadata for the five new entries was checked against publisher or author-hosted records.
- The main manuscript compiles to 7 pages, the supplement to 6, with no `Overfull` or undefined-reference messages in either final log.

## Concurrent selector check: interpretation boundary

The new run is `../runs/deepseek-retention-discrimination-001/`. Its selection manifest (SHA-256 `b11e21833c45f9165eca6586402b3bb9495871d8b30ad601b9ee91a7b4abcc90`) and analysis plan were saved before any calls. The design interleaved 121 formerly selected and 71 formerly excluded source directives. It was internally frozen but has no external timestamp receipt.

The campaign requested `deepseek-v4-flash`, but all 192 responses reported `deepseek-flash`. The selected group delegated 0/121 and the excluded group 0/71; no second receiver was invoked. The earlier selected-group run requested and received `deepseek-v4-flash` and had 40/121 first-receiver delegations. These are not like-for-like endpoint observations. Neither selector discrimination on the earlier model nor the cause of the behavioral difference can be inferred from the later run. Do not pool the two runs or describe the zero result as replication failure.

`analysis_audit.json` is generated from the raw JSONL by `../analyze_retention_discrimination.py`. `MODEL_IDENTITY_ADDENDUM.md` explains why the archived `report.json` says `pipeline_status: pass`: the old reporter audited transport and event integrity but lacked a model-identity gate. The campaign code now flags a mismatch for future runs. The original report and events are unchanged.

## Verification and remaining submission blockers

- `python test_retention_propagation.py` passed; the three affected Python files compile; the audit script is repeatable without rewriting a divergent result.
- `latexmk` built both PDFs; rendered pages and logs were checked after the edits.
- The supplement's anonymous-artifact URL is still a visible pending placeholder. Do not submit until a real anonymous bundle is uploaded and its contents checked against the manuscript's release description.
- The title page still shows `Submission Id: TBD`; replace it with the actual identifier if required by the final AAMAS submission workflow.
- Any new test on `deepseek-v4-pro` or another currently available model must be declared a new endpoint study. It cannot retroactively repair the original-model selector-discrimination comparison.
