# TASK SIGNALS — Worker Lifecycle Protocol

`TASK_SIGNALS_VERSION: 1.0`

## Purpose

Permitir que o Orchestrator reconstrua o estado real de cada tentativa diretamente do GitHub, sem depender de memória do chat nem de adivinhar se um worker foi aberto.

Os sinais são **telemetria operacional não canônica**. Workers escrevem sinais apenas como comentários na Issue da própria task; somente o Orchestrator continua autorizado a alterar `STATE`, `TASK_LEDGER`, manifests de wave e demais arquivos canônicos.

## Required lifecycle

Toda tentativa despachada a partir de `PROTOCOL_VERSION 1.6.0` segue:

```text
READY
  ↓
TASK_STARTED
  ↓
TASK_PROGRESS (0..N, somente em marcos materiais)
  ↓
TASK_COMPLETE | TASK_BLOCKED | TASK_STALE
```

`TASK_STARTED` é obrigatório e deve ser persistido **depois do CONTINUITY_CHECK e da criação/seleção da branch isolada, mas antes do trabalho substantivo**.

`TASK_PROGRESS` não é um heartbeat periódico. É opcional e deve ser emitido apenas quando um marco material foi alcançado ou quando uma execução longa precisa tornar progresso observável.

Um sinal terminal é obrigatório antes de o worker encerrar sua execução.

## Signal transport

Transporte primário: comentário na GitHub Issue da task.

O timestamp do comentário do GitHub é a referência temporal; o worker não precisa inventar horário próprio.

Branch, commits, PRs e presença de `SYSTEM/RESULTS/<TASK_ID>-<ATTEMPT_ID>.md` são evidência secundária para recuperação/auditoria, mas não substituem o sinal obrigatório em novas tentativas.

## Signal schema

### TASK_STARTED

```text
TASK_SIGNAL
TYPE: TASK_STARTED
TASK_ID: W###-T###
ATTEMPT_ID: A##
BASE_STATE_VERSION: ####
BASE_COMMIT_SHA: <40 hex>
OBSERVED_MAIN_SHA: <40 hex>
WORKER_BRANCH: worker/<TASK_ID>-<ATTEMPT_ID>
CONTINUITY_CHECK: PASS
```

### TASK_PROGRESS

```text
TASK_SIGNAL
TYPE: TASK_PROGRESS
TASK_ID: ...
ATTEMPT_ID: ...
BASE_STATE_VERSION: ...
BASE_COMMIT_SHA: ...
WORKER_BRANCH: ...
MILESTONE: <curto e verificável>
ARTIFACT_REF: <opcional>
```

### TASK_COMPLETE

Persistir o RESULT antes do sinal terminal.

```text
TASK_SIGNAL
TYPE: TASK_COMPLETE
TASK_ID: ...
ATTEMPT_ID: ...
BASE_STATE_VERSION: ...
BASE_COMMIT_SHA: ...
WORKER_BRANCH: ...
RESULT_REF: SYSTEM/RESULTS/<TASK_ID>-<ATTEMPT_ID>.md
RESULT_COMMIT_SHA: <40 hex>
```

### TASK_BLOCKED

```text
TASK_SIGNAL
TYPE: TASK_BLOCKED
TASK_ID: ...
ATTEMPT_ID: ...
BASE_STATE_VERSION: ...
BASE_COMMIT_SHA: ...
WORKER_BRANCH: ...
BLOCKER: <o que impede conclusão>
NEEDS: <informação/ação necessária>
```

### TASK_STALE

```text
TASK_SIGNAL
TYPE: TASK_STALE
TASK_ID: ...
ATTEMPT_ID: ...
BASE_STATE_VERSION: ...
BASE_COMMIT_SHA: ...
WORKER_BRANCH: ...
REASON: <drift/provenance incompatível>
```

## Derived runtime status

O Orchestrator deriva status operacional; comentários de worker não alteram o ledger por si só.

| Evidence | Derived status |
|---|---|
| nenhum start válido e nenhum resultado | `READY` |
| `TASK_STARTED`/`TASK_PROGRESS`, sem terminal | `RUNNING` |
| `TASK_COMPLETE` + RESULT existente + provenance válida | `RESULT_RECEIVED` |
| `TASK_BLOCKED` | `BLOCKED` |
| `TASK_STALE` ou provenance inválida | `STALE` |
| resultado aceito e integrado pelo Orchestrator | `INTEGRATED` |

Se existir branch/RESULT sem sinal por uma tentativa criada antes de 1.6.0, o Orchestrator pode usar essa evidência como fallback legado. Para tentativas 1.6.0+, ausência de sinal é finding de protocolo.

## Recovery and uncertain liveness

Não existe TTL que prove que um chat continua vivo. Por isso:

- `RUNNING` significa **iniciado e sem terminal observado**, não garantia de processo ativo em background;
- o Orchestrator pode inspecionar branch/commits/result para detectar progresso não sinalizado;
- se uma tentativa iniciada ficar sem terminal e sem progresso observável em ciclos posteriores, o Orchestrator registra `LIVENESS_UNCERTAIN` como classificação operacional e pode abrir novo `ATTEMPT_ID` quando isso reduzir risco no critical path;
- retries nunca reutilizam o mesmo attempt; resultados concorrentes são comparados pelo Orchestrator e apenas um é aceito/integrado.

## Orchestrator polling/reconstruction

Em cada `Continue o Autopilot`, o Orchestrator deve:

1. ler Issues das tasks ativas;
2. localizar sinais válidos do `TASK_ID + ATTEMPT_ID` atual;
3. verificar branch/result refs quando necessário;
4. derivar runtime status;
5. validar provenance/staleness;
6. liberar dependentes assim que seus pré-requisitos aceitos estiverem satisfeitos;
7. persistir mudanças canônicas somente em integração/checkpoint apropriado.

## Safety rules

- worker nunca edita `TASK_LEDGER`, `STATE` ou wave manifest para dizer que começou/terminou;
- `TASK_COMPLETE` sem RESULT persistido não é conclusão válida;
- sinal com task/attempt/base divergente é ignorado e auditado;
- sinais não mudam a autoridade exclusiva do Orchestrator;
- nenhum heartbeat por relógio é exigido: chats não são processos confiáveis de background;
- progresso deve ser verificável e não texto cosmético.
