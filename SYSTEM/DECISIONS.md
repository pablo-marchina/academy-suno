# DECISION LOG

Somente o Orchestrator com lease ativo pode alterar este arquivo.

## D-0001 — GitHub como fonte canônica

- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: o GitHub é a fonte de verdade do projeto. Histórico/memória de chats não garante continuidade.
- Motivo: permitir rotação de chats e recuperação determinística.

## D-0002 — Escrita exclusiva do Orchestrator

- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: workers não atualizam arquivos canônicos; integração é responsabilidade exclusiva do Orchestrator autorizado.
- Motivo: impedir race conditions entre chats paralelos.

## D-0003 — Waves paralelas versionadas

- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: tarefas independentes devem ser executadas em paralelo com identidade/base explícitas.
- Motivo: maximizar velocidade preservando rastreabilidade e detecção de staleness.

## D-0004 — Guardrails executáveis no repositório

- Status: `LOCKED`
- Estado de origem: `STATE-v0003`
- Decisão: o sistema canônico terá validação automática por GitHub Actions, ownership explícito e política de mudança via branch + Pull Request. O `main` deve exigir o check de integridade e bloquear force-push/deleção.
- Motivo: transformar continuidade e integridade em controles verificáveis.

## D-0005 — Lease atômico exclusivo do Orchestrator

- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: somente o holder do lease dinâmico na branch `control/orchestrator-lease` pode integrar estado canônico. Claim/handoff usa update baseado no blob SHA observado; conflito exige reload/abort.
- Motivo: impedir dois chats Orchestrator de possuírem autoridade simultânea sem depender de memória ou coordenação informal.

## D-0006 — Proveniência e idempotência por tentativa

- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: toda execução de worker usa `TASK_ID + ATTEMPT_ID + BASE_STATE_VERSION + BASE_COMMIT_SHA`; novas execuções recebem novo `ATTEMPT_ID`.
- Motivo: distinguir reexecuções, detectar trabalho stale e impedir integração duplicada.

## D-0007 — Checkpoints imutáveis e DAG executável

- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: cada mudança de estado cria snapshot imutável; waves são descritas por manifests JSON com dependências explícitas e ready queue liberada por DAG.
- Motivo: permitir recovery exato e maximizar paralelismo sem esperar barreiras artificiais de rodada.

## Próximo ID disponível

`D-0008`
