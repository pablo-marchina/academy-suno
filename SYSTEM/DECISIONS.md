# DECISION LOG

Somente o Orchestrator com lease ativo pode alterar este arquivo.

## D-0001 — GitHub como fonte canônica
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: GitHub é fonte de verdade; memória de chat não garante continuidade.

## D-0002 — Escrita exclusiva do Orchestrator
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: workers não atualizam arquivos canônicos.

## D-0003 — Waves paralelas versionadas
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: tarefas independentes são paralelizadas com identidade/base explícitas.

## D-0004 — Guardrails executáveis
- Status: `LOCKED`
- Estado de origem: `STATE-v0003`
- Decisão: validação automática, ownership e PR obrigatório para governança.

## D-0005 — Lease atômico exclusivo
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: somente holder do lease pode integrar estado.

## D-0006 — Proveniência por tentativa
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: toda execução usa `TASK_ID + ATTEMPT_ID + BASE_STATE_VERSION + BASE_COMMIT_SHA`.

## D-0007 — Checkpoints e DAG
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: cada mudança cria snapshot; waves têm DAG/ready queue.

## D-0008 — Função objetivo de qualidade do case
- Status: `SUPERSEDED`
- Estado de origem: `STATE-v0005`
- Decisão anterior: maximizar qualidade esperada segundo avaliação.
- Superseded by: `D-0010` — Partner Value passa a ser objetivo primário; qualidade da avaliação vira constraint/secondary objective.

## D-0009 — Quality loop obrigatório
- Status: `LOCKED`
- Estado de origem: `STATE-v0005`
- Decisão: projeto não termina por task/wave; itera até hard gates/stop condition.

## D-0010 — Partner Value é a função objetivo primária
- Status: `LOCKED`
- Estado de origem: `STATE-v0006`
- Decisão: maximizar valor real esperado para o parceiro, resolvendo a dor correta, prevalece sobre otimizar score, sofisticação, estética ou velocidade. Critérios do case continuam obrigatórios como constraints.
- Motivo: o sucesso real é ajudar o parceiro; uma solução que performa bem na apresentação mas entrega menos valor é subótima.

## D-0011 — Partner Contract, Partner Jury e Adoption Gate são obrigatórios
- Status: `LOCKED`
- Estado de origem: `STATE-v0006`
- Decisão: antes da finalização, dor/causa/status quo/outcome/restrições/adoção devem ser evidenciados; solução deve passar Partner Jury e possuir caminho acionável de implementação/adoção.
- Motivo: impedir solutionism e garantir que a recomendação seja utilizável no mundo real.

## Próximo ID disponível

`D-0012`
