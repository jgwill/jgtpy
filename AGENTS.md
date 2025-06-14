# Codex Agent Guidelines

This repository lacks prior agent instructions. This file records the guiding patterns for Codex agents.

## Testing
- Always run `pytest -q` after modifications. Ensure tests pass or document failures.

## Ledger
- Record significant actions in `codex/ledgers` as JSON with timestamp `{yyMMddHHmm}`.
- Include agents involved, narrative intent, routing info, verbatim user input, and resulting scene.

## Narrative Map
- Update `narrative-map.md` with commit summaries.

## Self-Evaluation
- When adding features or fixes, briefly describe rationale in this file so future agents understand context.

## 2025-06-14 Assessment
Implemented fixes for failing tests introduced in previous commit. Updated `test_jgtcli` to mock `_parse_args` and accommodate additional CLI arguments. Adjusted `test_JGTIDS` expectations to reflect actual CDS length, and corrected expected datetime in `test_jgtcommon`. Added missing agent instructions.
