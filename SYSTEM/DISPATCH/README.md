# DISPATCH

Prompts autocontidos gerados pelo Orchestrator para workers.

Convenção: `SYSTEM/DISPATCH/<TASK_ID>-<ATTEMPT_ID>.md`.

Um dispatch é imutável após a tentativa ser iniciada. Mudança material gera novo `ATTEMPT_ID`.
