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

## D-0016 — Foundation invariants lockados; implementação permanece evidence-driven
- Status: `LOCKED`
- Estado de origem: `STATE-v0016`
- Decisão: ficam lockados os invariantes comprovados em W002 — typed Python + Pydantic v2 nas fronteiras persistidas, canonical source/provenance spine, source-trust antes de generation, semantic table-role provenance para fatos de tabela, factual/policy/source hard gates não compensatórios, 3 audiências × 3 formatos nativos, branch identity/job_id estáveis, repair local e semantic/LLM judge apenas como sensor secundário. Plain async é o líder provisório por runtime evidence; LangGraph permanece challenger até runtime recheck. Parser library, provider/model, semantic backend e audience thresholds continuam desbloqueados até evidência específica.
- Motivo: W002-T010 reconciliou EXP-A/B/C e separou `foundation proven`, `pending experiment` e `production unknown`, evitando locks por preferência.
- Guardrail: qualquer mudança nesses invariantes exige evidência material de ganho e não pode enfraquecer `CRIT-001`.

## D-0017 — Waiver explícito para calibração automatizada cega em W004
- Status: `LOCKED`
- Estado de origem: `STATE-v0034`
- Tipo: `EVIDENCE_SUBSTITUTION_WAIVER`
- Autorização: operador autorizou explicitamente substituir o blocker de duas streams humanas pela validação automatizada cega completa e continuar o Autopilot.
- Evidência aceita: `artifacts/evals/w004/model_validation_a03.jsonl` + provenance/summary, Actions run `35668224695`, 36/36 itens únicos, `MODEL_AUTOMATED`, Groq `openai/gpt-oss-120b`, blind leakage guardrails PASS, fresh-clone byte identity PASS, output SHA-256 `adae7376415cd7052b8b2b84002ce0a7a5890047cb86e98dbe456747c7fe1bb4`.
- Decisão: para o escopo `W004-T005 → W004-T006/W004-T007 → W004-T008`, a evidência A03 pode satisfazer a dependência de calibração que originalmente exigia human gold, desde que todos os artifacts/results downstream preservem a classe `MODEL_AUTOMATED_BLIND_CALIBRATION` e suas limitações.
- Claims proibidos: não declarar human gold, human agreement, human preference, audience validation por humanos, produção validada por humanos ou equivalentes. `human_gold_eligible=false` continua verdadeiro.
- Thresholds: audience thresholds permanecem `DIAGNOSTIC_ONLY`; nenhum threshold de produção pode ser lockado com A03 sozinho.
- T006: semantic-off/on pode usar A03 como reference calibration set para ablation diagnóstica, preservando hard gates; backend preference só pode ser lockada se o ganho for reprodutível no escopo automatizado e descrito como tal, nunca como preferência humana.
- T007: provider/model quality comparison pode usar source-grounded checks + A03 para comparação automatizada cega, junto de mechanics/custo/latência observados; qualquer winner/preference deve ser qualificado como `AUTOMATED_EVIDENCE_ONLY` e somente se datasets/configs forem comparáveis.
- Completion posture: a ausência de duas anotações humanas deixa de ser hard blocker deste case e passa a risco residual controlado, desde que os scorecards/risks preservem a limitação e nenhum claim final dependa de human agreement. Uma amostra humana futura é melhoria opcional, não dependência de execução.
- Motivo: o gate humano bloqueava todo o critical path apesar de existir uma avaliação cega completa, rastreável e reproduzível; o operador escolheu explicitamente a troca entre velocidade/autonomia e força da evidência. O waiver mantém integridade sem fabricar humanos.

## D-0018 — Production-grade Autopilot + systematic Decision Research Gate
- Status: `LOCKED`
- Estado de origem: `STATE-v0040`
- Tipo: `OPERATOR_SCOPE_EXPANSION`
- Autorização: o operador solicitou explicitamente elevar o projeto de case/demo-grade para a melhor entrega possível orientada a produção, com múltiplos usuários, quantitativo-first, Eval-Driven Development, adaptação onde segura, máxima visualização live no frontend e pesquisa sistemática/data-driven para qualquer escolha material.
- Decisão: introduzir `SYSTEM/PRODUCTION_CONTRACT.md` e `SYSTEM/DECISION_RESEARCH_GATE.md` como contratos obrigatórios do Autopilot. O W004 permanece evidência histórica válida do case, mas deixa de ser o target final de engenharia.
- Demo: “sem demo” é interpretado como “sem sistema fake/descartável exclusivo para demo”. O vídeo obrigatório do briefing continua <=5:00 e deve demonstrar o mesmo produto real.
- Research gate: nenhuma escolha material de stack/arquitetura/modelo/provider/parser/eval/auth/storage/deploy/observability/security pode virar production default/LOCKED sem pesquisa sistemática + alternatives + workload benchmark quando testável + limitations + reversal conditions.
- Quantitative-first: propriedades mensuráveis devem ser instrumentadas; thresholds não podem ser inventados. Hard gates não são compensatórios.
- Adaptive policy: adaptação é preferida para otimização (routing/model/prompt/retrieval/repair/budget/concurrency) somente quando telemetrada e incapaz de relaxar source/factual/policy/schema/provenance/authz/tenant hard gates.
- Multi-user: auth, tenant/workspace binding, RBAC/authz, shared durable state, secure uploads, observability, reliability e deployment evidence tornam-se hard requirements antes de qualquer `PRODUCTION_READY` claim.
- Calibration: D-0017 continua válido apenas para fechamento do W004. Para production audience thresholds/claims fortes, o novo Production Contract volta a exigir evidência humana independente ou evidence class equivalente explicitamente justificada sem falsificar human claims.
- Implementation posture: preservar componentes W001–W004 que passem DRG/benchmarks; reescrita por moda é proibida. Plain async atual é baseline obrigatório nos bakeoffs de orchestration.
- Next: abrir nova fase/wave de production research + architecture synthesis antes de congelar stack e depois desenvolver incrementalmente sob eval/regression gates.

## Próximo ID disponível

`D-0019`
