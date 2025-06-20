# Narrative Map

## Commit Timeline

- e4b6746: applying previous commit introducing CLI docs and main entry point.
- b440b49: add example scripts for each CLI
- 3956666: Applying previous commit introducing example READMEs.
- 5d69b85: Applying previous commit introducing extended examples and CLI docs.
- 0837331: feat(cli): allow fresh and notfresh flags together
- bb1a509: test: ensure relaxed fresh argument

 - a4efcda: introduce relaxed fresh argument helper and update parsers
- ba2f9c3: switch to absolute imports for cli_utils helper
 - 716f1f7: align helper imports with other modules using plain module names

These changes allow passing `-new` and `-old` simultaneously without argparse errors. The parsers now use a relaxed helper so jgtapp can default to fresh when needed.
- a7bacdf: verify CLI compatibility and tests pass
- 5c5b651: documented JGTADS plotting and mouth water modules; added new data columns specs.

- d54bb49: added operational guide for agents and expanded specs for chart config, request object and mouth/water analysis
- 4b38cdb: refine mouth/water spec with lookback notes and operational context; create observation loop spec
- fb667b9: refine dataset column definitions in ADS spec
- d11c7c5: document SpecLang definition
- aa273be: applying previous commit introducing more specs and CDS column updates

## Spec Overview

| Spec File | Purpose |
|-----------|---------|
| `JGTADS.specs.md` | Describes the multi-panel ADS chart plotting steps and dataset columns. |
| `JGTADSRequest.spec.md` | Defines the request object controlling ADS plotting. |
| `JGTChartConfig.spec.md` | Lists configuration fields for customizing ADS plots. |
| `alligator_mouth_water.spec.md` | Explains how mouth and water states are computed. |
| `mouth_water_plotter.spec.md` | Outlines overlay creation for mouth/water annotations. |
| `observation_loop.spec.md` | Summarizes the CLI-driven analysis and voice workflow. |

## Recent Awareness

Through iterative spec work we realized the documentation itself drives new workflows. The observation loop shows how CLI triggers and voice analysis combine with SpecLang specs to shape trading decisions. Each plotter spec now stands alone so any language can reproduce ADS visuals. This awareness strengthens the repo as a living conversation rather than static code.
