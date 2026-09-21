# Academy Suno

Repositório canônico para o desenvolvimento do case Academy Suno.

A solução é construída com múltiplos workers coordenados por estado versionado no GitHub. Continuidade e claims de evidência devem vir dos artefatos persistidos no repositório, não da memória de um chat.

## Evaluator quick start — recipient app

Pré-requisito: Python 3.11+.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --disable-pip-version-check --no-cache-dir \
  'pydantic==2.13.4' 'pypdf==5.9.0'
PYTHONPATH=src python app/recipient/server.py --host 127.0.0.1 --port 8765
```

Abra `http://127.0.0.1:8765`. O app recipient-facing aceita texto colado ou PDF, mostra provenance/source trust, o fan-out 3×3, evidência persistida de repair e os non-claims no mesmo fluxo.

A captura final da task `W004-T019-A01` foi produzida em browser real no GitHub Actions run `35636285651`, a partir do commit `ffaa235e31667d1aab9a1f24253e647579e394e1`. O MP4 exportado (`final-demo.mp4`) mede `69.12 s`, H.264 `1280×720` a `25 fps`, sem áudio, com SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`. O artefato imutável é `w004-t019-final-demo-ffaa235e31667d1aab9a1f24253e647579e394e1`, ID `10656720873`, digest ZIP `sha256:7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`. Detalhes e boundaries: [`docs/demo/final/README.md`](docs/demo/final/README.md) e [`artifacts/demo_final/W004-T019-A01-ci-evidence.json`](artifacts/demo_final/W004-T019-A01-ci-evidence.json).

Essa captura fecha evidência da task para app/ingest/demonstração e duração; ela **não** é human calibration, evidência de qualidade de provider nem aprovação de produção. O BCB PDF real aparece deliberadamente como negative-control fail-closed (`SOURCE_BLOCKED / REVIEW_REQUIRED / LOW`) quando a provenance de papéis de tabela permanece ambígua.

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
- recipient-facing text/PDF ingest e demonstração browser-real de T019: `PROVEN` no escopo da task; a captura mede `69.12 s` e preserva source-trust fail-closed;
- audience thresholds: `DIAGNOSTIC_ONLY` até duas streams humanas cegas, independentes e válidas produzirem agreement/adjudication;
- confusion matrices observadas: `PENDING` e atualmente bloqueadas por human gold independente;
- real provider/model quality, latency, usage e cost: `PRODUCTION_UNKNOWN`; execução credenciada segue `BLOCKED`;
- parser behavior/source-trust nas fixtures atuais: `PROVEN` nesse corpus; identidade de implementação/parser winner continua `PENDING`/unlocked;
- production/release readiness: `PENDING` do fan-in W004-T008 + final review; T019 não substitui esse gate.

Detalhes e placeholders finais: [evidence packet](docs/release/EVIDENCE_PACKET.md), [submission checklist](docs/release/FINAL_REVIEW_CHECKLIST.md), [submission packet](docs/submission/SUBMISSION_PACKET.md) e [final paced demo](docs/demo/final/README.md).

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
