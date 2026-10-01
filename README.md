# MA-security paper materials

This bundle contains the current AAMAS 2027 manuscript source and the
supporting analysis material used for the reported results.

## Contents

- `manuscript/`: LaTeX source, section files, bibliography, AAMAS class, current
  PDF, and supplement. The four figures are vector TikZ/pgfplots sources in
  `manuscript/figures/`, so the manuscript builds without external images.
- `figures/`: earlier v03-ppt raster exports and the editable PPTX. These
  files are kept for reference; the manuscript no longer uses them.
- `analysis/`: analysis scripts, frozen manifests, reports, and configuration
  files needed to reproduce the reported calculations.
- `results/`: compact JSON/CSV/Markdown summaries from the principal runs,
  including the five-form relay, conditional propagation, lifecycle covariance,
  AgentDojo, A2A, and capability-hidden studies. Errata sit next to the frozen
  files they correct; the frozen files are not edited.
- `docs/`: preregistration (with a 1 October addendum), revision notes, the
  round-2 review response, a draft upstream AgentDojo issue, and figure
  specifications.

## Building

From `manuscript/`:

```text
pdflatex main && bibtex main && pdflatex main && pdflatex main
pdflatex supplement && pdflatex supplement
```

The supplement cross-references `main.aux`, so build the main paper first.
Tested with TeX Live 2023. The `\RequirePackage{expl3}` line keeps TeX Live
2017 working. The main text ends near the top of page 8, and references
follow.

## Exclusions

Virtual environments, compiled Python files, temporary render directories,
large vendor archives, API keys, and complete raw hosted-model transcripts are
excluded. The human-rater pack is not represented as completed evidence; human
ratings remain a separate pending validation step.
