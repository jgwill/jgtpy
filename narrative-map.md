# Narrative Map

## Commit Timeline

- e4b6746: applying previous commit introducing CLI docs and main entry point.
- b440b49: add example scripts for each CLI
- 3956666: Applying previous commit introducing example READMEs.
- 5d69b85: Applying previous commit introducing extended examples and CLI docs.
- 0837331: feat(cli): allow fresh and notfresh flags together
- bb1a509: test: ensure relaxed fresh argument

These changes allow passing `-new` and `-old` simultaneously without argparse errors. The parsers now use a relaxed helper so jgtapp can default to fresh when needed.
