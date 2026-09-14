# AGENTS.md — Academy Suno

Estas instruções valem para qualquer chat/agente que trabalhe neste repositório.

## Regra máxima — qualidade do case

O objetivo dominante é entregar o melhor case possível segundo o **objetivo do briefing, os entregáveis e os critérios reais de avaliação**. Leia `SYSTEM/QUALITY_MODEL.md` e `SYSTEM/QUALITY_SCORECARD.md` antes de priorizar trabalho.

Velocidade e paralelismo são meios para chegar mais rápido ao melhor resultado; nunca são a função objetivo final.

## Fonte de verdade

O histórico de conversa não é fonte de verdade. Prioridade:

1. `SYSTEM/CONSTITUTION.md`
2. `SYSTEM/STATE.md`
3. `SYSTEM/QUALITY_MODEL.md`
4. `SYSTEM/QUALITY_SCORECARD.md`
5. `SYSTEM/ROADMAP.md`
6. `SYSTEM/DECISIONS.md`
7. `SYSTEM/TASK_LEDGER.md`
8. `SYSTEM/WAVES/W###.json`
9. Issues/PRs/resultados persistidos
10. `SYSTEM/KNOWLEDGE_INDEX.md`

## Bootstrap obrigatório

Antes de trabalhar, leia as fontes aplicáveis e identifique protocolo, state, SHA do main, papel e identidade da tentativa. Confirme:

```text
CONTINUITY_CHECK
protocol_version: ...
state_version: ...
main_commit_sha: ...
role: ...
task_id: ...
attempt_id: ...
orchestrator_lease: ...
quality_gap_targeted: ...
status: PASS | FAIL
```

Divergência de estado/commit => `STALE_INPUT`.

## Orchestrator

- Existe no máximo um Orchestrator autorizado por vez.
- Lease dinâmico: branch `control/orchestrator-lease`, `SYSTEM/ORCHESTRATOR_LEASE.json`.
- Antes de integração, releia lease e confirme seu `holder_session_id`.
- O Orchestrator gera automaticamente tasks, Issues e prompts/dispatches; o usuário não deve precisar escrever prompts de workers.
- Toda priorização deve apontar para um gap do Quality Scorecard, hard gate, dependência crítica ou requisito direto do case.
- Após integração material, reavalie o case completo; não confunda task concluída com melhoria suficiente.

## Workers

Workers nunca alteram arquivos canônicos. Toda tentativa declara:

- `TASK_ID`
- `ATTEMPT_ID`
- `BASE_STATE_VERSION`
- `BASE_COMMIT_SHA`
- critério/gap de qualidade alvo
- dependências, objetivo e definition of done.

Branches de trabalho são isoladas por tentativa. Resultado relevante deve ser persistido no GitHub.

## Resultado

```text
RESULT
TASK_ID: ...
ATTEMPT_ID: A##
BASE_STATE_VERSION: ...
BASE_COMMIT_SHA: ...
QUALITY_GAP_TARGETED: ...
STATUS: COMPLETE | PARTIAL | BLOCKED | STALE
CONFIDENCE: 0-100

FINDINGS:
- ...
EVIDENCE:
- ...
QUALITY_IMPACT:
- critério afetado: ...
- impacto esperado: ...
STATE_DELTA_PROPOSED:
- ...
DECISIONS_PROPOSED:
- ...
OPEN_RISKS:
- ...
ARTIFACT_REFS:
- ...
NEXT_ACTIONS:
- ...
```

## Paralelismo

Tarefas independentes devem rodar em paralelo. O Orchestrator usa DAG/ready queue e micro-fan-in para liberar dependentes assim que possível.

## Checkpoints

Todo incremento de `STATE_VERSION` exige snapshot idêntico em `SYSTEM/CHECKPOINTS/STATE-v####.md`. Checkpoints antigos são append-only.

## Drift e decisões

Decisão `LOCKED` só muda via `DECISION_REVIEW`. A rubrica de qualidade também não pode ser rebaixada para facilitar aprovação.

## Critério de término

Nenhum agente declara o projeto concluído por completude operacional. Finalização exige `QUALITY_STATUS: PASS`, `STOP_CONDITION: PASS`, hard gates atendidos e revisão final contra briefing/entregáveis.
