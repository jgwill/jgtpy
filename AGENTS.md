# Agent Operating Guide

This repository uses multiple agents to maintain natural-language specifications for the plotting utilities in `jgtpy`. The specs in `./specs` act as the source of truth for future language model implementations.

## Primary Purpose
- Document the behavior of plotting modules and helper libraries in clear prose so another developer can recreate them in any language.
- Each specification should describe required data columns, configuration objects, algorithm steps and expected outputs.
- Specs should be implementation independent: avoid Python-specific details except to clarify data flow or structure.

## Working Rules
1. When adding or updating code or documentation, also update the corresponding spec file or create a new one under `./specs`.
2. Summaries in `narrative-map.md` must reflect ongoing work with short glyph cues.
3. Every commit must include a ledger entry under `codex/ledgers` describing the change, agents involved and the scene unlocked by the new docs.
4. Run `pytest -q` after modifications to verify that tests still pass.

These notes capture how to proceed with future specification work.
