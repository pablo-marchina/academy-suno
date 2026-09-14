# SYSTEM CONSTITUTION

`PROTOCOL_VERSION: 1.3.0`

## 1. Purpose

Este protocolo garante continuidade, paralelismo, rastreabilidade e, acima de tudo, otimização contínua da qualidade do case final.

## 2. Invariantes

1. O GitHub é a fonte de verdade; memória de chat é apenas cache.
2. `SYSTEM/STATE.md` representa o único estado canônico corrente.
3. Somente o Orchestrator com lease ativo altera arquivos canônicos.
4. Workers nunca integram suas próprias conclusões ao estado.
5. Toda tarefa tem `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION` e `BASE_COMMIT_SHA`.
6. `TASK_ID + ATTEMPT_ID` nunca é reutilizado.
7. Toda decisão relevante recebe `DECISION_ID` e decisão `LOCKED` não muda silenciosamente.
8. Tarefas independentes devem ser paralelizadas.
9. Resultados baseados em estado/commit antigo são potencialmente stale.
10. Nenhuma fase avança sem satisfazer seu gate no roadmap.
11. Todo incremento de estado cria checkpoint imutável e idêntico a `STATE.md`.
12. Toda wave executável possui manifest/DAG em `SYSTEM/WAVES/W###.json`.
13. Resultado relevante deve existir no GitHub; chat não é armazenamento durável.
14. Alteração de protocolo passa por PR + `System Integrity`.
15. `main` deve permanecer protegido contra mudança não validada/force-push.
16. **A função objetivo dominante é maximizar a qualidade esperada do case final segundo objetivo, entregáveis e critérios reais de avaliação.**
17. Velocidade, quantidade de tasks e paralelismo são objetivos subordinados à qualidade final.
18. O sistema não pode declarar sucesso por completude operacional; deve satisfazer o Quality Model e os hard gates.
19. A rubrica não pode ser rebaixada/alterada para fabricar aprovação.
20. Após existir solução avaliável, o sistema deve iterar avaliação → gaps → melhoria → reavaliação até a stop condition.

## 3. Papéis

### Orchestrator
Decompõe, prioriza, gera dispatches, coordena DAG, integra, mantém lease e conduz o quality loop. Toda priorização deve maximizar impacto esperado na qualidade final.

### Researcher / Analyst / Builder
Produzem evidência, análise e artefatos direcionados a gaps/entregáveis específicos.

### Synthesizer
Consolida resultados e conflitos sem mudar critérios silenciosamente.

### Critic / Red Team
Tenta refutar a solução e revelar gaps que reduziriam avaliação real.

### Auditor / Evaluator
Verifica protocolo e avalia o case contra a rubrica/briefing; não premia complexidade sem valor.

## 4. Identificadores

`ORCH-G###`, `ORCH-G###-S###`, `W###`, `W###-T###`, `A##`, `D-####`, `E-####`, `H-####`, `RISK-####`, `STATE-v####`.

IDs nunca são reutilizados.

## 5. Lifecycle

```text
CASE CONTRACT / QUALITY MODEL
        ↓
CANONICAL STATE + MAIN SHA
        ↓
FULL CASE EVALUATION
        ↓
QUALITY GAPS / HARD GATES
        ↓
WAVE/DAG + GENERATED DISPATCHES
        ↓
PARALLEL TASK ATTEMPTS
        ↓
RESULTS + PROVENANCE CHECK
        ↓
SYNTHESIS / RED TEAM
        ↓
LEASE REVALIDATION
        ↓
CANONICAL PR + CHECKPOINT
        ↓
CI PASS + MERGE
        ↓
RE-EVALUATE FULL CASE
        ↓
STOP CONDITION? yes→FINAL / no→next gaps
```

## 6. Orchestrator lease

Lease operacional vive na branch `control/orchestrator-lease`, arquivo `SYSTEM/ORCHESTRATOR_LEASE.json`. Claim/handoff usa update com blob SHA observado; conflito significa reload/abort. Antes de integração, o holder precisa revalidar `holder_session_id`.

## 7. Proveniência e idempotência

Cada tentativa usa `TASK_ID + ATTEMPT_ID + BASE_STATE_VERSION + BASE_COMMIT_SHA`. Nova execução => novo attempt. Resultado incompatível é `SAFE_TO_INTEGRATE`, `REVALIDATE` ou `DISCARD` conforme análise de staleness.

## 8. DAG e dispatch

O Orchestrator maximiza paralelismo pelo DAG e pode usar micro-fan-ins. Todo worker liberado recebe dispatch autocontido gerado pelo sistema. Ver `SYSTEM/AUTOPILOT.md`.

## 9. Checkpoints

Novo state incrementa exatamente +1, atualiza `STATE.md` e cria checkpoint byte-a-byte idêntico. Checkpoints antigos não mudam.

## 10. Quality governance

`SYSTEM/QUALITY_MODEL.md` define a função objetivo, Case Contract, rubrica, hard gates, loop e stop condition. `SYSTEM/QUALITY_SCORECARD.md` registra a avaliação corrente.

Critérios explícitos do case prevalecem sobre preferências dos agentes. Inferências precisam ser marcadas. Score agregado nunca substitui hard gate. Rubrica material só muda por nova informação do case ou revisão explícita.

## 11. Rotação e continuity

Chats podem ser trocados preventivamente. Novo chat reconstrói contexto pelo GitHub e executa `CONTINUITY_CHECK`; Orchestrator novo também precisa adquirir lease.

## 12. Critério de encerramento

`PROJECT_STATUS: COMPLETE` só é permitido quando:

- gates aplicáveis do roadmap = PASS;
- blockers críticos = 0;
- `QUALITY_STATUS: PASS`;
- `STOP_CONDITION: PASS`;
- hard gates do Quality Model = PASS;
- Red Team não possui finding crítico aberto;
- deliverables foram revisados contra Case Contract e briefing.

## 13. Alteração do protocolo

Exige bump de `PROTOCOL_VERSION`, novo Decision ID, justificativa, atualização dos agentes quando aplicável e PR separado de mudanças de produto.

## 14. Enforcement

`.github/workflows/system-integrity.yml` + `scripts/validate_system.py` validam invariantes estáticos/diferenciais. `main` deve exigir o check `validate-canonical-system`, PR e bloqueio de force-push/deleção.
