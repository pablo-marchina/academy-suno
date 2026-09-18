# Academy Suno

Repositório canônico para o desenvolvimento do case Academy Suno.

A solução é construída com múltiplos workers coordenados por estado versionado no GitHub. Continuidade e claims de evidência devem vir dos artefatos persistidos no repositório, não da memória de um chat.

## Clean start

Pré-requisito: Python 3.11+.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --disable-pip-version-check --no-cache-dir \
  'pydantic==2.13.4' 'pytest==9.0.2'
python experiments/foundation_regression/run_foundation_regression.py
python scripts/release_smoke/run_release_smoke.py \
  --workdir /tmp/academy-suno-release-smoke \
  --output /tmp/academy-suno-release-smoke/manifest.json
```

O release smoke regenera o proof mecânico W003, renderiza o evidence cockpit a partir da mesma linhagem persistida e reexecuta o bakeoff W004 de parser/source-trust. O manifesto deve terminar com `"status": "PASS"`. O HTML do cockpit fica em `/tmp/academy-suno-release-smoke/evidence-cockpit.html`.

Esse PASS é um **smoke de reprodutibilidade e invariantes**, não aprovação de produção.

## Arquitetura executável

```text
source + provenance
        |
        v
3 audiences x 3 formats
        |
        v
hard source/factual/policy gates + audience diagnostics
        |
        +--> targeted repair --> fresh re-evaluation
        |
        v
persistent RunStore + telemetry
        |
        v
evidence cockpit
        |
        v
release packet / demo / final review
```

A prova controlada existente usa `MECHANICS_ONLY` + `deterministic_stub` para demonstrar fan-out 3×3, retry, FAIL→repair→PASS, resume e auditabilidade. Ela não é evidência de qualidade de um provider real.

## Postura de evidência

Os artefatos de release e demo devem manter as categorias abaixo separadas:

| Estado | Significado no projeto |
|---|---|
| `PROVEN` | comportamento observado e reproduzido dentro do escopo declarado do artefato |
| `DIAGNOSTIC_ONLY` | sinal útil para diagnóstico; insuficiente para freeze/claim final |
| `PRODUCTION_UNKNOWN` | não observado de forma válida em execução real de produção/provider |
| `BLOCKED` | evidência depende de ação externa ainda ausente |
| `PENDING` | etapa downstream ainda não executada/concluída |

Postura atual que o README deliberadamente não promove:

- mechanics end-to-end, hard-gate non-compensation, RunStore/repair lineage e cockpit: `PROVEN` no escopo controlado;
- audience thresholds: `DIAGNOSTIC_ONLY` até duas streams humanas cegas, independentes e válidas produzirem agreement/adjudication;
- confusion matrices observadas: `PENDING` e atualmente bloqueadas por human gold independente;
- real provider/model quality, latency, usage e cost: `PRODUCTION_UNKNOWN`; execução credenciada segue `BLOCKED`;
- parser behavior/source-trust nas fixtures atuais: `PROVEN` nesse corpus; identidade de implementação/parser winner continua `PENDING`/unlocked;
- production/release readiness: `PENDING` do fan-in W004-T008 + final review. W004-T011 não substitui esse gate.

Detalhes e placeholders finais: [evidence packet](docs/release/EVIDENCE_PACKET.md), [submission checklist](docs/release/FINAL_REVIEW_CHECKLIST.md) e [demo <=5:00](docs/demo/DEMO_SCRIPT.md).

## Comece aqui

1. Leia [`START_HERE.md`](START_HERE.md).
2. Todo chat deve obedecer [`AGENTS.md`](AGENTS.md).
3. O estado oficial está em [`SYSTEM/STATE.md`](SYSTEM/STATE.md).
4. As regras permanentes estão em [`SYSTEM/CONSTITUTION.md`](SYSTEM/CONSTITUTION.md).
5. As fases e gates estão em [`SYSTEM/ROADMAP.md`](SYSTEM/ROADMAP.md).

## Control plane

| Arquivo | Função |
|---|---|
| `SYSTEM/CONSTITUTION.md` | protocolo, autoridade, concorrência, rotação e recovery |
| `SYSTEM/STATE.md` | ponto exato atual e próxima ação |
| `SYSTEM/ROADMAP.md` | fases e critérios de passagem |
| `SYSTEM/DECISIONS.md` | decisões versionadas e protegidas contra drift |
| `SYSTEM/TASK_LEDGER.md` | índice canônico de tasks/waves |
| `SYSTEM/KNOWLEDGE_INDEX.md` | evidências e conhecimento consolidado |
| `SYSTEM/AGENT_ROLES.md` | papéis e prompts-base dos chats |
| `SYSTEM/TEMPLATES.md` | Task, Result, Wave, Handoff, Audit e Decision Review |

## Modelo de execução

```text
STATE vN
   ↓
Orchestrator cria DAG + Wave
   ↓
┌────────┬────────┬────────┬────────┐
│Worker A│Worker B│Worker C│Worker D│  ← paralelo
└────────┴────────┴────────┴────────┘
   ↓
Synthesis → Red Team → Audit
   ↓
Orchestrator integra
   ↓
STATE vN+1
```

GitHub Issues são a fila operacional de tarefas. Workers entregam resultados na Issue ou em artefatos isolados; somente o Orchestrator modifica os arquivos canônicos.

## Princípio de continuidade

Qualquer chat pode ser descartado e recriado. O novo chat lê os arquivos canônicos, executa `CONTINUITY_CHECK` e retoma do último `STATE_VERSION` comprometido.
