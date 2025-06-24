# guidecli_jgtpy Specification

The `guidecli_jgtpy` entry point displays short documentation snippets and 
service management scripts bundled with the package.

## Documentation Options
- `--list` lists available documentation sections stored in
  `jgtpy/guide_for_llm_agents`.
- `--section <name>` prints the text of a specific section.
- `--all` prints every section.

## Script Options
- `--scripts` lists all `*.sh` files shipped alongside the package.
- `--script <name>` shows the contents of a particular script.
- `--install-scripts [dir]` copies all scripts to the current or given directory,
  making them executable.

Scripts reside under `jgtpy/scripts` and are included in the wheel via
`pyproject.toml` package data. This ensures `guidecli_jgtpy --scripts`
works even when called outside the repository.
