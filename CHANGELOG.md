# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Allow `--fresh` and `--notfresh` flags together via `add_use_fresh_argument_relaxed`.
- Updated CLI modules to use the relaxed parser.
- Packaged service scripts so guidecli can list them when installed.
 - Updated CLI imports to mirror the package style using `from cli_utils import ...`.
