# SYSTEM CONSTITUTION

`PROTOCOL_VERSION: 1.1.0`

## 1. Purpose

Este documento define o protocolo de operação do projeto Academy Suno. Ele existe para garantir continuidade entre chats, paralelismo máximo, rastreabilidade e recuperação exata após interrupções ou rotação de contexto.

## 2. Invariantes

1. O GitHub é a fonte de verdade; memória de chat é apenas cache.
2. `SYSTEM/STATE.md` representa o único estado canônico corrente.
3. Somente o Orchestrator altera arquivos canônicos.
4. Workers nunca integram suas próprias conclusões ao estado.
5. Toda tarefa tem `TASK_ID` e `BASE_STATE_VERSION`.
6. Toda decisão relevante recebe `DECISION_ID`.
7. Nenhuma decisão `LOCKED` é substituída silenciosamente.
8. Tarefas independentes devem ser paralelizadas.
9. Resultados baseados em estado antigo são tratados como potencialmente stale.
10. Nenhuma fase avança sem satisfazer seu gate no roadmap.
11. Toda wave termina em commit lógico: integrar ou manter o último estado válido.
12. O projeto só termina quando os critérios de conclusão do roadmap e do deliverable estiverem satisfeitos.
13. Alterações ao sistema canônico devem passar por Pull Request e pelo check automático `System Integrity`.
14. `main` deve permanecer protegido contra mudanças não validadas e force-push.

## 3. Papéis

### Orchestrator

Responsável por decomposição, dependências, waves, priorização, integração, atualização canônica e decisão de avançar/retroceder.

### Researcher

Busca fatos, fontes, benchmarks, concorrentes, mercado, documentação e evidências. Distingue fato, inferência e hipótese.

### Analyst

Executa análise quantitativa/qualitativa, modelos, causalidade, trade-offs, cenários e testes de hipótese.

### Synthesizer

Consolida resultados concorrentes, resolve duplicação aparente e explicita conflitos sem decidir silenciosamente.

### Critic / Red Team

Tenta refutar a solução, identificar ausência de evidência, contradições, riscos, edge cases e perguntas de banca/stakeholders.

### Auditor

Verifica aderência a este protocolo, consistência entre estado, decisões, tasks e roadmap.

### Builder / Writer

Produz código, documentos, slides, protótipos ou outros entregáveis aprovados no estado canônico.

## 4. Identificadores

- Wave: `W###` — ex.: `W003`
- Task: `W###-T###` — ex.: `W003-T002`
- Decision: `D-####` — ex.: `D-0012`
- Evidence: `E-####` — ex.: `E-0041`
- Hypothesis: `H-####`
- Risk: `RISK-####`
- Checkpoint: `STATE-v####`

IDs nunca são reutilizados.

## 5. Lifecycle de uma wave

```text
CANONICAL STATE vN
        ↓
DEPENDENCY GRAPH
        ↓
WAVE W### CREATED
        ↓
TASKS FAN-OUT
        ↓
RESULTS RETURN
        ↓
STALE / QUALITY CHECK
        ↓
SYNTHESIS
        ↓
RED TEAM (quando aplicável)
        ↓
ORCHESTRATOR DECISION
        ↓
CANONICAL COMMIT
        ↓
STATE vN+1
```

Uma wave parcialmente executada nunca substitui o último estado canônico.

## 6. Controle de concorrência

### Escrita exclusiva

Arquivos canônicos:

- `SYSTEM/STATE.md`
- `SYSTEM/ROADMAP.md`
- `SYSTEM/DECISIONS.md`
- `SYSTEM/TASK_LEDGER.md`

Somente o Orchestrator pode modificá-los.

### Escrita concorrente

Workers devem preferir:

- comentários na Issue da tarefa;
- artefatos em caminhos únicos por tarefa;
- branches/PRs isoladas quando gerarem código ou arquivos complexos.

Dois workers nunca editam simultaneamente o mesmo arquivo canônico.

## 7. Staleness

Um resultado é `STALE` quando `BASE_STATE_VERSION < CURRENT_STATE_VERSION` e as mudanças posteriores podem afetar suas premissas.

O Orchestrator deve classificar o resultado como:

- `SAFE_TO_INTEGRATE` — mudanças posteriores não afetam a conclusão;
- `REVALIDATE` — worker deve revisar contra estado atual;
- `DISCARD` — conclusão deixou de ser aplicável.

## 8. Decisões

Status possíveis:

- `PROPOSED`
- `LOCKED`
- `SUPERSEDED`
- `REOPENED`
- `REJECTED`

Para reabrir uma decisão `LOCKED`, registrar:

```text
DECISION_REVIEW
Decision: D-####
Trigger: nova evidência / mudança de requisito / inconsistência
Evidence: E-#### ...
Action: REOPEN | KEEP
Reason: ...
```

## 9. Rotação de chat

A rotação é preventiva, não reativa.

- Orchestrator: após 6–8 waves por padrão.
- Worker: por tarefa grande ou pequeno lote fortemente relacionado.
- Synthesizer/Critic/Auditor: após 8–10 waves.

Antes de encerrar, o chat antigo gera um handoff. O novo chat só começa após `CONTINUITY_CHECK: PASS`.

## 10. Continuity Check

Qualquer novo chat deve validar:

```text
CONTINUITY_CHECK
protocol_version: ...
state_version: ...
current_phase: ...
last_committed_wave: ...
role: ...
task_id: ...
locked_decisions_seen: ...
open_blockers_seen: ...
status: PASS | FAIL
```

`FAIL` impede execução até recarregar os arquivos canônicos.

## 11. Qualidade

Toda conclusão relevante deve informar nível de confiança e separar:

- fato verificado;
- inferência;
- hipótese;
- opinião/recomendação.

Quando pesquisa externa for necessária, evidências devem incluir fonte e data quando possível.

## 12. Critério de encerramento do projeto

O projeto termina somente quando:

1. todos os gates obrigatórios do roadmap estiverem `PASS`;
2. não houver blockers críticos abertos;
3. o Red Team não tiver objeção crítica sem resposta;
4. o deliverable final tiver sido validado contra o objetivo original;
5. o Orchestrator registrar `PROJECT_STATUS: COMPLETE` em `STATE.md`.

## 13. Alteração deste protocolo

Mudanças nesta Constituição exigem:

- incremento de `PROTOCOL_VERSION`;
- decisão explícita registrada em `DECISIONS.md`;
- justificativa;
- atualização de `AGENTS.md` se o comportamento dos agentes mudar.

## 14. Enforcement no repositório

A continuidade não deve depender apenas de disciplina humana.

- `.github/workflows/system-integrity.yml` valida invariantes canônicos em PRs e pushes no `main`.
- `scripts/validate_system.py` é o validador executável do protocolo.
- `.github/CODEOWNERS` identifica os arquivos de governança e seus responsáveis.
- Mudanças nos arquivos canônicos devem ocorrer via branch + Pull Request.
- O branch `main` deve exigir o status check `validate-canonical-system` antes de merge.
- Force-push e deleção do `main` devem permanecer desabilitados.
- Se o check falhar, o estado anterior no `main` continua sendo o último recovery point válido.
