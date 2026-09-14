# DECISION LOG

Somente o Orchestrator pode alterar este arquivo.

## D-0001 — GitHub como fonte canônica

- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: o GitHub é a fonte de verdade do projeto. Histórico/memória de chats não garante continuidade.
- Motivo: permitir rotação de chats e recuperação determinística.

## D-0002 — Escrita exclusiva do Orchestrator

- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: somente o Orchestrator atualiza `STATE.md`, `ROADMAP.md`, `DECISIONS.md` e `TASK_LEDGER.md`.
- Motivo: impedir race conditions entre chats paralelos.

## D-0003 — Waves paralelas versionadas

- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: toda tarefa recebe `TASK_ID` e `BASE_STATE_VERSION`; tarefas independentes devem ser executadas em paralelo.
- Motivo: maximizar velocidade preservando rastreabilidade e detecção de staleness.

## D-0004 — Guardrails executáveis no repositório

- Status: `LOCKED`
- Estado de origem: `STATE-v0003`
- Decisão: o sistema canônico terá validação automática por GitHub Actions, ownership explícito dos arquivos de governança e política de mudança via branch + Pull Request. O `main` deve exigir o check de integridade e bloquear force-push/deleção.
- Motivo: transformar continuidade e integridade de regras informais em controles verificáveis e impedir drift acidental do protocolo.

## Próximo ID disponível

`D-0005`
