# DISPATCH

Prompts autocontidos gerados pelo Orchestrator para workers.

Convenção: `SYSTEM/DISPATCH/<TASK_ID>-<ATTEMPT_ID>.md`.

Um dispatch é imutável após a tentativa ser iniciada. Mudança material gera novo `ATTEMPT_ID`.

## Required fields

Todo dispatch inclui pelo menos task/attempt, base state/SHA, Issue, role, success targets, case/production/pain/risk refs, dependencies, DRG applicability, objective/scope, evidence, quantitative targets (ou indicação de que devem ser estabelecidos pela pesquisa), adaptive-policy impact quando houver, DoD, output/result path e lifecycle requirements.

Se a tarefa decide stack/arquitetura/model/provider/parser/eval/auth/storage/deploy/observability/security, `DRG_APPLICABILITY` normalmente é `REQUIRED` e o worker deve produzir research record/benchmark sem promover a própria preferência.

## Worker lifecycle

Em protocolo 1.6.0+ o dispatch deve instruir explicitamente:

1. executar `CONTINUITY_CHECK`;
2. criar/usar branch isolada `worker/<TASK_ID>-<ATTEMPT_ID>`;
3. comentar `TASK_STARTED` na Issue antes do trabalho substantivo;
4. emitir `TASK_PROGRESS` apenas em marcos materiais quando útil;
5. persistir RESULT e artifacts/DR records exigidos;
6. comentar exatamente um terminal `TASK_COMPLETE`, `TASK_BLOCKED` ou `TASK_STALE`.

Schema e semântica em `SYSTEM/TASK_SIGNALS.md`; formatos em `SYSTEM/TEMPLATES.md`; production/decision rules em `SYSTEM/PRODUCTION_CONTRACT.md` e `SYSTEM/DECISION_RESEARCH_GATE.md`.

O usuário normalmente só precisa abrir o chat e dizer `Execute o dispatch ...`; o worker é responsável por sinais, branch e persistência.
