# DECISION LOG

Somente o Orchestrator com lease ativo pode alterar este arquivo.

## D-0001 — GitHub como fonte canônica
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: GitHub é fonte de verdade.

## D-0002 — Escrita exclusiva do Orchestrator
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: workers não atualizam canônicos.

## D-0003 — Waves paralelas versionadas
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: tarefas independentes são paralelizadas com base explícita.

## D-0004 — Guardrails executáveis
- Status: `LOCKED`
- Estado de origem: `STATE-v0003`
- Decisão: CI/ownership/PR protegem governança.

## D-0005 — Lease atômico exclusivo
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: somente holder do lease integra estado.

## D-0006 — Proveniência por tentativa
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: toda execução usa TASK+ATTEMPT+BASE_STATE+BASE_COMMIT.

## D-0007 — Checkpoints e DAG
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: mudanças de estado têm snapshot; waves têm DAG.

## D-0008 — Qualidade do case como função única
- Status: `SUPERSEDED`
- Estado de origem: `STATE-v0005`
- Superseded by: `D-0012`.

## D-0009 — Loop obrigatório
- Status: `LOCKED`
- Estado de origem: `STATE-v0005`
- Decisão: projeto itera até hard gates/stop condition.

## D-0010 — Partner Value como função primária isolada
- Status: `SUPERSEDED`
- Estado de origem: `STATE-v0006`
- Superseded by: `D-0012`.

## D-0011 — Partner Contract/Jury/Adoption Gate
- Status: `LOCKED`
- Estado de origem: `STATE-v0006`
- Decisão: utilidade real, adoção e counterfactuals são obrigatórios.

## D-0012 — Balanced Total Success é a função objetivo dominante
- Status: `LOCKED`
- Estado de origem: `STATE-v0007`
- Decisão: sucesso é multiobjetivo com hard gates: Partner Outcome, fit ao briefing/avaliação, evidência/rigor, solução/diferenciação, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução. Nenhum score alto compensa hard gate crítico.
- Motivo: a melhor entrega resulta da combinação, não de otimizar uma dimensão isolada.

## D-0013 — Traceability e critical assumptions são gates
- Status: `LOCKED`
- Estado de origem: `STATE-v0007`
- Decisão: requisito/pain/claim material deve ser rastreável até evidência/solução/métrica/artefato; premissa high-impact/high-uncertainty precisa ser validada ou controlada.

## D-0014 — Blind Final Review e deadline reserve são obrigatórios
- Status: `LOCKED`
- Estado de origem: `STATE-v0007`
- Decisão: material final é avaliado sem contexto interno e o scheduler reserva tempo para integração, QA, defesa e submissão.

## D-0015 — Lifecycle de worker é observável por sinais duráveis
- Status: `LOCKED`
- Estado de origem: `STATE-v0010`
- Decisão: toda tentativa de worker despachada em protocolo 1.6.0+ registra `TASK_STARTED` antes do trabalho substantivo e exatamente um terminal `TASK_COMPLETE`, `TASK_BLOCKED` ou `TASK_STALE` na Issue; `TASK_PROGRESS` é opcional em marcos materiais. O Orchestrator deriva runtime status dos sinais + artefatos, e somente ele atualiza status canônico.
- Motivo: eliminar a dependência do usuário para informar se chats foram abertos/terminaram e distinguir `READY` de `RUNNING` sem depender da memória da conversa.
- Guardrail: não usar heartbeat periódico/TTL como prova de liveness; chats não são processos confiáveis em background. Branch/commits/results são evidência secundária e attempts novos nunca são reutilizados.

## Próximo ID disponível

`D-0016`
