# Academy Suno

Repositório canônico do case Academy Suno e do ciclo de evolução para um produto real multiusuário, quantitativo/eval-driven, adaptativo onde seguro e observável ponta a ponta.

O GitHub é a fonte de verdade. Continuidade, decisões e claims de evidência vêm dos artefatos persistidos no repositório — não da memória de um chat.

## Estado atual

- protocolo: `1.8.0`;
- fase canônica: `8 — Production Scope & Decision Research Foundation`;
- wave ativa: `W005`;
- `W005-T001..T009` + `W005-T013..T014`: onze pesquisas/bakeoffs independentes prontos para execução paralela;
- `W005-T010..T012`: síntese → red-team → fan-in, bloqueados pelas dependências;
- W004 permanece baseline/evidência histórica válida, não o target final de engenharia;
- nenhum frontend, API, auth, banco, storage, parser/document-AI, workflow framework, provider/model, developer toolchain, observability stack ou deployment target possui winner de produção antes do respectivo Decision Research Gate;
- `PRODUCTION_READY` **não** é alegado neste ponto.

Leia primeiro:

1. [`START_HERE.md`](START_HERE.md)
2. [`AGENTS.md`](AGENTS.md)
3. [`SYSTEM/STATE.md`](SYSTEM/STATE.md)
4. [`SYSTEM/PRODUCTION_CONTRACT.md`](SYSTEM/PRODUCTION_CONTRACT.md)
5. [`SYSTEM/DECISION_RESEARCH_GATE.md`](SYSTEM/DECISION_RESEARCH_GATE.md)
6. [`SYSTEM/ROADMAP.md`](SYSTEM/ROADMAP.md)

## O que estamos construindo

O target final é um único produto real — não uma aplicação descartável para demo — capaz de:

```text
real user / workspace / tenant
        |
        v
secure text/PDF ingest + source provenance
        |
        v
stateful 3 audiences x 3 native formats
        |
        v
real provider/model path
        |
        v
hard source/factual/policy/schema/tenant gates
        |
        +--> targeted repair --> fresh evaluation
        |
        v
quantitative eval + experiment telemetry
        |
        v
shared durable persistence + audit trail
        |
        v
live Evidence Cockpit
(graph + source + 3x3 + eval + repair + traces + cost/latency/reliability)
```

Adaptação pode otimizar escolhas suaves como model/provider/prompt/retrieval/repair budget, mas nunca pode relaxar hard gates de factualidade, source trust, policy, schema ou isolamento entre tenants.

## Production Contract

`SYSTEM/PRODUCTION_CONTRACT.md` define os hard gates `PROD-001..017`, incluindo:

- identidade, organizações/workspaces, authn/authz e isolamento multi-tenant;
- API pública tipada, idempotência, limites e backpressure;
- persistência compartilhada e durável — SQLite/local não pode ser source of truth de produção;
- upload/document ingestion seguro, sem arbitrary server filesystem path;
- provider real conectado ao fluxo do usuário e aos nove outputs;
- workflow durável, resume/recovery e repair local;
- eval híbrido com hard gates determinísticos/source-grounded e sensores semânticos secundários;
- calibração humana de audiência para claims de produção, quando disponível;
- Eval-Driven Development offline/CI/online;
- runtime adaptativo com política versionada e rollback;
- Evidence Cockpit e arquitetura vivos no frontend;
- capacidade/reliability medidas, não inventadas;
- segurança, observabilidade, deploy, rollback, migrations e backup/restore.

## Decision Research Gate

Toda escolha material passa por `SYSTEM/DECISION_RESEARCH_GATE.md` antes de ser promovida a decisão de produção.

O processo exige, quando aplicável:

- problema/hipótese explícitos;
- baseline atual como counterfactual;
- pelo menos 3 alternativas materialmente diferentes quando existirem;
- documentação primária, standards/papers e fontes independentes relevantes;
- critérios/weights definidos antes de observar o resultado;
- benchmark reproduzível no workload do projeto quando a decisão for testável;
- métricas quantitativas, variância/percentis e custo/latência/reliability quando pertinentes;
- conclusão `LOCK`, `NO_PREFERENCE` ou `PENDING_EVIDENCE`;
- reversal conditions e evidence saturation stopping rule.

Consenso entre agentes não conta como evidência.

## Começar o Autopilot agora

A fila inicial da W005 é deliberadamente paralela. Abra workers independentes com:

```text
Execute o dispatch W005-T001-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T002-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T003-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T004-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T005-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T006-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T007-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T008-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T009-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T013-A01 do repositório pablo-marchina/academy-suno.
Execute o dispatch W005-T014-A01 do repositório pablo-marchina/academy-suno.
```

Cada worker deve executar `CONTINUITY_CHECK`, usar sua branch `worker/<TASK_ID>-<ATTEMPT_ID>`, emitir `TASK_STARTED`, persistir `SYSTEM/RESULTS/<TASK_ID>-<ATTEMPT_ID>.md` e emitir exatamente um terminal conforme `SYSTEM/TASK_SIGNALS.md`.

T010 só é liberada após os onze inputs de pesquisa/bakeoff serem aceitos; T011 faz red-team independente; T012 produz o DAG evidence-backed das waves de implementação.

As duas áreas adicionadas na revisão de readiness são deliberadas: T013 cobre developer platform/repo/package management/CI/CD e T014 cobre parsing/extraction/source-grounding de documentos financeiros. Sem essas pesquisas, T010 teria de inventar decisões materiais que a regra do projeto exige pesquisar sistematicamente.

## O que já foi provado em W004

W004 continua sendo o baseline técnico e counterfactual obrigatório quando aplicável:

- exact 3×3 fan-out + state + targeted repair + lossless join;
- factual/source/policy hard-gate non-compensation;
- RunStore/checkpoint/repair lineage no escopo controlado;
- ingest text/PDF fail-closed e recipient-facing app no escopo do case;
- provider mechanics reais observadas e comparação bounded de modelos, **sem winner global de produção**;
- `MODEL_AUTOMATED_BLIND_CALIBRATION` 36/36 aceita somente sob D-0017, **sem human-gold claim**;
- clean-E2E source→9→eval→repair→aggregate 9/9 no escopo W004;
- vídeo real browser-captured de 69.12 s, revisado e preservado.

Essas evidências não autorizam inferir multi-user readiness, production deployment, human-calibrated audience thresholds ou capacidade operacional real.

## Evidence posture

| Estado | Significado |
|---|---|
| `PROVEN` | comportamento observado/reproduzido no escopo declarado |
| `DIAGNOSTIC_ONLY` | diagnóstico útil, insuficiente para freeze/claim de produção |
| `MODEL_AUTOMATED_BLIND_CALIBRATION` | calibração automatizada cega; não é human gold |
| `PENDING_EVIDENCE` | decisão/claim aguarda evidência definida |
| `NO_PREFERENCE` | evidência atual não justifica winner |
| `OPEN_P0/P1` | production hard gate/risco ainda aberto |

Fatos atuais importantes:

- audience thresholds continuam `DIAGNOSTIC_ONLY` para produção;
- human gold/agreement/preference permanecem não observados;
- provider/model de produção permanece sem winner;
- current recipient UI é baseline W004, não o frontend final live;
- identidade/tenancy/authz/shared persistence/secure upload/reliability/deployment ainda precisam de evidência de produção;
- parser/document-intelligence e developer-platform/toolchain também permanecem unlocked até W005;
- deadline/submission mechanism e owner/workflow interno Suno continuam unknown externos.

## Reproduzir o baseline W004

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

O smoke deve terminar com `"status": "PASS"`. Isso prova reprodutibilidade/invariantes do baseline, não produção.

O recipient app histórico W004 pode ser executado com:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --disable-pip-version-check --no-cache-dir \
  'pydantic==2.13.4' 'pypdf==5.9.0'
PYTHONPATH=src python app/recipient/server.py --host 127.0.0.1 --port 8765
```

A produção ainda não possui manifest/toolchain definitivo de dependências porque essa escolha é material e permanece submetida à W005/DRG; não crie um lock tecnológico por conveniência antes da síntese T010/T012.

## Control plane

| Arquivo | Função |
|---|---|
| `SYSTEM/CONSTITUTION.md` | protocolo e invariantes |
| `SYSTEM/STATE.md` | ponto canônico atual e próxima ação |
| `SYSTEM/PRODUCTION_CONTRACT.md` | hard gates de produção |
| `SYSTEM/DECISION_RESEARCH_GATE.md` | pesquisa/benchmark obrigatório para decisões materiais |
| `SYSTEM/SUCCESS_MODEL.md` | função objetivo e hard gates globais |
| `SYSTEM/ROADMAP.md` | fases e critérios de passagem |
| `SYSTEM/DECISIONS.md` | decisões versionadas e protegidas contra drift |
| `SYSTEM/TASK_LEDGER.md` | índice de tasks/attempts/status |
| `SYSTEM/WAVES/W005.json` | DAG/ready queue corrente |
| `SYSTEM/TRACEABILITY_MATRIX.md` | requisito→evidência→solução→métrica→artefato |
| `SYSTEM/ASSUMPTION_RISK_REGISTER.md` | assumptions/risks e mitigação |
| `SYSTEM/KNOWLEDGE_INDEX.md` | conhecimento/evidence registry consolidado |

## Continuidade

Qualquer chat pode ser descartado e recriado. O sucessor lê os canônicos, verifica o lease quando for Orchestrator, executa `CONTINUITY_CHECK` e retoma do último `STATE_VERSION` comprometido.
