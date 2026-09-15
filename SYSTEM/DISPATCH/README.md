# DISPATCH

Prompts autocontidos gerados pelo Orchestrator para workers.

Convenção: `SYSTEM/DISPATCH/<TASK_ID>-<ATTEMPT_ID>.md`.

Um dispatch é imutável após a tentativa ser iniciada. Mudança material gera novo `ATTEMPT_ID`.

## Required fields

Todo dispatch inclui pelo menos task/attempt, base state/SHA, Issue, role, success targets, dependencies, objective/scope, evidence, DoD, output/result path e lifecycle requirements.

## Worker lifecycle

Em protocolo 1.6.0+ o dispatch deve instruir explicitamente:

1. executar `CONTINUITY_CHECK`;
2. criar/usar branch isolada `worker/<TASK_ID>-<ATTEMPT_ID>`;
3. comentar `TASK_STARTED` na Issue antes do trabalho substantivo;
4. emitir `TASK_PROGRESS` apenas em marcos materiais quando útil;
5. persistir RESULT;
6. comentar exatamente um terminal `TASK_COMPLETE`, `TASK_BLOCKED` ou `TASK_STALE`.

Schema e semântica em `SYSTEM/TASK_SIGNALS.md`.

O usuário normalmente só precisa abrir o chat e dizer `Execute o dispatch ...`; o worker é responsável por sinais, branch e persistência.
