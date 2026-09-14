# SYSTEM CONSTITUTION

`PROTOCOL_VERSION: 1.2.0`

## 1. Purpose

Este documento define o protocolo de operação do projeto Academy Suno. Ele existe para garantir continuidade entre chats, paralelismo máximo, rastreabilidade, idempotência e recuperação exata após interrupções ou rotação de contexto.

## 2. Invariantes

1. O GitHub é a fonte de verdade; memória de chat é apenas cache.
2. `SYSTEM/STATE.md` representa o único estado canônico corrente.
3. Somente o Orchestrator com lease ativo altera arquivos canônicos.
4. Workers nunca integram suas próprias conclusões ao estado.
5. Toda tarefa tem `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION` e `BASE_COMMIT_SHA`.
6. `TASK_ID + ATTEMPT_ID` nunca é reutilizado.
7. Toda decisão relevante recebe `DECISION_ID`.
8. Nenhuma decisão `LOCKED` é substituída silenciosamente.
9. Tarefas independentes devem ser paralelizadas.
10. Resultados baseados em estado/commit antigo são tratados como potencialmente stale.
11. Nenhuma fase avança sem satisfazer seu gate no roadmap.
12. Todo incremento de estado cria checkpoint imutável e idêntico a `STATE.md`.
13. Toda wave executável possui manifest/DAG em `SYSTEM/WAVES/W###.json`.
14. Toda integração canônica termina em PR validado ou mantém o último estado válido.
15. Alterações ao protocolo passam por Pull Request e pelo check automático `System Integrity`.
16. `main` deve permanecer protegido contra mudanças não validadas e force-push.
17. Resultado relevante deve ser persistido no GitHub; chat não é armazenamento durável.

## 3. Papéis

### Orchestrator

Responsável por decomposição, dependências, ready queue, waves, priorização, integração, atualização canônica e decisão de avançar/retroceder. Precisa manter lease exclusivo de integração.

### Researcher

Busca fatos, fontes, benchmarks, concorrentes, mercado, documentação e evidências. Distingue fato, inferência e hipótese.

### Analyst

Executa análise quantitativa/qualitativa, modelos, causalidade, trade-offs, cenários e testes de hipótese.

### Synthesizer

Consolida resultados concorrentes, resolve duplicação aparente e explicita conflitos sem decidir silenciosamente.

### Critic / Red Team

Tenta refutar a solução, identificar ausência de evidência, contradições, riscos, edge cases e perguntas de banca/stakeholders.

### Auditor

Verifica aderência ao protocolo, consistência entre estado, decisões, tasks, waves e roadmap.

### Builder / Writer

Produz código, documentos, slides, protótipos ou outros entregáveis aprovados no estado canônico.

## 4. Identificadores

- Orchestrator generation: `ORCH-G###`
- Orchestrator session: `ORCH-G###-S###`
- Wave: `W###`
- Task: `W###-T###`
- Attempt: `A##`
- Decision: `D-####`
- Evidence: `E-####`
- Hypothesis: `H-####`
- Risk: `RISK-####`
- Checkpoint: `STATE-v####`

IDs nunca são reutilizados.

## 5. Lifecycle de execução

```text
CANONICAL STATE vN + MAIN SHA
        ↓
WAVE/DAG + READY QUEUE
        ↓
TASK ATTEMPTS FAN-OUT
        ↓
RESULTS PERSISTED
        ↓
STALE / PROVENANCE CHECK
        ↓
MICRO-FAN-IN / SYNTHESIS
        ↓
RED TEAM (quando aplicável)
        ↓
LEASE REVALIDATION
        ↓
ORCHESTRATOR DECISION
        ↓
CHECKPOINT + CANONICAL PR
        ↓
CI PASS + MERGE
        ↓
STATE vN+1
```

Uma wave parcialmente executada nunca substitui o último estado canônico.

## 6. Controle de concorrência

### 6.1 Escrita exclusiva canônica

Arquivos canônicos incluem `STATE`, `ROADMAP`, `DECISIONS`, `TASK_LEDGER`, checkpoints e manifests de wave. Somente o holder do lease ativo pode propor integração canônica.

### 6.2 Lease atômico do Orchestrator

O lease operacional vive fora de `main`, na branch `control/orchestrator-lease`, arquivo `SYSTEM/ORCHESTRATOR_LEASE.json`.

Aquisição/transferência usa optimistic concurrency do GitHub:

1. ler o arquivo e guardar o blob SHA;
2. validar que o lease pode ser adquirido/transferido;
3. fazer update usando exatamente o SHA observado;
4. se houver conflito, outro writer venceu; recarregar e abortar a tentativa de claim;
5. antes de qualquer integração, reler o lease e confirmar `holder_session_id`.

Não há TTL automático: rotação é explícita para evitar expiração indevida de chats longos. Ver `SYSTEM/ORCHESTRATOR_LEASE.md`.

### 6.3 Escrita concorrente de workers

Workers devem preferir Issues, artefatos próprios e branches isoladas. Dois workers nunca escrevem na mesma branch de trabalho nem em arquivo canônico.

## 7. Proveniência, staleness e idempotência

Uma tentativa é identificada por `TASK_ID + ATTEMPT_ID` e recebe `BASE_STATE_VERSION + BASE_COMMIT_SHA` no dispatch.

Um resultado é potencialmente `STALE` se qualquer uma destas condições ocorrer:

- `BASE_STATE_VERSION != CURRENT_STATE_VERSION`;
- `BASE_COMMIT_SHA` não é ancestral/compatível com o estado esperado;
- dependência da tarefa mudou;
- decisão relevante foi reaberta/superseded.

O Orchestrator classifica como `SAFE_TO_INTEGRATE`, `REVALIDATE` ou `DISCARD`.

Resultados duplicados da mesma tentativa são tratados como a mesma execução; nova execução exige novo `ATTEMPT_ID`.

## 8. Waves, DAG e ready queue

Cada wave executável possui `SYSTEM/WAVES/W###.json`. O manifest registra base state/commit, tarefas, tentativas, dependências e status.

O Orchestrator deve maximizar paralelismo pelo DAG:

- tarefa sem dependência pendente => `READY`;
- dependência concluída pode liberar dependente imediatamente;
- micro-fan-ins são permitidos; não é preciso esperar a wave inteira;
- ciclo de dependência é inválido;
- uma task pode ter múltiplas tentativas, mas apenas uma tentativa aceita é integrada.

## 9. Checkpoints e recovery

A cada mudança de `STATE_VERSION`:

1. incremente exatamente em 1;
2. atualize `SYSTEM/STATE.md`;
3. crie `SYSTEM/CHECKPOINTS/STATE-v####.md` com conteúdo byte-a-byte equivalente ao novo `STATE.md`;
4. não altere checkpoints antigos.

O último checkpoint no `main` é recovery point. Tags Git `state-v####` são recomendadas quando operacionalmente disponíveis, mas o checkpoint no repositório é obrigatório.

## 10. Decisões

Status: `PROPOSED | LOCKED | SUPERSEDED | REOPENED | REJECTED`.

Para reabrir decisão `LOCKED`, use `DECISION_REVIEW` explícita com trigger, evidência, impacto e recomendação.

## 11. Rotação de chat

A rotação é preventiva:

- Orchestrator: após 6–8 waves por padrão;
- Worker: por tarefa/tentativa grande;
- Synthesizer/Critic/Auditor: após 8–10 waves.

Na rotação do Orchestrator, o antigo gera HANDOFF e transfere/revoga o lease; o novo só integra após claim atômico e `CONTINUITY_CHECK: PASS`.

## 12. Continuity Check

```text
CONTINUITY_CHECK
protocol_version: ...
state_version: ...
main_commit_sha: ...
current_phase: ...
last_committed_wave: ...
role: ...
task_id: ...
attempt_id: ...
orchestrator_lease: ...
locked_decisions_seen: ...
open_blockers_seen: ...
status: PASS | FAIL
```

`FAIL` impede execução/integração até recarregar as fontes canônicas.

## 13. Qualidade

Toda conclusão relevante deve informar confiança e separar fato verificado, inferência, hipótese e recomendação. Pesquisa externa deve registrar fonte e data quando possível.

## 14. Critério de encerramento do projeto

O projeto termina somente quando todos os gates obrigatórios aplicáveis estiverem `PASS`, blockers críticos estiverem fechados, Red Team não tiver objeção crítica sem resposta, deliverable estiver validado contra o objetivo e `STATE.md` registrar `PROJECT_STATUS: COMPLETE`.

## 15. Alteração deste protocolo

Mudanças nesta Constituição exigem:

- incremento de `PROTOCOL_VERSION`;
- decisão explícita registrada em `DECISIONS.md`;
- justificativa;
- atualização de `AGENTS.md` quando o comportamento dos agentes mudar;
- nenhum código/produto misturado no mesmo PR de alteração do protocolo.

## 16. Enforcement no repositório

- `.github/workflows/system-integrity.yml` executa validação estática e diferencial.
- `scripts/validate_system.py` valida invariantes, checkpoints, manifests e mudanças contra a base do PR.
- `.github/CODEOWNERS` identifica governança.
- Mudanças no protocolo não podem ser misturadas com mudanças de produto.
- `main` deve exigir `validate-canonical-system`, PR, bloqueio de force-push e deleção.
- Falha de check preserva o estado anterior no `main` como recovery point.
