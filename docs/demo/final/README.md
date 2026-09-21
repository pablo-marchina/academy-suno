# Final paced demo — W004-T019

This directory documents the evaluator-facing final browser capture produced by `W004-T019-A01`.

The capture intentionally shows two different source-trust outcomes in this order:

1. a genuine recipient-facing text input reaching `SOURCE_READY / PASS`, with exact input SHA-256, all 9/9 3×3 mechanics cells, persisted `FAIL → repair → PASS` evidence and explicit non-claims;
2. the real public Banco Central do Brasil PDF as a labelled negative-control, preserving `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` when table-role provenance is ambiguous.

The BCB path is not bypassed or promoted merely to create a green demo. The recording keeps `MECHANICS_ONLY`, `DIAGNOSTIC_ONLY`, `PRODUCTION_UNKNOWN/BLOCKED`, no human/provider evidence claim and no production-readiness claim visible.

The exact Actions run/artifact/hash/duration binding is added after the successful CI capture and is also persisted in `artifacts/demo_final/W004-T019-A01-ci-evidence.json` plus `SYSTEM/RESULTS/W004-T019-A01.md`.
