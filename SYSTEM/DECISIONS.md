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

## Próximo ID disponível

`D-0015`
